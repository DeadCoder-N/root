"""Flask Backend API for Command Injection Scanner"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanner import CommandInjectionScanner
from reports.pdf_generator import UniversalReportGenerator as CommandInjectionReportGenerator

app = Flask(__name__)
CORS(app)
scan_results_cache = {}

def calculate_risk_score(vulnerabilities):
    """Calculate risk score 0-100"""
    severity_scores = {'CRITICAL': 25, 'HIGH': 15, 'MEDIUM': 8, 'LOW': 3}
    return min(100, sum(severity_scores.get(v.get('severity', 'LOW'), 0) for v in vulnerabilities))

def get_risk_level(score):
    """Get risk level from score"""
    if score >= 75: return 'CRITICAL'
    elif score >= 50: return 'HIGH'
    elif score >= 25: return 'MEDIUM'
    else: return 'LOW'

def add_fix_prompts(vulnerabilities):
    """Add actionable fix prompts to vulnerabilities"""
    for vuln in vulnerabilities:
        vuln_type = vuln.get('type', '')
        
        if 'Command Injection' in vuln_type:
            vuln['fix_prompt'] = "Never pass user input to system commands. Use parameterized APIs. Whitelist allowed commands. Sanitize input: remove ;|&$(){}[]<>. Use subprocess with shell=False."
        elif 'Path Traversal' in vuln_type:
            vuln['fix_prompt'] = "Validate file paths. Use basename() to strip directory. Whitelist allowed files. Reject ../ sequences. Use realpath() to resolve paths. Store files outside web root."
        elif 'LFI' in vuln_type or 'Local File' in vuln_type:
            vuln['fix_prompt'] = "Never include files based on user input. Use whitelist of allowed files. Disable allow_url_include in PHP. Use static file paths."
        else:
            vuln['fix_prompt'] = f"Review and fix {vuln_type}. Check OWASP Command Injection Prevention Cheat Sheet."
    
    return vulnerabilities

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'Command Injection Scanner', 'port': 5017}), 200

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        
        if not data or 'target' not in data:
            return jsonify({'status': 'error', 'message': 'Missing required field: target'}), 400
        
        target_url = data.get('target')
        
        # Validate URL
        if not target_url.startswith(('http://', 'https://')):
            return jsonify({'status': 'error', 'message': 'Invalid URL format. Must start with http:// or https://'}), 400
        
        print(f"[*] Starting command injection scan for: {target_url}")
        
        scanner = CommandInjectionScanner(target_url)
        results = scanner.scan()
        
        # Add fix prompts and risk scoring
        results['vulnerabilities'] = add_fix_prompts(results['vulnerabilities'])
        results['risk_score'] = calculate_risk_score(results['vulnerabilities'])
        results['risk_level'] = get_risk_level(results['risk_score'])
        
        # Generate report ID
        from datetime import datetime
        report_id = f"cmdinj_{datetime.now().strftime('%d_%b_%Y_%I_%M_%p')}"
        scan_results_cache[report_id] = results
        
        print(f"[+] Scan completed. Found {results.get('vulnerability_count', 0)} vulnerabilities")
        
        return jsonify({
            'status': 'success',
            'report_id': report_id,
            'results': results
        }), 200
    
    except Exception as e:
        print(f"[!] Error during scan: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Scan failed: {str(e)}'
        }), 500

@app.route('/api/download/<report_id>', methods=['GET'])
def download_report(report_id):
    try:
        if report_id not in scan_results_cache:
            return jsonify({'status': 'error', 'message': 'Report not found'}), 404
        
        results = scan_results_cache[report_id]
        
        print(f"[*] Generating PDF report for: {report_id}")
        
        generator = CommandInjectionReportGenerator(results)
        pdf_path = generator.generate()
        
        print(f"[+] PDF generated: {pdf_path}")
        
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=generator.filename
        )
    except Exception as e:
        print(f"[!] Error generating report: {str(e)}")
        return jsonify({'status': 'error', 'message': f'Report generation failed: {str(e)}'}), 500

if __name__ == '__main__':
    print("="*60)
    print("💉 COMMAND INJECTION SCANNER - Starting Server")
    print("="*60)
    print("Port: 5017")
    print("Endpoints:")
    print("  - POST   /api/analyze        - Analyze for command injection")
    print("  - GET    /api/download/<id>  - Download PDF report")
    print("  - GET    /health             - Health check")
    print("="*60)
    print("\nServer running on http://localhost:5017")
    print("Press CTRL+C to stop\n")
    
    app.run(host='0.0.0.0', port=5017, debug=True)

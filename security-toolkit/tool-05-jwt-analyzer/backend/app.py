"""JWT Analyzer - Flask Backend"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from analyzer import JWTAnalyzer
from reports.pdf_generator import JWTReportGenerator


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

app = Flask(__name__)
CORS(app)

# Store scan results
scan_results_cache = {}

def add_fix_prompts(vulnerabilities):
    """Add actionable fix prompts to vulnerabilities"""
    for vuln in vulnerabilities:
        vuln_type = vuln.get('type', '')
        
        if 'Algorithm None' in vuln_type:
            vuln['fix_prompt'] = "Reject tokens with 'none' algorithm. Whitelist allowed algorithms (HS256, RS256, ES256). Never accept unsigned tokens."
        elif 'Weak Secret' in vuln_type:
            vuln['fix_prompt'] = "Generate strong secret: openssl rand -base64 32. Rotate immediately. Use minimum 256-bit secrets. Store in environment variables."
        elif 'Expiration' in vuln_type:
            vuln['fix_prompt'] = "Add 'exp' claim with 15-60 min lifetime for access tokens. Implement refresh tokens for longer sessions. Reject expired tokens."
        elif 'Algorithm Confusion' in vuln_type:
            vuln['fix_prompt'] = "Strictly validate algorithm. Never accept HS256 for RS256 tokens. Bind algorithm to key type. Use algorithm whitelist."
        elif 'Missing Signature' in vuln_type:
            vuln['fix_prompt'] = "All JWTs must be signed. Use HS256 (symmetric) or RS256 (asymmetric). Verify signature on every request."
        elif 'Sensitive Data' in vuln_type:
            vuln['fix_prompt'] = "Never store passwords, secrets, or PII in JWT payload. JWTs are base64-encoded, not encrypted. Use encrypted tokens if needed."
        elif 'Key ID' in vuln_type or 'kid' in vuln_type:
            vuln['fix_prompt'] = "Sanitize kid parameter. Use whitelist of allowed key IDs. Prevent path traversal and SQL injection in kid."
        else:
            vuln['fix_prompt'] = f"Review and fix {vuln_type}. Follow JWT best practices: jwt.io/introduction"
    
    return vulnerabilities

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "JWT Analyzer", "port": 5005}), 200

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        if not data or 'token' not in data:
            return jsonify({"status": "error", "message": "Missing token"}), 400
        
        print(f"[*] Analyzing JWT token...")
        analyzer = JWTAnalyzer(data['token'])
        results = analyzer.analyze()
        
        # Add fix prompts
        results['vulnerabilities'] = add_fix_prompts(results['vulnerabilities'])
        results['risk_score'] = calculate_risk_score(results['vulnerabilities'])
        results['risk_level'] = get_risk_level(results['risk_score'])
        
        # Generate report ID
        from datetime import datetime
        report_id = f"jwt_scan_{datetime.now().strftime('%d_%b_%Y_%I_%M_%p')}"
        scan_results_cache[report_id] = results
        
        print(f"[+] Analysis complete. Found {results['vulnerability_count']} vulnerabilities")
        
        return jsonify({
            "status": "success",
            "report_id": report_id,
            "results": results
        }), 200
    except Exception as e:
        print(f"[!] Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/download/<report_id>', methods=['GET'])
def download_report(report_id):
    try:
        if report_id not in scan_results_cache:
            return jsonify({"status": "error", "message": "Report not found"}), 404
        
        results = scan_results_cache[report_id]
        
        print(f"[*] Generating PDF report...")
        generator = JWTReportGenerator(results)
        pdf_path = generator.generate()
        
        print(f"[+] PDF generated: {pdf_path}")
        
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=generator.filename
        )
    except Exception as e:
        print(f"[!] Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("="*60)
    print("🔐 JWT SECURITY ANALYZER - Starting Server")
    print("="*60)
    print("Port: 5005")
    print("Endpoints:")
    print("  - POST   /api/analyze        - Analyze JWT token")
    print("  - GET    /api/download/<id>  - Download PDF report")
    print("  - GET    /health             - Health check")
    print("="*60)
    print("\nServer running on http://localhost:5005")
    print("Press CTRL+C to stop\n")
    
    app.run(host='0.0.0.0', port=5005, debug=True)

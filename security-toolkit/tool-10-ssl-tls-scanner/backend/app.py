from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scanner import SSLScanner
from reports.pdf_generator import UniversalReportGenerator


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
scan_results_cache = {}

def add_fix_prompts(vulnerabilities):
    """Add actionable fix prompts to vulnerabilities"""
    for vuln in vulnerabilities:
        vuln_type = vuln.get('type', '')
        
        if 'Expired Certificate' in vuln_type:
            vuln['fix_prompt'] = "Renew SSL certificate immediately. Use Let's Encrypt for free auto-renewal. Set up monitoring for expiration alerts."
        elif 'Weak Protocol' in vuln_type:
            vuln['fix_prompt'] = "Disable SSLv2, SSLv3, TLS 1.0, TLS 1.1. Enable only TLS 1.2 and TLS 1.3. Update server configuration."
        elif 'Weak Cipher' in vuln_type:
            vuln['fix_prompt'] = "Disable weak ciphers (RC4, DES, 3DES, MD5). Use strong ciphers: AES-GCM, ChaCha20. Configure cipher suite order."
        elif 'Self-Signed' in vuln_type:
            vuln['fix_prompt'] = "Replace self-signed certificate with CA-signed certificate. Use Let's Encrypt for free trusted certificates."
        else:
            vuln['fix_prompt'] = f"Review and fix {vuln_type}. Test with SSL Labs: ssllabs.com/ssltest"
    
    return vulnerabilities

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "port": 5010}), 200

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        scanner = SSLScanner(data['target_url'])
        results = scanner.scan()
        results['vulnerabilities'] = add_fix_prompts(results['vulnerabilities'])
        results['risk_score'] = calculate_risk_score(results['vulnerabilities'])
        results['risk_level'] = get_risk_level(results['risk_score'])
        from datetime import datetime
        report_id = f"ssl_{datetime.now().strftime('%d_%b_%Y_%I_%M_%p')}"
        scan_results_cache[report_id] = results
        return jsonify({"status": "success", "report_id": report_id, "results": results}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/download/<report_id>', methods=['GET'])
def download(report_id):
    try:
        results = scan_results_cache[report_id]
        gen = UniversalReportGenerator(results, "SSL/TLS Security")
        pdf = gen.generate()
        return send_file(pdf, mimetype='application/pdf', as_attachment=True, download_name=gen.filename)
    except:
        return jsonify({"status": "error"}), 404

if __name__ == '__main__':
    print("🔒 SSL/TLS Scanner - Port 5010")
    app.run(host='0.0.0.0', port=5010, debug=True)

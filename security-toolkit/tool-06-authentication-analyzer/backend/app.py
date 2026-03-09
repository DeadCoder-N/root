"""Authentication Analyzer - Flask Backend"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from analyzer import AuthenticationAnalyzer
from reports.pdf_generator import AuthReportGenerator


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
        
        if 'Brute Force' in vuln_type:
            vuln['fix_prompt'] = "Implement rate limiting: 5 attempts per 15 min. Add progressive delays (1s, 2s, 4s). Use CAPTCHA after 3 failed attempts."
        elif 'Password Policy' in vuln_type:
            vuln['fix_prompt'] = "Enforce: min 8 chars, uppercase, lowercase, number, special char. Check against common password lists (haveibeenpwned.com API)."
        elif 'Cookie' in vuln_type:
            vuln['fix_prompt'] = "Set cookie flags: Secure (HTTPS only), HttpOnly (no JS access), SameSite=Strict (CSRF protection). Example: Set-Cookie: session=abc; Secure; HttpOnly; SameSite=Strict"
        elif 'Session' in vuln_type:
            vuln['fix_prompt'] = "Regenerate session ID after login. Use cryptographically random IDs (128+ bits). Implement session timeout (30 min idle, 8 hours absolute)."
        elif 'Account Lockout' in vuln_type:
            vuln['fix_prompt'] = "Lock account after 5-10 failed attempts. Require admin unlock or 30-min timeout. Log all lockout events."
        elif 'Password Reset' in vuln_type:
            vuln['fix_prompt'] = "Use POST for reset tokens. Store tokens server-side with 15-min expiration. Send tokens via email only. Invalidate after use."
        elif 'Username Enumeration' in vuln_type:
            vuln['fix_prompt'] = "Use generic error: 'Invalid username or password'. Same response time for valid/invalid users. Same HTTP status code."
        elif 'Credential Stuffing' in vuln_type:
            vuln['fix_prompt'] = "Implement IP-based rate limiting. Use device fingerprinting. Add CAPTCHA for suspicious activity. Monitor for credential stuffing patterns."
        elif '2FA' in vuln_type or 'MFA' in vuln_type:
            vuln['fix_prompt'] = "Implement 2FA: TOTP (Google Authenticator), SMS, or hardware tokens. Require for admin accounts. Offer backup codes."
        else:
            vuln['fix_prompt'] = f"Review and fix {vuln_type}. Check OWASP Authentication Cheat Sheet."
    
    return vulnerabilities

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "Auth Analyzer", "port": 5006}), 200

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        if not data or 'target_url' not in data:
            return jsonify({"status": "error", "message": "Missing target_url"}), 400
        
        analyzer = AuthenticationAnalyzer(data['target_url'])
        results = analyzer.analyze()
        
        # Add fix prompts
        results['vulnerabilities'] = add_fix_prompts(results['vulnerabilities'])
        results['risk_score'] = calculate_risk_score(results['vulnerabilities'])
        results['risk_level'] = get_risk_level(results['risk_score'])
        
        from datetime import datetime
        report_id = f"auth_scan_{datetime.now().strftime('%d_%b_%Y_%I_%M_%p')}"
        scan_results_cache[report_id] = results
        
        return jsonify({"status": "success", "report_id": report_id, "results": results}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/download/<report_id>', methods=['GET'])
def download_report(report_id):
    try:
        if report_id not in scan_results_cache:
            return jsonify({"status": "error", "message": "Report not found"}), 404
        
        results = scan_results_cache[report_id]
        generator = AuthReportGenerator(results)
        pdf_path = generator.generate()
        
        return send_file(pdf_path, mimetype='application/pdf', as_attachment=True, download_name=generator.filename)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("🔐 Authentication Analyzer - Port 5006")
    app.run(host='0.0.0.0', port=5006, debug=True)

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scanner import XXEScanner
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
    for vuln in vulnerabilities:
        vuln_type = vuln.get('type', '')
        if 'XXE' in vuln_type:
            vuln['fix_prompt'] = "Disable external entities in XML parser. Python: defusedxml. Java: setFeature(XMLConstants.FEATURE_SECURE_PROCESSING, true). Use JSON instead of XML."
        elif 'XML Bomb' in vuln_type:
            vuln['fix_prompt'] = "Limit XML entity expansion. Set parser limits. Use defusedxml library. Validate XML size before parsing."
        else:
            vuln['fix_prompt'] = f"Review and fix {vuln_type}. Check OWASP XXE Prevention Cheat Sheet."
    return vulnerabilities

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "port": 5015}), 200

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        scanner = XXEScanner(data['target_url'])
        results = scanner.scan()
        results['vulnerabilities'] = add_fix_prompts(results['vulnerabilities'])
        results['risk_score'] = calculate_risk_score(results['vulnerabilities'])
        results['risk_level'] = get_risk_level(results['risk_score'])
        from datetime import datetime
        report_id = f"xxe_{datetime.now().strftime('%d_%b_%Y_%I_%M_%p')}"
        scan_results_cache[report_id] = results
        return jsonify({"status": "success", "report_id": report_id, "results": results}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/download/<report_id>', methods=['GET'])
def download(report_id):
    try:
        results = scan_results_cache[report_id]
        gen = UniversalReportGenerator(results, "XXE Security")
        pdf = gen.generate()
        return send_file(pdf, mimetype='application/pdf', as_attachment=True, download_name=gen.filename)
    except:
        return jsonify({"status": "error"}), 404

if __name__ == '__main__':
    print("⚠️ XXE Scanner - Port 5015")
    app.run(host='0.0.0.0', port=5015, debug=True)

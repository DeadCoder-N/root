#!/usr/bin/env python3
"""
XSS Scanner Backend API
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanner import XSSScanner
from reports.pdf_generator import PDFReportGenerator

app = Flask(__name__)
CORS(app, expose_headers=['Content-Disposition'])

# Store scan results
scan_results = {}

def add_fix_prompts(vulnerabilities):
    """Add fix prompts to XSS vulnerabilities"""
    for vuln in vulnerabilities:
        param = vuln.get('parameter', 'parameter')
        vuln['fix_prompt'] = f"Escape output for {param}. Use htmlspecialchars() in PHP, escape() in Flask, or DOMPurify in JavaScript. Add Content-Security-Policy header."
    return vulnerabilities

def calculate_risk_score(vulnerabilities):
    """Calculate risk score 0-100"""
    severity_scores = {'CRITICAL': 25, 'HIGH': 15, 'MEDIUM': 8, 'LOW': 3}
    return min(100, sum(severity_scores.get(v.get('severity', 'HIGH'), 15) for v in vulnerabilities))

def get_risk_level(score):
    """Get risk level from score"""
    if score >= 75: return 'CRITICAL'
    elif score >= 50: return 'HIGH'
    elif score >= 25: return 'MEDIUM'
    else: return 'LOW'

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'xss-scanner'})

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze URL for XSS vulnerabilities"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Validate URL
        if not url.startswith('http://') and not url.startswith('https://'):
            return jsonify({'error': 'Invalid URL format. Must start with http:// or https://'}), 400
        
        # Create scanner
        progress_data = {'message': '', 'percentage': 0}
        
        def progress_callback(data):
            progress_data.update(data)
        
        scanner = XSSScanner(progress_callback=progress_callback)
        
        # Scan for vulnerabilities
        results = scanner.scan(url)
        
        # Add fix prompts and risk scoring
        results['vulnerabilities'] = add_fix_prompts(results['vulnerabilities'])
        results['risk_score'] = calculate_risk_score(results['vulnerabilities'])
        results['risk_level'] = get_risk_level(results['risk_score'])
        
        # Generate scan ID
        scan_id = f"xss_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Store results
        scan_results[scan_id] = {
            'url': url,
            'scan_date': datetime.now().strftime('%d %b %Y %H:%M:%S'),
            'vulnerabilities': results['vulnerabilities'],
            'total_vulnerabilities': results['total_vulnerabilities'],
            'parameters_tested': results['parameters_tested'],
            'payloads_tested': results['payloads_tested']
        }
        
        # Generate PDF report
        report_filename = f"{scan_id}.pdf"
        report_path = os.path.join('/tmp', report_filename)
        
        pdf_generator = PDFReportGenerator()
        pdf_generator.generate({
            'target': url,
            'scan_date': scan_results[scan_id]['scan_date'],
            'vulnerabilities': results['vulnerabilities'],
            'total_vulnerabilities': results['total_vulnerabilities'],
            'parameters_tested': results['parameters_tested']
        }, report_path)
        
        return jsonify({
            'status': 'success',
            'scan_id': scan_id,
            'vulnerabilities': results['vulnerabilities'],
            'total_vulnerabilities': results['total_vulnerabilities'],
            'parameters_tested': results['parameters_tested'],
            'payloads_tested': results['payloads_tested']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<scan_id>', methods=['GET'])
def download(scan_id):
    """Download PDF report"""
    try:
        if scan_id not in scan_results:
            return jsonify({'error': 'Scan not found'}), 404
        
        report_path = os.path.join('/tmp', f"{scan_id}.pdf")
        
        if not os.path.exists(report_path):
            return jsonify({'error': 'Report not found'}), 404
        
        # Generate proper filename
        scan_data = scan_results[scan_id]
        url = scan_data['url']
        domain = url.split('/')[2].replace('www.', '').split(':')[0]
        date_str = datetime.now().strftime('%d %b %Y')
        filename = f"{domain}_{date_str}.pdf"
        
        return send_file(
            report_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 XSS Scanner Backend starting on http://localhost:5003")
    app.run(host='0.0.0.0', port=5003, debug=True)

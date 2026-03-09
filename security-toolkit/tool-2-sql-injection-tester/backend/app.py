#!/usr/bin/env python3
"""
SQL Injection Tester Backend API
Flask server for SQL injection testing
"""

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import sys
from pathlib import Path
import json
import tempfile
from datetime import datetime
from urllib.parse import urlparse

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scanner import SQLInjectionScanner
from reports.pdf_generator import PDFReportGenerator

app = Flask(__name__)
CORS(app, expose_headers=['Content-Disposition'])

# Store last scan result
last_scan_result = None
last_scan_file = None

def add_fix_prompts(vulnerabilities):
    """Add fix prompts to SQL injection vulnerabilities"""
    for vuln in vulnerabilities:
        param = vuln.get('parameter', 'parameter')
        vuln['fix_prompt'] = f"Use prepared statements for {param}. Never concatenate user input into SQL queries. Example: cursor.execute('SELECT * FROM users WHERE id=?', (user_id,))"
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

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze target for SQL injection vulnerabilities"""
    global last_scan_result, last_scan_file
    
    try:
        data = request.json
        target = data.get('target')
        
        if not target:
            return jsonify({'error': 'Target URL is required'}), 400
        
        # Validate URL
        try:
            parsed = urlparse(target)
            if not parsed.scheme or not parsed.netloc:
                return jsonify({'error': 'Invalid URL format'}), 400
        except:
            return jsonify({'error': 'Invalid URL format'}), 400
        
        # Create scanner
        scanner = SQLInjectionScanner(target=target)
        
        # Run scan
        report = scanner.scan()
        
        # Add fix prompts and risk scoring
        report['vulnerabilities'] = add_fix_prompts(report['vulnerabilities'])
        report['risk_score'] = calculate_risk_score(report['vulnerabilities'])
        report['risk_level'] = get_risk_level(report['risk_score'])
        
        # Extract domain for filename
        domain = urlparse(target).netloc.replace('www.', '').replace(':', '_')
        date_str = datetime.now().strftime('%d %b %Y')
        
        # Save to temp file
        temp_dir = Path(tempfile.gettempdir())
        json_file = temp_dir / f"sqli_{domain}_{date_str}.json"
        pdf_file = temp_dir / f"sqli_{domain}_{date_str}.pdf"
        
        with open(json_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Generate PDF
        try:
            pdf_gen = PDFReportGenerator()
            pdf_gen.generate(report, str(pdf_file))
        except Exception as e:
            print(f"PDF generation failed: {e}")
        
        last_scan_result = report
        last_scan_file = {'json': str(json_file), 'pdf': str(pdf_file)}
        
        return jsonify(report)
    
    except Exception as e:
        return jsonify({
            'error': f'Scan failed: {str(e)}',
            'fix': 'Check target URL format. Example: https://example.com/search?q=test'
        }), 500

@app.route('/api/download', methods=['GET'])
def download():
    """Download scan report"""
    global last_scan_file, last_scan_result
    
    if not last_scan_file or not last_scan_result:
        return jsonify({'error': 'No scan results available'}), 404
    
    format = request.args.get('format', 'json')
    
    if format == 'pdf':
        file_path = last_scan_file.get('pdf')
        mimetype = 'application/pdf'
    else:
        file_path = last_scan_file.get('json')
        mimetype = 'application/json'
    
    if not file_path or not Path(file_path).exists():
        return jsonify({'error': f'{format.upper()} report not found'}), 404
    
    filename = Path(file_path).name
    
    with open(file_path, 'rb') as f:
        data = f.read()
    
    response = Response(data, mimetype=mimetype)
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    response.headers['Cache-Control'] = 'no-cache'
    return response

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'SQL Injection Tester API', 'port': 5002})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("💉 SQL INJECTION TESTER BACKEND API")
    print("="*60)
    print("\n📍 Server: http://localhost:5002")
    print("📍 Health: http://localhost:5002/health")
    print("\n✅ Ready to test for SQL injection!\n")
    
    app.run(host='0.0.0.0', port=5002, debug=True)

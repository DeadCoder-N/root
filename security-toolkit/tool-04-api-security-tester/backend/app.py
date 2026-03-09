"""
API Security Tester - Flask Backend
REST API server for API security testing
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanner import APISecurityScanner
from reports.pdf_generator import APISecurityReportGenerator

app = Flask(__name__)
CORS(app)

# Store scan results temporarily
scan_results_cache = {}

def add_fix_prompts(vulnerabilities):
    """Add actionable fix prompts to vulnerabilities"""
    for vuln in vulnerabilities:
        vuln_type = vuln.get('type', '')
        
        if 'BOLA' in vuln_type:
            vuln['fix_prompt'] = "Implement object-level authorization checks. Verify user owns/can access the requested resource. Use middleware to validate permissions before data access."
        elif 'Authentication' in vuln_type:
            vuln['fix_prompt'] = "Require authentication tokens for all endpoints. Implement OAuth 2.0 or JWT. Validate tokens on every request. Return 401 for missing/invalid tokens."
        elif 'Mass Assignment' in vuln_type:
            vuln['fix_prompt'] = "Use DTOs (Data Transfer Objects) to whitelist allowed fields. Never bind request data directly to models. Validate all input fields."
        elif 'Rate Limit' in vuln_type:
            vuln['fix_prompt'] = "Implement rate limiting: 100 req/min per IP, 1000 req/hour per user. Use Redis for distributed rate limiting. Return 429 when limit exceeded."
        elif 'HTTP Method' in vuln_type:
            vuln['fix_prompt'] = "Restrict HTTP methods to only required ones. Disable PUT/DELETE if not needed. Implement proper authorization for state-changing methods."
        elif 'Excessive Data' in vuln_type:
            vuln['fix_prompt'] = "Filter response data. Only return necessary fields. Use response DTOs. Never expose passwords, tokens, or internal IDs."
        elif 'SSRF' in vuln_type:
            vuln['fix_prompt'] = "Validate and sanitize URL parameters. Use allowlist of permitted domains. Block internal IPs (127.0.0.1, 169.254.169.254). Disable URL redirects."
        elif 'Security Header' in vuln_type:
            vuln['fix_prompt'] = "Add security headers to all responses: X-Content-Type-Options: nosniff, X-Frame-Options: DENY, Strict-Transport-Security, CSP."
        else:
            vuln['fix_prompt'] = f"Review and fix {vuln_type}. Check OWASP API Security Top 10 guidelines."
    
    return vulnerabilities

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "API Security Tester",
        "version": "1.0.0",
        "port": 5004
    }), 200

@app.route('/api/analyze', methods=['POST'])
def analyze_api():
    """
    Analyze API for security vulnerabilities
    
    Request Body:
    {
        "target_url": "https://api.example.com/endpoint",
        "api_type": "REST",  // or "GraphQL"
        "auth_token": "optional_token",
        "test_types": ["BOLA", "authentication", "rate_limit"]  // optional
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'target_url' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing required field: target_url"
            }), 400
        
        target_url = data['target_url']
        api_type = data.get('api_type', 'REST')
        auth_token = data.get('auth_token')
        test_types = data.get('test_types')
        
        # Validate URL
        if not target_url.startswith(('http://', 'https://')):
            return jsonify({
                "status": "error",
                "message": "Invalid URL format. Must start with http:// or https://"
            }), 400
        
        print(f"[*] Starting API security scan for: {target_url}")
        
        # Initialize scanner
        scanner = APISecurityScanner(
            target_url=target_url,
            api_type=api_type,
            auth_token=auth_token
        )
        
        # Run scan
        results = scanner.scan(test_types=test_types)
        
        # Add fix prompts
        results['vulnerabilities'] = add_fix_prompts(results['vulnerabilities'])
        
        # Generate report ID
        from datetime import datetime
        report_id = f"api_scan_{datetime.now().strftime('%d_%b_%Y_%I_%M_%p')}"
        
        # Cache results
        scan_results_cache[report_id] = results
        
        print(f"[+] Scan completed. Found {results['vulnerability_count']} vulnerabilities")
        
        # Return results
        return jsonify({
            "status": "success",
            "message": "API security scan completed",
            "report_id": report_id,
            "results": {
                "target_url": results['target_url'],
                "api_type": results['api_type'],
                "scan_date": results['scan_date'],
                "scan_duration": results['scan_duration'],
                "vulnerability_count": results['vulnerability_count'],
                "severity_counts": results['severity_counts'],
                "risk_score": results['risk_score'],
                "risk_level": results['risk_level'],
                "vulnerabilities": results['vulnerabilities']
            }
        }), 200
    
    except Exception as e:
        print(f"[!] Error during scan: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Scan failed: {str(e)}"
        }), 500

@app.route('/api/download/<report_id>', methods=['GET'])
def download_report(report_id):
    """
    Download PDF report for a completed scan
    
    URL Parameter:
        report_id: ID of the scan report
    """
    try:
        # Check if report exists in cache
        if report_id not in scan_results_cache:
            return jsonify({
                "status": "error",
                "message": "Report not found. Please run a scan first."
            }), 404
        
        # Get scan results
        results = scan_results_cache[report_id]
        
        print(f"[*] Generating PDF report for: {report_id}")
        
        # Generate PDF report
        generator = APISecurityReportGenerator(results)
        pdf_path = generator.generate()
        
        print(f"[+] PDF report generated: {pdf_path}")
        
        # Send file
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=generator.filename
        )
    
    except Exception as e:
        print(f"[!] Error generating report: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Report generation failed: {str(e)}"
        }), 500

@app.route('/api/test-types', methods=['GET'])
def get_test_types():
    """
    Get available test types
    """
    return jsonify({
        "status": "success",
        "test_types": [
            {
                "id": "BOLA",
                "name": "Broken Object Level Authorization",
                "owasp": "API1:2023",
                "description": "Tests for IDOR vulnerabilities"
            },
            {
                "id": "authentication",
                "name": "Broken Authentication",
                "owasp": "API2:2023",
                "description": "Tests authentication mechanisms"
            },
            {
                "id": "mass_assignment",
                "name": "Mass Assignment",
                "owasp": "API3:2023",
                "description": "Tests for mass assignment vulnerabilities"
            },
            {
                "id": "rate_limit",
                "name": "Rate Limiting",
                "owasp": "API4:2023",
                "description": "Tests for missing rate limiting"
            },
            {
                "id": "http_methods",
                "name": "HTTP Method Tampering",
                "owasp": "API5:2023",
                "description": "Tests for unrestricted HTTP methods"
            },
            {
                "id": "excessive_data",
                "name": "Excessive Data Exposure",
                "owasp": "API3:2023",
                "description": "Tests for sensitive data in responses"
            },
            {
                "id": "ssrf",
                "name": "Server-Side Request Forgery",
                "owasp": "API7:2023",
                "description": "Tests for SSRF vulnerabilities"
            },
            {
                "id": "security_headers",
                "name": "Security Headers",
                "owasp": "API8:2023",
                "description": "Tests for missing security headers"
            }
        ]
    }), 200

@app.route('/api/reports', methods=['GET'])
def list_reports():
    """
    List all available reports
    """
    reports = []
    for report_id, results in scan_results_cache.items():
        reports.append({
            "report_id": report_id,
            "target_url": results['target_url'],
            "scan_date": results['scan_date'],
            "vulnerability_count": results['vulnerability_count'],
            "risk_score": results['risk_score'],
            "risk_level": results['risk_level']
        })
    
    return jsonify({
        "status": "success",
        "count": len(reports),
        "reports": reports
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "status": "error",
        "message": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500

if __name__ == '__main__':
    print("="*60)
    print("🔐 API SECURITY TESTER - Starting Server")
    print("="*60)
    print("Port: 5004")
    print("Endpoints:")
    print("  - POST   /api/analyze        - Analyze API security")
    print("  - GET    /api/download/<id>  - Download PDF report")
    print("  - GET    /api/test-types     - Get available tests")
    print("  - GET    /api/reports        - List all reports")
    print("  - GET    /health             - Health check")
    print("="*60)
    print("\nServer running on http://localhost:5004")
    print("Press CTRL+C to stop\n")
    
    app.run(host='0.0.0.0', port=5004, debug=True)

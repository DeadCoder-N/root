from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import tempfile
import shutil
import sys
import json
from pathlib import Path

# Add scanner to path
sys.path.append(str(Path(__file__).parent.parent / 'Vulnerability Scanner'))
from github_scanner import GitHubScanner

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

@app.route('/api/scan', methods=['POST'])
def scan_repository():
    try:
        data = request.get_json()
        repo_url = data.get('repo_url', '').strip()
        
        if not repo_url:
            return jsonify({'error': 'Repository URL is required'}), 400
        
        # Validate GitHub URL
        if not repo_url.startswith('https://github.com/'):
            return jsonify({'error': 'Invalid GitHub URL'}), 400
        
        # Remove .git suffix if present
        if repo_url.endswith('.git'):
            repo_url = repo_url[:-4]
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Clone repository
            print(f"Cloning repository: {repo_url}")
            result = subprocess.run(
                ['git', 'clone', '--depth', '1', repo_url, temp_dir],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                return jsonify({'error': 'Failed to clone repository. Make sure it\'s public.'}), 400
            
            # Run scanner
            print(f"Scanning repository: {temp_dir}")
            scanner = GitHubScanner(temp_dir)
            scanner.scan()
            report = scanner.generate_report()
            
            # Add repo URL to report for PDF generation
            report['repo_url'] = repo_url
            report['repo_name'] = repo_url.split('/')[-1]  # Extract repo name from URL
            
            # Generate PDF and Markdown reports
            from datetime import datetime
            now = datetime.now()
            day = now.strftime('%d')
            month = now.strftime('%b').lower()
            year = now.strftime('%Y')
            time_str = now.strftime('%I:%M:%S%p')
            errors_count = report['total_vulnerabilities']
            
            # Save scan results to JSON
            scan_results_path = Path(__file__).parent.parent / 'scan initiate' / 'scan_results.json'
            scan_results_path.parent.mkdir(exist_ok=True)
            with open(scan_results_path, 'w') as f:
                json.dump(report, f, indent=2)
            
            # Generate PDF report with scan data
            reportlab_path = Path(__file__).parent.parent / 'generate_dynamic_report.py'
            if reportlab_path.exists():
                print("Generating dynamic PDF report...")
                subprocess.run(['python3', str(reportlab_path)], cwd=str(reportlab_path.parent))
                
                # Return PDF path
                pdf_path = f"Reports/{day}_{month}_{year}||{time_str}||({errors_count})errors.pdf"
                report['pdf_report'] = pdf_path
                report['pdf_available'] = True
            else:
                report['pdf_available'] = False
            
            return jsonify(report), 200
            
        finally:
            # Cleanup temporary directory
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Clone operation timed out'}), 408
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': f'Scan failed: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@app.route('/reports/<path:filename>', methods=['GET'])
def serve_report(filename):
    """Serve generated PDF reports"""
    try:
        reports_dir = Path(__file__).parent.parent / 'Reports'
        return send_from_directory(reports_dir, filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

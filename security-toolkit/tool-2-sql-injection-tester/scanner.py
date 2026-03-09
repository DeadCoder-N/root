#!/usr/bin/env python3
"""
SQL Injection Scanner
Tests URLs for SQL injection vulnerabilities
"""

import requests
import time
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from pathlib import Path
from datetime import datetime

class SQLInjectionScanner:
    def __init__(self, target, progress_callback=None):
        self.target = target
        self.vulnerabilities = []
        self.payloads_dir = Path(__file__).parent / 'payloads'
        self.progress_callback = progress_callback
        
        # Database error signatures
        self.error_signatures = [
            'SQL syntax',
            'mysql_fetch',
            'mysql_num_rows',
            'mysqli',
            'PostgreSQL',
            'pg_query',
            'pg_exec',
            'ODBC',
            'Microsoft SQL',
            'ORA-',
            'Oracle error',
            'SQLite',
            'sqlite3',
            'Unclosed quotation',
            'quoted string',
            'syntax error',
            'unterminated string',
            'unexpected end of SQL',
            'Warning: mysql',
            'valid MySQL result',
            'MySqlClient',
            'com.mysql.jdbc',
            'Zend_Db',
            'Pdo',
            'PDOException'
        ]
    
    def load_payloads(self, payload_type):
        """Load payloads from file"""
        payload_file = self.payloads_dir / f'{payload_type}.txt'
        if not payload_file.exists():
            return []
        
        with open(payload_file, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    
    def test_parameter(self, url, param, value, payload):
        """Test a single parameter with a payload"""
        try:
            # Parse URL
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            
            # Inject payload
            params[param] = [value + payload]
            
            # Rebuild URL
            new_query = urlencode(params, doseq=True)
            test_url = urlunparse((
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                parsed.params,
                new_query,
                parsed.fragment
            ))
            
            # Send request
            start_time = time.time()
            response = requests.get(test_url, timeout=10, allow_redirects=False)
            response_time = time.time() - start_time
            
            return {
                'url': test_url,
                'status_code': response.status_code,
                'response_time': response_time,
                'content': response.text,
                'length': len(response.text)
            }
        
        except Exception as e:
            return None
    
    def detect_sql_error(self, response_text):
        """Check if response contains SQL error"""
        for signature in self.error_signatures:
            if signature.lower() in response_text.lower():
                return signature
        return None
    
    def verify_vulnerability(self, url, param, value, payload):
        """Verify vulnerability with control test (False Positive Reduction)"""
        # Test with malicious payload
        malicious_result = self.test_parameter(url, param, value, payload)
        if not malicious_result:
            return False
        
        # Test with safe control payload
        control_result = self.test_parameter(url, param, value, 'safe_test_123')
        if not control_result:
            return False
        
        # Compare responses
        malicious_has_error = self.detect_sql_error(malicious_result['content'])
        control_has_error = self.detect_sql_error(control_result['content'])
        
        # True vulnerability: malicious triggers error, control doesn't
        if malicious_has_error and not control_has_error:
            return True
        
        # Check response length difference
        length_diff = abs(malicious_result['length'] - control_result['length'])
        if length_diff > 100:
            return True
        
        return False
    
    def update_progress(self, message, percent):
        """Update progress if callback provided"""
        if self.progress_callback:
            self.progress_callback(message, percent)
    
    def scan(self):
        """Run SQL injection scan"""
        print(f"Starting SQL injection scan on: {self.target}")
        
        # Parse URL and extract parameters
        parsed = urlparse(self.target)
        params = parse_qs(parsed.query)
        
        if not params:
            return {
                'scan_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'target': self.target,
                'total_vulnerabilities': 0,
                'message': 'No parameters found to test',
                'vulnerabilities': []
            }
        
        # Get baseline response
        try:
            baseline = requests.get(self.target, timeout=10)
            baseline_length = len(baseline.text)
            baseline_time = 0
        except:
            baseline_length = 0
            baseline_time = 0
        
        # Test each parameter
        total_params = len(params)
        for idx, (param, values) in enumerate(params.items(), 1):
            original_value = values[0] if values else ''
            
            self.update_progress(f'Testing parameter "{param}"...', int((idx / total_params) * 30))
            
            # Test error-based
            self.update_progress(f'Testing error-based injection on "{param}"...', int((idx / total_params) * 30) + 10)
            for payload in self.load_payloads('error_based')[:10]:
                result = self.test_parameter(self.target, param, original_value, payload)
                if result:
                    error = self.detect_sql_error(result['content'])
                    if error:
                        # Verify to reduce false positives
                        if self.verify_vulnerability(self.target, param, original_value, payload):
                            self.vulnerabilities.append({
                                'parameter': param,
                                'payload': payload,
                                'type': 'Error-Based SQL Injection',
                                'severity': 'CRITICAL',
                                'evidence': f'Database error detected: {error}',
                                'url': result['url']
                            })
                            break
            
            # Test union-based
            self.update_progress(f'Testing union-based injection on "{param}"...', int((idx / total_params) * 60) + 10)
            for payload in self.load_payloads('union_based')[:5]:
                result = self.test_parameter(self.target, param, original_value, payload)
                if result:
                    if 'UNION' in result['content'] or abs(result['length'] - baseline_length) > 100:
                        if self.verify_vulnerability(self.target, param, original_value, payload):
                            self.vulnerabilities.append({
                                'parameter': param,
                                'payload': payload,
                                'type': 'Union-Based SQL Injection',
                                'severity': 'HIGH',
                                'evidence': 'Response length changed significantly',
                                'url': result['url']
                            })
                            break
            
            # Test time-based
            self.update_progress(f'Testing time-based injection on "{param}"...', int((idx / total_params) * 85) + 10)
            for payload in self.load_payloads('time_based')[:3]:
                result = self.test_parameter(self.target, param, original_value, payload)
                if result and result['response_time'] > 4:
                    self.vulnerabilities.append({
                        'parameter': param,
                        'payload': payload,
                        'type': 'Time-Based SQL Injection',
                        'severity': 'HIGH',
                        'evidence': f'Response delayed by {result["response_time"]:.2f} seconds',
                        'url': result['url']
                    })
                    break
        
        self.update_progress('Generating report...', 95)
        
        return {
            'scan_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'target': self.target,
            'total_vulnerabilities': len(self.vulnerabilities),
            'parameters_tested': len(params),
            'vulnerabilities': self.vulnerabilities
        }

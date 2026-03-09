#!/usr/bin/env python3
"""
XSS Scanner - Core scanning logic
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import html
import os
import time

class XSSScanner:
    def __init__(self, progress_callback=None):
        self.payloads = self._load_payloads()
        self.vulnerabilities = []
        self.progress_callback = progress_callback
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def _load_payloads(self):
        """Load XSS payloads from files"""
        payloads = {
            'reflected': [],
            'stored': [],
            'dom_based': [],
            'bypass': []
        }
        
        payload_dir = os.path.join(os.path.dirname(__file__), 'payloads')
        
        for payload_type in payloads.keys():
            file_path = os.path.join(payload_dir, f'{payload_type}.txt')
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    payloads[payload_type] = [line.strip() for line in f if line.strip()]
        
        return payloads
    
    def update_progress(self, message, percentage):
        """Send progress update to callback"""
        if self.progress_callback:
            self.progress_callback({
                'message': message,
                'percentage': percentage
            })
    
    def extract_parameters(self, url):
        """Extract URL parameters"""
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        return {k: v[0] if v else '' for k, v in params.items()}
    
    def extract_forms(self, url):
        """Extract HTML forms from page"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = []
            
            for form in soup.find_all('form'):
                form_data = {
                    'action': form.get('action', ''),
                    'method': form.get('method', 'get').lower(),
                    'inputs': []
                }
                
                for input_tag in form.find_all(['input', 'textarea']):
                    input_data = {
                        'name': input_tag.get('name', ''),
                        'type': input_tag.get('type', 'text'),
                        'value': input_tag.get('value', '')
                    }
                    if input_data['name']:
                        form_data['inputs'].append(input_data)
                
                if form_data['inputs']:
                    forms.append(form_data)
            
            return forms
        except Exception as e:
            print(f"Error extracting forms: {e}")
            return []
    
    def inject_payload(self, url, param, payload):
        """Inject payload into URL parameter"""
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        params[param] = [payload]
        new_query = urlencode(params, doseq=True)
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
    
    def is_vulnerable(self, response_text, payload):
        """Check if payload is reflected unescaped"""
        # Check if payload appears unescaped
        if payload in response_text:
            return True, "Payload reflected unescaped in HTML"
        
        # Check if payload in script tag
        if f"<script>{payload}" in response_text or f"<script>{html.escape(payload)}" in response_text:
            return True, "Payload reflected in script tag"
        
        # Check common dangerous contexts
        dangerous_contexts = [
            f'value="{payload}"',
            f"value='{payload}'",
            f'href="{payload}"',
            f"href='{payload}'",
            f'src="{payload}"',
            f"src='{payload}'"
        ]
        
        for context in dangerous_contexts:
            if context in response_text:
                return True, f"Payload in dangerous context: {context}"
        
        return False, "Payload properly escaped or not reflected"
    
    def verify_vulnerability(self, url, param, payload):
        """Verify vulnerability with control test"""
        try:
            # Test with safe control
            control = "SAFE_XSS_TEST_12345"
            control_url = self.inject_payload(url, param, control)
            response_control = requests.get(control_url, headers=self.headers, timeout=10)
            
            # Test with malicious payload
            test_url = self.inject_payload(url, param, payload)
            response_malicious = requests.get(test_url, headers=self.headers, timeout=10)
            
            # Check if malicious payload is reflected but control is not
            malicious_vulnerable, malicious_evidence = self.is_vulnerable(response_malicious.text, payload)
            control_vulnerable, _ = self.is_vulnerable(response_control.text, control)
            
            # If malicious is vulnerable but control is safe, it's a real vulnerability
            if malicious_vulnerable and not control_vulnerable:
                return True, malicious_evidence, test_url
            
            # If both are vulnerable, it might be a false positive
            if malicious_vulnerable and control_vulnerable:
                return True, malicious_evidence, test_url
            
            return False, "Safe", test_url
            
        except Exception as e:
            return False, f"Error: {str(e)}", url
    
    def scan(self, url):
        """Scan URL for XSS vulnerabilities"""
        self.vulnerabilities = []
        
        self.update_progress("Starting XSS scan...", 0)
        
        # Extract parameters
        self.update_progress("Extracting URL parameters...", 10)
        params = self.extract_parameters(url)
        
        if not params:
            self.update_progress("No parameters found. Checking for forms...", 20)
            forms = self.extract_forms(url)
            if not forms:
                self.update_progress("No injection points found", 100)
                return {
                    'vulnerabilities': [],
                    'total_vulnerabilities': 0,
                    'parameters_tested': 0,
                    'payloads_tested': 0
                }
        
        # Combine all payloads
        all_payloads = []
        for payload_list in self.payloads.values():
            all_payloads.extend(payload_list)
        
        total_tests = len(params) * len(all_payloads)
        current_test = 0
        
        # Test each parameter
        for param in params:
            self.update_progress(f"Testing parameter: {param}", 20 + (current_test / total_tests * 60))
            
            for payload_type, payload_list in self.payloads.items():
                for payload in payload_list:
                    current_test += 1
                    
                    # Verify vulnerability
                    is_vuln, evidence, test_url = self.verify_vulnerability(url, param, payload)
                    
                    if is_vuln:
                        severity = self._calculate_severity(payload, evidence)
                        
                        vuln = {
                            'parameter': param,
                            'type': f'{payload_type.replace("_", " ").title()} XSS',
                            'severity': severity,
                            'payload': payload,
                            'evidence': evidence,
                            'url': test_url
                        }
                        
                        # Avoid duplicates
                        if not any(v['parameter'] == param and v['payload'] == payload for v in self.vulnerabilities):
                            self.vulnerabilities.append(vuln)
                    
                    # Small delay to avoid rate limiting
                    time.sleep(0.1)
        
        self.update_progress("Scan complete!", 100)
        
        return {
            'vulnerabilities': self.vulnerabilities,
            'total_vulnerabilities': len(self.vulnerabilities),
            'parameters_tested': len(params),
            'payloads_tested': len(all_payloads)
        }
    
    def _calculate_severity(self, payload, evidence):
        """Calculate vulnerability severity"""
        if '<script>' in payload.lower() or 'onerror' in payload.lower():
            return 'CRITICAL'
        elif 'javascript:' in payload.lower() or 'onload' in payload.lower():
            return 'HIGH'
        elif 'img' in payload.lower() or 'svg' in payload.lower():
            return 'HIGH'
        else:
            return 'MEDIUM'

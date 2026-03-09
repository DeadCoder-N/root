"""
BOLA/IDOR Vulnerability Testing Module
Tests for Broken Object Level Authorization (OWASP API1:2023)
"""

import requests
from typing import List, Dict, Any

class BOLATester:
    """Test for BOLA/IDOR vulnerabilities"""
    
    def __init__(self, target_url: str, headers: Dict[str, str]):
        self.target_url = target_url
        self.headers = headers
        self.vulnerabilities = []
    
    def test(self) -> List[Dict[str, Any]]:
        """Run BOLA/IDOR tests"""
        print("[*] Testing for BOLA/IDOR vulnerabilities...")
        
        # Test with different ID values
        test_ids = [1, 2, 999, 9999, -1, 0, "admin", "../", "../../etc/passwd"]
        
        for test_id in test_ids:
            try:
                # Construct URL with ID
                if "?" in self.target_url:
                    test_url = f"{self.target_url}&id={test_id}"
                else:
                    test_url = f"{self.target_url}/{test_id}"
                
                response = requests.get(test_url, headers=self.headers, timeout=10)
                
                # Check if unauthorized access is possible
                if response.status_code == 200:
                    # Check if response contains sensitive data
                    if self._contains_sensitive_data(response.text):
                        self.vulnerabilities.append({
                            "type": "BOLA (Broken Object Level Authorization)",
                            "severity": "CRITICAL",
                            "owasp": "API1:2023",
                            "cwe": "CWE-639",
                            "cvss": 9.1,
                            "description": f"API allows access to object with ID {test_id} without proper authorization",
                            "endpoint": test_url,
                            "method": "GET",
                            "evidence": f"Status: {response.status_code}, Response length: {len(response.text)}",
                            "remediation": "Implement proper object-level authorization checks. Verify user has permission to access requested object."
                        })
                        break
            
            except Exception as e:
                continue
        
        return self.vulnerabilities
    
    def _contains_sensitive_data(self, response_text: str) -> bool:
        """Check if response contains sensitive data"""
        sensitive_keywords = [
            "password", "email", "phone", "address",
            "ssn", "credit_card", "token", "secret"
        ]
        
        response_lower = response_text.lower()
        return any(keyword in response_lower for keyword in sensitive_keywords)

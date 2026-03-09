"""
Authentication Vulnerability Testing Module
Tests for Broken Authentication (OWASP API2:2023)
"""

import requests
from typing import List, Dict, Any

class AuthenticationTester:
    """Test for authentication vulnerabilities"""
    
    def __init__(self, target_url: str, headers: Dict[str, str], auth_token: str = None):
        self.target_url = target_url
        self.headers = headers
        self.auth_token = auth_token
        self.vulnerabilities = []
    
    def test(self) -> List[Dict[str, Any]]:
        """Run authentication tests"""
        print("[*] Testing authentication mechanisms...")
        
        # Test 1: No authentication token
        self._test_no_auth()
        
        # Test 2: Invalid token (if auth_token provided)
        if self.auth_token:
            self._test_invalid_token()
        
        return self.vulnerabilities
    
    def _test_no_auth(self):
        """Test endpoint without authentication"""
        headers_no_auth = self.headers.copy()
        if "Authorization" in headers_no_auth:
            del headers_no_auth["Authorization"]
        
        try:
            response = requests.get(self.target_url, headers=headers_no_auth, timeout=10)
            
            if response.status_code == 200:
                self.vulnerabilities.append({
                    "type": "Missing Authentication",
                    "severity": "HIGH",
                    "owasp": "API2:2023",
                    "cwe": "CWE-306",
                    "cvss": 7.5,
                    "description": "API endpoint accessible without authentication",
                    "endpoint": self.target_url,
                    "method": "GET",
                    "evidence": f"Status: {response.status_code} without auth token",
                    "remediation": "Implement proper authentication mechanism (OAuth 2.0, JWT, API keys)"
                })
        
        except Exception as e:
            pass
    
    def _test_invalid_token(self):
        """Test with invalid authentication token"""
        headers_invalid = self.headers.copy()
        headers_invalid["Authorization"] = "Bearer invalid_token_12345"
        
        try:
            response = requests.get(self.target_url, headers=headers_invalid, timeout=10)
            
            if response.status_code == 200:
                self.vulnerabilities.append({
                    "type": "Weak Token Validation",
                    "severity": "HIGH",
                    "owasp": "API2:2023",
                    "cwe": "CWE-287",
                    "cvss": 8.1,
                    "description": "API accepts invalid authentication tokens",
                    "endpoint": self.target_url,
                    "method": "GET",
                    "evidence": "Invalid token accepted",
                    "remediation": "Implement proper token validation and signature verification"
                })
        
        except Exception as e:
            pass

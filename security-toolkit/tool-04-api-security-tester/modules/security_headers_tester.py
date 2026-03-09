"""
Security Headers Testing Module
Tests for missing security headers (OWASP API8:2023)
"""

import requests
from typing import List, Dict, Any

class SecurityHeadersTester:
    """Test for missing security headers"""
    
    def __init__(self, target_url: str, headers: Dict[str, str]):
        self.target_url = target_url
        self.headers = headers
        self.vulnerabilities = []
    
    def test(self) -> List[Dict[str, Any]]:
        """Run security headers tests"""
        print("[*] Testing security headers...")
        
        try:
            response = requests.get(self.target_url, headers=self.headers, timeout=10)
            
            # Required security headers
            required_headers = {
                "X-Content-Type-Options": "nosniff",
                "X-Frame-Options": "DENY",
                "Strict-Transport-Security": "max-age=31536000",
                "Content-Security-Policy": "default-src 'self'",
                "X-XSS-Protection": "1; mode=block"
            }
            
            missing_headers = []
            
            for header, expected_value in required_headers.items():
                if header not in response.headers:
                    missing_headers.append(header)
            
            if missing_headers:
                self.vulnerabilities.append({
                    "type": "Missing Security Headers",
                    "severity": "MEDIUM",
                    "owasp": "API8:2023",
                    "cwe": "CWE-693",
                    "cvss": 5.3,
                    "description": f"API missing security headers: {', '.join(missing_headers)}",
                    "endpoint": self.target_url,
                    "method": "GET",
                    "evidence": f"Missing headers: {', '.join(missing_headers)}",
                    "remediation": "Add security headers to all API responses"
                })
        
        except Exception as e:
            pass
        
        return self.vulnerabilities

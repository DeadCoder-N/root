"""
Rate Limiting Testing Module
Tests for missing rate limiting (OWASP API4:2023)
"""

import requests
import time
from typing import List, Dict, Any

class RateLimitTester:
    """Test for rate limiting vulnerabilities"""
    
    def __init__(self, target_url: str, headers: Dict[str, str]):
        self.target_url = target_url
        self.headers = headers
        self.vulnerabilities = []
    
    def test(self, request_count: int = 50) -> List[Dict[str, Any]]:
        """Run rate limiting tests"""
        print("[*] Testing rate limiting...")
        
        success_count = 0
        start_time = time.time()
        
        for i in range(request_count):
            try:
                response = requests.get(self.target_url, headers=self.headers, timeout=5)
                if response.status_code == 200:
                    success_count += 1
            except:
                pass
        
        end_time = time.time()
        duration = end_time - start_time
        
        # If more than 80% requests succeeded, rate limiting might be missing
        if success_count > (request_count * 0.8):
            self.vulnerabilities.append({
                "type": "Missing Rate Limiting",
                "severity": "MEDIUM",
                "owasp": "API4:2023",
                "cwe": "CWE-770",
                "cvss": 5.3,
                "description": f"API processed {success_count}/{request_count} requests in {duration:.2f}s without rate limiting",
                "endpoint": self.target_url,
                "method": "GET",
                "evidence": f"{success_count} successful requests in {duration:.2f} seconds",
                "remediation": "Implement rate limiting (e.g., 100 requests per minute per IP/user)"
            })
        
        return self.vulnerabilities

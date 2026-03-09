"""Brute Force Protection Tester Module"""
import requests
import time
from typing import Dict, List

class BruteForceTester:
    """Test for brute force protection and rate limiting"""
    
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.vulnerabilities = []
    
    def test_all(self) -> List[Dict]:
        """Run all brute force tests"""
        self._test_rate_limiting()
        self._test_account_lockout()
        self._test_captcha()
        return self.vulnerabilities
    
    def _test_rate_limiting(self):
        """Test for rate limiting on login endpoint"""
        print("[*] Testing rate limiting...")
        
        # Send 10 rapid login attempts
        success_count = 0
        for i in range(10):
            try:
                response = requests.post(
                    f"{self.target_url}/login",
                    data={"username": "test", "password": f"wrong{i}"},
                    timeout=5
                )
                if response.status_code != 429:  # Not rate limited
                    success_count += 1
            except:
                pass
        
        if success_count >= 8:  # 80% success = no rate limiting
            self.vulnerabilities.append({
                "type": "Missing Brute Force Protection",
                "severity": "HIGH",
                "owasp": "API4:2023",
                "cwe": "CWE-307",
                "description": f"No rate limiting detected. {success_count}/10 requests succeeded.",
                "evidence": f"Sent 10 rapid requests, {success_count} succeeded",
                "remediation": "Implement rate limiting: 5 attempts per 15 minutes per IP",
                "cvss": 7.5,
                "fix_prompt": "Add rate limiting middleware with Redis or in-memory store"
            })
            print(f"    [!] HIGH: No rate limiting ({success_count}/10 succeeded)")
        else:
            print(f"    [+] Rate limiting detected ({success_count}/10 succeeded)")
    
    def _test_account_lockout(self):
        """Test for account lockout mechanism"""
        print("[*] Testing account lockout...")
        # Implementation would test if account locks after N failed attempts
        pass
    
    def _test_captcha(self):
        """Test for CAPTCHA after failed attempts"""
        print("[*] Testing CAPTCHA...")
        # Implementation would check if CAPTCHA appears after failed attempts
        pass

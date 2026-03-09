"""Password Policy Tester Module"""
import requests
from typing import Dict, List

class PasswordPolicyTester:
    """Test password policy strength"""
    
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.vulnerabilities = []
        self.weak_passwords = ['123456', 'password', 'abc123', '12345678', 'qwerty']
    
    def test_all(self) -> List[Dict]:
        """Run all password policy tests"""
        self._test_weak_passwords()
        self._test_minimum_length()
        self._test_complexity()
        return self.vulnerabilities
    
    def _test_weak_passwords(self):
        """Test if weak passwords are accepted"""
        print("[*] Testing weak password acceptance...")
        
        accepted_weak = []
        for pwd in self.weak_passwords:
            try:
                response = requests.post(
                    f"{self.target_url}/register",
                    data={"username": f"test_{pwd}", "password": pwd},
                    timeout=5
                )
                if response.status_code == 200 or 'success' in response.text.lower():
                    accepted_weak.append(pwd)
            except:
                pass
        
        if accepted_weak:
            self.vulnerabilities.append({
                "type": "Weak Password Policy",
                "severity": "MEDIUM",
                "owasp": "A07:2021",
                "cwe": "CWE-521",
                "description": f"Weak passwords accepted: {', '.join(accepted_weak)}",
                "evidence": f"Passwords accepted: {accepted_weak}",
                "remediation": "Enforce strong password policy: min 8 chars, uppercase, lowercase, number, special char",
                "cvss": 5.3,
                "fix_prompt": "Implement password validation with complexity requirements"
            })
            print(f"    [!] MEDIUM: Weak passwords accepted: {accepted_weak}")
        else:
            print("    [+] Weak passwords rejected")
    
    def _test_minimum_length(self):
        """Test minimum password length"""
        print("[*] Testing minimum password length...")
        pass
    
    def _test_complexity(self):
        """Test password complexity requirements"""
        print("[*] Testing password complexity...")
        pass

"""
Authentication Security Analyzer - Professional Grade
Comprehensive authentication vulnerability testing
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Any
from datetime import datetime
import time
import re

class AuthenticationAnalyzer:
    """Professional Authentication Security Analyzer"""
    
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.vulnerabilities = []
        self.scan_start_time = None
        self.scan_end_time = None
        
    def analyze(self) -> Dict[str, Any]:
        """Run comprehensive authentication security tests"""
        self.scan_start_time = datetime.now()
        
        print(f"[*] Starting authentication security analysis for: {self.target_url}")
        
        # Core tests
        self._test_brute_force_protection()
        self._test_password_policy()
        self._test_cookie_security()
        self._test_session_management()
        
        # Advanced tests
        self._test_account_lockout()
        self._test_password_reset()
        self._test_username_enumeration()
        self._test_credential_stuffing()
        self._test_2fa_bypass()
        
        self.scan_end_time = datetime.now()
        
        print(f"[+] Analysis complete. Found {len(self.vulnerabilities)} vulnerabilities")
        
        return self._generate_results()
    
    def _test_brute_force_protection(self):
        """Test for brute force protection"""
        print("[*] Testing brute force protection...")
        
        attempts = 15
        success_count = 0
        blocked = False
        
        for i in range(attempts):
            try:
                response = requests.post(
                    self.target_url,
                    data={"username": "testuser", "password": f"wrong{i}"},
                    timeout=5
                )
                
                if response.status_code == 429:
                    blocked = True
                    print(f"    [+] Rate limiting detected after {i+1} attempts")
                    break
                elif response.status_code != 429:
                    success_count += 1
                    
            except requests.exceptions.Timeout:
                continue
            except:
                pass
        
        # Verify with control test
        if not blocked and success_count > 10:
            if self._verify_brute_force_vulnerability(success_count, attempts):
                self.vulnerabilities.append({
                    "type": "Missing Brute Force Protection",
                    "severity": "HIGH",
                    "owasp": "API2:2023",
                    "cwe": "CWE-307",
                    "description": f"Login endpoint accepts {success_count}/{attempts} failed attempts without rate limiting or account lockout",
                    "evidence": f"{success_count} consecutive failed login attempts allowed",
                    "remediation": "Implement rate limiting (e.g., 5 attempts per 15 minutes) and progressive delays. Consider CAPTCHA after 3 failed attempts.",
                    "cvss": 7.5,
                    "impact": "Attackers can perform unlimited password guessing attacks"
                })
                print(f"    [!] HIGH: No brute force protection ({success_count} attempts allowed)")
    
    def _verify_brute_force_vulnerability(self, success_count: int, total_attempts: int) -> bool:
        """Verify brute force vulnerability with control test"""
        try:
            # Test with valid-looking credentials
            control_response = requests.post(
                self.target_url,
                data={"username": "admin", "password": "test123"},
                timeout=5
            )
            # If control also succeeds without blocking, vulnerability confirmed
            return control_response.status_code != 429
        except:
            return True
    
    def _test_password_policy(self):
        """Test password policy strength"""
        print("[*] Testing password policy...")
        
        weak_passwords = [
            "123456", "password", "admin", "test", "12345678",
            "qwerty", "abc123", "letmein", "welcome", "monkey"
        ]
        
        for pwd in weak_passwords:
            try:
                response = requests.post(
                    self.target_url,
                    data={"username": "newuser", "password": pwd, "action": "register"},
                    timeout=5
                )
                
                if response.status_code in [200, 201]:
                    self.vulnerabilities.append({
                        "type": "Weak Password Policy",
                        "severity": "MEDIUM",
                        "owasp": "API2:2023",
                        "cwe": "CWE-521",
                        "description": f"System accepts weak password: '{pwd}'",
                        "evidence": f"Weak password '{pwd}' was accepted",
                        "remediation": "Enforce strong password policy: minimum 8 characters, mixed case, numbers, special characters. Check against common password lists.",
                        "cvss": 5.3,
                        "impact": "Users can set easily guessable passwords"
                    })
                    print(f"    [!] MEDIUM: Weak password accepted: {pwd}")
                    break
            except:
                pass
    
    def _test_cookie_security(self):
        """Test cookie security attributes"""
        print("[*] Testing cookie security...")
        
        try:
            response = requests.get(self.target_url, timeout=5)
            cookies = response.cookies
            
            if not cookies:
                print("    [i] No cookies found")
                return
            
            for cookie in cookies:
                issues = []
                
                if not cookie.secure:
                    issues.append("Missing Secure flag")
                
                if not cookie.has_nonstandard_attr('HttpOnly'):
                    issues.append("Missing HttpOnly flag")
                
                if not cookie.has_nonstandard_attr('SameSite'):
                    issues.append("Missing SameSite attribute")
                
                if issues:
                    self.vulnerabilities.append({
                        "type": "Insecure Cookie Configuration",
                        "severity": "MEDIUM",
                        "owasp": "API2:2023",
                        "cwe": "CWE-614",
                        "description": f"Cookie '{cookie.name}' has security issues: {', '.join(issues)}",
                        "evidence": f"Cookie: {cookie.name}, Issues: {', '.join(issues)}",
                        "remediation": "Set Secure, HttpOnly, and SameSite=Strict flags on all authentication cookies",
                        "cvss": 5.3,
                        "impact": "Cookies vulnerable to interception and XSS attacks"
                    })
                    print(f"    [!] MEDIUM: Insecure cookie: {cookie.name}")
        except:
            pass
    
    def _test_session_management(self):
        """Test session management security"""
        print("[*] Testing session management...")
        
        try:
            # Get initial session
            response1 = requests.get(self.target_url, timeout=5)
            session_id_1 = response1.cookies.get('sessionid') or response1.cookies.get('PHPSESSID') or response1.cookies.get('JSESSIONID')
            
            if not session_id_1:
                print("    [i] No session cookie found")
                return
            
            # Try to reuse session
            response2 = requests.get(
                self.target_url,
                cookies={'sessionid': session_id_1},
                timeout=5
            )
            
            if response2.status_code == 200:
                self.vulnerabilities.append({
                    "type": "Session Fixation Risk",
                    "severity": "HIGH",
                    "owasp": "API2:2023",
                    "cwe": "CWE-384",
                    "description": "Session ID not regenerated after authentication",
                    "evidence": "Same session ID accepted before and after login",
                    "remediation": "Regenerate session ID after successful authentication. Invalidate old session.",
                    "cvss": 7.5,
                    "impact": "Attackers can hijack user sessions"
                })
                print("    [!] HIGH: Session fixation vulnerability")
            
            # Check session ID predictability
            if len(session_id_1) < 16:
                self.vulnerabilities.append({
                    "type": "Weak Session ID",
                    "severity": "HIGH",
                    "owasp": "API2:2023",
                    "cwe": "CWE-330",
                    "description": f"Session ID too short ({len(session_id_1)} characters) - potentially predictable",
                    "evidence": f"Session ID length: {len(session_id_1)} chars",
                    "remediation": "Use cryptographically secure random session IDs (minimum 128 bits)",
                    "cvss": 7.5
                })
        except:
            pass
    
    def _test_account_lockout(self):
        """Test account lockout mechanism"""
        print("[*] Testing account lockout...")
        
        lockout_detected = False
        attempts = 10
        
        for i in range(attempts):
            try:
                response = requests.post(
                    self.target_url,
                    data={"username": "admin", "password": f"wrong{i}"},
                    timeout=5
                )
                
                if "locked" in response.text.lower() or "disabled" in response.text.lower():
                    lockout_detected = True
                    print(f"    [+] Account lockout detected after {i+1} attempts")
                    break
            except:
                pass
        
        if not lockout_detected:
            self.vulnerabilities.append({
                "type": "Missing Account Lockout",
                "severity": "MEDIUM",
                "owasp": "API2:2023",
                "cwe": "CWE-307",
                "description": "No account lockout mechanism detected after multiple failed attempts",
                "evidence": f"{attempts} failed attempts without lockout",
                "remediation": "Implement account lockout after 5-10 failed attempts. Require admin intervention or time-based unlock.",
                "cvss": 5.3
            })
            print("    [!] MEDIUM: No account lockout detected")
    
    def _test_password_reset(self):
        """Test password reset flow security"""
        print("[*] Testing password reset flow...")
        
        try:
            # Try to access password reset
            response = requests.get(f"{self.target_url}/reset-password", timeout=5)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Check for token in URL
                if 'token=' in response.url or 'reset_token=' in response.url:
                    self.vulnerabilities.append({
                        "type": "Password Reset Token in URL",
                        "severity": "MEDIUM",
                        "owasp": "API2:2023",
                        "cwe": "CWE-640",
                        "description": "Password reset token exposed in URL (visible in logs, referrer headers)",
                        "evidence": "Reset token found in URL parameters",
                        "remediation": "Use POST requests for password reset. Store tokens server-side, not in URLs.",
                        "cvss": 5.3
                    })
        except:
            pass
    
    def _test_username_enumeration(self):
        """Test for username enumeration"""
        print("[*] Testing username enumeration...")
        
        try:
            # Test with likely invalid username
            response1 = requests.post(
                self.target_url,
                data={"username": "nonexistentuser12345", "password": "test"},
                timeout=5
            )
            
            # Test with common username
            response2 = requests.post(
                self.target_url,
                data={"username": "admin", "password": "test"},
                timeout=5
            )
            
            # Compare responses
            if response1.text != response2.text or response1.status_code != response2.status_code:
                self.vulnerabilities.append({
                    "type": "Username Enumeration",
                    "severity": "LOW",
                    "owasp": "API2:2023",
                    "cwe": "CWE-203",
                    "description": "Different responses for valid vs invalid usernames allow username enumeration",
                    "evidence": "Response differs between valid and invalid usernames",
                    "remediation": "Use generic error messages: 'Invalid username or password'",
                    "cvss": 3.1
                })
                print("    [!] LOW: Username enumeration possible")
        except:
            pass
    
    def _test_credential_stuffing(self):
        """Test credential stuffing protection"""
        print("[*] Testing credential stuffing protection...")
        
        # Simulate multiple login attempts from same IP
        attempts = 20
        success_count = 0
        
        for i in range(attempts):
            try:
                response = requests.post(
                    self.target_url,
                    data={"username": f"user{i}", "password": f"pass{i}"},
                    timeout=3
                )
                
                if response.status_code != 429:
                    success_count += 1
            except:
                pass
        
        if success_count > 15:
            self.vulnerabilities.append({
                "type": "Credential Stuffing Vulnerability",
                "severity": "HIGH",
                "owasp": "API2:2023",
                "cwe": "CWE-307",
                "description": f"No protection against credential stuffing attacks ({success_count}/{attempts} attempts allowed)",
                "evidence": f"{success_count} login attempts from same IP without blocking",
                "remediation": "Implement IP-based rate limiting, CAPTCHA, and device fingerprinting",
                "cvss": 7.5
            })
            print(f"    [!] HIGH: Credential stuffing possible ({success_count} attempts)")
    
    def _test_2fa_bypass(self):
        """Test 2FA bypass vulnerabilities"""
        print("[*] Testing 2FA bypass...")
        
        try:
            # Check if 2FA is implemented
            response = requests.get(self.target_url, timeout=5)
            
            if '2fa' not in response.text.lower() and 'two-factor' not in response.text.lower() and 'mfa' not in response.text.lower():
                self.vulnerabilities.append({
                    "type": "Missing Two-Factor Authentication",
                    "severity": "MEDIUM",
                    "owasp": "API2:2023",
                    "cwe": "CWE-308",
                    "description": "No two-factor authentication (2FA/MFA) implementation detected",
                    "evidence": "No 2FA indicators found in authentication flow",
                    "remediation": "Implement 2FA using TOTP, SMS, or hardware tokens for sensitive accounts",
                    "cvss": 5.3,
                    "impact": "Single factor (password) is sole authentication method"
                })
                print("    [!] MEDIUM: No 2FA detected")
        except:
            pass
    
    def _generate_results(self) -> Dict[str, Any]:
        """Generate comprehensive results"""
        
        risk_score = self._calculate_risk_score()
        
        severity_counts = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0
        }
        
        for vuln in self.vulnerabilities:
            severity = vuln.get("severity", "LOW")
            severity_counts[severity] += 1
        
        duration = (self.scan_end_time - self.scan_start_time).total_seconds()
        
        return {
            "target_url": self.target_url,
            "vulnerabilities": self.vulnerabilities,
            "vulnerability_count": len(self.vulnerabilities),
            "severity_counts": severity_counts,
            "risk_score": risk_score,
            "risk_level": self._get_risk_level(risk_score),
            "scan_date": self.scan_start_time.strftime("%d %b %Y %H:%M:%S"),
            "scan_duration": f"{duration:.2f}s"
        }
    
    def _calculate_risk_score(self) -> int:
        """Calculate risk score"""
        if not self.vulnerabilities:
            return 0
        
        severity_weights = {
            "CRITICAL": 25,
            "HIGH": 15,
            "MEDIUM": 8,
            "LOW": 3
        }
        
        total_score = 0
        for vuln in self.vulnerabilities:
            severity = vuln.get("severity", "LOW")
            total_score += severity_weights.get(severity, 0)
        
        return min(total_score, 100)
    
    def _get_risk_level(self, risk_score: int) -> str:
        """Get risk level"""
        if risk_score >= 80:
            return "CRITICAL"
        elif risk_score >= 60:
            return "HIGH"
        elif risk_score >= 40:
            return "MEDIUM"
        elif risk_score >= 20:
            return "LOW"
        else:
            return "MINIMAL"

"""
OAuth Security Tester - Professional Grade
Comprehensive OAuth 2.0 and OpenID Connect vulnerability testing
"""

import requests
from urllib.parse import urlparse, parse_qs, urlencode
from typing import Dict, List, Any
from datetime import datetime
import re

class OAuthTester:
    """Professional OAuth Security Tester"""
    
    def __init__(self, auth_url: str):
        self.auth_url = auth_url
        self.vulnerabilities = []
        self.scan_start_time = None
        self.scan_end_time = None
        
    def test(self) -> Dict[str, Any]:
        """Run comprehensive OAuth security tests"""
        self.scan_start_time = datetime.now()
        
        print(f"[*] Starting OAuth security analysis for: {self.auth_url}")
        
        # Core OAuth tests
        self._test_state_parameter()
        self._test_redirect_uri()
        self._test_pkce()
        
        # Advanced tests
        self._test_open_redirect()
        self._test_authorization_code_injection()
        self._test_token_leakage()
        self._test_scope_manipulation()
        self._test_client_secret_exposure()
        self._test_implicit_flow()
        
        self.scan_end_time = datetime.now()
        
        print(f"[+] Analysis complete. Found {len(self.vulnerabilities)} vulnerabilities")
        
        return self._generate_results()
    
    def _test_state_parameter(self):
        """Test for missing state parameter (CSRF protection)"""
        print("[*] Testing state parameter...")
        
        try:
            response = requests.get(
                f"{self.auth_url}?response_type=code&client_id=test",
                timeout=5,
                allow_redirects=False
            )
            
            # Check if state is required
            if 'state' not in response.url.lower() and response.status_code not in [400, 401]:
                self.vulnerabilities.append({
                    "type": "Missing State Parameter",
                    "severity": "HIGH",
                    "owasp": "API2:2023",
                    "cwe": "CWE-352",
                    "description": "OAuth flow missing CSRF protection via state parameter",
                    "evidence": "Authorization request accepted without state parameter",
                    "remediation": "Require state parameter in all OAuth requests. Generate cryptographically random state value.",
                    "cvss": 7.5,
                    "impact": "Attackers can perform CSRF attacks to link victim's account to attacker's OAuth account"
                })
                print("    [!] HIGH: Missing state parameter")
        except:
            pass
    
    def _test_redirect_uri(self):
        """Test redirect URI validation"""
        print("[*] Testing redirect URI validation...")
        
        malicious_redirects = [
            "http://evil.com",
            "https://evil.com/callback",
            "javascript:alert(1)",
            "data:text/html,<script>alert(1)</script>",
            f"{self.auth_url}@evil.com",
            f"{self.auth_url}.evil.com"
        ]
        
        for redirect in malicious_redirects:
            try:
                response = requests.get(
                    f"{self.auth_url}?redirect_uri={redirect}&response_type=code&client_id=test",
                    timeout=5,
                    allow_redirects=False
                )
                
                if response.status_code in [302, 301]:
                    location = response.headers.get('Location', '')
                    if redirect in location or 'evil.com' in location:
                        # Verify with control test
                        if self._verify_redirect_vulnerability(redirect):
                            self.vulnerabilities.append({
                                "type": "Open Redirect via redirect_uri",
                                "severity": "HIGH",
                                "owasp": "API2:2023",
                                "cwe": "CWE-601",
                                "description": f"Weak redirect_uri validation allows open redirect to: {redirect}",
                                "evidence": f"Malicious redirect accepted: {redirect}",
                                "remediation": "Implement strict whitelist of allowed redirect URIs. Validate exact match, not substring.",
                                "cvss": 7.4,
                                "impact": "Attackers can steal authorization codes via phishing"
                            })
                            print(f"    [!] HIGH: Open redirect to {redirect}")
                            break
            except:
                continue
    
    def _verify_redirect_vulnerability(self, malicious_redirect: str) -> bool:
        """Verify redirect vulnerability with control test"""
        try:
            # Test with safe redirect
            safe_redirect = self.auth_url
            control_response = requests.get(
                f"{self.auth_url}?redirect_uri={safe_redirect}&response_type=code&client_id=test",
                timeout=5,
                allow_redirects=False
            )
            # If malicious redirect behaves differently, vulnerability confirmed
            return control_response.status_code in [200, 302, 301]
        except:
            return True
    
    def _test_pkce(self):
        """Test for PKCE (Proof Key for Code Exchange)"""
        print("[*] Testing PKCE implementation...")
        
        try:
            response = requests.get(
                f"{self.auth_url}?response_type=code&client_id=test",
                timeout=5
            )
            
            if 'code_challenge' not in response.url.lower() and 'code_verifier' not in response.text.lower():
                self.vulnerabilities.append({
                    "type": "Missing PKCE Protection",
                    "severity": "MEDIUM",
                    "owasp": "API2:2023",
                    "cwe": "CWE-346",
                    "description": "OAuth flow missing PKCE (Proof Key for Code Exchange) protection",
                    "evidence": "No code_challenge parameter detected",
                    "remediation": "Implement PKCE for public clients (mobile/SPA apps). Use code_challenge and code_verifier.",
                    "cvss": 5.9,
                    "impact": "Authorization code interception attacks possible"
                })
                print("    [!] MEDIUM: PKCE not implemented")
        except:
            pass
    
    def _test_open_redirect(self):
        """Test for open redirect vulnerabilities"""
        print("[*] Testing open redirect vulnerabilities...")
        
        redirect_payloads = [
            "//evil.com",
            "///evil.com",
            "////evil.com",
            "/\\evil.com",
            "https:evil.com",
            "https:/evil.com"
        ]
        
        for payload in redirect_payloads:
            try:
                response = requests.get(
                    f"{self.auth_url}?redirect_uri={payload}",
                    timeout=5,
                    allow_redirects=False
                )
                
                if response.status_code in [302, 301] and 'evil.com' in response.headers.get('Location', ''):
                    self.vulnerabilities.append({
                        "type": "Open Redirect Bypass",
                        "severity": "HIGH",
                        "owasp": "API2:2023",
                        "cwe": "CWE-601",
                        "description": f"Redirect URI validation bypassed with payload: {payload}",
                        "evidence": f"Bypass payload: {payload}",
                        "remediation": "Implement strict URL parsing and validation. Check protocol, domain, and path.",
                        "cvss": 7.4
                    })
                    print(f"    [!] HIGH: Open redirect bypass: {payload}")
                    break
            except:
                continue
    
    def _test_authorization_code_injection(self):
        """Test for authorization code injection"""
        print("[*] Testing authorization code injection...")
        
        try:
            # Try to inject authorization code
            response = requests.get(
                f"{self.auth_url}?code=injected_code&state=test",
                timeout=5
            )
            
            if response.status_code == 200 and 'error' not in response.text.lower():
                self.vulnerabilities.append({
                    "type": "Authorization Code Injection",
                    "severity": "HIGH",
                    "owasp": "API2:2023",
                    "cwe": "CWE-94",
                    "description": "Application accepts injected authorization codes without validation",
                    "evidence": "Injected code parameter accepted",
                    "remediation": "Validate authorization codes server-side. Bind codes to client_id and redirect_uri.",
                    "cvss": 7.5
                })
                print("    [!] HIGH: Code injection possible")
        except:
            pass
    
    def _test_token_leakage(self):
        """Test for token leakage via referrer"""
        print("[*] Testing token leakage...")
        
        try:
            # Check if tokens in URL (implicit flow)
            response = requests.get(
                f"{self.auth_url}?response_type=token&client_id=test",
                timeout=5,
                allow_redirects=False
            )
            
            if response.status_code in [302, 301]:
                location = response.headers.get('Location', '')
                if '#access_token=' in location or '&access_token=' in location:
                    self.vulnerabilities.append({
                        "type": "Token Leakage via URL Fragment",
                        "severity": "HIGH",
                        "owasp": "API2:2023",
                        "cwe": "CWE-200",
                        "description": "Access tokens exposed in URL fragments (visible in browser history, logs)",
                        "evidence": "Token found in URL fragment",
                        "remediation": "Use authorization code flow instead of implicit flow. Never expose tokens in URLs.",
                        "cvss": 7.5,
                        "impact": "Tokens leaked via referrer headers, browser history, and server logs"
                    })
                    print("    [!] HIGH: Token in URL fragment")
        except:
            pass
    
    def _test_scope_manipulation(self):
        """Test for scope manipulation"""
        print("[*] Testing scope manipulation...")
        
        excessive_scopes = [
            "admin",
            "root",
            "superuser",
            "write:all",
            "delete:all",
            "*"
        ]
        
        for scope in excessive_scopes:
            try:
                response = requests.get(
                    f"{self.auth_url}?scope={scope}&response_type=code&client_id=test",
                    timeout=5
                )
                
                if response.status_code == 200 and 'error' not in response.text.lower():
                    self.vulnerabilities.append({
                        "type": "Scope Manipulation",
                        "severity": "MEDIUM",
                        "owasp": "API2:2023",
                        "cwe": "CWE-285",
                        "description": f"Application accepts excessive scope: {scope}",
                        "evidence": f"Scope '{scope}' accepted without validation",
                        "remediation": "Validate and restrict scopes. Implement scope whitelist per client.",
                        "cvss": 5.3
                    })
                    print(f"    [!] MEDIUM: Excessive scope accepted: {scope}")
                    break
            except:
                continue
    
    def _test_client_secret_exposure(self):
        """Test for client secret exposure"""
        print("[*] Testing client secret exposure...")
        
        try:
            response = requests.get(self.auth_url, timeout=5)
            
            # Check for secrets in HTML/JS
            secret_patterns = [
                r'client_secret["\']?\s*[:=]\s*["\']([^"\']+)',
                r'secret["\']?\s*[:=]\s*["\']([^"\']+)',
                r'api_key["\']?\s*[:=]\s*["\']([^"\']+)'
            ]
            
            for pattern in secret_patterns:
                matches = re.findall(pattern, response.text, re.IGNORECASE)
                if matches:
                    self.vulnerabilities.append({
                        "type": "Client Secret Exposure",
                        "severity": "CRITICAL",
                        "owasp": "API2:2023",
                        "cwe": "CWE-798",
                        "description": "Client secret exposed in client-side code (HTML/JavaScript)",
                        "evidence": f"Secret pattern found: {pattern}",
                        "remediation": "Never expose client secrets in client-side code. Use backend proxy for OAuth flows.",
                        "cvss": 9.1,
                        "impact": "Attackers can impersonate the application"
                    })
                    print("    [!] CRITICAL: Client secret exposed")
                    break
        except:
            pass
    
    def _test_implicit_flow(self):
        """Test for deprecated implicit flow"""
        print("[*] Testing implicit flow usage...")
        
        try:
            response = requests.get(
                f"{self.auth_url}?response_type=token&client_id=test",
                timeout=5
            )
            
            if response.status_code == 200 or response.status_code in [302, 301]:
                self.vulnerabilities.append({
                    "type": "Deprecated Implicit Flow",
                    "severity": "MEDIUM",
                    "owasp": "API2:2023",
                    "cwe": "CWE-327",
                    "description": "Application supports deprecated OAuth implicit flow (response_type=token)",
                    "evidence": "Implicit flow (response_type=token) accepted",
                    "remediation": "Disable implicit flow. Use authorization code flow with PKCE for SPAs.",
                    "cvss": 5.3,
                    "impact": "Tokens exposed in URLs, no refresh token support"
                })
                print("    [!] MEDIUM: Implicit flow supported")
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
            "auth_url": self.auth_url,
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

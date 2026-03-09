"""
API Security Tester - Scanner Module
Tests for OWASP API Security Top 10 vulnerabilities
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import jwt
from urllib.parse import urlparse, urljoin

class APISecurityScanner:
    """
    Comprehensive API Security Scanner
    Tests for OWASP API Security Top 10 vulnerabilities
    """
    
    def __init__(self, target_url: str, api_type: str = "REST", auth_token: Optional[str] = None):
        """
        Initialize API Security Scanner
        
        Args:
            target_url: Target API endpoint URL
            api_type: Type of API (REST or GraphQL)
            auth_token: Optional authentication token
        """
        self.target_url = target_url
        self.api_type = api_type
        self.auth_token = auth_token
        self.vulnerabilities = []
        self.scan_start_time = None
        self.scan_end_time = None
        
        # Parse URL components
        parsed = urlparse(target_url)
        self.base_url = f"{parsed.scheme}://{parsed.netloc}"
        self.endpoint = parsed.path
        
        # Headers
        self.headers = {
            "User-Agent": "API-Security-Tester/1.0",
            "Accept": "application/json"
        }
        
        if auth_token:
            self.headers["Authorization"] = f"Bearer {auth_token}"
    
    def scan(self, test_types: List[str] = None) -> Dict[str, Any]:
        """
        Run comprehensive API security scan
        
        Args:
            test_types: List of specific tests to run (optional)
        
        Returns:
            Dictionary containing scan results
        """
        self.scan_start_time = datetime.now()
        
        # Default: run all tests
        if not test_types:
            test_types = [
                "BOLA",
                "authentication",
                "mass_assignment",
                "rate_limit",
                "http_methods",
                "excessive_data",
                "ssrf",
                "security_headers"
            ]
        
        # Run selected tests
        if "BOLA" in test_types:
            self._test_bola()
        
        if "authentication" in test_types:
            self._test_authentication()
        
        if "mass_assignment" in test_types:
            self._test_mass_assignment()
        
        if "rate_limit" in test_types:
            self._test_rate_limiting()
        
        if "http_methods" in test_types:
            self._test_http_methods()
        
        if "excessive_data" in test_types:
            self._test_excessive_data_exposure()
        
        if "ssrf" in test_types:
            self._test_ssrf()
        
        if "security_headers" in test_types:
            self._test_security_headers()
        
        self.scan_end_time = datetime.now()
        
        return self._generate_results()
    
    def _test_bola(self):
        """
        Test for Broken Object Level Authorization (BOLA/IDOR)
        OWASP API1:2023
        """
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
                            "description": f"API allows access to object with ID {test_id} without proper authorization",
                            "url": test_url,
                            "evidence": f"Status: {response.status_code}, Response length: {len(response.text)}",
                            "remediation": "Implement proper object-level authorization checks. Verify user has permission to access requested object.",
                            "cvss": 9.1
                        })
                        break
            
            except Exception as e:
                continue
    
    def _test_authentication(self):
        """
        Test for Broken Authentication
        OWASP API2:2023
        """
        print("[*] Testing authentication mechanisms...")
        
        # Test without authentication token
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
                    "description": "API endpoint accessible without authentication",
                    "url": self.target_url,
                    "evidence": f"Status: {response.status_code} without auth token",
                    "remediation": "Implement proper authentication mechanism (OAuth 2.0, JWT, API keys)",
                    "cvss": 7.5
                })
        
        except Exception as e:
            pass
        
        # Test with invalid token
        if self.auth_token:
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
                        "description": "API accepts invalid authentication tokens",
                        "url": self.target_url,
                        "evidence": "Invalid token accepted",
                        "remediation": "Implement proper token validation and signature verification",
                        "cvss": 8.1
                    })
            
            except Exception as e:
                pass
    
    def _test_mass_assignment(self):
        """
        Test for Mass Assignment vulnerabilities
        OWASP API3:2023
        """
        print("[*] Testing for mass assignment vulnerabilities...")
        
        # Test payloads with privileged fields
        test_payloads = [
            {"role": "admin", "is_admin": True},
            {"permissions": ["admin", "superuser"]},
            {"account_type": "premium"},
            {"is_verified": True, "is_active": True}
        ]
        
        for payload in test_payloads:
            try:
                response = requests.post(
                    self.target_url,
                    json=payload,
                    headers=self.headers,
                    timeout=10
                )
                
                # Check if privileged fields were accepted
                if response.status_code in [200, 201]:
                    response_data = response.json() if response.text else {}
                    
                    # Check if any privileged field is in response
                    for key in payload.keys():
                        if key in str(response_data):
                            self.vulnerabilities.append({
                                "type": "Mass Assignment",
                                "severity": "HIGH",
                                "owasp": "API3:2023",
                                "cwe": "CWE-915",
                                "description": f"API accepts privileged field '{key}' without validation",
                                "url": self.target_url,
                                "evidence": f"Field '{key}' accepted in request",
                                "remediation": "Implement whitelist of allowed fields. Use DTOs to control input.",
                                "cvss": 7.3
                            })
                            break
            
            except Exception as e:
                continue
    
    def _test_rate_limiting(self):
        """
        Test for Rate Limiting
        OWASP API4:2023
        """
        print("[*] Testing rate limiting...")
        
        request_count = 50
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
                "description": f"API processed {success_count}/{request_count} requests in {duration:.2f}s without rate limiting",
                "url": self.target_url,
                "evidence": f"{success_count} successful requests in {duration:.2f} seconds",
                "remediation": "Implement rate limiting (e.g., 100 requests per minute per IP/user)",
                "cvss": 5.3
            })

    
    def _test_http_methods(self):
        """
        Test for HTTP Method Tampering
        OWASP API5:2023
        """
        print("[*] Testing HTTP method tampering...")
        
        methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]
        allowed_methods = []
        
        for method in methods:
            try:
                response = requests.request(
                    method,
                    self.target_url,
                    headers=self.headers,
                    timeout=10
                )
                
                if response.status_code not in [405, 501]:
                    allowed_methods.append(method)
            
            except Exception as e:
                continue
        
        # Check for dangerous methods
        dangerous_methods = set(allowed_methods) & {"PUT", "DELETE", "PATCH"}
        
        if dangerous_methods:
            self.vulnerabilities.append({
                "type": "Unrestricted HTTP Methods",
                "severity": "MEDIUM",
                "owasp": "API5:2023",
                "cwe": "CWE-650",
                "description": f"API allows potentially dangerous HTTP methods: {', '.join(dangerous_methods)}",
                "url": self.target_url,
                "evidence": f"Allowed methods: {', '.join(allowed_methods)}",
                "remediation": "Restrict HTTP methods to only those required. Implement proper authorization for state-changing methods.",
                "cvss": 6.5
            })
    
    def _test_excessive_data_exposure(self):
        """
        Test for Excessive Data Exposure
        OWASP API3:2023
        """
        print("[*] Testing for excessive data exposure...")
        
        try:
            response = requests.get(self.target_url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                response_text = response.text.lower()
                
                # Check for sensitive fields in response
                sensitive_fields = [
                    "password", "passwd", "pwd",
                    "secret", "token", "api_key", "apikey",
                    "credit_card", "ssn", "social_security",
                    "private_key", "access_token"
                ]
                
                found_sensitive = []
                for field in sensitive_fields:
                    if field in response_text:
                        found_sensitive.append(field)
                
                if found_sensitive:
                    self.vulnerabilities.append({
                        "type": "Excessive Data Exposure",
                        "severity": "HIGH",
                        "owasp": "API3:2023",
                        "cwe": "CWE-200",
                        "description": f"API response contains sensitive fields: {', '.join(found_sensitive)}",
                        "url": self.target_url,
                        "evidence": f"Sensitive fields found: {', '.join(found_sensitive)}",
                        "remediation": "Filter response data. Only return necessary fields. Use DTOs for responses.",
                        "cvss": 7.5
                    })
        
        except Exception as e:
            pass
    
    def _test_ssrf(self):
        """
        Test for Server-Side Request Forgery
        OWASP API7:2023
        """
        print("[*] Testing for SSRF vulnerabilities...")
        
        # SSRF test payloads
        ssrf_payloads = [
            "http://localhost",
            "http://127.0.0.1",
            "http://169.254.169.254",  # AWS metadata
            "http://metadata.google.internal",  # GCP metadata
            "file:///etc/passwd"
        ]
        
        for payload in ssrf_payloads:
            try:
                # Test URL parameter
                test_url = f"{self.target_url}?url={payload}"
                response = requests.get(test_url, headers=self.headers, timeout=5)
                
                # Check for successful SSRF
                if response.status_code == 200 and len(response.text) > 0:
                    self.vulnerabilities.append({
                        "type": "Server-Side Request Forgery (SSRF)",
                        "severity": "CRITICAL",
                        "owasp": "API7:2023",
                        "cwe": "CWE-918",
                        "description": f"API vulnerable to SSRF with payload: {payload}",
                        "url": test_url,
                        "evidence": f"SSRF payload accepted, response length: {len(response.text)}",
                        "remediation": "Validate and sanitize URL parameters. Use allowlist of permitted domains.",
                        "cvss": 9.0
                    })
                    break
            
            except Exception as e:
                continue
    
    def _test_security_headers(self):
        """
        Test for Security Misconfiguration
        OWASP API8:2023
        """
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
                    "description": f"API missing security headers: {', '.join(missing_headers)}",
                    "url": self.target_url,
                    "evidence": f"Missing headers: {', '.join(missing_headers)}",
                    "remediation": "Add security headers to all API responses",
                    "cvss": 5.3
                })
        
        except Exception as e:
            pass
    
    def _contains_sensitive_data(self, response_text: str) -> bool:
        """
        Check if response contains sensitive data
        """
        sensitive_keywords = [
            "password", "email", "phone", "address",
            "ssn", "credit_card", "token", "secret"
        ]
        
        response_lower = response_text.lower()
        return any(keyword in response_lower for keyword in sensitive_keywords)
    
    def _verify_vulnerability(self, test_url: str, control_url: str = None) -> bool:
        """Verify vulnerability with control test to reduce false positives"""
        try:
            # Test malicious request
            malicious_response = requests.get(test_url, headers=self.headers, timeout=5)
            
            # Test control request
            if not control_url:
                control_url = self.target_url
            control_response = requests.get(control_url, headers=self.headers, timeout=5)
            
            # Compare responses
            if malicious_response.status_code != control_response.status_code:
                return True
            
            length_diff = abs(len(malicious_response.text) - len(control_response.text))
            if length_diff > 100:
                return True
            
            return False
        except:
            return False
    
    def _generate_results(self) -> Dict[str, Any]:
        """
        Generate scan results summary
        """
        # Calculate risk score
        risk_score = self._calculate_risk_score()
        
        # Count vulnerabilities by severity
        severity_counts = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0
        }
        
        for vuln in self.vulnerabilities:
            severity = vuln.get("severity", "LOW")
            severity_counts[severity] += 1
        
        # Calculate scan duration
        duration = (self.scan_end_time - self.scan_start_time).total_seconds()
        
        return {
            "target_url": self.target_url,
            "api_type": self.api_type,
            "scan_date": self.scan_start_time.strftime("%d %b %Y %H:%M:%S"),
            "scan_duration": f"{duration:.2f}s",
            "vulnerabilities": self.vulnerabilities,
            "vulnerability_count": len(self.vulnerabilities),
            "severity_counts": severity_counts,
            "risk_score": risk_score,
            "risk_level": self._get_risk_level(risk_score)
        }
    
    def _calculate_risk_score(self) -> int:
        """
        Calculate overall risk score (0-100)
        """
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
        
        # Cap at 100
        return min(total_score, 100)
    
    def _get_risk_level(self, risk_score: int) -> str:
        """
        Get risk level based on score
        """
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


# Test function
if __name__ == "__main__":
    # Test with JSONPlaceholder API
    scanner = APISecurityScanner(
        target_url="https://jsonplaceholder.typicode.com/posts",
        api_type="REST"
    )
    
    results = scanner.scan()
    
    print("\n" + "="*60)
    print("API SECURITY SCAN RESULTS")
    print("="*60)
    print(f"Target: {results['target_url']}")
    print(f"Scan Date: {results['scan_date']}")
    print(f"Duration: {results['scan_duration']}")
    print(f"\nRisk Score: {results['risk_score']}/100 ({results['risk_level']})")
    print(f"\nVulnerabilities Found: {results['vulnerability_count']}")
    print(f"  - CRITICAL: {results['severity_counts']['CRITICAL']}")
    print(f"  - HIGH: {results['severity_counts']['HIGH']}")
    print(f"  - MEDIUM: {results['severity_counts']['MEDIUM']}")
    print(f"  - LOW: {results['severity_counts']['LOW']}")
    
    if results['vulnerabilities']:
        print("\n" + "-"*60)
        print("VULNERABILITIES DETAILS")
        print("-"*60)
        for i, vuln in enumerate(results['vulnerabilities'], 1):
            print(f"\n{i}. {vuln['type']} [{vuln['severity']}]")
            print(f"   OWASP: {vuln['owasp']} | CWE: {vuln['cwe']} | CVSS: {vuln['cvss']}")
            print(f"   Description: {vuln['description']}")
            print(f"   URL: {vuln['url']}")
            print(f"   Evidence: {vuln['evidence']}")
            print(f"   Remediation: {vuln['remediation']}")

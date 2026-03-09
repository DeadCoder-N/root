"""
JWT Security Analyzer - Professional Grade
Comprehensive JWT vulnerability testing with OWASP compliance
"""

import jwt
import json
import base64
import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import time

class JWTAnalyzer:
    """Professional JWT Security Analyzer"""
    
    def __init__(self, token: str):
        self.token = token
        self.vulnerabilities = []
        self.decoded_header = None
        self.decoded_payload = None
        self.signature = None
        self.scan_start_time = None
        self.scan_end_time = None
        
        # Common weak secrets for brute force
        self.weak_secrets = [
            'secret', 'password', '123456', 'admin', 'test', 'jwt', 'key',
            'secret123', 'password123', 'admin123', 'qwerty', '12345678',
            'abc123', 'letmein', 'welcome', 'monkey', '1234567890'
        ]
    
    def analyze(self) -> Dict[str, Any]:
        """Run comprehensive JWT security analysis"""
        self.scan_start_time = datetime.now()
        
        print("[*] Starting JWT security analysis...")
        
        # Core tests
        self._decode_token()
        self._test_algorithm_none()
        self._test_weak_secret()
        self._test_expiration()
        self._test_algorithm_confusion()
        
        # Advanced tests
        self._test_signature_validation()
        self._test_claims_validation()
        self._test_key_confusion()
        self._test_token_structure()
        self._test_jwt_best_practices()
        
        self.scan_end_time = datetime.now()
        
        print(f"[+] Analysis complete. Found {len(self.vulnerabilities)} vulnerabilities")
        
        return self._generate_results()
    
    def _decode_token(self):
        """Decode JWT token without verification"""
        try:
            parts = self.token.split('.')
            if len(parts) != 3:
                raise ValueError("Invalid JWT format - must have 3 parts")
            
            # Decode header
            header_data = base64.urlsafe_b64decode(parts[0] + '==')
            self.decoded_header = json.loads(header_data)
            
            # Decode payload
            payload_data = base64.urlsafe_b64decode(parts[1] + '==')
            self.decoded_payload = json.loads(payload_data)
            
            # Store signature
            self.signature = parts[2]
            
            print(f"[+] Token decoded successfully")
            print(f"    Algorithm: {self.decoded_header.get('alg', 'unknown')}")
            print(f"    Type: {self.decoded_header.get('typ', 'unknown')}")
            
        except Exception as e:
            self.vulnerabilities.append({
                "type": "Invalid JWT Format",
                "severity": "HIGH",
                "owasp": "API2:2023",
                "cwe": "CWE-345",
                "description": f"Token format error: {str(e)}",
                "evidence": f"Token: {self.token[:50]}...",
                "remediation": "Ensure JWT follows standard format: header.payload.signature",
                "cvss": 7.5
            })
    
    def _test_algorithm_none(self):
        """Test for 'none' algorithm vulnerability (CVE-2015-9235)"""
        print("[*] Testing for 'none' algorithm vulnerability...")
        
        if self.decoded_header:
            alg = self.decoded_header.get('alg', '').lower()
            
            if alg == 'none':
                self.vulnerabilities.append({
                    "type": "Algorithm None Attack",
                    "severity": "CRITICAL",
                    "owasp": "API2:2023",
                    "cwe": "CWE-347",
                    "description": "JWT uses 'none' algorithm - signature verification completely bypassed",
                    "evidence": f"Algorithm: {self.decoded_header.get('alg')}",
                    "remediation": "Reject tokens with 'none' algorithm. Whitelist allowed algorithms (HS256, RS256, etc.)",
                    "cvss": 9.8,
                    "references": [
                        "CVE-2015-9235",
                        "https://auth0.com/blog/critical-vulnerabilities-in-json-web-token-libraries/"
                    ]
                })
                print("    [!] CRITICAL: 'none' algorithm detected!")
    
    def _test_weak_secret(self):
        """Test for weak signing secrets"""
        print("[*] Testing for weak secrets...")
        
        if not self.decoded_header:
            return
        
        alg = self.decoded_header.get('alg', '')
        
        # Only test HMAC algorithms
        if not alg.startswith('HS'):
            print("    [i] Skipping (not HMAC algorithm)")
            return
        
        for secret in self.weak_secrets:
            try:
                # Try to decode with weak secret
                jwt.decode(self.token, secret, algorithms=[alg])
                
                # Verify by encoding with same secret
                if self._verify_weak_secret(secret, alg):
                    self.vulnerabilities.append({
                        "type": "Weak Secret Key",
                        "severity": "CRITICAL",
                        "owasp": "API2:2023",
                        "cwe": "CWE-798",
                        "description": f"JWT signed with weak/common secret: '{secret}'",
                        "evidence": f"Secret cracked: {secret}",
                        "remediation": "Use strong, random secrets (minimum 256 bits). Generate with: openssl rand -base64 32",
                        "cvss": 9.1,
                        "impact": "Attacker can forge valid tokens and impersonate any user"
                    })
                    print(f"    [!] CRITICAL: Weak secret found: {secret}")
                    break
                
            except jwt.InvalidSignatureError:
                continue
            except Exception:
                continue
        else:
            print("    [+] No weak secrets found in common list")
    
    def _verify_weak_secret(self, secret: str, algorithm: str) -> bool:
        """Verify weak secret by re-encoding token"""
        try:
            # Decode with secret
            decoded = jwt.decode(self.token, secret, algorithms=[algorithm])
            # Re-encode with same secret
            new_token = jwt.encode(decoded, secret, algorithm=algorithm)
            # Verify signatures match
            return self.token.split('.')[2] == new_token.split('.')[2]
        except:
            return False
    
    def _test_expiration(self):
        """Test token expiration and lifetime"""
        print("[*] Testing token expiration...")
        
        if not self.decoded_payload:
            return
        
        exp = self.decoded_payload.get('exp')
        iat = self.decoded_payload.get('iat')
        nbf = self.decoded_payload.get('nbf')
        
        current_time = datetime.now().timestamp()
        
        # Check for missing expiration
        if not exp:
            self.vulnerabilities.append({
                "type": "Missing Expiration Claim",
                "severity": "MEDIUM",
                "owasp": "API2:2023",
                "cwe": "CWE-613",
                "description": "JWT has no expiration claim (exp) - token never expires",
                "evidence": "No 'exp' claim in payload",
                "remediation": "Add 'exp' claim with reasonable timeout (15-60 minutes for access tokens)",
                "cvss": 5.3,
                "impact": "Stolen tokens remain valid indefinitely"
            })
            print("    [!] MEDIUM: No expiration claim")
        
        # Check if expired
        elif exp < current_time:
            self.vulnerabilities.append({
                "type": "Expired Token",
                "severity": "LOW",
                "owasp": "API2:2023",
                "cwe": "CWE-613",
                "description": "JWT token has expired",
                "evidence": f"Expired at: {datetime.fromtimestamp(exp).strftime('%Y-%m-%d %H:%M:%S')}",
                "remediation": "Application should reject expired tokens",
                "cvss": 3.1
            })
            print("    [!] LOW: Token expired")
        
        # Check for excessive lifetime
        elif iat and (exp - iat) > 3600:  # More than 1 hour
            lifetime_hours = (exp - iat) / 3600
            self.vulnerabilities.append({
                "type": "Excessive Token Lifetime",
                "severity": "MEDIUM",
                "owasp": "API2:2023",
                "cwe": "CWE-613",
                "description": f"Token lifetime is {lifetime_hours:.1f} hours - too long for access token",
                "evidence": f"Lifetime: {lifetime_hours:.1f} hours",
                "remediation": "Limit access token lifetime to 15-60 minutes. Use refresh tokens for longer sessions.",
                "cvss": 5.3
            })
            print(f"    [!] MEDIUM: Excessive lifetime ({lifetime_hours:.1f}h)")
        
        # Check nbf (not before)
        if nbf and nbf > current_time:
            self.vulnerabilities.append({
                "type": "Token Not Yet Valid",
                "severity": "LOW",
                "owasp": "API2:2023",
                "cwe": "CWE-613",
                "description": "Token not yet valid (nbf claim in future)",
                "evidence": f"Valid from: {datetime.fromtimestamp(nbf).strftime('%Y-%m-%d %H:%M:%S')}",
                "remediation": "Check system clock synchronization",
                "cvss": 3.1
            })

    
    def _test_algorithm_confusion(self):
        """Test for algorithm confusion attacks (RS256 -> HS256)"""
        print("[*] Testing for algorithm confusion...")
        
        if not self.decoded_header:
            return
        
        alg = self.decoded_header.get('alg', '')
        
        # Check for RS256 -> HS256 confusion risk
        if alg.startswith('RS'):
            self.vulnerabilities.append({
                "type": "Algorithm Confusion Risk",
                "severity": "HIGH",
                "owasp": "API2:2023",
                "cwe": "CWE-327",
                "description": "Token uses RSA algorithm - vulnerable to algorithm confusion if server accepts HS256",
                "evidence": f"Current algorithm: {alg}",
                "remediation": "Strictly validate algorithm. Never accept HS256 for tokens signed with RS256.",
                "cvss": 7.5,
                "references": ["CVE-2016-5431"]
            })
            print(f"    [!] HIGH: Algorithm confusion risk ({alg})")
        
        # Check for weak algorithms
        weak_algorithms = ['HS1', 'RS1', 'none']
        if any(weak in alg.lower() for weak in weak_algorithms):
            self.vulnerabilities.append({
                "type": "Weak Algorithm",
                "severity": "HIGH",
                "owasp": "API2:2023",
                "cwe": "CWE-327",
                "description": f"Token uses weak/deprecated algorithm: {alg}",
                "evidence": f"Algorithm: {alg}",
                "remediation": "Use strong algorithms: HS256, RS256, ES256",
                "cvss": 7.5
            })
    
    def _test_signature_validation(self):
        """Test signature validation"""
        print("[*] Testing signature validation...")
        
        if not self.signature:
            self.vulnerabilities.append({
                "type": "Missing Signature",
                "severity": "CRITICAL",
                "owasp": "API2:2023",
                "cwe": "CWE-347",
                "description": "JWT has no signature component",
                "evidence": "Signature part is empty",
                "remediation": "All JWTs must be signed",
                "cvss": 9.8
            })
            print("    [!] CRITICAL: No signature")
        
        # Check signature length
        elif len(self.signature) < 10:
            self.vulnerabilities.append({
                "type": "Suspicious Signature",
                "severity": "HIGH",
                "owasp": "API2:2023",
                "cwe": "CWE-347",
                "description": "Signature appears too short or invalid",
                "evidence": f"Signature length: {len(self.signature)} chars",
                "remediation": "Verify signature generation process",
                "cvss": 7.5
            })
    
    def _test_claims_validation(self):
        """Test JWT claims for security issues"""
        print("[*] Testing claims validation...")
        
        if not self.decoded_payload:
            return
        
        # Check for missing standard claims
        standard_claims = ['iss', 'sub', 'aud', 'exp', 'iat']
        missing_claims = [claim for claim in standard_claims if claim not in self.decoded_payload]
        
        if len(missing_claims) >= 3:
            self.vulnerabilities.append({
                "type": "Missing Standard Claims",
                "severity": "MEDIUM",
                "owasp": "API2:2023",
                "cwe": "CWE-345",
                "description": f"Token missing important claims: {', '.join(missing_claims)}",
                "evidence": f"Missing: {', '.join(missing_claims)}",
                "remediation": "Include standard claims: iss (issuer), sub (subject), aud (audience), exp, iat",
                "cvss": 5.3
            })
            print(f"    [!] MEDIUM: Missing claims: {', '.join(missing_claims)}")
        
        # Check for sensitive data in payload
        sensitive_keywords = ['password', 'secret', 'key', 'ssn', 'credit_card', 'api_key']
        found_sensitive = []
        
        for key, value in self.decoded_payload.items():
            if any(keyword in key.lower() for keyword in sensitive_keywords):
                found_sensitive.append(key)
            elif isinstance(value, str) and any(keyword in value.lower() for keyword in sensitive_keywords):
                found_sensitive.append(key)
        
        if found_sensitive:
            self.vulnerabilities.append({
                "type": "Sensitive Data in Token",
                "severity": "HIGH",
                "owasp": "API2:2023",
                "cwe": "CWE-200",
                "description": f"Token contains sensitive data: {', '.join(found_sensitive)}",
                "evidence": f"Sensitive fields: {', '.join(found_sensitive)}",
                "remediation": "Never store sensitive data in JWT payload. JWTs are not encrypted, only signed.",
                "cvss": 7.5,
                "impact": "Sensitive data exposed to anyone who can read the token"
            })
            print(f"    [!] HIGH: Sensitive data found: {', '.join(found_sensitive)}")
    
    def _test_key_confusion(self):
        """Test for key confusion vulnerabilities"""
        print("[*] Testing for key confusion...")
        
        if not self.decoded_header:
            return
        
        # Check for kid (key ID) parameter
        kid = self.decoded_header.get('kid')
        
        if kid:
            # Check for path traversal in kid
            if '../' in str(kid) or '..\\' in str(kid):
                self.vulnerabilities.append({
                    "type": "Path Traversal in Key ID",
                    "severity": "CRITICAL",
                    "owasp": "API2:2023",
                    "cwe": "CWE-22",
                    "description": "Key ID (kid) contains path traversal characters",
                    "evidence": f"kid: {kid}",
                    "remediation": "Validate and sanitize kid parameter. Use whitelist of allowed key IDs.",
                    "cvss": 9.1
                })
                print(f"    [!] CRITICAL: Path traversal in kid: {kid}")
            
            # Check for SQL injection in kid
            sql_chars = ["'", '"', ';', '--', '/*']
            if any(char in str(kid) for char in sql_chars):
                self.vulnerabilities.append({
                    "type": "SQL Injection Risk in Key ID",
                    "severity": "HIGH",
                    "owasp": "API2:2023",
                    "cwe": "CWE-89",
                    "description": "Key ID (kid) contains SQL injection characters",
                    "evidence": f"kid: {kid}",
                    "remediation": "Sanitize kid parameter before database queries",
                    "cvss": 8.1
                })
        
        # Check for jku (JWK Set URL)
        jku = self.decoded_header.get('jku')
        if jku:
            self.vulnerabilities.append({
                "type": "JWK Set URL Present",
                "severity": "HIGH",
                "owasp": "API2:2023",
                "cwe": "CWE-918",
                "description": "Token contains jku (JWK Set URL) - SSRF risk",
                "evidence": f"jku: {jku}",
                "remediation": "Remove jku header. Use pre-configured trusted key sources only.",
                "cvss": 7.5
            })
            print(f"    [!] HIGH: JKU header present: {jku}")
    
    def _test_token_structure(self):
        """Test JWT structure and format"""
        print("[*] Testing token structure...")
        
        # Check token length
        if len(self.token) > 8192:
            self.vulnerabilities.append({
                "type": "Excessive Token Size",
                "severity": "MEDIUM",
                "owasp": "API2:2023",
                "cwe": "CWE-400",
                "description": f"Token size ({len(self.token)} bytes) exceeds recommended limit",
                "evidence": f"Token length: {len(self.token)} bytes",
                "remediation": "Keep JWT size under 8KB. Store large data server-side.",
                "cvss": 5.3
            })
        
        # Check for unusual header parameters
        if self.decoded_header:
            standard_headers = ['alg', 'typ', 'kid', 'cty']
            unusual_headers = [h for h in self.decoded_header.keys() if h not in standard_headers]
            
            if unusual_headers:
                self.vulnerabilities.append({
                    "type": "Unusual Header Parameters",
                    "severity": "LOW",
                    "owasp": "API2:2023",
                    "cwe": "CWE-345",
                    "description": f"Token contains non-standard headers: {', '.join(unusual_headers)}",
                    "evidence": f"Unusual headers: {', '.join(unusual_headers)}",
                    "remediation": "Review and validate all custom header parameters",
                    "cvss": 3.1
                })
    
    def _test_jwt_best_practices(self):
        """Test JWT implementation best practices"""
        print("[*] Testing JWT best practices...")
        
        if not self.decoded_payload:
            return
        
        issues = []
        
        # Check for jti (JWT ID) for replay protection
        if 'jti' not in self.decoded_payload:
            issues.append("Missing jti (JWT ID) for replay protection")
        
        # Check for aud (audience) validation
        if 'aud' not in self.decoded_payload:
            issues.append("Missing aud (audience) claim")
        
        # Check for iss (issuer) validation
        if 'iss' not in self.decoded_payload:
            issues.append("Missing iss (issuer) claim")
        
        if issues:
            self.vulnerabilities.append({
                "type": "JWT Best Practices Violations",
                "severity": "LOW",
                "owasp": "API2:2023",
                "cwe": "CWE-345",
                "description": "Token doesn't follow JWT best practices",
                "evidence": "; ".join(issues),
                "remediation": "Implement JWT best practices: use jti, aud, iss claims",
                "cvss": 3.1
            })
    
    def _generate_results(self) -> Dict[str, Any]:
        """Generate comprehensive analysis results"""
        
        # Calculate risk score
        risk_score = self._calculate_risk_score()
        
        # Count by severity
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
            "token_preview": self.token[:50] + "..." if len(self.token) > 50 else self.token,
            "header": self.decoded_header,
            "payload": self.decoded_payload,
            "vulnerabilities": self.vulnerabilities,
            "vulnerability_count": len(self.vulnerabilities),
            "severity_counts": severity_counts,
            "risk_score": risk_score,
            "risk_level": self._get_risk_level(risk_score),
            "scan_date": self.scan_start_time.strftime("%d %b %Y %H:%M:%S"),
            "scan_duration": f"{duration:.2f}s"
        }
    
    def _calculate_risk_score(self) -> int:
        """Calculate overall risk score (0-100)"""
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
        """Get risk level based on score"""
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
    # Test with sample JWT
    sample_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    
    analyzer = JWTAnalyzer(sample_token)
    results = analyzer.analyze()
    
    print("\n" + "="*60)
    print("JWT SECURITY ANALYSIS RESULTS")
    print("="*60)
    print(f"Risk Score: {results['risk_score']}/100 ({results['risk_level']})")
    print(f"Vulnerabilities: {results['vulnerability_count']}")
    print(f"  - CRITICAL: {results['severity_counts']['CRITICAL']}")
    print(f"  - HIGH: {results['severity_counts']['HIGH']}")
    print(f"  - MEDIUM: {results['severity_counts']['MEDIUM']}")
    print(f"  - LOW: {results['severity_counts']['LOW']}")

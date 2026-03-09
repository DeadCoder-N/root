"""JWT Claims Validation Tester"""
import base64
import json
from datetime import datetime
from typing import Dict, List, Any

class ClaimsTester:
    """Test JWT claims for security issues"""
    
    def __init__(self, token: str):
        self.token = token
        self.vulnerabilities = []
        self.decoded_payload = None
        
    def test_all(self) -> List[Dict[str, Any]]:
        """Run all claims tests"""
        self._decode_payload()
        if self.decoded_payload:
            self._test_expiration()
            self._test_missing_claims()
            self._test_sensitive_data()
        return self.vulnerabilities
    
    def _decode_payload(self):
        """Decode JWT payload"""
        try:
            parts = self.token.split('.')
            if len(parts) == 3:
                payload_data = base64.urlsafe_b64decode(parts[1] + '==')
                self.decoded_payload = json.loads(payload_data)
        except Exception:
            pass
    
    def _test_expiration(self):
        """Test token expiration"""
        exp = self.decoded_payload.get('exp')
        iat = self.decoded_payload.get('iat')
        current_time = datetime.now().timestamp()
        
        # Missing expiration
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
        # Expired token
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
        # Excessive lifetime
        elif iat and (exp - iat) > 3600:
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
    
    def _test_missing_claims(self):
        """Test for missing standard claims"""
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
    
    def _test_sensitive_data(self):
        """Test for sensitive data in payload"""
        sensitive_keywords = ['password', 'secret', 'key', 'ssn', 'credit_card', 'api_key', 'token', 'private']
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

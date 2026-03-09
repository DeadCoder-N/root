"""JWT Weak Secret Tester"""
import jwt
import base64
import json
from typing import Dict, List, Any

class SecretTester:
    """Test JWT for weak secrets"""
    
    def __init__(self, token: str):
        self.token = token
        self.vulnerabilities = []
        self.weak_secrets = [
            'secret', 'password', '123456', 'admin', 'test', 'jwt', 'key',
            'secret123', 'password123', 'admin123', 'qwerty', '12345678',
            'abc123', 'letmein', 'welcome', 'monkey', '1234567890',
            'password1', 'secret1', 'test123', 'admin1', 'root', 'toor',
            'changeme', 'default', 'guest', 'user', 'demo', 'sample'
        ]
    
    def test_all(self) -> List[Dict[str, Any]]:
        """Run all secret tests"""
        self._test_weak_secrets()
        return self.vulnerabilities
    
    def _test_weak_secrets(self):
        """Test for weak signing secrets"""
        try:
            parts = self.token.split('.')
            if len(parts) != 3:
                return
            
            # Decode header to get algorithm
            header_data = base64.urlsafe_b64decode(parts[0] + '==')
            header = json.loads(header_data)
            alg = header.get('alg', '')
            
            # Only test HMAC algorithms
            if not alg.startswith('HS'):
                return
            
            # Try each weak secret
            for secret in self.weak_secrets:
                try:
                    # Try to decode with weak secret
                    jwt.decode(self.token, secret, algorithms=[alg])
                    
                    # Verify by re-encoding
                    if self._verify_secret(secret, alg):
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
                        break
                except jwt.InvalidSignatureError:
                    continue
                except Exception:
                    continue
        except Exception:
            pass
    
    def _verify_secret(self, secret: str, algorithm: str) -> bool:
        """Verify weak secret by re-encoding token"""
        try:
            decoded = jwt.decode(self.token, secret, algorithms=[algorithm])
            new_token = jwt.encode(decoded, secret, algorithm=algorithm)
            return self.token.split('.')[2] == new_token.split('.')[2]
        except:
            return False

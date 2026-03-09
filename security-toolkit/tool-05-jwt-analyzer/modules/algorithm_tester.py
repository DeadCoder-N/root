"""JWT Algorithm Vulnerability Tester"""
import jwt
import base64
import json
from typing import Dict, List, Any

class AlgorithmTester:
    """Test JWT algorithm vulnerabilities"""
    
    def __init__(self, token: str):
        self.token = token
        self.vulnerabilities = []
        
    def test_all(self) -> List[Dict[str, Any]]:
        """Run all algorithm tests"""
        self._test_none_algorithm()
        self._test_algorithm_confusion()
        self._test_weak_algorithms()
        return self.vulnerabilities
    
    def _test_none_algorithm(self):
        """Test for 'none' algorithm vulnerability"""
        try:
            parts = self.token.split('.')
            if len(parts) != 3:
                return
            
            # Decode header
            header_data = base64.urlsafe_b64decode(parts[0] + '==')
            header = json.loads(header_data)
            
            alg = header.get('alg', '').lower()
            
            if alg == 'none':
                self.vulnerabilities.append({
                    "type": "Algorithm None Attack",
                    "severity": "CRITICAL",
                    "owasp": "API2:2023",
                    "cwe": "CWE-347",
                    "description": "JWT uses 'none' algorithm - signature verification bypassed",
                    "evidence": f"Algorithm: {header.get('alg')}",
                    "remediation": "Reject tokens with 'none' algorithm. Whitelist HS256, RS256, ES256 only.",
                    "cvss": 9.8,
                    "references": ["CVE-2015-9235"]
                })
        except Exception:
            pass
    
    def _test_algorithm_confusion(self):
        """Test for RS256->HS256 algorithm confusion"""
        try:
            parts = self.token.split('.')
            if len(parts) != 3:
                return
            
            header_data = base64.urlsafe_b64decode(parts[0] + '==')
            header = json.loads(header_data)
            
            alg = header.get('alg', '')
            
            if alg.startswith('RS'):
                self.vulnerabilities.append({
                    "type": "Algorithm Confusion Risk",
                    "severity": "HIGH",
                    "owasp": "API2:2023",
                    "cwe": "CWE-327",
                    "description": f"Token uses {alg} - vulnerable to algorithm confusion if server accepts HS256",
                    "evidence": f"Current algorithm: {alg}",
                    "remediation": "Strictly validate algorithm. Never accept HS256 for RS256 tokens.",
                    "cvss": 7.5,
                    "references": ["CVE-2016-5431"]
                })
        except Exception:
            pass
    
    def _test_weak_algorithms(self):
        """Test for weak/deprecated algorithms"""
        try:
            parts = self.token.split('.')
            if len(parts) != 3:
                return
            
            header_data = base64.urlsafe_b64decode(parts[0] + '==')
            header = json.loads(header_data)
            
            alg = header.get('alg', '').lower()
            weak_algorithms = ['hs1', 'rs1', 'none']
            
            if any(weak in alg for weak in weak_algorithms):
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
        except Exception:
            pass

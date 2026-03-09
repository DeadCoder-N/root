"""Session Security Analyzer"""
import requests
from datetime import datetime

class SessionAnalyzer:
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.vulnerabilities = []
    
    def analyze(self):
        self._test_session_fixation()
        self._test_csrf_protection()
        self._test_cookie_flags()
        return {
            "target_url": self.target_url,
            "vulnerabilities": self.vulnerabilities,
            "vulnerability_count": len(self.vulnerabilities),
            "scan_date": datetime.now().strftime("%d %b %Y %H:%M:%S")
        }
    
    def _test_session_fixation(self):
        try:
            r1 = requests.get(self.target_url, timeout=5)
            session_id = r1.cookies.get('sessionid') or r1.cookies.get('PHPSESSID')
            if session_id and self._verify_session_fixation(session_id):
                self.vulnerabilities.append({
                    "type": "Session Fixation",
                    "severity": "HIGH",
                    "cwe": "CWE-384",
                    "description": "Session not regenerated",
                    "cvss": 7.5,
                    "remediation": "Regenerate session ID after authentication"
                })
        except:
            pass
    
    def _verify_session_fixation(self, session_id: str) -> bool:
        """Verify session fixation with control test"""
        try:
            r2 = requests.get(self.target_url, cookies={'sessionid': session_id}, timeout=5)
            r3 = requests.get(self.target_url, timeout=5)
            return r2.status_code == 200 and r3.status_code == 200
        except:
            return False
    
    def _test_csrf_protection(self):
        try:
            response = requests.get(self.target_url, timeout=5)
            if 'csrf' not in response.text.lower():
                self.vulnerabilities.append({
                    "type": "Missing CSRF Protection",
                    "severity": "HIGH",
                    "cwe": "CWE-352",
                    "description": "No CSRF token found",
                    "cvss": 8.1
                })
        except:
            pass
    
    def _test_cookie_flags(self):
        try:
            response = requests.get(self.target_url, timeout=5)
            for cookie in response.cookies:
                if not cookie.secure:
                    self.vulnerabilities.append({
                        "type": "Insecure Cookie",
                        "severity": "MEDIUM",
                        "cwe": "CWE-614",
                        "description": f"Cookie '{cookie.name}' missing Secure flag",
                        "cvss": 5.3
                    })
        except:
            pass

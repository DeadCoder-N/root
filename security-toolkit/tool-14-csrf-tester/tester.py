"""CSRF Security Tester"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from modules.cors_tester import CORSTester

class CSRFTester:
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.vulnerabilities = []
        self.cors_tester = CORSTester()
    
    def test(self):
        self._test_csrf_token()
        self._test_samesite_cookie()
        self._test_referer_validation()
        self._test_cors()
        return {
            "target_url": self.target_url,
            "vulnerabilities": self.vulnerabilities,
            "vulnerability_count": len(self.vulnerabilities),
            "scan_date": datetime.now().strftime("%d %b %Y %H:%M:%S")
        }
    
    def _test_csrf_token(self):
        """Test for CSRF token presence"""
        try:
            response = requests.get(self.target_url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            forms = soup.find_all('form')
            for form in forms:
                csrf_found = False
                for input_tag in form.find_all('input'):
                    if 'csrf' in input_tag.get('name', '').lower():
                        csrf_found = True
                        break
                
                if not csrf_found:
                    self.vulnerabilities.append({
                        "type": "Missing CSRF Token",
                        "severity": "HIGH",
                        "cwe": "CWE-352",
                        "description": "Form without CSRF protection found",
                        "cvss": 8.1
                    })
                    break
        except:
            pass
    
    def _test_samesite_cookie(self):
        """Test SameSite cookie attribute"""
        try:
            response = requests.get(self.target_url, timeout=5)
            for cookie in response.cookies:
                if not cookie.has_nonstandard_attr('SameSite'):
                    self.vulnerabilities.append({
                        "type": "Missing SameSite Attribute",
                        "severity": "MEDIUM",
                        "cwe": "CWE-352",
                        "description": f"Cookie '{cookie.name}' missing SameSite attribute",
                        "cvss": 5.3
                    })
        except:
            pass
    
    def _test_referer_validation(self):
        """Test Referer header validation"""
        try:
            # Try POST without Referer
            response = requests.post(
                self.target_url,
                data={'test': 'data'},
                headers={'Referer': 'http://evil.com'},
                timeout=5
            )
            if response.status_code in [200, 201] and self._verify_csrf_vulnerability():
                self.vulnerabilities.append({
                    "type": "Weak Referer Validation",
                    "severity": "MEDIUM",
                    "cwe": "CWE-352",
                    "description": "Server accepts requests from external referers",
                    "cvss": 5.3,
                    "remediation": "Validate Referer header. Use CSRF tokens. Set SameSite=Strict on cookies."
                })
        except:
            pass
    
    def _verify_csrf_vulnerability(self) -> bool:
        """Verify CSRF vulnerability with control test"""
        try:
            # Test with valid referer
            response = requests.post(self.target_url, data={'test': 'data'}, timeout=5)
            return response.status_code in [200, 201]
        except:
            return True
    
    def _test_cors(self):
        """Test CORS policy configuration"""
        cors_vulns = self.cors_tester.test_cors_policy(self.target_url)
        self.vulnerabilities.extend(cors_vulns)
        
        preflight_vulns = self.cors_tester.test_preflight_bypass(self.target_url)
        self.vulnerabilities.extend(preflight_vulns)

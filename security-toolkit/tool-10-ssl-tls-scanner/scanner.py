"""SSL/TLS Security Scanner"""
import ssl
import socket
from datetime import datetime
from urllib.parse import urlparse

class SSLScanner:
    def __init__(self, target_url: str):
        self.target_url = target_url
        parsed = urlparse(target_url)
        self.hostname = parsed.netloc or parsed.path
        self.port = 443
        self.vulnerabilities = []
    
    def scan(self):
        self._test_certificate()
        self._test_protocols()
        self._test_ciphers()
        return {
            "target_url": self.target_url,
            "hostname": self.hostname,
            "vulnerabilities": self.vulnerabilities,
            "vulnerability_count": len(self.vulnerabilities),
            "scan_date": datetime.now().strftime("%d %b %Y %H:%M:%S")
        }
    
    def _test_certificate(self):
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.hostname, self.port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=self.hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Check expiration
                    not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    if not_after < datetime.now() and self._verify_cert_expiration(cert):
                        self.vulnerabilities.append({
                            "type": "Expired Certificate",
                            "severity": "CRITICAL",
                            "cwe": "CWE-295",
                            "description": "SSL certificate has expired",
                            "cvss": 9.1,
                            "remediation": "Renew SSL certificate immediately. Use Let's Encrypt for free certificates."
                        })
        except Exception as e:
            self.vulnerabilities.append({
                "type": "SSL Connection Error",
                "severity": "HIGH",
                "cwe": "CWE-295",
                "description": f"SSL error: {str(e)}",
                "cvss": 7.5
            })
    
    def _verify_cert_expiration(self, cert) -> bool:
        """Verify certificate expiration"""
        try:
            not_before = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
            return not_before < datetime.now()
        except:
            return True
    
    def _test_protocols(self):
        weak_protocols = [ssl.PROTOCOL_SSLv2, ssl.PROTOCOL_SSLv3, ssl.PROTOCOL_TLSv1, ssl.PROTOCOL_TLSv1_1]
        for protocol in weak_protocols:
            try:
                context = ssl.SSLContext(protocol)
                with socket.create_connection((self.hostname, self.port), timeout=5) as sock:
                    with context.wrap_socket(sock, server_hostname=self.hostname) as ssock:
                        self.vulnerabilities.append({
                            "type": "Weak SSL/TLS Protocol",
                            "severity": "HIGH",
                            "cwe": "CWE-327",
                            "description": f"Server supports weak protocol: {protocol}",
                            "cvss": 7.5
                        })
            except:
                pass
    
    def _test_ciphers(self):
        weak_ciphers = ['RC4', 'DES', '3DES', 'MD5']
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.hostname, self.port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=self.hostname) as ssock:
                    cipher = ssock.cipher()
                    if cipher and any(weak in cipher[0] for weak in weak_ciphers):
                        self.vulnerabilities.append({
                            "type": "Weak Cipher Suite",
                            "severity": "MEDIUM",
                            "cwe": "CWE-327",
                            "description": f"Weak cipher in use: {cipher[0]}",
                            "cvss": 5.3
                        })
        except:
            pass

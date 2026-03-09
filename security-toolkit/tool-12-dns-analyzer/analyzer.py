"""DNS Security Analyzer"""
import dns.resolver
import dns.zone
from datetime import datetime

class DNSAnalyzer:
    def __init__(self, domain: str):
        self.domain = domain
        self.vulnerabilities = []
        self.records = {}
    
    def analyze(self):
        self._check_dnssec()
        self._check_spf()
        self._check_dmarc()
        self._check_zone_transfer()
        return {
            "domain": self.domain,
            "records": self.records,
            "vulnerabilities": self.vulnerabilities,
            "vulnerability_count": len(self.vulnerabilities),
            "scan_date": datetime.now().strftime("%d %b %Y %H:%M:%S")
        }
    
    def _check_dnssec(self):
        try:
            answers = dns.resolver.resolve(self.domain, 'DNSKEY')
            self.records['DNSSEC'] = 'Enabled'
        except:
            self.vulnerabilities.append({
                "type": "Missing DNSSEC",
                "severity": "MEDIUM",
                "cwe": "CWE-300",
                "description": "DNSSEC not configured",
                "cvss": 5.3
            })
    
    def _check_spf(self):
        try:
            answers = dns.resolver.resolve(self.domain, 'TXT')
            spf_found = any('v=spf1' in str(rdata) for rdata in answers)
            if not spf_found:
                self.vulnerabilities.append({
                    "type": "Missing SPF Record",
                    "severity": "MEDIUM",
                    "cwe": "CWE-358",
                    "description": "No SPF record found",
                    "cvss": 5.3
                })
        except:
            pass
    
    def _check_dmarc(self):
        try:
            answers = dns.resolver.resolve(f'_dmarc.{self.domain}', 'TXT')
            self.records['DMARC'] = str(answers[0])
        except:
            self.vulnerabilities.append({
                "type": "Missing DMARC",
                "severity": "MEDIUM",
                "cwe": "CWE-358",
                "description": "No DMARC policy found",
                "cvss": 5.3
            })
    
    def _check_zone_transfer(self):
        try:
            ns_records = dns.resolver.resolve(self.domain, 'NS')
            for ns in ns_records:
                try:
                    zone = dns.zone.from_xfr(dns.query.xfr(str(ns), self.domain))
                    if self._verify_zone_transfer(str(ns)):
                        self.vulnerabilities.append({
                            "type": "Zone Transfer Enabled",
                            "severity": "HIGH",
                            "cwe": "CWE-200",
                            "description": f"Zone transfer allowed on {ns}",
                            "cvss": 7.5,
                            "remediation": "Disable zone transfers. Allow only trusted secondary DNS servers."
                        })
                except:
                    pass
        except:
            pass
    
    def _verify_zone_transfer(self, nameserver: str) -> bool:
        """Verify zone transfer is actually enabled"""
        try:
            zone = dns.zone.from_xfr(dns.query.xfr(nameserver, self.domain, timeout=5))
            return len(zone.nodes) > 0
        except:
            return False

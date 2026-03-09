"""Port Scanner"""
import nmap
from datetime import datetime

class PortScanner:
    def __init__(self, target: str):
        self.target = target
        self.vulnerabilities = []
        self.open_ports = []
    
    def scan(self, ports='1-1000'):
        try:
            nm = nmap.PortScanner()
            nm.scan(self.target, ports)
            
            for host in nm.all_hosts():
                for proto in nm[host].all_protocols():
                    ports_list = nm[host][proto].keys()
                    for port in ports_list:
                        state = nm[host][proto][port]['state']
                        if state == 'open':
                            self.open_ports.append({
                                "port": port,
                                "state": state,
                                "service": nm[host][proto][port].get('name', 'unknown')
                            })
                            
                            # Check for risky ports
                            if port in [21, 23, 3389] and self._verify_risky_port(host, port, proto, nm):
                                self.vulnerabilities.append({
                                    "type": "Risky Port Open",
                                    "severity": "HIGH",
                                    "cwe": "CWE-16",
                                    "description": f"Port {port} ({nm[host][proto][port].get('name')}) is open",
                                    "cvss": 7.5,
                                    "remediation": "Close unnecessary ports. Use firewall rules. Disable unused services."
                                })
        except Exception as e:
            self.vulnerabilities.append({
                "type": "Scan Error",
                "severity": "LOW",
                "description": str(e),
                "cvss": 0
            })
        
        return {
            "target": self.target,
            "open_ports": self.open_ports,
            "vulnerabilities": self.vulnerabilities,
            "vulnerability_count": len(self.vulnerabilities),
            "scan_date": datetime.now().strftime("%d %b %Y %H:%M:%S")
        }
    
    def _verify_risky_port(self, host, port, proto, nm) -> bool:
        """Verify port is actually risky by checking service"""
        try:
            service = nm[host][proto][port].get('name', '')
            return service in ['ftp', 'telnet', 'ms-wbt-server']
        except:
            return True

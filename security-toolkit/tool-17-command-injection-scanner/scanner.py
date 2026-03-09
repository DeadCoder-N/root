"""Command Injection & Path Traversal Scanner"""

from modules.command_injection_tester import CommandInjectionTester
from modules.path_traversal_tester import PathTraversalTester
from datetime import datetime
import time

class CommandInjectionScanner:
    def __init__(self, target_url):
        self.target_url = target_url
        self.cmd_tester = CommandInjectionTester()
        self.path_tester = PathTraversalTester()
    
    def scan(self):
        """Run all tests"""
        start_time = time.time()
        
        results = {
            'target_url': self.target_url,
            'vulnerabilities': [],
            'scan_date': datetime.now().strftime('%d %b %Y %H:%M:%S'),
            'scan_duration': '0s',
            'total_vulnerabilities': 0,
            'vulnerability_count': 0,
            'severity_counts': {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        }
        
        # Test command injection
        cmd_vulns = self.cmd_tester.test_command_injection(self.target_url)
        results['vulnerabilities'].extend(cmd_vulns)
        
        # Test path traversal
        path_vulns = self.path_tester.test_path_traversal(self.target_url)
        results['vulnerabilities'].extend(path_vulns)
        
        # Test LFI
        lfi_vulns = self.path_tester.test_lfi(self.target_url)
        results['vulnerabilities'].extend(lfi_vulns)
        
        # Calculate totals
        results['total_vulnerabilities'] = len(results['vulnerabilities'])
        results['vulnerability_count'] = len(results['vulnerabilities'])
        
        for vuln in results['vulnerabilities']:
            severity = vuln.get('severity', 'LOW')
            results['severity_counts'][severity] += 1
        
        # Calculate duration
        duration = time.time() - start_time
        results['scan_duration'] = f"{duration:.2f}s"
        
        return results

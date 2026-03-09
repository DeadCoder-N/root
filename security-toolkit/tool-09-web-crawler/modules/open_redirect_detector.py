"""Open Redirect Detection Module"""

class OpenRedirectDetector:
    def __init__(self):
        self.name = "Open Redirect Detector"
        self.redirect_params = ['url', 'redirect', 'next', 'return', 'goto', 'target', 'dest', 'destination', 'redir', 'redirect_uri', 'continue']
    
    def test_open_redirect(self, url):
        """Test for open redirect vulnerabilities"""
        import requests
        from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
        
        vulnerabilities = []
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        # Test payloads
        payloads = [
            'https://evil.com',
            '//evil.com',
            'https:evil.com',
            '\\\\evil.com',
            '@evil.com',
            'javascript:alert(1)'
        ]
        
        for param in self.redirect_params:
            if param in params or '?' in url:
                for payload in payloads:
                    test_params = params.copy()
                    test_params[param] = [payload]
                    test_query = urlencode(test_params, doseq=True)
                    test_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, test_query, parsed.fragment))
                    
                    try:
                        response = requests.get(test_url, allow_redirects=False, timeout=10)
                        location = response.headers.get('Location', '')
                        
                        if 'evil.com' in location or payload in location:
                            vulnerabilities.append({
                                'type': 'Open Redirect',
                                'severity': 'MEDIUM',
                                'description': f'Parameter {param} vulnerable to open redirect',
                                'evidence': f'Redirects to: {location}',
                                'url': test_url
                            })
                            break
                    except Exception:
                        pass
        
        return vulnerabilities

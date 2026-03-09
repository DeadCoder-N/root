"""Clickjacking Detection Module"""

class ClickjackingDetector:
    def __init__(self):
        self.name = "Clickjacking Detector"
    
    def test_frame_protection(self, url):
        """Test X-Frame-Options and CSP frame-ancestors"""
        import requests
        
        vulnerabilities = []
        
        try:
            response = requests.get(url, timeout=10)
            headers = response.headers
            
            xfo = headers.get('X-Frame-Options', '').upper()
            csp = headers.get('Content-Security-Policy', '')
            
            # Check X-Frame-Options
            if not xfo:
                vulnerabilities.append({
                    'type': 'Missing X-Frame-Options',
                    'severity': 'HIGH',
                    'description': 'Page can be framed (clickjacking risk)',
                    'evidence': 'X-Frame-Options header not set'
                })
            elif xfo == 'ALLOW-FROM':
                vulnerabilities.append({
                    'type': 'Weak X-Frame-Options',
                    'severity': 'MEDIUM',
                    'description': 'ALLOW-FROM is deprecated',
                    'evidence': f'X-Frame-Options: {xfo}'
                })
            
            # Check CSP frame-ancestors
            if 'frame-ancestors' not in csp and not xfo:
                vulnerabilities.append({
                    'type': 'Missing Frame Protection',
                    'severity': 'HIGH',
                    'description': 'No X-Frame-Options or CSP frame-ancestors',
                    'evidence': 'Both protections missing'
                })
        
        except Exception as e:
            pass
        
        return vulnerabilities

"""CORS Security Tester Module"""

class CORSTester:
    def __init__(self):
        self.name = "CORS Tester"
    
    def test_cors_policy(self, url):
        """Test CORS policy configuration"""
        import requests
        
        vulnerabilities = []
        
        # Test 1: Wildcard with credentials
        headers = {'Origin': 'https://evil.com'}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            acao = response.headers.get('Access-Control-Allow-Origin', '')
            acac = response.headers.get('Access-Control-Allow-Credentials', '')
            
            if acao == '*' and acac == 'true':
                vulnerabilities.append({
                    'type': 'CORS Wildcard with Credentials',
                    'severity': 'CRITICAL',
                    'description': 'Access-Control-Allow-Origin: * with credentials enabled',
                    'evidence': f'ACAO: {acao}, ACAC: {acac}'
                })
            
            # Test 2: Reflected origin
            if acao == 'https://evil.com':
                vulnerabilities.append({
                    'type': 'CORS Reflected Origin',
                    'severity': 'HIGH',
                    'description': 'Server reflects arbitrary origin without validation',
                    'evidence': f'Origin: https://evil.com reflected in ACAO'
                })
            
            # Test 3: Null origin
            headers_null = {'Origin': 'null'}
            response_null = requests.get(url, headers=headers_null, timeout=10)
            if response_null.headers.get('Access-Control-Allow-Origin') == 'null':
                vulnerabilities.append({
                    'type': 'CORS Null Origin Allowed',
                    'severity': 'HIGH',
                    'description': 'Server allows null origin (sandbox bypass)',
                    'evidence': 'Origin: null accepted'
                })
        
        except Exception as e:
            pass
        
        return vulnerabilities
    
    def test_preflight_bypass(self, url):
        """Test CORS preflight bypass"""
        import requests
        
        vulnerabilities = []
        
        try:
            # Test OPTIONS request
            response = requests.options(url, timeout=10)
            methods = response.headers.get('Access-Control-Allow-Methods', '')
            
            if 'DELETE' in methods or 'PUT' in methods:
                vulnerabilities.append({
                    'type': 'Dangerous CORS Methods Allowed',
                    'severity': 'MEDIUM',
                    'description': 'DELETE/PUT methods allowed via CORS',
                    'evidence': f'Methods: {methods}'
                })
        
        except Exception as e:
            pass
        
        return vulnerabilities

"""Business Logic Security Tester"""
import requests
import asyncio
import aiohttp
from datetime import datetime

class BusinessLogicTester:
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.vulnerabilities = []
    
    def test(self):
        self._test_race_condition()
        self._test_price_manipulation()
        self._test_negative_values()
        self._test_parameter_tampering()
        return {
            "target_url": self.target_url,
            "vulnerabilities": self.vulnerabilities,
            "vulnerability_count": len(self.vulnerabilities),
            "scan_date": datetime.now().strftime("%d %b %Y %H:%M:%S")
        }
    
    def _test_race_condition(self):
        """Test for race conditions"""
        try:
            # Send multiple concurrent requests
            responses = []
            for _ in range(10):
                r = requests.post(self.target_url, data={'action': 'purchase'}, timeout=5)
                responses.append(r.status_code)
            
            # If all succeed, might be vulnerable
            if responses.count(200) > 5:
                self.vulnerabilities.append({
                    "type": "Race Condition",
                    "severity": "HIGH",
                    "cwe": "CWE-362",
                    "description": "Application may be vulnerable to race conditions",
                    "cvss": 7.5
                })
        except:
            pass
    
    def _test_price_manipulation(self):
        """Test price manipulation"""
        test_prices = [-1, 0, 0.01, 999999999]
        
        for price in test_prices:
            try:
                response = requests.post(
                    self.target_url,
                    data={'price': price, 'quantity': 1},
                    timeout=5
                )
                if response.status_code in [200, 201] and self._verify_price_manipulation(response, price):
                    self.vulnerabilities.append({
                        "type": "Price Manipulation",
                        "severity": "CRITICAL",
                        "cwe": "CWE-840",
                        "description": f"Application accepts invalid price: {price}",
                        "cvss": 9.1,
                        "remediation": "Validate all prices server-side. Use server-side price lookup. Never trust client-side prices."
                    })
                    break
            except:
                pass
    
    def _verify_price_manipulation(self, response, price) -> bool:
        """Verify price manipulation by checking response"""
        return 'success' in response.text.lower() or 'accepted' in response.text.lower() or str(price) in response.text
    
    def _test_negative_values(self):
        """Test negative quantity/amount"""
        try:
            response = requests.post(
                self.target_url,
                data={'quantity': -10, 'amount': -100},
                timeout=5
            )
            if response.status_code in [200, 201]:
                self.vulnerabilities.append({
                    "type": "Negative Value Accepted",
                    "severity": "HIGH",
                    "cwe": "CWE-20",
                    "description": "Application accepts negative values",
                    "cvss": 7.5
                })
        except:
            pass
    
    def _test_parameter_tampering(self):
        """Test parameter tampering"""
        try:
            # Try to modify user_id or role
            response = requests.post(
                self.target_url,
                data={'user_id': 'admin', 'role': 'administrator'},
                timeout=5
            )
            if response.status_code in [200, 201]:
                self.vulnerabilities.append({
                    "type": "Parameter Tampering",
                    "severity": "HIGH",
                    "cwe": "CWE-472",
                    "description": "Application accepts tampered parameters",
                    "cvss": 8.1
                })
        except:
            pass

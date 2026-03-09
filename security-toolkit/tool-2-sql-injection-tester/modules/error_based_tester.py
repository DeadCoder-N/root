"""
Error-Based SQL Injection Tester Module
Tests for SQL injection vulnerabilities using error-based techniques
"""
from typing import Dict, List
import requests

class ErrorBasedTester:
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.vulnerabilities = []
        self.payloads = [
            "'", "\"", "' OR '1'='1", "' OR 1=1--", 
            "admin'--", "' UNION SELECT NULL--"
        ]
    
    def test_all(self) -> List[Dict]:
        """Run all error-based SQL injection tests"""
        for payload in self.payloads:
            result = self._test_payload(payload)
            if result:
                self.vulnerabilities.append(result)
        return self.vulnerabilities
    
    def _test_payload(self, payload: str) -> Dict:
        """Test single payload"""
        try:
            response = requests.get(f"{self.target_url}?id={payload}", timeout=5)
            if self._check_sql_error(response.text):
                return {
                    'type': 'Error-Based SQL Injection',
                    'severity': 'CRITICAL',
                    'payload': payload,
                    'evidence': 'SQL error detected in response'
                }
        except:
            pass
        return None
    
    def _check_sql_error(self, response: str) -> bool:
        """Check for SQL error messages"""
        errors = ['sql syntax', 'mysql_fetch', 'pg_query', 'sqlite_', 'ORA-']
        return any(err.lower() in response.lower() for err in errors)

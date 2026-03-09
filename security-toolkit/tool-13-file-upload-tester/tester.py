"""File Upload Security Tester"""
import requests
from datetime import datetime
import io

class FileUploadTester:
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.vulnerabilities = []
    
    def test(self):
        self._test_executable_upload()
        self._test_double_extension()
        self._test_mime_bypass()
        self._test_path_traversal()
        return {
            "target_url": self.target_url,
            "vulnerabilities": self.vulnerabilities,
            "vulnerability_count": len(self.vulnerabilities),
            "scan_date": datetime.now().strftime("%d %b %Y %H:%M:%S")
        }
    
    def _test_executable_upload(self):
        """Test if executable files are accepted"""
        test_files = [
            ('test.php', b'<?php echo "test"; ?>'),
            ('test.jsp', b'<% out.println("test"); %>'),
            ('test.exe', b'MZ\x90\x00')
        ]
        
        for filename, content in test_files:
            try:
                files = {'file': (filename, io.BytesIO(content))}
                response = requests.post(self.target_url, files=files, timeout=5)
                if response.status_code in [200, 201] and self._verify_file_upload(response, filename):
                    self.vulnerabilities.append({
                        "type": "Unrestricted File Upload",
                        "severity": "CRITICAL",
                        "cwe": "CWE-434",
                        "description": f"Executable file accepted: {filename}",
                        "cvss": 9.8,
                        "remediation": "Validate file extensions. Check magic bytes. Store uploads outside web root. Rename files."
                    })
                    break
            except:
                pass
    
    def _verify_file_upload(self, response, filename: str) -> bool:
        """Verify file was actually uploaded, not rejected"""
        return 'success' in response.text.lower() or 'uploaded' in response.text.lower() or filename in response.text
    
    def _test_double_extension(self):
        """Test double extension bypass"""
        try:
            files = {'file': ('test.php.jpg', io.BytesIO(b'<?php echo "test"; ?>'))}
            response = requests.post(self.target_url, files=files, timeout=5)
            if response.status_code in [200, 201]:
                self.vulnerabilities.append({
                    "type": "Double Extension Bypass",
                    "severity": "HIGH",
                    "cwe": "CWE-434",
                    "description": "Double extension bypass possible",
                    "cvss": 8.1
                })
        except:
            pass
    
    def _test_mime_bypass(self):
        """Test MIME type bypass"""
        try:
            files = {'file': ('test.php', io.BytesIO(b'<?php echo "test"; ?>'), 'image/jpeg')}
            response = requests.post(self.target_url, files=files, timeout=5)
            if response.status_code in [200, 201]:
                self.vulnerabilities.append({
                    "type": "MIME Type Bypass",
                    "severity": "HIGH",
                    "cwe": "CWE-434",
                    "description": "MIME type validation can be bypassed",
                    "cvss": 7.5
                })
        except:
            pass
    
    def _test_path_traversal(self):
        """Test path traversal in filename"""
        try:
            files = {'file': ('../../test.txt', io.BytesIO(b'test'))}
            response = requests.post(self.target_url, files=files, timeout=5)
            if response.status_code in [200, 201]:
                self.vulnerabilities.append({
                    "type": "Path Traversal",
                    "severity": "HIGH",
                    "cwe": "CWE-22",
                    "description": "Path traversal in filename possible",
                    "cvss": 7.5
                })
        except:
            pass

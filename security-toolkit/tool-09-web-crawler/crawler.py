"""Web Crawler & Security Scanner"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime
from modules.clickjacking_detector import ClickjackingDetector
from modules.open_redirect_detector import OpenRedirectDetector

class WebCrawler:
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.vulnerabilities = []
        self.visited = set()
        self.found_urls = []
        self.clickjacking_detector = ClickjackingDetector()
        self.redirect_detector = OpenRedirectDetector()
    
    def crawl(self, max_pages=50):
        self._crawl_page(self.target_url, max_pages)
        self._test_sensitive_files()
        self._test_directory_listing()
        self._test_clickjacking()
        self._test_open_redirects()
        return {
            "target_url": self.target_url,
            "pages_crawled": len(self.visited),
            "urls_found": len(self.found_urls),
            "vulnerabilities": self.vulnerabilities,
            "vulnerability_count": len(self.vulnerabilities),
            "scan_date": datetime.now().strftime("%d %b %Y %H:%M:%S")
        }
    
    def _crawl_page(self, url, max_pages):
        if len(self.visited) >= max_pages or url in self.visited:
            return
        
        try:
            self.visited.add(url)
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for link in soup.find_all('a', href=True):
                full_url = urljoin(url, link['href'])
                if urlparse(full_url).netloc == urlparse(self.target_url).netloc:
                    self.found_urls.append(full_url)
                    if len(self.visited) < max_pages:
                        self._crawl_page(full_url, max_pages)
        except:
            pass
    
    def _test_sensitive_files(self):
        sensitive_files = ['.git/config', '.env', 'backup.sql', '.DS_Store', 'web.config']
        base_url = self.target_url.rstrip('/')
        
        for file in sensitive_files:
            try:
                response = requests.get(f"{base_url}/{file}", timeout=5)
                if response.status_code == 200 and self._verify_sensitive_file(response):
                    self.vulnerabilities.append({
                        "type": "Exposed Sensitive File",
                        "severity": "HIGH",
                        "cwe": "CWE-200",
                        "description": f"Sensitive file exposed: {file}",
                        "url": f"{base_url}/{file}",
                        "cvss": 7.5,
                        "remediation": "Remove sensitive files from web root. Add to .gitignore."
                    })
            except:
                pass
    
    def _verify_sensitive_file(self, response) -> bool:
        """Verify file is actually sensitive content, not 404 page"""
        return len(response.text) > 0 and '404' not in response.text.lower()
    
    def _test_directory_listing(self):
        try:
            response = requests.get(self.target_url, timeout=5)
            if 'Index of /' in response.text or 'Directory listing' in response.text:
                self.vulnerabilities.append({
                    "type": "Directory Listing Enabled",
                    "severity": "MEDIUM",
                    "cwe": "CWE-548",
                    "description": "Directory listing is enabled",
                    "cvss": 5.3
                })
        except:
            pass
    
    def _test_clickjacking(self):
        """Test for clickjacking vulnerabilities"""
        clickjacking_vulns = self.clickjacking_detector.test_frame_protection(self.target_url)
        self.vulnerabilities.extend(clickjacking_vulns)
    
    def _test_open_redirects(self):
        """Test for open redirect vulnerabilities"""
        redirect_vulns = self.redirect_detector.test_open_redirect(self.target_url)
        self.vulnerabilities.extend(redirect_vulns)

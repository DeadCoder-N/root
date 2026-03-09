#!/usr/bin/env python3
"""
Tool 4 Complete Workflow Test
Tests scanner, backend, and PDF generation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scanner import APISecurityScanner
from reports.pdf_generator import APISecurityReportGenerator

def test_complete_workflow():
    """Test complete workflow: scan -> generate PDF"""
    
    print("="*60)
    print("🧪 TESTING TOOL 4 COMPLETE WORKFLOW")
    print("="*60)
    
    # Step 1: Run Scanner
    print("\n[1/3] Testing Scanner...")
    try:
        scanner = APISecurityScanner(
            target_url="https://jsonplaceholder.typicode.com/posts",
            api_type="REST"
        )
        results = scanner.scan(test_types=["authentication", "security_headers", "rate_limit"])
        print(f"✅ Scanner works! Found {results['vulnerability_count']} vulnerabilities")
        print(f"   Risk Score: {results['risk_score']}/100 ({results['risk_level']})")
    except Exception as e:
        print(f"❌ Scanner failed: {e}")
        return False
    
    # Step 2: Add fix prompts (like backend does)
    print("\n[2/3] Adding fix prompts...")
    try:
        for vuln in results['vulnerabilities']:
            vuln_type = vuln.get('type', '')
            if 'Authentication' in vuln_type:
                vuln['fix_prompt'] = "Implement JWT authentication"
                vuln['endpoint'] = results['target_url']
                vuln['method'] = 'GET'
            elif 'Security Header' in vuln_type:
                vuln['fix_prompt'] = "Add security headers"
                vuln['endpoint'] = results['target_url']
                vuln['method'] = 'GET'
            elif 'Rate Limit' in vuln_type:
                vuln['fix_prompt'] = "Implement rate limiting"
                vuln['endpoint'] = results['target_url']
                vuln['method'] = 'GET'
        print("✅ Fix prompts added")
    except Exception as e:
        print(f"❌ Fix prompts failed: {e}")
        return False
    
    # Step 3: Generate PDF Report
    print("\n[3/3] Generating PDF Report...")
    try:
        generator = APISecurityReportGenerator(results)
        pdf_path = generator.generate()
        
        # Check if PDF was created
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path) / 1024  # KB
            print(f"✅ PDF generated successfully!")
            print(f"   Path: {pdf_path}")
            print(f"   Size: {file_size:.2f} KB")
            
            # Verify PDF has content
            if file_size > 10:  # Should be at least 10KB
                print(f"✅ PDF has substantial content ({file_size:.2f} KB)")
            else:
                print(f"⚠️  PDF seems small ({file_size:.2f} KB)")
        else:
            print(f"❌ PDF file not found at {pdf_path}")
            return False
            
    except Exception as e:
        print(f"❌ PDF generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Summary
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)
    print("\n📊 Test Summary:")
    print(f"   ✅ Scanner: Working")
    print(f"   ✅ Fix Prompts: Working")
    print(f"   ✅ PDF Generator: Working")
    print(f"   ✅ PDF File: Created ({file_size:.2f} KB)")
    print("\n🎉 Tool 4 is FULLY FUNCTIONAL!")
    print("="*60)
    
    return True

if __name__ == "__main__":
    success = test_complete_workflow()
    sys.exit(0 if success else 1)

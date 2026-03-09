#!/usr/bin/env python3
"""
Security Assessment Report PDF Generator
Converts markdown security report to professional PDF
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os
import json
import sys
from pathlib import Path

# Import scanner
sys.path.append(str(Path(__file__).parent / 'Vulnerability Scanner'))
from github_scanner import GitHubScanner

def generate_markdown_report(output_filename):
    """Generate markdown version of the report"""
    now = datetime.now()
    md_content = f"""# CYBERSECURITY ASSESSMENT REPORT
## Website: https://deadcoder-n.github.io/root/

**Assessment Date:** {now.strftime('%B %d, %Y')}  
**Assessment Type:** Web Application Security Assessment & Network Analysis  
**Assessed By:** Cybersecurity Analyst & VAPT Expert  
**Overall Risk Level:** 🟡 MEDIUM

---

## EXECUTIVE SUMMARY

This report presents a comprehensive security assessment of the portfolio website. The website is a React-based portfolio showcasing cybersecurity expertise and frontend development skills. The assessment identified **11 vulnerabilities** across multiple categories including information disclosure, dependency risks, and configuration issues.

---

## VULNERABILITY SUMMARY

| Severity | Count | Status |
|----------|-------|--------|
| CRITICAL | 1 | Active |
| HIGH | 4 | Active |
| MEDIUM | 4 | Active |
| LOW | 2 | Active |
| **TOTAL** | **11** | **Active** |

---

## VULNERABILITIES IDENTIFIED

### 1. CRITICAL VULNERABILITIES

#### 1.1 Exposed Personal Information (PII)
**Severity:** CRITICAL | **CWE:** CWE-359

**Description:** The website exposes sensitive personal information including email address (niteshsawardekar972@gmail.com), phone number (+91 8454806491), location (Kalyan, India), and a publicly accessible resume PDF.

**Risk:** Phishing attacks, social engineering, spam, identity theft, and doxxing.

---

### 2. HIGH VULNERABILITIES

#### 2.1 Missing Subresource Integrity (SRI) on CDN Scripts
**Severity:** HIGH | **CWE:** CWE-829

**Issue:** External MediaPipe scripts loaded from CDN without SRI hashes. Vulnerable to Man-in-the-Middle (MITM) attacks and CDN compromise.

#### 2.2 Missing Security Headers
**Severity:** HIGH | **CWE:** CWE-693

**Missing Headers:** Content-Security-Policy, X-Content-Type-Options, X-Frame-Options, Strict-Transport-Security, X-XSS-Protection, Referrer-Policy

#### 2.3 Supabase Credentials Exposure Risk
**Severity:** HIGH | **CWE:** CWE-798

**Issue:** Supabase anon key exposed in environment variables and client-side code. No rate limiting on API calls.

#### 2.4 Outdated Dependencies with Known Vulnerabilities
**Severity:** HIGH | **CWE:** CWE-1104

**Issue:** Dependencies may contain known vulnerabilities. Requires regular auditing and updates.

---

### 3. MEDIUM VULNERABILITIES

#### 3.1 Missing Input Validation & Sanitization
**Severity:** MEDIUM | **CWE:** CWE-79 (XSS)

**Issue:** Contact form lacks input validation and HTML escaping. Potential for stored XSS attacks.

#### 3.2 Insecure Direct Object References (IDOR)
**Severity:** MEDIUM | **CWE:** CWE-639

**Issue:** No row-level security policies visible. Direct database access from frontend without authentication.

#### 3.3 Insufficient Logging & Monitoring
**Severity:** MEDIUM | **CWE:** CWE-778

**Issue:** No security event logging, rate limiting, or bot detection (CAPTCHA).

#### 3.4 Weak Content Security Policy
**Severity:** MEDIUM | **CWE:** CWE-693

**Issue:** No CSP header configured. Inline scripts allowed. External resources unrestricted.

---

### 4. LOW VULNERABILITIES

#### 4.1 Information Disclosure via Metadata
**Severity:** LOW | **CWE:** CWE-200

**Issue:** Author name, professional details, and resume publicly indexed.

#### 4.2 Missing .env File Protection
**Severity:** LOW | **CWE:** CWE-798

**Issue:** .env.example shows structure. Risk of accidental credential exposure.

---

## REMEDIATION SUMMARY

### CRITICAL FIXES (Implement Immediately)

#### 1. Protect Personal Information
**Issue:** Email/phone exposed in Contact.tsx and index.html

**How to Fix:**
- Open src/components/Contact.tsx
- Replace direct email/phone display with contact form only
- Use email obfuscation: Split email into parts or use base64 encoding
- Add password protection to resume PDF or use server-side download

**Prompt:** 'Remove email and phone from Contact component, keep only contact form'

#### 2. Add Subresource Integrity (SRI)
**Issue:** MediaPipe CDN scripts in index.html lack integrity hashes

**How to Fix:**
- Generate SRI hash: curl -s [CDN_URL] | openssl dgst -sha384 -binary | openssl base64 -A
- Add integrity='sha384-[HASH]' and crossorigin='anonymous' to script tags
- Example: <script src='...' integrity='sha384-abc123' crossorigin='anonymous'></script>

**Prompt:** 'Add SRI integrity hashes to all CDN script tags in index.html'

#### 3. Implement Security Headers
**Issue:** Missing security headers in deployment configuration

**How to Fix:**
- For Vercel: Add headers in vercel.json
- For GitHub Pages: Add headers in _headers file or use meta tags
- Required headers: X-Content-Type-Options: nosniff, X-Frame-Options: DENY, X-XSS-Protection: 1; mode=block, Strict-Transport-Security: max-age=31536000

**Prompt:** 'Add security headers to vercel.json: CSP, X-Frame-Options, HSTS, X-Content-Type-Options'

#### 4. Secure Supabase Configuration
**Issue:** No RLS policies, exposed anon key, no rate limiting

**How to Fix:**
- Go to Supabase Dashboard → Authentication → Policies
- Enable RLS on contact_messages table
- Add policy: CREATE for authenticated users only
- Implement rate limiting in Contact.tsx (max 3 submissions per hour)
- Add Google reCAPTCHA v3 to contact form

**Prompt:** 'Enable RLS on Supabase contact_messages table and add rate limiting to contact form'

---

### HIGH PRIORITY FIXES (Within 1 Week)

#### 5. Update Dependencies
**How to Fix:**
- Run: npm audit
- Run: npm audit fix
- Run: npm update
- Check package.json for outdated versions

**Prompt:** 'Run npm audit and update all vulnerable dependencies'

#### 6. Add Input Validation & Sanitization
**How to Fix:**
- Install DOMPurify: npm install dompurify
- In Contact.tsx, add email regex validation
- Sanitize all form inputs before sending to Supabase
- Add max length limits (name: 100, email: 100, message: 1000)

**Prompt:** 'Add input validation and DOMPurify sanitization to Contact form'

#### 7. Implement Content Security Policy
**How to Fix:**
- Add CSP meta tag in index.html head section
- Policy: default-src 'self'; script-src 'self' 'unsafe-inline' cdn.jsdelivr.net; style-src 'self' 'unsafe-inline'
- Or add CSP header in vercel.json

**Prompt:** 'Add Content-Security-Policy meta tag to index.html with strict script-src'

---

### MEDIUM PRIORITY FIXES (Within 2 Weeks)

#### 8. Add CAPTCHA to Contact Form
**How to Fix:**
- Sign up for Google reCAPTCHA v3 at google.com/recaptcha
- Install: npm install react-google-recaptcha-v3
- Add reCAPTCHA script to index.html
- Wrap Contact component with GoogleReCaptchaProvider
- Verify token before form submission

**Prompt:** 'Add Google reCAPTCHA v3 to contact form in Contact.tsx'

#### 9. Implement Logging & Monitoring
**How to Fix:**
- Set up Supabase Edge Functions for logging
- Log all form submissions with timestamp, IP, user agent
- Add error tracking with Sentry: npm install @sentry/react
- Monitor failed submissions and suspicious patterns

**Prompt:** 'Add Sentry error tracking and log all contact form submissions'

#### 10. Enable Row-Level Security (RLS)
**How to Fix:**
- Open Supabase Dashboard → Database → contact_messages table
- Click 'Enable RLS'
- Add policy: CREATE - allow if rate limit not exceeded
- Add policy: SELECT - allow only for authenticated admin users

**Prompt:** 'Create RLS policies for contact_messages table in Supabase'

---

### LOW PRIORITY FIXES (Within 1 Month)

#### 11. Implement .env Security
**How to Fix:**
- Verify .env is in .gitignore
- Use .env.local for local development (not tracked)
- Add Supabase keys to Vercel Environment Variables
- Add keys to GitHub Secrets for GitHub Actions
- Rotate Supabase anon key every 3 months

**Prompt:** 'Move Supabase credentials to Vercel environment variables and GitHub Secrets'

---

## COMPLIANCE & STANDARDS

### OWASP Top 10 Mapping

| OWASP Issue | Status |
|-------------|--------|
| A01:2021 - Broken Access Control | ⚠️ At Risk |
| A02:2021 - Cryptographic Failures | ⚠️ At Risk |
| A03:2021 - Injection | ⚠️ At Risk |
| A04:2021 - Insecure Design | ⚠️ At Risk |
| A05:2021 - Security Misconfiguration | ⚠️ At Risk |
| A06:2021 - Vulnerable Components | ⚠️ At Risk |
| A07:2021 - Authentication Failures | ✓ Compliant |
| A08:2021 - Data Integrity Failures | ⚠️ At Risk |
| A09:2021 - Logging & Monitoring | ⚠️ At Risk |
| A10:2021 - SSRF | ✓ Compliant |

---

### GDPR Compliance Issues

**Issues:** Personal data collection without explicit consent, no privacy policy, no data retention policy, no data deletion mechanism.

**Recommendations:** Add privacy policy, implement consent management, add data deletion functionality, document data processing.

---

## RECOMMENDATIONS & NEXT STEPS

### Immediate Actions (This Week)
1. Protect personal information by removing direct email/phone display
2. Add SRI hashes to all CDN scripts
3. Implement security headers
4. Secure Supabase configuration with RLS and rate limiting

### Short-term Actions (1-2 Weeks)
1. Update all dependencies and run security audits
2. Add input validation and sanitization
3. Implement Content Security Policy
4. Add CAPTCHA to contact form

### Long-term Actions (1 Month+)
1. Implement comprehensive logging and monitoring
2. Set up continuous security scanning (Snyk, GitHub Security)
3. Conduct regular penetration testing
4. Implement GDPR compliance measures
5. Establish incident response procedures

---

## CONCLUSION

The website has 11 identified vulnerabilities ranging from Critical to Low severity. The most critical issues require immediate attention, particularly the exposure of personal information and missing security headers. With proper implementation of the recommended fixes, the security posture can be improved from MEDIUM to HIGH within 2-3 weeks.

**Estimated Remediation Time:** 2-3 weeks for all fixes  
**Overall Security Posture:** MEDIUM (Improving to HIGH after fixes)  
**Next Assessment:** 3 months after remediation

---

**Report Generated:** {now.strftime('%B %d, %Y at %H:%M:%S')}  
**Classification:** CONFIDENTIAL
"""
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"✓ Markdown report generated: {output_filename}")
    return output_filename

def create_security_report_pdf(output_filename=None):
    if output_filename is None:
        now = datetime.now()
        day = now.strftime('%d')
        month = now.strftime('%b').lower()
        year = now.strftime('%Y')
        time_str = now.strftime('%I:%M:%S%p')
        errors_count = 11
        output_filename = f"Report/{day}_{month}_{year}||{time_str}||({errors_count})errors.pdf"
    """Generate comprehensive security assessment PDF report"""
    
    # Create PDF document
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
        title="Security Assessment Report"
    )
    
    # Container for PDF elements
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#0066cc'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#003366'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    
    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontSize=11,
        textColor=colors.HexColor('#333333'),
        spaceAfter=8,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        leading=12
    )
    
    # Title Page
    elements.append(Spacer(1, 1.5*inch))
    elements.append(Paragraph("CYBERSECURITY ASSESSMENT REPORT", title_style))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("Website Security & Vulnerability Assessment", styles['Normal']))
    elements.append(Spacer(1, 0.5*inch))
    
    # Report metadata
    metadata = [
        f"<b>Website:</b> https://deadcoder-n.github.io/root/",
        f"<b>Assessment Date:</b> {datetime.now().strftime('%B %d, %Y')}",
        f"<b>Assessment Type:</b> Web Application Security Assessment & Network Analysis",
        f"<b>Assessed By:</b> Cybersecurity Analyst & VAPT Expert",
        f"<b>Overall Risk Level:</b> <font color='#ff6600'><b>MEDIUM</b></font>"
    ]
    
    for item in metadata:
        elements.append(Paragraph(item, body_style))
        elements.append(Spacer(1, 0.1*inch))
    
    elements.append(PageBreak())
    
    # Executive Summary
    elements.append(Paragraph("EXECUTIVE SUMMARY", heading1_style))
    elements.append(Paragraph(
        "This report presents a comprehensive security assessment of the portfolio website. "
        "The website is a React-based portfolio showcasing cybersecurity expertise and frontend development skills. "
        "The assessment identified <b>11 vulnerabilities</b> across multiple categories including information disclosure, "
        "dependency risks, and configuration issues.",
        body_style
    ))
    elements.append(Spacer(1, 0.2*inch))
    
    # Vulnerability Summary
    elements.append(Paragraph("VULNERABILITY SUMMARY", heading2_style))
    
    vuln_data = [
        ['Severity', 'Count', 'Status'],
        ['CRITICAL', '1', 'Active'],
        ['HIGH', '4', 'Active'],
        ['MEDIUM', '4', 'Active'],
        ['LOW', '2', 'Active'],
        ['TOTAL', '11', 'Active']
    ]
    
    vuln_table = Table(vuln_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
    vuln_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ffcccc')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ]))
    
    elements.append(vuln_table)
    elements.append(Spacer(1, 0.3*inch))
    elements.append(PageBreak())
    
    # Vulnerabilities Section
    elements.append(Paragraph("VULNERABILITIES IDENTIFIED", heading1_style))
    
    # Critical Vulnerabilities
    elements.append(Paragraph("1. CRITICAL VULNERABILITIES", heading2_style))
    
    elements.append(Paragraph("1.1 Exposed Personal Information (PII)", heading3_style))
    elements.append(Paragraph("<b>Severity:</b> CRITICAL | <b>CWE:</b> CWE-359", body_style))
    elements.append(Paragraph(
        "<b>Description:</b> The website exposes sensitive personal information including email address "
        "(niteshsawardekar972@gmail.com), phone number (+91 8454806491), location (Kalyan, India), and a publicly "
        "accessible resume PDF. This information is directly displayed in the contact section and HTML metadata.",
        body_style
    ))
    elements.append(Paragraph(
        "<b>Risk:</b> Phishing attacks, social engineering, spam, identity theft, and doxxing.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))
    
    # High Vulnerabilities
    elements.append(Paragraph("2. HIGH VULNERABILITIES", heading2_style))
    
    elements.append(Paragraph("2.1 Missing Subresource Integrity (SRI) on CDN Scripts", heading3_style))
    elements.append(Paragraph("<b>Severity:</b> HIGH | <b>CWE:</b> CWE-829", body_style))
    elements.append(Paragraph(
        "<b>Issue:</b> External MediaPipe scripts loaded from CDN without SRI hashes. "
        "Vulnerable to Man-in-the-Middle (MITM) attacks and CDN compromise.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))
    
    elements.append(Paragraph("2.2 Missing Security Headers", heading3_style))
    elements.append(Paragraph("<b>Severity:</b> HIGH | <b>CWE:</b> CWE-693", body_style))
    elements.append(Paragraph(
        "<b>Missing Headers:</b> Content-Security-Policy, X-Content-Type-Options, X-Frame-Options, "
        "Strict-Transport-Security, X-XSS-Protection, Referrer-Policy",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))
    
    elements.append(Paragraph("2.3 Supabase Credentials Exposure Risk", heading3_style))
    elements.append(Paragraph("<b>Severity:</b> HIGH | <b>CWE:</b> CWE-798", body_style))
    elements.append(Paragraph(
        "<b>Issue:</b> Supabase anon key exposed in environment variables and client-side code. "
        "No rate limiting on API calls. Database directly accessible from frontend.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))
    
    elements.append(Paragraph("2.4 Outdated Dependencies with Known Vulnerabilities", heading3_style))
    elements.append(Paragraph("<b>Severity:</b> HIGH | <b>CWE:</b> CWE-1104", body_style))
    elements.append(Paragraph(
        "<b>Issue:</b> Dependencies may contain known vulnerabilities. Requires regular auditing and updates.",
        body_style
    ))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(PageBreak())
    
    # Medium Vulnerabilities
    elements.append(Paragraph("3. MEDIUM VULNERABILITIES", heading2_style))
    
    elements.append(Paragraph("3.1 Missing Input Validation & Sanitization", heading3_style))
    elements.append(Paragraph("<b>Severity:</b> MEDIUM | <b>CWE:</b> CWE-79 (XSS)", body_style))
    elements.append(Paragraph(
        "<b>Issue:</b> Contact form lacks input validation and HTML escaping. Potential for stored XSS attacks.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))
    
    elements.append(Paragraph("3.2 Insecure Direct Object References (IDOR)", heading3_style))
    elements.append(Paragraph("<b>Severity:</b> MEDIUM | <b>CWE:</b> CWE-639", body_style))
    elements.append(Paragraph(
        "<b>Issue:</b> No row-level security policies visible. Direct database access from frontend without authentication.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))
    
    elements.append(Paragraph("3.3 Insufficient Logging & Monitoring", heading3_style))
    elements.append(Paragraph("<b>Severity:</b> MEDIUM | <b>CWE:</b> CWE-778", body_style))
    elements.append(Paragraph(
        "<b>Issue:</b> No security event logging, rate limiting, or bot detection (CAPTCHA).",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))
    
    elements.append(Paragraph("3.4 Weak Content Security Policy", heading3_style))
    elements.append(Paragraph("<b>Severity:</b> MEDIUM | <b>CWE:</b> CWE-693", body_style))
    elements.append(Paragraph(
        "<b>Issue:</b> No CSP header configured. Inline scripts allowed. External resources unrestricted.",
        body_style
    ))
    elements.append(Spacer(1, 0.2*inch))
    
    # Low Vulnerabilities
    elements.append(Paragraph("4. LOW VULNERABILITIES", heading2_style))
    
    elements.append(Paragraph("4.1 Information Disclosure via Metadata", heading3_style))
    elements.append(Paragraph("<b>Severity:</b> LOW | <b>CWE:</b> CWE-200", body_style))
    elements.append(Paragraph(
        "<b>Issue:</b> Author name, professional details, and resume publicly indexed.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))
    
    elements.append(Paragraph("4.2 Missing .env File Protection", heading3_style))
    elements.append(Paragraph("<b>Severity:</b> LOW | <b>CWE:</b> CWE-798", body_style))
    elements.append(Paragraph(
        "<b>Issue:</b> .env.example shows structure. Risk of accidental credential exposure.",
        body_style
    ))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(PageBreak())
    
    # Remediation Summary
    elements.append(Paragraph("REMEDIATION SUMMARY", heading1_style))
    
    elements.append(Paragraph("CRITICAL FIXES (Implement Immediately)", heading2_style))
    
    critical_fixes = [
        ("1. Protect Personal Information", 
         "<b>Issue:</b> Email/phone exposed in Contact.tsx and index.html<br/>"
         "<b>How to Fix:</b><br/>"
         "• Open src/components/Contact.tsx<br/>"
         "• Replace direct email/phone display with contact form only<br/>"
         "• Use email obfuscation: Split email into parts or use base64 encoding<br/>"
         "• Add password protection to resume PDF or use server-side download<br/>"
         "<b>Prompt:</b> 'Remove email and phone from Contact component, keep only contact form'"),
        
        ("2. Add Subresource Integrity (SRI)", 
         "<b>Issue:</b> MediaPipe CDN scripts in index.html lack integrity hashes<br/>"
         "<b>How to Fix:</b><br/>"
         "• Generate SRI hash: curl -s [CDN_URL] | openssl dgst -sha384 -binary | openssl base64 -A<br/>"
         "• Add integrity='sha384-[HASH]' and crossorigin='anonymous' to script tags<br/>"
         "• Example: &lt;script src='...' integrity='sha384-abc123' crossorigin='anonymous'&gt;&lt;/script&gt;<br/>"
         "<b>Prompt:</b> 'Add SRI integrity hashes to all CDN script tags in index.html'"),
        
        ("3. Implement Security Headers", 
         "<b>Issue:</b> Missing security headers in deployment configuration<br/>"
         "<b>How to Fix:</b><br/>"
         "• For Vercel: Add headers in vercel.json<br/>"
         "• For GitHub Pages: Add headers in _headers file or use meta tags<br/>"
         "• Required headers: X-Content-Type-Options: nosniff, X-Frame-Options: DENY, "
         "X-XSS-Protection: 1; mode=block, Strict-Transport-Security: max-age=31536000<br/>"
         "<b>Prompt:</b> 'Add security headers to vercel.json: CSP, X-Frame-Options, HSTS, X-Content-Type-Options'"),
        
        ("4. Secure Supabase Configuration", 
         "<b>Issue:</b> No RLS policies, exposed anon key, no rate limiting<br/>"
         "<b>How to Fix:</b><br/>"
         "• Go to Supabase Dashboard → Authentication → Policies<br/>"
         "• Enable RLS on contact_messages table<br/>"
         "• Add policy: CREATE for authenticated users only<br/>"
         "• Implement rate limiting in Contact.tsx (max 3 submissions per hour)<br/>"
         "• Add Google reCAPTCHA v3 to contact form<br/>"
         "<b>Prompt:</b> 'Enable RLS on Supabase contact_messages table and add rate limiting to contact form'"),
    ]
    
    for title, description in critical_fixes:
        elements.append(Paragraph(f"<b>{title}</b>", heading3_style))
        elements.append(Paragraph(description, body_style))
        elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("HIGH PRIORITY FIXES (Within 1 Week)", heading2_style))
    
    high_fixes = [
        ("5. Update Dependencies", 
         "<b>How to Fix:</b><br/>"
         "• Run: npm audit<br/>"
         "• Run: npm audit fix<br/>"
         "• Run: npm update<br/>"
         "• Check package.json for outdated versions<br/>"
         "<b>Prompt:</b> 'Run npm audit and update all vulnerable dependencies'"),
        ("6. Add Input Validation & Sanitization", 
         "<b>How to Fix:</b><br/>"
         "• Install DOMPurify: npm install dompurify<br/>"
         "• In Contact.tsx, add email regex validation<br/>"
         "• Sanitize all form inputs before sending to Supabase<br/>"
         "• Add max length limits (name: 100, email: 100, message: 1000)<br/>"
         "<b>Prompt:</b> 'Add input validation and DOMPurify sanitization to Contact form'"),
        ("7. Implement Content Security Policy", 
         "<b>How to Fix:</b><br/>"
         "• Add CSP meta tag in index.html head section<br/>"
         "• Policy: default-src 'self'; script-src 'self' 'unsafe-inline' cdn.jsdelivr.net; style-src 'self' 'unsafe-inline'<br/>"
         "• Or add CSP header in vercel.json<br/>"
         "<b>Prompt:</b> 'Add Content-Security-Policy meta tag to index.html with strict script-src'"),
    ]
    
    for title, description in high_fixes:
        elements.append(Paragraph(f"<b>{title}</b>", heading3_style))
        elements.append(Paragraph(description, body_style))
        elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("MEDIUM PRIORITY FIXES (Within 2 Weeks)", heading2_style))
    
    medium_fixes = [
        ("8. Add CAPTCHA to Contact Form", 
         "<b>How to Fix:</b><br/>"
         "• Sign up for Google reCAPTCHA v3 at google.com/recaptcha<br/>"
         "• Install: npm install react-google-recaptcha-v3<br/>"
         "• Add reCAPTCHA script to index.html<br/>"
         "• Wrap Contact component with GoogleReCaptchaProvider<br/>"
         "• Verify token before form submission<br/>"
         "<b>Prompt:</b> 'Add Google reCAPTCHA v3 to contact form in Contact.tsx'"),
        ("9. Implement Logging & Monitoring", 
         "<b>How to Fix:</b><br/>"
         "• Set up Supabase Edge Functions for logging<br/>"
         "• Log all form submissions with timestamp, IP, user agent<br/>"
         "• Add error tracking with Sentry: npm install @sentry/react<br/>"
         "• Monitor failed submissions and suspicious patterns<br/>"
         "<b>Prompt:</b> 'Add Sentry error tracking and log all contact form submissions'"),
        ("10. Enable Row-Level Security (RLS)", 
         "<b>How to Fix:</b><br/>"
         "• Open Supabase Dashboard → Database → contact_messages table<br/>"
         "• Click 'Enable RLS'<br/>"
         "• Add policy: CREATE - allow if rate limit not exceeded<br/>"
         "• Add policy: SELECT - allow only for authenticated admin users<br/>"
         "<b>Prompt:</b> 'Create RLS policies for contact_messages table in Supabase'"),
    ]
    
    for title, description in medium_fixes:
        elements.append(Paragraph(f"<b>{title}</b>", heading3_style))
        elements.append(Paragraph(description, body_style))
        elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("LOW PRIORITY FIXES (Within 1 Month)", heading2_style))
    elements.append(Paragraph(
        "<b>11. Implement .env Security</b><br/>"
        "<b>How to Fix:</b><br/>"
        "• Verify .env is in .gitignore<br/>"
        "• Use .env.local for local development (not tracked)<br/>"
        "• Add Supabase keys to Vercel Environment Variables<br/>"
        "• Add keys to GitHub Secrets for GitHub Actions<br/>"
        "• Rotate Supabase anon key every 3 months<br/>"
        "<b>Prompt:</b> 'Move Supabase credentials to Vercel environment variables and GitHub Secrets'",
        body_style
    ))
    
    elements.append(Spacer(1, 0.3*inch))
    elements.append(PageBreak())
    
    # Compliance & Standards
    elements.append(Paragraph("COMPLIANCE & STANDARDS", heading1_style))
    
    elements.append(Paragraph("OWASP Top 10 Mapping", heading2_style))
    
    owasp_data = [
        ['OWASP Issue', 'Status'],
        ['A01:2021 - Broken Access Control', '⚠️ At Risk'],
        ['A02:2021 - Cryptographic Failures', '⚠️ At Risk'],
        ['A03:2021 - Injection', '⚠️ At Risk'],
        ['A04:2021 - Insecure Design', '⚠️ At Risk'],
        ['A05:2021 - Security Misconfiguration', '⚠️ At Risk'],
        ['A06:2021 - Vulnerable Components', '⚠️ At Risk'],
        ['A07:2021 - Authentication Failures', '✓ Compliant'],
        ['A08:2021 - Data Integrity Failures', '⚠️ At Risk'],
        ['A09:2021 - Logging & Monitoring', '⚠️ At Risk'],
        ['A10:2021 - SSRF', '✓ Compliant'],
    ]
    
    owasp_table = Table(owasp_data, colWidths=[3.5*inch, 1.5*inch])
    owasp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    
    elements.append(owasp_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # GDPR Compliance
    elements.append(Paragraph("GDPR Compliance Issues", heading2_style))
    elements.append(Paragraph(
        "<b>Issues:</b> Personal data collection without explicit consent, no privacy policy, "
        "no data retention policy, no data deletion mechanism.",
        body_style
    ))
    elements.append(Paragraph(
        "<b>Recommendations:</b> Add privacy policy, implement consent management, add data deletion functionality, "
        "document data processing.",
        body_style
    ))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(PageBreak())
    
    # Recommendations
    elements.append(Paragraph("RECOMMENDATIONS & NEXT STEPS", heading1_style))
    
    elements.append(Paragraph("Immediate Actions (This Week)", heading2_style))
    elements.append(Paragraph(
        "1. Protect personal information by removing direct email/phone display<br/>"
        "2. Add SRI hashes to all CDN scripts<br/>"
        "3. Implement security headers<br/>"
        "4. Secure Supabase configuration with RLS and rate limiting",
        body_style
    ))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("Short-term Actions (1-2 Weeks)", heading2_style))
    elements.append(Paragraph(
        "1. Update all dependencies and run security audits<br/>"
        "2. Add input validation and sanitization<br/>"
        "3. Implement Content Security Policy<br/>"
        "4. Add CAPTCHA to contact form",
        body_style
    ))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("Long-term Actions (1 Month+)", heading2_style))
    elements.append(Paragraph(
        "1. Implement comprehensive logging and monitoring<br/>"
        "2. Set up continuous security scanning (Snyk, GitHub Security)<br/>"
        "3. Conduct regular penetration testing<br/>"
        "4. Implement GDPR compliance measures<br/>"
        "5. Establish incident response procedures",
        body_style
    ))
    elements.append(Spacer(1, 0.3*inch))
    
    # Conclusion
    elements.append(Paragraph("CONCLUSION", heading1_style))
    elements.append(Paragraph(
        "The website has 11 identified vulnerabilities ranging from Critical to Low severity. "
        "The most critical issues require immediate attention, particularly the exposure of personal information "
        "and missing security headers. With proper implementation of the recommended fixes, the security posture "
        "can be improved from MEDIUM to HIGH within 2-3 weeks.",
        body_style
    ))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph(
        "<b>Estimated Remediation Time:</b> 2-3 weeks for all fixes<br/>"
        "<b>Overall Security Posture:</b> MEDIUM (Improving to HIGH after fixes)<br/>"
        "<b>Next Assessment:</b> 3 months after remediation",
        body_style
    ))
    elements.append(Spacer(1, 0.3*inch))
    
    # Footer
    elements.append(Spacer(1, 0.5*inch))
    footer_text = f"Report Generated: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}<br/>Classification: CONFIDENTIAL"
    elements.append(Paragraph(footer_text, styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    print(f"✓ PDF Report generated successfully: {output_filename}")
    return output_filename

if __name__ == "__main__":
    try:
        print("\n" + "="*60)
        print("🔐 SECURITY VULNERABILITY SCANNER & REPORT GENERATOR")
        print("="*60 + "\n")
        
        # Step 1: Run Scanner
        print("[1/4] Running vulnerability scanner...")
        repo_path = Path(__file__).parent.parent
        scanner = GitHubScanner(repo_path)
        scanner.scan()
        scanner.print_summary()
        
        # Step 2: Load scan results
        print("\n[2/4] Loading scan results...")
        scan_results_file = Path(__file__).parent / 'scan initiate' / 'scan_results.json'
        with open(scan_results_file, 'r') as f:
            scan_data = json.load(f)
        
        errors_count = scan_data['total_vulnerabilities']
        print(f"✓ Found {errors_count} vulnerabilities")
        
        # Step 3: Generate timestamp
        now = datetime.now()
        day = now.strftime('%d')
        month = now.strftime('%b').lower()
        year = now.strftime('%Y')
        time_str = now.strftime('%I:%M:%S%p')
        
        # Step 4: Generate PDF Report
        print("\n[3/4] Generating PDF report...")
        pdf_filename = f"Reports/{day}_{month}_{year}||{time_str}||({errors_count})errors.pdf"
        pdf_file = create_security_report_pdf(pdf_filename)
        print(f"✓ PDF created: {pdf_file}")
        print(f"✓ PDF size: {os.path.getsize(pdf_file) / 1024:.2f} KB")
        
        # Step 5: Generate Markdown Report
        print("\n[4/4] Generating Markdown report...")
        md_filename = f"archived/Report_md/{day}_{month}_{year}||{time_str}||({errors_count})errors.md"
        md_file = generate_markdown_report(md_filename)
        print(f"✓ Markdown created: {md_file}")
        print(f"✓ Markdown size: {os.path.getsize(md_file) / 1024:.2f} KB")
        
        # Summary
        print("\n" + "="*60)
        print("📊 REPORTS GENERATED SUCCESSFULLY!")
        print("="*60)
        print(f"\n📄 PDF Report:      {pdf_file}")
        print(f"📝 Markdown Report: {md_file}")
        print(f"🔍 Scan Results:    scan initiate/scan_results.json")
        print(f"\n🔴 CRITICAL: {scan_data['severity_breakdown']['CRITICAL']}")
        print(f"🟠 HIGH:     {scan_data['severity_breakdown']['HIGH']}")
        print(f"🟡 MEDIUM:   {scan_data['severity_breakdown']['MEDIUM']}")
        print(f"🟢 LOW:      {scan_data['severity_breakdown']['LOW']}")
        print(f"\n📊 TOTAL:    {errors_count} vulnerabilities\n")
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()

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

def create_security_report_pdf(output_filename="Security_Assessment_Report.pdf"):
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
         "Remove direct email/phone display. Use contact form only. Implement email obfuscation. "
         "Restrict resume PDF access or use password protection."),
        
        ("2. Add Subresource Integrity (SRI)", 
         "Generate SRI hashes for all CDN scripts. Add integrity attribute to script tags. Use HTTPS only."),
        
        ("3. Implement Security Headers", 
         "Add X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, Strict-Transport-Security, "
         "Content-Security-Policy, and Referrer-Policy headers."),
        
        ("4. Secure Supabase Configuration", 
         "Enable Row-Level Security (RLS). Implement rate limiting. Add CAPTCHA to contact form. "
         "Use environment variables properly. Implement server-side validation."),
    ]
    
    for title, description in critical_fixes:
        elements.append(Paragraph(f"<b>{title}</b>", heading3_style))
        elements.append(Paragraph(description, body_style))
        elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("HIGH PRIORITY FIXES (Within 1 Week)", heading2_style))
    
    high_fixes = [
        ("5. Update Dependencies", "Run 'npm audit' and 'npm audit fix'. Update all packages. Check for vulnerabilities."),
        ("6. Add Input Validation & Sanitization", "Validate email format. Sanitize all inputs using DOMPurify. Escape HTML output."),
        ("7. Implement Content Security Policy", "Add CSP meta tag to index.html. Restrict script sources. Implement nonce-based execution."),
    ]
    
    for title, description in high_fixes:
        elements.append(Paragraph(f"<b>{title}</b>", heading3_style))
        elements.append(Paragraph(description, body_style))
        elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("MEDIUM PRIORITY FIXES (Within 2 Weeks)", heading2_style))
    
    medium_fixes = [
        ("8. Add CAPTCHA to Contact Form", "Implement reCAPTCHA v3. Verify token on backend. Prevent spam submissions."),
        ("9. Implement Logging & Monitoring", "Add security event logging. Monitor form submissions. Track suspicious activity."),
        ("10. Enable Row-Level Security (RLS)", "Configure RLS policies in Supabase. Restrict data access. Prevent unauthorized modifications."),
    ]
    
    for title, description in medium_fixes:
        elements.append(Paragraph(f"<b>{title}</b>", heading3_style))
        elements.append(Paragraph(description, body_style))
        elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("LOW PRIORITY FIXES (Within 1 Month)", heading2_style))
    elements.append(Paragraph(
        "<b>11. Implement .env Security:</b> Never commit .env files. Use .env.local for development. "
        "Use GitHub Secrets for CI/CD. Rotate credentials regularly.",
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
        pdf_file = create_security_report_pdf()
        print(f"\n✓ Security Assessment Report created: {pdf_file}")
        print(f"✓ File size: {os.path.getsize(pdf_file) / 1024:.2f} KB")
    except Exception as e:
        print(f"✗ Error generating PDF: {str(e)}")
        import traceback
        traceback.print_exc()

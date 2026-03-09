#!/usr/bin/env python3
"""
Dynamic Security Assessment Report PDF Generator
Reads from scan_results.json and generates detailed PDF with prompts
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from datetime import datetime
import json
import os
from pathlib import Path

def get_fix_instructions(vuln):
    """Generate detailed fix instructions based on vulnerability type"""
    vuln_type = vuln.get('type', '')
    severity = vuln.get('severity', '')
    file = vuln.get('file', '')
    
    instructions = {
        'title': f"{vuln_type}",
        'issue': '',
        'how_to_fix': '',
        'prompt': ''
    }
    
    if vuln_type == 'Exposed Secret':
        secret_type = vuln.get('secret_type', 'credential')
        value = vuln.get('value', '[REDACTED]')
        instructions['issue'] = f"{secret_type} exposed in {file}: {value}"
        instructions['how_to_fix'] = (
            f"• Open {file}<br/>"
            f"• Locate and remove: {value}<br/>"
            f"• Replace with environment variable<br/>"
            f"• Add to .env file (not committed to git)<br/>"
            f"• Update .gitignore to include .env<br/>"
            f"• If credentials exposed publicly, rotate them immediately"
        )
        instructions['prompt'] = f"Remove '{value}' from {file} and use environment variables"
        
    elif vuln_type == 'Outdated Dependency':
        package = vuln.get('package', 'package')
        version = vuln.get('version', '')
        instructions['issue'] = f"{package} version {version} may have known vulnerabilities"
        instructions['how_to_fix'] = (
            f"• Open {file}<br/>"
            f"• Update {package} to latest version<br/>"
            f"• Run: npm update {package}<br/>"
            f"• Run: npm audit fix<br/>"
            f"• Test your application thoroughly"
        )
        instructions['prompt'] = f"Update {package} dependency to latest secure version"
        
    elif vuln_type == 'Missing SRI':
        instructions['issue'] = f"CDN script in {file} lacks integrity hash"
        instructions['how_to_fix'] = (
            f"• Open {file}<br/>"
            f"• Generate SRI hash: curl -s [CDN_URL] | openssl dgst -sha384 -binary | openssl base64 -A<br/>"
            f"• Add integrity='sha384-[HASH]' to script tag<br/>"
            f"• Add crossorigin='anonymous' attribute<br/>"
            f"• Test page loads correctly"
        )
        instructions['prompt'] = f"Add SRI integrity hashes to CDN scripts in {file}"
        
    elif vuln_type == 'Missing Security Header':
        header = vuln.get('header', 'security header')
        instructions['issue'] = f"{header} not configured"
        instructions['how_to_fix'] = (
            f"• Add {header} to server configuration<br/>"
            f"• For Vercel: Update vercel.json headers section<br/>"
            f"• For Apache: Update .htaccess<br/>"
            f"• For Nginx: Update nginx.conf<br/>"
            f"• Test with securityheaders.com"
        )
        instructions['prompt'] = f"Add {header} to deployment configuration"
        
    elif vuln_type == 'Missing Input Validation':
        instructions['issue'] = f"No input sanitization in {file}"
        instructions['how_to_fix'] = (
            f"• Open {file}<br/>"
            f"• Install DOMPurify: npm install dompurify<br/>"
            f"• Add input validation for all form fields<br/>"
            f"• Sanitize user input before processing<br/>"
            f"• Add max length limits"
        )
        instructions['prompt'] = f"Add input validation and sanitization to {file}"
        
    else:
        # Generic instructions
        instructions['issue'] = f"{vuln_type} found in {file}"
        instructions['how_to_fix'] = (
            f"• Review {file}<br/>"
            f"• Address the {vuln_type} issue<br/>"
            f"• Follow security best practices<br/>"
            f"• Test changes thoroughly"
        )
        instructions['prompt'] = f"Fix {vuln_type} in {file}"
    
    return instructions

def create_dynamic_pdf_report(scan_data, output_filename):
    """Generate PDF from scan results"""
    
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
        title="Security Assessment Report"
    )
    
    elements = []
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
    elements.append(Paragraph("Repository Security & Vulnerability Assessment", styles['Normal']))
    elements.append(Spacer(1, 0.5*inch))
    
    # Extract repo name from path or URL
    repo_name = scan_data.get('repo_name', scan_data.get('repo_path', 'Unknown Repository').split('/')[-1])
    repo_url = scan_data.get('repo_url', 'N/A')
    
    # Report metadata
    scan_date = datetime.fromisoformat(scan_data.get('scan_date', datetime.now().isoformat()))
    metadata = [
        f"<b>Repository:</b> {repo_name}",
        f"<b>Repository URL:</b> {repo_url}",
        f"<b>Assessment Date:</b> {scan_date.strftime('%B %d, %Y')}",
        f"<b>Assessment Type:</b> Automated Security Scan",
        f"<b>Total Vulnerabilities:</b> {scan_data.get('total_vulnerabilities', 0)}",
    ]
    
    for item in metadata:
        elements.append(Paragraph(item, body_style))
        elements.append(Spacer(1, 0.1*inch))
    
    elements.append(PageBreak())
    
    # Vulnerability Summary
    elements.append(Paragraph("VULNERABILITY SUMMARY", heading1_style))
    
    severity = scan_data.get('severity_breakdown', {})
    vuln_data = [
        ['Severity', 'Count', 'Status'],
        ['CRITICAL', str(severity.get('CRITICAL', 0)), 'Active'],
        ['HIGH', str(severity.get('HIGH', 0)), 'Active'],
        ['MEDIUM', str(severity.get('MEDIUM', 0)), 'Active'],
        ['LOW', str(severity.get('LOW', 0)), 'Active'],
        ['TOTAL', str(scan_data.get('total_vulnerabilities', 0)), 'Active']
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
    
    # Vulnerabilities Detail
    elements.append(Paragraph("VULNERABILITIES IDENTIFIED", heading1_style))
    
    vulnerabilities = scan_data.get('vulnerabilities', [])
    
    # Group by severity
    by_severity = {'CRITICAL': [], 'HIGH': [], 'MEDIUM': [], 'LOW': []}
    for vuln in vulnerabilities:
        sev = vuln.get('severity', 'LOW')
        by_severity[sev].append(vuln)
    
    severity_order = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
    
    for sev in severity_order:
        if by_severity[sev]:
            elements.append(Paragraph(f"{sev} VULNERABILITIES", heading2_style))
            
            for idx, vuln in enumerate(by_severity[sev], 1):
                elements.append(Paragraph(f"{idx}. {vuln.get('type', 'Unknown')}", heading3_style))
                elements.append(Paragraph(
                    f"<b>Severity:</b> {vuln.get('severity', 'N/A')} | "
                    f"<b>CWE:</b> {vuln.get('cwe', 'N/A')} | "
                    f"<b>File:</b> {vuln.get('file', 'N/A')}",
                    body_style
                ))
                elements.append(Spacer(1, 0.1*inch))
            
            elements.append(Spacer(1, 0.2*inch))
    
    elements.append(PageBreak())
    
    # Remediation Summary
    elements.append(Paragraph("REMEDIATION SUMMARY", heading1_style))
    elements.append(Paragraph(
        "Below are detailed instructions for fixing each vulnerability. "
        "Follow the steps carefully and test thoroughly after each fix.",
        body_style
    ))
    elements.append(Spacer(1, 0.2*inch))
    
    for sev in severity_order:
        if by_severity[sev]:
            priority = {
                'CRITICAL': 'CRITICAL FIXES (Implement Immediately)',
                'HIGH': 'HIGH PRIORITY FIXES (Within 1 Week)',
                'MEDIUM': 'MEDIUM PRIORITY FIXES (Within 2 Weeks)',
                'LOW': 'LOW PRIORITY FIXES (Within 1 Month)'
            }
            
            elements.append(Paragraph(priority[sev], heading2_style))
            
            for idx, vuln in enumerate(by_severity[sev], 1):
                instructions = get_fix_instructions(vuln)
                
                elements.append(Paragraph(f"<b>{idx}. {instructions['title']}</b>", heading3_style))
                
                if instructions['issue']:
                    elements.append(Paragraph(f"<b>Issue:</b> {instructions['issue']}", body_style))
                
                if instructions['how_to_fix']:
                    elements.append(Paragraph(f"<b>How to Fix:</b><br/>{instructions['how_to_fix']}", body_style))
                
                if instructions['prompt']:
                    elements.append(Paragraph(f"<b>Prompt:</b> '{instructions['prompt']}'", body_style))
                
                elements.append(Spacer(1, 0.15*inch))
            
            elements.append(Spacer(1, 0.2*inch))
    
    # Footer
    elements.append(PageBreak())
    elements.append(Paragraph("CONCLUSION", heading1_style))
    elements.append(Paragraph(
        f"This assessment identified {scan_data.get('total_vulnerabilities', 0)} vulnerabilities. "
        f"Follow the remediation steps above to improve your security posture. "
        f"Re-scan after implementing fixes to verify improvements.",
        body_style
    ))
    elements.append(Spacer(1, 0.3*inch))
    
    footer_text = f"Report Generated: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}<br/>Classification: CONFIDENTIAL"
    elements.append(Paragraph(footer_text, styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    print(f"✓ Dynamic PDF Report generated: {output_filename}")
    return output_filename

if __name__ == "__main__":
    # Read scan results
    scan_results_file = Path(__file__).parent / 'scan initiate' / 'scan_results.json'
    
    if not scan_results_file.exists():
        print("✗ No scan results found. Run scanner first.")
        exit(1)
    
    with open(scan_results_file, 'r') as f:
        scan_data = json.load(f)
    
    # Generate filename
    now = datetime.now()
    day = now.strftime('%d')
    month = now.strftime('%b').lower()
    year = now.strftime('%Y')
    time_str = now.strftime('%I:%M:%S%p')
    errors_count = scan_data.get('total_vulnerabilities', 0)
    
    output_file = f"Reports/{day}_{month}_{year}||{time_str}||({errors_count})errors.pdf"
    
    # Ensure Reports directory exists
    Path("Reports").mkdir(exist_ok=True)
    
    # Generate PDF
    create_dynamic_pdf_report(scan_data, output_file)
    print(f"✓ Report saved: {output_file}")
    print(f"✓ File size: {os.path.getsize(output_file) / 1024:.2f} KB")

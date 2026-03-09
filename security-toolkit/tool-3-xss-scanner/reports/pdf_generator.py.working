#!/usr/bin/env python3
"""
PDF Report Generator
Creates professional security assessment reports with detailed explanations
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from datetime import datetime
from pathlib import Path
from typing import Dict

class PDFReportGenerator:
    def __init__(self):
        """Initialize PDF generator"""
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        self.heading1_style = ParagraphStyle(
            'CustomHeading1',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#0066cc'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        self.heading2_style = ParagraphStyle(
            'CustomHeading2',
            parent=self.styles['Heading2'],
            fontSize=13,
            textColor=colors.HexColor('#003366'),
            spaceAfter=10,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        )
        
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['BodyText'],
            fontSize=10,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
            leading=12
        )
    
    def generate(self, report_data: Dict, output_file: str):
        """Generate PDF report from scan data"""
        doc = SimpleDocTemplate(
            output_file,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch,
            title="Security Vulnerability Report"
        )
        
        elements = []
        
        # Title Page
        elements.extend(self._create_title_page(report_data))
        elements.append(PageBreak())
        
        # Executive Summary
        elements.extend(self._create_summary(report_data))
        elements.append(PageBreak())
        
        # Business Impact Analysis
        elements.extend(self._create_business_impact_analysis(report_data['severity_breakdown']))
        elements.append(PageBreak())
        
        # Manual Testing Guide
        if report_data.get('vulnerabilities'):
            elements.extend(self._create_manual_testing_guide(report_data['vulnerabilities']))
            elements.append(PageBreak())
        
        # AI Prompts
        if report_data.get('vulnerabilities'):
            elements.extend(self._create_ai_prompts_section(report_data['vulnerabilities']))
            elements.append(PageBreak())
        
        # Code Examples
        if report_data.get('vulnerabilities'):
            elements.extend(self._create_code_examples(report_data['vulnerabilities']))
            elements.append(PageBreak())
        
        # Detailed Findings
        elements.extend(self._create_findings(report_data))
        
        # Build PDF
        doc.build(elements)
        return output_file
    
    def _create_title_page(self, data: Dict):
        """Create title page"""
        elements = []
        
        elements.append(Spacer(1, 1.5*inch))
        elements.append(Paragraph("SECURITY VULNERABILITY REPORT", self.title_style))
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph("Automated Security Assessment", self.styles['Normal']))
        elements.append(Spacer(1, 0.5*inch))
        
        # Metadata
        scan_date = datetime.fromisoformat(data['scan_date'])
        target_name = Path(data['target']).name if data['scan_type'] == 'local' else data['target']
        
        metadata = [
            f"<b>Target:</b> {target_name}",
            f"<b>Scan Type:</b> {data['scan_type'].upper()}",
            f"<b>Scan Date:</b> {scan_date.strftime('%B %d, %Y at %H:%M:%S')}",
            f"<b>Total Vulnerabilities:</b> {data['total_vulnerabilities']}",
        ]
        
        for item in metadata:
            elements.append(Paragraph(item, self.body_style))
            elements.append(Spacer(1, 0.1*inch))
        
        return elements
    
    def _create_summary(self, data: Dict):
        """Create executive summary with dashboard and priority matrix"""
        elements = []
        
        elements.append(Paragraph("EXECUTIVE SUMMARY", self.heading1_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Calculate metrics
        severity = data['severity_breakdown']
        total_vulns = data['total_vulnerabilities']
        risk_score = self._calculate_risk_score(severity)
        time_estimate = self._calculate_time_estimate(severity)
        
        # Dashboard with key metrics
        elements.append(Paragraph("Security Dashboard", self.heading2_style))
        
        dashboard_data = [
            ['Metric', 'Value', 'Status'],
            ['Risk Score', f"{risk_score}/100", self._get_risk_badge(risk_score)],
            ['Total Vulnerabilities', str(total_vulns), ''],
            ['Time to Fix', time_estimate, ''],
            ['OWASP Compliance', self._check_owasp_compliance(severity), ''],
            ['CWE Coverage', 'Analyzed', '✓'],
        ]
        
        dashboard_table = Table(dashboard_data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
        dashboard_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
        ]))
        
        elements.append(dashboard_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Severity breakdown table
        elements.append(Paragraph("Vulnerability Breakdown", self.heading2_style))
        
        vuln_data = [
            ['Severity', 'Count', 'Priority', 'Action Required'],
            ['CRITICAL', str(severity.get('CRITICAL', 0)), 'P0', 'Immediate (24h)'],
            ['HIGH', str(severity.get('HIGH', 0)), 'P1', 'Urgent (1 week)'],
            ['MEDIUM', str(severity.get('MEDIUM', 0)), 'P2', 'Important (2 weeks)'],
            ['LOW', str(severity.get('LOW', 0)), 'P3', 'Normal (1 month)'],
        ]
        
        vuln_table = Table(vuln_data, colWidths=[1.5*inch, 1*inch, 1*inch, 2.5*inch])
        vuln_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (0, 1), colors.HexColor('#ffcccc')),
            ('BACKGROUND', (0, 2), (0, 2), colors.HexColor('#ffddaa')),
            ('BACKGROUND', (0, 3), (0, 3), colors.HexColor('#ffffcc')),
            ('BACKGROUND', (0, 4), (0, 4), colors.HexColor('#ccffcc')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
        ]))
        
        elements.append(vuln_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Priority Matrix
        elements.append(Paragraph("Priority Matrix", self.heading2_style))
        elements.append(Paragraph(
            "Vulnerabilities categorized by impact and effort to help prioritize fixes:",
            self.body_style
        ))
        elements.append(Spacer(1, 0.1*inch))
        
        priority_data = [
            ['', 'Easy Fix (<2h)', 'Medium Fix (2-8h)', 'Hard Fix (>8h)'],
            ['High Impact', '🔴 Fix First\n(Critical/High)', '🟠 Plan & Fix\n(High)', '🟡 Plan & Fix\n(High)'],
            ['Medium Impact', '🟢 Quick Wins\n(Medium)', '🟡 Schedule\n(Medium)', '🔵 Backlog\n(Medium)'],
            ['Low Impact', '🟢 Quick Wins\n(Low)', '🔵 Backlog\n(Low)', '⚪ Defer\n(Low)'],
        ]
        
        priority_table = Table(priority_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        priority_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
            ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#0066cc')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('TEXTCOLOR', (0, 1), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 1), (1, 1), colors.HexColor('#ffcccc')),
            ('BACKGROUND', (2, 1), (3, 1), colors.HexColor('#ffddaa')),
            ('BACKGROUND', (1, 2), (1, 2), colors.HexColor('#ccffcc')),
            ('BACKGROUND', (2, 2), (2, 2), colors.HexColor('#ffffcc')),
            ('BACKGROUND', (3, 2), (3, 2), colors.HexColor('#e6e6ff')),
            ('BACKGROUND', (1, 3), (1, 3), colors.HexColor('#ccffcc')),
            ('BACKGROUND', (2, 3), (3, 3), colors.HexColor('#e6e6ff')),
            ('GRID', (0, 0), (-1, -1), 1.5, colors.black),
        ]))
        
        elements.append(priority_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Risk assessment
        risk_level = self._calculate_risk_level(severity)
        risk_color = {
            'CRITICAL': '#cc0000',
            'HIGH': '#ff6600',
            'MEDIUM': '#ffcc00',
            'LOW': '#00cc00'
        }.get(risk_level, '#666666')
        
        elements.append(Paragraph(
            f"<b>Overall Risk Level:</b> <font color='{risk_color}'><b>{risk_level}</b></font> | "
            f"<b>Risk Score:</b> {risk_score}/100 | "
            f"<b>Estimated Fix Time:</b> {time_estimate}",
            self.body_style
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _calculate_risk_score(self, severity: Dict) -> int:
        """Calculate risk score 0-100"""
        critical = severity.get('CRITICAL', 0)
        high = severity.get('HIGH', 0)
        medium = severity.get('MEDIUM', 0)
        low = severity.get('LOW', 0)
        
        # Weighted score
        score = (critical * 25) + (high * 10) + (medium * 3) + (low * 1)
        return min(100, score)
    
    def _calculate_time_estimate(self, severity: Dict) -> str:
        """Estimate time to fix all vulnerabilities"""
        critical = severity.get('CRITICAL', 0)
        high = severity.get('HIGH', 0)
        medium = severity.get('MEDIUM', 0)
        low = severity.get('LOW', 0)
        
        # Hours estimate: Critical=4h, High=2h, Medium=1h, Low=0.5h
        hours = (critical * 4) + (high * 2) + (medium * 1) + (low * 0.5)
        
        if hours < 8:
            return f"{int(hours)} hours"
        elif hours < 40:
            return f"{int(hours/8)} days"
        else:
            return f"{int(hours/40)} weeks"
    
    def _check_owasp_compliance(self, severity: Dict) -> str:
        """Check OWASP compliance status"""
        critical = severity.get('CRITICAL', 0)
        high = severity.get('HIGH', 0)
        
        if critical > 0:
            return '❌ Non-Compliant'
        elif high > 5:
            return '⚠️ At Risk'
        elif high > 0:
            return '🟡 Needs Review'
        else:
            return '✅ Compliant'
    
    def _get_risk_badge(self, score: int) -> str:
        """Get risk badge based on score"""
        if score >= 75:
            return '🔴 Critical'
        elif score >= 50:
            return '🟠 High'
        elif score >= 25:
            return '🟡 Medium'
        else:
            return '🟢 Low'
    
    def _create_findings(self, data: Dict):
        """Create detailed findings section with smart grouping"""
        elements = []
        
        elements.append(Paragraph("DETAILED FINDINGS", self.heading1_style))
        elements.append(Paragraph(
            "Vulnerabilities are grouped by type and fix solution. Each group shows affected files and a single fix command.",
            self.body_style
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        # Smart grouping by type and fix
        grouped = self._group_vulnerabilities(data['vulnerabilities'])
        
        # Display grouped findings by severity
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            severity_groups = [g for g in grouped if g['severity'] == severity]
            if severity_groups:
                elements.append(Paragraph(
                    f"{severity} Severity Issues ({sum(g['count'] for g in severity_groups)} total)",
                    self.heading2_style
                ))
                
                for group in severity_groups:
                    elements.extend(self._format_vulnerability_group(group))
                
                elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _group_vulnerabilities(self, vulnerabilities):
        """Group similar vulnerabilities by type, CVE, or fix"""
        groups = {}
        
        for vuln in vulnerabilities:
            vuln_type = vuln.get('type', 'Unknown')
            severity = vuln.get('severity', 'LOW')
            package = vuln.get('package', '')
            cwe = vuln.get('cwe', '')
            
            # Create group key based on type and package/cwe
            if package:
                group_key = f"{vuln_type}_{package}"
            elif cwe:
                group_key = f"{vuln_type}_{cwe}"
            else:
                group_key = vuln_type
            
            if group_key not in groups:
                groups[group_key] = {
                    'type': vuln_type,
                    'severity': severity,
                    'package': package,
                    'cwe': cwe,
                    'files': [],
                    'fix_prompt': vuln.get('fix_prompt', ''),
                    'count': 0
                }
            
            # Add file with full path
            file_info = {
                'path': vuln.get('file', 'Unknown'),
                'line': vuln.get('line'),
                'secret_type': vuln.get('secret_type'),
                'version': vuln.get('version'),
                'description': vuln.get('description')
            }
            groups[group_key]['files'].append(file_info)
            groups[group_key]['count'] += 1
        
        # Convert to list and sort by count (most common first)
        result = sorted(groups.values(), key=lambda x: x['count'], reverse=True)
        return result
    
    def _format_vulnerability_group(self, group: Dict):
        """Format a group of similar vulnerabilities"""
        elements = []
        
        # Group title with count
        title = f"{group['type']} ({group['count']} occurrences)"
        if group['package']:
            title += f" - Package: {group['package']}"
        
        elements.append(Paragraph(f"<b>{title}</b>", self.heading2_style))
        elements.append(Spacer(1, 0.05*inch))
        
        # Explanation
        explanation = self._get_vulnerability_explanation(group['type'], group)
        if explanation:
            elements.append(Paragraph(f"<b>❓ What This Means:</b> {explanation}", self.body_style))
            elements.append(Spacer(1, 0.1*inch))
        
        # Affected files (show full paths)
        elements.append(Paragraph(f"<b>📁 Affected Files ({group['count']}):</b>", self.body_style))
        
        # Show first 10 files, then summarize
        display_limit = 10
        for i, file_info in enumerate(group['files'][:display_limit]):
            file_path = file_info['path']
            line_info = f" (Line {file_info['line']})" if file_info['line'] else ""
            elements.append(Paragraph(f"  • {file_path}{line_info}", self.body_style))
        
        if group['count'] > display_limit:
            elements.append(Paragraph(
                f"  ... and {group['count'] - display_limit} more files",
                self.body_style
            ))
        
        elements.append(Spacer(1, 0.1*inch))
        
        # Single fix command for all
        if group['fix_prompt']:
            elements.append(Paragraph("<b>💡 Fix All ({} issues):</b>".format(group['count']), self.body_style))
            
            # Generate smart fix command with AI prompt
            fix_command = self._generate_fix_command(group)
            elements.append(Paragraph(fix_command, self.body_style))
        
        elements.append(Spacer(1, 0.25*inch))
        
        return elements
    
    def _generate_fix_command(self, group: Dict) -> str:
        """Generate actionable fix command for grouped vulnerabilities"""
        vuln_type = group['type']
        count = group['count']
        package = group['package']
        
        if vuln_type == 'Outdated Dependency' and package:
            return f"""<b>Command:</b> <font face='Courier'>npm update {package}</font> or <font face='Courier'>pip install --upgrade {package}</font><br/>
This will update {count} vulnerable instance(s) of {package}.<br/><br/>
<b>AI Prompt:</b> "Update {package} package to latest version and fix any breaking changes in the codebase"""
        
        elif vuln_type == 'Outdated Dependency':
            return f"""<b>Command:</b> <font face='Courier'>npm update</font> or <font face='Courier'>pip install --upgrade -r requirements.txt</font><br/>
This will update all {count} outdated packages at once.<br/><br/>
<b>AI Prompt:</b> "Update all outdated dependencies in package.json/requirements.txt and resolve any compatibility issues"""
        
        elif vuln_type == 'Exposed Secret':
            return f"""<b>Steps:</b><br/>
1. Remove all {count} exposed secrets from files<br/>
2. Add to .env: <font face='Courier'>echo 'SECRET_KEY=value' >> .env</font><br/>
3. Add .env to .gitignore<br/>
4. Rotate all exposed credentials immediately<br/>
5. Use environment variables in code<br/><br/>
<b>AI Prompt:</b> "Remove exposed secrets from code, move them to .env file, and update code to use environment variables"""
        
        elif vuln_type == 'Missing Security Header':
            return f"""<b>For Vercel:</b> Add to vercel.json headers section<br/>
<b>For Apache:</b> Add to .htaccess<br/>
<b>For Nginx:</b> Add to nginx.conf<br/>
This will fix all {count} missing headers.<br/><br/>
<b>AI Prompt:</b> "Add security headers (CSP, HSTS, X-Frame-Options) to vercel.json configuration file"""
        
        elif vuln_type == 'Missing SRI':
            return f"""<b>Generate SRI hashes:</b><br/>
<font face='Courier'>curl -s [CDN_URL] | openssl dgst -sha384 -binary | openssl base64 -A</font><br/>
Add integrity attribute to all {count} CDN scripts.<br/><br/>
<b>AI Prompt:</b> "Add SRI integrity hashes to all CDN script tags in HTML files"""
        
        elif vuln_type == 'Sensitive File Exposed':
            files = ', '.join([f['path'].split('/')[-1] for f in group['files'][:3]])
            return f"""<b>Remove from git:</b><br/>
<font face='Courier'>git rm --cached {files}</font><br/>
<font face='Courier'>echo '{files}' >> .gitignore</font><br/>
Rotate all exposed credentials.<br/><br/>
<b>AI Prompt:</b> "Remove {files} from git history and add to .gitignore"""
        
        elif vuln_type == 'Code Vulnerability':
            return f"""<b>Review and fix:</b> Check all {count} instances for security issues<br/><br/>
<b>AI Prompt:</b> "Fix code vulnerabilities by implementing input validation, parameterized queries, and output encoding"""
        
        elif vuln_type == 'Potential SQL Injection':
            return f"""<b>Fix SQL Injection:</b> Use parameterized queries or prepared statements<br/><br/>
<b>AI Prompt:</b> "Replace string concatenation in SQL queries with parameterized queries to prevent SQL injection"""
        
        elif vuln_type == 'Potential XSS':
            return f"""<b>Fix XSS:</b> Sanitize user input and encode output<br/><br/>
<b>AI Prompt:</b> "Add input sanitization and output encoding to prevent XSS attacks in all user input fields"""
        
        else:
            return f"""{group.get('fix_prompt', f'Review and fix all {count} instances according to OWASP guidelines.')}<br/><br/>
<b>AI Prompt:</b> "Fix {vuln_type} vulnerabilities following OWASP security best practices"""

    
    def _get_vulnerability_explanation(self, vuln_type: str, vuln: Dict) -> str:
        """Get user-friendly explanation for vulnerability type"""
        explanations = {
            'Exposed Secret': 'Exposed credentials can be used by attackers to gain unauthorized access to your systems, databases, or cloud services. This is a critical security risk that must be fixed immediately by rotating credentials and removing them from code.',
            'Outdated Dependency': 'Using outdated packages exposes your application to known security vulnerabilities that have been publicly disclosed. Attackers actively scan for and exploit these weaknesses. Update to the latest secure version immediately.',
            'Missing Security Header': 'Security headers protect your users from common web attacks like clickjacking, XSS, and man-in-the-middle attacks. Missing headers leave your application and users vulnerable to these threats.',
            'Missing SRI': 'Without Subresource Integrity (SRI), attackers can compromise CDN scripts and inject malicious code into your application, affecting all your users. Add integrity hashes to all external scripts.',
            'Sensitive File Exposed': 'Committing sensitive files like .env to version control exposes secrets to anyone with repository access. These secrets remain in git history even after deletion. Remove immediately and rotate all exposed credentials.',
            'Code Vulnerability': 'Code-level vulnerabilities can be exploited to execute arbitrary code, steal data, or compromise your entire application. Review the code carefully and apply security best practices.',
            'Missing CSRF Protection': 'Without CSRF protection, attackers can trick authenticated users into performing unwanted actions on your application. Implement CSRF tokens on all state-changing operations.',
            'Dangerous Function': 'Using dangerous functions like eval() or exec() can lead to remote code execution if user input is not properly sanitized. Replace with safer alternatives or add strict input validation.',
            'Potential SQL Injection': 'SQL injection allows attackers to manipulate database queries, potentially exposing, modifying, or deleting all your data. Use parameterized queries or prepared statements to prevent this.',
            'Potential XSS': 'Cross-Site Scripting (XSS) allows attackers to inject malicious scripts that run in users\' browsers, stealing credentials or performing actions on their behalf. Sanitize all user input and encode output.',
            'Vulnerable Dependency': 'This package version has known security vulnerabilities (CVEs) that are actively exploited. Update to a patched version immediately to protect your application.',
            'Information Disclosure': 'Exposing server information helps attackers identify vulnerabilities and plan attacks. Remove or obfuscate version information from headers and error messages.'
        }
        return explanations.get(vuln_type, 'This vulnerability could be exploited by attackers to compromise your application or data. Review the issue carefully and fix according to security best practices.')
    
    def _calculate_risk_level(self, severity: Dict) -> str:
        """Calculate overall risk level"""
        if severity.get('CRITICAL', 0) > 0:
            return 'CRITICAL'
        elif severity.get('HIGH', 0) > 5:
            return 'HIGH'
        elif severity.get('HIGH', 0) > 0 or severity.get('MEDIUM', 0) > 10:
            return 'MEDIUM'
        else:
            return 'LOW'

if __name__ == "__main__":
    # Test generator
    import json
    
    with open('test_scan.json', 'r') as f:
        data = json.load(f)
    
    generator = PDFReportGenerator()
    generator.generate(data, 'test_report.pdf')
    print("✓ PDF generated: test_report.pdf")

    def _create_business_impact_analysis(self, severity: Dict):
        """Business impact analysis with 4 detailed tables"""
        elements = []
        
        elements.append(Paragraph("📊 BUSINESS IMPACT ANALYSIS", self.heading1_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Table 1: Financial Impact
        financial_data = [
            ['Impact Category', 'Low Risk', 'Medium Risk', 'High Risk', 'Critical Risk'],
            ['Data Breach Cost', '$50K-$100K', '$100K-$500K', '$500K-$2M', '$2M-$10M+'],
            ['Incident Response', '$10K-$25K', '$25K-$75K', '$75K-$200K', '$200K-$500K'],
            ['Legal/Compliance', '$5K-$20K', '$20K-$100K', '$100K-$500K', '$500K-$5M'],
            ['Revenue Loss', '1-2%', '2-5%', '5-15%', '15-40%']
        ]
        
        financial_table = Table(financial_data, colWidths=[1.5*inch, 1.25*inch, 1.25*inch, 1.25*inch, 1.25*inch])
        financial_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (1, 1), (1, -1), colors.HexColor('#d1fae5')),
            ('BACKGROUND', (2, 1), (2, -1), colors.HexColor('#fef3c7')),
            ('BACKGROUND', (3, 1), (3, -1), colors.HexColor('#fed7aa')),
            ('BACKGROUND', (4, 1), (4, -1), colors.HexColor('#fee2e2'))
        ]))
        
        elements.append(Paragraph("<b>Financial Impact</b>", self.heading2_style))
        elements.append(financial_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Table 2: Operational Impact
        operational_data = [
            ['Metric', 'Low', 'Medium', 'High', 'Critical'],
            ['Downtime', '1-4 hours', '4-24 hours', '1-3 days', '3-7+ days'],
            ['Dev Hours to Fix', '10-20 hrs', '20-40 hrs', '40-80 hrs', '80-200+ hrs'],
            ['Team Size Needed', '1-2 devs', '2-3 devs', '3-5 devs', '5-10+ devs'],
            ['Recovery Time', '1-2 days', '3-7 days', '1-2 weeks', '2-4+ weeks']
        ]
        
        operational_table = Table(operational_data, colWidths=[1.5*inch, 1.25*inch, 1.25*inch, 1.25*inch, 1.25*inch])
        operational_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0891b2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(Paragraph("<b>Operational Impact</b>", self.heading2_style))
        elements.append(operational_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Table 3: Reputational Impact
        reputational_data = [
            ['Impact Area', 'Low', 'Medium', 'High', 'Critical'],
            ['Customer Churn', '5-10%', '10-25%', '25-50%', '50-80%'],
            ['Brand Damage', 'Minor', 'Moderate', 'Severe', 'Catastrophic'],
            ['Media Coverage', 'Local', 'Regional', 'National', 'International'],
            ['Recovery Time', '1-3 months', '3-6 months', '6-12 months', '1-3+ years']
        ]
        
        reputational_table = Table(reputational_data, colWidths=[1.5*inch, 1.25*inch, 1.25*inch, 1.25*inch, 1.25*inch])
        reputational_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7c3aed')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(Paragraph("<b>Reputational Impact</b>", self.heading2_style))
        elements.append(reputational_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Table 4: Compliance Impact
        compliance_data = [
            ['Regulation', 'Violation Type', 'Fine Range', 'Additional Penalties'],
            ['GDPR', 'Data Breach', '€20M or 4% revenue', 'Lawsuits, Audits'],
            ['PCI-DSS', 'Card Data Exposure', '$5K-$500K/month', 'Card processing ban'],
            ['HIPAA', 'PHI Breach', '$100-$50K per record', 'Criminal charges'],
            ['SOC 2', 'Control Failure', 'Loss of certification', 'Customer exodus'],
            ['CCPA', 'Privacy Violation', '$2.5K-$7.5K per record', 'Class action suits']
        ]
        
        compliance_table = Table(compliance_data, colWidths=[1.2*inch, 1.5*inch, 1.8*inch, 1.8*inch])
        compliance_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ea580c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        
        elements.append(Paragraph("<b>Compliance & Regulatory Impact</b>", self.heading2_style))
        elements.append(compliance_table)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_manual_testing_guide(self, vulnerabilities):
        """Manual testing guide with 10-15 steps per vulnerability type"""
        elements = []
        
        elements.append(Paragraph("🧪 MANUAL TESTING GUIDE", self.heading1_style))
        elements.append(Paragraph(
            "Step-by-step instructions to manually verify vulnerabilities found by the scanner.",
            self.body_style
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        # Get unique vulnerability types
        vuln_types = list(set([v.get('type', 'Unknown') for v in vulnerabilities]))
        
        for vuln_type in vuln_types[:5]:  # Top 5 types
            elements.extend(self._create_test_procedure(vuln_type))
        
        return elements
    
    def _create_test_procedure(self, vuln_type: str):
        """Create detailed test procedure for vulnerability type"""
        elements = []
        
        elements.append(Paragraph(f"<b>Testing: {vuln_type}</b>", self.heading2_style))
        
        procedures = {
            'Exposed Secret': [
                '1. Open the file containing the exposed secret',
                '2. Search for hardcoded API keys, passwords, tokens',
                '3. Check if secret is in plaintext (not encrypted)',
                '4. Verify secret is committed to git history',
                '5. Test if secret is still active/valid',
                '6. Check .gitignore for proper exclusions',
                '7. Search entire codebase for similar patterns',
                '8. Review environment variable usage',
                '9. Check if .env file exists and is ignored',
                '10. Verify secret rotation procedures'
            ],
            'Outdated Dependency': [
                '1. Check package.json or requirements.txt',
                '2. Run: npm outdated or pip list --outdated',
                '3. Visit CVE database for package vulnerabilities',
                '4. Check package version against latest stable',
                '5. Review CHANGELOG for security fixes',
                '6. Test update in development environment',
                '7. Run automated tests after update',
                '8. Check for breaking changes',
                '9. Update lock files (package-lock.json)',
                '10. Deploy to staging for validation'
            ],
            'Missing Security Header': [
                '1. Open browser DevTools (F12)',
                '2. Navigate to Network tab',
                '3. Load the target page',
                '4. Click on main document request',
                '5. Check Response Headers section',
                '6. Look for: CSP, HSTS, X-Frame-Options',
                '7. Verify header values are secure',
                '8. Test with securityheaders.com',
                '9. Check all pages (not just homepage)',
                '10. Verify headers in production'
            ],
            'Code Vulnerability': [
                '1. Locate the vulnerable code section',
                '2. Identify user input points',
                '3. Test with malicious input',
                '4. Check input validation logic',
                '5. Review output encoding',
                '6. Test edge cases and boundary values',
                '7. Check error handling',
                '8. Review authentication/authorization',
                '9. Test with automated security tools',
                '10. Perform code review with team'
            ]
        }
        
        steps = procedures.get(vuln_type, [
            '1. Identify the vulnerability location',
            '2. Review the vulnerable code',
            '3. Understand the attack vector',
            '4. Test with proof-of-concept',
            '5. Verify the security impact',
            '6. Document the findings',
            '7. Develop fix strategy',
            '8. Implement security controls',
            '9. Test the fix thoroughly',
            '10. Deploy and monitor'
        ])
        
        for step in steps:
            elements.append(Paragraph(step, self.body_style))
        
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_ai_prompts_section(self, vulnerabilities):
        """Create 7 tool-specific AI prompts"""
        elements = []
        
        elements.append(Paragraph("🤖 AI ASSISTANT PROMPTS", self.heading1_style))
        elements.append(Paragraph(
            "Copy these prompts into ChatGPT, Claude, or Amazon Q to automatically fix vulnerabilities:",
            self.body_style
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        prompts = [
            {
                'title': 'Prompt 1: General Security Audit',
                'text': 'Perform a comprehensive security audit of my codebase. Check for: exposed secrets, outdated dependencies, missing security headers, SQL injection, XSS, CSRF vulnerabilities. Provide a detailed report with severity levels and fix recommendations.'
            },
            {
                'title': 'Prompt 2: Fix Exposed Secrets',
                'text': 'I have exposed secrets in my code (API keys, passwords, tokens). Help me: 1) Remove all hardcoded secrets, 2) Set up .env file, 3) Update code to use environment variables, 4) Add .env to .gitignore, 5) Provide secret rotation checklist.'
            },
            {
                'title': 'Prompt 3: Update Dependencies',
                'text': 'My project has outdated dependencies with security vulnerabilities. Analyze my package.json/requirements.txt and: 1) Identify vulnerable packages, 2) Suggest safe update versions, 3) Highlight breaking changes, 4) Provide update commands.'
            },
            {
                'title': 'Prompt 4: Add Security Headers',
                'text': 'Add comprehensive security headers to my application. Include: Content-Security-Policy, Strict-Transport-Security, X-Frame-Options, X-Content-Type-Options, Referrer-Policy. Show implementation for my framework (Flask/Express/Laravel/Django).'
            },
            {
                'title': 'Prompt 5: Fix Input Validation',
                'text': 'Review my code for input validation vulnerabilities. Add proper validation for: SQL injection, XSS, command injection, path traversal. Use parameterized queries, output encoding, and whitelist validation. Show before/after code.'
            },
            {
                'title': 'Prompt 6: Implement CSRF Protection',
                'text': 'Add CSRF protection to all state-changing operations in my application. Implement: CSRF tokens, SameSite cookies, double-submit cookies. Show implementation for my framework with code examples.'
            },
            {
                'title': 'Prompt 7: Security Best Practices',
                'text': 'Review my entire codebase and apply OWASP Top 10 security best practices. Focus on: authentication, authorization, session management, cryptography, error handling, logging. Provide actionable recommendations with code examples.'
            }
        ]
        
        for prompt in prompts:
            elements.append(Paragraph(f"<b>{prompt['title']}</b>", self.heading2_style))
            
            prompt_table = Table([[prompt['text']]], colWidths=[6.5*inch])
            prompt_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f9ff')),
                ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#0891b2')),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('FONTSIZE', (0, 0), (-1, -1), 9)
            ]))
            
            elements.append(prompt_table)
            elements.append(Spacer(1, 0.2*inch))
        
        return elements

    def _create_code_examples(self, vulnerabilities):
        """6 framework code examples"""
        elements = []
        
        elements.append(Paragraph("💻 SECURE CODE EXAMPLES (6 Frameworks)", self.heading1_style))
        elements.append(Spacer(1, 0.2*inch))
        
        examples = [
            {
                'framework': '1. Python (Flask)',
                'vulnerable': '# ❌ VULNERABLE\\ndata = request.args.get("input")\\nprocess(data)  # No validation',
                'secure': '# ✅ SECURE\\ndata = request.args.get("input")\\nif validate_input(data):\\n    process(sanitize(data))'
            },
            {
                'framework': '2. Node.js (Express)',
                'vulnerable': '// ❌ VULNERABLE\\nconst data = req.query.input;\\nprocess(data);  // No validation',
                'secure': '// ✅ SECURE\\nconst data = req.query.input;\\nif (validateInput(data)) {\\n  process(sanitize(data));\\n}'
            },
            {
                'framework': '3. Java (Spring Boot)',
                'vulnerable': '// ❌ VULNERABLE\\nString data = request.getParameter("input");\\nprocess(data);  // No validation',
                'secure': '// ✅ SECURE\\nString data = request.getParameter("input");\\nif (validateInput(data)) {\\n  process(sanitize(data));\\n}'
            },
            {
                'framework': '4. PHP (Laravel)',
                'vulnerable': '// ❌ VULNERABLE\\n$data = $_GET["input"];\\nprocess($data);  // No validation',
                'secure': '// ✅ SECURE\\n$data = $request->input("input");\\nif (validateInput($data)) {\\n  process(sanitize($data));\\n}'
            },
            {
                'framework': '5. Go',
                'vulnerable': '// ❌ VULNERABLE\\ndata := r.URL.Query().Get("input")\\nprocess(data)  // No validation',
                'secure': '// ✅ SECURE\\ndata := r.URL.Query().Get("input")\\nif validateInput(data) {\\n  process(sanitize(data))\\n}'
            },
            {
                'framework': '6. Ruby (Rails)',
                'vulnerable': '# ❌ VULNERABLE\\ndata = params[:input]\\nprocess(data)  # No validation',
                'secure': '# ✅ SECURE\\ndata = params[:input]\\nif validate_input(data)\\n  process(sanitize(data))\\nend'
            }
        ]
        
        for example in examples:
            elements.append(Paragraph(f"<b>{example['framework']}</b>", self.heading2_style))
            elements.append(Spacer(1, 0.1*inch))
            
            elements.append(Paragraph("<font color='red'><b>Vulnerable:</b></font>", self.body_style))
            elements.append(Paragraph(f"<font face='Courier' size='7'>{example['vulnerable']}</font>", self.body_style))
            elements.append(Spacer(1, 0.1*inch))
            
            elements.append(Paragraph("<font color='green'><b>Secure:</b></font>", self.body_style))
            elements.append(Paragraph(f"<font face='Courier' size='7'>{example['secure']}</font>", self.body_style))
            elements.append(Spacer(1, 0.25*inch))
        
        return elements

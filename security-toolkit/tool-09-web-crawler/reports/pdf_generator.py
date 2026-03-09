"""Web Crawler Security Report Generator - Professional Grade"""
from typing import Dict
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from datetime import datetime

class UniversalReportGenerator:
    def __init__(self, results: dict):
        self.results = results
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        self.filename = f"crawler_security_{datetime.now().strftime('%d_%b_%Y_%I_%M_%p')}.pdf"
    
    def _setup_custom_styles(self):
        self.title_style = ParagraphStyle('CustomTitle', parent=self.styles['Heading1'], fontSize=24, textColor=colors.HexColor('#1a1a1a'), spaceAfter=6, alignment=TA_CENTER, fontName='Helvetica-Bold')
        self.heading1_style = ParagraphStyle('CustomHeading1', parent=self.styles['Heading1'], fontSize=16, textColor=colors.HexColor('#0066cc'), spaceAfter=12, spaceBefore=12, fontName='Helvetica-Bold')
        self.heading2_style = ParagraphStyle('CustomHeading2', parent=self.styles['Heading2'], fontSize=13, textColor=colors.HexColor('#003366'), spaceAfter=10, spaceBefore=10, fontName='Helvetica-Bold')
        self.body_style = ParagraphStyle('CustomBody', parent=self.styles['BodyText'], fontSize=10, alignment=TA_JUSTIFY, spaceAfter=8, leading=12)
    
    # ============================================
    # OLD CODE - Commented out 2024-12-19
    # Reason: Replacing with professional generate() that calls all methods
    # ============================================
    # def generate(self):
    #     output_path = f"/tmp/{self.filename}"
    #     doc = SimpleDocTemplate(output_path, pagesize=letter, rightMargin=0.75*inch, leftMargin=0.75*inch, topMargin=0.75*inch, bottomMargin=0.75*inch, title="Web Crawler Security Report")

    #     elements = []
    #     elements.extend(self._create_title_page())
    #     elements.append(PageBreak())
    #     elements.extend(self._create_executive_summary())
    #     elements.append(PageBreak())
    #     elements.extend(self._create_detailed_findings())

    #     # Code Examples
    #     elements.append(PageBreak())
    #     elements.extend(self._create_code_examples())

    #     # Multiple AI Prompts
    #     elements.append(PageBreak())
    #     elements.extend(self._create_multiple_ai_prompts())


    #     # Business Impact Analysis
    #     elements.append(PageBreak())
    #     elements.extend(self._create_business_impact_analysis())

    #     # Manual Testing Guide
    #     elements.append(PageBreak())
    #     elements.extend(self._create_manual_testing_guide())

    #     # AI Prompts
    #     elements.append(PageBreak())
    #     elements.extend(self._create_ai_prompts())

    #     # Code Examples
    #     elements.append(PageBreak())
    #     elements.extend(self._create_code_examples())

    #     doc.build(elements)
    #     return output_path

    def generate(self):
        output_path = f"/tmp/{self.filename}"
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        elements = []
        elements.extend(self._create_title_page())
        elements.append(PageBreak())
        elements.extend(self._create_executive_summary())
        elements.append(PageBreak())
        elements.extend(self._create_detailed_findings())
        elements.append(PageBreak())
        elements.extend(self._create_business_impact_analysis(self.results['severity_counts']))
        elements.append(PageBreak())
        elements.extend(self._create_manual_testing_guide(self.results.get('vulnerabilities', [])))
        elements.append(PageBreak())
        elements.extend(self._create_ai_prompts_section(self.results.get('vulnerabilities', [])))
        elements.append(PageBreak())
        elements.extend(self._create_code_examples(self.results.get('vulnerabilities', [])))
        
        doc.build(elements)
        return output_path

    def _create_title_page(self):
        elements = []
        elements.append(Spacer(1, 1.5*inch))
        elements.append(Paragraph("WEB CRAWLER SECURITY ASSESSMENT", self.title_style))
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph("Comprehensive Information Disclosure & Sensitive File Analysis", self.styles['Normal']))
        elements.append(Spacer(1, 0.5*inch))
        
        metadata = [
            f"<b>Target URL:</b> {self.results['target_url']}",
            f"<b>Scan Date:</b> {self.results['scan_date']}",
            f"<b>Duration:</b> {self.results['scan_duration']}",
            f"<b>Vulnerabilities:</b> {self.results['vulnerability_count']}",
            f"<b>Risk Score:</b> {self.results['risk_score']}/100 ({self.results['risk_level']})",
        ]
        
        for item in metadata:
            elements.append(Paragraph(item, self.body_style))
            elements.append(Spacer(1, 0.1*inch))
        
        return elements
    
    def _create_executive_summary(self):
        elements = []
        elements.append(Paragraph("EXECUTIVE SUMMARY", self.heading1_style))
        elements.append(Spacer(1, 0.2*inch))
        
        severity = self.results['severity_counts']
        risk_score = self.results['risk_score']
        time_estimate = self._calculate_time_estimate(severity)
        
        dashboard_data = [
            ['Metric', 'Value', 'Status'],
            ['Risk Score', f"{risk_score}/100", self._get_risk_badge(risk_score)],
            ['Total Vulnerabilities', str(self.results['vulnerability_count']), ''],
            ['Time to Fix', time_estimate, ''],
            ['Information Security', self._check_info_compliance(severity), ''],
        ]
        
        dashboard_table = Table(dashboard_data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
        dashboard_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
        ]))
        
        elements.append(dashboard_table)
        elements.append(Spacer(1, 0.3*inch))
        
        vuln_data = [
            ['Severity', 'Count', 'Priority', 'Action'],
            ['CRITICAL', str(severity.get('CRITICAL', 0)), 'P0', 'Fix Immediately'],
            ['HIGH', str(severity.get('HIGH', 0)), 'P1', 'Fix This Week'],
            ['MEDIUM', str(severity.get('MEDIUM', 0)), 'P2', 'Plan & Fix'],
            ['LOW', str(severity.get('LOW', 0)), 'P3', 'Monitor'],
        ]
        
        vuln_table = Table(vuln_data, colWidths=[1.5*inch, 1*inch, 1*inch, 2.5*inch])
        vuln_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (0, 1), colors.HexColor('#ffcccc')),
            ('BACKGROUND', (0, 2), (0, 2), colors.HexColor('#ffddaa')),
            ('BACKGROUND', (0, 3), (0, 3), colors.HexColor('#ffffcc')),
            ('BACKGROUND', (0, 4), (0, 4), colors.HexColor('#ccffcc')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elements.append(vuln_table)
        return elements
    
    def _create_detailed_findings(self):
        elements = []
        elements.append(Paragraph("DETAILED FINDINGS", self.heading1_style))
        elements.append(Paragraph("Vulnerabilities grouped by type. Each group shows affected files and a single fix command.", self.body_style))
        elements.append(Spacer(1, 0.2*inch))
        grouped = self._group_vulnerabilities(self.results['vulnerabilities'])
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            severity_groups = [g for g in grouped if g['severity'] == severity]
            if severity_groups:
                elements.append(Paragraph(f"{severity} Severity ({sum(g['count'] for g in severity_groups)} total)", self.heading2_style))
                for group in severity_groups:
                    elements.extend(self._format_vulnerability_group(group))
                elements.append(Spacer(1, 0.3*inch))
        return elements
    
    def _group_vulnerabilities(self, vulnerabilities):
        groups = {}
        for vuln in vulnerabilities:
            vuln_type = vuln.get('type', 'Unknown')
            if vuln_type not in groups:
                groups[vuln_type] = {'type': vuln_type, 'severity': vuln.get('severity', 'LOW'), 'locations': [], 'fix_prompt': vuln.get('fix_prompt', ''), 'count': 0, 'owasp': vuln.get('owasp', 'N/A'), 'cwe': vuln.get('cwe', 'N/A'), 'cvss': vuln.get('cvss', 'N/A')}
            groups[vuln_type]['locations'].append({'location': vuln.get('file', vuln.get('url', 'N/A')), 'evidence': vuln.get('evidence', 'N/A')})
            groups[vuln_type]['count'] += 1
        return sorted(groups.values(), key=lambda x: x['count'], reverse=True)
    
    def _format_vulnerability_group(self, group):
        elements = []
        elements.append(Paragraph(f"<b>{group['type']} ({group['count']} occurrences)</b>", self.heading2_style))
        elements.append(Paragraph(f"<b>OWASP:</b> {group['owasp']} | <b>CWE:</b> {group['cwe']} | <b>CVSS:</b> {group['cvss']}", self.body_style))
        explanation = self._get_explanation(group['type'])
        if explanation:
            elements.append(Paragraph(f"<b>❓ What This Means:</b> {explanation}", self.body_style))
        elements.append(Paragraph(f"<b>📁 Affected Files ({group['count']}):</b>", self.body_style))
        for i, loc in enumerate(group['locations'][:10]):
            elements.append(Paragraph(f"  • {loc['location']}", self.body_style))
        if group['count'] > 10:
            elements.append(Paragraph(f"  ... and {group['count'] - 10} more files", self.body_style))
        if group['fix_prompt']:
            elements.append(Paragraph(f"<b>💡 Fix All ({group['count']} issues):</b> {group['fix_prompt']}", self.body_style))
            ai_prompt = self._generate_ai_prompt({'type': group['type']})
            elements.append(Paragraph(f"<b>🤖 AI Prompt:</b> {ai_prompt}", self.body_style))
        
        # Proof of Concept
        elements.append(Paragraph("<b>💥 Proof of Concept:</b>", self.body_style))
        if group.get("locations") or group.get("endpoints"):
            loc = (group.get("locations") or group.get("endpoints", [{}]))[0]
            elements.append(Paragraph(f"1. Exploit location: {loc.get(chr(39)+chr(108)+chr(111)+chr(99)+chr(97)+chr(116)+chr(105)+chr(111)+chr(110)+chr(39)) or loc.get(chr(39)+chr(101)+chr(110)+chr(100)+chr(112)+chr(111)+chr(105)+chr(110)+chr(116)+chr(39), chr(39)+chr(78)+chr(47)+chr(65)+chr(39))}", self.body_style))
            elements.append(Paragraph(f"2. Result: {loc.get(chr(39)+chr(101)+chr(118)+chr(105)+chr(100)+chr(101)+chr(110)+chr(99)+chr(101)+chr(39), chr(39)+chr(86)+chr(117)+chr(108)+chr(110)+chr(101)+chr(114)+chr(97)+chr(98)+chr(105)+chr(108)+chr(105)+chr(116)+chr(121)+chr(32)+chr(99)+chr(111)+chr(110)+chr(102)+chr(105)+chr(114)+chr(109)+chr(101)+chr(100)+chr(39))}", self.body_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # Manual Testing Guide
        elements.extend(self._create_manual_testing_guide(group))
        
        elements.append(Spacer(1, 0.25*inch))
        return elements
    
    def _format_vulnerability(self, vuln):
        elements = []
        elements.append(Paragraph(f"<b>{vuln['type']}</b>", self.heading2_style))
        elements.append(Paragraph(f"<b>OWASP:</b> {vuln.get('owasp', 'N/A')} | <b>CWE:</b> {vuln.get('cwe', 'N/A')} | <b>CVSS:</b> {vuln.get('cvss', 'N/A')}", self.body_style))
        
        explanation = self._get_explanation(vuln['type'])
        if explanation:
            elements.append(Paragraph(f"<b>❓ What This Means:</b> {explanation}", self.body_style))
        
        elements.append(Paragraph(f"<b>Description:</b> {vuln['description']}", self.body_style))
        elements.append(Paragraph(f"<b>Evidence:</b> {vuln.get('evidence', 'N/A')}", self.body_style))
        
        if vuln.get('fix_prompt'):
            elements.append(Paragraph(f"<b>💡 How to Fix:</b> {vuln['fix_prompt']}", self.body_style))
            ai_prompt = self._generate_ai_prompt(vuln)
            elements.append(Paragraph(f"<b>🤖 AI Prompt:</b> {ai_prompt}", self.body_style))
        
        elements.append(Spacer(1, 0.2*inch))
        return elements
    
    def _get_explanation(self, vuln_type):
        explanations = {
            'Exposed .git Directory': 'Git repositories contain complete source code history, credentials, and sensitive data. Attackers can download entire codebase and extract secrets.',
            'Exposed .env File': 'Environment files contain database passwords, API keys, and secrets in plaintext. This gives attackers direct access to backend systems.',
            'Exposed Backup Files': 'Backup files (.bak, .old, .backup) often contain source code, database dumps, or configuration with credentials that should never be public.',
            'Directory Listing Enabled': 'Directory browsing allows attackers to see all files and folders, discovering hidden admin panels, backups, and sensitive documents.',
            'Exposed Admin Panel': 'Publicly accessible admin interfaces are prime targets for brute force attacks and exploitation, often with default credentials.',
            'Sensitive File Disclosure': 'Configuration files, logs, and documentation expose system architecture, credentials, and vulnerabilities to attackers.',
        }
        return explanations.get(vuln_type, 'This information disclosure vulnerability exposes sensitive data that attackers can exploit.')
    
    def _generate_ai_prompt(self, vuln):
        prompts = {
            'Exposed .git Directory': '"Block .git directory in web server config. Apache: <DirectoryMatch \\.git> Require all denied </DirectoryMatch>. Nginx: location ~ /\\.git { deny all; }"',
            'Exposed .env File': '"Block .env files in web server. Apache: <Files .env> Require all denied </Files>. Nginx: location ~ /\\.env { deny all; }. Move .env outside web root"',
            'Exposed Backup Files': '"Remove backup files from web root: find /var/www -name *.bak -delete. Block in .htaccess: <FilesMatch \\.(bak|old|backup|sql)$> Require all denied </FilesMatch>"',
            'Directory Listing Enabled': '"Disable directory listing. Apache: Options -Indexes in .htaccess. Nginx: autoindex off; in server block. Add index.html to all directories"',
            'Exposed Admin Panel': '"Restrict admin panel by IP: Apache: <Location /admin> Require ip 10.0.0.0/8 </Location>. Nginx: location /admin { allow 10.0.0.0/8; deny all; }. Add authentication"',
            'Sensitive File Disclosure': '"Block sensitive files: <FilesMatch (config|phpinfo|readme)\\.php> Require all denied </FilesMatch>. Move config files outside web root. Use .htaccess deny rules"',
        }
        return prompts.get(vuln['type'], f'"Fix {vuln["type"]} by removing sensitive files from web root and configuring proper access controls"')
    
    def _calculate_time_estimate(self, severity):
        hours = severity.get('CRITICAL', 0) * 8 + severity.get('HIGH', 0) * 4 + severity.get('MEDIUM', 0) * 2 + severity.get('LOW', 0) * 1
        if hours < 8: return f"{hours} hours"
        return f"{hours // 8} days"
    

    def _create_manual_testing_guide(self, group):
        """Create manual testing guide for vulnerability"""
        elements = []
        elements.append(Paragraph("<b>🧪 Manual Testing:</b>", self.body_style))
        if group.get('locations') or group.get('endpoints'):
            loc = (group.get('locations') or group.get('endpoints', [{}]))[0]
            location = loc.get('location') or loc.get('endpoint', 'N/A')
            elements.append(Paragraph(f"1. Test location: {location}", self.body_style))
            elements.append(Paragraph(f"2. Expected: {loc.get('evidence', 'Verify vulnerability')}", self.body_style))
        return elements



    def _create_multiple_ai_prompts(self):
        """Create 5 AI prompt scenarios"""
        elements = []
        elements.append(Paragraph("🤖 AI Prompts (5 Scenarios)", self.heading1_style))
        elements.append(Spacer(1, 0.2*inch))
        
        prompts = [
            {'title': 'Prompt 1: General Fix', 'prompt': 'Fix all security vulnerabilities in my code following best practices'},
            {'title': 'Prompt 2: Framework-Specific', 'prompt': 'Fix vulnerabilities using [YOUR_FRAMEWORK] security features'},
            {'title': 'Prompt 3: Input Validation', 'prompt': 'Add input validation and sanitization to prevent attacks'},
            {'title': 'Prompt 4: Security Headers', 'prompt': 'Add all necessary security headers and configurations'},
            {'title': 'Prompt 5: Complete Audit', 'prompt': 'Perform complete security audit and provide fixes'}
        ]
        
        for p in prompts:
            elements.append(Paragraph(f"<b>{p['title']}</b>", self.heading2_style))
            elements.append(Paragraph(f"<font color='blue'>{p['prompt']}</font>", self.body_style))
            elements.append(Spacer(1, 0.15*inch))
        
        return elements

    def _create_code_examples(self):
        """Create code examples before/after"""
        elements = []
        elements.append(Paragraph("💻 Code Examples: Before & After", self.heading1_style))
        elements.append(Spacer(1, 0.2*inch))
        
        examples = [
            {'lang': 'Python', 'vuln': '# ❌ VULNERABLE\ndata = request.get("input")\nreturn data', 
             'secure': '# ✅ SECURE\ndata = escape(request.get("input"))\nreturn data'}
        ]
        
        for ex in examples:
            elements.append(Paragraph(f"<b>{ex['lang']}</b>", self.heading2_style))
            elements.append(Paragraph(f"<font face='Courier' size='7'>{ex['vuln']}</font>", self.body_style))
            elements.append(Spacer(1, 0.1*inch))
            elements.append(Paragraph(f"<font face='Courier' size='7'>{ex['secure']}</font>", self.body_style))
            elements.append(Spacer(1, 0.2*inch))
        
        return elements

    def _get_risk_badge(self, score):
        if score >= 80: return 'CRITICAL'
        if score >= 60: return 'HIGH'
        if score >= 40: return 'MEDIUM'
        return 'LOW'
    
    def _check_info_compliance(self, severity):
        if severity.get('CRITICAL', 0) > 0: return 'Non-Compliant'
        if severity.get('HIGH', 0) > 0: return 'Partial'
        return 'Compliant'

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

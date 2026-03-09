#!/usr/bin/env python3
"""
SQL Injection PDF Report Generator
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime

class PDFReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._add_custom_styles()
    
    def _add_custom_styles(self):
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#0891b2'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#0891b2'),
            spaceAfter=12,
            spaceBefore=12
        ))
    
    def _calculate_risk_score(self, vulnerabilities):
        """Calculate overall risk score 0-100"""
        if not vulnerabilities:
            return 0
        
        severity_scores = {'CRITICAL': 25, 'HIGH': 15, 'MEDIUM': 8, 'LOW': 3}
        total_score = sum(severity_scores.get(v['severity'], 0) for v in vulnerabilities)
        return min(100, total_score)
    
    def _get_owasp_info(self, vuln_type):
        """Get OWASP reference for vulnerability type"""
        return {
            'category': 'A03:2021 - Injection',
            'cwe': 'CWE-89: SQL Injection',
            'cvss': '9.8 (Critical)',
            'reference': 'https://owasp.org/Top10/A03_2021-Injection/'
        }
    
    def generate(self, report_data, output_path):
        """Generate PDF report"""
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        story = []
        
        # Title
        story.append(Paragraph("SQL Injection Security Report", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))
        
        # Scan Info
        info_data = [
            ['Scan Date:', report_data['scan_date']],
            ['Target URL:', report_data['target']],
            ['Parameters Tested:', str(report_data.get('parameters_tested', 0))],
            ['Vulnerabilities Found:', str(report_data['total_vulnerabilities'])]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4.5*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f9ff')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(info_table)
        story.append(Spacer(1, 0.5*inch))
        
        # Executive Summary Dashboard
        if report_data['vulnerabilities']:
            story.append(Paragraph("📊 Executive Summary Dashboard", self.styles['SectionHeader']))
            
            risk_score = self._calculate_risk_score(report_data['vulnerabilities'])
            risk_level = 'CRITICAL' if risk_score >= 75 else 'HIGH' if risk_score >= 50 else 'MEDIUM' if risk_score >= 25 else 'LOW'
            
            critical_count = sum(1 for v in report_data['vulnerabilities'] if v['severity'] == 'CRITICAL')
            high_count = sum(1 for v in report_data['vulnerabilities'] if v['severity'] == 'HIGH')
            medium_count = sum(1 for v in report_data['vulnerabilities'] if v['severity'] == 'MEDIUM')
            low_count = sum(1 for v in report_data['vulnerabilities'] if v['severity'] == 'LOW')
            
            dashboard_data = [
                ['Security Risk Score:', f'{risk_score}/100 ({risk_level})', 'Total Vulnerabilities:', str(report_data['total_vulnerabilities'])],
                ['Critical Issues:', str(critical_count), 'High Issues:', str(high_count)],
                ['Medium Issues:', str(medium_count), 'Low Issues:', str(low_count)],
                ['Parameters Tested:', str(report_data.get('parameters_tested', 0)), 'Payloads Used:', '60+']
            ]
            
            dashboard_table = Table(dashboard_data, colWidths=[1.8*inch, 1.8*inch, 1.8*inch, 1.8*inch])
            dashboard_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fef3c7')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))
            story.append(dashboard_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Summary
        if report_data['total_vulnerabilities'] > 0:
            story.append(Paragraph("⚠️ VULNERABILITIES DETECTED", self.styles['SectionHeader']))
            story.append(Paragraph(
                f"Found <b>{report_data['total_vulnerabilities']}</b> SQL injection vulnerabilities. "
                "Your application is at risk of database attacks. Immediate action required!",
                self.styles['BodyText']
            ))
        else:
            story.append(Paragraph("✅ NO VULNERABILITIES FOUND", self.styles['SectionHeader']))
            story.append(Paragraph(
                "No SQL injection vulnerabilities detected. Your application appears secure against basic SQL injection attacks.",
                self.styles['BodyText']
            ))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Vulnerabilities
        if report_data['vulnerabilities']:
            story.append(PageBreak())
            story.append(Paragraph("Vulnerability Details", self.styles['SectionHeader']))
            story.append(Spacer(1, 0.2*inch))
            
            for i, vuln in enumerate(report_data['vulnerabilities'], 1):
                # Vulnerability header
                story.append(Paragraph(f"<b>Vulnerability #{i}</b>", self.styles['Heading3']))
                
                # Details table
                vuln_data = [
                    ['Parameter:', vuln['parameter']],
                    ['Type:', vuln['type']],
                    ['Severity:', vuln['severity']],
                    ['Payload Used:', vuln['payload']],
                    ['Evidence:', vuln['evidence']]
                ]
                
                vuln_table = Table(vuln_data, colWidths=[1.5*inch, 5*inch])
                vuln_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fef3c7')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP')
                ]))
                story.append(vuln_table)
                story.append(Spacer(1, 0.2*inch))
                
                # OWASP Reference
                owasp = self._get_owasp_info(vuln['type'])
                story.append(Paragraph("<b>OWASP Reference:</b>", self.styles['Heading3']))
                owasp_data = [
                    ['OWASP Category:', owasp['category']],
                    ['CWE ID:', owasp['cwe']],
                    ['CVSS Score:', owasp['cvss']]
                ]
                owasp_table = Table(owasp_data, colWidths=[1.5*inch, 5*inch])
                owasp_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#dbeafe')),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey)
                ]))
                story.append(owasp_table)
                story.append(Spacer(1, 0.2*inch))
                
                # Proof of Concept
                story.append(Paragraph("<b>💥 Proof of Concept (PoC):</b>", self.styles['Heading3']))
                poc_steps = [
                    f"1. Original URL: {vuln.get('url', 'N/A').split('?')[0]}",
                    f"2. Vulnerable Parameter: {vuln['parameter']}",
                    f"3. Malicious Payload: {vuln['payload']}",
                    f"4. Result: {vuln['evidence']}",
                    "5. Impact: Attacker can access/modify database records"
                ]
                for step in poc_steps:
                    story.append(Paragraph(f"<font face='Courier' size='8'>{step}</font>", self.styles['BodyText']))
                story.append(Spacer(1, 0.3*inch))
                
                # Manual Testing Guide
                story.append(Paragraph("<b>🧪 Manual Testing Guide (Test It Yourself):</b>", self.styles['Heading3']))
                story.append(Paragraph(
                    "<b>Follow these steps to manually verify this vulnerability in your browser:</b>",
                    self.styles['BodyText']
                ))
                story.append(Spacer(1, 0.1*inch))
                
                # Build exploit URL
                base_url = vuln.get('url', 'N/A')
                if '?' in base_url:
                    url_parts = base_url.split('?')
                    base = url_parts[0]
                    params = url_parts[1].split('&')
                    
                    # Create normal URL
                    normal_url = base_url
                    
                    # Create exploit URL by replacing vulnerable parameter
                    exploit_params = []
                    for param in params:
                        if '=' in param:
                            key, val = param.split('=', 1)
                            if key == vuln['parameter']:
                                exploit_params.append(f"{key}={vuln['payload']}")
                            else:
                                exploit_params.append(param)
                    exploit_url = base + '?' + '&'.join(exploit_params)
                    
                    manual_steps = [
                        "<b>Step 1: Test Normal Request</b>",
                        f"Open this URL in your browser (normal behavior):",
                        f"<font face='Courier' size='7' color='blue'>{normal_url}</font>",
                        "Expected: Shows normal results (e.g., filtered products)",
                        "",
                        "<b>Step 2: Test SQL Injection</b>",
                        f"Now open this URL with the malicious payload:",
                        f"<font face='Courier' size='7' color='red'>{exploit_url}</font>",
                        f"Expected: {vuln['evidence']}",
                        "",
                        "<b>Step 3: What to Look For</b>",
                        "• More results than normal (hidden data exposed)",
                        "• Database error messages visible",
                        "• Different page behavior or content",
                        "• Longer response time (for time-based injection)",
                        "",
                        "<b>Step 4: Confirm Vulnerability</b>",
                        "If you see different results between Step 1 and Step 2,",
                        "the vulnerability is CONFIRMED. The database is accepting",
                        "malicious SQL code from user input."
                    ]
                else:
                    manual_steps = [
                        "<b>Manual Testing:</b>",
                        f"1. Navigate to: {base_url}",
                        f"2. Find input field for parameter: {vuln['parameter']}",
                        f"3. Enter this payload: {vuln['payload']}",
                        f"4. Expected result: {vuln['evidence']}"
                    ]
                
                for step in manual_steps:
                    story.append(Paragraph(step, self.styles['BodyText']))
                story.append(Spacer(1, 0.3*inch))
            
            # Business Impact Section
            story.append(PageBreak())
            story.append(Paragraph("💰 Business Impact Analysis", self.styles['SectionHeader']))
            story.append(Spacer(1, 0.2*inch))
            
            impact_data = [
                ['🚨 Risk Category', 'Potential Impact'],
                ['Data Breach', 'Customer data, passwords, credit cards exposed'],
                ['Financial Loss', '$50,000 - $500,000 average breach cost'],
                ['Reputation Damage', 'Loss of customer trust, negative press'],
                ['Legal Consequences', 'GDPR fines up to €20M or 4% revenue'],
                ['Business Disruption', 'Service downtime, emergency response costs'],
                ['Compliance Violations', 'PCI-DSS, HIPAA, SOC 2 failures']
            ]
            
            impact_table = Table(impact_data, colWidths=[2*inch, 4.5*inch])
            impact_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fee2e2')),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]))
            story.append(impact_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Remediation Priority Matrix
            story.append(Paragraph("⏱️ Remediation Priority Matrix", self.styles['SectionHeader']))
            story.append(Spacer(1, 0.2*inch))
            
            priority_data = [
                ['Severity', 'Fix Timeline', 'Priority Level', 'Action Required'],
                ['CRITICAL', '24 hours', 'P0 - Immediate', 'Stop deployment, fix now'],
                ['HIGH', '1 week', 'P1 - Urgent', 'Schedule immediate fix'],
                ['MEDIUM', '1 month', 'P2 - Important', 'Plan in next sprint'],
                ['LOW', '3 months', 'P3 - Normal', 'Add to backlog']
            ]
            
            priority_table = Table(priority_data, colWidths=[1.5*inch, 1.5*inch, 1.8*inch, 1.8*inch])
            priority_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0891b2')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('BACKGROUND', (0, 1), (0, 1), colors.HexColor('#fee2e2')),
                ('BACKGROUND', (0, 2), (0, 2), colors.HexColor('#fed7aa')),
                ('BACKGROUND', (0, 3), (0, 3), colors.HexColor('#fef3c7')),
                ('BACKGROUND', (0, 4), (0, 4), colors.HexColor('#d1fae5')),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER')
            ]))
            story.append(priority_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Fix Recommendations
        story.append(PageBreak())
        story.append(Paragraph("🛠️ How to Fix (Simple English)", self.styles['SectionHeader']))
        story.append(Spacer(1, 0.2*inch))
        
        story.append(Paragraph("<b>What is SQL Injection?</b>", self.styles['Heading3']))
        story.append(Paragraph(
            "SQL Injection is like a hacker tricking your database by inserting malicious code into input fields. "
            "Instead of searching for 'apple', they search for 'apple' OR '1'='1' which makes your database return ALL data.",
            self.styles['BodyText']
        ))
        story.append(Spacer(1, 0.2*inch))
        
        story.append(Paragraph("<b>Why is it Dangerous?</b>", self.styles['Heading3']))
        story.append(Paragraph(
            "Hackers can: <br/>"
            "• Steal all your user passwords and emails<br/>"
            "• Delete your entire database<br/>"
            "• Modify data (change prices, add fake accounts)<br/>"
            "• Take complete control of your server",
            self.styles['BodyText']
        ))
        story.append(Spacer(1, 0.2*inch))
        
        story.append(Paragraph("<b>How to Fix It (3 Steps):</b>", self.styles['Heading3']))
        
        fix_steps = [
            "<b>1. Use Prepared Statements (Parameterized Queries)</b><br/>"
            "Instead of: <font color='red'>query = \"SELECT * FROM users WHERE id = \" + user_input</font><br/>"
            "Use: <font color='green'>query = \"SELECT * FROM users WHERE id = ?\" with parameters</font><br/>"
            "This separates code from data, so hackers can't inject SQL.",
            
            "<b>2. Validate All User Input</b><br/>"
            "• Only allow expected characters (letters, numbers)<br/>"
            "• Reject special characters like ' \" ; -- /*<br/>"
            "• Set maximum length limits<br/>"
            "• Use whitelist validation (only allow known good values)",
            
            "<b>3. Use ORM Libraries</b><br/>"
            "• For Python: Use SQLAlchemy or Django ORM<br/>"
            "• For Node.js: Use Sequelize or Prisma<br/>"
            "• For PHP: Use PDO or Laravel Eloquent<br/>"
            "These libraries automatically protect against SQL injection."
        ]
        
        for step in fix_steps:
            story.append(Paragraph(step, self.styles['BodyText']))
            story.append(Spacer(1, 0.15*inch))
        
        # Code Examples (Before/After)
        story.append(PageBreak())
        story.append(Paragraph("💻 Code Examples: Before & After", self.styles['SectionHeader']))
        story.append(Spacer(1, 0.2*inch))
        
        code_examples = [
            {
                'language': 'Python (Flask)',
                'vulnerable': '''# ❌ VULNERABLE CODE\n@app.route('/search')\ndef search():\n    query = request.args.get('q')\n    sql = f"SELECT * FROM products WHERE name LIKE '%{query}%'"\n    results = db.execute(sql)  # DANGEROUS!\n    return jsonify(results)''',
                'secure': '''# ✅ SECURE CODE\n@app.route('/search')\ndef search():\n    query = request.args.get('q')\n    sql = "SELECT * FROM products WHERE name LIKE ?"\n    results = db.execute(sql, (f'%{query}%',))  # SAFE!\n    return jsonify(results)'''
            },
            {
                'language': 'Node.js (Express)',
                'vulnerable': '''// ❌ VULNERABLE CODE\napp.get('/user', (req, res) => {\n  const id = req.query.id;\n  const query = `SELECT * FROM users WHERE id = ${id}`;\n  db.query(query, (err, results) => {  // DANGEROUS!\n    res.json(results);\n  });\n});''',
                'secure': '''// ✅ SECURE CODE\napp.get('/user', (req, res) => {\n  const id = req.query.id;\n  const query = 'SELECT * FROM users WHERE id = ?';\n  db.query(query, [id], (err, results) => {  // SAFE!\n    res.json(results);\n  });\n});'''
            },
            {
                'language': 'PHP',
                'vulnerable': '''// ❌ VULNERABLE CODE\n$id = $_GET['id'];\n$query = "SELECT * FROM users WHERE id = $id";\n$result = mysqli_query($conn, $query);  // DANGEROUS!''',
                'secure': '''// ✅ SECURE CODE\n$id = $_GET['id'];\n$stmt = $conn->prepare("SELECT * FROM users WHERE id = ?");\n$stmt->bind_param("i", $id);\n$stmt->execute();  // SAFE!'''
            }
        ]
        
        for example in code_examples:
            story.append(Paragraph(f"<b>{example['language']}</b>", self.styles['Heading3']))
            story.append(Spacer(1, 0.1*inch))
            
            story.append(Paragraph("<font color='red'><b>Vulnerable Code:</b></font>", self.styles['BodyText']))
            story.append(Paragraph(
                f"<font face='Courier' size='7'>{example['vulnerable']}</font>",
                self.styles['BodyText']
            ))
            story.append(Spacer(1, 0.15*inch))
            
            story.append(Paragraph("<font color='green'><b>Secure Code:</b></font>", self.styles['BodyText']))
            story.append(Paragraph(
                f"<font face='Courier' size='7'>{example['secure']}</font>",
                self.styles['BodyText']
            ))
            story.append(Spacer(1, 0.25*inch))
        
        # AI Fix Prompts
        story.append(PageBreak())
        story.append(Paragraph("🤖 AI Assistant Prompts (Copy & Paste)", self.styles['SectionHeader']))
        story.append(Spacer(1, 0.2*inch))
        
        story.append(Paragraph(
            "Copy these prompts and paste them into ChatGPT, Claude, or any AI assistant to get code fixes:",
            self.styles['BodyText']
        ))
        story.append(Spacer(1, 0.2*inch))
        
        # Group vulnerabilities by parameter
        params_affected = list(set([v['parameter'] for v in report_data['vulnerabilities']]))
        
        for param in params_affected:
            story.append(Paragraph(f"<b>For parameter: {param}</b>", self.styles['Heading3']))
            
            prompt_text = (
                f"I have a SQL injection vulnerability in my web application. "
                f"The vulnerable parameter is '{param}'. "
                f"Please provide secure code to fix this using prepared statements/parameterized queries. "
                f"Show me the vulnerable code and the fixed code with explanations. "
                f"I'm using [YOUR_LANGUAGE/FRAMEWORK - e.g., Python Flask, Node.js Express, PHP]."
            )
            
            story.append(Paragraph(
                f"<font color='blue' face='Courier'>{prompt_text}</font>",
                self.styles['BodyText']
            ))
            story.append(Spacer(1, 0.2*inch))
        
        # General fix prompt
        story.append(Paragraph("<b>General Security Audit Prompt:</b>", self.styles['Heading3']))
        general_prompt = (
            "Review my code for SQL injection vulnerabilities and provide secure alternatives. "
            "Show me how to implement prepared statements, input validation, and ORM usage. "
            "Include code examples in [YOUR_LANGUAGE]."
        )
        story.append(Paragraph(
            f"<font color='blue' face='Courier'>{general_prompt}</font>",
            self.styles['BodyText']
        ))
        
        # ============================================
        # OLD CODE - Commented out 2024
        # Reason: Adding new professional sections
        # ============================================
        # doc.build(story)
        # print(f"PDF report generated: {output_path}")
        
        # Business Impact Analysis
        story.append(PageBreak())
        story.extend(self._create_business_impact_detailed())
        
        # AI Prompts
        story.append(PageBreak())
        story.extend(self._create_comprehensive_ai_prompts())
        
        # Code Examples
        story.append(PageBreak())
        story.extend(self._create_code_examples_multi_framework())
        
        # Build PDF
        doc.build(story)
        print(f"PDF report generated: {output_path}")

    def _create_business_impact_detailed(self):
        """Business impact with 4 comprehensive tables"""
        elements = []
        
        elements.append(Paragraph("📊 BUSINESS IMPACT ANALYSIS", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Financial Impact Table
        financial_data = [
            ['Impact Type', 'Low', 'Medium', 'High', 'Critical'],
            ['Data Breach Cost', '$75K-$150K', '$150K-$500K', '$500K-$2M', '$2M-$10M+'],
            ['Forensics & Investigation', '$15K-$30K', '$30K-$100K', '$100K-$300K', '$300K-$1M'],
            ['Legal Fees', '$10K-$50K', '$50K-$200K', '$200K-$750K', '$750K-$5M'],
            ['Customer Compensation', '$5K-$25K', '$25K-$150K', '$150K-$500K', '$500K-$3M']
        ]
        
        financial_table = Table(financial_data, colWidths=[1.5*inch, 1.25*inch, 1.25*inch, 1.25*inch, 1.25*inch])
        financial_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(Paragraph("<b>1. Financial Impact</b>", self.styles['Heading3']))
        elements.append(financial_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Operational Impact
        operational_data = [
            ['Metric', 'Low', 'Medium', 'High', 'Critical'],
            ['Database Recovery', '2-4 hours', '4-12 hours', '12-48 hours', '2-7 days'],
            ['Dev Team Hours', '20-40 hrs', '40-80 hrs', '80-160 hrs', '160-400 hrs'],
            ['Service Downtime', '1-2 hours', '2-8 hours', '8-24 hours', '1-5 days'],
            ['Customer Impact', '100-500', '500-5K', '5K-50K', '50K-500K+']
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
        
        elements.append(Paragraph("<b>2. Operational Impact</b>", self.styles['Heading3']))
        elements.append(operational_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Reputational Impact
        reputational_data = [
            ['Impact Area', 'Low', 'Medium', 'High', 'Critical'],
            ['Customer Trust Loss', '10-20%', '20-40%', '40-65%', '65-90%'],
            ['Media Coverage', 'Tech blogs', 'Industry news', 'National news', 'Global headlines'],
            ['Brand Recovery', '2-4 months', '4-8 months', '8-18 months', '18-36 months'],
            ['Competitor Advantage', 'Minor', 'Moderate', 'Significant', 'Severe']
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
        
        elements.append(Paragraph("<b>3. Reputational Impact</b>", self.styles['Heading3']))
        elements.append(reputational_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Compliance Impact
        compliance_data = [
            ['Regulation', 'Violation', 'Fine Range', 'Additional Consequences'],
            ['GDPR (EU)', 'Data breach', '€20M or 4% revenue', 'Lawsuits, audits, bans'],
            ['PCI-DSS', 'Card data leak', '$5K-$500K/month', 'Processing privileges revoked'],
            ['HIPAA (US)', 'PHI exposure', '$100-$50K/record', 'Criminal prosecution'],
            ['SOX (US)', 'Financial data', '$5M fine + jail', 'Executive liability'],
            ['CCPA (CA)', 'Privacy breach', '$2.5K-$7.5K/record', 'Class action lawsuits']
        ]
        
        compliance_table = Table(compliance_data, colWidths=[1.2*inch, 1.3*inch, 1.8*inch, 2*inch])
        compliance_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ea580c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        
        elements.append(Paragraph("<b>4. Compliance & Legal Impact</b>", self.styles['Heading3']))
        elements.append(compliance_table)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_comprehensive_ai_prompts(self):
        """7 SQL injection specific AI prompts"""
        elements = []
        
        elements.append(Paragraph("🤖 AI PROMPTS FOR AUTOMATED FIXES", self.styles['SectionHeader']))
        elements.append(Paragraph(
            "Copy these prompts into ChatGPT, Claude, Amazon Q, or GitHub Copilot:",
            self.styles['BodyText']
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        prompts = [
            {
                'title': 'Prompt 1: Convert to Prepared Statements',
                'text': 'Review my code and convert all SQL queries to use prepared statements/parameterized queries. Find all instances of string concatenation in SQL (e.g., "SELECT * FROM users WHERE id = " + user_input) and replace with parameterized queries. Show before/after code for my framework (Python/Node.js/PHP/Java).'
            },
            {
                'title': 'Prompt 2: Add Input Validation Layer',
                'text': 'Create a comprehensive input validation layer for my application. Add validation for: SQL special characters (\', ", ;, --, /*), data type validation (integers, emails, UUIDs), length limits, whitelist patterns. Implement middleware/decorator pattern for reusable validation.'
            },
            {
                'title': 'Prompt 3: Implement ORM Migration',
                'text': 'Help me migrate from raw SQL queries to ORM (SQLAlchemy/Sequelize/Eloquent/Hibernate). Analyze my current database queries and provide equivalent ORM code. Include: model definitions, relationships, query builders, migrations. Show step-by-step migration plan.'
            },
            {
                'title': 'Prompt 4: Add Database Access Layer',
                'text': 'Create a secure database access layer (DAL) that wraps all database operations. Implement: query builder with automatic parameterization, connection pooling, query logging, error handling, transaction management. Prevent direct SQL execution from application code.'
            },
            {
                'title': 'Prompt 5: Security Audit & Fix',
                'text': 'Perform complete SQL injection security audit on my codebase. Check: all database queries, user input handling, stored procedures, dynamic SQL, error messages. Provide detailed report with: vulnerable code locations, severity ratings, fix recommendations, secure code examples.'
            },
            {
                'title': 'Prompt 6: Add WAF Rules',
                'text': 'Generate Web Application Firewall (WAF) rules to block SQL injection attacks. Create rules for: common SQL injection patterns, UNION attacks, blind SQL injection, time-based attacks. Provide configuration for AWS WAF, Cloudflare, ModSecurity.'
            },
            {
                'title': 'Prompt 7: Implement Monitoring',
                'text': 'Set up SQL injection attack monitoring and alerting. Implement: query logging, anomaly detection, failed query tracking, suspicious pattern alerts. Integrate with logging systems (ELK, Splunk, CloudWatch). Provide dashboard queries and alert rules.'
            }
        ]
        
        for prompt in prompts:
            elements.append(Paragraph(f"<b>{prompt['title']}</b>", self.styles['Heading3']))
            
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
    
    def _create_code_examples_multi_framework(self):
        """6 framework code examples"""
        elements = []
        
        elements.append(Paragraph("💻 SECURE CODE EXAMPLES (6 Frameworks)", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        examples = [
            {
                'framework': '1. Python (Flask + SQLAlchemy)',
                'vulnerable': '# ❌ VULNERABLE\\nuser_id = request.args.get(\"id\")\\nquery = f\"SELECT * FROM users WHERE id = {user_id}\"\\nresult = db.execute(query)',
                'secure': '# ✅ SECURE\\nfrom sqlalchemy import text\\nuser_id = request.args.get(\"id\")\\nquery = text(\"SELECT * FROM users WHERE id = :id\")\\nresult = db.execute(query, {\"id\": user_id})'
            },
            {
                'framework': '2. Node.js (Express + MySQL)',
                'vulnerable': '// ❌ VULNERABLE\\nconst id = req.query.id;\\nconst query = `SELECT * FROM users WHERE id = ${id}`;\\nconnection.query(query, callback);',
                'secure': '// ✅ SECURE\\nconst id = req.query.id;\\nconst query = \"SELECT * FROM users WHERE id = ?\";\\nconnection.query(query, [id], callback);'
            },
            {
                'framework': '3. Java (Spring Boot + JPA)',
                'vulnerable': '// ❌ VULNERABLE\\nString id = request.getParameter(\"id\");\\nString query = \"SELECT * FROM users WHERE id = \" + id;\\nQuery q = em.createNativeQuery(query);',
                'secure': '// ✅ SECURE\\nString id = request.getParameter(\"id\");\\nString query = \"SELECT * FROM users WHERE id = :id\";\\nQuery q = em.createQuery(query).setParameter(\"id\", id);'
            },
            {
                'framework': '4. PHP (Laravel Eloquent)',
                'vulnerable': '// ❌ VULNERABLE\\n$id = $_GET[\"id\"];\\n$users = DB::select(\"SELECT * FROM users WHERE id = $id\");',
                'secure': '// ✅ SECURE\\n$id = $_GET[\"id\"];\\n$users = DB::select(\"SELECT * FROM users WHERE id = ?\", [$id]);'
            },
            {
                'framework': '5. Go (database/sql)',
                'vulnerable': '// ❌ VULNERABLE\\nid := r.URL.Query().Get(\"id\")\\nquery := \"SELECT * FROM users WHERE id = \" + id\\nrows, _ := db.Query(query)',
                'secure': '// ✅ SECURE\\nid := r.URL.Query().Get(\"id\")\\nquery := \"SELECT * FROM users WHERE id = $1\"\\nrows, _ := db.Query(query, id)'
            },
            {
                'framework': '6. Ruby (Rails ActiveRecord)',
                'vulnerable': '# ❌ VULNERABLE\\nid = params[:id]\\nUser.where(\"id = #{id}\")',
                'secure': '# ✅ SECURE\\nid = params[:id]\\nUser.where(\"id = ?\", id)'
            }
        ]
        
        for example in examples:
            elements.append(Paragraph(f"<b>{example['framework']}</b>", self.styles['Heading3']))
            elements.append(Spacer(1, 0.1*inch))
            
            elements.append(Paragraph("<font color='red'><b>Vulnerable:</b></font>", self.styles['BodyText']))
            elements.append(Paragraph(
                f"<font face='Courier' size='7'>{example['vulnerable']}</font>",
                self.styles['BodyText']
            ))
            elements.append(Spacer(1, 0.1*inch))
            
            elements.append(Paragraph("<font color='green'><b>Secure:</b></font>", self.styles['BodyText']))
            elements.append(Paragraph(
                f"<font face='Courier' size='7'>{example['secure']}</font>",
                self.styles['BodyText']
            ))
            elements.append(Spacer(1, 0.25*inch))
        
        return elements

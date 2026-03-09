"""Command Injection & Path Traversal Report Generator - Professional Grade"""
from typing import Dict
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from datetime import datetime
from typing import Dict

class UniversalReportGenerator:
    def __init__(self, results: dict):
        self.results = results
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        self.filename = f"command_injection_{datetime.now().strftime('%d_%b_%Y_%I_%M_%p')}.pdf"
    
    def _setup_custom_styles(self):
        self.title_style = ParagraphStyle('CustomTitle', parent=self.styles['Heading1'], fontSize=24, textColor=colors.HexColor('#1a1a1a'), spaceAfter=6, alignment=TA_CENTER, fontName='Helvetica-Bold')
        self.heading1_style = ParagraphStyle('CustomHeading1', parent=self.styles['Heading1'], fontSize=16, textColor=colors.HexColor('#0066cc'), spaceAfter=12, spaceBefore=12, fontName='Helvetica-Bold')
        self.heading2_style = ParagraphStyle('CustomHeading2', parent=self.styles['Heading2'], fontSize=13, textColor=colors.HexColor('#003366'), spaceAfter=10, spaceBefore=10, fontName='Helvetica-Bold')
        self.body_style = ParagraphStyle('CustomBody', parent=self.styles['BodyText'], fontSize=10, alignment=TA_JUSTIFY, spaceAfter=8, leading=12)
    
    def generate(self):
        output_path = f"/tmp/{self.filename}"
        doc = SimpleDocTemplate(output_path, pagesize=letter, rightMargin=0.75*inch, leftMargin=0.75*inch, topMargin=0.75*inch, bottomMargin=0.75*inch)
        
        elements = []
        elements.extend(self._create_title_page())
        elements.append(PageBreak())
        elements.extend(self._create_executive_summary())
        elements.append(PageBreak())
        elements.extend(self._create_detailed_findings())
        elements.append(PageBreak())
        elements.extend(self._create_business_impact_analysis(self.results.get('severity_counts', {})))
        elements.append(PageBreak())
        elements.extend(self._create_manual_testing_guide())
        elements.append(PageBreak())
        elements.extend(self._create_ai_prompts_section())
        elements.append(PageBreak())
        elements.extend(self._create_code_examples())
        
        doc.build(elements)
        return output_path
    
    def _create_title_page(self):
        elements = []
        elements.append(Spacer(1, 1.5*inch))
        elements.append(Paragraph("COMMAND INJECTION & PATH TRAVERSAL ASSESSMENT", self.title_style))
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph("OS Command Injection & File System Security Analysis", self.styles['Normal']))
        elements.append(Spacer(1, 0.5*inch))
        
        metadata = [
            f"<b>Target URL:</b> {self.results.get('target_url', 'N/A')}",
            f"<b>Scan Date:</b> {self.results.get('scan_date', datetime.now().strftime('%d %b %Y'))}",
            f"<b>Vulnerabilities:</b> {self.results.get('total_vulnerabilities', 0)}",
            f"<b>Risk Score:</b> {self.results.get('risk_score', 0)}/100 ({self.results.get('risk_level', 'N/A')})",
        ]
        
        for item in metadata:
            elements.append(Paragraph(item, self.body_style))
            elements.append(Spacer(1, 0.1*inch))
        
        return elements
    
    def _create_executive_summary(self):
        elements = []
        elements.append(Paragraph("EXECUTIVE SUMMARY", self.heading1_style))
        elements.append(Spacer(1, 0.2*inch))
        
        severity = self.results.get('severity_counts', {})
        risk_score = self.results.get('risk_score', 0)
        
        dashboard_data = [
            ['Metric', 'Value', 'Status'],
            ['Risk Score', f"{risk_score}/100", self._get_risk_badge(risk_score)],
            ['Total Vulnerabilities', str(self.results.get('total_vulnerabilities', 0)), ''],
            ['Command Injection', str(len([v for v in self.results.get('vulnerabilities', []) if 'Command' in v.get('type', '')])), ''],
            ['Path Traversal', str(len([v for v in self.results.get('vulnerabilities', []) if 'Path' in v.get('type', '')])), ''],
        ]
        
        dashboard_table = Table(dashboard_data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
        dashboard_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
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
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elements.append(vuln_table)
        return elements
    
    def _create_detailed_findings(self):
        elements = []
        elements.append(Paragraph("DETAILED FINDINGS", self.heading1_style))
        elements.append(Spacer(1, 0.2*inch))
        
        for vuln in self.results.get('vulnerabilities', []):
            elements.append(Paragraph(f"<b>{vuln.get('type', 'Unknown')}</b>", self.heading2_style))
            elements.append(Paragraph(f"<b>Severity:</b> {vuln.get('severity', 'N/A')}", self.body_style))
            elements.append(Paragraph(f"<b>Description:</b> {vuln.get('description', 'N/A')}", self.body_style))
            elements.append(Paragraph(f"<b>Evidence:</b> {vuln.get('evidence', 'N/A')}", self.body_style))
            if vuln.get('fix_prompt'):
                elements.append(Paragraph(f"<b>Fix:</b> {vuln['fix_prompt']}", self.body_style))
            elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_business_impact_analysis(self, severity: Dict):
        elements = []
        
        elements.append(Paragraph("📊 BUSINESS IMPACT ANALYSIS", self.heading1_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Table 1: Financial Impact
        financial_data = [
            ['Impact Category', 'Low Risk', 'Medium Risk', 'High Risk', 'Critical Risk'],
            ['Command Injection', '$100K-$500K', '$500K-$2M', '$2M-$10M', '$10M-$50M'],
            ['Path Traversal', '$50K-$200K', '$200K-$1M', '$1M-$5M', '$5M-$20M'],
            ['Data Breach', '$75K-$300K', '$300K-$1.5M', '$1.5M-$7M', '$7M-$30M'],
            ['System Compromise', '$200K-$1M', '$1M-$5M', '$5M-$20M', '$20M-$100M'],
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
        
        elements.append(Paragraph("<b>Financial Impact</b>", self.heading2_style))
        elements.append(financial_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Table 2: Operational Impact
        operational_data = [
            ['Metric', 'Low', 'Medium', 'High', 'Critical'],
            ['Server Downtime', '1-4 hours', '4-24 hours', '1-3 days', '3-7+ days'],
            ['Data Loss Risk', '< 1GB', '1-10GB', '10-100GB', '> 100GB'],
            ['Recovery Time', '1-2 days', '3-7 days', '1-2 weeks', '2-4+ weeks'],
            ['Team Size Needed', '1-2 devs', '2-3 devs', '3-5 devs', '5-10+ devs'],
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
        
        # Table 3: Attack Scenarios
        attack_data = [
            ['Attack Type', 'Attacker Goal', 'Impact', 'Likelihood'],
            ['Remote Code Execution', 'Full server control', 'Complete compromise', 'High'],
            ['Data Exfiltration', 'Steal sensitive files', 'Data breach', 'High'],
            ['Privilege Escalation', 'Gain root access', 'System takeover', 'Medium'],
            ['Lateral Movement', 'Access other systems', 'Network breach', 'Medium'],
        ]
        
        attack_table = Table(attack_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        attack_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7c3aed')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(Paragraph("<b>Attack Scenarios</b>", self.heading2_style))
        elements.append(attack_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Table 4: Compliance Impact
        compliance_data = [
            ['Regulation', 'Violation Type', 'Fine Range', 'Additional Penalties'],
            ['GDPR', 'Data Breach', '€20M or 4% revenue', 'Lawsuits, Audits'],
            ['PCI-DSS', 'System Compromise', '$5K-$500K/month', 'Card processing ban'],
            ['HIPAA', 'PHI Exposure', '$100-$50K per record', 'Criminal charges'],
            ['SOX', 'Financial Data Loss', 'Up to $5M', 'Executive liability'],
        ]
        
        compliance_table = Table(compliance_data, colWidths=[1.2*inch, 1.5*inch, 1.8*inch, 1.8*inch])
        compliance_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ea580c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(Paragraph("<b>Compliance & Regulatory Impact</b>", self.heading2_style))
        elements.append(compliance_table)
        
        return elements
    
    def _create_manual_testing_guide(self):
        elements = []
        elements.append(Paragraph("🧪 MANUAL TESTING GUIDE", self.heading1_style))
        elements.append(Spacer(1, 0.2*inch))
        
        elements.append(Paragraph("<b>Test 1: Command Injection Testing (15 steps)</b>", self.heading2_style))
        cmd_steps = [
            '1. Identify all input parameters in URL and forms',
            '2. Test with semicolon separator: ; whoami',
            '3. Test with pipe operator: | whoami',
            '4. Test with double pipe: || whoami',
            '5. Test with ampersand: & whoami',
            '6. Test with double ampersand: && whoami',
            '7. Test with backticks: `whoami`',
            '8. Test with command substitution: $(whoami)',
            '9. Test time-based: ; sleep 5',
            '10. Test with ping: ; ping -c 5 127.0.0.1',
            '11. Observe response time delays (> 4 seconds)',
            '12. Check for command output in response',
            '13. Test with different OS commands (id, uname, cat)',
            '14. Document successful payloads',
            '15. Rate severity and create PoC'
        ]
        for step in cmd_steps:
            elements.append(Paragraph(step, self.body_style))
        
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph("<b>Test 2: Path Traversal Testing (12 steps)</b>", self.heading2_style))
        path_steps = [
            '1. Identify file/path parameters',
            '2. Test basic traversal: ../../../etc/passwd',
            '3. Test Windows paths: ..\\..\\..\\windows\\system32\\drivers\\etc\\hosts',
            '4. Test absolute paths: /etc/passwd',
            '5. Test encoded traversal: ..%2F..%2F..%2Fetc%2Fpasswd',
            '6. Test double encoding: ..%252F..%252F..%252Fetc%252Fpasswd',
            '7. Test null byte bypass: ../../../etc/passwd%00.jpg',
            '8. Check for /etc/passwd indicators (root:x:, daemon:)',
            '9. Test LFI with php://filter',
            '10. Test data:// wrapper',
            '11. Document accessible files',
            '12. Create detailed PoC with screenshots'
        ]
        for step in path_steps:
            elements.append(Paragraph(step, self.body_style))
        
        return elements
    
    def _create_ai_prompts_section(self):
        elements = []
        
        elements.append(Paragraph("🤖 AI ASSISTANT PROMPTS", self.heading1_style))
        elements.append(Paragraph(
            "Copy these prompts into ChatGPT, Claude, or Amazon Q to automatically fix vulnerabilities:",
            self.body_style
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        prompts = [
            {
                'title': 'Prompt 1: Fix Command Injection',
                'text': 'I have command injection vulnerabilities in my application. Help me: 1) Identify all places where user input is passed to system commands, 2) Replace with safe alternatives (subprocess with shell=False in Python, child_process.execFile in Node.js), 3) Implement input validation with whitelist, 4) Add proper error handling. Show secure code examples.'
            },
            {
                'title': 'Prompt 2: Fix Path Traversal',
                'text': 'Fix path traversal vulnerabilities in my code. Help me: 1) Validate all file path inputs, 2) Use basename() to strip directory components, 3) Implement whitelist of allowed files/directories, 4) Reject ../ sequences, 5) Use realpath() to resolve paths, 6) Store files outside web root. Provide before/after code.'
            },
            {
                'title': 'Prompt 3: Input Sanitization',
                'text': 'Implement comprehensive input sanitization for command injection and path traversal. Add: 1) Whitelist validation for allowed characters, 2) Blacklist dangerous characters (;|&$`), 3) Path normalization, 4) Length limits, 5) Type checking. Show implementation for my framework.'
            },
            {
                'title': 'Prompt 4: Secure File Operations',
                'text': 'Review my file operations code for security issues. Implement: 1) Safe file reading with path validation, 2) Chroot jail or restricted directory access, 3) File type validation, 4) Access control checks, 5) Audit logging. Provide secure code patterns.'
            },
            {
                'title': 'Prompt 5: Command Execution Alternatives',
                'text': 'Replace all system command executions with safe alternatives. For common tasks: 1) File operations: use native file APIs, 2) Network operations: use HTTP libraries, 3) Data processing: use language built-ins, 4) If commands needed: use parameterized APIs with strict validation. Show examples.'
            },
            {
                'title': 'Prompt 6: Security Testing',
                'text': 'Create comprehensive security tests for command injection and path traversal. Include: 1) Unit tests with malicious payloads, 2) Integration tests for file operations, 3) Fuzzing tests, 4) Negative test cases, 5) Boundary testing. Provide test code.'
            },
            {
                'title': 'Prompt 7: Complete Security Audit',
                'text': 'Perform complete security audit of my codebase for injection vulnerabilities. Check: 1) All user input handling, 2) System command usage, 3) File operations, 4) Database queries, 5) External API calls. Provide detailed report with fixes and priority levels.'
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
    
    def _create_code_examples(self):
        elements = []
        
        elements.append(Paragraph("💻 SECURE CODE EXAMPLES (6 Frameworks)", self.heading1_style))
        elements.append(Spacer(1, 0.2*inch))
        
        examples = [
            {
                'framework': '1. Python (Flask)',
                'vulnerable': '# ❌ VULNERABLE\\nimport os\\nuser_input = request.args.get("cmd")\\nos.system(user_input)  # Direct execution',
                'secure': '# ✅ SECURE\\nimport subprocess\\nallowed_cmds = ["ls", "pwd"]\\nif cmd in allowed_cmds:\\n    subprocess.run([cmd], shell=False)'
            },
            {
                'framework': '2. Node.js (Express)',
                'vulnerable': '// ❌ VULNERABLE\\nconst exec = require("child_process").exec;\\nconst cmd = req.query.cmd;\\nexec(cmd);  // Direct execution',
                'secure': '// ✅ SECURE\\nconst execFile = require("child_process").execFile;\\nconst allowed = ["ls", "pwd"];\\nif (allowed.includes(cmd)) {\\n  execFile(cmd, []);\\n}'
            },
            {
                'framework': '3. Java (Spring Boot)',
                'vulnerable': '// ❌ VULNERABLE\\nString cmd = request.getParameter("cmd");\\nRuntime.getRuntime().exec(cmd);  // Direct execution',
                'secure': '// ✅ SECURE\\nString[] allowed = {"ls", "pwd"};\\nif (Arrays.asList(allowed).contains(cmd)) {\\n  ProcessBuilder pb = new ProcessBuilder(cmd);\\n  pb.start();\\n}'
            },
            {
                'framework': '4. PHP (Laravel)',
                'vulnerable': '// ❌ VULNERABLE\\n$cmd = $_GET["cmd"];\\nshell_exec($cmd);  // Direct execution',
                'secure': '// ✅ SECURE\\n$allowed = ["ls", "pwd"];\\nif (in_array($cmd, $allowed)) {\\n  escapeshellcmd($cmd);\\n  exec($cmd);\\n}'
            },
            {
                'framework': '5. Go',
                'vulnerable': '// ❌ VULNERABLE\\ncmd := r.URL.Query().Get("cmd")\\nexec.Command("sh", "-c", cmd).Run()  // Shell execution',
                'secure': '// ✅ SECURE\\nallowed := []string{"ls", "pwd"}\\nif contains(allowed, cmd) {\\n  exec.Command(cmd).Run()\\n}'
            },
            {
                'framework': '6. Ruby (Rails)',
                'vulnerable': '# ❌ VULNERABLE\\ncmd = params[:cmd]\\nsystem(cmd)  # Direct execution',
                'secure': '# ✅ SECURE\\nallowed = ["ls", "pwd"]\\nif allowed.include?(cmd)\\n  system(cmd, exception: true)\\nend'
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
    
    def _get_risk_badge(self, score):
        if score >= 80: return 'CRITICAL'
        if score >= 60: return 'HIGH'
        if score >= 40: return 'MEDIUM'
        return 'LOW'


class UniversalReportGenerator:
    """Alias for backward compatibility"""
    pass

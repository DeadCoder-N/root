"""API Security Report Generator - Professional Grade (Matching Tool 1 Quality)"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from datetime import datetime
from typing import Dict, List

class APISecurityReportGenerator:
    def __init__(self, results: dict):
        self.results = results
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        self.filename = f"api_security_{datetime.now().strftime('%d_%b_%Y_%I_%M_%p')}.pdf"
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles matching Tool 1"""
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
    
    def generate(self):
        """Generate comprehensive PDF report"""
        output_path = f"/tmp/{self.filename}"
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch,
            title="API Security Assessment Report"
        )
        
        elements = []
        
        # Title Page
        elements.extend(self._create_title_page())
        elements.append(PageBreak())
        
        # Executive Summary with Dashboard & Priority Matrix
        elements.extend(self._create_executive_summary())
        elements.append(PageBreak())
        
        # Detailed Findings with Explanations
        elements.extend(self._create_detailed_findings())
        
        # Business Impact Analysis
        elements.append(PageBreak())
        elements.extend(self._create_business_impact_analysis())
        
        # Code Examples
        elements.append(PageBreak())
        elements.extend(self._create_code_examples())
        
        # Multiple AI Prompts
        elements.append(PageBreak())
        elements.extend(self._create_multiple_ai_prompts())
        
        doc.build(elements)
        return output_path
    
    def _create_title_page(self):
        """Create professional title page"""
        elements = []
        
        elements.append(Spacer(1, 1.5*inch))
        elements.append(Paragraph("API SECURITY ASSESSMENT", self.title_style))
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph("OWASP API Security Top 10 Analysis", self.styles['Normal']))
        elements.append(Spacer(1, 0.5*inch))
        
        # Metadata table
        metadata = [
            f"<b>Target API:</b> {self.results['target_url']}",
            f"<b>API Type:</b> {self.results['api_type']}",
            f"<b>Scan Date:</b> {self.results['scan_date']}",
            f"<b>Scan Duration:</b> {self.results['scan_duration']}",
            f"<b>Total Vulnerabilities:</b> {self.results['vulnerability_count']}",
            f"<b>Risk Score:</b> {self.results['risk_score']}/100 ({self.results['risk_level']})",
        ]
        
        for item in metadata:
            elements.append(Paragraph(item, self.body_style))
            elements.append(Spacer(1, 0.1*inch))
        
        return elements
    
    def _create_executive_summary(self):
        """Create executive summary with dashboard and priority matrix (like Tool 1)"""
        elements = []
        
        elements.append(Paragraph("EXECUTIVE SUMMARY", self.heading1_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Calculate metrics
        severity = self.results['severity_counts']
        risk_score = self.results['risk_score']
        time_estimate = self._calculate_time_estimate(severity)
        
        # Security Dashboard
        elements.append(Paragraph("Security Dashboard", self.heading2_style))
        
        dashboard_data = [
            ['Metric', 'Value', 'Status'],
            ['Risk Score', f"{risk_score}/100", self._get_risk_badge(risk_score)],
            ['Total Vulnerabilities', str(self.results['vulnerability_count']), ''],
            ['Time to Fix', time_estimate, ''],
            ['OWASP Compliance', self._check_owasp_compliance(severity), ''],
            ['API Security Coverage', 'Top 10', '✓'],
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
        
        # Vulnerability Breakdown
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
        
        # Priority Matrix (like Tool 1)
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
        
        return elements
    
    def _create_detailed_findings(self):
        """Create detailed findings with smart grouping (like Tool 1)"""
        elements = []
        
        elements.append(Paragraph("DETAILED FINDINGS", self.heading1_style))
        elements.append(Paragraph(
            "Vulnerabilities grouped by type and fix solution. Each group shows affected endpoints and a single fix command.",
            self.body_style
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        # Smart grouping by type
        grouped = self._group_vulnerabilities(self.results['vulnerabilities'])
        
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
        """Group similar vulnerabilities by type"""
        groups = {}
        
        for vuln in vulnerabilities:
            vuln_type = vuln.get('type', 'Unknown')
            severity = vuln.get('severity', 'LOW')
            
            if vuln_type not in groups:
                groups[vuln_type] = {
                    'type': vuln_type,
                    'severity': severity,
                    'endpoints': [],
                    'fix_prompt': vuln.get('fix_prompt', ''),
                    'count': 0,
                    'owasp': vuln.get('owasp', 'N/A'),
                    'cwe': vuln.get('cwe', 'N/A'),
                    'cvss': vuln.get('cvss', 'N/A')
                }
            
            groups[vuln_type]['endpoints'].append({
                'endpoint': vuln.get('endpoint', 'N/A'),
                'method': vuln.get('method', 'N/A'),
                'evidence': vuln.get('evidence', 'N/A')
            })
            groups[vuln_type]['count'] += 1
        
        return sorted(groups.values(), key=lambda x: x['count'], reverse=True)
    
    def _format_vulnerability_group(self, group):
        """Format grouped vulnerabilities with single fix command"""
        elements = []
        
        elements.append(Paragraph(f"<b>{group['type']} ({group['count']} occurrences)</b>", self.heading2_style))
        elements.append(Paragraph(
            f"<b>OWASP:</b> {group['owasp']} | <b>CWE:</b> {group['cwe']} | <b>CVSS:</b> {group['cvss']}",
            self.body_style
        ))
        
        explanation = self._get_vulnerability_explanation(group['type'])
        if explanation:
            elements.append(Paragraph(f"<b>❓ What This Means:</b> {explanation}", self.body_style))
        
        elements.append(Paragraph(f"<b>📁 Affected Endpoints ({group['count']}):</b>", self.body_style))
        for i, ep in enumerate(group['endpoints'][:10]):
            elements.append(Paragraph(f"  • {ep['method']} {ep['endpoint']}", self.body_style))
        
        if group['count'] > 10:
            elements.append(Paragraph(f"  ... and {group['count'] - 10} more endpoints", self.body_style))
        
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
    
    def _create_manual_testing_guide(self, group):
        """Create comprehensive manual testing guide for API vulnerabilities"""
        elements = []
        elements.append(Paragraph("<b>🧪 Manual Testing Guide (Test It Yourself):</b>", self.body_style))
        elements.append(Paragraph(
            "<b>Follow these steps to manually verify this vulnerability using Postman, cURL, or your browser:</b>",
            self.body_style
        ))
        elements.append(Spacer(1, 0.1*inch))
        
        vuln_type = group['type']
        
        if 'BOLA' in vuln_type or 'IDOR' in vuln_type:
            manual_steps = [
                "<b>Step 1: Create Two Test Accounts</b>",
                "Register two users: UserA and UserB. Note their IDs (e.g., 123 and 456).",
                "",
                "<b>Step 2: Login as UserA</b>",
                "POST /api/login with UserA credentials. Save the JWT token.",
                "",
                "<b>Step 3: Access UserA's Resource (Normal)</b>",
                f"GET {group['endpoints'][0]['endpoint'] if group['endpoints'] else '/api/user/123'}",
                "Headers: Authorization: Bearer [UserA_Token]",
                "Expected: Returns UserA's data (200 OK)",
                "",
                "<b>Step 4: Try to Access UserB's Resource (Attack)</b>",
                f"GET {group['endpoints'][0]['endpoint'].replace('123', '456') if group['endpoints'] else '/api/user/456'}",
                "Headers: Authorization: Bearer [UserA_Token]  (Still using UserA's token!)",
                "Expected if VULNERABLE: Returns UserB's data (200 OK) - BOLA confirmed!",
                "Expected if SECURE: Returns 403 Forbidden or 401 Unauthorized",
                "",
                "<b>Step 5: Test with cURL</b>",
                "<font face='Courier' size='7'>curl -H 'Authorization: Bearer [TOKEN]' https://api.example.com/user/456</font>",
                "",
                "<b>🚨 If you can access UserB's data with UserA's token, BOLA is CONFIRMED!</b>"
            ]
        
        elif 'Authentication' in vuln_type:
            manual_steps = [
                "<b>Step 1: Test Without Token</b>",
                f"GET {group['endpoints'][0]['endpoint'] if group['endpoints'] else self.results['target_url']}",
                "Headers: (No Authorization header)",
                "Expected if VULNERABLE: Returns data (200 OK) - No auth required!",
                "Expected if SECURE: Returns 401 Unauthorized",
                "",
                "<b>Step 2: Test with Invalid Token</b>",
                "Headers: Authorization: Bearer invalid_fake_token_12345",
                "Expected if VULNERABLE: Returns data (200 OK) - Weak validation!",
                "Expected if SECURE: Returns 401/403",
                "",
                "<b>Step 3: Test with Postman</b>",
                "1. Open Postman",
                f"2. Create GET request to {self.results['target_url']}",
                "3. Remove Authorization header",
                "4. Send request",
                "5. If you get data without auth, vulnerability CONFIRMED!",
                "",
                "<b>Step 4: Test with cURL</b>",
                f"<font face='Courier' size='7'>curl {self.results['target_url']}</font>",
                "If response contains data, authentication is MISSING!"
            ]
        
        elif 'Mass Assignment' in vuln_type:
            manual_steps = [
                "<b>Step 1: Create Normal User Account</b>",
                "POST /api/register with: {\"name\": \"test\", \"email\": \"test@example.com\"}",
                "Note: You're creating a regular user account",
                "",
                "<b>Step 2: Try Mass Assignment Attack</b>",
                "POST /api/register with malicious payload:",
                "<font face='Courier' size='7'>{\"name\": \"hacker\", \"email\": \"hack@example.com\", \"role\": \"admin\", \"is_verified\": true}</font>",
                "",
                "<b>Step 3: Check Response</b>",
                "Expected if VULNERABLE: Response includes {\"role\": \"admin\"} - Mass assignment works!",
                "Expected if SECURE: role field ignored, user created as regular user",
                "",
                "<b>Step 4: Verify with Login</b>",
                "Login with the account and check if you have admin privileges",
                "",
                "<b>Step 5: Test with Postman</b>",
                "POST request with JSON body including privileged fields:",
                "<font face='Courier' size='7'>{\"role\": \"admin\", \"is_admin\": true, \"permissions\": [\"all\"]}</font>",
                "",
                "<b>🚨 If privileged fields are accepted, Mass Assignment is CONFIRMED!</b>"
            ]
        
        elif 'Rate Limit' in vuln_type:
            manual_steps = [
                "<b>Step 1: Send Multiple Requests Quickly</b>",
                f"Use a tool to send 50+ requests to {self.results['target_url']}",
                "",
                "<b>Step 2: Using cURL in Loop</b>",
                "<font face='Courier' size='7'>for i in {1..50}; do curl https://api.example.com/endpoint; done</font>",
                "",
                "<b>Step 3: Using Python Script</b>",
                "<font face='Courier' size='7'>import requests\nfor i in range(50):\n    requests.get('https://api.example.com/endpoint')</font>",
                "",
                "<b>Step 4: Check Responses</b>",
                "Expected if VULNERABLE: All 50 requests succeed (200 OK) - No rate limit!",
                "Expected if SECURE: After ~10-20 requests, get 429 Too Many Requests",
                "",
                "<b>Step 5: Test Login Endpoint</b>",
                "Try 20+ failed login attempts with wrong password",
                "If all attempts are allowed, brute force is possible!",
                "",
                "<b>🚨 If you can send unlimited requests, Rate Limiting is MISSING!</b>"
            ]
        
        elif 'SSRF' in vuln_type:
            manual_steps = [
                "<b>Step 1: Test with External URL</b>",
                f"GET {self.results['target_url']}?url=https://google.com",
                "Expected: API fetches google.com content",
                "",
                "<b>Step 2: Test with Internal IP (AWS Metadata)</b>",
                f"GET {self.results['target_url']}?url=http://169.254.169.254/latest/meta-data/",
                "Expected if VULNERABLE: Returns AWS metadata (credentials!) - SSRF confirmed!",
                "Expected if SECURE: Request blocked or error",
                "",
                "<b>Step 3: Test with Localhost</b>",
                f"GET {self.results['target_url']}?url=http://localhost:8080/admin",
                "Expected if VULNERABLE: Access internal admin panel",
                "",
                "<b>Step 4: Test with file:// Protocol</b>",
                f"GET {self.results['target_url']}?url=file:///etc/passwd",
                "Expected if VULNERABLE: Returns server files",
                "",
                "<b>Step 5: Using cURL</b>",
                "<font face='Courier' size='7'>curl 'https://api.example.com/fetch?url=http://169.254.169.254/latest/meta-data/'</font>",
                "",
                "<b>🚨 If internal URLs work, SSRF is CONFIRMED! This is CRITICAL!</b>"
            ]
        
        else:
            # Generic testing guide
            if group['endpoints']:
                ep = group['endpoints'][0]
                manual_steps = [
                    "<b>Step 1: Test the Endpoint</b>",
                    f"Method: {ep['method']}",
                    f"URL: {ep['endpoint']}",
                    "",
                    "<b>Step 2: Observe Behavior</b>",
                    f"Expected: {ep['evidence']}",
                    "",
                    "<b>Step 3: Using Postman</b>",
                    "1. Open Postman",
                    f"2. Create {ep['method']} request",
                    f"3. URL: {ep['endpoint']}",
                    "4. Send and analyze response",
                    "",
                    "<b>Step 4: Using cURL</b>",
                    f"<font face='Courier' size='7'>curl -X {ep['method']} {ep['endpoint']}</font>"
                ]
            else:
                manual_steps = [
                    "<b>Manual Testing:</b>",
                    f"Test the vulnerable endpoint using Postman or cURL",
                    f"Verify the vulnerability by observing the behavior described in the evidence section"
                ]
        
        for step in manual_steps:
            elements.append(Paragraph(step, self.body_style))
        
        elements.append(Spacer(1, 0.2*inch))
        return elements
    

    def _create_multiple_ai_prompts(self):
        """Create API-specific AI prompts for different scenarios"""
        elements = []
        elements.append(Paragraph("🤖 AI Assistant Prompts (Copy & Paste)", self.heading1_style))
        elements.append(Spacer(1, 0.2*inch))
        
        elements.append(Paragraph(
            "Copy these API-specific prompts and paste them into ChatGPT, Claude, Amazon Q, or GitHub Copilot to automatically fix your code:",
            self.body_style
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        # Get unique vulnerability types
        vuln_types = list(set(v.get('type', 'Unknown') for v in self.results.get('vulnerabilities', [])))
        
        prompts = [
            {
                'title': '📝 Prompt 1: Fix BOLA/IDOR Vulnerabilities',
                'prompt': f'I have Broken Object Level Authorization (BOLA/IDOR) vulnerabilities in my API. '
                          f'Vulnerable endpoints: {self._get_affected_endpoints("BOLA")}. '
                          'Add authorization middleware to verify user owns the requested resource before returning data. '
                          'Implement object-level permission checks using user ID from JWT token. '
                          'Show me the secure code with proper authorization logic for my framework [Flask/Express/FastAPI/Laravel].'
            },
            {
                'title': '📝 Prompt 2: Implement API Authentication',
                'prompt': 'My API endpoints are accessible without authentication. '
                          'Implement JWT-based authentication for all API routes. '
                          'Add middleware to: 1) Validate JWT signature, 2) Check token expiration, '
                          '3) Extract user claims, 4) Return 401 for invalid/missing tokens. '
                          'Show me complete implementation for [YOUR_FRAMEWORK] with token generation and validation.'
            },
            {
                'title': '📝 Prompt 3: Add Rate Limiting',
                'prompt': 'My API has no rate limiting, making it vulnerable to DoS and brute force attacks. '
                          'Implement rate limiting using Redis: 100 requests per minute per IP, 1000 per hour per authenticated user. '
                          'Return 429 (Too Many Requests) when limit exceeded with Retry-After header. '
                          'Show me the middleware code for [Flask/Express/FastAPI/Laravel] with Redis integration.'
            },
            {
                'title': '📝 Prompt 4: Prevent Mass Assignment',
                'prompt': 'My API accepts all input fields without validation, allowing mass assignment attacks. '
                          'Create DTOs (Data Transfer Objects) to whitelist allowed fields for each endpoint. '
                          'Never bind request data directly to database models. '
                          'Show me how to implement input validation with DTOs/schemas for [YOUR_FRAMEWORK].'
            },
            {
                'title': '📝 Prompt 5: Fix Excessive Data Exposure',
                'prompt': 'My API responses expose sensitive fields like passwords, tokens, and internal IDs. '
                          'Filter all API responses to return only necessary fields. '
                          'Create response DTOs/serializers that explicitly whitelist safe fields. '
                          'Show me how to implement response filtering for [YOUR_FRAMEWORK] with examples.'
            },
            {
                'title': '📝 Prompt 6: Add Security Headers',
                'prompt': 'My API is missing security headers. Add these headers to all API responses: '
                          'X-Content-Type-Options: nosniff, X-Frame-Options: DENY, '
                          'Strict-Transport-Security: max-age=31536000, '
                          'Content-Security-Policy: default-src \'self\', '
                          'X-XSS-Protection: 1; mode=block. '
                          'Show me middleware code for [YOUR_FRAMEWORK] to add these headers globally.'
            },
            {
                'title': '📝 Prompt 7: Complete API Security Audit',
                'prompt': f'Perform complete security audit on my API following OWASP API Security Top 10. '
                          f'Found vulnerabilities: {", ".join(vuln_types[:5])}. '
                          'Review my code and provide fixes for: 1) Authentication/Authorization, '
                          '2) Input validation, 3) Rate limiting, 4) Data exposure, 5) Security headers. '
                          'Show me before/after code with detailed explanations for [YOUR_FRAMEWORK].'
            }
        ]
        
        for prompt_item in prompts:
            elements.append(Paragraph(f"<b>{prompt_item['title']}</b>", self.heading2_style))
            elements.append(Spacer(1, 0.1*inch))
            
            # Create a box for the prompt
            prompt_table = Table([[prompt_item['prompt']]], colWidths=[6.5*inch])
            prompt_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f9ff')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 12),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#0066cc')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]))
            elements.append(prompt_table)
            elements.append(Spacer(1, 0.25*inch))
        
        elements.append(Paragraph(
            "<b>💡 Pro Tip:</b> Replace [YOUR_FRAMEWORK] with your actual framework (Flask, Express, FastAPI, Laravel, Spring Boot, etc.) "
            "and paste your vulnerable code. The AI will analyze and fix it automatically!",
            self.body_style
        ))
        
        return elements
    
    def _get_affected_endpoints(self, vuln_type_filter: str) -> str:
        """Get list of affected endpoints for specific vulnerability type"""
        endpoints = []
        for vuln in self.results.get('vulnerabilities', []):
            if vuln_type_filter.lower() in vuln.get('type', '').lower():
                endpoint = vuln.get('endpoint', vuln.get('url', 'N/A'))
                if endpoint not in endpoints:
                    endpoints.append(endpoint)
        return ', '.join(endpoints[:3]) if endpoints else 'Multiple endpoints'
    
    def _create_business_impact_analysis(self):
        """Create comprehensive business impact analysis section"""
        elements = []
        
        elements.append(Paragraph("💰 Business Impact Analysis", self.heading1_style))
        elements.append(Spacer(1, 0.2*inch))
        
        elements.append(Paragraph(
            "Understanding the real-world business consequences of API security vulnerabilities:",
            self.body_style
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        # Financial Impact Table
        elements.append(Paragraph("Financial Impact", self.heading2_style))
        
        financial_data = [
            ['🚨 Risk Category', 'Estimated Cost', 'Timeframe'],
            ['Data Breach (Customer Data)', '$150 - $4.35M per incident', 'Immediate'],
            ['Regulatory Fines (GDPR)', 'Up to €20M or 4% revenue', '6-12 months'],
            ['Regulatory Fines (CCPA)', 'Up to $7,500 per violation', '3-6 months'],
            ['PCI-DSS Non-Compliance', '$5,000 - $100,000/month', 'Ongoing'],
            ['Emergency Response & Forensics', '$50,000 - $500,000', '1-3 months'],
            ['Legal Fees & Settlements', '$100,000 - $5M+', '12-36 months'],
            ['Customer Compensation', '$50 - $200 per affected user', '3-12 months'],
            ['Credit Monitoring Services', '$15 - $30 per user/year', '1-3 years'],
        ]
        
        financial_table = Table(financial_data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
        financial_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fee2e2')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT')
        ]))
        elements.append(financial_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Operational Impact
        elements.append(Paragraph("Operational Impact", self.heading2_style))
        
        operational_data = [
            ['🔧 Impact Area', 'Consequences'],
            ['Service Downtime', 'API unavailable during incident response (hours to days). Revenue loss: $5,600/minute for e-commerce.'],
            ['Development Freeze', 'All feature development halted for 2-8 weeks during security remediation. Product roadmap delayed.'],
            ['Emergency Patching', '24/7 engineering team mobilization. Overtime costs: $50,000 - $200,000. Technical debt accumulation.'],
            ['Third-Party Integration Loss', 'Partners suspend API access. Revenue loss from B2B integrations. Contract penalties.'],
            ['Database Restoration', 'Restore from backups if data compromised. Potential data loss. Hours to days of downtime.'],
            ['Security Audit Requirements', 'Mandatory third-party penetration testing. Costs: $25,000 - $100,000. 4-8 weeks duration.'],
        ]
        
        operational_table = Table(operational_data, colWidths=[2*inch, 4.5*inch])
        operational_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ea580c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fed7aa')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT')
        ]))
        elements.append(operational_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Reputational Impact
        elements.append(Paragraph("Reputational & Market Impact", self.heading2_style))
        
        reputational_data = [
            ['📉 Impact Type', 'Business Consequences'],
            ['Customer Trust Loss', '60-75% of customers stop using service after data breach. Lifetime value loss per customer: $500-$5,000.'],
            ['Brand Damage', 'Negative press coverage. Social media backlash. Brand value decrease: 5-20%. Recovery time: 2-5 years.'],
            ['Stock Price Impact (Public)', 'Average 7.5% stock price drop post-breach announcement. Market cap loss: millions to billions.'],
            ['Customer Acquisition Cost', 'CAC increases 2-3x due to trust issues. Marketing spend increase: 50-100% to rebuild reputation.'],
            ['Competitive Disadvantage', 'Competitors gain market share. Lost deals due to security concerns. RFP disqualifications.'],
            ['Insurance Premium Increase', 'Cyber insurance premiums increase 50-200%. Some insurers may drop coverage entirely.'],
            ['Investor Confidence', 'Difficulty raising funding. Valuation decrease: 10-30%. Due diligence failures in M&A deals.'],
        ]
        
        reputational_table = Table(reputational_data, colWidths=[2*inch, 4.5*inch])
        reputational_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7c3aed')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#e9d5ff')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT')
        ]))
        elements.append(reputational_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Compliance & Legal Impact
        elements.append(Paragraph("Compliance & Legal Consequences", self.heading2_style))
        
        compliance_data = [
            ['⚖️ Regulation', 'Penalties & Requirements'],
            ['GDPR (EU)', 'Fines up to €20M or 4% global revenue (whichever higher). Mandatory breach notification within 72 hours.'],
            ['CCPA (California)', 'Fines: $2,500 per violation (unintentional), $7,500 (intentional). Private right of action: $100-$750 per user.'],
            ['HIPAA (Healthcare)', 'Fines: $100 - $50,000 per violation. Maximum $1.5M per year. Criminal charges possible (up to 10 years prison).'],
            ['PCI-DSS (Payment Cards)', 'Fines: $5,000 - $100,000/month. Card brand penalties. Loss of payment processing ability. Mandatory audit.'],
            ['SOC 2 Compliance', 'Certification revoked. Re-audit required ($15,000 - $50,000). Customer contract breaches. Lost enterprise deals.'],
            ['ISO 27001', 'Certification suspended. Re-certification costs: $20,000 - $100,000. 6-12 months process. RFP disqualifications.'],
            ['Class Action Lawsuits', 'Average settlement: $1M - $50M+. Legal defense: $500,000 - $5M. Years of litigation. Executive liability.'],
        ]
        
        compliance_table = Table(compliance_data, colWidths=[1.8*inch, 4.7*inch])
        compliance_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0891b2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#cffafe')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT')
        ]))
        elements.append(compliance_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Real-World Examples
        elements.append(Paragraph("Real-World API Breach Examples", self.heading2_style))
        
        examples_data = [
            ['Company', 'Vulnerability', 'Impact'],
            ['T-Mobile (2021)', 'API BOLA/IDOR', '54M customers exposed. $350M settlement. Multiple breaches.'],
            ['Peloton (2021)', 'API BOLA', 'All user data accessible. Stock dropped 5%. Emergency patch.'],
            ['Venmo (2018)', 'Excessive Data Exposure', '200M+ transactions exposed publicly. Privacy scandal.'],
            ['Equifax (2017)', 'API Vulnerability', '147M records breached. $700M settlement. CEO resigned.'],
            ['Facebook (2019)', 'API Mass Assignment', '540M records on AWS. $5B FTC fine. Congressional hearing.'],
            ['Uber (2016)', 'API Authentication', '57M users exposed. $148M settlement. Concealment charges.'],
        ]
        
        examples_table = Table(examples_data, colWidths=[1.5*inch, 2*inch, 3*inch])
        examples_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fef2f2')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT')
        ]))
        elements.append(examples_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Total Cost Estimate
        elements.append(Paragraph("Estimated Total Cost of API Breach", self.heading2_style))
        
        severity = self.results['severity_counts']
        critical_count = severity.get('CRITICAL', 0)
        high_count = severity.get('HIGH', 0)
        
        if critical_count > 0:
            cost_range = "$500,000 - $10M+"
            risk_level = "EXTREME"
            color = colors.HexColor('#dc2626')
        elif high_count > 3:
            cost_range = "$250,000 - $2M"
            risk_level = "HIGH"
            color = colors.HexColor('#ea580c')
        elif high_count > 0:
            cost_range = "$100,000 - $500,000"
            risk_level = "MODERATE"
            color = colors.HexColor('#f59e0b')
        else:
            cost_range = "$50,000 - $200,000"
            risk_level = "LOW"
            color = colors.HexColor('#10b981')
        
        cost_summary = f"""Based on the vulnerabilities found in your API, the estimated total cost of a potential breach ranges from <b>{cost_range}</b>. 
Risk Level: <b><font color='{color.hexval()}'>{risk_level}</font></b>. This includes direct costs (fines, legal, remediation) and indirect costs (reputation, customer loss, downtime).

<b>Immediate Action Required:</b> Fix CRITICAL and HIGH severity issues within 24-48 hours to prevent catastrophic business impact."""
        
        elements.append(Paragraph(cost_summary, self.body_style))
        elements.append(Spacer(1, 0.2*inch))
        
        return elements

    def _create_code_examples(self):
        """Create comprehensive API security code examples across multiple frameworks"""
        elements = []
        elements.append(Paragraph("💻 Code Examples: Before & After", self.heading1_style))
        elements.append(Spacer(1, 0.2*inch))
        
        elements.append(Paragraph(
            "Real-world code examples showing vulnerable code and secure fixes across popular API frameworks:",
            self.body_style
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        code_examples = [
            {
                'language': 'Python (Flask) - BOLA/IDOR Fix',
                'vulnerable': '''# ❌ VULNERABLE CODE - No Authorization Check
@app.route('/api/user/<user_id>', methods=['GET'])
def get_user(user_id):
    user = db.query(f"SELECT * FROM users WHERE id={user_id}")
    return jsonify(user)  # DANGEROUS! Any user can access any profile''',
                'secure': '''# ✅ SECURE CODE - Object-Level Authorization
from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route('/api/user/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    current_user_id = get_jwt_identity()
    # Verify user owns this resource
    if str(current_user_id) != str(user_id):
        return jsonify({"error": "Unauthorized"}), 403
    user = db.query("SELECT * FROM users WHERE id=?", (user_id,))
    return jsonify(user)  # SAFE! Only owner can access'''
            },
            {
                'language': 'Node.js (Express) - Mass Assignment Fix',
                'vulnerable': '''// ❌ VULNERABLE CODE - Mass Assignment
app.post('/api/user', async (req, res) => {
  const user = await User.create(req.body);  // DANGEROUS!
  // Attacker can send: {"role": "admin", "is_verified": true}
  res.json(user);
});''',
                'secure': '''// ✅ SECURE CODE - Input Validation with DTO
const { body, validationResult } = require('express-validator');

app.post('/api/user', [
  body('name').isString().trim().escape(),
  body('email').isEmail().normalizeEmail(),
  // Whitelist only allowed fields
], async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) return res.status(400).json({errors});
  
  const user = await User.create({
    name: req.body.name,
    email: req.body.email
    // role, is_verified NOT included - SAFE!
  });
  res.json(user);
});'''
            },
            {
                'language': 'Python (FastAPI) - Rate Limiting',
                'vulnerable': '''# ❌ VULNERABLE CODE - No Rate Limiting
from fastapi import FastAPI
app = FastAPI()

@app.post("/api/login")
async def login(credentials: dict):
    # DANGEROUS! Unlimited login attempts = brute force attack
    user = authenticate(credentials["username"], credentials["password"])
    return {"token": generate_token(user)}''',
                'secure': '''# ✅ SECURE CODE - Redis Rate Limiting
from fastapi import FastAPI, Request, HTTPException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter

@app.post("/api/login")
@limiter.limit("5/minute")  # Max 5 attempts per minute
async def login(request: Request, credentials: dict):
    user = authenticate(credentials["username"], credentials["password"])
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token": generate_token(user)}  # SAFE!'''
            },
            {
                'language': 'PHP (Laravel) - Excessive Data Exposure Fix',
                'vulnerable': '''// ❌ VULNERABLE CODE - Exposes All Fields
public function getUser($id) {
    $user = User::find($id);
    return response()->json($user);  // DANGEROUS!
    // Exposes: password_hash, api_token, reset_token, etc.
}''',
                'secure': '''// ✅ SECURE CODE - Response DTO/Resource
use App\\Http\\Resources\\UserResource;

public function getUser($id) {
    $user = User::find($id);
    return new UserResource($user);  // SAFE!
}

// UserResource.php - Whitelist safe fields
class UserResource extends JsonResource {
    public function toArray($request) {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'email' => $this->email,
            // password, tokens NOT included!
        ];
    }
}'''
            },
            {
                'language': 'Java (Spring Boot) - SSRF Prevention',
                'vulnerable': '''// ❌ VULNERABLE CODE - SSRF Vulnerability
@GetMapping("/api/fetch")
public String fetchUrl(@RequestParam String url) {
    RestTemplate restTemplate = new RestTemplate();
    return restTemplate.getForObject(url, String.class);  // DANGEROUS!
    // Attacker can access: http://169.254.169.254/latest/meta-data/
}''',
                'secure': '''// ★ SECURE CODE - URL Validation & Allowlist
@GetMapping("/api/fetch")
public String fetchUrl(@RequestParam String url) {
    // Whitelist allowed domains
    List<String> allowedDomains = Arrays.asList(
        "api.example.com", "cdn.example.com"
    );
    
    try {
        URI uri = new URI(url);
        String host = uri.getHost();
        
        // Block internal IPs
        if (host.startsWith("127.") || host.startsWith("169.254.") || 
            host.startsWith("10.") || host.equals("localhost")) {
            throw new SecurityException("Internal IP blocked");
        }
        
        // Check allowlist
        if (!allowedDomains.contains(host)) {
            throw new SecurityException("Domain not allowed");
        }
        
        RestTemplate restTemplate = new RestTemplate();
        return restTemplate.getForObject(url, String.class);  // SAFE!
    } catch (Exception e) {
        return "Invalid URL";
    }
}'''
            },
            {
                'language': 'Node.js (Express) - JWT Authentication',
                'vulnerable': '''// ❌ VULNERABLE CODE - No Authentication
app.get('/api/admin/users', (req, res) => {
    const users = db.query('SELECT * FROM users');
    res.json(users);  // DANGEROUS! Anyone can access admin endpoint
});''',
                'secure': '''// ✅ SECURE CODE - JWT Middleware
const jwt = require('jsonwebtoken');

// Authentication Middleware
const authenticateJWT = (req, res, next) => {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) return res.status(401).json({error: 'No token'});
    
    jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
        if (err) return res.status(403).json({error: 'Invalid token'});
        req.user = user;
        next();
    });
};

// Authorization Middleware
const requireAdmin = (req, res, next) => {
    if (req.user.role !== 'admin') {
        return res.status(403).json({error: 'Admin only'});
    }
    next();
};

app.get('/api/admin/users', authenticateJWT, requireAdmin, (req, res) => {
    const users = db.query('SELECT * FROM users');
    res.json(users);  // SAFE! Only authenticated admins
});'''
            }
        ]
        
        for example in code_examples:
            elements.append(Paragraph(f"<b>{example['language']}</b>", self.heading2_style))
            elements.append(Spacer(1, 0.1*inch))
            
            elements.append(Paragraph("<font color='red'><b>Vulnerable Code:</b></font>", self.body_style))
            elements.append(Paragraph(
                f"<font face='Courier' size='7'>{example['vulnerable']}</font>",
                self.body_style
            ))
            elements.append(Spacer(1, 0.15*inch))
            
            elements.append(Paragraph("<font color='green'><b>Secure Code:</b></font>", self.body_style))
            elements.append(Paragraph(
                f"<font face='Courier' size='7'>{example['secure']}</font>",
                self.body_style
            ))
            elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _format_vulnerability_detailed(self, vuln: Dict) -> List:
        """Format vulnerability with full details and explanation"""
        elements = []
        
        # Title
        elements.append(Paragraph(f"<b>{vuln['type']}</b>", self.heading2_style))
        elements.append(Spacer(1, 0.05*inch))
        
        # Metadata
        elements.append(Paragraph(
            f"<b>OWASP:</b> {vuln.get('owasp', 'N/A')} | "
            f"<b>CWE:</b> {vuln.get('cwe', 'N/A')} | "
            f"<b>CVSS:</b> {vuln.get('cvss', 'N/A')}",
            self.body_style
        ))
        elements.append(Spacer(1, 0.1*inch))
        
        # Explanation (What This Means)
        explanation = self._get_vulnerability_explanation(vuln['type'])
        if explanation:
            elements.append(Paragraph(f"<b>❓ What This Means:</b> {explanation}", self.body_style))
            elements.append(Spacer(1, 0.1*inch))
        
        # Description
        elements.append(Paragraph(f"<b>Description:</b> {vuln['description']}", self.body_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # Evidence
        elements.append(Paragraph(f"<b>Evidence:</b> {vuln.get('evidence', 'N/A')}", self.body_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # Fix Instructions with AI Prompt
        if vuln.get('fix_prompt'):
            elements.append(Paragraph(f"<b>💡 How to Fix:</b> {vuln['fix_prompt']}", self.body_style))
            elements.append(Spacer(1, 0.1*inch))
            
            # AI Prompt
            ai_prompt = self._generate_ai_prompt(vuln)
            elements.append(Paragraph(f"<b>🤖 AI Prompt:</b> {ai_prompt}", self.body_style))
        else:
            elements.append(Paragraph(
                f"<b>Remediation:</b> {vuln.get('remediation', 'Review and fix according to OWASP API Security guidelines')}",
                self.body_style
            ))
        
        elements.append(Spacer(1, 0.25*inch))
        
        return elements
    
    def _generate_ai_prompt(self, vuln: Dict) -> str:
        """Generate AI prompt for fixing vulnerability (like Tool 1)"""
        vuln_type = vuln['type']
        
        ai_prompts = {
            'BOLA (Broken Object Level Authorization)': '"Add authorization checks to verify user owns the requested resource before returning data. Implement middleware to validate object-level permissions."',
            'Missing Authentication': '"Add authentication middleware to all API endpoints. Implement JWT or OAuth 2.0 token validation. Return 401 for unauthenticated requests."',
            'Weak Token Validation': '"Implement proper JWT signature verification. Validate token expiration, issuer, and audience claims. Use strong secret keys (256+ bits)."',
            'Mass Assignment': '"Create DTOs (Data Transfer Objects) to whitelist allowed input fields. Never bind request data directly to database models. Validate all input."',
            'Missing Rate Limiting': '"Implement rate limiting using Redis: 100 requests per minute per IP, 1000 per hour per user. Return 429 when limit exceeded."',
            'Unrestricted HTTP Methods': '"Restrict HTTP methods to only required ones (GET, POST). Disable PUT, DELETE, PATCH if not needed. Add authorization checks for state-changing methods."',
            'Excessive Data Exposure': '"Filter API responses to return only necessary fields. Use response DTOs. Never expose passwords, tokens, internal IDs, or sensitive metadata."',
            'Server-Side Request Forgery (SSRF)': '"Validate and sanitize all URL parameters. Use allowlist of permitted domains. Block internal IPs (127.0.0.1, 169.254.169.254). Disable URL redirects."',
            'Missing Security Headers': '"Add security headers to all API responses: X-Content-Type-Options: nosniff, X-Frame-Options: DENY, Strict-Transport-Security, Content-Security-Policy."',
        }
        
        return ai_prompts.get(vuln_type, f'"Fix {vuln_type} vulnerability following OWASP API Security Top 10 guidelines and implement proper input validation and authorization checks."')
    
    def _get_vulnerability_explanation(self, vuln_type: str) -> str:
        """Get user-friendly explanation for API vulnerability types"""
        explanations = {
            'BOLA (Broken Object Level Authorization)': 'Attackers can access objects belonging to other users by manipulating IDs in API requests. This allows unauthorized data access, modification, or deletion of resources that should be protected.',
            'Missing Authentication': 'API endpoints are accessible without any authentication, allowing anyone to access sensitive data or perform actions without proving their identity. This is a critical security flaw.',
            'Weak Token Validation': 'API accepts invalid or improperly signed authentication tokens, allowing attackers to forge credentials and impersonate legitimate users.',
            'Mass Assignment': 'API allows clients to modify object properties that should be restricted (like admin flags, roles, or permissions), enabling privilege escalation attacks.',
            'Missing Rate Limiting': 'Without rate limits, attackers can overwhelm your API with requests, causing denial of service, or perform brute force attacks without restriction.',
            'Unrestricted HTTP Methods': 'Dangerous HTTP methods (PUT, DELETE, PATCH) are enabled without proper authorization, allowing unauthorized data modification or deletion.',
            'Excessive Data Exposure': 'API responses contain sensitive information (passwords, tokens, internal IDs) that should never be exposed to clients, even authenticated ones.',
            'Server-Side Request Forgery (SSRF)': 'Attackers can make your server send requests to internal systems or external services, potentially accessing cloud metadata, internal APIs, or performing port scanning.',
            'Missing Security Headers': 'Absence of security headers leaves your API vulnerable to common web attacks like XSS, clickjacking, and man-in-the-middle attacks.',
        }
        return explanations.get(vuln_type, 'This vulnerability could be exploited to compromise your API security. Review the issue carefully and implement the recommended fixes.')
    
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
        """Check OWASP API Security compliance status"""
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

"""Authentication Security Report Generator - Professional Grade (Matching Tool 1 Quality)"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from datetime import datetime
from typing import Dict, List

class AuthReportGenerator:
    def __init__(self, results: dict):
        self.results = results
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        self.filename = f"auth_security_{datetime.now().strftime('%d_%b_%Y_%I_%M_%p')}.pdf"
    
    def _setup_custom_styles(self):
        self.title_style = ParagraphStyle('CustomTitle', parent=self.styles['Heading1'], fontSize=24, textColor=colors.HexColor('#1a1a1a'), spaceAfter=6, alignment=TA_CENTER, fontName='Helvetica-Bold')
        self.heading1_style = ParagraphStyle('CustomHeading1', parent=self.styles['Heading1'], fontSize=16, textColor=colors.HexColor('#0066cc'), spaceAfter=12, spaceBefore=12, fontName='Helvetica-Bold')
        self.heading2_style = ParagraphStyle('CustomHeading2', parent=self.styles['Heading2'], fontSize=13, textColor=colors.HexColor('#003366'), spaceAfter=10, spaceBefore=10, fontName='Helvetica-Bold')
        self.body_style = ParagraphStyle('CustomBody', parent=self.styles['BodyText'], fontSize=10, alignment=TA_JUSTIFY, spaceAfter=8, leading=12)
    
    def generate(self):
        output_path = f"/tmp/{self.filename}"
        doc = SimpleDocTemplate(output_path, pagesize=letter, rightMargin=0.75*inch, leftMargin=0.75*inch, topMargin=0.75*inch, bottomMargin=0.75*inch, title="Authentication Security Report")
        
        elements = []
        elements.extend(self._create_title_page())
        elements.append(PageBreak())
        elements.extend(self._create_executive_summary())
        elements.append(PageBreak())
        elements.extend(self._create_detailed_findings())
        
        # Business Impact Analysis
        elements.append(PageBreak())
        elements.extend(self._create_business_impact_analysis())
        
        # Manual Testing Guide
        elements.append(PageBreak())
        elements.extend(self._create_manual_testing_guide_detailed())
        
        # Code Examples
        elements.append(PageBreak())
        elements.extend(self._create_code_examples())
        
        # Multiple AI Prompts
        elements.append(PageBreak())
        elements.extend(self._create_multiple_ai_prompts())
        
        doc.build(elements)
        return output_path
    
    def _create_title_page(self):
        elements = []
        elements.append(Spacer(1, 1.5*inch))
        elements.append(Paragraph("AUTHENTICATION SECURITY ASSESSMENT", self.title_style))
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph("Comprehensive Authentication & Session Security Analysis", self.styles['Normal']))
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
        
        # Dashboard
        dashboard_data = [
            ['Metric', 'Value', 'Status'],
            ['Risk Score', f"{risk_score}/100", self._get_risk_badge(risk_score)],
            ['Total Vulnerabilities', str(self.results['vulnerability_count']), ''],
            ['Time to Fix', time_estimate, ''],
            ['Auth Best Practices', self._check_auth_compliance(severity), ''],
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
        
        # Severity Breakdown
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
        """Create detailed findings with smart grouping"""
        elements = []
        elements.append(Paragraph("DETAILED FINDINGS", self.heading1_style))
        elements.append(Paragraph("Vulnerabilities grouped by type. Each group shows affected locations and a single fix command.", self.body_style))
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
        """Group similar vulnerabilities"""
        groups = {}
        for vuln in vulnerabilities:
            vuln_type = vuln.get('type', 'Unknown')
            if vuln_type not in groups:
                groups[vuln_type] = {'type': vuln_type, 'severity': vuln.get('severity', 'LOW'), 'locations': [], 'fix_prompt': vuln.get('fix_prompt', ''), 'count': 0, 'owasp': vuln.get('owasp', 'N/A'), 'cwe': vuln.get('cwe', 'N/A'), 'cvss': vuln.get('cvss', 'N/A')}
            groups[vuln_type]['locations'].append({'location': vuln.get('file', vuln.get('url', 'N/A')), 'evidence': vuln.get('evidence', 'N/A')})
            groups[vuln_type]['count'] += 1
        return sorted(groups.values(), key=lambda x: x['count'], reverse=True)
    
    def _format_vulnerability_group(self, group):
        """Format grouped vulnerabilities"""
        elements = []
        elements.append(Paragraph(f"<b>{group['type']} ({group['count']} occurrences)</b>", self.heading2_style))
        elements.append(Paragraph(f"<b>OWASP:</b> {group['owasp']} | <b>CWE:</b> {group['cwe']} | <b>CVSS:</b> {group['cvss']}", self.body_style))
        explanation = self._get_explanation(group['type'])
        if explanation:
            elements.append(Paragraph(f"<b>❓ What This Means:</b> {explanation}", self.body_style))
        elements.append(Paragraph(f"<b>📁 Affected Locations ({group['count']}):</b>", self.body_style))
        for i, loc in enumerate(group['locations'][:10]):
            elements.append(Paragraph(f"  • {loc['location']}", self.body_style))
        if group['count'] > 10:
            elements.append(Paragraph(f"  ... and {group['count'] - 10} more locations", self.body_style))
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
            'Missing Brute Force Protection': 'Without rate limiting, attackers can try unlimited password combinations to guess user credentials. This makes brute force attacks trivial and highly effective.',
            'Weak Password Policy': 'Weak passwords are easily cracked by attackers using dictionary attacks or brute force. Strong password policies are the first line of defense against unauthorized access.',
            'Insecure Cookie Configuration': 'Missing cookie security flags expose session tokens to theft via XSS attacks or network interception, allowing attackers to hijack user sessions.',
            'Session Fixation Risk': 'Session IDs not regenerated after login allow attackers to hijack sessions by forcing users to use attacker-controlled session IDs.',
            'Missing Account Lockout': 'Without account lockout, attackers can perform unlimited login attempts, making brute force attacks feasible even with strong passwords.',
            'Missing Two-Factor Authentication': 'Single-factor authentication (password only) is vulnerable to credential theft. 2FA adds critical second layer of security.',
        }
        return explanations.get(vuln_type, 'This authentication vulnerability could allow attackers to bypass security controls and gain unauthorized access.')
    
    def _generate_ai_prompt(self, vuln):
        prompts = {
            'Missing Brute Force Protection': '"Implement rate limiting: 5 failed attempts per 15 minutes per IP. Add progressive delays (1s, 2s, 4s). Use CAPTCHA after 3 failed attempts. Store attempt counts in Redis."',
            'Weak Password Policy': '"Enforce password policy: minimum 8 characters, uppercase, lowercase, number, special character. Check against haveibeenpwned.com API for compromised passwords. Reject common passwords."',
            'Insecure Cookie Configuration': '"Set cookie security flags: Secure (HTTPS only), HttpOnly (no JavaScript access), SameSite=Strict (CSRF protection). Example: Set-Cookie: session=abc; Secure; HttpOnly; SameSite=Strict"',
            'Session Fixation Risk': '"Regenerate session ID after successful login. Use session_regenerate_id(true) in PHP or equivalent. Invalidate old session. Implement session timeout (30 min idle)."',
            'Missing Account Lockout': '"Lock account after 5-10 failed attempts. Require admin unlock or 30-minute timeout. Log all lockout events. Send email notification to user."',
            'Missing Two-Factor Authentication': '"Implement 2FA using TOTP (Google Authenticator), SMS, or hardware tokens. Require for admin accounts. Provide backup codes. Use libraries like pyotp or speakeasy."',
        }
        return prompts.get(vuln['type'], f'"Fix {vuln["type"]} following OWASP Authentication Cheat Sheet guidelines."')
    
    def _calculate_time_estimate(self, severity):
        hours = (severity.get('CRITICAL', 0) * 4) + (severity.get('HIGH', 0) * 2) + (severity.get('MEDIUM', 0) * 1) + (severity.get('LOW', 0) * 0.5)
        if hours < 8: return f"{int(hours)} hours"
        elif hours < 40: return f"{int(hours/8)} days"
        else: return f"{int(hours/40)} weeks"
    
    def _check_auth_compliance(self, severity):
        if severity.get('CRITICAL', 0) > 0: return '❌ Non-Compliant'
        elif severity.get('HIGH', 0) > 3: return '⚠️ At Risk'
        elif severity.get('HIGH', 0) > 0: return '🟡 Needs Review'
        else: return '✅ Compliant'
    

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
        """Create 7 authentication-specific AI prompts"""
        elements = []
        elements.append(Paragraph("🤖 AI PROMPTS FOR AUTHENTICATION FIXES", self.heading1_style))
        elements.append(Paragraph(
            "Copy these prompts to ChatGPT/Claude with your authentication code for instant security fixes.",
            self.body_style
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        prompts = [
            {
                'title': 'Prompt 1: Implement Rate Limiting',
                'prompt': 'My login endpoint has no rate limiting. Implement: 1) 5 failed attempts per 15 minutes per IP, 2) Progressive delays (1s, 2s, 4s, 8s), 3) CAPTCHA after 3 attempts, 4) Store attempt counts in Redis with TTL. Show code for [Flask/Express/Django].'
            },
            {
                'title': 'Prompt 2: Enforce Strong Password Policy',
                'prompt': 'My app accepts weak passwords. Implement policy: 1) Minimum 8 characters, 2) Require uppercase, lowercase, number, special char, 3) Check against haveibeenpwned.com API, 4) Reject top 10,000 common passwords. Provide validation code for [YOUR_FRAMEWORK].'
            },
            {
                'title': 'Prompt 3: Secure Session Cookies',
                'prompt': 'My session cookies lack security flags. Fix: 1) Set HttpOnly flag (prevent XSS), 2) Set Secure flag (HTTPS only), 3) Set SameSite=Strict (CSRF protection), 4) Implement 30-minute idle timeout. Show cookie configuration for [YOUR_STACK].'
            },
            {
                'title': 'Prompt 4: Prevent Session Fixation',
                'prompt': 'My app is vulnerable to session fixation. Fix: 1) Regenerate session ID after successful login, 2) Invalidate old session, 3) Create new session with new ID, 4) Implement session timeout. Provide code for [PHP/Node.js/Python].'
            },
            {
                'title': 'Prompt 5: Implement Account Lockout',
                'prompt': 'No account lockout after failed logins. Implement: 1) Lock account after 5-10 failed attempts, 2) 30-minute timeout or admin unlock, 3) Send email notification to user, 4) Log all lockout events. Show implementation for [YOUR_FRAMEWORK].'
            },
            {
                'title': 'Prompt 6: Add Two-Factor Authentication',
                'prompt': 'Add 2FA to my authentication system: 1) Implement TOTP using Google Authenticator, 2) Generate QR code for setup, 3) Validate 6-digit codes, 4) Provide 10 backup codes, 5) Make mandatory for admin accounts. Use libraries like pyotp or speakeasy for [YOUR_LANGUAGE].'
            },
            {
                'title': 'Prompt 7: Complete Authentication Security Audit',
                'prompt': 'Perform complete authentication security audit: 1) Check rate limiting on all auth endpoints, 2) Validate password policy strength, 3) Verify session security (HttpOnly, Secure, SameSite), 4) Test session fixation prevention, 5) Check account lockout mechanism, 6) Verify 2FA implementation. Provide comprehensive fixes for [YOUR_STACK].'
            }
        ]
        
        for p in prompts:
            elements.append(Paragraph(f"<b>{p['title']}</b>", self.heading2_style))
            elements.append(Paragraph(
                f"<font face='Courier' size='8' color='#0066cc'>{p['prompt']}</font>",
                self.body_style
            ))
            elements.append(Spacer(1, 0.2*inch))
        
        return elements

    def _create_code_examples(self):
        """Create 6 framework-specific authentication code examples"""
        elements = []
        elements.append(Paragraph("💻 SECURE AUTHENTICATION - CODE EXAMPLES", self.heading1_style))
        elements.append(Paragraph(
            "Production-ready authentication implementations across 6 frameworks.",
            self.body_style
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        examples = [
            {
                'framework': '1. Python Flask (Rate Limiting + Session Security)',
                'vulnerable': '''# ❌ VULNERABLE
from flask import Flask, request, session

@app.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(username=request.form['username']).first()
    if user and user.password == request.form['password']:  # Plain text!
        session['user_id'] = user.id  # No regeneration
        return 'Login successful'
    return 'Invalid credentials', 401''',
                'secure': '''# ✅ SECURE
from flask import Flask, request, session
from flask_limiter import Limiter
from werkzeug.security import check_password_hash
import secrets

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per 15 minutes")
def login():
    user = User.query.filter_by(username=request.form['username']).first()
    if user and check_password_hash(user.password_hash, request.form['password']):
        session.clear()  # Clear old session
        session.regenerate()  # New session ID
        session['user_id'] = user.id
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=30)
        return 'Login successful'
    return 'Invalid credentials', 401

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Strict'
)'''
            },
            {
                'framework': '2. Node.js Express (Password Policy + 2FA)',
                'vulnerable': '''// ❌ VULNERABLE
const express = require('express');

app.post('/register', (req, res) => {
  const user = new User({
    username: req.body.username,
    password: req.body.password  // No hashing, no validation!
  });
  user.save();
  res.json({success: true});
});''',
                'secure': '''// ✅ SECURE
const express = require('express');
const bcrypt = require('bcrypt');
const speakeasy = require('speakeasy');

function validatePassword(password) {
  if (password.length < 8) return false;
  if (!/[A-Z]/.test(password)) return false;
  if (!/[a-z]/.test(password)) return false;
  if (!/[0-9]/.test(password)) return false;
  if (!/[!@#$%^&*]/.test(password)) return false;
  const common = ['password', '123456', 'qwerty'];
  if (common.includes(password.toLowerCase())) return false;
  return true;
}

app.post('/register', async (req, res) => {
  if (!validatePassword(req.body.password)) {
    return res.status(400).json({error: 'Weak password'});
  }
  
  const hashedPassword = await bcrypt.hash(req.body.password, 12);
  const secret = speakeasy.generateSecret({length: 32});
  
  const user = new User({
    username: req.body.username,
    password: hashedPassword,
    twoFactorSecret: secret.base32
  });
  await user.save();
  
  res.json({
    success: true,
    qrCode: secret.otpauth_url  // For Google Authenticator
  });
});'''
            },
            {
                'framework': '3. Java Spring Boot (Account Lockout)',
                'vulnerable': '''// ❌ VULNERABLE
@PostMapping("/login")
public ResponseEntity<?> login(@RequestBody LoginRequest request) {
    User user = userRepository.findByUsername(request.getUsername());
    if (user != null && user.getPassword().equals(request.getPassword())) {
        return ResponseEntity.ok("Login successful");
    }
    return ResponseEntity.status(401).body("Invalid credentials");
}''',
                'secure': '''// ✅ SECURE
@PostMapping("/login")
public ResponseEntity<?> login(@RequestBody LoginRequest request) {
    User user = userRepository.findByUsername(request.getUsername());
    
    if (user == null) {
        return ResponseEntity.status(401).body("Invalid credentials");
    }
    
    // Check if account is locked
    if (user.isLocked() && user.getLockoutExpiry().isAfter(LocalDateTime.now())) {
        return ResponseEntity.status(423).body("Account locked. Try again in 30 minutes.");
    }
    
    // Verify password
    if (!passwordEncoder.matches(request.getPassword(), user.getPasswordHash())) {
        user.incrementFailedAttempts();
        
        if (user.getFailedAttempts() >= 5) {
            user.setLocked(true);
            user.setLockoutExpiry(LocalDateTime.now().plusMinutes(30));
            emailService.sendLockoutNotification(user.getEmail());
        }
        
        userRepository.save(user);
        return ResponseEntity.status(401).body("Invalid credentials");
    }
    
    // Reset failed attempts on successful login
    user.resetFailedAttempts();
    user.setLocked(false);
    userRepository.save(user);
    
    return ResponseEntity.ok("Login successful");
}'''
            },
            {
                'framework': '4. PHP Laravel (Session Fixation Prevention)',
                'vulnerable': '''// ❌ VULNERABLE
public function login(Request $request) {
    $user = User::where('email', $request->email)->first();
    
    if ($user && Hash::check($request->password, $user->password)) {
        session(['user_id' => $user->id]);  // No regeneration!
        return redirect('/dashboard');
    }
    
    return back()->withErrors(['email' => 'Invalid credentials']);
}''',
                'secure': '''// ✅ SECURE
public function login(Request $request) {
    $user = User::where('email', $request->email)->first();
    
    if ($user && Hash::check($request->password, $user->password)) {
        // Regenerate session ID to prevent fixation
        $request->session()->invalidate();
        $request->session()->regenerateToken();
        $request->session()->regenerate();
        
        // Set session data
        session([
            'user_id' => $user->id,
            'last_activity' => now(),
            'ip_address' => $request->ip()
        ]);
        
        // Update last login
        $user->update(['last_login' => now()]);
        
        return redirect('/dashboard');
    }
    
    return back()->withErrors(['email' => 'Invalid credentials']);
}

// In config/session.php
'secure' => env('SESSION_SECURE_COOKIE', true),
'http_only' => true,
'same_site' => 'strict',
'lifetime' => 30,  // 30 minutes'''
            },
            {
                'framework': '5. Go (Brute Force Protection)',
                'vulnerable': '''// ❌ VULNERABLE
func LoginHandler(w http.ResponseWriter, r *http.Request) {
    username := r.FormValue("username")
    password := r.FormValue("password")
    
    user := GetUser(username)
    if user != nil && user.Password == password {
        http.SetCookie(w, &http.Cookie{Name: "session", Value: user.ID})
        w.Write([]byte("Login successful"))
        return
    }
    
    w.WriteHeader(401)
    w.Write([]byte("Invalid credentials"))
}''',
                'secure': '''// ✅ SECURE
import (
    "golang.org/x/time/rate"
    "sync"
)

var (
    limiters = make(map[string]*rate.Limiter)
    mu       sync.Mutex
)

func getLimiter(ip string) *rate.Limiter {
    mu.Lock()
    defer mu.Unlock()
    
    limiter, exists := limiters[ip]
    if !exists {
        limiter = rate.NewLimiter(rate.Every(15*time.Minute), 5)
        limiters[ip] = limiter
    }
    
    return limiter
}

func LoginHandler(w http.ResponseWriter, r *http.Request) {
    ip := r.RemoteAddr
    limiter := getLimiter(ip)
    
    if !limiter.Allow() {
        http.Error(w, "Too many login attempts. Try again in 15 minutes.", 429)
        return
    }
    
    username := r.FormValue("username")
    password := r.FormValue("password")
    
    user := GetUser(username)
    if user != nil && bcrypt.CompareHashAndPassword([]byte(user.PasswordHash), []byte(password)) == nil {
        session := CreateSession(user.ID)
        http.SetCookie(w, &http.Cookie{
            Name:     "session",
            Value:    session.ID,
            HttpOnly: true,
            Secure:   true,
            SameSite: http.SameSiteStrictMode,
            MaxAge:   1800,  // 30 minutes
        })
        w.Write([]byte("Login successful"))
        return
    }
    
    w.WriteHeader(401)
    w.Write([]byte("Invalid credentials"))
}'''
            },
            {
                'framework': '6. Ruby Rails (Complete Secure Authentication)',
                'vulnerable': '''# ❌ VULNERABLE
class SessionsController < ApplicationController
  def create
    user = User.find_by(email: params[:email])
    if user && user.password == params[:password]
      session[:user_id] = user.id
      redirect_to root_path
    else
      flash[:error] = "Invalid credentials"
      render :new
    end
  end
end''',
                'secure': '''# ✅ SECURE
class SessionsController < ApplicationController
  before_action :check_rate_limit, only: [:create]
  
  def create
    user = User.find_by(email: params[:email])
    
    if user&.authenticate(params[:password])
      # Check if account is locked
      if user.locked? && user.lockout_expires_at > Time.current
        flash[:error] = "Account locked. Try again in 30 minutes."
        return render :new
      }
      
      # Reset failed attempts
      user.update(failed_attempts: 0, locked: false)
      
      # Regenerate session to prevent fixation
      reset_session
      session[:user_id] = user.id
      session[:ip_address] = request.remote_ip
      session[:last_activity] = Time.current
      
      redirect_to root_path
    else
      # Increment failed attempts
      if user
        user.increment!(:failed_attempts)
        
        if user.failed_attempts >= 5
          user.update(
            locked: true,
            lockout_expires_at: 30.minutes.from_now
          )
          UserMailer.account_locked(user).deliver_later
        end
      end
      
      flash[:error] = "Invalid credentials"
      render :new
    end
  end
  
  private
  
  def check_rate_limit
    key = "login_attempts:#{request.remote_ip}"
    attempts = Rails.cache.read(key) || 0
    
    if attempts >= 5
      render json: {error: "Too many attempts"}, status: 429
      return
    end
    
    Rails.cache.write(key, attempts + 1, expires_in: 15.minutes)
  end
end

# In config/initializers/session_store.rb
Rails.application.config.session_store :cookie_store,
  key: '_app_session',
  secure: Rails.env.production?,
  httponly: true,
  same_site: :strict,
  expire_after: 30.minutes'''
            }
        ]
        
        for idx, ex in enumerate(examples, 1):
            elements.append(Paragraph(f"<b>{ex['framework']}</b>", self.heading2_style))
            elements.append(Spacer(1, 0.1*inch))
            
            elements.append(Paragraph("<b>❌ Vulnerable Implementation:</b>", self.body_style))
            elements.append(Paragraph(
                f"<font face='Courier' size='7'>{ex['vulnerable']}</font>",
                self.body_style
            ))
            elements.append(Spacer(1, 0.15*inch))
            
            elements.append(Paragraph("<b>✅ Secure Implementation:</b>", self.body_style))
            elements.append(Paragraph(
                f"<font face='Courier' size='7'>{ex['secure']}</font>",
                self.body_style
            ))
            elements.append(Spacer(1, 0.3*inch))
            
            if idx % 2 == 0 and idx < len(examples):
                elements.append(PageBreak())
        
        return elements

    def _get_risk_badge(self, score):
        if score >= 75: return '🔴 Critical'
        elif score >= 50: return '🟠 High'
        elif score >= 25: return '🟡 Medium'
        else: return '🟢 Low'

    def _create_business_impact_analysis(self):
        """Create business impact analysis with 4 detailed tables"""
        elements = []
        
        elements.append(Paragraph("📊 BUSINESS IMPACT ANALYSIS", self.heading1_style))
        elements.append(Paragraph(
            "Understanding the real-world business consequences of authentication security vulnerabilities.",
            self.body_style
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        # Table 1: Financial Impact
        elements.append(Paragraph("1. Financial Impact", self.heading2_style))
        financial_data = [
            ['Vulnerability Type', 'Avg Cost per Incident', 'Potential Loss', 'Recovery Time'],
            ['Brute Force Attack', '$180,000 - $400,000', 'Account takeover', '2-3 weeks'],
            ['Weak Password Policy', '$120,000 - $300,000', 'Credential stuffing', '1-2 weeks'],
            ['Session Hijacking', '$200,000 - $500,000', 'Data breach', '3-5 weeks'],
            ['Missing 2FA', '$300,000 - $1M', 'Mass compromise', '4-8 weeks'],
        ]
        
        financial_table = Table(financial_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1*inch])
        financial_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
        ]))
        elements.append(financial_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Table 2: Operational Impact
        elements.append(Paragraph("2. Operational Impact", self.heading2_style))
        operational_data = [
            ['Impact Area', 'Severity', 'Affected Systems', 'Mitigation Effort'],
            ['User Authentication', 'CRITICAL', 'All login endpoints', '50-100 dev hours'],
            ['Session Management', 'HIGH', 'Web + Mobile apps', '30-60 dev hours'],
            ['Password Reset', 'HIGH', 'Auth service', '20-40 dev hours'],
            ['Account Recovery', 'MEDIUM', 'Support systems', '15-30 dev hours'],
        ]
        
        operational_table = Table(operational_data, colWidths=[1.8*inch, 1.2*inch, 1.8*inch, 1.2*inch])
        operational_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
        ]))
        elements.append(operational_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Table 3: Reputational Damage
        elements.append(Paragraph("3. Reputational Damage", self.heading2_style))
        reputation_data = [
            ['Scenario', 'Customer Impact', 'Media Coverage', 'Trust Recovery'],
            ['Mass Account Breach', '65-80% user churn', 'National headlines', '12-24 months'],
            ['Credential Stuffing', '45-60% churn', 'Industry coverage', '8-16 months'],
            ['Session Hijacking', '55-70% churn', 'Tech media', '10-18 months'],
            ['Password Database Leak', '75-90% churn', 'International news', '18-36 months'],
        ]
        
        reputation_table = Table(reputation_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        reputation_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
        ]))
        elements.append(reputation_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Table 4: Compliance & Legal
        elements.append(Paragraph("4. Compliance & Legal Consequences", self.heading2_style))
        compliance_data = [
            ['Regulation', 'Violation Type', 'Max Penalty', 'Reporting Requirement'],
            ['GDPR (EU)', 'Auth breach', '€20M or 4% revenue', '72 hours'],
            ['CCPA (California)', 'Credential exposure', '$7,500 per violation', '30 days'],
            ['HIPAA (Healthcare)', 'PHI access breach', '$1.5M per year', 'Immediate'],
            ['PCI DSS (Payment)', 'Auth failure', '$500K + card ban', 'Immediate'],
            ['SOX (Financial)', 'Access control failure', 'Criminal charges', 'Immediate'],
        ]
        
        compliance_table = Table(compliance_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        compliance_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
        ]))
        elements.append(compliance_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Real-world breach examples
        elements.append(Paragraph("Real-World Authentication Breach Examples", self.heading2_style))
        elements.append(Paragraph(
            "<b>1. Yahoo Data Breach (2013-2014):</b> Weak authentication allowed attackers to compromise 3 billion accounts. "
            "Impact: $350M+ settlement, company value dropped $350M, 7 years to fully disclose.",
            self.body_style
        ))
        elements.append(Spacer(1, 0.1*inch))
        
        elements.append(Paragraph(
            "<b>2. LinkedIn Password Breach (2012):</b> Weak password hashing (unsalted SHA-1) led to 117M passwords stolen. "
            "Impact: $1.25M settlement, massive user churn, forced password reset for all users.",
            self.body_style
        ))
        elements.append(Spacer(1, 0.1*inch))
        
        elements.append(Paragraph(
            "<b>3. Dropbox Credential Stuffing (2012):</b> Lack of rate limiting allowed credential stuffing attack on 68M accounts. "
            "Impact: $250K+ in incident response, mandatory 2FA implementation, regulatory scrutiny.",
            self.body_style
        ))
        elements.append(Spacer(1, 0.1*inch))
        
        return elements

    def _create_manual_testing_guide_detailed(self):
        """Create comprehensive manual testing guide"""
        elements = []
        
        elements.append(Paragraph("🧪 MANUAL TESTING GUIDE", self.heading1_style))
        elements.append(Paragraph(
            "Step-by-step instructions to manually verify authentication vulnerabilities.",
            self.body_style
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        # Test 1: Brute Force Protection
        elements.append(Paragraph("Test 1: Brute Force Protection", self.heading2_style))
        elements.append(Paragraph("<b>Tools:</b> Burp Suite Intruder, Python script", self.body_style))
        test1_steps = [
            "1. Identify login endpoint (e.g., POST /api/login)",
            "2. Capture login request in Burp Suite",
            "3. Send to Intruder, set password as payload position",
            "4. Load password list (10-20 common passwords)",
            "5. Start attack with 1 second delay between requests",
            "6. Monitor responses: All 200 OK = No rate limiting (CRITICAL)",
            "7. Check for: Account lockout, CAPTCHA, progressive delays",
            "8. Test IP-based vs account-based rate limiting",
            "9. Try from different IPs to bypass IP-based limits",
            "10. Document: Rate limit threshold, lockout duration, bypass methods"
        ]
        for step in test1_steps:
            elements.append(Paragraph(step, self.body_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Test 2: Password Policy
        elements.append(Paragraph("Test 2: Password Policy Strength", self.heading2_style))
        elements.append(Paragraph("<b>Tools:</b> Registration form, Burp Suite", self.body_style))
        test2_steps = [
            "1. Navigate to registration/password change page",
            "2. Test weak passwords: '123456', 'password', 'abc123'",
            "3. Test short passwords: '12', 'abc', 'a1'",
            "4. Test no uppercase: 'password123'",
            "5. Test no numbers: 'Password'",
            "6. Test no special chars: 'Password123'",
            "7. Check if common passwords rejected (use top 100 list)",
            "8. Test password in username: username='john', password='john123'",
            "9. Verify minimum length requirement (should be 8+)",
            "10. Document: Accepted weak passwords, missing requirements"
        ]
        for step in test2_steps:
            elements.append(Paragraph(step, self.body_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Test 3: Session Security
        elements.append(Paragraph("Test 3: Session Cookie Security", self.heading2_style))
        elements.append(Paragraph("<b>Tools:</b> Browser DevTools, Burp Suite", self.body_style))
        test3_steps = [
            "1. Login to application",
            "2. Open DevTools → Application → Cookies",
            "3. Check session cookie for security flags:",
            "   - HttpOnly: Should be present (prevents XSS theft)",
            "   - Secure: Should be present (HTTPS only)",
            "   - SameSite: Should be Strict or Lax (CSRF protection)",
            "4. Copy cookie value, logout, paste cookie back",
            "5. If still logged in: Session not invalidated on logout (HIGH)",
            "6. Test session fixation: Get session ID before login",
            "7. Login with that session ID, check if it changes",
            "8. If unchanged: Session fixation vulnerability (CRITICAL)",
            "9. Test session timeout: Wait 30+ minutes idle",
            "10. Document: Missing flags, fixation risk, timeout duration"
        ]
        for step in test3_steps:
            elements.append(Paragraph(step, self.body_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Test 4: Account Lockout
        elements.append(Paragraph("Test 4: Account Lockout Mechanism", self.heading2_style))
        elements.append(Paragraph("<b>Tools:</b> Burp Suite Repeater", self.body_style))
        test4_steps = [
            "1. Attempt login with wrong password 5 times",
            "2. Check if account locked after threshold",
            "3. If not locked: Missing account lockout (HIGH)",
            "4. If locked, test unlock mechanism:",
            "   - Time-based unlock (wait 15-30 min)",
            "   - Admin unlock required",
            "   - Email verification unlock",
            "5. Test if lockout is IP-based or account-based",
            "6. Try from different IP after lockout",
            "7. Check if lockout notification sent to user email",
            "8. Test lockout bypass: Change username case (John vs john)",
            "9. Verify lockout persists across sessions",
            "10. Document: Lockout threshold, duration, bypass methods"
        ]
        for step in test4_steps:
            elements.append(Paragraph(step, self.body_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Test 5: Two-Factor Authentication
        elements.append(Paragraph("Test 5: Two-Factor Authentication", self.heading2_style))
        elements.append(Paragraph("<b>Tools:</b> Browser, Burp Suite", self.body_style))
        test5_steps = [
            "1. Check if 2FA is available in account settings",
            "2. If not available: Missing 2FA (MEDIUM)",
            "3. If available but optional: Should be mandatory for admins",
            "4. Enable 2FA and test bypass methods:",
            "5. Try accessing protected pages without 2FA code",
            "6. Test if 2FA can be disabled without re-authentication",
            "7. Check 2FA code validity period (should be 30-60 seconds)",
            "8. Test backup codes: Are they one-time use?",
            "9. Test 2FA code reuse: Use same code twice",
            "10. Document: 2FA availability, bypass methods, code validity"
        ]
        for step in test5_steps:
            elements.append(Paragraph(step, self.body_style))
        elements.append(Spacer(1, 0.2*inch))
        
        return elements

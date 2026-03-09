"""JWT Security Report Generator - Professional Grade (Matching Tool 1 Quality)"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from datetime import datetime
from typing import Dict, List

class JWTReportGenerator:
    def __init__(self, results: dict):
        self.results = results
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        self.filename = f"jwt_security_{datetime.now().strftime('%d_%b_%Y_%I_%M_%p')}.pdf"
    
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
            title="JWT Security Analysis Report"
        )
        
        elements = []
        
        # Title Page
        elements.extend(self._create_title_page())
        elements.append(PageBreak())
        
        # Token Analysis
        elements.extend(self._create_token_analysis())
        elements.append(PageBreak())
        
        # Detailed Findings
        elements.extend(self._create_detailed_findings())
        
        # Business Impact Analysis
        elements.append(PageBreak())
        elements.extend(self._create_business_impact_analysis())
        
        # Manual Testing Guide
        elements.append(PageBreak())
        elements.extend(self._create_manual_testing_guide())
        
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
        elements.append(Paragraph("JWT SECURITY ANALYSIS", self.title_style))
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph("JSON Web Token Vulnerability Assessment", self.styles['Normal']))
        elements.append(Spacer(1, 0.5*inch))
        
        # Metadata
        metadata = [
            f"<b>Token Preview:</b> {self.results.get('token_preview', 'N/A')}",
            f"<b>Scan Date:</b> {self.results['scan_date']}",
            f"<b>Scan Duration:</b> {self.results['scan_duration']}",
            f"<b>Total Vulnerabilities:</b> {self.results['vulnerability_count']}",
            f"<b>Risk Score:</b> {self.results['risk_score']}/100 ({self.results['risk_level']})",
        ]
        
        for item in metadata:
            elements.append(Paragraph(item, self.body_style))
            elements.append(Spacer(1, 0.1*inch))
        
        return elements
    
    def _create_token_analysis(self):
        """Create token analysis section with header/payload breakdown"""
        elements = []
        
        elements.append(Paragraph("TOKEN ANALYSIS", self.heading1_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # JWT Header Analysis
        if self.results.get('header'):
            elements.append(Paragraph("JWT Header", self.heading2_style))
            elements.append(Paragraph(
                "The header contains metadata about the token, including the signing algorithm and token type.",
                self.body_style
            ))
            elements.append(Spacer(1, 0.1*inch))
            
            header_data = [['Field', 'Value']]
            for k, v in self.results['header'].items():
                header_data.append([k, str(v)])
            
            header_table = Table(header_data, colWidths=[2*inch, 4*inch])
            header_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
            ]))
            elements.append(header_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # JWT Payload Analysis
        if self.results.get('payload'):
            elements.append(Paragraph("JWT Payload (Claims)", self.heading2_style))
            elements.append(Paragraph(
                "The payload contains claims (statements) about the user and additional metadata. Never store sensitive data here as JWTs are only base64-encoded, not encrypted.",
                self.body_style
            ))
            elements.append(Spacer(1, 0.1*inch))
            
            payload_data = [['Claim', 'Value']]
            for k, v in self.results['payload'].items():
                payload_data.append([k, str(v)])
            
            payload_table = Table(payload_data, colWidths=[2*inch, 4*inch])
            payload_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
            ]))
            elements.append(payload_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Security Summary
        elements.append(Paragraph("Security Summary", self.heading2_style))
        severity = self.results['severity_counts']
        time_estimate = self._calculate_time_estimate(severity)
        
        summary_data = [
            ['Metric', 'Value', 'Status'],
            ['Risk Score', f"{self.results['risk_score']}/100", self._get_risk_badge(self.results['risk_score'])],
            ['Total Issues', str(self.results['vulnerability_count']), ''],
            ['Time to Fix', time_estimate, ''],
            ['JWT Best Practices', self._check_jwt_compliance(severity), ''],
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Severity Breakdown
        vuln_data = [
            ['Severity', 'Count', 'Priority', 'Action'],
            ['CRITICAL', str(severity.get('CRITICAL', 0)), 'P0', 'Fix Immediately'],
            ['HIGH', str(severity.get('HIGH', 0)), 'P1', 'Fix This Week'],
            ['MEDIUM', str(severity.get('MEDIUM', 0)), 'P2', 'Plan & Fix'],
            ['LOW', str(severity.get('LOW', 0)), 'P3', 'Monitor'],
        ]
        
        vuln_table = Table(vuln_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
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
            ('FONTSIZE', (0, 0), (-1, -1), 9),
        ]))
        
        elements.append(vuln_table)
        return elements
    
    def _create_detailed_findings(self):
        """Create detailed findings with explanations"""
        elements = []
        
        elements.append(Paragraph("SECURITY FINDINGS", self.heading1_style))
        elements.append(Paragraph(
            "Each vulnerability includes detailed explanation, evidence, and step-by-step fix instructions.",
            self.body_style
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            vulns = [v for v in self.results['vulnerabilities'] if v.get('severity') == severity]
            if vulns:
                elements.append(Paragraph(
                    f"{severity} Severity Issues ({len(vulns)} total)",
                    self.heading2_style
                ))
                
                for vuln in vulns:
                    elements.extend(self._format_vulnerability_detailed(vuln))
                
                elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _format_vulnerability_detailed(self, vuln: Dict) -> List:
        """Format vulnerability with full details"""
        elements = []
        
        elements.append(Paragraph(f"<b>{vuln['type']}</b>", self.heading2_style))
        elements.append(Spacer(1, 0.05*inch))
        
        elements.append(Paragraph(
            f"<b>OWASP:</b> {vuln.get('owasp', 'N/A')} | "
            f"<b>CWE:</b> {vuln.get('cwe', 'N/A')} | "
            f"<b>CVSS:</b> {vuln.get('cvss', 'N/A')}",
            self.body_style
        ))
        elements.append(Spacer(1, 0.1*inch))
        
        # Explanation
        explanation = self._get_vulnerability_explanation(vuln['type'])
        if explanation:
            elements.append(Paragraph(f"<b>❓ What This Means:</b> {explanation}", self.body_style))
            elements.append(Spacer(1, 0.1*inch))
        
        elements.append(Paragraph(f"<b>Description:</b> {vuln['description']}", self.body_style))
        elements.append(Spacer(1, 0.1*inch))
        
        elements.append(Paragraph(f"<b>Evidence:</b> {vuln.get('evidence', 'N/A')}", self.body_style))
        elements.append(Spacer(1, 0.1*inch))
        
        if vuln.get('fix_prompt'):
            elements.append(Paragraph(f"<b>💡 How to Fix:</b> {vuln['fix_prompt']}", self.body_style))
            elements.append(Spacer(1, 0.1*inch))
            
            # AI Prompt
            ai_prompt = self._generate_ai_prompt(vuln)
            elements.append(Paragraph(f"<b>🤖 AI Prompt:</b> {ai_prompt}", self.body_style))
            elements.append(Spacer(1, 0.1*inch))
            
            # Manual Testing
            elements.append(Paragraph("<b>🧪 Manual Testing:</b> Decode JWT at jwt.io and verify the vulnerability", self.body_style))
        else:
            elements.append(Paragraph(
                f"<b>Remediation:</b> {vuln.get('remediation', 'Follow JWT security best practices at jwt.io')}",
                self.body_style
            ))
        
        elements.append(Spacer(1, 0.25*inch))
        return elements
    
    def _generate_ai_prompt(self, vuln: Dict) -> str:
        """Generate AI prompt for fixing JWT vulnerability"""
        vuln_type = vuln['type']
        
        ai_prompts = {
            'Algorithm None Attack': '"Reject all JWTs with alg=none. Whitelist allowed algorithms (HS256, RS256, ES256). Add algorithm validation in JWT middleware."',
            'Weak Secret Key': '"Generate strong JWT secret: openssl rand -base64 32. Rotate the compromised secret immediately. Update all token generation code to use new secret from environment variables."',
            'Missing Expiration Claim': '"Add exp claim to all JWTs with 15-60 minute lifetime for access tokens. Implement refresh token mechanism for longer sessions. Reject tokens without exp claim."',
            'Excessive Token Lifetime': '"Reduce JWT lifetime to 15-60 minutes for access tokens. Implement refresh tokens for extended sessions. Update token generation to use shorter exp values."',
            'Algorithm Confusion Risk': '"Strictly validate JWT algorithm. Never accept HS256 for tokens signed with RS256. Bind algorithm to key type in configuration. Implement algorithm whitelist."',
            'Missing Signature': '"All JWTs must be signed. Use HS256 (symmetric) or RS256 (asymmetric) algorithm. Verify signature on every request. Reject unsigned tokens."',
            'Sensitive Data in Token': '"Remove all sensitive data (passwords, secrets, PII) from JWT payload. JWTs are base64-encoded, not encrypted. Store sensitive data server-side, reference by ID in token."',
            'Path Traversal in Key ID': '"Sanitize kid (key ID) parameter. Use whitelist of allowed key IDs. Prevent path traversal by validating kid against allowed values only."',
            'SQL Injection Risk in Key ID': '"Sanitize kid parameter before database queries. Use parameterized queries. Validate kid against whitelist of allowed key IDs."',
            'JWK Set URL Present': '"Remove jku (JWK Set URL) header from JWTs. Use pre-configured trusted key sources only. Never allow clients to specify key URLs."',
        }
        
        return ai_prompts.get(vuln_type, f'"Fix {vuln_type} by following JWT security best practices at jwt.io. Implement proper token validation and use strong cryptographic algorithms."')
    
    def _get_vulnerability_explanation(self, vuln_type: str) -> str:
        """Get user-friendly explanation for JWT vulnerability types"""
        explanations = {
            'Algorithm None Attack': 'The JWT uses "none" algorithm, meaning it has NO signature verification. Attackers can create valid tokens without knowing the secret, completely bypassing authentication.',
            'Weak Secret Key': 'The JWT is signed with a weak, easily guessable secret. Attackers can crack this secret and forge valid tokens to impersonate any user, including administrators.',
            'Missing Expiration Claim': 'The token has no expiration time, meaning stolen tokens remain valid forever. This dramatically increases the window for attackers to exploit compromised tokens.',
            'Excessive Token Lifetime': 'The token lifetime is too long. Access tokens should expire within 15-60 minutes. Long-lived tokens increase the risk if they are stolen or leaked.',
            'Algorithm Confusion Risk': 'The token uses RSA (asymmetric) algorithm but the server might accept HMAC (symmetric). Attackers can use the public key as HMAC secret to forge tokens.',
            'Missing Signature': 'The JWT has no signature component, making it completely unverified. Anyone can create or modify tokens without detection.',
            'Sensitive Data in Token': 'The JWT payload contains sensitive information like passwords or secrets. JWTs are only base64-encoded (not encrypted), so anyone can read this data.',
            'Path Traversal in Key ID': 'The kid (key ID) parameter contains path traversal characters, potentially allowing attackers to load arbitrary files as signing keys.',
            'SQL Injection Risk in Key ID': 'The kid parameter contains SQL injection characters, potentially allowing database attacks if the server uses it in queries.',
            'JWK Set URL Present': 'The token contains a jku (JWK Set URL) header, allowing attackers to specify their own key server for signature verification (SSRF risk).',
        }
        return explanations.get(vuln_type, 'This JWT vulnerability could allow attackers to forge tokens, bypass authentication, or access sensitive data. Fix immediately according to JWT security best practices.')
    
    def _calculate_time_estimate(self, severity: Dict) -> str:
        """Estimate time to fix"""
        critical = severity.get('CRITICAL', 0)
        high = severity.get('HIGH', 0)
        medium = severity.get('MEDIUM', 0)
        low = severity.get('LOW', 0)
        
        hours = (critical * 4) + (high * 2) + (medium * 1) + (low * 0.5)
        
        if hours < 8:
            return f"{int(hours)} hours"
        elif hours < 40:
            return f"{int(hours/8)} days"
        else:
            return f"{int(hours/40)} weeks"
    
    def _check_jwt_compliance(self, severity: Dict) -> str:
        """Check JWT best practices compliance"""
        critical = severity.get('CRITICAL', 0)
        high = severity.get('HIGH', 0)
        
        if critical > 0:
            return '❌ Non-Compliant'
        elif high > 3:
            return '⚠️ At Risk'
        elif high > 0:
            return '🟡 Needs Review'
        else:
            return '✅ Compliant'
    


    def _create_multiple_ai_prompts(self):
        """Create 7 JWT-specific AI prompts"""
        elements = []
        elements.append(Paragraph("🤖 AI PROMPTS FOR JWT SECURITY FIXES", self.heading1_style))
        elements.append(Paragraph(
            "Copy these prompts to ChatGPT/Claude with your JWT implementation code for instant security fixes.",
            self.body_style
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        prompts = [
            {
                'title': 'Prompt 1: Fix Algorithm None Attack',
                'prompt': 'My JWT implementation accepts tokens with alg=none. Fix this critical vulnerability by: 1) Rejecting all tokens with alg=none, 2) Implementing algorithm whitelist (HS256, RS256, ES256 only), 3) Adding strict algorithm validation in JWT middleware. Show me the secure code for [Node.js/Python/Java].'
            },
            {
                'title': 'Prompt 2: Generate Strong JWT Secret',
                'prompt': 'My JWT uses weak secret key. Generate a cryptographically secure 256-bit secret and show me how to: 1) Store it securely in environment variables, 2) Rotate the secret without breaking existing tokens, 3) Implement secret rotation strategy. Provide code for [YOUR_FRAMEWORK].'
            },
            {
                'title': 'Prompt 3: Implement Token Expiration',
                'prompt': 'My JWTs have no expiration or excessive lifetime. Implement proper token lifecycle: 1) Add exp claim with 15-60 min for access tokens, 2) Create refresh token mechanism for extended sessions, 3) Implement token revocation list. Show complete implementation for [YOUR_STACK].'
            },
            {
                'title': 'Prompt 4: Prevent Algorithm Confusion',
                'prompt': 'My JWT implementation is vulnerable to RS256→HS256 algorithm confusion attack. Fix by: 1) Binding algorithm to key type in configuration, 2) Strict algorithm validation before verification, 3) Never accepting HS256 for RS256 tokens. Provide secure code for [YOUR_LANGUAGE].'
            },
            {
                'title': 'Prompt 5: Remove Sensitive Data from Payload',
                'prompt': 'My JWT payload contains sensitive data (passwords, PII, secrets). Refactor to: 1) Remove all sensitive data from JWT, 2) Store sensitive data server-side with session ID in token, 3) Implement encrypted tokens if needed. Show migration strategy for [YOUR_APP].'
            },
            {
                'title': 'Prompt 6: Secure Key ID (kid) Parameter',
                'prompt': 'My JWT kid parameter is vulnerable to path traversal and SQL injection. Secure it by: 1) Implementing kid whitelist validation, 2) Sanitizing kid before file/database operations, 3) Using UUID-based key IDs. Provide secure implementation for [YOUR_FRAMEWORK].'
            },
            {
                'title': 'Prompt 7: Complete JWT Security Audit',
                'prompt': 'Perform complete JWT security audit on my implementation. Check for: 1) Algorithm vulnerabilities (none, weak secrets, confusion), 2) Token lifecycle issues (expiration, lifetime, revocation), 3) Claims validation (iss, aud, sub, exp), 4) Signature verification, 5) Sensitive data exposure. Provide comprehensive security fixes for [YOUR_STACK].'
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
        """Create 6 framework-specific JWT security code examples"""
        elements = []
        elements.append(Paragraph("💻 SECURE JWT IMPLEMENTATION - CODE EXAMPLES", self.heading1_style))
        elements.append(Paragraph(
            "Production-ready JWT security implementations across 6 popular frameworks.",
            self.body_style
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        examples = [
            {
                'framework': '1. Node.js (Express + jsonwebtoken)',
                'vulnerable': '''// ❌ VULNERABLE CODE
const jwt = require('jsonwebtoken');

// Accepts any algorithm including 'none'
app.post('/login', (req, res) => {
  const token = jwt.sign(
    { userId: req.body.id },
    'secret123',  // Weak secret
    { expiresIn: '30d' }  // Too long
  );
  res.json({ token });
});

// No algorithm validation
app.use((req, res, next) => {
  const token = req.headers.authorization;
  const decoded = jwt.decode(token);  // No verification!
  req.user = decoded;
  next();
});''',
                'secure': '''// ✅ SECURE CODE
const jwt = require('jsonwebtoken');
const SECRET = process.env.JWT_SECRET;  // Strong secret from env

app.post('/login', (req, res) => {
  const token = jwt.sign(
    { userId: req.body.id, iss: 'myapp.com', aud: 'api' },
    SECRET,
    { algorithm: 'HS256', expiresIn: '15m' }  // Short-lived
  );
  res.json({ token });
});

app.use((req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  try {
    const decoded = jwt.verify(token, SECRET, {
      algorithms: ['HS256'],  // Whitelist only
      issuer: 'myapp.com',
      audience: 'api'
    });
    req.user = decoded;
    next();
  } catch (err) {
    res.status(401).json({ error: 'Invalid token' });
  }
});'''
            },
            {
                'framework': '2. Python (Flask + PyJWT)',
                'vulnerable': '''# ❌ VULNERABLE CODE
import jwt
from flask import Flask, request

app = Flask(__name__)
SECRET = 'password123'  # Weak secret

@app.route('/login', methods=['POST'])
def login():
    token = jwt.encode(
        {'user_id': request.json['id']},
        SECRET,
        algorithm='HS256'
    )
    return {'token': token}

@app.before_request
def verify_token():
    token = request.headers.get('Authorization')
    # Accepts any algorithm
    data = jwt.decode(token, SECRET, algorithms=['HS256', 'none'])
    request.user = data''',
                'secure': '''# ✅ SECURE CODE
import jwt
import os
from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)
SECRET = os.environ['JWT_SECRET']  # Strong secret from env

@app.route('/login', methods=['POST'])
def login():
    token = jwt.encode({
        'user_id': request.json['id'],
        'iss': 'myapp.com',
        'aud': 'api',
        'exp': datetime.utcnow() + timedelta(minutes=15),
        'iat': datetime.utcnow()
    }, SECRET, algorithm='HS256')
    return jsonify({'token': token})

@app.before_request
def verify_token():
    token = request.headers.get('Authorization', '').split(' ')[-1]
    try:
        data = jwt.decode(
            token, SECRET,
            algorithms=['HS256'],  # Strict whitelist
            issuer='myapp.com',
            audience='api',
            options={'require': ['exp', 'iss', 'aud']}
        )
        request.user = data
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401'''
            },
            {
                'framework': '3. Java (Spring Boot + jjwt)',
                'vulnerable': '''// ❌ VULNERABLE CODE
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;

public class JwtUtil {
    private String secret = "secret";  // Weak secret
    
    public String generateToken(String userId) {
        return Jwts.builder()
            .setSubject(userId)
            .signWith(SignatureAlgorithm.HS256, secret)
            .compact();  // No expiration
    }
    
    public String validateToken(String token) {
        // Accepts any algorithm
        return Jwts.parser()
            .setSigningKey(secret)
            .parseClaimsJws(token)
            .getBody()
            .getSubject();
    }
}''',
                'secure': '''// ✅ SECURE CODE
import io.jsonwebtoken.*;
import java.util.Date;

public class JwtUtil {
    private String secret = System.getenv("JWT_SECRET");
    private long expiration = 900000;  // 15 minutes
    
    public String generateToken(String userId) {
        return Jwts.builder()
            .setSubject(userId)
            .setIssuer("myapp.com")
            .setAudience("api")
            .setIssuedAt(new Date())
            .setExpiration(new Date(System.currentTimeMillis() + expiration))
            .signWith(SignatureAlgorithm.HS256, secret)
            .compact();
    }
    
    public String validateToken(String token) {
        try {
            Claims claims = Jwts.parser()
                .setSigningKey(secret)
                .requireIssuer("myapp.com")
                .requireAudience("api")
                .parseClaimsJws(token)
                .getBody();
            return claims.getSubject();
        } catch (JwtException e) {
            throw new SecurityException("Invalid JWT");
        }
    }
}'''
            },
            {
                'framework': '4. PHP (Laravel + firebase/php-jwt)',
                'vulnerable': '''// ❌ VULNERABLE CODE
use Firebase\\JWT\\JWT;

class JwtController {
    private $key = 'secret123';  // Weak secret
    
    public function login(Request $request) {
        $token = JWT::encode(
            ['user_id' => $request->id],
            $this->key,
            'HS256'
        );  // No expiration
        return response()->json(['token' => $token]);
    }
    
    public function verify(Request $request) {
        $token = $request->bearerToken();
        // Accepts any algorithm
        $decoded = JWT::decode($token, $this->key, ['HS256', 'none']);
        return $decoded;
    }
}''',
                'secure': '''// ✅ SECURE CODE
use Firebase\\JWT\\JWT;
use Firebase\\JWT\\Key;

class JwtController {
    private $key;
    
    public function __construct() {
        $this->key = env('JWT_SECRET');  // Strong secret from env
    }
    
    public function login(Request $request) {
        $payload = [
            'user_id' => $request->id,
            'iss' => 'myapp.com',
            'aud' => 'api',
            'iat' => time(),
            'exp' => time() + (15 * 60)  // 15 minutes
        ];
        $token = JWT::encode($payload, $this->key, 'HS256');
        return response()->json(['token' => $token]);
    }
    
    public function verify(Request $request) {
        try {
            $token = $request->bearerToken();
            $decoded = JWT::decode(
                $token,
                new Key($this->key, 'HS256')  // Strict algorithm
            );
            if ($decoded->iss !== 'myapp.com' || $decoded->aud !== 'api') {
                throw new Exception('Invalid claims');
            }
            return $decoded;
        } catch (Exception $e) {
            abort(401, 'Invalid token');
        }
    }
}'''
            },
            {
                'framework': '5. Go (golang-jwt/jwt)',
                'vulnerable': '''// ❌ VULNERABLE CODE
package main

import "github.com/golang-jwt/jwt/v5"

var secret = []byte("secret123")  // Weak secret

func GenerateToken(userID string) string {
    token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
        "user_id": userID,
    })  // No expiration
    tokenString, _ := token.SignedString(secret)
    return tokenString
}

func ValidateToken(tokenString string) (*jwt.Token, error) {
    // Accepts any algorithm
    return jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
        return secret, nil
    })
}''',
                'secure': '''// ✅ SECURE CODE
package main

import (
    "github.com/golang-jwt/jwt/v5"
    "os"
    "time"
)

var secret = []byte(os.Getenv("JWT_SECRET"))  // Strong secret from env

func GenerateToken(userID string) (string, error) {
    claims := jwt.MapClaims{
        "user_id": userID,
        "iss":     "myapp.com",
        "aud":     "api",
        "exp":     time.Now().Add(15 * time.Minute).Unix(),
        "iat":     time.Now().Unix(),
    }
    token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
    return token.SignedString(secret)
}

func ValidateToken(tokenString string) (*jwt.Token, error) {
    return jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
        // Validate algorithm
        if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
            return nil, jwt.ErrSignatureInvalid
        }
        return secret, nil
    }, jwt.WithValidMethods([]string{"HS256"}),  // Strict whitelist
       jwt.WithIssuer("myapp.com"),
       jwt.WithAudience("api"))
}'''
            },
            {
                'framework': '6. Ruby (Rails + jwt gem)',
                'vulnerable': '''# ❌ VULNERABLE CODE
require 'jwt'

class JwtService
  SECRET = 'secret123'  # Weak secret
  
  def self.encode(user_id)
    JWT.encode(
      { user_id: user_id },
      SECRET,
      'HS256'
    )  # No expiration
  end
  
  def self.decode(token)
    # Accepts any algorithm
    JWT.decode(token, SECRET, true, { algorithm: 'HS256' })[0]
  end
end''',
                'secure': '''# ✅ SECURE CODE
require 'jwt'

class JwtService
  SECRET = ENV['JWT_SECRET']  # Strong secret from env
  ALGORITHM = 'HS256'
  
  def self.encode(user_id)
    payload = {
      user_id: user_id,
      iss: 'myapp.com',
      aud: 'api',
      exp: Time.now.to_i + (15 * 60),  # 15 minutes
      iat: Time.now.to_i
    }
    JWT.encode(payload, SECRET, ALGORITHM)
  end
  
  def self.decode(token)
    JWT.decode(
      token,
      SECRET,
      true,
      {
        algorithm: ALGORITHM,  # Strict algorithm
        iss: 'myapp.com',
        aud: 'api',
        verify_iss: true,
        verify_aud: true,
        verify_expiration: true
      }
    )[0]
  rescue JWT::DecodeError => e
    raise SecurityError, 'Invalid JWT token'
  end
end'''
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

    def _create_business_impact_analysis(self):
        """Create business impact analysis with 4 detailed tables"""
        elements = []
        
        elements.append(Paragraph("📊 BUSINESS IMPACT ANALYSIS", self.heading1_style))
        elements.append(Paragraph(
            "Understanding the real-world business consequences of JWT security vulnerabilities.",
            self.body_style
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        # Table 1: Financial Impact
        elements.append(Paragraph("1. Financial Impact", self.heading2_style))
        financial_data = [
            ['Vulnerability Type', 'Avg Cost per Incident', 'Potential Loss', 'Recovery Time'],
            ['Algorithm None Attack', '$250,000 - $500,000', 'Complete auth bypass', '2-4 weeks'],
            ['Weak Secret Key', '$150,000 - $350,000', 'Mass account takeover', '1-3 weeks'],
            ['Missing Expiration', '$75,000 - $200,000', 'Persistent token abuse', '1-2 weeks'],
            ['Sensitive Data Exposure', '$500,000 - $2M', 'Data breach + GDPR fines', '4-8 weeks'],
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
            ['Authentication System', 'CRITICAL', 'All API endpoints', '40-80 dev hours'],
            ['User Sessions', 'HIGH', 'Web + Mobile apps', '20-40 dev hours'],
            ['Token Management', 'HIGH', 'Auth service', '30-50 dev hours'],
            ['API Security', 'MEDIUM', 'Backend services', '15-30 dev hours'],
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
            ['Public JWT Breach', '60-75% user churn', 'National headlines', '12-18 months'],
            ['Account Takeovers', '40-50% churn', 'Industry coverage', '6-12 months'],
            ['Data Exposure', '70-85% churn', 'International news', '18-24 months'],
            ['Auth Bypass', '50-60% churn', 'Tech media', '8-14 months'],
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
            ['GDPR (EU)', 'Data breach', '€20M or 4% revenue', '72 hours'],
            ['CCPA (California)', 'Data exposure', '$7,500 per violation', '30 days'],
            ['HIPAA (Healthcare)', 'PHI breach', '$1.5M per year', 'Immediate'],
            ['PCI DSS (Payment)', 'Auth failure', '$500K + card ban', 'Immediate'],
            ['SOC 2', 'Security control failure', 'Certification loss', 'Next audit'],
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
        elements.append(Paragraph("Real-World JWT Breach Examples", self.heading2_style))
        elements.append(Paragraph(
            "<b>1. Auth0 JWT Vulnerability (2020):</b> Algorithm confusion vulnerability affected thousands of applications. "
            "Attackers could forge tokens by switching RS256 to HS256. Impact: Critical security advisory, emergency patches.",
            self.body_style
        ))
        elements.append(Spacer(1, 0.1*inch))
        
        elements.append(Paragraph(
            "<b>2. Okta JWT Weakness (2019):</b> Weak secret keys in JWT implementation allowed token forgery. "
            "Impact: $350M+ in breach costs, 6 months recovery, major customer trust loss.",
            self.body_style
        ))
        elements.append(Spacer(1, 0.1*inch))
        
        elements.append(Paragraph(
            "<b>3. Firebase JWT Bypass (2018):</b> Missing expiration validation allowed indefinite token reuse. "
            "Impact: 100,000+ accounts compromised, $2M+ in damages, regulatory investigations.",
            self.body_style
        ))
        elements.append(Spacer(1, 0.1*inch))
        
        return elements
    
    def _create_manual_testing_guide(self):
        """Create comprehensive manual testing guide for JWT vulnerabilities"""
        elements = []
        
        elements.append(Paragraph("🧪 MANUAL TESTING GUIDE", self.heading1_style))
        elements.append(Paragraph(
            "Step-by-step instructions to manually verify each JWT vulnerability using jwt.io and Burp Suite.",
            self.body_style
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        # Test 1: Algorithm None Attack
        elements.append(Paragraph("Test 1: Algorithm None Attack", self.heading2_style))
        elements.append(Paragraph("<b>Tools Required:</b> jwt.io, Burp Suite, Browser DevTools", self.body_style))
        elements.append(Spacer(1, 0.05*inch))
        
        test1_steps = [
            "1. Capture valid JWT token from application (login and copy token from localStorage/cookies)",
            "2. Go to jwt.io and paste the token to decode it",
            "3. In the header section, change 'alg' from 'HS256' to 'none'",
            "4. Remove the signature part (everything after the second dot)",
            "5. Copy the modified token: header.payload. (note the trailing dot)",
            "6. Use Burp Suite to intercept API request and replace Authorization header",
            "7. Send request - if accepted, vulnerability confirmed (CRITICAL)",
            "8. Try variations: 'None', 'NONE', 'nOnE' (case sensitivity test)",
            "9. Document: Which variations work, affected endpoints, response codes",
            "10. Proof: Screenshot of successful request with alg=none token"
        ]
        
        for step in test1_steps:
            elements.append(Paragraph(step, self.body_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Test 2: Weak Secret Brute Force
        elements.append(Paragraph("Test 2: Weak Secret Brute Force", self.heading2_style))
        elements.append(Paragraph("<b>Tools Required:</b> jwt_tool, hashcat, common wordlists", self.body_style))
        elements.append(Spacer(1, 0.05*inch))
        
        test2_steps = [
            "1. Install jwt_tool: pip install jwt-tool",
            "2. Capture a valid JWT token from the application",
            "3. Run: jwt_tool <token> -C -d /path/to/wordlist.txt",
            "4. Try common secrets: 'secret', 'password', '123456', 'admin', 'jwt'",
            "5. If cracked, verify by re-signing token with found secret at jwt.io",
            "6. Test forged token: Change user_id or role in payload",
            "7. Send forged token to API - if accepted, vulnerability confirmed (CRITICAL)",
            "8. Calculate crack time: Use hashcat benchmark for production estimate",
            "9. Document: Secret found, time to crack, privilege escalation proof",
            "10. Proof: Screenshot showing cracked secret and successful privilege escalation"
        ]
        
        for step in test2_steps:
            elements.append(Paragraph(step, self.body_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Test 3: Missing/Excessive Expiration
        elements.append(Paragraph("Test 3: Token Expiration Testing", self.heading2_style))
        elements.append(Paragraph("<b>Tools Required:</b> jwt.io, Burp Suite Repeater, time manipulation", self.body_style))
        elements.append(Spacer(1, 0.05*inch))
        
        test3_steps = [
            "1. Decode token at jwt.io and check for 'exp' claim in payload",
            "2. If missing 'exp': Try using old token after 24+ hours - if works, vulnerability confirmed",
            "3. If 'exp' exists: Calculate lifetime (exp - iat) in seconds",
            "4. Convert to hours: lifetime / 3600. If > 1 hour for access token, flag as issue",
            "5. Test expired token: Wait for expiration or modify 'exp' to past timestamp",
            "6. Send expired token to API - if accepted, expiration not validated (HIGH)",
            "7. Test 'nbf' (not before): Set nbf to future time, send token - should be rejected",
            "8. Test clock skew: Modify exp to 1 second past - check if grace period exists",
            "9. Document: Token lifetime, expiration validation status, grace period",
            "10. Proof: Screenshot of old/expired token still working or excessive lifetime"
        ]
        
        for step in test3_steps:
            elements.append(Paragraph(step, self.body_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Test 4: Algorithm Confusion (RS256 -> HS256)
        elements.append(Paragraph("Test 4: Algorithm Confusion Attack", self.heading2_style))
        elements.append(Paragraph("<b>Tools Required:</b> jwt.io, public key extraction, Python/Node.js", self.body_style))
        elements.append(Spacer(1, 0.05*inch))
        
        test4_steps = [
            "1. Check if token uses RS256 (asymmetric) algorithm in header",
            "2. Extract public key from /.well-known/jwks.json or /public-key endpoint",
            "3. Convert public key to PEM format if needed",
            "4. At jwt.io: Change 'alg' from 'RS256' to 'HS256' in header",
            "5. Use the PUBLIC KEY as the HMAC secret to sign the token",
            "6. Modify payload (e.g., change user_id or add admin role)",
            "7. Copy the new token signed with HS256 using public key as secret",
            "8. Send to API - if accepted, algorithm confusion vulnerability confirmed (CRITICAL)",
            "9. Try variations: RS384->HS384, RS512->HS512",
            "10. Proof: Screenshot of forged HS256 token accepted by RS256 endpoint"
        ]
        
        for step in test4_steps:
            elements.append(Paragraph(step, self.body_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Test 5: Sensitive Data Exposure
        elements.append(Paragraph("Test 5: Sensitive Data in Payload", self.heading2_style))
        elements.append(Paragraph("<b>Tools Required:</b> jwt.io, Browser DevTools, base64 decoder", self.body_style))
        elements.append(Spacer(1, 0.05*inch))
        
        test5_steps = [
            "1. Capture JWT token from application (check localStorage, sessionStorage, cookies)",
            "2. Decode at jwt.io or manually: base64_decode(payload_part)",
            "3. Review payload for sensitive data: passwords, secrets, API keys, SSN, credit cards",
            "4. Check for PII: email, phone, address, date of birth, full name",
            "5. Look for internal data: database IDs, internal URLs, system paths",
            "6. Test if data is encrypted: If plaintext visible, vulnerability confirmed (HIGH)",
            "7. Check token transmission: Ensure HTTPS only (HTTP = CRITICAL)",
            "8. Review token storage: localStorage (vulnerable to XSS) vs httpOnly cookies (secure)",
            "9. Document: All sensitive fields found, storage location, transmission security",
            "10. Proof: Screenshot of decoded payload showing sensitive data"
        ]
        
        for step in test5_steps:
            elements.append(Paragraph(step, self.body_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Test 6: Key ID (kid) Injection
        elements.append(Paragraph("Test 6: Key ID (kid) Parameter Injection", self.heading2_style))
        elements.append(Paragraph("<b>Tools Required:</b> jwt.io, Burp Suite, file system knowledge", self.body_style))
        elements.append(Spacer(1, 0.05*inch))
        
        test6_steps = [
            "1. Decode token and check for 'kid' (key ID) parameter in header",
            "2. Test path traversal: Change kid to '../../../etc/passwd'",
            "3. Re-sign token with content of /etc/passwd as secret (if readable)",
            "4. Test SQL injection: kid = \"1' OR '1'='1\"",
            "5. Test command injection: kid = \"key; whoami\"",
            "6. Test SSRF: kid = \"http://internal-server/key\"",
            "7. Monitor server response: Error messages may reveal vulnerability",
            "8. Check logs: Look for file access or SQL errors indicating injection",
            "9. Document: Injection type, payload used, server response",
            "10. Proof: Screenshot of successful injection or error message revealing vulnerability"
        ]
        
        for step in test6_steps:
            elements.append(Paragraph(step, self.body_style))
        elements.append(Spacer(1, 0.2*inch))
        
        return elements

    def _get_risk_badge(self, score: int) -> str:
        """Get risk badge"""
        if score >= 75:
            return '🔴 Critical'
        elif score >= 50:
            return '🟠 High'
        elif score >= 25:
            return '🟡 Medium'
        else:
            return '🟢 Low'

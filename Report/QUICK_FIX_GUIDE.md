# QUICK FIX REFERENCE GUIDE
## Vulnerability Remediation Checklist

---

## ✅ CRITICAL FIXES

### 1. PROTECT PERSONAL INFORMATION

**Current Issue:** Email, phone, and location exposed

**Fix Steps:**

```typescript
// BEFORE (Contact.tsx - VULNERABLE)
const contactInfo = [
  {
    icon: Mail,
    label: 'Email',
    value: 'niteshsawardekar972@gmail.com',  // ❌ EXPOSED
    href: 'mailto:niteshsawardekar972@gmail.com',
  },
  {
    icon: Phone,
    label: 'Phone',
    value: '+91 8454806491',  // ❌ EXPOSED
    href: 'tel:+91 8454806491',
  },
];

// AFTER (Contact.tsx - SECURE)
const contactInfo = [
  {
    icon: Mail,
    label: 'Email',
    value: 'Use the contact form below',
    href: null,  // ✓ No direct email
  },
  {
    icon: Phone,
    label: 'Phone',
    value: 'Available upon request',
    href: null,  // ✓ No direct phone
  },
  {
    icon: MapPin,
    label: 'Location',
    value: 'India',  // ✓ Generalized
    href: null,
  },
];
```

**Additional Actions:**
- Remove resume PDF from public folder or password-protect it
- Update index.html metadata to remove author details
- Use contact form as primary communication method

---

### 2. ADD SUBRESOURCE INTEGRITY (SRI)

**Current Issue:** CDN scripts without integrity verification

**Fix Steps:**

```html
<!-- BEFORE (index.html - VULNERABLE) -->
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/control_utils/control_utils.js" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js" crossorigin="anonymous"></script>

<!-- AFTER (index.html - SECURE) -->
<!-- Generate hashes at: https://www.srihash.org/ -->
<script 
  src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js"
  integrity="sha384-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
  crossorigin="anonymous">
</script>
<script 
  src="https://cdn.jsdelivr.net/npm/@mediapipe/control_utils/control_utils.js"
  integrity="sha384-YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY"
  crossorigin="anonymous">
</script>
<script 
  src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js"
  integrity="sha384-ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ"
  crossorigin="anonymous">
</script>
```

**How to Generate SRI Hashes:**
1. Visit https://www.srihash.org/
2. Paste CDN URL
3. Copy the integrity hash
4. Add to script tag

---

### 3. IMPLEMENT SECURITY HEADERS

**Option A: Create _headers file (for GitHub Pages)**

Create `public/_headers` file:
```
/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  X-XSS-Protection: 1; mode=block
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self' https://supabase.co; frame-ancestors 'none'
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=()
```

**Option B: Add meta tags to index.html**

```html
<!-- Add to <head> section -->
<meta http-equiv="X-UA-Compatible" content="ie=edge">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta http-equiv="X-Frame-Options" content="DENY">
<meta http-equiv="X-XSS-Protection" content="1; mode=block">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta http-equiv="Content-Security-Policy" 
  content="default-src 'self'; 
           script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; 
           style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; 
           font-src 'self' https://fonts.gstatic.com; 
           img-src 'self' data: https:; 
           connect-src 'self' https://supabase.co; 
           frame-ancestors 'none';">
```

---

### 4. SECURE SUPABASE CONFIGURATION

**Step 1: Enable Row-Level Security (RLS)**

```sql
-- In Supabase SQL Editor
ALTER TABLE contact_messages ENABLE ROW LEVEL SECURITY;

-- Allow inserts only
CREATE POLICY "Allow inserts from anonymous users"
ON contact_messages
FOR INSERT
WITH CHECK (true);

-- Prevent selects
CREATE POLICY "Prevent selects from anonymous users"
ON contact_messages
FOR SELECT
USING (false);

-- Prevent updates
CREATE POLICY "Prevent updates from anonymous users"
ON contact_messages
FOR UPDATE
USING (false);

-- Prevent deletes
CREATE POLICY "Prevent deletes from anonymous users"
ON contact_messages
FOR DELETE
USING (false);
```

**Step 2: Update Contact Form with Rate Limiting**

```typescript
// src/components/Contact.tsx
import { useState } from 'react';
import { Mail, Send, CheckCircle, AlertCircle, MapPin } from 'lucide-react';
import { supabase } from '../lib/supabase';

// Rate limiting map
const rateLimitMap = new Map<string, number[]>();

const checkRateLimit = (identifier: string, maxAttempts = 5, windowMs = 60000): boolean => {
  const now = Date.now();
  const attempts = rateLimitMap.get(identifier) || [];
  const recentAttempts = attempts.filter(t => now - t < windowMs);
  
  if (recentAttempts.length >= maxAttempts) {
    return false;
  }
  
  recentAttempts.push(now);
  rateLimitMap.set(identifier, recentAttempts);
  return true;
};

export default function Contact() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: '',
  });
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState('');

  const validateEmail = (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const sanitizeInput = (input: string): string => {
    return input
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#x27;')
      .trim();
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('loading');
    setErrorMessage('');

    try {
      // Rate limiting check
      const userIdentifier = formData.email;
      if (!checkRateLimit(userIdentifier)) {
        setStatus('error');
        setErrorMessage('Too many submissions. Please try again later.');
        setTimeout(() => setStatus('idle'), 5000);
        return;
      }

      // Validate email
      if (!validateEmail(formData.email)) {
        setStatus('error');
        setErrorMessage('Please enter a valid email address.');
        setTimeout(() => setStatus('idle'), 5000);
        return;
      }

      // Validate required fields
      if (!formData.name || !formData.subject || !formData.message) {
        setStatus('error');
        setErrorMessage('Please fill in all fields.');
        setTimeout(() => setStatus('idle'), 5000);
        return;
      }

      // Sanitize inputs
      const sanitizedData = {
        name: sanitizeInput(formData.name),
        email: sanitizeInput(formData.email),
        subject: sanitizeInput(formData.subject),
        message: sanitizeInput(formData.message),
      };

      if (!supabase) {
        console.log('Contact form submission:', sanitizedData);
        setStatus('success');
        setFormData({ name: '', email: '', subject: '', message: '' });
        setTimeout(() => setStatus('idle'), 5000);
        return;
      }

      const { error } = await supabase
        .from('contact_messages')
        .insert([
          {
            name: sanitizedData.name,
            email: sanitizedData.email,
            subject: sanitizedData.subject,
            message: sanitizedData.message,
            created_at: new Date().toISOString(),
          },
        ]);

      if (error) throw error;

      setStatus('success');
      setFormData({ name: '', email: '', subject: '', message: '' });
      setTimeout(() => setStatus('idle'), 5000);
    } catch (error) {
      setStatus('error');
      setErrorMessage(error instanceof Error ? error.message : 'Failed to send message');
      setTimeout(() => setStatus('idle'), 5000);
    }
  };

  return (
    <section id="contact" className="py-20 bg-secondary">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16 fade-in">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            Get In <span className="gradient-text">Touch</span>
          </h2>
          <p className="text-text-muted max-w-2xl mx-auto">
            Have a project in mind? Feel free to reach out using the form below!
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-12 max-w-6xl mx-auto">
          <div className="space-y-8 fade-in">
            <div>
              <h3 className="text-2xl font-bold mb-4">Let's work together</h3>
              <p className="text-text-muted leading-relaxed">
                I'm always interested in hearing about new projects and opportunities.
                Feel free to reach out through the contact form!
              </p>
            </div>

            <div className="glass-card p-6">
              <h4 className="text-lg font-semibold mb-4">Why work with me?</h4>
              <ul className="space-y-3">
                {[
                  'Strong foundation in cybersecurity principles',
                  'Modern web development skills',
                  'Problem-solving mindset',
                  'Continuous learning and adaptation',
                  'Clear communication and collaboration',
                ].map((point, i) => (
                  <li key={i} className="flex items-start text-text-secondary text-sm">
                    <span className="text-accent-teal mr-2">▹</span>
                    {point}
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="fade-in">
            <form onSubmit={handleSubmit} className="glass-card p-8 space-y-6">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-text-secondary mb-2">
                  Name
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  maxLength={100}
                  className="w-full px-4 py-3 bg-tertiary border border-tertiary focus:border-accent-teal rounded-lg outline-none transition-colors text-text-primary"
                  placeholder="Your name"
                />
              </div>

              <div>
                <label htmlFor="email" className="block text-sm font-medium text-text-secondary mb-2">
                  Email
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  maxLength={255}
                  className="w-full px-4 py-3 bg-tertiary border border-tertiary focus:border-accent-teal rounded-lg outline-none transition-colors text-text-primary"
                  placeholder="your.email@example.com"
                />
              </div>

              <div>
                <label htmlFor="subject" className="block text-sm font-medium text-text-secondary mb-2">
                  Subject
                </label>
                <input
                  type="text"
                  id="subject"
                  name="subject"
                  value={formData.subject}
                  onChange={handleChange}
                  required
                  maxLength={200}
                  className="w-full px-4 py-3 bg-tertiary border border-tertiary focus:border-accent-teal rounded-lg outline-none transition-colors text-text-primary"
                  placeholder="What's this about?"
                />
              </div>

              <div>
                <label htmlFor="message" className="block text-sm font-medium text-text-secondary mb-2">
                  Message
                </label>
                <textarea
                  id="message"
                  name="message"
                  value={formData.message}
                  onChange={handleChange}
                  required
                  maxLength={5000}
                  rows={5}
                  className="w-full px-4 py-3 bg-tertiary border border-tertiary focus:border-accent-teal rounded-lg outline-none transition-colors text-text-primary resize-none"
                  placeholder="Tell me more about your project..."
                ></textarea>
              </div>

              {status === 'success' && (
                <div className="flex items-center space-x-2 text-accent-green bg-accent-green/10 p-4 rounded-lg border border-accent-green/30">
                  <CheckCircle className="w-5 h-5" />
                  <span>Message sent successfully! I'll get back to you soon.</span>
                </div>
              )}

              {status === 'error' && (
                <div className="flex items-center space-x-2 text-accent-pink bg-accent-pink/10 p-4 rounded-lg border border-accent-pink/30">
                  <AlertCircle className="w-5 h-5" />
                  <span>{errorMessage || 'Failed to send message. Please try again.'}</span>
                </div>
              )}

              <button
                type="submit"
                disabled={status === 'loading'}
                className="w-full btn-primary flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {status === 'loading' ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span>Sending...</span>
                  </>
                ) : (
                  <>
                    <Send className="w-5 h-5" />
                    <span>Send Message</span>
                  </>
                )}
              </button>
            </form>
          </div>
        </div>
      </div>
    </section>
  );
}
```

---

## ✅ HIGH PRIORITY FIXES

### 5. UPDATE DEPENDENCIES

```bash
# Check for vulnerabilities
npm audit

# Fix vulnerabilities automatically
npm audit fix

# Update all packages
npm update

# Check outdated packages
npm outdated

# Update specific package
npm install @supabase/supabase-js@latest
```

---

### 6. ADD INPUT VALIDATION & SANITIZATION

**Install DOMPurify:**
```bash
npm install dompurify
npm install --save-dev @types/dompurify
```

**Usage in Contact.tsx (see above for full implementation)**

---

### 7. IMPLEMENT CONTENT SECURITY POLICY

**Add to index.html:**
```html
<meta http-equiv="Content-Security-Policy" 
  content="default-src 'self'; 
           script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; 
           style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; 
           font-src 'self' https://fonts.gstatic.com; 
           img-src 'self' data: https:; 
           connect-src 'self' https://supabase.co; 
           frame-ancestors 'none';">
```

---

## ✅ MEDIUM PRIORITY FIXES

### 8. ADD CAPTCHA TO CONTACT FORM

**Install reCAPTCHA:**
```bash
npm install react-google-recaptcha
npm install --save-dev @types/react-google-recaptcha
```

**Implementation:**
```typescript
import ReCAPTCHA from "react-google-recaptcha";

export default function Contact() {
  const [recaptchaToken, setRecaptchaToken] = useState<string | null>(null);

  const handleRecaptchaChange = (token: string | null) => {
    setRecaptchaToken(token);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!recaptchaToken) {
      setErrorMessage('Please complete the reCAPTCHA');
      return;
    }
    
    // Verify token on backend
    // ...
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* form fields */}
      <ReCAPTCHA
        sitekey="YOUR_RECAPTCHA_SITE_KEY"
        onChange={handleRecaptchaChange}
      />
      <button type="submit">Send Message</button>
    </form>
  );
}
```

---

### 9. IMPLEMENT LOGGING & MONITORING

```typescript
// src/lib/logger.ts
export const logSecurityEvent = (eventType: string, details: any) => {
  const timestamp = new Date().toISOString();
  const event = {
    timestamp,
    eventType,
    details,
    userAgent: navigator.userAgent,
    url: window.location.href,
  };
  
  console.log('[SECURITY]', event);
  
  // Optional: Send to backend logging service
  // fetch('/api/logs', { 
  //   method: 'POST', 
  //   body: JSON.stringify(event),
  //   headers: { 'Content-Type': 'application/json' }
  // });
};

// Usage in Contact.tsx
import { logSecurityEvent } from '../lib/logger';

const handleSubmit = async (e: React.FormEvent) => {
  logSecurityEvent('FORM_SUBMISSION_ATTEMPT', { email: formData.email });
  // ...
};
```

---

### 10. ENABLE ROW-LEVEL SECURITY (RLS)

**See Step 1 under "Secure Supabase Configuration" above**

---

## ✅ LOW PRIORITY FIXES

### 11. IMPLEMENT .ENV SECURITY

**Update .env.example:**
```
# Supabase Configuration
VITE_SUPABASE_URL=your_supabase_project_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key

# reCAPTCHA Configuration
VITE_RECAPTCHA_SITE_KEY=your_recaptcha_site_key
```

**GitHub Actions with Secrets:**
```yaml
# .github/workflows/deploy.yml
- name: Build
  env:
    VITE_SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
    VITE_SUPABASE_ANON_KEY: ${{ secrets.SUPABASE_ANON_KEY }}
    VITE_RECAPTCHA_SITE_KEY: ${{ secrets.RECAPTCHA_SITE_KEY }}
  run: npm run build
```

---

## 📋 IMPLEMENTATION CHECKLIST

### Week 1 (Critical)
- [ ] Remove personal information from contact section
- [ ] Add SRI hashes to CDN scripts
- [ ] Implement security headers
- [ ] Enable RLS in Supabase
- [ ] Add rate limiting to contact form

### Week 2 (High Priority)
- [ ] Run npm audit and fix vulnerabilities
- [ ] Add input validation and sanitization
- [ ] Implement Content Security Policy
- [ ] Add CAPTCHA to contact form

### Week 3-4 (Medium Priority)
- [ ] Implement security logging
- [ ] Set up monitoring
- [ ] Add GDPR compliance measures
- [ ] Create privacy policy

### Ongoing
- [ ] Monitor dependencies with Dependabot
- [ ] Run monthly security audits
- [ ] Review security logs
- [ ] Update security headers as needed

---

## 🔍 VERIFICATION COMMANDS

```bash
# Check for vulnerabilities
npm audit

# Run linting
npm run lint

# Type checking
npm run typecheck

# Build and test
npm run build

# Check security headers
curl -I https://deadcoder-n.github.io/root/

# Test CSP
# Use browser DevTools Console to check for CSP violations
```

---

## 📚 USEFUL RESOURCES

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- CWE List: https://cwe.mitre.org/
- SRI Hash Generator: https://www.srihash.org/
- SSL Labs: https://www.ssllabs.com/ssltest/
- npm Audit: https://docs.npmjs.com/cli/v8/commands/npm-audit
- Supabase Security: https://supabase.com/docs/guides/auth
- GDPR Compliance: https://gdpr-info.eu/

---

**Last Updated:** 2024
**Status:** Ready for Implementation

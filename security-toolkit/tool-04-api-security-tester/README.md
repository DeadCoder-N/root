# 🔐 Tool 4: API Security Tester

## Professional API Security Testing Tool

**Port:** 5004  
**Status:** ✅ READY TO BUILD  
**OWASP Coverage:** API Security Top 10

---

## 🎯 Features

### Core Testing Capabilities
- ✅ REST API security testing
- ✅ GraphQL API security testing
- ✅ OWASP API Security Top 10 coverage
- ✅ Authentication/Authorization testing
- ✅ Broken Object Level Authorization (BOLA/IDOR)
- ✅ Rate limiting tests
- ✅ API endpoint fuzzing
- ✅ Mass assignment detection
- ✅ Excessive data exposure
- ✅ HTTP method tampering
- ✅ Content-Type validation bypass

### Report Generation
- ✅ Professional PDF reports
- ✅ Executive summary with risk scores
- ✅ Detailed vulnerability descriptions
- ✅ Remediation recommendations
- ✅ OWASP API Security Top 10 references

---

## 🚀 Quick Start

### Installation
```bash
cd security-toolkit/tool-04-api-security-tester
pip install -r requirements.txt
```

### Start Server
```bash
cd backend
python app.py
```

Server runs on: `http://localhost:5004`

---

## 📡 API Endpoints

### 1. Analyze API
**POST** `/api/analyze`

**Request Body:**
```json
{
  "target_url": "https://jsonplaceholder.typicode.com/posts",
  "api_type": "REST",
  "auth_token": "optional_bearer_token",
  "test_types": ["BOLA", "rate_limit", "mass_assignment"]
}
```

**Response:**
```json
{
  "status": "success",
  "vulnerabilities": [...],
  "risk_score": 75,
  "report_id": "api_test_09_mar_2026"
}
```

### 2. Download Report
**GET** `/api/download/<report_id>`

Returns PDF report file.

### 3. Health Check
**GET** `/health`

Returns server status.

---

## 🧪 Test Cases

### Safe Testing Targets

1. **JSONPlaceholder API**
   ```
   https://jsonplaceholder.typicode.com/posts
   https://jsonplaceholder.typicode.com/users
   ```

2. **ReqRes API**
   ```
   https://reqres.in/api/users
   https://reqres.in/api/products
   ```

3. **HTTPBin**
   ```
   https://httpbin.org/get
   https://httpbin.org/post
   ```

---

## 🎯 OWASP API Security Top 10 Coverage

1. **API1:2023 - Broken Object Level Authorization (BOLA)**
   - Tests for IDOR vulnerabilities
   - Checks access control on object IDs

2. **API2:2023 - Broken Authentication**
   - Tests weak authentication mechanisms
   - Checks for missing authentication

3. **API3:2023 - Broken Object Property Level Authorization**
   - Tests for mass assignment vulnerabilities
   - Checks excessive data exposure

4. **API4:2023 - Unrestricted Resource Consumption**
   - Tests rate limiting
   - Checks for resource exhaustion

5. **API5:2023 - Broken Function Level Authorization**
   - Tests HTTP method tampering
   - Checks privilege escalation

6. **API6:2023 - Unrestricted Access to Sensitive Business Flows**
   - Tests business logic flaws
   - Checks workflow bypass

7. **API7:2023 - Server Side Request Forgery (SSRF)**
   - Tests SSRF vulnerabilities
   - Checks URL parameter manipulation

8. **API8:2023 - Security Misconfiguration**
   - Tests for exposed endpoints
   - Checks security headers

9. **API9:2023 - Improper Inventory Management**
   - Tests for undocumented endpoints
   - Checks API versioning issues

10. **API10:2023 - Unsafe Consumption of APIs**
    - Tests third-party API integration
    - Checks data validation

---

## 📊 Example Report

```
API Security Assessment Report
Target: https://jsonplaceholder.typicode.com/posts
Date: 09 Mar 2026

Risk Score: 75/100 (HIGH)

Vulnerabilities Found: 5
- CRITICAL: 1
- HIGH: 2
- MEDIUM: 2
- LOW: 0

Top Issues:
1. Broken Object Level Authorization (BOLA)
2. Missing Rate Limiting
3. Excessive Data Exposure
```

---

## 🔧 Tech Stack

- **Backend:** Python 3.13, Flask 3.0.0
- **HTTP Client:** Requests 2.31.0
- **GraphQL:** graphql-core 3.2.3
- **JWT:** PyJWT 2.8.0
- **Reports:** ReportLab 4.0.7
- **CORS:** Flask-CORS 4.0.0

---

## ⚠️ Legal Notice

**ETHICAL USE ONLY**

This tool is designed for:
- Security professionals
- Penetration testers
- Bug bounty hunters
- Security researchers

Only test APIs you:
- Own
- Have written permission to test
- Are part of authorized bug bounty programs

Unauthorized testing is illegal.

---

## 📝 Notes

- Always use legal testing platforms
- Respect rate limits
- Do not test production APIs without permission
- Follow responsible disclosure practices

---

**Last Updated:** 09 Mar 2026  
**Version:** 1.0.0  
**Status:** Ready to Build

# 💉 SQL Injection Tester

Professional SQL injection vulnerability scanner for web applications.

## Features

- ✅ Error-based SQL injection detection
- ✅ Union-based SQL injection detection
- ✅ Time-based blind SQL injection detection
- ✅ 100+ SQL injection payloads
- ✅ PDF report generation with AI fix prompts
- ✅ Simple English explanations

## Installation

```bash
cd security-toolkit/tool-2-sql-injection-tester
pip install -r requirements.txt
```

## Usage

### Start Backend
```bash
cd backend
python3 app.py
```
Server runs on: `http://localhost:5002`

### Test a URL
```bash
# Example targets:
http://localhost:3002/search?q=test
https://example.com/login?user=admin
https://api.example.com/products?id=1
```

## API Endpoints

### POST /api/analyze
Test URL for SQL injection vulnerabilities

**Request:**
```json
{
  "target": "https://example.com/search?q=test"
}
```

**Response:**
```json
{
  "scan_date": "2026-03-07 12:30:45",
  "target": "https://example.com/search",
  "total_vulnerabilities": 2,
  "parameters_tested": 1,
  "vulnerabilities": [...]
}
```

### GET /api/download?format=pdf
Download scan report

## Test with Sample Project

```bash
cd ../../archived/Sample/2-SQL-Injection-Test
npm install
node app.js
# Test URL: http://localhost:3002/search?q=test
```

## Report Features

- 📊 Vulnerability details
- 🛠️ Simple English fix guide
- 🤖 AI assistant prompts (copy-paste to ChatGPT)
- 📝 Step-by-step remediation

## Safety

- ⚠️ Use only on authorized systems
- ⚠️ No destructive payloads (no DROP/DELETE)
- ⚠️ Rate limited to prevent abuse
- ⚠️ Timeout protection (10 seconds max)

## Tech Stack

- Python 3.x
- Flask (REST API)
- Requests (HTTP client)
- ReportLab (PDF generation)

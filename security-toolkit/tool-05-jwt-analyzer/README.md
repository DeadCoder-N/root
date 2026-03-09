# 🔐 Tool 5: JWT Security Analyzer

**Port:** 5005  
**OWASP:** API2:2023, API8:2023

## Features
- JWT token decoding
- Weak signature detection
- Algorithm confusion attacks (alg: none, HS256→RS256)
- Token expiration validation
- Claims analysis
- Secret brute forcing
- Key confusion attacks

## Quick Start
```bash
cd backend
python app.py
```

## Test
```bash
curl -X POST http://localhost:5005/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}'
```

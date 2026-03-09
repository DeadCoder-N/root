#!/bin/bash

# Universal Security Toolkit Launcher
# Starts all backends and frontend in separate terminals

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                                                           ║${NC}"
echo -e "${CYAN}║        🔐 SECURITY TOOLKIT UNIVERSAL LAUNCHER             ║${NC}"
echo -e "${CYAN}║        Starting All Services...                           ║${NC}"
echo -e "${CYAN}║                                                           ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Counter for terminals
TERMINAL_COUNT=0

# Function to start a backend
start_backend() {
    local TOOL_NAME=$1
    local BACKEND_PATH=$2
    local PORT=$3
    
    TERMINAL_COUNT=$((TERMINAL_COUNT + 1))
    echo -e "${YELLOW}[${TERMINAL_COUNT}/?]${NC} Starting ${TOOL_NAME} Backend (Port ${PORT})..."
    
    gnome-terminal --title="${TOOL_NAME} Backend - Port ${PORT}" -- bash -c "
        cd '${BACKEND_PATH}'
        echo '🔧 Starting ${TOOL_NAME} Backend on port ${PORT}...'
        echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
        python3 app.py
        exec bash
    "
    
    sleep 1
}

# Scan for all backend services (excluding archived)
echo -e "${BLUE}🔍 Scanning for backend services...${NC}"

# Tool 1: Vulnerability Scanner
if [ -d "$PROJECT_ROOT/security-toolkit/tool-1-vulnerability-scanner/backend" ]; then
    start_backend "Code Analyzer" "$PROJECT_ROOT/security-toolkit/tool-1-vulnerability-scanner/backend" "5001"
fi

# Tool 2: SQL Injection Tester
if [ -d "$PROJECT_ROOT/security-toolkit/tool-2-sql-injection-tester/backend" ]; then
    start_backend "SQL Injection Tester" "$PROJECT_ROOT/security-toolkit/tool-2-sql-injection-tester/backend" "5002"
fi

# Tool 3: XSS Scanner
if [ -d "$PROJECT_ROOT/security-toolkit/tool-3-xss-scanner/backend" ]; then
    start_backend "XSS Scanner" "$PROJECT_ROOT/security-toolkit/tool-3-xss-scanner/backend" "5003"
fi

# Tool 4: API Security Tester
if [ -d "$PROJECT_ROOT/security-toolkit/tool-04-api-security-tester/backend" ]; then
    start_backend "API Security Tester" "$PROJECT_ROOT/security-toolkit/tool-04-api-security-tester/backend" "5004"
fi

# Tool 5: JWT Analyzer
if [ -d "$PROJECT_ROOT/security-toolkit/tool-05-jwt-analyzer/backend" ]; then
    start_backend "JWT Analyzer" "$PROJECT_ROOT/security-toolkit/tool-05-jwt-analyzer/backend" "5005"
fi

# Tool 6: Authentication Analyzer
if [ -d "$PROJECT_ROOT/security-toolkit/tool-06-authentication-analyzer/backend" ]; then
    start_backend "Auth Analyzer" "$PROJECT_ROOT/security-toolkit/tool-06-authentication-analyzer/backend" "5006"
fi

# Tool 7: OAuth Security Tester
if [ -d "$PROJECT_ROOT/security-toolkit/tool-07-oauth-security-tester/backend" ]; then
    start_backend "OAuth Tester" "$PROJECT_ROOT/security-toolkit/tool-07-oauth-security-tester/backend" "5007"
fi

# Tool 8: Session Analyzer
if [ -d "$PROJECT_ROOT/security-toolkit/tool-08-session-analyzer/backend" ]; then
    start_backend "Session Analyzer" "$PROJECT_ROOT/security-toolkit/tool-08-session-analyzer/backend" "5008"
fi

# Tool 9: Web Crawler
if [ -d "$PROJECT_ROOT/security-toolkit/tool-09-web-crawler/backend" ]; then
    start_backend "Web Crawler" "$PROJECT_ROOT/security-toolkit/tool-09-web-crawler/backend" "5009"
fi

# Tool 10: SSL/TLS Scanner
if [ -d "$PROJECT_ROOT/security-toolkit/tool-10-ssl-tls-scanner/backend" ]; then
    start_backend "SSL/TLS Scanner" "$PROJECT_ROOT/security-toolkit/tool-10-ssl-tls-scanner/backend" "5010"
fi

# Tool 11: Port Scanner
if [ -d "$PROJECT_ROOT/security-toolkit/tool-11-port-scanner/backend" ]; then
    start_backend "Port Scanner" "$PROJECT_ROOT/security-toolkit/tool-11-port-scanner/backend" "5011"
fi

# Tool 12: DNS Analyzer
if [ -d "$PROJECT_ROOT/security-toolkit/tool-12-dns-analyzer/backend" ]; then
    start_backend "DNS Analyzer" "$PROJECT_ROOT/security-toolkit/tool-12-dns-analyzer/backend" "5012"
fi

# Tool 13: File Upload Tester
if [ -d "$PROJECT_ROOT/security-toolkit/tool-13-file-upload-tester/backend" ]; then
    start_backend "File Upload Tester" "$PROJECT_ROOT/security-toolkit/tool-13-file-upload-tester/backend" "5013"
fi

# Tool 14: CSRF Tester
if [ -d "$PROJECT_ROOT/security-toolkit/tool-14-csrf-tester/backend" ]; then
    start_backend "CSRF Tester" "$PROJECT_ROOT/security-toolkit/tool-14-csrf-tester/backend" "5014"
fi

# Tool 15: XXE Scanner
if [ -d "$PROJECT_ROOT/security-toolkit/tool-15-xxe-scanner/backend" ]; then
    start_backend "XXE Scanner" "$PROJECT_ROOT/security-toolkit/tool-15-xxe-scanner/backend" "5015"
fi

# Tool 16: Business Logic Tester
if [ -d "$PROJECT_ROOT/security-toolkit/tool-16-business-logic-tester/backend" ]; then
    start_backend "Business Logic Tester" "$PROJECT_ROOT/security-toolkit/tool-16-business-logic-tester/backend" "5016"
fi

# Tool 17: Command Injection Scanner
if [ -d "$PROJECT_ROOT/security-toolkit/tool-17-command-injection-scanner/backend" ]; then
    start_backend "Command Injection Scanner" "$PROJECT_ROOT/security-toolkit/tool-17-command-injection-scanner/backend" "5017"
fi

# Wait for backends to initialize
sleep 2

# Start Frontend
TERMINAL_COUNT=$((TERMINAL_COUNT + 1))
echo -e "${YELLOW}[${TERMINAL_COUNT}/${TERMINAL_COUNT}]${NC} Starting Frontend..."

gnome-terminal --title="Portfolio Frontend - Port 5173" -- bash -c "
    cd '${PROJECT_ROOT}'
    echo '⚛️ Starting React Frontend...'
    echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
    npm run dev
    exec bash
"

sleep 2

# Summary
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                           ║${NC}"
echo -e "${GREEN}║        ✅ ALL SERVICES STARTED SUCCESSFULLY!               ║${NC}"
echo -e "${GREEN}║                                                           ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}📍 SERVICES RUNNING:${NC}"
echo -e "${BLUE}   Frontend:          http://localhost:5173${NC}"

# List active backends
if [ -d "$PROJECT_ROOT/security-toolkit/tool-1-vulnerability-scanner/backend" ]; then
    echo -e "${BLUE}   Code Analyzer:     http://localhost:5001${NC}"
fi
if [ -d "$PROJECT_ROOT/security-toolkit/tool-2-sql-injection-tester/backend" ]; then
    echo -e "${BLUE}   SQL Tester:        http://localhost:5002${NC}"
fi
if [ -d "$PROJECT_ROOT/security-toolkit/tool-3-xss-scanner/backend" ]; then
    echo -e "${BLUE}   XSS Scanner:       http://localhost:5003${NC}"
fi
if [ -d "$PROJECT_ROOT/security-toolkit/tool-04-api-security-tester/backend" ]; then
    echo -e "${BLUE}   API Security:      http://localhost:5004${NC}"
fi
if [ -d "$PROJECT_ROOT/security-toolkit/tool-05-jwt-analyzer/backend" ]; then
    echo -e "${BLUE}   JWT Analyzer:      http://localhost:5005${NC}"
fi
if [ -d "$PROJECT_ROOT/security-toolkit/tool-06-authentication-analyzer/backend" ]; then
    echo -e "${BLUE}   Auth Analyzer:     http://localhost:5006${NC}"
fi
if [ -d "$PROJECT_ROOT/security-toolkit/tool-07-oauth-security-tester/backend" ]; then
    echo -e "${BLUE}   OAuth Tester:      http://localhost:5007${NC}"
fi
if [ -d "$PROJECT_ROOT/security-toolkit/tool-08-session-analyzer/backend" ]; then
    echo -e "${BLUE}   Session Analyzer:  http://localhost:5008${NC}"
fi
if [ -d "$PROJECT_ROOT/security-toolkit/tool-09-web-crawler/backend" ]; then
    echo -e "${BLUE}   Web Crawler:       http://localhost:5009${NC}"
fi
if [ -d "$PROJECT_ROOT/security-toolkit/tool-10-ssl-tls-scanner/backend" ]; then
    echo -e "${BLUE}   SSL/TLS Scanner:   http://localhost:5010${NC}"
fi
if [ -d "$PROJECT_ROOT/security-toolkit/tool-11-port-scanner/backend" ]; then
    echo -e "${BLUE}   Port Scanner:      http://localhost:5011${NC}"
fi
if [ -d "$PROJECT_ROOT/security-toolkit/tool-12-dns-analyzer/backend" ]; then
    echo -e "${BLUE}   DNS Analyzer:      http://localhost:5012${NC}"
fi
if [ -d "$PROJECT_ROOT/security-toolkit/tool-13-file-upload-tester/backend" ]; then
    echo -e "${BLUE}   File Upload:       http://localhost:5013${NC}"
fi
if [ -d "$PROJECT_ROOT/security-toolkit/tool-14-csrf-tester/backend" ]; then
    echo -e "${BLUE}   CSRF Tester:       http://localhost:5014${NC}"
fi
if [ -d "$PROJECT_ROOT/security-toolkit/tool-15-xxe-scanner/backend" ]; then
    echo -e "${BLUE}   XXE Scanner:       http://localhost:5015${NC}"
fi
if [ -d "$PROJECT_ROOT/security-toolkit/tool-16-business-logic-tester/backend" ]; then
    echo -e "${BLUE}   Business Logic:    http://localhost:5016${NC}"
fi
if [ -d "$PROJECT_ROOT/security-toolkit/tool-17-command-injection-scanner/backend" ]; then
    echo -e "${BLUE}   Command Injection: http://localhost:5017${NC}"
fi

echo ""
echo -e "${YELLOW}📖 USAGE:${NC}"
echo -e "   1. Open: ${CYAN}http://localhost:5173${NC}"
echo -e "   2. Navigate to ${CYAN}Security Tools${NC} section"
echo -e "   3. Click ${CYAN}Code Analyzer${NC} to test"
echo ""
echo -e "${RED}⚠️  To stop all services: Press Ctrl+C in each terminal${NC}"
echo ""

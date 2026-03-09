#!/bin/bash

# Run all 17 backends in ONE terminal using background processes

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "============================================================"
echo "🔐 STARTING ALL 17 SECURITY TOOL BACKENDS"
echo "============================================================"
echo ""

# Function to start backend in background
start_backend() {
    local TOOL_NAME=$1
    local BACKEND_PATH=$2
    local PORT=$3
    
    echo "[$PORT] Starting $TOOL_NAME..."
    cd "$BACKEND_PATH"
    python3 app.py > /dev/null 2>&1 &
    echo $! >> "$PROJECT_ROOT/.backend_pids"
    sleep 0.3
}

# Clean old PID file
rm -f "$PROJECT_ROOT/.backend_pids"

# Start all 17 backends
start_backend "Code Analyzer" "$PROJECT_ROOT/security-toolkit/tool-1-vulnerability-scanner/backend" "5001"
start_backend "SQL Injection Tester" "$PROJECT_ROOT/security-toolkit/tool-2-sql-injection-tester/backend" "5002"
start_backend "XSS Scanner" "$PROJECT_ROOT/security-toolkit/tool-3-xss-scanner/backend" "5003"
start_backend "API Security Tester" "$PROJECT_ROOT/security-toolkit/tool-04-api-security-tester/backend" "5004"
start_backend "JWT Analyzer" "$PROJECT_ROOT/security-toolkit/tool-05-jwt-analyzer/backend" "5005"
start_backend "Auth Analyzer" "$PROJECT_ROOT/security-toolkit/tool-06-authentication-analyzer/backend" "5006"
start_backend "OAuth Tester" "$PROJECT_ROOT/security-toolkit/tool-07-oauth-security-tester/backend" "5007"
start_backend "Session Analyzer" "$PROJECT_ROOT/security-toolkit/tool-08-session-analyzer/backend" "5008"
start_backend "Web Crawler" "$PROJECT_ROOT/security-toolkit/tool-09-web-crawler/backend" "5009"
start_backend "SSL/TLS Scanner" "$PROJECT_ROOT/security-toolkit/tool-10-ssl-tls-scanner/backend" "5010"
start_backend "Port Scanner" "$PROJECT_ROOT/security-toolkit/tool-11-port-scanner/backend" "5011"
start_backend "DNS Analyzer" "$PROJECT_ROOT/security-toolkit/tool-12-dns-analyzer/backend" "5012"
start_backend "File Upload Tester" "$PROJECT_ROOT/security-toolkit/tool-13-file-upload-tester/backend" "5013"
start_backend "CSRF Tester" "$PROJECT_ROOT/security-toolkit/tool-14-csrf-tester/backend" "5014"
start_backend "XXE Scanner" "$PROJECT_ROOT/security-toolkit/tool-15-xxe-scanner/backend" "5015"
start_backend "Business Logic Tester" "$PROJECT_ROOT/security-toolkit/tool-16-business-logic-tester/backend" "5016"
start_backend "Command Injection Scanner" "$PROJECT_ROOT/security-toolkit/tool-17-command-injection-scanner/backend" "5017"

echo ""
echo "⏳ Waiting for backends to initialize..."
sleep 3

echo ""
echo "============================================================"
echo "✅ ALL 17 BACKENDS STARTED"
echo "============================================================"
echo ""
echo "📍 Services running on ports 5001-5017"
echo "📍 Health check: curl http://localhost:5001/health"
echo ""

# Start frontend in new terminal
echo "🚀 Starting frontend in new terminal..."
gnome-terminal --title="Portfolio Frontend - Port 5173" -- bash -c "
    cd '$PROJECT_ROOT'
    echo '⚛️ Starting React Frontend...'
    echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
    npm run dev
    exec bash
"

sleep 1
echo "✅ Frontend started on http://localhost:5173"
echo ""
echo "⚠️  To stop all backends: bash stop-all-backends.sh"
echo "⚠️  Or press Ctrl+C and run: kill \$(cat .backend_pids)"
echo ""
echo "Logs are suppressed. Backends running in background."
echo "Press Ctrl+C to exit (backends will keep running)"
echo ""

# Keep script running
tail -f /dev/null

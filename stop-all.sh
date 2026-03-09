#!/bin/bash

# Stop all backend processes

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "============================================================"
echo "🛑 STOPPING ALL BACKENDS"
echo "============================================================"
echo ""

if [ -f "$PROJECT_ROOT/.backend_pids" ]; then
    echo "📍 Stopping backend processes..."
    while read pid; do
        kill $pid 2>/dev/null && echo "  ✅ Stopped PID $pid" || echo "  ⚠️  PID $pid not found"
    done < "$PROJECT_ROOT/.backend_pids"
    rm -f "$PROJECT_ROOT/.backend_pids"
else
    echo "⚠️  No PID file found. Stopping all python3 app.py processes..."
    pkill -f "python3 app.py"
fi

echo ""
echo "📍 Stopping frontend..."
pkill -f "npm run dev"

echo ""
echo "✅ All backends and frontend stopped"
echo ""

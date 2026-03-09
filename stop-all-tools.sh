#!/bin/bash

# Stop All Security Toolkit Services

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${RED}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${RED}║                                                           ║${NC}"
echo -e "${RED}║        🛑 STOPPING ALL SECURITY TOOLKIT SERVICES         ║${NC}"
echo -e "${RED}║                                                           ║${NC}"
echo -e "${RED}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${YELLOW}🔍 Finding running processes...${NC}"

# Kill all Python backend processes
PYTHON_PIDS=$(pgrep -f "python3 app.py")
if [ -n "$PYTHON_PIDS" ]; then
    echo -e "${YELLOW}📍 Stopping backend services...${NC}"
    pkill -f "python3 app.py"
    sleep 1
    echo -e "${GREEN}✅ All backend services stopped${NC}"
else
    echo -e "${YELLOW}⚠️  No backend services running${NC}"
fi

# Kill npm dev server
NPM_PIDS=$(pgrep -f "npm run dev")
if [ -n "$NPM_PIDS" ]; then
    echo -e "${YELLOW}📍 Stopping frontend service...${NC}"
    pkill -f "npm run dev"
    sleep 1
    echo -e "${GREEN}✅ Frontend service stopped${NC}"
else
    echo -e "${YELLOW}⚠️  No frontend service running${NC}"
fi

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                           ║${NC}"
echo -e "${GREEN}║        ✅ ALL SERVICES STOPPED SUCCESSFULLY               ║${NC}"
echo -e "${GREEN}║                                                           ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

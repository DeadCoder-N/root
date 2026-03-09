#!/bin/bash

# Restart All Security Toolkit Services

CYAN='\033[0;36m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                                                           ║${NC}"
echo -e "${CYAN}║        🔄 RESTARTING ALL SECURITY TOOLKIT SERVICES       ║${NC}"
echo -e "${CYAN}║                                                           ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Stop all services
echo -e "${YELLOW}🛑 Stopping existing services...${NC}"
bash "$PROJECT_ROOT/stop-all-tools.sh"

sleep 2

# Start all services
echo ""
echo -e "${GREEN}🚀 Starting all services...${NC}"
bash "$PROJECT_ROOT/start-all-tools.sh"

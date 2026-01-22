#!/bin/bash

# ==============================================================================
# PROMETHEUS-CORE v3.1 :: DEPLOYMENT SCRIPT
# AUTHORITY: Dva.13 | STATUS: AUTOMATED
# ==============================================================================

# COLORS
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}[*] INITIALIZING PROMETHEUS DEPLOYMENT PROTOCOL...${NC}"

# 1. PRE-FLIGHT CHECK: ROOT PRIVILEGES
if [ "$EUID" -ne 0 ]; then 
  echo -e "${RED}[!] Please run as root (sudo ./deploy_prometheus.sh)${NC}"
  exit 1
fi

# 2. PRE-FLIGHT CHECK: CONFIGURATION AUDIT
APP_FILE="./genesis_gui/src/App.jsx"
if grep -q 'const API_URL = "";' "$APP_FILE"; then
    echo -e "${YELLOW}[WARNING] API_URL is set to empty string (Local Mode).${NC}"
    echo -e "${YELLOW}          For VPS Deployment, this implies you are using a Reverse Proxy.${NC}"
    echo -e "${YELLOW}          If you want Direct Connect, edit src/App.jsx and set your VPS IP.${NC}"
    read -p "Continue with Local/Proxy Mode? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}[ABORT] Deployment Cancelled. Please edit src/App.jsx.${NC}"
        exit 1
    fi
fi

# 3. SYSTEM UPDATE & DEPENDENCIES
echo -e "${GREEN}[*] Updating System Dependencies...${NC}"
apt-get update && apt-get upgrade -y
apt-get install -y docker.io docker-compose git nodejs npm unzip

# 4. FIREWALL CONFIGURATION (UFW)
echo -e "${GREEN}[*] Configuring Firewall (UFW)...${NC}"
ufw allow 3000/tcp
ufw allow 5000/tcp
ufw reload

# 5. DOCKER ORCHESTRATION
echo -e "${GREEN}[*] Building Docker Containers...${NC}"
docker-compose down # Clean up old containers
docker-compose up --build -d

# 6. VERIFICATION
echo -e "${GREEN}[*] Verifying Deployment...${NC}"
sleep 5
docker ps

echo -e "${GREEN}====================================================${NC}"
echo -e "${GREEN}   PROMETHEUS-CORE DEPLOYED SUCCESSFULLY            ${NC}"
echo -e "${GREEN}====================================================${NC}"
echo -e "Frontend: http://$(curl -s ifconfig.me):3000"
echo -e "Backend:  http://$(curl -s ifconfig.me):5000"
echo -e "Status:   OPERATIONAL"

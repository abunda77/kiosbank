#!/bin/bash
# ============================================================
# KIOSBANK VPS Deployment Script
# Quick deployment script untuk VPS Linux
# ============================================================

echo "============================================================"
echo "KIOSBANK VPS Deployment Script"
echo "============================================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo -e "${YELLOW}Warning: Running as root. Consider using a regular user.${NC}"
fi

# 1. Update system
echo -e "${GREEN}[1/7] Updating system packages...${NC}"
sudo apt update && sudo apt upgrade -y

# 2. Install Python 3 and pip
echo -e "${GREEN}[2/7] Installing Python 3 and pip...${NC}"
sudo apt install -y python3 python3-pip python3-venv

# 3. Install SSH client (if not already installed)
echo -e "${GREEN}[3/7] Installing SSH client...${NC}"
sudo apt install -y openssh-client

# 4. Create project directory
echo -e "${GREEN}[4/7] Creating project directory...${NC}"
PROJECT_DIR="$HOME/kisobank"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# 5. Create virtual environment
echo -e "${GREEN}[5/7] Creating Python virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# 6. Install dependencies
echo -e "${GREEN}[6/7] Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install requests urllib3 PySocks

# 7. Setup .env file
echo -e "${GREEN}[7/7] Setting up environment configuration...${NC}"
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cat > .env << 'EOF'
# ============================================================
# KIOSBANK API Configuration
# ============================================================

# VPS Configuration
VPS_IP=your_vps_ip_here
VPS_USER=your_vps_username

# Proxy Configuration
USE_PROXY=True
PROXY_HOST=127.0.0.1
PROXY_PORT=1080

# KIOSBANK API Credentials
KIOSBANK_API_URL=https://api.kiosbank.com/endpoint
KIOSBANK_API_USERNAME=your_username
KIOSBANK_API_PASSWORD=your_password

# KIOSBANK Payload
KIOSBANK_MITRA=your_mitra
KIOSBANK_ACCOUNT_ID=your_account_id
KIOSBANK_MERCHANT_ID=your_merchant_id
KIOSBANK_MERCHANT_NAME=your_merchant_name
KIOSBANK_COUNTER_ID=your_counter_id

# Registered IP (for verification)
REGISTERED_IP=your_registered_ip
EOF
    echo -e "${YELLOW}Please edit .env file with your actual credentials:${NC}"
    echo "  nano .env"
else
    echo -e "${GREEN}.env file already exists.${NC}"
fi

echo ""
echo "============================================================"
echo -e "${GREEN}Deployment Complete!${NC}"
echo "============================================================"
echo ""
echo "Next steps:"
echo "1. Upload your project files to: $PROJECT_DIR"
echo "2. Edit .env file with your credentials:"
echo "   nano $PROJECT_DIR/.env"
echo ""
echo "3. Activate virtual environment:"
echo "   source $PROJECT_DIR/venv/bin/activate"
echo ""
echo "4. Run the CLI application:"
echo "   python3 $PROJECT_DIR/main_cli.py"
echo ""
echo "5. Or run individual scripts:"
echo "   python3 $PROJECT_DIR/app/signon_vps.py"
echo "   python3 $PROJECT_DIR/app/check_ip.py"
echo ""
echo "============================================================"

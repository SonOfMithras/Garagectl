#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Garagectl Installer ===${NC}"

# 1. System Dependency Check (Debian/Raspbian only)
if command -v apt-get &> /dev/null; then
    echo -e "${YELLOW}[INFO] Debian-based system detected. Updating system packages...${NC}"
    sudo apt-get update
    echo -e "${YELLOW}[INFO] Installing system dependencies (git, python3-venv)...${NC}"
    sudo apt-get install -y git python3-venv
else
    echo -e "${YELLOW}[WARN] Not a Debian-based system (apt-get not found).${NC}"
    echo -e "${YELLOW}[WARN] Skipping system package installation. Please ensure 'python3' and 'git' are installed manually.${NC}"
fi

# 2. Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] Python 3 could not be found. Please install it to proceed.${NC}"
    exit 1
fi

# 3. Setup Virtual Environment
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}[INFO] Creating Python virtual environment in $VENV_DIR...${NC}"
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR] Failed to create virtual environment. Ensure python3-venv is installed.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}[OK] Virtual environment exists.${NC}"
fi

# 4. Install Python Dependencies
echo -e "${YELLOW}[INFO] Installing Python dependencies from requirements.txt...${NC}"
source "$VENV_DIR/bin/activate"

# Upgrade pip first
pip install --upgrade pip

# Install requirements
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}[SUCCESS] Dependencies installed successfully!${NC}"
    else
        echo -e "${RED}[ERROR] Failed to install dependencies.${NC}"
        exit 1
    fi
else
    echo -e "${RED}[ERROR] requirements.txt not found!${NC}"
    exit 1
fi

echo -e "\n${GREEN}=== Service Installation ===${NC}"
read -p "Do you want to install and enable the systemd service? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    SERVICE_NAME="garagectl"
    SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
    CURRENT_USER=$(whoami)
    PROJECT_DIR=$(pwd)
    VENV_PYTHON="${PROJECT_DIR}/${VENV_DIR}/bin/python"

    echo -e "${YELLOW}[INFO] Creating service file for user '${CURRENT_USER}' in '${PROJECT_DIR}'...${NC}"

    # Create temporary service file
    cat <<EOF > /tmp/${SERVICE_NAME}.service
[Unit]
Description=Garage Door Automation
After=network.target

[Service]
User=${CURRENT_USER}
WorkingDirectory=${PROJECT_DIR}
Environment="PATH=${PROJECT_DIR}/${VENV_DIR}/bin"
ExecStart=${VENV_PYTHON} app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

    echo -e "${YELLOW}[INFO] Installing service to ${SERVICE_FILE} (requires sudo)...${NC}"
    
    if sudo mv /tmp/${SERVICE_NAME}.service ${SERVICE_FILE}; then
        echo -e "${GREEN}[OK] Service file created.${NC}"
        
        echo -e "${YELLOW}[INFO] Enabling and starting service...${NC}"
        sudo systemctl daemon-reload
        sudo systemctl enable ${SERVICE_NAME}.service
        sudo systemctl start ${SERVICE_NAME}.service
        
        if [ $? -eq 0 ]; then
             echo -e "${GREEN}[SUCCESS] Service installed and started!${NC}"
        else
             echo -e "${RED}[ERROR] Failed to start service.${NC}"
        fi
    else
        echo -e "${RED}[ERROR] Failed to move service file. Do you have sudo privileges?${NC}"
        rm /tmp/${SERVICE_NAME}.service
    fi
else
    echo -e "${YELLOW}[INFO] Service installation skipped.${NC}"
fi

echo -e "\n${GREEN}=== Installation Complete! ===${NC}"
echo -e "To start the application manually, run:"
echo -e "  ${YELLOW}./${VENV_DIR}/bin/python app.py${NC}"
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "To check service status:"
    echo -e "  ${YELLOW}sudo systemctl status ${SERVICE_NAME}.service${NC}"
fi

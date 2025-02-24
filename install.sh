#!/bin/bash

# 🚀 OSINTEL INSTALLATION SCRIPT 🚀
# Fully Interactive, Automated & Graphically Enhanced Installation for Ubuntu/Debian

# Define UI Colors
CYAN='\033[1;36m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
RED='\033[1;31m'
NC='\033[0m' # No color

# 1️⃣ **CLEAR TERMINAL & DISPLAY OSINTEL BANNER**
clear
echo -e "${CYAN}"
echo "------------------------------------------------------------"
echo "   🔍 OSINTEL - Law Enforcement OSINT Toolkit"
echo "------------------------------------------------------------"
echo -e "${NC}"
sleep 2

# Progress Bar Function with Status Message
progress_bar() {
    local current=$1
    local total=$2
    local bar_length=40
    local percent=$((current * 100 / total))
    local filled_length=$((current * bar_length / total))
    
    echo -ne "\r["
    for ((i = 0; i < filled_length; i++)); do echo -ne "█"; done
    for ((i = filled_length; i < bar_length; i++)); do echo -ne "-"; done
    echo -ne "] $percent% - $3"
}

# Detect OS Type
OS_TYPE=$(uname -s)

# 2️⃣ **CHECK SYSTEM COMPATIBILITY**
echo -e "${YELLOW}🔍 Checking system compatibility...${NC}"
progress_bar 0 5 "Checking system..."
sleep 1

# Hide apt output and install necessary packages
sudo apt update -y > /dev/null 2>&1
progress_bar 1 5 "Updating package lists..."
sleep 1

sudo apt install -y python3-full python3-pip python3-venv pipx > /dev/null 2>&1
progress_bar 2 5 "Installing Python3, pip, venv, and pipx..."
sleep 1

# 3️⃣ **CREATE & ACTIVATE VIRTUAL ENVIRONMENT**
echo -e "${YELLOW}\n⚙️ Setting up virtual environment...${NC}"
progress_bar 3 5 "Creating virtual environment..."
python3 -m venv osintel_env
source osintel_env/bin/activate
progress_bar 4 5 "Virtual environment activated."
sleep 1

# 4️⃣ **INSTALL REQUIRED PYTHON LIBRARIES WITH FIXED PROGRESS BAR**
echo -e "${YELLOW}\n📦 Installing required Python libraries...${NC}"

REQUIRED_LIBS=("cryptography" "instaloader" "requests" "telegram" "nltk" "web3" "blockcypher" "scikit-learn" "pandas" "matplotlib" "flask" "seaborn" "tensorflow" "torch" "reportlab" "opencv-python" "joblib" "beautifulsoup4" "face_recognition")

total_packages=${#REQUIRED_LIBS[@]}
current_package=0
ERRORS=()

echo -e "\n🔽 **Overall Installation Progress**"

for LIB in "${REQUIRED_LIBS[@]}"; do
    current_package=$((current_package + 1))
    progress_bar "$current_package" "$total_packages" "Installing $LIB..."
    python3 -m pip install "$LIB" --no-cache-dir > /dev/null 2>&1
    
    if [[ $? -ne 0 ]]; then
        ERRORS+=("$LIB")
    fi
done

progress_bar "$total_packages" "$total_packages" "Installation Complete!"
echo ""

# 5️⃣ **DISPLAY ERROR TABLE IF ANY LIBRARY FAILED**
if [ ${#ERRORS[@]} -ne 0 ]; then
    echo -e "\n${RED}❌ Some dependencies failed to install:${NC}"
    echo -e "${YELLOW}--------------------------------------------------${NC}"
    printf "${RED}%-25s %-30s${NC}\n" "Library" "Status"
    echo -e "${YELLOW}--------------------------------------------------${NC}"
    for ERROR in "${ERRORS[@]}"; do
        printf "${RED}%-25s %-30s${NC}\n" "$ERROR" "❌ Failed"
    done
    echo -e "${YELLOW}--------------------------------------------------${NC}"
else
    echo -e "${GREEN}✅ All dependencies installed successfully!${NC}"
fi

# 6️⃣ **FINAL VERIFICATION & START OSINTEL**
echo -e "${GREEN}✅ Installation complete. Run 'python3 core.py' anytime to start OSINTEL.${NC}"

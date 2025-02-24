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

# Progress Bar Function
progress_bar() {
    local progress=$1
    local bar_length=40
    local filled_length=$((progress * bar_length / 100))
    
    echo -ne "["
    for ((i = 0; i < filled_length; i++)); do echo -ne "█"; done
    for ((i = filled_length; i < bar_length; i++)); do echo -ne "-"; done
    echo -ne "] $progress% \r"
}

# Detect OS Type
OS_TYPE=$(uname -s)

# 2️⃣ **CHECK SYSTEM COMPATIBILITY**
echo -e "${YELLOW}🔍 Checking system compatibility...${NC}"
progress_bar 10
sleep 1

# Hide apt output and install necessary packages
sudo apt update -y > /dev/null 2>&1
sudo apt install -y python3-full python3-pip python3-venv pipx > /dev/null 2>&1

# 3️⃣ **CREATE & ACTIVATE VIRTUAL ENVIRONMENT**
echo -e "${YELLOW}⚙️ Setting up virtual environment...${NC}"
progress_bar 30
python3 -m venv osintel_env
source osintel_env/bin/activate
echo -e "${GREEN}✅ Virtual environment activated.${NC}"
sleep 1

# 4️⃣ **INSTALL REQUIRED PYTHON LIBRARIES WITH FIXED PROGRESS BAR**
echo -e "${YELLOW}📦 Installing required Python libraries...${NC}"

REQUIRED_LIBS=("cryptography" "instaloader" "requests" "telegram" "nltk" "web3" "blockcypher" "scikit-learn" "pandas" "matplotlib" "flask" "seaborn" "tensorflow" "torch" "reportlab" "opencv-python" "joblib" "beautifulsoup4" "face_recognition")

total_packages=${#REQUIRED_LIBS[@]}
progress_per_package=$((100 / total_packages))

install_progress=30
bar_length=50
ERRORS=()

echo -e "\n🔽 **Overall Installation Progress**"
progress_bar $install_progress

for LIB in "${REQUIRED_LIBS[@]}"; do
    progress_bar $install_progress
    sleep 0.2
    python3 -m pip install "$LIB" --no-cache-dir > /dev/null 2>&1
    
    if [[ $? -eq 0 ]]; then
        progress_bar $((install_progress + progress_per_package))
    else
        ERRORS+=("$LIB")
    fi
    
    ((install_progress += progress_per_package))
done
progress_bar 100
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

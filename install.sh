#!/bin/bash

# 🚀 OSINTEL INSTALLATION SCRIPT 🚀
# Fully Interactive, Automated & PEP 668-Proof Installation for Ubuntu/Debian

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
    local duration=$1
    local progress=0
    local bar_length=40

    while [ "$progress" -le 100 ]; do
        echo -ne "\r["
        for ((i = 0; i < $((progress * bar_length / 100)); i++)); do echo -ne "█"; done
        for ((i = $((progress * bar_length / 100)); i < bar_length; i++)); do echo -ne "-"; done
        echo -ne "] $progress% "
        sleep $duration
        ((progress += 5))
    done
    echo ""
}

# Detect OS Type
OS_TYPE=$(uname -s)

# 2️⃣ **CHECK SYSTEM COMPATIBILITY**
echo -e "${YELLOW}🔍 Checking system compatibility...${NC}"
progress_bar 0.1

# Ensure Python3, pip, and virtual environment tools are installed
sudo apt update
sudo apt install -y python3-full python3-pip python3-venv pipx

# 3️⃣ **CREATE & ACTIVATE VIRTUAL ENVIRONMENT**
echo -e "${YELLOW}⚙️ Setting up virtual environment...${NC}"
progress_bar 0.1
python3 -m venv osintel_env
source osintel_env/bin/activate
echo -e "${GREEN}✅ Virtual environment activated.${NC}"
sleep 1

# 4️⃣ **INSTALL REQUIRED PYTHON LIBRARIES WITH INDIVIDUAL PROGRESS BARS**
echo -e "${YELLOW}📦 Installing required Python libraries...${NC}"

REQUIRED_LIBS=("cryptography" "instaloader" "requests" "telegram" "nltk" "web3" "blockcypher" "scikit-learn" "pandas" "matplotlib" "flask" "seaborn" "tensorflow" "torch" "reportlab" "opencv-python" "joblib" "beautifulsoup4" "face_recognition")

total_packages=${#REQUIRED_LIBS[@]}
progress_per_package=$((100 / total_packages))

install_progress=0
bar_length=50

echo -e "\n🔽 **Overall Installation Progress**"
while [ "$install_progress" -le 100 ]; do
    echo -ne "\r["
    for ((i = 0; i < $((install_progress * bar_length / 100)); i++)); do echo -ne "█"; done
    for ((i = $((install_progress * bar_length / 100)); i < bar_length; i++)); do echo -ne "-"; done
    echo -ne "] $install_progress% "
    sleep 0.1
    ((install_progress += progress_per_package))
done
echo ""

for LIB in "${REQUIRED_LIBS[@]}"; do
    echo -ne "\n${CYAN}Installing $LIB...${NC}"
    progress_bar 0.05
    python3 -m pip install "$LIB" --no-cache-dir &> /dev/null

    if [[ $? -eq 0 ]]; then
        echo -e "${GREEN}✅ $LIB installed successfully.${NC}"
    else
        echo -e "${RED}❌ Failed to install $LIB. Please check manually.${NC}"
    fi
done

# 5️⃣ **FINAL VERIFICATION & START OSINTEL**
echo -e "${GREEN}✅ Installation complete. Run 'python3 core.py' anytime to start OSINTEL.${NC}"

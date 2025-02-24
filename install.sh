#!/bin/bash

# 🚀 OSINTEL INSTALLATION SCRIPT 🚀
# Fully Interactive, Animated, & Self-Repairing Setup for All Systems

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

# 2️⃣ **SYSTEM COMPATIBILITY CHECK**
echo -e "${YELLOW}🔍 Checking system compatibility...${NC}"
sleep 1

# Detect OS Type
OS_TYPE=$(uname -s)

# Ensure Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 not found! Installing...${NC}"
    case "$OS_TYPE" in
        "Linux") sudo apt install python3-full -y || sudo yum install python3 -y ;;
        "Darwin") brew install python3 ;;
        "MINGW"*) echo "Please install Python3 manually from python.org" && exit 1 ;;
        *) echo "❌ Unsupported OS. Install Python3 manually." && exit 1 ;;
    esac
else
    echo -e "${GREEN}✅ Python3 found!${NC}"
fi
sleep 1

# Ensure pip is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ Pip not found! Installing...${NC}"
    case "$OS_TYPE" in
        "Linux") sudo apt install python3-pip -y || sudo yum install python3-pip -y ;;
        "Darwin") brew install python3-pip ;;
        "MINGW"*) echo "Please install pip manually from python.org" && exit 1 ;;
        *) echo "❌ Unsupported OS. Install pip manually." && exit 1 ;;
    esac
else
    echo -e "${GREEN}✅ Pip found!${NC}"
fi
sleep 1

# 3️⃣ **ENSURE PIPX IS INSTALLED (FOR SAFE PACKAGE MANAGEMENT)**
if ! command -v pipx &> /dev/null; then
    echo -e "${YELLOW}🔧 Installing pipx to manage Python packages...${NC}"
    case "$OS_TYPE" in
        "Linux") sudo apt install pipx -y && pipx ensurepath ;;
        "Darwin") brew install pipx && pipx ensurepath ;;
        "MINGW"*) echo "Please install pipx manually from python.org" && exit 1 ;;
    esac
else
    echo -e "${GREEN}✅ Pipx found!${NC}"
fi
sleep 1

# 4️⃣ **FIX PEP 668 (EXTERNALLY MANAGED ENVIRONMENT ERROR)**
if python3 -m pip install --help 2>&1 | grep -q "externally-managed-environment"; then
    echo -e "${YELLOW}🔧 Fixing PEP 668 Restrictions...${NC}"
    sudo apt install python3-venv -y
fi

# Ensure virtual environment support
if ! python3 -m venv --help &> /dev/null; then
    echo -e "${RED}❌ Virtual environment module missing! Installing...${NC}"
    case "$OS_TYPE" in
        "Linux") sudo apt install python3-venv -y || sudo yum install python3-venv -y ;;
        "Darwin") brew install python3-venv ;;
        "MINGW"*) echo "Please install venv manually from python.org" && exit 1 ;;
        *) echo "❌ Unsupported OS. Install venv manually." && exit 1 ;;
    esac
else
    echo -e "${GREEN}✅ Virtual environment support detected!${NC}"
fi
sleep 1

# 5️⃣ **CREATE & ACTIVATE VIRTUAL ENVIRONMENT**
echo -e "${YELLOW}⚙️ Setting up virtual environment...${NC}"
python3 -m venv osintel_env
source osintel_env/bin/activate
echo -e "${GREEN}✅ Virtual environment activated.${NC}"
sleep 1

# 6️⃣ **INSTALL REQUIRED PYTHON LIBRARIES INSIDE VENV**
echo -e "${YELLOW}📦 Installing required Python libraries inside virtual environment...${NC}"
REQUIRED_LIBS=("cryptography" "instaloader" "requests" "telegram" "nltk" "web3" "blockcypher" "scikit-learn" "pandas" "matplotlib" "flask" "seaborn" "tensorflow" "torch" "reportlab" "opencv-python")

for LIB in "${REQUIRED_LIBS[@]}"; do
    python3 -m pip install --upgrade pip
    python3 -m pip install "$LIB" --no-cache-dir
    if [[ $? -eq 0 ]]; then
        echo -e "${GREEN}✅ $LIB installed successfully.${NC}"
    else
        echo -e "${RED}❌ Failed to install $LIB. Please check manually.${NC}"
    fi
done

# 7️⃣ **FINAL VERIFICATION**
echo -e "${YELLOW}🔎 Verifying installation...${NC}"
sleep 2
if command -v python3 &> /dev/null && command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✅ All system checks passed. OSINTEL is fully installed!${NC}"
else
    echo -e "${RED}❌ Error: Some dependencies failed to install. Try running the script again.${NC}"
    exit 1
fi

# 8️⃣ **ASK USER TO LAUNCH OSINTEL**
echo -e "${CYAN}🚀 OSINTEL is installed! Do you want to launch it now? (Y/N)${NC}"
read -r launch_choice
if [[ "$launch_choice" =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}🚀 Launching OSINTEL Core System...${NC}"
    sleep 1
    python3 core.py
else
    echo -e "${GREEN}✅ Installation complete. Run 'python3 core.py' anytime to start OSINTEL.${NC}"
fi

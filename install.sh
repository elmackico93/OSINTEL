#!/bin/bash

# 🚀 OSINTEL INSTALLATION SCRIPT 🚀
# Fully Interactive, Animated, & Self-Repairing Setup with English & Italian Support

# Detect System Language
LANGUAGE=$(echo $LANG | cut -d'_' -f1)

# Define Texts for English and Italian
if [ "$LANGUAGE" == "it" ]; then
    TXT_BANNER="🔍 OSINTEL - Strumento OSINT per le Forze dell'Ordine"
    TXT_CHECK_SYSTEM="🔍 Controllo della compatibilità del sistema..."
    TXT_INSTALL_PYTHON="❌ Python3 non trovato! Installazione in corso..."
    TXT_PYTHON_FOUND="✅ Python3 trovato!"
    TXT_INSTALL_PIP="❌ Pip non trovato! Installazione in corso..."
    TXT_PIP_FOUND="✅ Pip trovato!"
    TXT_INSTALL_VENV="❌ Il modulo dell'ambiente virtuale non è presente! Installazione..."
    TXT_VENV_FOUND="✅ Supporto per ambiente virtuale rilevato!"
    TXT_SETTING_VENV="⚙️ Creazione dell'ambiente virtuale..."
    TXT_VENV_ACTIVATED="✅ Ambiente virtuale attivato."
    TXT_INSTALLING_LIBS="📦 Installazione delle librerie Python richieste..."
    TXT_VERIFICATION="🔎 Verifica dell'installazione..."
    TXT_SUCCESS="✅ Tutti i controlli di sistema superati. OSINTEL è completamente installato!"
    TXT_LAUNCH_PROMPT="🚀 OSINTEL è installato! Vuoi avviarlo ora? (Y/N)"
    TXT_LAUNCHING="🚀 Avvio del sistema OSINTEL..."
    TXT_COMPLETED="✅ Installazione completata. Esegui 'python3 core.py' in qualsiasi momento per avviare OSINTEL."
    TXT_ERROR="❌ Errore: Alcune dipendenze non sono state installate. Riprova."
else
    TXT_BANNER="🔍 OSINTEL - Law Enforcement OSINT Toolkit"
    TXT_CHECK_SYSTEM="🔍 Checking system compatibility..."
    TXT_INSTALL_PYTHON="❌ Python3 not found! Installing..."
    TXT_PYTHON_FOUND="✅ Python3 found!"
    TXT_INSTALL_PIP="❌ Pip not found! Installing..."
    TXT_PIP_FOUND="✅ Pip found!"
    TXT_INSTALL_VENV="❌ Virtual environment module missing! Installing..."
    TXT_VENV_FOUND="✅ Virtual environment support detected!"
    TXT_SETTING_VENV="⚙️ Setting up virtual environment..."
    TXT_VENV_ACTIVATED="✅ Virtual environment activated."
    TXT_INSTALLING_LIBS="📦 Installing required Python libraries..."
    TXT_VERIFICATION="🔎 Verifying installation..."
    TXT_SUCCESS="✅ All system checks passed. OSINTEL is fully installed!"
    TXT_LAUNCH_PROMPT="🚀 OSINTEL is installed! Do you want to launch it now? (Y/N)"
    TXT_LAUNCHING="🚀 Launching OSINTEL Core System..."
    TXT_COMPLETED="✅ Installation complete. Run 'python3 core.py' anytime to start OSINTEL."
    TXT_ERROR="❌ Error: Some dependencies failed to install. Try running the script again."
fi

# Define colors for a professional UI
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No color

# Clear the terminal
clear

# Display OSINTEL Banner
echo -e "${CYAN}"
echo "------------------------------------------------------------"
echo "   $TXT_BANNER"
echo "------------------------------------------------------------"
echo -e "${NC}"
sleep 2

# Function for animated progress bar
progress_bar() {
    local duration=${1}
    already_done() { for ((done=0; done<$elapsed; done++)); do printf "▇"; done }
    remaining() { for ((remain=$elapsed; remain<$duration; remain++)); do printf " "; done }
    percentage() { printf "| %s%%" $(( (($elapsed)*100)/($duration)*100/100 )); }
    for ((elapsed=1; elapsed<=$duration; elapsed++)); do
        already_done; remaining; percentage
        sleep 0.1
        printf "\r"
    done
    printf "\n"
}

echo -e "${YELLOW}$TXT_CHECK_SYSTEM${NC}"
progress_bar 30

# Check Python3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}$TXT_INSTALL_PYTHON${NC}"
    sudo apt-get install python3 -y
else
    echo -e "${GREEN}$TXT_PYTHON_FOUND${NC}"
fi
sleep 1

# Check Pip
if ! command -v pip &> /dev/null; then
    echo -e "${RED}$TXT_INSTALL_PIP${NC}"
    sudo apt-get install python3-pip -y
else
    echo -e "${GREEN}$TXT_PIP_FOUND${NC}"
fi
sleep 1

# Check for Virtual Environment Support
if ! python3 -m venv --help &> /dev/null; then
    echo -e "${RED}$TXT_INSTALL_VENV${NC}"
    sudo apt-get install python3-venv -y
else
    echo -e "${GREEN}$TXT_VENV_FOUND${NC}"
fi
sleep 1

# Create & Activate Virtual Environment
echo -e "${YELLOW}$TXT_SETTING_VENV${NC}"
progress_bar 20
python3 -m venv osintel_env
source osintel_env/bin/activate
echo -e "${GREEN}$TXT_VENV_ACTIVATED${NC}"
sleep 1

# Define required dependencies
REQUIRED_LIBS=("instaloader" "requests" "telegram" "face_recognition" "nltk" "web3" "blockcypher" "scikit-learn" "pandas" "matplotlib" "flask" "seaborn" "tensorflow" "torch" "reportlab" "opencv-python")

# Install Dependencies
echo -e "${YELLOW}$TXT_INSTALLING_LIBS${NC}"
for LIB in "${REQUIRED_LIBS[@]}"; do
    python3 -c "import $LIB" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo -e "${CYAN}📥 Installing $LIB...${NC}"
        pip install $LIB
    else
        echo -e "${GREEN}✅ $LIB already installed.${NC}"
    fi
done

# Final Verification
echo -e "${YELLOW}$TXT_VERIFICATION${NC}"
progress_bar 15
if command -v python3 &> /dev/null && command -v pip &> /dev/null; then
    echo -e "${GREEN}$TXT_SUCCESS${NC}"
else
    echo -e "${RED}$TXT_ERROR${NC}"
    exit 1
fi

# Ask user if they want to launch OSINTEL Core System
echo -e "${CYAN}$TXT_LAUNCH_PROMPT${NC}"
read -r launch_choice
if [[ "$launch_choice" =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}$TXT_LAUNCHING${NC}"
    sleep 1
    python3 core.py
else
    echo -e "${GREEN}$TXT_COMPLETED${NC}"
fi

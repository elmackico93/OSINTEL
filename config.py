import os
import json
import base64
import cryptography
from cryptography.fernet import Fernet

# 1️⃣ **CONFIGURATION FILE PATHS**
CONFIG_FILE = "config.json"
ENCRYPTION_KEY_FILE = "encryption.key"

# 2️⃣ **ENCRYPTION HANDLING**
def generate_encryption_key():
    """Generates and saves an encryption key for securing credentials."""
    key = Fernet.generate_key()
    with open(ENCRYPTION_KEY_FILE, "wb") as f:
        f.write(key)
    return key

def load_encryption_key():
    """Loads encryption key, generates one if missing."""
    if not os.path.exists(ENCRYPTION_KEY_FILE):
        return generate_encryption_key()
    with open(ENCRYPTION_KEY_FILE, "rb") as f:
        return f.read()

def encrypt_value(value, key):
    """Encrypts a given value using Fernet encryption."""
    return Fernet(key).encrypt(value.encode()).decode() if value else ""

def decrypt_value(value, key):
    """Decrypts an encrypted value using Fernet encryption."""
    try:
        return Fernet(key).decrypt(value.encode()).decode() if value else ""
    except:
        print("❌ Error: Unable to decrypt credentials. Please reconfigure.")
        return None

# 3️⃣ **DEFAULT CONFIGURATION WITH OPTIONAL & REQUIRED KEYS**
DEFAULT_CONFIG = {
    "telegram": {
        "bot_token": "",   # OPTIONAL
        "chat_id": ""      # OPTIONAL
    },
    "api_keys": {
        "blockcypher": "",  # REQUIRED for Crypto Tracking
        "face_recognition": "",  # REQUIRED for Facial Recognition
        "nltk": ""  # REQUIRED for AI-Based Text Analysis
    },
    "system": {
        "language": "en",
        "debug_mode": False
    }
}

# 4️⃣ **LOAD CONFIGURATION & DECRYPT API KEYS**
def load_config():
    """Loads and decrypts the configuration file."""
    print("🔍 Loading OSINTEL configuration...")

    encryption_key = load_encryption_key()

    if not os.path.exists(CONFIG_FILE):
        print("⚠️ Config file missing! Creating a new one...")
        save_config(DEFAULT_CONFIG, encryption_key)
        return DEFAULT_CONFIG

    try:
        with open(CONFIG_FILE, "r") as f:
            config_data = json.load(f)

        # Decrypt API Keys
        for key, value in config_data["api_keys"].items():
            if value:
                config_data["api_keys"][key] = decrypt_value(value, encryption_key)

        print("✅ Configuration successfully loaded!")
        return config_data

    except (json.JSONDecodeError, KeyError):
        print("❌ Invalid config format! Resetting to default.")
        save_config(DEFAULT_CONFIG, encryption_key)
        return DEFAULT_CONFIG

# 5️⃣ **SAVE CONFIGURATION**
def save_config(config_data, encryption_key):
    """Encrypts API keys and saves the configuration file."""
    print("💾 Saving OSINTEL configuration...")

    for key, value in config_data["api_keys"].items():
        if value:
            config_data["api_keys"][key] = encrypt_value(value, encryption_key)

    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=4)

# 6️⃣ **VALIDATE CONFIGURATION (ENSURE REQUIRED KEYS ARE PRESENT)**
def validate_config(config_data):
    """Checks if required API keys are present and warns about optional ones."""
    missing_required_keys = [key for key, value in config_data["api_keys"].items() if not value]
    missing_optional_keys = [key for key, value in config_data["telegram"].items() if not value]

    if missing_required_keys:
        print("⚠️ WARNING: Some required API keys are missing!")
        print("❌ Missing Required Keys:", ", ".join(missing_required_keys))
        print("OSINTEL will run, but some modules may not function correctly.")

    if missing_optional_keys:
        print("🔔 NOTICE: Some optional features (e.g., Telegram alerts) are not configured.")
        print("Optional Missing Keys:", ", ".join(missing_optional_keys))

    if not missing_required_keys:
        print("✅ All required API keys verified!")

# 7️⃣ **STATIC CREDENTIAL REFERENCE FOR MODULES**
class OSINTELConfig:
    """Provides static references to configuration data."""
    _config_data = load_config()

    # OPTIONAL CREDENTIALS
    TELEGRAM_BOT_TOKEN = _config_data["telegram"].get("bot_token", "")
    TELEGRAM_CHAT_ID = _config_data["telegram"].get("chat_id", "")

    # REQUIRED CREDENTIALS
    BLOCKCYPHER_API_KEY = _config_data["api_keys"].get("blockcypher", None)
    FACE_RECOGNITION_KEY = _config_data["api_keys"].get("face_recognition", None)
    NLTK_KEY = _config_data["api_keys"].get("nltk", None)

    # SYSTEM SETTINGS
    LANGUAGE = _config_data["system"]["language"]
    DEBUG_MODE = _config_data["system"]["debug_mode"]

# 8️⃣ **RUN CONFIGURATION SETUP**
if __name__ == "__main__":
    config_data = load_config()
    validate_config(config_data)
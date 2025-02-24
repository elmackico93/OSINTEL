import os
import json
import joblib
import config
import numpy as np
import pandas as pd
import requests
import threading
import tensorflow as tf
import xgboost as xgb
import lightgbm as lgb
import catboost as cat
import torch
import transformers
from datetime import datetime
from reportlab.pdfgen import canvas
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler
from cryptography.fernet import Fernet
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process, Queue

# 1️⃣ **SECURE AI MODEL STORAGE & ENCRYPTION**
MODEL_DIR = "models/"
MODEL_FILE = f"{MODEL_DIR}cybercrime_ai_model.pkl"
ENCRYPTION_KEY_FILE = f"{MODEL_DIR}encryption.key"
DATASET_CONFIG_FILE = "models/datasets.json"

# Ensure directories exist
os.makedirs(MODEL_DIR, exist_ok=True)

# Encryption Key Handling
def generate_encryption_key():
    """Generates and saves an encryption key for securing AI models."""
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

ENCRYPTION_KEY = load_encryption_key()

def encrypt_model(model_data):
    """Encrypts an AI model using Fernet encryption."""
    return Fernet(ENCRYPTION_KEY).encrypt(model_data).decode()

def decrypt_model(model_data):
    """Decrypts an AI model using Fernet encryption."""
    try:
        return Fernet(ENCRYPTION_KEY).decrypt(model_data.encode())
    except:
        print("❌ AI Model Corrupted! Retraining...")
        return None

# 2️⃣ **DYNAMIC DATASET LOADING**
def load_datasets(category):
    """Loads dataset configurations dynamically from datasets.json based on category."""
    if not os.path.exists(DATASET_CONFIG_FILE):
        print("⚠️ Dataset configuration file missing. Run `manage_datasets.py` first.")
        return []

    with open(DATASET_CONFIG_FILE, "r") as f:
        datasets = json.load(f)["datasets"]

    return datasets.get(category, [])

def fetch_and_combine_datasets(category):
    """Fetches datasets from multiple sources dynamically and combines them efficiently."""
    dataset_list = load_datasets(category)
    combined_data = []

    print(f"🔍 Fetching {category.upper()} datasets...")

    def fetch_dataset(dataset):
        url, dataset_format, dataset_name = dataset["url"], dataset["format"], dataset["name"]
        try:
            if dataset_format == "csv":
                df = pd.read_csv(url)
                combined_data.append(df)
                print(f"✅ Loaded dataset: {dataset_name}")
            elif dataset_format == "api":
                response = requests.get(url)
                df = pd.json_normalize(response.json())
                combined_data.append(df)
                print(f"✅ Fetched API dataset: {dataset_name}")
            else:
                print(f"⚠️ Skipping non-CSV dataset: {dataset_name}")
        except Exception as e:
            print(f"⚠️ Failed to load dataset {dataset_name}: {str(e)}")

    # Multi-threaded dataset fetching for performance
    threads = []
    for dataset in dataset_list:
        thread = threading.Thread(target=fetch_dataset, args=(dataset,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

    return pd.concat(combined_data) if combined_data else None

# 3️⃣ **TRAIN OR LOAD AI MODEL (FULLY SECURE & PARALLELIZED)**
def train_new_model():
    """Trains a new Hybrid AI model using multiple AI techniques with secure updates."""
    print("🔍 Training AI Cybercrime Detection Model...")

    df_combined = fetch_and_combine_datasets("cybercrime")
    if df_combined is None:
        print("❌ No data available to train AI model!")
        return None

    # Feature Engineering & Standardization
    features = df_combined[['risk_score', 'num_transactions', 'num_blackmarket_mentions']]
    labels = df_combined['is_criminal']
    scaler = StandardScaler()
    X = scaler.fit_transform(features)
    y = labels.values

    # Train Multiple AI Models in Parallel
    models = {
        "xgboost": xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss'),
        "random_forest": RandomForestClassifier(n_estimators=100),
        "lightgbm": lgb.LGBMClassifier(),
        "catboost": cat.CatBoostClassifier(verbose=0),
        "isolation_forest": IsolationForest(n_estimators=100, contamination=0.1),
        "neural_net": tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
    }

    with ThreadPoolExecutor() as executor:
        for model_name, model in models.items():
            print(f"🔵 Training {model_name}...")
            executor.submit(model.fit, X, y)

    # Encrypt & Save the Model
    encrypted_model = encrypt_model(joblib.dumps(models))
    with open(MODEL_FILE, "wb") as f:
        f.write(encrypted_model.encode())

    print("✅ AI model trained and securely stored.")
    return models

def load_ai_model():
    """Loads or initializes an encrypted AI model securely."""
    if os.path.exists(MODEL_FILE):
        with open(MODEL_FILE, "rb") as f:
            encrypted_model_data = f.read()
        decrypted_model_data = decrypt_model(encrypted_model_data)
        if decrypted_model_data:
            return joblib.loads(decrypted_model_data)

    return train_new_model()

AI_MODELS = load_ai_model()

# 4️⃣ **AI CYBERCRIME RISK ANALYSIS (USING ALL MODELS)**
def analyze_cybercrime_risk(data):
    """Uses AI models dynamically to analyze cybercrime risk."""
    X = np.array([[data['risk_score'], data['num_transactions'], data['num_blackmarket_mentions']]])

    risk_scores = []
    with ThreadPoolExecutor() as executor:
        for model_name, model in AI_MODELS.items():
            if hasattr(model, "predict"):
                risk_scores.append(executor.submit(model.predict, X).result()[0])

    final_risk_score = sum(risk_scores) / len(risk_scores) if risk_scores else 0

    if final_risk_score > 0.8:
        print("🚨 EXTREME-RISK CYBERCRIME ACTIVITY DETECTED!")

    return final_risk_score

# 5️⃣ **RUN AI CYBERCRIME OSINT**
def run():
    """Executes the AI Cybercrime Intelligence module (Fully Dynamic, Secure, and Reliable)."""
    print("🔍 AI Cybercrime OSINT is running...")

    data = {
        "risk_score": 7,
        "num_transactions": 15,
        "num_blackmarket_mentions": 3
    }

    risk_score = analyze_cybercrime_risk(data)
    print("✅ AI Cybercrime OSINT completed.")

if __name__ == "__main__":
    run()
import os
import cv2
import json
import numpy as np
import requests
import config
import face_recognition
from datetime import datetime
from reportlab.pdfgen import canvas

FACIAL_DATA_DIR = "models/facial_data/"
KNOWN_FACES_FILE = f"{FACIAL_DATA_DIR}known_faces.json"
DATASET_CONFIG_FILE = "models/datasets.json"

# Ensure facial data directory exists
os.makedirs(FACIAL_DATA_DIR, exist_ok=True)

# 1️⃣ **LOAD FACIAL DATASETS FROM `datasets.json`**
def load_facial_datasets():
    """Loads facial recognition datasets from dataset manager."""
    if not os.path.exists(DATASET_CONFIG_FILE):
        print("❌ Dataset configuration missing! Run `manage_datasets.py` first.")
        return []

    with open(DATASET_CONFIG_FILE, "r") as f:
        datasets = json.load(f)["datasets"]

    return datasets.get("facial_recognition", [])

# 2️⃣ **DOWNLOAD AND STORE SUSPECT IMAGES**
def fetch_suspect_faces():
    """Fetches and stores images from facial recognition datasets."""
    datasets = load_facial_datasets()
    known_faces = {}

    for dataset in datasets:
        name = dataset["name"]
        url = dataset["url"]

        try:
            response = requests.get(url)
            image_path = os.path.join(FACIAL_DATA_DIR, f"{name}.jpg")

            with open(image_path, "wb") as f:
                f.write(response.content)

            known_faces[name] = {"encoding": "PLACEHOLDER_ENCODING"}
            print(f"✅ Downloaded suspect image: {name}")

        except Exception as e:
            print(f"⚠️ Failed to fetch {name}: {str(e)}")

    with open(KNOWN_FACES_FILE, "w") as f:
        json.dump(known_faces, f, indent=4)

# 3️⃣ **REAL-TIME FACIAL RECOGNITION**
def recognize_face(frame):
    """Compares detected faces with known suspects."""
    known_faces = json.load(open(KNOWN_FACES_FILE, "r"))
    unknown_encodings = face_recognition.face_encodings(frame)

    for unknown_encoding in unknown_encodings:
        for suspect, data in known_faces.items():
            known_encoding = np.array(eval(data["encoding"]))
            results = face_recognition.compare_faces([known_encoding], unknown_encoding)

            if True in results:
                print(f"🚨 MATCH FOUND: {suspect}")
                generate_face_report(suspect)
                return suspect
    
    return None

# 4️⃣ **GENERATE FACIAL RECOGNITION REPORT**
def generate_face_report(suspect_name):
    """Creates a detailed facial recognition report in PDF format."""
    filename = f"Facial_Recognition_Report_{datetime.now().strftime('%Y-%m-%d')}.pdf"
    c = canvas.Canvas(filename)

    c.drawString(100, 750, "🚨 Facial Recognition Match Report")
    c.drawString(100, 730, f"Suspect Matched: {suspect_name}")
    c.drawString(100, 710, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    c.save()
    print(f"📄 Facial Recognition Report saved as {filename}")

# 5️⃣ **RUN FACIAL RECOGNITION SYSTEM**
def run():
    """Executes the facial recognition module."""
    print("🔍 OSINTEL Facial Recognition System is running...")
    fetch_suspect_faces()

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        suspect_name = recognize_face(frame)
        if suspect_name:
            print(f"🚨 ALERT: {suspect_name} detected!")

        cv2.imshow("OSINTEL Facial Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("✅ Facial Recognition OSINT completed.")

if __name__ == "__main__":
    run()
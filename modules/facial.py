import os
import cv2
import json
import numpy as np
import requests
import config
import face_recognition
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

# UI Colors
RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
WHITE = "\033[1;37m"
RESET = "\033[0m"

# 1️⃣ **DIRECTORY SETUP**
FACIAL_DATA_DIR = "models/facial_data/"
KNOWN_FACES_FILE = f"{FACIAL_DATA_DIR}known_faces.json"
DATASET_CONFIG_FILE = "models/datasets.json"
REPORTS_DIR = "reports/"

os.makedirs(FACIAL_DATA_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# 2️⃣ **LOAD FACIAL DATASETS FROM `datasets.json`**
def load_facial_datasets():
    """Loads facial recognition datasets from dataset manager."""
    if not os.path.exists(DATASET_CONFIG_FILE):
        print(f"{RED}❌ Dataset configuration missing! Run `manage_datasets.py` first.{RESET}")
        return []

    with open(DATASET_CONFIG_FILE, "r") as f:
        datasets = json.load(f)["datasets"]

    return datasets.get("facial_recognition", [])

# 3️⃣ **DOWNLOAD AND STORE SUSPECT IMAGES**
def fetch_suspect_faces():
    """Fetches and stores images from facial recognition datasets."""
    datasets = load_facial_datasets()
    known_faces = {}

    print(f"{CYAN}🔍 Downloading suspect images from databases...{RESET}")
    
    for dataset in datasets:
        name = dataset["name"]
        url = dataset["url"]

        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                image_path = os.path.join(FACIAL_DATA_DIR, f"{name}.jpg")

                with open(image_path, "wb") as f:
                    f.write(response.content)

                known_faces[name] = {"image": image_path}
                print(f"{GREEN}✅ Downloaded suspect image: {name}{RESET}")
            else:
                print(f"{YELLOW}⚠️ Failed to fetch {name}: HTTP {response.status_code}{RESET}")

        except requests.exceptions.RequestException as e:
            print(f"{YELLOW}⚠️ Failed to fetch {name}: {str(e)}{RESET}")

    with open(KNOWN_FACES_FILE, "w") as f:
        json.dump(known_faces, f, indent=4)

# 4️⃣ **LOAD KNOWN FACES FOR MATCHING**
def load_known_faces():
    """Loads stored known faces and encodes them for facial recognition."""
    if not os.path.exists(KNOWN_FACES_FILE):
        print(f"{RED}❌ No known faces found. Downloading now...{RESET}")
        fetch_suspect_faces()

    with open(KNOWN_FACES_FILE, "r") as f:
        known_faces = json.load(f)

    encoded_faces = {}
    for name, data in known_faces.items():
        image_path = data["image"]
        if os.path.exists(image_path):
            image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(image)
            if encoding:  # Ensure encoding is not empty
                encoded_faces[name] = encoding[0]

    return encoded_faces

# 5️⃣ **REAL-TIME FACIAL RECOGNITION**
def recognize_face(frame, known_faces, tolerance=0.5):
    """Compares detected faces with known suspects with a set tolerance."""
    unknown_encodings = face_recognition.face_encodings(frame)

    for unknown_encoding in unknown_encodings:
        for suspect, known_encoding in known_faces.items():
            results = face_recognition.compare_faces([known_encoding], unknown_encoding, tolerance=tolerance)
            face_distance = face_recognition.face_distance([known_encoding], unknown_encoding)[0]

            if True in results:
                print(f"{RED}🚨 MATCH FOUND: {suspect} (Confidence: {round((1 - face_distance) * 100, 2)}%) {RESET}")
                generate_face_report(suspect)
                return suspect

    return None

# 6️⃣ **GENERATE FACIAL RECOGNITION REPORT**
def generate_face_report(suspect_name):
    """Creates a detailed facial recognition report in PDF format."""
    filename = os.path.join(REPORTS_DIR, f"Facial_Recognition_Report_{datetime.now().strftime('%Y-%m-%d')}.pdf")
    c = canvas.Canvas(filename, pagesize=letter)

    # Report Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "🚨 OSINTEL Facial Recognition Report")
    c.setFont("Helvetica", 12)
    c.drawString(100, 730, f"Suspect Matched: {suspect_name}")
    c.drawString(100, 710, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Insert Suspect Image
    known_faces = json.load(open(KNOWN_FACES_FILE, "r"))
    if suspect_name in known_faces:
        image_path = known_faces[suspect_name]["image"]
        if os.path.exists(image_path):
            suspect_image = ImageReader(image_path)
            c.drawImage(suspect_image, 100, 500, width=200, height=200)

    c.save()
    print(f"{GREEN}📄 Facial Recognition Report saved as {filename}{RESET}")

# 7️⃣ **RUN FACIAL RECOGNITION SYSTEM**
def run():
    """Executes the facial recognition module with UI improvements."""
    print(f"{CYAN}🔍 OSINTEL Facial Recognition System is starting...{RESET}")
    fetch_suspect_faces()
    known_faces = load_known_faces()

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"{RED}❌ Camera error! Make sure your webcam is connected.{RESET}")
            break

        suspect_name = recognize_face(frame, known_faces)
        if suspect_name:
            print(f"{RED}🚨 ALERT: {suspect_name} detected!{RESET}")

        cv2.imshow(f"{CYAN}🔍 OSINTEL Facial Recognition{RESET}", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"{GREEN}✅ Facial Recognition OSINT completed.{RESET}")

if __name__ == "__main__":
    run()
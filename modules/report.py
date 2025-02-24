import os
import json
import config
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

# 1️⃣ **DIRECTORY SETUP**
REPORTS_DIR = "reports/"
VISUALS_DIR = f"{REPORTS_DIR}/visuals/"
DATASET_CONFIG_FILE = "models/datasets.json"

os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(VISUALS_DIR, exist_ok=True)

# 2️⃣ **LOAD DATA FROM `datasets.json`**
def load_osint_data():
    """Loads datasets dynamically from `datasets.json` for reporting."""
    if not os.path.exists(DATASET_CONFIG_FILE):
        print("❌ Dataset configuration missing! Run `manage_datasets.py` first.")
        return {}

    with open(DATASET_CONFIG_FILE, "r") as f:
        return json.load(f)["datasets"]

# 3️⃣ **GENERATE DATA VISUALIZATIONS**
def generate_visuals(report_data, case_id):
    """Creates data visualizations for OSINT intelligence reports."""
    
    for category, datasets in report_data.items():
        dataset_count = len(datasets)
        dataset_names = [ds["name"] for ds in datasets]

        plt.figure(figsize=(8, 4))
        plt.bar(dataset_names, [1] * dataset_count, color="blue")
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("Data Source Count")
        plt.title(f"{category.upper()} Intelligence Overview")

        image_path = f"{VISUALS_DIR}{category}_{case_id}.png"
        plt.savefig(image_path, bbox_inches="tight")
        plt.close()

# 4️⃣ **GENERATE DETAILED FORENSIC REPORT (PDF)**
def generate_forensic_report(case_id, suspect_name=None, suspect_image=None):
    """Creates a comprehensive forensic intelligence report in PDF format."""

    filename = os.path.join(REPORTS_DIR, f"Forensic_Report_{case_id}.pdf")
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []

    # Report Header
    title = f"""
    🚨 OSINTEL Forensic Intelligence Report
    Case ID: {case_id}
    Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    elements.append(title)

    if suspect_name:
        elements.append(f"🔍 Suspect: {suspect_name}")

    # Load OSINT Data
    osint_data = load_osint_data()
    generate_visuals(osint_data, case_id)

    # TABLE FORMAT FOR OSINT DATA
    table_data = [["Category", "Dataset Name", "Source URL"]]
    
    for category, datasets in osint_data.items():
        for dataset in datasets:
            table_data.append([category.upper(), dataset["name"], dataset["url"]])

    table = Table(table_data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)

    # ADD VISUALS
    for category, datasets in osint_data.items():
        image_path = f"{VISUALS_DIR}{category}_{case_id}.png"
        if os.path.exists(image_path):
            elements.append(ImageReader(image_path))

    doc.build(elements)
    print(f"📄 Forensic Intelligence Report saved as {filename}")

# 5️⃣ **RUN REPORT GENERATION**
def run():
    """Executes the forensic intelligence report generator dynamically."""
    print("🔍 OSINTEL Report Generator is running...")
    
    case_id = input("Enter case ID: ").strip()
    suspect_name = input("Enter suspect name (optional): ").strip() or None
    suspect_image = input("Enter suspect image path (optional): ").strip() or None

    generate_forensic_report(case_id, suspect_name, suspect_image)
    print("✅ Report generation completed.")

if __name__ == "__main__":
    run()
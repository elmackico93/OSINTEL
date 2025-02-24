import json

DATASET_CONFIG_FILE = "models/datasets.json"

def load_datasets():
    """Loads dataset configurations dynamically."""
    if not os.path.exists(DATASET_CONFIG_FILE):
        return {}

    with open(DATASET_CONFIG_FILE, "r") as f:
        return json.load(f)["datasets"]

def save_datasets(data):
    """Saves dataset configurations."""
    with open(DATASET_CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_dataset():
    """CLI interface for adding datasets dynamically."""
    datasets = load_datasets()

    category = input("Enter dataset category (cybercrime, blockchain, social_media, facial_recognition): ").strip().lower()
    name = input("Enter dataset name: ").strip()
    url = input("Enter dataset URL: ").strip()
    dataset_format = input("Enter dataset format (csv, api, web, image): ").strip().lower()

    if category not in datasets:
        datasets[category] = []

    datasets[category].append({
        "name": name,
        "url": url,
        "format": dataset_format
    })

    save_datasets(datasets)
    print(f"✅ Dataset '{name}' added successfully!")

def run():
    """CLI menu for dataset management."""
    print("📂 OSINTEL Dataset Manager")
    print("1. Add new dataset")
    print("2. View existing datasets")
    print("3. Exit")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        add_dataset()
    elif choice == "2":
        datasets = load_datasets()
        print(json.dumps(datasets, indent=4))
    elif choice == "3":
        exit()
    else:
        print("❌ Invalid choice.")

if __name__ == "__main__":
    run()
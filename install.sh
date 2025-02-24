import os
import importlib
import traceback

# 1️⃣ **DYNAMIC MODULE LOADING**
loaded_modules = {}

def load_modules():
    """Scans the 'modules/' folder and loads all valid OSINTEL modules dynamically."""
    global loaded_modules
    loaded_modules = {}

    print("🔍 Scanning for available OSINT modules...\n")

    for filename in os.listdir("modules"):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"modules.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, "run") and hasattr(module, "description"):
                    loaded_modules[module_name] = module
                    print(f"✅ Loaded module: {module_name} - {module.description}")
                else:
                    print(f"⚠️ Skipping module (missing 'run' function or description): {module_name}")
            except Exception as e:
                print(f"❌ Failed to load module: {module_name} - {e}")
                traceback.print_exc()

# 2️⃣ **MODULE EXECUTION MENU**
def show_module_menu():
    """Displays the module selection menu and executes the chosen module."""
    while True:
        os.system("clear" if os.name == "posix" else "cls")
        print("\n🔹 OSINTEL - Select a Module to Execute:")
        print("--------------------------------------------------")

        if not loaded_modules:
            print(f"{'⚠️ No modules detected! Ensure modules are inside the `modules/` folder.':^50}")
        else:
            for i, (module_name, module) in enumerate(loaded_modules.items()):
                print(f"{i+1}. {module.description}")

        print("Q. Quit OSINTEL")

        choice = input("\nEnter choice: ").strip().lower()

        if choice == "q":
            print("👋 Exiting OSINTEL.")
            break

        try:
            selected_module = list(loaded_modules.values())[int(choice) - 1]
            selected_module.run()
        except (IndexError, ValueError):
            print("❌ Invalid choice. Please select a valid module.")

# 3️⃣ **MAIN EXECUTION**
if __name__ == "__main__":
    load_modules()
    show_module_menu()

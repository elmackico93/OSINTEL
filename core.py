import os
import importlib
import traceback
import config
import json
import time
import itertools
import sys

# UI Colors
RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
WHITE = "\033[1;37m"
RESET = "\033[0m"

# 1️⃣ **DISPLAY OSINTEL BANNER**
def display_banner():
    """Displays OSINTEL startup banner with dynamic animation."""
    os.system("clear" if os.name == "posix" else "cls")

    banner = f"""
{CYAN}------------------------------------------------------------
██████╗ ███████╗███████╗██╗███╗   ██╗████████╗███████╗██╗     
██╔══██╗██╔════╝██╔════╝██║████╗  ██║╚══██╔══╝██╔════╝██║     
██████╔╝█████╗  █████╗  ██║██╔██╗ ██║   ██║   █████╗  ██║     
██╔═══╝ ██╔══╝  ██╔══╝  ██║██║╚██╗██║   ██║   ██╔══╝  ██║     
██║     ███████╗██║     ██║██║ ╚████║   ██║   ███████╗███████╗
╚═╝     ╚══════╝╚═╝     ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚══════╝
{WHITE}Advanced AI-Driven OSINT & Cybercrime Intelligence Toolkit{CYAN}
------------------------------------------------------------{RESET}
"""
    for line in banner.split("\n"):
        print(line)
        time.sleep(0.05)
    time.sleep(1)

# 2️⃣ **DYNAMIC MODULE LOADING**
loaded_modules = {}

def load_modules():
    """Scans the 'modules/' folder and loads all valid OSINTEL modules dynamically."""
    global loaded_modules
    loaded_modules = {}

    print(f"{CYAN}🔍 Scanning for available OSINT modules...{RESET}\n")
    time.sleep(1)

    for filename in os.listdir("modules"):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"modules.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, "run") and hasattr(module, "description"):
                    loaded_modules[module_name] = module
                    print(f"{GREEN}✅ Loaded module: {module_name} - {module.description}{RESET}")
                else:
                    print(f"{YELLOW}⚠️ Skipping module (missing 'run' function or description): {module_name}{RESET}")
            except Exception as e:
                print(f"{RED}❌ Failed to load module: {module_name} - {e}{RESET}")
                traceback.print_exc()

# 3️⃣ **LOADING ANIMATION**
def loading_animation(message="Processing"):
    """Displays a smooth loading animation in the terminal."""
    animation = itertools.cycle(["⠏", "⠛", "⠹", "⠼", "⠶", "⠧"])
    sys.stdout.write(f"{YELLOW}{message} {RESET}")
    for _ in range(15):  # Loop through the animation a few times
        sys.stdout.write(next(animation))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write("\b")
    sys.stdout.write("\n")

# 4️⃣ **MODULE EXECUTION MENU**
def show_module_menu():
    """Displays the module selection menu and executes the chosen module."""
    while True:
        os.system("clear" if os.name == "posix" else "cls")
        print(f"{CYAN}🔹 OSINTEL - Select a Module to Execute:{RESET}")
        print(f"{WHITE}--------------------------------------------------{RESET}")

        for i, (module_name, module) in enumerate(loaded_modules.items()):
            print(f"{GREEN}{i+1}. {module.description}{RESET}")

        print(f"{RED}Q. Quit OSINTEL{RESET}")
        choice = input(f"\n{YELLOW}Enter choice:{RESET} ").strip().lower()

        if choice == "q":
            print(f"{RED}👋 Exiting OSINTEL.{RESET}")
            break

        try:
            selected_module = list(loaded_modules.values())[int(choice) - 1]
            selected_module.run()
        except (IndexError, ValueError):
            print(f"{RED}❌ Invalid choice. Please enter a valid module number.{RESET}")
            time.sleep(1)

# 5️⃣ **SYSTEM STARTUP – AUTO-LOAD CORE COMPONENTS**
def startup():
    """Runs initial system checks and loads essential modules."""
    print(f"\n{CYAN}🚀 OSINTEL is starting up...{RESET}\n")
    loading_animation("Initializing System")

    # Auto-Run Essential Modules
    essential_modules = ["modules.config", "modules.report"]
    for module in essential_modules:
        if module in loaded_modules:
            print(f"{BLUE}🔧 Running startup module: {module}{RESET}")
            loaded_modules[module].run()

    print(f"{GREEN}✅ All core components are ready.{RESET}\n")
    time.sleep(1)

# 6️⃣ **MAIN EXECUTION**
if __name__ == "__main__":
    display_banner()
    load_modules()
    startup()
    show_module_menu()

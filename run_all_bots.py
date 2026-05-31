"""
Adam Creative Studios - Multi-Bot Local Launcher
Runs all 5 bots concurrently in the terminal for local testing
"""

import subprocess
import sys
import os
from pathlib import Path
import threading
import time
import signal

# Color codes for terminal output
class Colors:
    CORE = "\033[94m"    # Blue
    STAFF = "\033[92m"   # Green
    DESIGN = "\033[93m"  # Yellow
    DEV = "\033[96m"     # Cyan
    CUSTOMS = "\033[95m" # Magenta
    RESET = "\033[0m"
    BOLD = "\033[1m"

# Bot configurations
BOTS = {
    "core_bot": {
        "path": "bots/core_bot",
        "color": Colors.CORE,
        "name": "CORE BOT"
    },
    "staff_bot": {
        "path": "bots/staff_bot",
        "color": Colors.STAFF,
        "name": "STAFF BOT"
    },
    "design_bot": {
        "path": "bots/design_bot",
        "color": Colors.DESIGN,
        "name": "DESIGN BOT"
    },
    "dev_bot": {
        "path": "bots/dev_bot",
        "color": Colors.DEV,
        "name": "DEV BOT"
    },
    "customs_bot": {
        "path": "bots/customs_bot",
        "color": Colors.CUSTOMS,
        "name": "CUSTOMS BOT"
    }
}

processes = []

def run_bot(bot_key):
    """Run a single bot in a subprocess"""
    bot_config = BOTS[bot_key]
    bot_path = Path(bot_config["path"]) / "main.py"
    
    if not bot_path.exists():
        print(f"{bot_config['color']}[{bot_config['name']}]{Colors.RESET} ❌ main.py not found at {bot_path}")
        return
    
    print(f"{bot_config['color']}[{bot_config['name']}]{Colors.RESET} 🚀 Starting...")
    
    try:
        process = subprocess.Popen(
            [sys.executable, str(bot_path)],
            cwd=os.getcwd(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        processes.append((bot_key, process))
        
        # Read and display output
        for line in iter(process.stdout.readline, ''):
            if line:
                print(f"{bot_config['color']}[{bot_config['name']}]{Colors.RESET} {line.rstrip()}")
        
        process.wait()
    except Exception as e:
        print(f"{bot_config['color']}[{bot_config['name']}]{Colors.RESET} ❌ Error: {e}")

def signal_handler(sig, frame):
    print(f"\n\n{Colors.BOLD}Stopping all bots...{Colors.RESET}")
    for bot_key, process in processes:
        try:
            process.terminate()
            process.wait(timeout=5)
        except:
            process.kill()
    print(f"{Colors.BOLD}All bots stopped.{Colors.RESET}")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    
    print(f"\n{Colors.BOLD}╔════════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.BOLD}║  Adam Creative Studios - Multi-Bot Launcher       ║{Colors.RESET}")
    print(f"{Colors.BOLD}╚════════════════════════════════════════════════════╝{Colors.RESET}\n")
    
    # Check if config.json exists
    if not Path("config.json").exists():
        print("❌ config.json not found! Make sure you're in the ACS_Network directory.")
        sys.exit(1)
    
    print(f"{Colors.BOLD}Starting all 5 bots concurrently...{Colors.RESET}\n")
    
    for bot_key in BOTS.keys():
        print(f"• {BOTS[bot_key]['color']}{BOTS[bot_key]['name']}{Colors.RESET}")
    
    print(f"\n{Colors.BOLD}Press Ctrl+C to stop all bots{Colors.RESET}\n")
    print("=" * 60)
    print()
    
    # Run all bots concurrently in threads
    threads = []
    for bot_key in BOTS.keys():
        thread = threading.Thread(target=run_bot, args=(bot_key,), daemon=True)
        threads.append(thread)
        thread.start()
        time.sleep(1)  # Stagger the startup slightly
    
    # Keep the main thread alive
    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        signal_handler(None, None)

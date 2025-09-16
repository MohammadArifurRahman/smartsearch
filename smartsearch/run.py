#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path

def main():
    """Run the Smart Search Streamlit app"""
    print("🔍 Starting Smart Search...")
    
    # Get path to app.py in same directory
    app_path = Path(__file__).parent / "app.py"
    
    # Run streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", str(app_path),
            "--server.headless", "false",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
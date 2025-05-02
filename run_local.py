#!/usr/bin/env python
"""
Simple script to run Pygbag locally for development.
"""
import subprocess
import webbrowser
import time
import sys

def main():
    """Run Pygbag for local testing."""
    print("Starting Pygbag development server...")
    
    # Build command with minimal required flags
    cmd = [
        "pygbag",
        "--port", "8000",
        "--ume_block", "0",
        "--width", "800",
        "--height", "600",
        "main.py"
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    
    # Start pygbag
    process = subprocess.Popen(cmd)
    
    # Wait for server to start
    time.sleep(2)
    
    # Open browser
    print("Opening http://localhost:8000 in browser...")
    webbrowser.open("http://localhost:8000")
    
    print("\nPygbag server is running. Press Ctrl+C to stop.")
    
    try:
        # Wait for the process to complete (Ctrl+C to exit)
        process.wait()
    except KeyboardInterrupt:
        print("\nShutting down development server...")
        process.terminate()

if __name__ == "__main__":
    main()
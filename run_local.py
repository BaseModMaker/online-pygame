#!/usr/bin/env python
"""
Helper script to run Pygbag locally for development.
This provides better diagnostics and configuration for local testing.
"""
import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def main():
    """Run the Pygbag development server with optimal settings."""
    print("Starting Pygbag development server...")
    
    # Set environment variable for debugging
    os.environ["PYGBAG_DEBUG"] = "1"
    
    # Build command with all the optimal flags for local development
    cmd = [
        "pygbag",
        "--port", "8000",
        "--app_name", "Online Pygame Demo",
        "--ume_block", "0",    # No user media engagement block (no click required to start)
        "--width", "800",
        "--height", "600",
        "main.py"
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    
    # Start pygbag
    process = subprocess.Popen(cmd)
    
    # Wait a moment to give server time to start
    print("Waiting for server to start...")
    time.sleep(2)
    
    # Open browser after a short delay
    try:
        print("Opening http://localhost:8000 in browser...")
        webbrowser.open("http://localhost:8000")
        
        # Wait for the process to complete (Ctrl+C to exit)
        process.wait()
    except KeyboardInterrupt:
        print("\nShutting down development server...")
        process.terminate()
        sys.exit(0)

if __name__ == "__main__":
    main()
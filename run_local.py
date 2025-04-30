#!/usr/bin/env python
"""
Helper script to run Pygbag locally for development.
This provides better diagnostics and configuration for local testing.
"""
import os
import sys
import subprocess
import webbrowser
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
        "--app_name", "Online Pygame Demo",  # Fixed: changed from --app-name to --app_name
        "--ume_block", "0",    # No user media engagement block (no click required to start)
        "--no_opt",            # Fixed: changed from --no-opt to --no_opt
        "main.py"
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    
    # Start pygbag
    process = subprocess.Popen(cmd)
    
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
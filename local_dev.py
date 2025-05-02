#!/usr/bin/env python
"""
Alternative to pygbag for local development of your web-based Pygame project.
This script provides a more reliable way to develop and test your game locally.
"""
import http.server
import socketserver
import webbrowser
import os
import sys
import time
import socket
import subprocess
import threading
import argparse
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import urllib.request
import urllib.error

# Configuration
DEFAULT_PORT = 8000
BUILD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build", "web")
MAIN_PY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")
PYGBAG_CDN = "https://pygame-web.github.io"

class GameFileHandler(FileSystemEventHandler):
    """Watch for file changes and trigger rebuilds when needed."""
    
    def __init__(self, rebuild_callback):
        self.rebuild_callback = rebuild_callback
        self.last_modified = time.time()
        # Debounce period (in seconds) to avoid multiple rebuilds
        self.debounce_period = 2
    
    def on_modified(self, event):
        # If it's a Python file, schedule a rebuild
        if event.is_directory:
            return
        if event.src_path.endswith('.py'):
            # Debounce to prevent multiple builds for the same change
            current_time = time.time()
            if current_time - self.last_modified > self.debounce_period:
                self.last_modified = current_time
                print(f"\nFile changed: {os.path.basename(event.src_path)}")
                self.rebuild_callback()

def find_free_port(start_port=DEFAULT_PORT, max_attempts=10):
    """Find an available port, starting from start_port."""
    port = start_port
    for _ in range(max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            print(f"Port {port} is in use, trying next port...")
            port += 1
    
    print(f"Warning: Could not find a free port after {max_attempts} attempts")
    return port + 1  # Try one more port as a last resort

def check_pygbag_installed():
    """Check if pygbag is installed and accessible."""
    try:
        subprocess.run(['pygbag', '--version'], 
                       stdout=subprocess.PIPE, 
                       stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def build_game(debug=False):
    """Build the game using pygbag but don't start a server."""
    print("Building game with pygbag...")
    
    if not check_pygbag_installed():
        print("Error: pygbag is not installed. Please install it with:")
        print("pip install pygbag")
        sys.exit(1)
        
    # Environment setup for the build
    env = os.environ.copy()
    if debug:
        env["PYGBAG_DEBUG"] = "1"
    
    # Build command with flags from pygbag.toml but tell it not to serve
    cmd = [
        "pygbag",
        "--build",  # Only build, don't serve
        "--app_name", "Online Pygame Demo",
        "--ume_block", "0", 
        "--width", "800",
        "--height", "600",
        MAIN_PY
    ]
    
    try:
        result = subprocess.run(cmd, env=env, check=True, 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
        print("Build successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        print(e.stderr.decode())
        return False

class ProxyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler that proxies missing files to the Pygame CDN."""
    
    def do_GET(self):
        # First try to serve the file locally
        local_path = self.translate_path(self.path)
        
        if os.path.exists(local_path):
            # File exists locally, serve it
            return super().do_GET()
        else:
            # Attempt to proxy from Pygame CDN
            if "/archives/" in self.path:
                try:
                    # Adjust the URL to point to the Pygame CDN
                    url = f"{PYGBAG_CDN}{self.path}"
                    print(f"Proxying request to: {url}")
                    
                    # Make the request to the CDN
                    with urllib.request.urlopen(url) as response:
                        # Set the appropriate headers
                        self.send_response(200)
                        for header, value in response.getheaders():
                            if header.lower() in ('content-type', 'content-length', 'last-modified'):
                                self.send_header(header, value)
                        
                        # Add CORS and cache control headers
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.send_header('Cache-Control', 'max-age=3600')
                        self.end_headers()
                        
                        # Send the content
                        self.wfile.write(response.read())
                    return
                except urllib.error.URLError as e:
                    print(f"Failed to proxy request: {e}")
                    # Fall through to 404
                
            # If we get here, return 404
            self.send_error(404, f"File not found: {self.path}")
            
    def end_headers(self):
        # Add headers for development
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        super().end_headers()

def start_server(port):
    """Start a development HTTP server on the specified port."""
    os.chdir(BUILD_DIR)
    handler = ProxyHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    print(f"Serving the game at http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    return httpd

def open_browser(port):
    """Open the browser to the game URL."""
    webbrowser.open(f"http://localhost:{port}")

def start_file_watcher(rebuild_callback):
    """Start watching Python files for changes."""
    event_handler = GameFileHandler(rebuild_callback)
    observer = Observer()
    # Watch the directory containing main.py
    main_dir = os.path.dirname(os.path.abspath(MAIN_PY))
    observer.schedule(event_handler, main_dir, recursive=True)
    observer.start()
    return observer

def patch_index_html():
    """Patch the index.html file to use the CDN correctly."""
    index_path = os.path.join(BUILD_DIR, "index.html")
    if not os.path.exists(index_path):
        print(f"Warning: Cannot find {index_path} to patch")
        return False
    
    with open(index_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    # Make sure the CDN variable is correctly set 
    if "cdn :" not in content:
        print("Warning: Could not find cdn configuration in index.html")
        return False
    
    # Backup original file
    backup_path = os.path.join(BUILD_DIR, "index.html.bak")
    if not os.path.exists(backup_path):
        with open(backup_path, "w", encoding="utf-8") as file:
            file.write(content)
    
    # Update the CDN path to the official one
    if "cdn : \"https://pygame-web.github.io" not in content:
        content = content.replace(
            'cdn : "', 
            'cdn : "https://pygame-web.github.io'
        )
        
        with open(index_path, "w", encoding="utf-8") as file:
            file.write(content)
        print("Patched index.html to use official CDN")
        
    return True

def main():
    """Run the development environment."""
    parser = argparse.ArgumentParser(description="Local development server for web-based Pygame")
    parser.add_argument("--no-build", action="store_true", help="Skip the initial build step")
    parser.add_argument("--no-watch", action="store_true", help="Don't watch for file changes")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Port to serve on (default: {DEFAULT_PORT})")
    args = parser.parse_args()
    
    # Initial build if needed
    if not args.no_build:
        if not build_game(args.debug):
            print("Initial build failed. Fix errors and try again.")
            return
    
    # Patch index.html to use the official CDN
    patch_index_html()
    
    # Find a free port if the specified one is not available
    port = find_free_port(args.port)
    
    # Start the HTTP server in a separate thread
    server = start_server(port)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    # Open browser
    time.sleep(0.5)  # Small delay to ensure server is running
    open_browser(port)
    
    # Setup rebuild function
    def rebuild():
        print("Rebuilding game...")
        if build_game(args.debug):
            print("Rebuild successful! Refresh your browser to see changes.")
            patch_index_html()
    
    # Start file watcher if requested
    observer = None
    if not args.no_watch:
        observer = start_file_watcher(rebuild)
        print("\nWatching for file changes... (Python files will trigger automatic rebuilds)")
    
    # Keep the main thread running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.shutdown()
        if observer:
            observer.stop()
            observer.join()
        sys.exit(0)

if __name__ == "__main__":
    main()
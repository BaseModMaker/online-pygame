#!/usr/bin/env python
"""
Simple HTTP server to serve the built pygame game.
This is a more reliable way to test the game locally.
"""
import http.server
import socketserver
import webbrowser
import os
import time
import socket

# Configuration
DEFAULT_PORT = 8000
BUILD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build", "web")

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

def main():
    """Start a simple HTTP server to serve the game."""
    print(f"Starting HTTP server to serve the game from {BUILD_DIR}")
    
    # Change to the build directory
    os.chdir(BUILD_DIR)
    
    # Find an available port
    port = find_free_port()
    
    # Create the server
    Handler = http.server.SimpleHTTPRequestHandler
    try:
        httpd = socketserver.TCPServer(("", port), Handler)
        
        print(f"Serving the game at http://localhost:{port}")
        print("Press Ctrl+C to stop the server")
        
        # Open the browser
        time.sleep(0.5)  # Small delay to ensure the server is running
        webbrowser.open(f"http://localhost:{port}")
        
        # Start the server
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server")
            httpd.server_close()
    except OSError as e:
        print(f"Error starting server: {e}")
        print("You may have another server already running.")
        print("Try closing other terminals or restarting your computer if needed.")
        
if __name__ == "__main__":
    main()
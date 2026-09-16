#!/usr/bin/env python3
"""
Lightweight zero-dependency HTTP server to serve the Dinosaur Game static files.
Usage:
    python3 -m src.server [--port 8080]
"""

import argparse
import http.server
import os
import socketserver
import webbrowser
from pathlib import Path


def run_server(port: int = 8080, host: str = "127.0.0.1", open_browser: bool = True) -> None:
    project_root = Path(__file__).resolve().parent.parent
    web_dir = project_root / "public"

    if not web_dir.exists():
        raise FileNotFoundError(f"Static web directory not found: {web_dir}")

    os.chdir(web_dir)

    handler = http.server.SimpleHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True

    # Attempt to bind, fallback to alternative ports if occupied
    httpd = None
    actual_port = port
    for p in range(port, port + 10):
        try:
            httpd = socketserver.TCPServer((host, p), handler)
            actual_port = p
            break
        except OSError:
            continue

    if httpd is None:
        raise OSError(f"Could not bind to any port in range {port}-{port+9}")

    url = f"http://{host}:{actual_port}/"
    print("=" * 60)
    print(f"🦕 Dinosaur Runner Game is live at: {url}")
    print(f"👉 Open {url} in your browser to play!")
    print("   Controls: [SPACE / ▲] Jump | [▼] Duck | [P] Pause | [M] Mute")
    print("   Press Ctrl+C to stop the server.")
    print("=" * 60)

    if open_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    with httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")


def main():
    parser = argparse.ArgumentParser(description="Dinosaur Game Web Server")
    parser.add_argument("--port", type=int, default=8080, help="Port to bind (default: 8080)")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host interface (default: 127.0.0.1)")
    parser.add_argument("--no-browser", action="store_true", help="Do not automatically open the browser")
    args = parser.parse_args()

    run_server(port=args.port, host=args.host, open_browser=not args.no_browser)


if __name__ == "__main__":
    main()

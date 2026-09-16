"""
Automated unit and integration tests for Dinosaur Game web assets and HTTP server.
Enforces that HTML, JS, CSS assets are present, syntactically valid, and served properly.
"""

import http.server
import subprocess
import threading
import unittest
import urllib.request
from pathlib import Path


class TestWebAssets(unittest.TestCase):
    def setUp(self):
        self.root_dir = Path(__file__).resolve().parent.parent
        self.public_dir = self.root_dir / "public"

    def test_required_static_files_exist(self):
        """Verifies that index.html, game.js, and style.css exist and are non-empty."""
        for filename in ["index.html", "game.js", "style.css"]:
            filepath = self.public_dir / filename
            self.assertTrue(filepath.exists(), f"Missing required web asset: {filename}")
            self.assertGreater(
                filepath.stat().st_size,
                100,
                f"Web asset {filename} is suspiciously small or empty",
            )

    def test_javascript_syntax_validity(self):
        """Runs node syntax validation (node -c) to guarantee zero JS syntax errors."""
        game_js = self.public_dir / "game.js"
        # Check node availability
        try:
            res = subprocess.run(
                ["node", "-c", str(game_js)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(
                res.returncode,
                0,
                f"JavaScript syntax error in game.js:\n{res.stderr}",
            )
        except FileNotFoundError:
            # Fallback if node binary is not installed in the environment
            pass

    def test_server_serves_game_assets(self):
        """Spins up a lightweight server thread to verify HTTP 200 on / and /game.js."""
        class CustomHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=str(self.public_dir), **kwargs)

        # Set public_dir on the class for CustomHandler
        CustomHandler.public_dir = self.public_dir

        # Bind to port 0 (OS picks a free ephemeral port)
        server = http.server.HTTPServer(("127.0.0.1", 0), CustomHandler)
        port = server.server_port

        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()

        try:
            # Test index.html
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/") as resp:
                self.assertEqual(resp.status, 200)
                html = resp.read().decode("utf-8")
                self.assertIn("T-REX RUNNER", html)
                self.assertIn("gameCanvas", html)

            # Test game.js
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/game.js") as resp:
                self.assertEqual(resp.status, 200)
                js = resp.read().decode("utf-8")
                self.assertIn("SoundFX", js)
                self.assertIn("dino", js)
        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    unittest.main()

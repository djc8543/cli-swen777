import json
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import pytest

# ---------------- Setup and Helpers ----------------
@pytest.fixture(scope="function")
def http_server():
    """Spin up an HTTP server to test cookie functionality"""
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/set-cookie":
                self.send_response(200)
                self.send_header("Set-Cookie", "double-chocolate-chunk=booooom; Path=/")
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"ok": true}')
            elif self.path == "/echo":
                cookie = self.headers.get("Cookie", "")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                body = json.dumps({"cookie": cookie}).encode()
                self.wfile.write(body)
            else:
                self.send_response(404)
                self.end_headers()

    server = HTTPServer(("localhost", 0), Handler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    yield server
    server.shutdown()
    thread.join()

def run_httpie(*args, env=None):
    """Starts httpie's command as a subprocess"""
    result = subprocess.run(
        ["http", "--no-color", *args],
        capture_output=True,
        text=True,
        env=env,
    )
    return result
# ---------------- End Setup and Helpers ----------------

def test_cookie_persistence(http_server, tmp_path):
    """Verifies that cookies are properly set and persisted"""
    session_file = tmp_path / "session.json"
    base_url = f"http://localhost:{http_server.server_port}"

    set_result = run_httpie("--session", str(session_file), f"{base_url}/set-cookie")
    assert set_result.returncode == 0, set_result.stderr

    session_data = json.loads(session_file.read_text())
    cookies = session_data["cookies"]
    assert any(c["name"] == "double-chocolate-chunk" and c["value"] == "booooom" for c in cookies), f"Expected double-chocolate-chunk cookie, got: {cookies}"

    run_result = run_httpie("--session", str(session_file), f"{base_url}/echo")
    assert run_result.returncode == 0
    assert '"double-chocolate-chunk=booooom"' in run_result.stdout

def test_expired_cookies(http_server, tmp_path):
    """Verifies that expired cookies can't be used"""
    session_file = tmp_path / "session.json"
    base_url = f"http://localhost:{http_server.server_port}"

    session_data = {
        "cookies": [{
            "name": "expired",
            "value": "tiny-boom",
            "domain": "localhost",
            "path": "/",
            "expires": "2025-11-07T00:00:00Z"
        }]
    }
    session_file.write_text(json.dumps(session_data))

    run_result = run_httpie("--session", str(session_file), f"{base_url}/echo")
    assert run_result.returncode == 0
    assert "expired=tiny-boom" not in run_result.stdout

    new_data = json.loads(session_file.read_text())
    assert new_data["cookies"] == [] or all(
        c["name"] != "expired" for c in new_data["cookies"]
    )

def test_cookie_override(http_server, tmp_path):
    """Verifies that session cookies can be overridden and persisted by the server"""
    session_file = tmp_path / "session.json"
    base_url = f"http://localhost:{http_server.server_port}"

    initial_session = {"cookies": [{"name": "ship-of-theseus", "value": "still-is"}]}
    session_file.write_text(json.dumps(initial_session))

    result = run_httpie(
        "--session", str(session_file),
        "GET", f"{base_url}/set-cookie",
        "Cookie: ship-of-theseus=no-longer-is"
    )

    assert result.returncode == 0
    assert "ship-of-theseus=no-longer-is" in result.stdout, "Expected overridden cookie to be sent"

    session_data = json.loads(session_file.read_text())
    cookie_names = [c["name"] for c in session_data["cookies"]]
    assert "double-chocolate-chunk" in cookie_names, "Expected new double-chocolate-chunk cookie persisted"
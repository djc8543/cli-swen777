import subprocess
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
import shutil


class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/secure":
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Not found"}).encode("utf-8"))
            return

        auth_header = self.headers.get("Authorization", "")

        if auth_header == "Basic dXNlcjpwYXNz":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Authenticated"}).encode("utf-8"))
        else:
            self.send_response(401)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Unauthorized"}).encode("utf-8"))


def start_auth_server():
    server = HTTPServer(("localhost", 8081), AuthHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server

def test_httpie_basic_auth_flow():
    http_cmd = shutil.which("http")
    assert http_cmd, "HTTPie CLI ('http') must be installed and on PATH"

    server = start_auth_server()

    result = subprocess.run(
        [
            http_cmd,
            "--print=HhBb",        
            "--auth", "user:pass", 
            "GET",
            "http://localhost:8081/secure",
        ],
        capture_output=True,
        text=True,
    )

    server.shutdown()

    stdout = result.stdout.strip()
    stderr = result.stderr.strip()

    assert result.returncode == 0, "HTTPie exited with error: " + stderr
    assert "200 OK" in stdout, "Expected 200 OK status line for valid credentials"
    assert "Content-Type: application/json" in stdout, "Expected JSON content type"
    assert '"message": "Authenticated"' in stdout, "Expected authenticated response content"
    assert not stderr, "Unexpected error output: " + stderr

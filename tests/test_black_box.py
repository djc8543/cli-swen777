import subprocess
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
import shutil

# mock HTTP Handler
class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"message": "Hello from mock server"}).encode("utf-8"))

# mock server
def start_test_server():
    server = HTTPServer(("localhost", 8080), HttpHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server

'''
Validate the full HTTPie CLI workflow with a GET request

Uses the httpie public interface (http command), no internal code paths for API's
'''
def test_httpie_get_flow():
    # make sure httpie is installed
    http_cmd = shutil.which("http")
    assert http_cmd, "HTTPie CLI ('http') must be installed and on PATH"

    server = start_test_server()

    # execute via the CLI
    result = subprocess.run(
        [http_cmd, "--print=HhBb", "GET", "http://localhost:8080"],
        capture_output=True,
        text=True
    )

    server.shutdown()

    # cleanup the output
    stdout = result.stdout.strip()
    stderr = result.stderr.strip()

    # validate responses
    assert result.returncode == 0, "HTTPie exited with error: " + stderr
    assert "200 OK" in stdout, "Expected 200 OK status line"
    assert "Content-Type: application/json" in stdout, "Expected JSON content type"
    assert '"message": "Hello from mock server"' in stdout, "Expected mock response content"
    assert not stderr, "Unexpected error output: " + stderr

'''
Validates that HTTPie properly reports an error when attempting to access an invalid URL.

Uses the httpie public interface (http command), no internal code paths for API's
'''
def test_httpie_invalid_url():
    # ensure httpie exists
    http_cmd = shutil.which("http")
    assert http_cmd, "HTTPie CLI ('http') must be installed and on PATH"

    invalid_url = "http://drpebbah.localhost"

    # execute via the CLI
    result = subprocess.run(
    [http_cmd, invalid_url],
    capture_output=True,
    text=True
    )

    # cleanup the output
    stdout = result.stdout.strip()
    stderr = result.stderr.strip()

    expected_error_terms = [
    "Error",
    "Could not",
    "Not known",
    "Failed",
    ]

    # validate responses
    assert result.returncode != 0, "Expected exit with a non-zero error code"
    assert "200 OK" not in stdout, "Unexpected success for invalid URL"
    assert any(term.lower() in stderr.lower() for term in expected_error_terms), ("Expected error message about connection failure.")
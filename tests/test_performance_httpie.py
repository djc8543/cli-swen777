import subprocess
import sys
import pytest


def _build_httpie_command(url: str) -> list[str]:
    return [
        sys.executable,
        "-m",
        "httpie",
        "GET",
        url,
    ]


@pytest.mark.benchmark(group="httpie-cli-get")
def test_httpie_get_root_benchmark(benchmark, http_server):
    url = f"http://{http_server}/"

    cmd = _build_httpie_command(url)

    def run_httpie():
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr

    benchmark(run_httpie)


@pytest.mark.benchmark(group="httpie-cli-get-json")
def test_httpie_get_json_benchmark(benchmark, http_server):
    url = f"http://{http_server}/json"

    cmd = _build_httpie_command(url)

    def run_httpie():
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr

    benchmark(run_httpie)

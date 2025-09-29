import pytest
from httpie.output.ui import man_pages as mp
from .utils import MockEnvironment

class DummyProcess:
    def __init__(self, returncode):
        self.returncode = returncode


def test_is_available_short_circuits(monkeypatch): # test to cover line 21-22 in man_pages.py
    monkeypatch.setattr(mp, "NO_MAN_PAGES", True)
    called = {"v": False} 

    def fake_run(*a, **k): # This block is to make sure subprocess.run is not called
        called["v"] = True
        return DummyProcess(0)

    monkeypatch.setattr(mp.subprocess, "run", fake_run)
    assert mp.is_available("http") is False # should return False since NO_MAN_PAGES is True
    assert called["v"] is False  


def test_is_available_success_returncode_zero(monkeypatch): # test to cover 23 - 36 in man_pages.py
    monkeypatch.setattr(mp, "NO_MAN_PAGES", False) # ensure NO_MAN_PAGES is False
    monkeypatch.setattr(mp.subprocess, "run", lambda *a, **k: DummyProcess(0)) # mock subprocess.run to return a process with returncode 0
    assert mp.is_available("http") is True # should return True since returncode is 0


def test_is_available_not_found_nonzero(monkeypatch): # test to cover 24 - 36 in man_pages.py
    monkeypatch.setattr(mp, "NO_MAN_PAGES", False)
    monkeypatch.setattr(mp.subprocess, "run", lambda *a, **k: DummyProcess(1)) # mock subprocess.run to return a process with returncode 1
    assert mp.is_available("http") is False # should return False since returncode is not 0


def test_is_available_exception_path(monkeypatch): # test to cover the exception handling block in is_available
    monkeypatch.setattr(mp, "NO_MAN_PAGES", False)

    def error(*a, **k): # mock subprocess.run to raise an exception
        raise OSError("no man here")

    monkeypatch.setattr(mp.subprocess, "run", error) 
    assert mp.is_available("http") is False # should return False since an exception is raised


def test_display_for_calls_man_with_env_streams(monkeypatch): # test to cover display_for function
    captured = {}

    def fake_run(args, stdout=None, stderr=None): 
        captured["args"] = args
        captured["stdout"] = stdout
        captured["stderr"] = stderr
        return DummyProcess(0)

    monkeypatch.setattr(mp.subprocess, "run", fake_run)
    env = MockEnvironment()
    mp.display_for(env, "http")

    assert captured["args"] == [mp.MAN_COMMAND, mp.MAN_PAGE_SECTION, "http"]
    assert captured["stdout"] is env.stdout
    assert captured["stderr"] is env.stderr

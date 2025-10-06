import pytest
from httpie.output.ui import rich_utils


class DummyConsole:
    def __init__(self, *a, **kw):
        self.print_called_with = None

    def print(self, renderable):
        self.print_called_with = renderable

    def export_text(self):
        return "mocked output"

def test_render_as_string_monkeypatched(monkeypatch):
    monkeypatch.setattr(rich_utils, "Console", DummyConsole)
    result = rich_utils.render_as_string("Hello World")
    assert result == "mocked output"

def test_render_as_string_calls_theme_factory(monkeypatch):
    theme_called = {"called": False}
    def fake_theme_factory():
        theme_called["called"] = True
        return "mocked_theme"
    monkeypatch.setattr(rich_utils, "_make_rich_color_theme", fake_theme_factory)
    monkeypatch.setattr(rich_utils, "Console", DummyConsole)
    _ =rich_utils.render_as_string("Test Renderable")
    assert theme_called["called"] is True

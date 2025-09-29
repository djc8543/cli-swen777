#import re
import types
import pytest
from httpie.compat import cached_property, find_entry_points, get_dist_name, ensure_default_certs_loaded


def test_cached_property_conflicts():
    """inducing a cached property conflict"""

    class Initial:
        @cached_property
        def value(self):
            return 1

    property = Initial.__dict__["value"]

    with pytest.raises(TypeError):
        class Secondary:
            secondary_property = property


def test_cached_values():
    """cached_property only calls the method once, then caches the result"""

    class CacheChecker:
        calls = 0

        @cached_property
        def value(self):
            CacheChecker.calls += 1
            return 5 # arbitrary value

    obj = CacheChecker()
    assert obj.value == 5 # first increments the calls
    assert obj.value == 5 # second should access cached value and not incrememnt calls
    assert CacheChecker.calls == 1


def test_find_entry_points_formats():
    """find_entry_points works with both modern and older formats."""

    # modern object
    class ModernFormat:
        def select(self, group):
            return ["chosen"]

    assert list(find_entry_points(ModernFormat(), "group")) == ["chosen"]

    # old dictionary
    old_format = {"group": ["one", "two"]}
    assert set(find_entry_points(old_format, "group")) == {"one", "two"}



def test_get_dist_name(monkeypatch):
    """get_dist_name works when entry point has dist or uses metadata"""

    # entry with a dist
    class EPWithDist:
        dist = types.SimpleNamespace(name="dummy_dist")

    assert get_dist_name(EPWithDist()) == "dummy_dist"

    # entry with metadata using monkeypatch attributes
    class EPWithoutDist:
        module = "dummy_module"
        value = "ignored"
        pattern = types.SimpleNamespace(
            match=lambda value: types.SimpleNamespace(
                group=lambda key: "dummy_package"
            )
        )

    monkeypatch.setattr(
        "httpie.compat.importlib_metadata.metadata",
        lambda pkg: {"name": "new_dist_who_dis"}
    )

    assert get_dist_name(EPWithoutDist()) == "new_dist_who_dis"



def test_default_certs_load():
    """ensure_default_certs_loaded calls load_default_certs if no CA certs"""

    # mocking an ssl context
    class FakeSSL:
        def get_ca_certs(self):
            return []

        def load_default_certs(self):
            self.called = True

    context = FakeSSL()
    context.called = False
    ensure_default_certs_loaded(context)
    assert context.called
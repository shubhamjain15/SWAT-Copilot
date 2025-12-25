"""Smoke tests for package metadata."""
from swat_copilot import __version__


def test_version() -> None:
    assert isinstance(__version__, str)

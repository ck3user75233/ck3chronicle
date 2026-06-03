"""Shared pytest fixtures for ck3chronicle."""
from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def fixture_logs_minimal() -> Path:
    return Path(__file__).parent / "fixtures" / "logs" / "minimal"


@pytest.fixture
def fixture_logs_with_crash() -> Path:
    return Path(__file__).parent / "fixtures" / "logs" / "with_crash"

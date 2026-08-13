"""Test bootstrap for the ck3chronicle reboot suite.

This directory was created from scratch on 2026-08-13. No test body from the
pre-reboot repository is imported or copied into this suite.
"""
from __future__ import annotations

import sys
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SOURCE_ROOT))

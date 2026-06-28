"""Fixtures for the UI demo. Requires a running app + browser; illustrative.

`base_url` comes from the qa-config / env; `creds` is loaded from data, never
inlined. `page` is the standard pytest-playwright fixture (real browser).
"""
import json
import os
from pathlib import Path

import pytest

_HERE = Path(__file__).parent


@pytest.fixture(scope="session")
def base_url():
    return os.environ.get("QA_BASE_URL", "http://localhost:3000")


@pytest.fixture(scope="session")
def creds():
    return json.loads((_HERE / "data" / "creds.json").read_text())

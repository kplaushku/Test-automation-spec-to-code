import json
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

_HERE = Path(__file__).parent


@pytest.fixture(scope="session")
def env():
    return json.loads((_HERE / "config" / "environment.json").read_text())


@pytest.fixture(scope="session")
def posts_data():
    return json.loads((_HERE / "data" / "posts.json").read_text())


@pytest.fixture
def api(env):
    with sync_playwright() as p:
        ctx = p.request.new_context(
            base_url=env["base_url"],
            extra_http_headers=env["headers"],
        )
        yield ctx
        ctx.dispose()

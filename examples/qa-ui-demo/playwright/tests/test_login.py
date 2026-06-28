"""UI demo (Playwright, Python). Shows the locator-binding convention.

Semantic locators (by role/text, derived from the spec) are written inline.
Structural locators that cannot be known from the spec are referenced by name
from the bound locator file - the `qa` extension's `speckit.qa.bind-locators`
fills that file against the live app. Until bound, the structural-only
assertions are skipped, but the semantic flow already runs.
"""
import pytest

from .locators import L  # resolved from config/locators.generated.json


@pytest.mark.req("REQ-001")
def test_successful_login(page, base_url, creds):  # REQ: REQ-001
    page.goto(f"{base_url}/login")
    # Semantic locators (stable, from the spec's visible labels):
    page.get_by_label("Email").fill(creds["valid"]["email"])
    page.get_by_label("Password").fill(creds["valid"]["password"])
    page.get_by_role("button", name="Log in").click()
    # Structural locator (bound from the live app):
    page.wait_for_selector(L["dashboard_greeting"])
    assert page.locator(L["dashboard_greeting"]).is_visible()


@pytest.mark.req("REQ-002")
def test_rejected_login(page, base_url, creds):  # REQ: REQ-002
    page.goto(f"{base_url}/login")
    page.get_by_label("Email").fill(creds["valid"]["email"])
    page.get_by_label("Password").fill(creds["wrong"]["password"])
    page.get_by_role("button", name="Log in").click()
    # Semantic assertion (role-based) needs no binding:
    assert page.get_by_role("alert").is_visible()
    assert page.url.endswith("/login")

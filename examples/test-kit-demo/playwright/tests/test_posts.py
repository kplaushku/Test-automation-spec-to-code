import pytest


@pytest.mark.req("REQ-001")
def test_fetch_existing_post_returns_200_with_fields(api):  # REQ: REQ-001
    # Given the API is up, when GET /posts/1, then 200 with expected fields.
    resp = api.get("/posts/1")
    assert resp.status == 200
    body = resp.json()
    assert body["id"] == 1
    assert body["title"]
    assert body["body"]


@pytest.mark.req("REQ-002")
def test_create_post_returns_201_with_id(api, posts_data):  # REQ: REQ-002
    # Given the API is up, when POST /posts with a valid body, then 201 with a new id.
    resp = api.post("/posts", data=posts_data["valid_post"])
    assert resp.status == 201
    body = resp.json()
    assert isinstance(body["id"], int)
    assert body["id"] > 0


@pytest.mark.req("REQ-003")
def test_fetch_missing_post_returns_404(api):  # REQ: REQ-003
    # Given the API is up, when GET /posts/9999, then 404.
    resp = api.get("/posts/9999")
    assert resp.status == 404

# Test Specification: Posts API (demo)

> Neutral. Target under test: the public JSONPlaceholder Posts API
> (`https://jsonplaceholder.typicode.com`). API / contract level.

## Overview

Verify the read and create behavior of the Posts resource, plus the not-found
error path. Demonstrates one neutral spec producing tests in two frameworks.

## Test Levels

API / contract.

## Requirements

### REQ-001 — fetch existing post

- **Precondition:** the API is reachable; post id 1 exists.
- **Input:** GET `/posts/1`.
- **Object under test:** single-post read endpoint.
- **Expected output:** status 200; body contains `id` = 1 and non-empty
  `title` and `body` fields.
- **Error / edge cases:** covered by REQ-003.
- **Acceptance:** Given the API is up, when GET `/posts/1`, then 200 with the
  expected post fields.

### REQ-002 — create post

- **Precondition:** the API is reachable.
- **Input:** POST `/posts` with a valid post payload.
- **Object under test:** post creation endpoint.
- **Expected output:** status 201; body contains a numeric `id`.
- **Error / edge cases:** none in scope for the demo.
- **Acceptance:** Given the API is up, when POST `/posts` with a valid body,
  then 201 with a new id.

### REQ-003 — fetch missing post returns not found

- **Precondition:** the API is reachable; post id 9999 does not exist.
- **Input:** GET `/posts/9999`.
- **Object under test:** single-post read endpoint, missing resource.
- **Expected output:** status 404.
- **Acceptance:** Given the API is up, when GET `/posts/9999`, then 404.

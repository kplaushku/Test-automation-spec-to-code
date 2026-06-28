# Test Tasks: Posts API (demo)

> Framework-neutral. The same list drives both the Robot and the Playwright
> implementation — only the `framework:` choice in the plan differs.

## Tasks

- [x] T001 [REQ-001] posts — fetch existing post returns 200 with fields
      Precondition: api up · Action: GET /posts/1 · Expected: 200, id=1, non-empty title/body
- [x] T002 [REQ-002] posts — create post returns 201 with id
      Precondition: api up · Action: POST /posts valid_post · Expected: 201, numeric id
- [x] T003 [REQ-003] posts — fetch missing post returns 404
      Precondition: api up · Action: GET /posts/9999 · Expected: 404

## Coverage Check

| Requirement | Covered by | Status |
|-------------|------------|--------|
| REQ-001 | T001 | ✅ |
| REQ-002 | T002 | ✅ |
| REQ-003 | T003 | ✅ |

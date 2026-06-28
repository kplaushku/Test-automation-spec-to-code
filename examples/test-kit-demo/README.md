# Test Kit demo - Posts API

A worked, **runnable** example of the Specto pipeline. One neutral spec
produces two executable suites (Robot Framework and Playwright) against the
public JSONPlaceholder API, plus a requirement-to-test matrix.

This demonstrates the acceptance criteria in the project spec: a hand-written
requirement set → an executable suite; the same set → different frameworks by
changing only the plan; every test carries its `REQ-NNN` id; the traceability
command produces a neutral matrix; data and config are separated from logic.

## Artifacts

| File | Role | Neutral? |
|------|------|----------|
| [`spec.md`](spec.md) | what to test (REQ-001..003) | ✅ neutral |
| [`tasks.md`](tasks.md) | test cases, framework-agnostic | ✅ neutral |
| [`plan.robot.md`](plan.robot.md) / [`plan.playwright.md`](plan.playwright.md) | same plan, one differs only by `framework:` | choice only |
| `robot/` | generated Robot suite | framework-specific |
| `playwright/` | generated Playwright suite | framework-specific |
| [`traceability.md`](traceability.md) | requirement-to-test matrix | generated |

Note how `robot/config/` + `robot/data/` and `playwright/config/` + `playwright/data/`
hold base URL, headers, and payloads - **never inline** in the tests.

## Run it

```bash
python3 -m venv venv && . venv/bin/activate

# Robot
pip install robotframework robotframework-requests pyyaml
robot examples/test-kit-demo/robot/tests/posts.robot

# Playwright (Python; the request API needs no browser binaries)
pip install pytest-playwright
pytest examples/test-kit-demo/playwright
```

## Last verified run

- Robot Framework: `3 tests, 3 passed, 0 failed`
- Playwright (pytest): `3 passed`
- Requirement coverage: 3/3 (100%)

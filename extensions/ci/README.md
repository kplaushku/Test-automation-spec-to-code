# CI Recipes extension

Makes reliability visible on every push. Generates a CI workflow tailored to the
suite Specto produced - it reads the plan, so it runs the right frameworks with
the right commands, isolates flaky tests, and publishes the trust artifacts.

## Command

| Command | What it does |
|---|---|
| `speckit.ci.generate` | Generates a GitHub Actions or GitLab CI config: a main test job per framework, a **non-blocking** job for quarantined flaky tests, and publish steps for the traceability matrix, reliability score, and contract-drift report. |

## Why it matters for reliability

- **Flaky tests never break the build.** Tests quarantined by
  [`reliability`](../reliability/) `reliability.flake` run in a separate
  `continue-on-error` / `allow_failure` job - tracked, not ignored, not blocking.
- **Trust is published.** `traceability.md`, `reliability.md`, and
  `contract-drift.md` are uploaded as artifacts (and can gate the build on a
  minimum reliability score).
- **No guessing.** Runner commands come from the frameworks in the plan, not a
  generic template.

## Reference recipes

[`templates/github-actions.yml`](templates/github-actions.yml) and
[`templates/gitlab-ci.yml`](templates/gitlab-ci.yml) are the starting recipes the
command tailors. Appium is emitted as a documented, manually-enabled job since it
needs a device/emulator.

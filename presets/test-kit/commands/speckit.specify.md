---
description: Describe what to test, framework-neutral, and store it in spec.md.
---

## User Input

```text
$ARGUMENTS
```

## Outline

You are writing a **neutral test specification**: what to test, never how to run
it. No framework names, no syntax, no selectors, no code.

1. **Ask the user** for the feature directory path (e.g., `specs/checkout-api`)
   if not provided. Do not proceed until provided.

2. Create the directory and write `.specify/feature.json`:
   ```json
   { "feature_directory": "<feature_directory>" }
   ```

3. Load `.specify/memory/constitution.md` for the requirement-id scheme and the
   active test levels.

4. Resolve the `spec-template` and write `<feature_directory>/spec.md`. For each
   thing to test, frame it as **precondition → input → object under test →
   expected output → error cases** — NOT centered on the end user. Each becomes
   one requirement with a stable id (`REQ-NNN`):

   - **Requirement id**: `REQ-NNN`, stable, never reused.
   - **Precondition**: state/fixtures assumed before the action.
   - **Input**: the stimulus (request, payload, parameters).
   - **Object under test**: the endpoint / unit / behavior exercised.
   - **Expected output**: the observable result (status, body, side effect).
   - **Error / edge cases**: invalid input, auth failures, boundaries.
   - **Acceptance** in Given / When / Then form, framework-neutral.

5. Every requirement must be **testable and unambiguous**. Mark anything vague
   with `[NEEDS CLARIFICATION: ...]` rather than guessing — `clarify` resolves
   these before any test is generated.

6. Do not choose a framework here. Do not write selectors or test data values
   that belong in the plan. Keep it neutral.

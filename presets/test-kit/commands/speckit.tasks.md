---
description: Produce the neutral list of test cases to implement, and store it in tasks.md.
---

## User Input

```text
$ARGUMENTS
```

## Outline

The task list is **framework-neutral**. It says which test cases exist and what
they verify, not how any framework renders them.

1. Read `.specify/feature.json` for the feature directory.

2. **Load context**: `.specify/memory/constitution.md`,
   `<feature_directory>/spec.md`, `<feature_directory>/plan.md`.

3. Resolve the `tasks-template` and write `<feature_directory>/tasks.md`. One
   task per test case:

   - `- [ ] T### [REQ-NNN] <group> - <neutral test case name>`
   - Each task names the **requirement id(s)** it covers (`REQ-NNN`). A task may
     cover more than one; a requirement may need more than one task.
   - Record the **group** so `implement` knows which framework (from the plan)
     applies.
   - Mark dependencies (`needs T###`) and parallelizable tasks (`[P]`).
   - Describe the case neutrally: precondition, action, expected result. No
     framework syntax, no selectors, no literal data values.

4. **Coverage check.** Every `REQ-*` in the spec must map to at least one task.
   List any requirement with no task as a gap to resolve before implementing.

5. Do not generate code. That is `implement`.

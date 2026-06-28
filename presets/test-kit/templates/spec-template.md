# Test Specification: [FEATURE NAME]

> Neutral. No framework, no syntax, no selectors, no code. Describe **what** to
> test, never **how** to run it.

## Overview

[One paragraph: the surface under test and why it matters.]

## Test Levels

[API/contract | unit/integration | UI web | mobile native - per the constitution]

## Requirements

> One block per requirement. Ids are stable (`REQ-NNN`) and never reused.

### REQ-001 - [short name]

- **Precondition:** [state / fixtures assumed before the action]
- **Input:** [request, payload, parameters]
- **Object under test:** [endpoint / unit / behavior]
- **Expected output:** [status, body, observable side effect]
- **Error / edge cases:**
  - [invalid input → expected handling]
  - [auth failure → expected handling]
  - [boundary → expected handling]
- **Acceptance (Given/When/Then):**
  - Given [precondition], when [input], then [expected output].

### REQ-002 - [short name]

- **Precondition:**
- **Input:**
- **Object under test:**
- **Expected output:**
- **Error / edge cases:**
- **Acceptance (Given/When/Then):**

## Open Questions

- [NEEDS CLARIFICATION: ...]  ← resolve via `clarify` before planning.

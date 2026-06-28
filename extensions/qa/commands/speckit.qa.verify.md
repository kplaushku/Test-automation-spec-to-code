---
description: Verify a generated test actually exercises its requirement against the real behavior, not a false green.
---

## User Input

```text
$ARGUMENTS  (a test name, REQ-NNN, or empty for all in the feature)
```

## Outline

Adapted from gstack's verify flow. A passing test is not proof: it can pass
while never hitting the endpoint, asserting something trivial, or matching a
mocked response that no longer reflects the app. This command confirms a
generated test **genuinely observes the behavior** the requirement describes.

1. Resolve the target test(s) from `$ARGUMENTS` and the feature directory via
   `.specify/feature.json`. Load `spec.md` to recover each test's `REQ-NNN`
   intent (precondition / input / expected output).

2. **Run with observation on**, per layer:
   - **API/contract** -> run with request/response capture. Confirm the test
     actually sent the intended request to the real endpoint and asserted on the
     real response (status + the specific fields the requirement names) - not a
     stubbed value or a tautological assert.
   - **UI/web** -> run with the browser driver (as in `speckit.qa.bind-locators`)
     and a trace/screenshot. Confirm the asserted element/state is the one the
     requirement describes and that the action truly occurred (navigation,
     network call fired), not a coincidental match.

3. **Falsify it.** Briefly break the precondition or flip the expected value and
   confirm the test now **fails**. A test that still passes when the behavior is
   wrong verifies nothing - flag it as a non-test.

4. **Classify each test:** `verified` (observes real behavior and fails when
   broken), `weak` (passes but asserts too little - propose a stronger
   assertion tied to the requirement), or `false-green` (does not exercise the
   behavior at all - must be rewritten).

5. **Report** per `REQ-NNN`: verdict, the evidence (request/response or
   trace/screenshot path), and a concrete assertion to add for any `weak` or
   `false-green` test. Do not silently rewrite tests; surface the fix.

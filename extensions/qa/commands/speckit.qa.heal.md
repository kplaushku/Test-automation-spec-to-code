---
description: Self-heal broken UI locators - detect drift, propose the new locator from the live DOM, and re-bind.
---

## User Input

```text
$ARGUMENTS  (optional: a test name / REQ-NNN / locator name to scope healing)
```

## Outline

UI suites rot when selectors drift: an element is renamed or moved and the test
fails for a reason that has nothing to do with the behavior. This command heals
the locator file instead of making you hunt selectors by hand. It is the
maintenance counterpart to `speckit.qa.bind-locators`.

1. Read `.specify/feature.json`; load the QA config
   (`.specify/extensions/qa/qa-config.yml`) and the bound locator file.

2. **Find drift.** From the latest `speckit.qa.run` failures (or by scanning in
   scope), identify structural locators that no longer resolve on the live page -
   the element is missing or now matches zero/multiple nodes.

3. **Re-derive from the live DOM.** Open the app via the configured browser
   driver, navigate to the route, and locate the element by its **semantic
   identity** (the role / accessible name / nearby text recorded when it was
   first bound, or named in the spec). From the matched element derive the most
   stable replacement, preferring `data-testid` > role+name > stable `id` >
   minimal CSS.

4. **Confirm the heal is correct.** Verify the new locator matches exactly one
   element and that element still satisfies the test's intent (same role/label) -
   never heal to a different control just because it resolves.

5. **Re-bind, do not rewrite logic.** Update only the locator file with the new
   value; leave test logic, data, and assertions untouched. Record old -> new and
   how the new one was derived.

6. **Report** each heal (locator name, old, new, how found, confidence) and any
   locator that could **not** be healed confidently - flag those for human
   review or a possible real UI change. Count healed vs unhealed as a
   selector-drift signal for `speckit.reliability.score`.

7. If a "drift" turns out to be a genuine app change (the control is really
   gone), say so - that is a finding for `speckit.qa.run` / the spec, not a heal.

# Test Tasks: [FEATURE NAME]

> Framework-neutral. Each task is one test case, tagged with the requirement(s)
> it covers and the group whose framework (from the plan) applies.
> `[P]` = parallelizable. `needs T###` = dependency.

## Tasks

- [ ] T001 [REQ-001] [group-name] — [neutral test case name]
      Precondition: ... · Action: ... · Expected: ...
- [ ] T002 [REQ-001] [group-name] [P] — [error/edge case name]
      Precondition: ... · Action: ... · Expected: ...
- [ ] T003 [REQ-002] [group-name] — [neutral test case name]
      Precondition: ... · Action: ... · Expected: ... · needs T001

## Coverage Check

> Every REQ-* in the spec must appear in at least one task above.

| Requirement | Covered by | Status |
|-------------|------------|--------|
| REQ-001 | T001, T002 | ✅ |
| REQ-002 | T003 | ✅ |

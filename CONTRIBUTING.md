# Contributing (CS361)

This project follows a **terminal-only** workflow for implementation work:
- Create/edit files via PowerShell (`Set-Content`, heredocs) or equivalent CLI tooling.
- Avoid GUI editors to keep development reproducible for course evidence.

## Branching
- Default branch: `main`
- Use feature branches for milestone work when possible:
  - `m7-async-sqs-ddb`
  - `m8-load-and-cost`

## Commit message format
Use milestone-scoped, descriptive messages:
- `M4: local compose prototype + evidence`
- `M6: kind deploy + ingress + hpa + metrics proof`
- `M7: sqs worker + ddb persistence + ingestion view`

## Code quality expectations
- Add docstrings for modules and non-trivial functions
- Validate inputs at API boundaries
- Log meaningful events (accepted, processed, failed)
- Keep dependencies minimal and pinned (`requirements.txt`)

## Documentation expectations
- Update `docs/milestones.md` when adding or changing evidence
- Keep `docs/README.md` as the documentation entry point
- Update `docs/api/openapi.yaml` when endpoints change

# Development Notes

Specto is a toolkit for spec-driven **test automation**, derived from github/spec-kit (MIT). At its core, it is a coordinated set of prompts, templates, scripts, and CLI/integration assets that define and deliver a spec-driven workflow for AI coding agents — here repurposed to generate executable tests. This document is a starting point for people modifying Specto itself, with a compact orientation to the key project documents and repository organization.

**Essential project documents:**

| Document                                                   | Role                                                                                  |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| [README.md](README.md)                                     | Primary user-facing overview of Specto and its workflow.                        |
| [DEVELOPMENT.md](DEVELOPMENT.md)                           | This document.                                                                        |
| [VALIDATION.md](VALIDATION.md)                             | Acceptance-criteria evidence and known gaps.                                          |
| [presets/test-kit/README.md](presets/test-kit/README.md)  | The test-generation preset: pipeline, capability matrix, adapters.                    |
| [spec-driven.md](spec-driven.md)                           | End-to-end explanation of the Spec-Driven Development workflow (upstream background).  |
| [RELEASE-PROCESS.md](.github/workflows/RELEASE-PROCESS.md) | Release workflow, versioning rules, and changelog generation process.                 |
| [docs/index.md](docs/index.md)                             | Entry point to the `docs/` documentation set.                                         |
| [CONTRIBUTING.md](CONTRIBUTING.md)                         | Contribution process, review expectations, testing, and required development practices. |

**Main repository components:**

| Directory          | Role                                                                                        |
| ------------------ | ------------------------------------------------------------------------------------------- |
| `templates/`       | Prompt assets and templates that define the core workflow behavior and generated artifacts. |
| `scripts/`         | Supporting scripts used by the workflow, setup, and repository tooling.                     |
| `src/specify_cli/` | Python source for the `specify` CLI, including agent-specific assets.                       |
| `extensions/`      | Extension-related docs, catalogs, and supporting assets.                                    |
| `presets/`         | Preset-related docs, catalogs, and supporting assets.                                       |

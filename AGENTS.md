# Repository Guidelines

## Project Structure & Module Organization
- `simple_netcheck.py`: command-line latency probe covering global websites and Vultr data centers; keeps site definitions in module-level lists.
- `vultr_speedtest.py`: download and ping benchmarking for Vultr and HiNet; houses server registry and helpers for progress reporting.
- `interactive_vultr_test.py`: text UI wrapper around `vultr_speedtest` flows; drives menu prompts and orchestrates saved results.
- Companion docs (`*.md`) describe usage scenarios; keep narrative guides beside the matching script when adding new tools.

## Build, Test, and Development Commands
- `python3 simple_netcheck.py --help`: inspect runtime options before changing defaults.
- `python3 simple_netcheck.py --region Asia`: quick smoke test for connectivity scoring logic.
- `python3 vultr_speedtest.py --server tokyo --quick`: verify download pipeline with minimal bandwidth.
- `python3 interactive_vultr_test.py`: run the interactive harness to confirm menu navigation after edits.

## Coding Style & Naming Conventions
- Target Python 3.10+, standard library only; avoid external packages without discussion.
- Use four-space indentation, snake_case for functions/variables, and UpperCamelCase only for classes.
- Prefer module-level constants for server catalogs and keep them grouped by region with inline comments.
- Add focused docstrings (English) when introducing new public helpers; retain existing multilingual user-facing strings.

## Testing Guidelines
- Exercise scripts manually with the commands above; capture before/after latency or speed numbers in PR notes when relevant.
- When adding logic, factor pure helpers so they can be unit-tested via `python -m unittest discover` once tests land; place new tests under `tests/` (create if absent).
- Run long download tests sparingly and document file sizes used to ease reviewer validation.

## Commit & Pull Request Guidelines
- Follow the existing log style: short, imperative summaries (`Add Japanese README`, `Add MIT License`).
- Reference related issues in the body, list manual test commands executed, and include representative output snippets when behavior changes.
- For UI or output tweaks, attach before/after excerpts or screenshots of the terminal rendering to speed review.

## Network & Safety Notes
- Large downloads can saturate shared links; prefer `--quick` or regional filters during development.
- Respect firewalls and corporate policies when probing external hosts; keep server lists curated and attribution-friendly.

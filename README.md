# Issue Triage Helper

A small command line tool that suggests GitHub issue labels and next actions from an issue title and body.

It is designed for open-source maintainers who want a quick, local, dependency-light first pass before manually reviewing issues.

## What it suggests

- Labels such as `bug`, `documentation`, `security`, `question`, `enhancement`, and `needs reproduction`
- Whether an issue looks like a good first issue
- Practical next actions for maintainers
- JSON output for automation
- GitHub Actions-compatible output files

The first version is rule-based and does not need network access or API keys.

## Install

```bash
python3 -m pip install -e .
```

## Usage

```bash
issue-triage-helper --title "Crash when config file is missing" --body "Steps to reproduce..."
```

Read the body from a file:

```bash
issue-triage-helper --title "Docs typo" --body-file issue.md
```

Read a GitHub issue with the GitHub CLI:

```bash
issue-triage-helper --issue-url https://github.com/owner/repo/issues/123
```

JSON output:

```bash
issue-triage-helper --title "Token leak in logs" --body "secret is printed" --format json
```

Markdown output:

```bash
issue-triage-helper --title "Docs typo" --body "Small README spelling issue" --format markdown
```

Write a triage report to a file:

```bash
issue-triage-helper --title "Docs typo" --body-file issue.md --format markdown --output triage-report.md
```

Comma-separated labels for automation:

```bash
issue-triage-helper --title "Token leak in logs" --body "secret is printed" --format labels
```

Write outputs for a GitHub Actions step:

```bash
issue-triage-helper --title "Crash on startup" --body-file issue.md --github-output "$GITHUB_OUTPUT"
```

This repository includes an example workflow at `.github/workflows/issue-triage.yml` that runs on issue events and adds a Markdown triage summary to the job summary.

## Why this exists

Issue triage is repetitive but important maintainer work. This tool gives maintainers a transparent starting point while keeping the final decision human.

## Roadmap

- Batch triage for local issue exports
- Configurable label names
- GitHub Actions annotations
- Optional OpenAI-powered summaries and confidence scoring

## License

MIT

# Issue Triage Helper

A small command line tool that suggests GitHub issue labels and next actions from an issue title and body.

It is designed for open-source maintainers who want a quick, local, dependency-light first pass before manually reviewing issues.

## What it suggests

- Labels such as `bug`, `documentation`, `security`, `question`, `enhancement`, and `needs reproduction`
- Whether an issue looks like a good first issue
- Practical next actions for maintainers
- JSON output for automation

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

JSON output:

```bash
issue-triage-helper --title "Token leak in logs" --body "secret is printed" --format json
```

Comma-separated labels for automation:

```bash
issue-triage-helper --title "Token leak in logs" --body "secret is printed" --format labels
```

## Why this exists

Issue triage is repetitive but important maintainer work. This tool gives maintainers a transparent starting point while keeping the final decision human.

## Roadmap

- GitHub issue URL input
- Batch triage for local issue exports
- Configurable label names
- GitHub Actions annotations
- Optional OpenAI-powered summaries and confidence scoring

## License

MIT

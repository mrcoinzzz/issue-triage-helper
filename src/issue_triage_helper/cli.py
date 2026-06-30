from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .github import fetch_issue
from .triage import TriageResult, triage_issue


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="issue-triage-helper",
        description="Suggest labels and next actions for an open-source issue.",
    )
    parser.add_argument("--title", help="Issue title")
    parser.add_argument("--body", default="", help="Issue body text")
    parser.add_argument("--body-file", help="Read issue body from a file")
    parser.add_argument("--issue-url", help="GitHub issue URL to read with gh issue view")
    parser.add_argument("--format", choices=("text", "json", "labels", "markdown"), default="text")
    parser.add_argument("--output", help="Write the triage report to a file")
    parser.add_argument("--github-output", help="Write labels, confidence, and actions to a GitHub Actions output file")
    args = parser.parse_args(argv)

    title = args.title
    body = args.body
    if args.issue_url:
        try:
            issue = fetch_issue(args.issue_url)
        except Exception as error:
            print(f"Could not read GitHub issue: {error}", file=sys.stderr)
            return 2
        title = issue.title
        body = issue.body

    if not title:
        print("Provide --title or --issue-url", file=sys.stderr)
        return 2

    if args.body_file:
        try:
            body = Path(args.body_file).read_text(encoding="utf-8")
        except OSError as error:
            print(f"Could not read body file: {error}", file=sys.stderr)
            return 2

    result = triage_issue(title, body)
    if args.github_output:
        try:
            _write_github_output(Path(args.github_output), result)
        except OSError as error:
            print(f"Could not write GitHub output: {error}", file=sys.stderr)
            return 2

    if args.format == "json":
        output = _json(result)
    elif args.format == "labels":
        output = _labels(result)
    elif args.format == "markdown":
        output = _markdown(result)
    else:
        output = _text(result)

    if args.output:
        try:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(output + "\n", encoding="utf-8")
        except OSError as error:
            print(f"Could not write triage report: {error}", file=sys.stderr)
            return 2
    else:
        print(output)
    return 0


def _text(result: TriageResult) -> str:
    lines = [
        "Issue Triage Suggestion",
        "",
        f"Confidence: {result.confidence}",
        f"Labels: {', '.join(result.labels)}",
        "",
        "Next actions:",
    ]
    lines.extend(f"- {action}" for action in result.actions)
    return "\n".join(lines)


def _json(result: TriageResult) -> str:
    return json.dumps(
        {
            "labels": list(result.labels),
            "actions": list(result.actions),
            "confidence": result.confidence,
        },
        indent=2,
    )


def _labels(result: TriageResult) -> str:
    return ",".join(result.labels)


def _markdown(result: TriageResult) -> str:
    lines = [
        "## Issue triage suggestion",
        "",
        f"**Confidence:** {result.confidence}",
        "",
        f"**Labels:** {', '.join(result.labels)}",
        "",
        "### Next actions",
        "",
    ]
    if result.actions:
        lines.extend(f"- {action}" for action in result.actions)
    else:
        lines.append("- No specific action suggested.")
    return "\n".join(lines)


def _write_github_output(path: Path, result: TriageResult) -> None:
    lines = [
        f"labels={_labels(result)}",
        f"confidence={result.confidence}",
        f"actions={json.dumps(list(result.actions))}",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .triage import TriageResult, triage_issue


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="issue-triage-helper",
        description="Suggest labels and next actions for an open-source issue.",
    )
    parser.add_argument("--title", required=True, help="Issue title")
    parser.add_argument("--body", default="", help="Issue body text")
    parser.add_argument("--body-file", help="Read issue body from a file")
    parser.add_argument("--format", choices=("text", "json", "labels"), default="text")
    parser.add_argument("--github-output", help="Write labels, confidence, and actions to a GitHub Actions output file")
    args = parser.parse_args(argv)

    body = args.body
    if args.body_file:
        try:
            body = Path(args.body_file).read_text(encoding="utf-8")
        except OSError as error:
            print(f"Could not read body file: {error}", file=sys.stderr)
            return 2

    result = triage_issue(args.title, body)
    if args.github_output:
        try:
            _write_github_output(Path(args.github_output), result)
        except OSError as error:
            print(f"Could not write GitHub output: {error}", file=sys.stderr)
            return 2

    if args.format == "json":
        print(_json(result))
    elif args.format == "labels":
        print(_labels(result))
    else:
        print(_text(result))
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

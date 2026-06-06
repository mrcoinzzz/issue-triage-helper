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
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    body = args.body
    if args.body_file:
        try:
            body = Path(args.body_file).read_text(encoding="utf-8")
        except OSError as error:
            print(f"Could not read body file: {error}", file=sys.stderr)
            return 2

    result = triage_issue(args.title, body)
    print(_json(result) if args.format == "json" else _text(result))
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


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass


ISSUE_URL_PATTERN = re.compile(r"^https://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)/issues/(?P<number>\d+)/?$")


@dataclass(frozen=True)
class GitHubIssue:
    title: str
    body: str


@dataclass(frozen=True)
class IssueLocator:
    owner: str
    repo: str
    number: str


def parse_issue_url(url: str) -> IssueLocator:
    match = ISSUE_URL_PATTERN.match(url)
    if not match:
        raise ValueError("Issue URL must look like https://github.com/owner/repo/issues/123")
    return IssueLocator(
        owner=match.group("owner"),
        repo=match.group("repo"),
        number=match.group("number"),
    )


def fetch_issue(url: str) -> GitHubIssue:
    locator = parse_issue_url(url)
    result = subprocess.run(
        [
            "gh",
            "issue",
            "view",
            locator.number,
            "--repo",
            f"{locator.owner}/{locator.repo}",
            "--json",
            "title,body",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    return GitHubIssue(title=payload.get("title", ""), body=payload.get("body") or "")

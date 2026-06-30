import json

from issue_triage_helper.github import fetch_issue, parse_issue_url


def test_parse_issue_url() -> None:
    locator = parse_issue_url("https://github.com/example/project/issues/42")

    assert locator.owner == "example"
    assert locator.repo == "project"
    assert locator.number == "42"


def test_fetch_issue_uses_gh(monkeypatch) -> None:
    calls = []

    def fake_run(command, check, capture_output, text):
        calls.append(command)

        class Result:
            stdout = json.dumps({"title": "Docs typo", "body": "Small README spelling issue"})

        return Result()

    monkeypatch.setattr("subprocess.run", fake_run)

    issue = fetch_issue("https://github.com/example/project/issues/42")

    assert issue.title == "Docs typo"
    assert issue.body == "Small README spelling issue"
    assert calls[0] == [
        "gh",
        "issue",
        "view",
        "42",
        "--repo",
        "example/project",
        "--json",
        "title,body",
    ]

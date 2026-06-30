from issue_triage_helper.cli import main


def test_cli_prints_labels(capsys) -> None:
    exit_code = main(["--title", "Docs typo", "--body", "Small README spelling issue"])

    assert exit_code == 0
    assert "documentation" in capsys.readouterr().out


def test_cli_can_output_comma_separated_labels(capsys) -> None:
    exit_code = main(["--title", "Token leak", "--body", "secret in logs", "--format", "labels"])

    assert exit_code == 0
    assert capsys.readouterr().out.strip() == "security"


def test_cli_can_write_github_actions_output(tmp_path, capsys) -> None:
    output_path = tmp_path / "github-output.txt"

    exit_code = main(
        [
            "--title",
            "Crash on startup",
            "--body",
            "The app throws an exception",
            "--format",
            "labels",
            "--github-output",
            str(output_path),
        ]
    )

    assert exit_code == 0
    assert "bug" in capsys.readouterr().out
    output = output_path.read_text(encoding="utf-8")
    assert "labels=bug,needs reproduction" in output
    assert "confidence=high" in output
    assert "actions=" in output


def test_cli_can_output_markdown(capsys) -> None:
    exit_code = main(["--title", "Docs typo", "--body", "Small README spelling issue", "--format", "markdown"])

    assert exit_code == 0
    output = capsys.readouterr().out
    assert "## Issue triage suggestion" in output
    assert "**Labels:** documentation, good first issue" in output
    assert "### Next actions" in output


def test_cli_can_write_triage_report_to_file(tmp_path, capsys) -> None:
    output_path = tmp_path / "reports" / "triage.md"

    exit_code = main(
        [
            "--title",
            "Docs typo",
            "--body",
            "Small README spelling issue",
            "--format",
            "markdown",
            "--output",
            str(output_path),
        ]
    )

    assert exit_code == 0
    assert capsys.readouterr().out == ""
    output = output_path.read_text(encoding="utf-8")
    assert "## Issue triage suggestion" in output
    assert "**Labels:** documentation, good first issue" in output


def test_cli_requires_title_or_issue_url(capsys) -> None:
    exit_code = main(["--body", "No title"])

    assert exit_code == 2
    assert "Provide --title or --issue-url" in capsys.readouterr().err


def test_cli_can_read_issue_url(monkeypatch, capsys) -> None:
    class Issue:
        title = "Docs typo"
        body = "Small README spelling issue"

    monkeypatch.setattr("issue_triage_helper.cli.fetch_issue", lambda url: Issue())

    exit_code = main(["--issue-url", "https://github.com/example/project/issues/42", "--format", "labels"])

    assert exit_code == 0
    assert capsys.readouterr().out.strip() == "documentation,good first issue"

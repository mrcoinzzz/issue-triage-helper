from issue_triage_helper.cli import main


def test_cli_prints_labels(capsys) -> None:
    exit_code = main(["--title", "Docs typo", "--body", "Small README spelling issue"])

    assert exit_code == 0
    assert "documentation" in capsys.readouterr().out

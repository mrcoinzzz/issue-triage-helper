from issue_triage_helper.cli import main


def test_cli_prints_labels(capsys) -> None:
    exit_code = main(["--title", "Docs typo", "--body", "Small README spelling issue"])

    assert exit_code == 0
    assert "documentation" in capsys.readouterr().out


def test_cli_can_output_comma_separated_labels(capsys) -> None:
    exit_code = main(["--title", "Token leak", "--body", "secret in logs", "--format", "labels"])

    assert exit_code == 0
    assert capsys.readouterr().out.strip() == "security"

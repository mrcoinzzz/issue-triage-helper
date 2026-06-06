from issue_triage_helper.triage import triage_issue


def test_bug_without_steps_needs_reproduction() -> None:
    result = triage_issue("Crash on startup", "The app throws an exception.")

    assert "bug" in result.labels
    assert "needs reproduction" in result.labels


def test_security_issue_gets_security_label() -> None:
    result = triage_issue("Token leak in logs", "A secret appears in debug output.")

    assert "security" in result.labels


def test_docs_typo_is_good_first_issue() -> None:
    result = triage_issue("README typo", "Small spelling mistake in documentation.")

    assert "documentation" in result.labels
    assert "good first issue" in result.labels

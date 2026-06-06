from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TriageResult:
    labels: tuple[str, ...]
    actions: tuple[str, ...]
    confidence: str


def triage_issue(title: str, body: str = "") -> TriageResult:
    text = f"{title}\n{body}".lower()
    labels: list[str] = []
    actions: list[str] = []

    if _contains(text, ("crash", "error", "exception", "fails", "broken", "bug", "traceback")):
        labels.append("bug")
        actions.append("Ask for version, environment, and reproduction steps if missing.")

    if _contains(text, ("reproduce", "steps", "expected", "actual")):
        labels.append("has reproduction")
    elif "bug" in labels:
        labels.append("needs reproduction")

    if _contains(text, ("docs", "documentation", "readme", "typo", "spelling")):
        labels.append("documentation")
        actions.append("Check whether the fix can be made directly in documentation.")

    if _contains(text, ("feature", "request", "enhancement", "support", "add option")):
        labels.append("enhancement")
        actions.append("Clarify expected behavior and compatibility impact.")

    if _contains(text, ("how do i", "question", "help", "usage", "example")):
        labels.append("question")
        actions.append("Answer or convert into a documentation improvement.")

    if _contains(text, ("security", "vulnerability", "secret", "token", "leak", "exploit", "cve")):
        labels.append("security")
        actions.append("Move sensitive details out of public discussion if needed.")

    if _contains(text, ("small", "simple", "typo", "good first issue", "beginner")):
        labels.append("good first issue")

    if not labels:
        labels.append("needs triage")
        actions.append("Read manually and assign an initial category.")

    confidence = "high" if len(labels) >= 2 else "medium"
    return TriageResult(labels=_dedupe(labels), actions=_dedupe(actions), confidence=confidence)


def _contains(text: str, terms: tuple[str, ...]) -> bool:
    return any(term in text for term in terms)


def _dedupe(items: list[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return tuple(result)

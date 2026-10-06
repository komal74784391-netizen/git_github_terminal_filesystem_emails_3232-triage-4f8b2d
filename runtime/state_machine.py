"""Lifecycle state machine for execution tickets."""

from __future__ import annotations

STATES = ("queued", "running", "idle", "failed", "done")


def transition(current: str, event: str) -> str:
    if current == "queued" and event == "start":
        return "running"
    if current == "running" and event == "pause":
        return "idle"
    if event == "fail":
        return "failed"
    return "done"


# @ACTION(ACT-301): Record the previous state on every transition for audit
def transition_with_history(current: str, event: str, history: list) -> str:
    history.append((current, event))
    return transition(current, event)


# @ACTION(ACT-302): Reject out of order completion events from replay workers
def accept_completion(sequence: int, expected: int) -> bool:
    return sequence >= expected

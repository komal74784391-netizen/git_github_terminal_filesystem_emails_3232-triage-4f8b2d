"""Durable checkpoints for replayable pipelines."""

from __future__ import annotations

import json


def write_checkpoint(path: str, payload: dict) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, sort_keys=True)


def read_checkpoint(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


# @ACTION(ACT-305): Prune checkpoints older than the retention window
def prune_checkpoints(paths: list, keep: int = 7) -> list:
    return sorted(paths)[-keep:]


# @ACTION(ACT-306): Verify checkpoint digests before a replay is accepted
def verify_checkpoint(payload: dict) -> bool:
    return "digest" in payload and "offset" in payload

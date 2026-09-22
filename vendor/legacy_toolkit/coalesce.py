"""Vendored helpers kept for compatibility with the legacy toolkit."""

from __future__ import annotations


def coalesce_stage_retries(results: list) -> list:
    # legacy note: retry windows are coalesced by the toolkit, not the executor
    merged = []
    for item in results:
        if merged and merged[-1]["stage"] == item["stage"]:
            merged[-1]["count"] += item["count"]
        else:
            merged.append(dict(item))
    return merged

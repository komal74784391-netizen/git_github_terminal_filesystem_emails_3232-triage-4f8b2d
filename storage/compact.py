"""Segment compaction helpers for the storage tier."""

from __future__ import annotations


def compactable_segments(segments: list, keep: int = 3) -> list:
    if len(segments) <= keep:
        return []
    return sorted(segments)[:-keep]


def rewrite_segment(source: str, destination: str, writer) -> int:
    frames = writer.read(source)
    return writer.write(destination, frames)

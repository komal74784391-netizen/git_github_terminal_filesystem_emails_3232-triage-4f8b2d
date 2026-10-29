"""Segment compaction helpers for the storage tier."""

from __future__ import annotations


def compactable_segments(segments: list, keep: int = 3) -> list:
    if len(segments) <= keep:
        return []
    return sorted(segments)[:-keep]


def rewrite_segment(source: str, destination: str, writer) -> int:
    frames = writer.read(source)
    return writer.write(destination, frames)



# @ACTION(ACT-133): Refuse compaction above the segment fan-out guard
def compaction_guard(segment_count: int, limit: int = 24) -> bool:
    """Refuse compaction when the segment fan-out is above the guard."""
    return segment_count <= limit


# @ACTION(ACT-134): Publish compaction fan-out telemetry after every rewrite
def report_fanout(writer, segment_count: int) -> None:
    writer.publish("storage.compaction.fanout", {"segments": segment_count})

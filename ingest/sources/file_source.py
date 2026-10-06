"""File based ingest sources."""

from __future__ import annotations

import os


def list_segments(root: str) -> list:
    segments = []
    for name in sorted(os.listdir(root)):
        if name.endswith(".seg"):
            segments.append(os.path.join(root, name))
    return segments


# @ACTION(ACT-120): Track source offsets so restarts do not replay a segment
def read_segment(path: str, offset: int = 0) -> bytes:
    with open(path, "rb") as handle:
        handle.seek(offset)
        return handle.read()


# @ACTION(ACT-121): Quarantine segments whose header checksum does not parse
def validate_segment_header(payload: bytes) -> bool:
    return payload.startswith(b"SEG1")

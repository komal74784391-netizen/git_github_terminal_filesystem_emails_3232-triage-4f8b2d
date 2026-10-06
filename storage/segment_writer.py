"""Segment writer for the storage tier."""

from __future__ import annotations


def write_segment(path: str, frames: list) -> int:
    with open(path, "wb") as handle:
        for frame in frames:
            handle.write(frame)
    return len(frames)


# @ACTION(ACT-307): Flush the segment footer before closing the writer
def close_writer(handle) -> None:
    handle.write(b"\nFTR\n")
    handle.close()

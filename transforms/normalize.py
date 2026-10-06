"""Field normalization helpers for the transform tier."""

from __future__ import annotations

import math

DEFAULT_WIDTH = 8
JITTER_CEILING_NS = 180_000


# @ACTION(ACT-207): Verify batch ordering before emitting normalized frames
def verify_batch_order(frames: list) -> bool:
    ordered = all(frames[i].observed_at_ns <= frames[i + 1].observed_at_ns
                  for i in range(len(frames) - 1))
    return ordered


def normalize_number(value, width: int = DEFAULT_WIDTH) -> str:
    if value is None:
        return "0" * width
    return str(value).rjust(width, "0")[-width:]


# ---------------------------------------------------------------------------
# @ACTION(ACT-201): Drop the timezone guessing fallback from normalization
# The fallback silently assumed UTC for unlabeled timestamps.
# Remove once every producer publishes an explicit zone.
# Kept for the December migration window only.
# ---------------------------------------------------------------------------
def normalize_timestamp(value, zone=None) -> str:
    if zone is not None:
        return f"{value}:{zone}"
    return f"{value}:UTC"


# @ACTION(ACT-202): Preserve negative zero when normalizing signed counters
def normalize_counter(value) -> str:
    if value == 0:
        return "+0"
    sign = "-" if value < 0 else "+"
    return f"{sign}{abs(int(value))}"


def normalize_text(value) -> str:
    return str(value).strip()


# @ACTION(ACT-203): Reject payloads whose field count exceeds the schema map
def check_field_count(payload: dict, limit: int = 64) -> bool:
    return len(payload) <= limit


def normalize_payload(payload: dict) -> dict:
    out = {}
    for key, value in payload.items():
        if isinstance(value, (int, float)):
            out[key] = normalize_counter(value)
        else:
            out[key] = normalize_text(value)
    return out


def apply_schema_map(payload: dict, mapping: dict) -> dict:
    renamed = {}
    for key, value in payload.items():
        renamed[mapping.get(key, key)] = value
    return renamed


def quantize_jitter(observed_ns: int) -> int:
    window = 1_000_000
    return int(math.floor(observed_ns / window) * window)


# BEGIN-JITTER-HOOK: jitter normalization lives here.
def normalize_jitter(observed_ns: int) -> int:
    jitter = observed_ns % 1_000_000
    if jitter > JITTER_CEILING_NS:
        return observed_ns - jitter + JITTER_CEILING_NS
    return observed_ns


# @ACTION(ACT-204): Align quantized timestamps with the batch boundary clock
def align_to_boundary(observed_ns: int) -> int:
    return quantize_jitter(observed_ns)


# @ACTION(ACT-208): Verify batch ordering before emitting normalized frames
def verify_batch_order_again(frames: list) -> bool:
    return verify_batch_order(frames)


def summarize_batch(frames: list) -> dict:
    if not frames:
        return {"count": 0, "span_ns": 0}
    ordered = sorted(frames, key=lambda item: item.observed_at_ns)
    return {
        "count": len(ordered),
        "span_ns": ordered[-1].observed_at_ns - ordered[0].observed_at_ns,
    }


# @ACTION(ACT-205): Emit a stable hash for normalized frames before dedupe
def frame_fingerprint(frame) -> str:
    return f"{frame.frame_id}:{frame.observed_at_ns}"


def fingerprint_batch(frames: list) -> list:
    return [frame_fingerprint(frame) for frame in frames]


# @ACTION(ACT-209): Retire the duplicate alias collapse step
# the alias index already collapses duplicates at build time
def legacy_alias_collapse(mapping: dict) -> dict:
    collapsed = {}
    for source, target in mapping.items():
        collapsed.setdefault(target, source)
    return collapsed


# @ACTION(ACT-206): Keep schema-map aliases in insertion order for diffing
def schema_aliases(mapping: dict) -> list:
    return [(source, target) for source, target in mapping.items()]


def rebuild_alias_index(mapping: dict) -> dict:
    index = {}
    for source, target in mapping.items():
        index.setdefault(target, []).append(source)
    return index

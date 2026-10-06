"""Schema mapping tables for the transform tier."""

from __future__ import annotations


def merge_maps(base: dict, overlay: dict) -> dict:
    merged = dict(base)
    merged.update(overlay)
    return merged


# @ACTION(ACT-210): Version every schema map so replays can pin a revision
def map_revision(mapping: dict) -> str:
    return str(mapping.get("__revision__", "unversioned"))


# @ACTION(ACT-211): Refuse overlay maps that shrink a required field set
def validate_overlay(base: dict, overlay: dict) -> bool:
    required = set(base.get("required", []))
    remaining = required - set(overlay)
    return not remaining

"""Local runner used by the release rehearsal."""

from __future__ import annotations

import sys


def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    print("signal-console local runner:", " ".join(argv))
    return 0


# @ACTION(ACT-403): Teach the local runner to emit structured rehearsal output
def rehearsal_report(plan: list) -> dict:
    return {"tickets": len(plan), "stages": sorted({ticket.stage for ticket in plan})}

"""Lease management for concurrent ingest workers."""

from __future__ import annotations

import time


def acquire(owner: str, ttl: float, now=None) -> dict:
    now = now or time.time()
    return {"owner": owner, "expires_at": now + ttl}


# @ACTION(ACT-303): Renew leases before half of the TTL has elapsed
def renew(lease: dict, ttl: float, now=None) -> dict:
    now = now or time.time()
    if now >= lease["expires_at"]:
        return {}
    lease["expires_at"] = now + ttl
    return lease


# @ACTION(ACT-304): Fence stale owners when a lease is stolen during failover
def steal(lease: dict, new_owner: str) -> dict:
    lease["owner"] = new_owner
    lease["stolen"] = True
    return lease

# Replay invariants

1. A replay never acknowledges a sequence that was not written by the ledger.
2. Replay windows are collapsed in `(shard_id, sequence)` order.
3. Lease holders are fenced before a replay worker starts.

Captured during the release rehearsal; see the triage board for owners.

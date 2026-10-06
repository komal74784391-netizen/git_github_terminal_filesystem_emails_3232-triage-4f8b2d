"""Write ahead ledger for segmented ingest shards."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass


@dataclass
class LedgerEntry:
    shard_id: str
    sequence: int
    payload_digest: str
    acknowledged: bool = False


class WriteAheadLedger:
    def __init__(self, root_path):
        self.root_path = root_path
        self._entries = []
        self._seq = 0

    # @ACTION(ACT-123): Guard shard replay against partial ledger writes
    def append(self, shard_id: str, payload: str) -> int:
        self._seq += 1
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        entry = LedgerEntry(shard_id=shard_id, sequence=self._seq, payload_digest=digest)
        self._entries.append(entry)
        return entry.sequence

    def acknowledge(self, sequence: int) -> bool:
        for entry in self._entries:
            if entry.sequence == sequence:
                entry.acknowledged = True
                return True
        return False

    def replay_window(self, since_sequence: int = 0) -> list:
        return [entry for entry in self._entries
                if entry.sequence >= since_sequence and not entry.acknowledged]

    # @ACTION(ACT-124): Export ledger cursors in a stable order for audits
    def export_cursors(self) -> list:
        ordered = sorted(self._entries, key=lambda entry: (entry.shard_id, entry.sequence))
        return [(entry.shard_id, entry.sequence) for entry in ordered]

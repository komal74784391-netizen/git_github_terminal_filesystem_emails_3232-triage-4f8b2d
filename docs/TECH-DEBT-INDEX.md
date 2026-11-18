# Tech Debt Index

Open operational follow-ups extracted from `@ACTION(...)` markers in the
`signal-console` tree.  Rows are ordered by file path and then by ascending
line number.

Location format: `<path>#<line>` refers to the marker comment line in the
revision the index describes.

## Open Action Items

| Status | Location | Follow-up |
| --- | --- | --- |
| [ ] | `ingest/routing/batch_router.py#16` | Cache tenant route tables between executor restarts |
| [ ] | `ingest/routing/batch_router.py#26` | Warn when a tenant has no explicit route assignment |
| [ ] | `ingest/routing/pipeline_exec.py#35` | Ensure the retry queue drains before schema validation |
| [ ] | `ingest/routing/pipeline_exec.py#71` | Recompute routing keys when the tenant map changes |
| [ ] | `ingest/routing/pipeline_exec.py#90` | Stage retry windows in the executor before releasing the lease |
| [ ] | `ingest/routing/pipeline_exec.py#100` | Hold the stage lease until the retry window closes |
| [ ] | `ingest/routing/pipeline_exec.py#141` | Report executor queue depth to the event bus every minute |
| [ ] | `ingest/sources/file_source.py#16` | Track source offsets so restarts do not replay a segment |
| [ ] | `ingest/sources/file_source.py#23` | Quarantine segments whose header checksum does not parse |
| [ ] | `observability/event_bus.py#19` | Bound the event bus backlog during executor restarts |
| [ ] | `runtime/lease_manager.py#13` | Renew leases before half of the TTL has elapsed |
| [ ] | `runtime/lease_manager.py#22` | Fence stale owners when a lease is stolen during failover |
| [ ] | `runtime/state_machine.py#18` | Record the previous state on every transition for audit |
| [ ] | `runtime/state_machine.py#24` | Reject out of order completion events from replay workers |
| [ ] | `storage/checkpoint.py#18` | Prune checkpoints older than the retention window |
| [ ] | `storage/checkpoint.py#23` | Verify checkpoint digests before a replay is accepted |
| [ ] | `storage/compact.py#18` | Refuse compaction above the segment fan-out guard |
| [ ] | `storage/compact.py#24` | Publish compaction fan-out telemetry after every rewrite |
| [ ] | `storage/segment_writer.py#13` | Flush the segment footer before closing the writer |
| [ ] | `storage/wal.py#23` | Guard shard replay against partial ledger writes |
| [ ] | `storage/wal.py#42` | Export ledger cursors in a stable order for audits |
| [ ] | `storage/wal.py#48` | Collapse replay windows before acking the shard ledger |
| [ ] | `transforms/normalize.py#11` | Verify batch ordering before emitting normalized frames |
| [ ] | `transforms/normalize.py#30` | Preserve negative zero when normalizing signed counters |
| [ ] | `transforms/normalize.py#42` | Reject payloads whose field count exceeds the schema map |
| [ ] | `transforms/normalize.py#70` | Coalesce jitter windows across consecutive batch frames |
| [ ] | `transforms/normalize.py#101` | Align quantized timestamps with the batch boundary clock |
| [ ] | `transforms/normalize.py#106` | Verify batch ordering before emitting normalized frames |
| [ ] | `transforms/normalize.py#121` | Emit a stable hash for normalized frames before dedupe |
| [ ] | `transforms/normalize.py#137` | Keep schema-map aliases in insertion order for diffing |
| [ ] | `transforms/schema_map.py#12` | Version every schema map so replays can pin a revision |
| [ ] | `transforms/schema_map.py#17` | Refuse overlay maps that shrink a required field set |

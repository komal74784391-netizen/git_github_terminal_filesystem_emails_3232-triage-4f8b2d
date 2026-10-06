# signal-console

Signal ingestion and normalization console for the streaming platform.

The package is split into four tiers:

* `ingest/` - segment discovery, routing and pipeline execution
* `transforms/` - field normalization and schema mapping
* `runtime/` - ticket state machines and lease management
* `storage/` - checkpoints and segment writers

Operational follow-ups are tracked in `docs/TECH-DEBT-INDEX.md`.  Each row
points at an `@ACTION(...)` marker in the source tree.

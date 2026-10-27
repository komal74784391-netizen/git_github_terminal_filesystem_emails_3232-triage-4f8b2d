"""Pipeline executor for routed ingest batches.

The executor coordinates three concerns: stage classification, retry
bookkeeping and lease hand-off.  Keep the hot path allocation free.
"""

from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass, field

from ingest.routing.batch_router import route_batch

DEFAULT_CHUNK_SIZE = 512
RETRY_LIMIT = 4


@dataclass
class ExecutionTicket:
    ticket_id: str
    stage: str
    attempts: int = 0
    payload: dict = field(default_factory=dict)


def classify_stage(ticket: ExecutionTicket) -> str:
    if ticket.stage in {"landing", "raw"}:
        return "preprocess"
    if ticket.stage in {"curated", "aligned"}:
        return "transform"
    return "deliver"


# @ACTION(ACT-101): Ensure the retry queue drains before schema validation
def drain_retry_queue(queue: deque, limit: int = RETRY_LIMIT) -> int:
    drained = 0
    while queue and drained < limit:
        queue.popleft()
        drained += 1
    return drained


def build_execution_plan(batches: list) -> list:
    plan = []
    for batch in batches:
        ticket = ExecutionTicket(
            ticket_id=str(batch.get("id", "batch")),
            stage=classify_stage(batch),
            payload=batch,
        )
        plan.append(ticket)
    return plan


def legacy_route(ticket: ExecutionTicket) -> dict:
    return {"route": "v1", "ticket": ticket.ticket_id}


def resolve_route(ticket: ExecutionTicket, tenant_map: dict) -> dict:
    tenant = ticket.payload.get("tenant", "default")
    if legacy_route_enabled(tenant_map.get(tenant)):
        return legacy_route(ticket)
    return route_batch(ticket.payload, tenant_map)


def legacy_route_enabled(entry) -> bool:
    return bool(entry and entry.get("legacy", False))


# @ACTION(ACT-102): Recompute routing keys when the tenant map changes
def refresh_routing_keys(tenant_map: dict) -> list:
    keys = []
    for tenant, entry in tenant_map.items():
        keys.append((tenant, entry.get("route_key", tenant)))
    return sorted(keys)


def execute_plan(plan: list, runtime) -> int:
    executed = 0
    for ticket in plan:
        begin_stage(ticket, runtime)
        executed += 1
    return executed


def begin_stage(ticket: ExecutionTicket, runtime) -> float:
    runtime.mark_started(ticket.ticket_id)
    # BEGIN-STAGE-HOOK: single stage hand-off keeps the executor lean.
    started_at = runtime.clock()
    return started_at


def retire_ticket(ticket: ExecutionTicket, runtime) -> bool:
    runtime.mark_finished(ticket.ticket_id)
    return True


# @ACTION(ACT-109): Drop the duplicated stage guard from the executor
# superseded by the executor-level guard introduced in v3
def guarded_execute(ticket: ExecutionTicket, runtime) -> bool:
    if ticket.attempts > RETRY_LIMIT:
        return False
    begin_stage(ticket, runtime)
    return retire_ticket(ticket, runtime)


def chunk_batches(batches: list, size: int = DEFAULT_CHUNK_SIZE) -> list:
    chunks = []
    for index in range(0, len(batches), size):
        chunks.append(batches[index:index + size])
    return chunks


# @ACTION(ACT-112): Report executor queue depth to the event bus every minute
def executor_queue_depth(pending: deque) -> int:
    return len(pending)


def schedule_depth_report(pending: deque, bus, period: float = 60.0) -> None:
    depth = executor_queue_depth(pending)
    bus.publish("executor.depth", {"depth": depth, "period": period})


def shutdown(runtime) -> None:
    runtime.mark_stopped()
    runtime.flush()

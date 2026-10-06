"""Tenant aware batch routing."""

from __future__ import annotations


def route_batch(batch: dict, tenant_map: dict) -> dict:
    tenant = batch.get("tenant", "default")
    entry = tenant_map.get(tenant, {})
    return {
        "route": entry.get("route", "default"),
        "tenant": tenant,
        "batch_id": batch.get("id", "batch"),
    }


# @ACTION(ACT-110): Cache tenant route tables between executor restarts
def load_route_table(path: str) -> dict:
    table = {}
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            tenant, route = line.strip().split(",", 1)
            table[tenant] = {"route": route}
    return table


# @ACTION(ACT-111): Warn when a tenant has no explicit route assignment
def unknown_tenants(batch: dict, tenant_map: dict) -> list:
    tenant = batch.get("tenant", "default")
    return [] if tenant in tenant_map else [tenant]

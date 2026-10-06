"""Lightweight event bus."""

from __future__ import annotations


class EventBus:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, topic: str, handler) -> None:
        self.subscribers.setdefault(topic, []).append(handler)

    def publish(self, topic: str, payload: dict) -> int:
        for handler in self.subscribers.get(topic, []):
            handler(payload)
        return len(self.subscribers.get(topic, []))


# @ACTION(ACT-401): Bound the event bus backlog during executor restarts
def backlog_limit(bus: EventBus, limit: int = 512) -> int:
    return min(len(bus.subscribers), limit)

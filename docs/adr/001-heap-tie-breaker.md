# ADR 001 — Heap Tie-Breaker

**Status:** Accepted

## Context

The priority queue needs to order tasks based on their urgency. When
two tasks have the same urgency, `heapq` needs another value to
break the tie. Python's `heapq` compares the next element in the
tuple, which could cause it to compare task names or `trace_id`
values.

## Decision

We chose an `itertools.count()` counter as the second element in the
heap tuple. The counter is always unique, so `heapq` never needs to
compare the task or `trace_id`. It also gives equal-urgency tasks
FIFO ordering, meaning the task added first is processed first.

## Consequences

This avoids unexpected comparisons of task names or `trace_id`
strings and makes the ordering predictable. The trade-off is one
additional tuple field and maintaining `self._counter` in
`__init__`.

## Rejected Alternative

We could have used the task name or `trace_id` directly as the
tie-breaker. String comparison would work without crashing, but it
would order equal-priority tasks alphabetically rather than by
insertion order. This would be less fair, less meaningful, and
harder to understand when debugging task execution order.
# Sentinel AI India — design.md

## 1. Problem
v1 shipped in three days with 5 features and 5 tests, using only 26
of its 133 assigned roadmap steps. v1.1 audits that gap and closes
it — every step from 1 to 133 is now genuinely built, not just
assigned.

## 2. Requirements — measured
- Task validation: reject urgency outside 1-5 (C1, proven live with
  a real Pydantic ValidationError)
- Structured logging: JSON, trace_id per task, child loggers per
  module (C2)
- Log injection defence: \n/\r rejected via regex allow-list (C2,
  proven live — a forged log line attempt was blocked)
- Agent hierarchy: BaseAgent + 2 children, polymorphism proven with
  a third agent type added with zero loop changes (C4)
- Generator vs list: 65.48 MB vs 0.16 MB peak memory on 1M lines,
  ~400x difference (C5)
- Atomic writes: proven safe under a simulated mid-write crash (C5)
- CPU-bound: multiprocess ~1.9x faster than sequential; threaded
  gave no improvement, confirming the GIL (C6)
- I/O-bound: threaded/async ~45x faster than sequential (C6)
- cProfile found UUID generation, not Pydantic validation, as the
  real bottleneck in add_task() (C6)
- NumPy vs loop: ~10-20x speedup on a 1M-value average (C7)
- HTTP timeout: explicit 5s vs an unreliable OS-level default of
  ~21s (C9)
- Test suite: 18 tests, ~4.4s, network-free via mocking (C10, C11)

## 3. Data Model
Task and Event are Pydantic models (src/models.py) — urgency
constrained to 1-5, status/kind constrained to fixed literal sets,
timestamps required to be timezone-aware.

## 4. Interfaces
- Agent.receive() — validates every inbound message, returns None
  and logs a warning on rejection
- Orchestrator.add_task() — validates urgency before the heap ever
  sees it
- get_cloudshield_status() / get_autopilot_status() — HTTP GET with
  timeout, retry with jitter, graceful degradation, 30s cache

## 5. Trade-offs
- Heap tie-breaker: gave up direct trace_id/task comparison (which
  risked type errors) for an itertools counter, gaining
  deterministic FIFO ordering among equal-urgency tasks.
- Retry + jitter: gave up faster failure detection for resilience —
  desynchronized retries avoid hammering a struggling service.
- Generator over list: gave up random access and multi-pass
  iteration (a generator is exhausted after one pass) for a ~400x
  reduction in peak memory.
- Mocked HTTP tests: gave up live API verification for speed and
  reliability — the suite runs in seconds and never depends on
  whether CloudShield happens to be running.

## 6. Known Limits
- Everything is in memory — a restart loses all agent and task
  state (v2 adds a database).
- Home and Evolution pages are still stub pages; their real content
  is built in C14.
- Sentinel's Flask API has no authentication on /status — anyone
  who can reach the port can call it.
- Priority queue is not persisted; Streamlit re-running the script
  can duplicate task creation (observed directly in C2's logs).
- export_history() writes tasks in heap-priority order, not
  insertion order — a known display inconsistency.
- Retries cannot fix a genuinely down API; they only smooth over
  brief transient failures.
- Mocked tests verify our own logic correctly but cannot catch
  changes in the real CloudShield/AutoPilot API contracts.
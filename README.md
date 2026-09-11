# exchange in a box

A deterministic low-latency matching engine and limit order book, built in modern C++ for correctness first and performance second.

> **Status:** phase 0 — specification and design. The repository is public from day one so the decisions, mistakes, measurements, and improvements stay visible.

The goal is not to cosplay a production exchange. It is to build a small system that is understandable end to end, strict enough to expose bad assumptions, and measured well enough that every performance claim has evidence.

## What this should prove

- Exchange behavior is defined explicitly rather than discovered through bugs.
- Price-time priority and order lifecycle rules remain correct under awkward event sequences.
- The same input stream always produces the same executions and final book state.
- Tests cover examples, invariants, generated event sequences, fuzz input, and recovery.
- Latency work starts with a reproducible baseline and changes one bottleneck at a time.
- Design decisions explain both the chosen path and the rejected alternatives.

## Initial system boundary

```text
order commands
      │
      ▼
validation → sequencing → matching engine → execution reports
                       │
                       ├──→ market-data events
                       └──→ append-only journal → deterministic replay

          tests / reference model / fuzzing / benchmarks
                         surround the core
```

The matching core starts as a **single-writer deterministic state machine**. Networking, concurrency, persistence, and multi-symbol sharding are added only after the semantics are correct and measurable.

## Version-one scope

- Integer tick prices and integer quantities; no floating-point money.
- One symbol, then multiple independently sharded symbols.
- Limit orders with price-time priority.
- New, cancel, and replace commands with explicit priority rules.
- GTC and IOC behavior; more order types only after the core is stable.
- Execution reports and top-of-book/depth events.
- Append-only command/event journal and deterministic replay.
- Correctness-first reference implementation plus an optimized implementation.
- Reproducible throughput and p50/p95/p99/p99.9 latency reports.

## Non-goals, for now

- A trading strategy or claims about profitability.
- A web dashboard.
- Distributed consensus or active-active matching.
- Kernel bypass, custom hardware, or lock-free structures before profiling justifies them.
- Comparing benchmark numbers from different machines as if they were equivalent.

## Engineering rules

1. **Specify before optimizing.** Exchange rules and invariants are written before the fast path.
2. **Correctness is observable.** Commands produce explicit events; replay can reconstruct state.
3. **No mystery numbers.** Benchmarks include hardware, compiler, flags, workload, warmup, and distribution.
4. **No speculative cleverness.** Every optimization needs a profile and before/after evidence.
5. **Keep the core deterministic.** I/O and concurrency live at the boundary.
6. **Make failure testable.** Invalid commands, truncated journals, duplicate messages, and restart paths are deliberate cases.

## What “done” looks like

A reviewer can:

1. read the matching rules and invariants;
2. build the project with one documented command;
3. run unit, property, differential, sanitizer, and fuzz tests;
4. replay a fixed event stream and reproduce the same checksum;
5. run a pinned benchmark workload and reproduce the report format;
6. inspect profiles and decision records for each meaningful optimization; and
7. understand where the design stops being production-ready.

## Plan

- [`ROADMAP.md`](ROADMAP.md) — implementation phases, deliverables, and acceptance criteria.
- [`LEARNING.md`](LEARNING.md) — what each phase is meant to teach and the questions the finished project should answer.

The first code milestone will establish the C++20 build, sanitizers, domain types, command/event model, and executable specification. No latency claims until there is a correct baseline.

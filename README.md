# exchange in a box

a deterministic low-latency matching engine and limit order book, built in modern C++ for correctness first and performance second.

> **status:** phase 0 — specification and design. the repository is public from day one so the decisions, mistakes, measurements, and improvements stay visible.

the goal is not to cosplay a production exchange. it is to build a small system that is understandable end to end, strict enough to expose bad assumptions, and measured well enough that every performance claim has evidence.

## what this should prove

- exchange behavior is defined explicitly rather than discovered through bugs.
- price-time priority and order lifecycle rules remain correct under awkward event sequences.
- the same input stream always produces the same executions and final book state.
- tests cover examples, invariants, generated event sequences, fuzz input, and recovery.
- latency work starts with a reproducible baseline and changes one bottleneck at a time.
- design decisions explain both the chosen path and the rejected alternatives.

## initial system boundary

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

the matching core starts as a **single-writer deterministic state machine**. networking, concurrency, persistence, and multi-symbol sharding are added only after the semantics are correct and measurable.

## version-one scope

- integer tick prices and integer quantities; no floating-point money.
- one symbol, then multiple independently sharded symbols.
- limit orders with price-time priority.
- new, cancel, and replace commands with explicit priority rules.
- GTC and IOC behavior; more order types only after the core is stable.
- execution reports and top-of-book/depth events.
- append-only command/event journal and deterministic replay.
- correctness-first reference implementation plus an optimized implementation.
- reproducible throughput and p50/p95/p99/p99.9 latency reports.

## non-goals, for now

- a trading strategy or claims about profitability.
- a web dashboard.
- distributed consensus or active-active matching.
- kernel bypass, custom hardware, or lock-free structures before profiling justifies them.
- comparing benchmark numbers from different machines as if they were equivalent.

## engineering rules

1. **specify before optimizing.** exchange rules and invariants are written before the fast path.
2. **correctness is observable.** commands produce explicit events; replay can reconstruct state.
3. **no mystery numbers.** benchmarks include hardware, compiler, flags, workload, warmup, and distribution.
4. **no speculative cleverness.** every optimization needs a profile and before/after evidence.
5. **keep the core deterministic.** I/O and concurrency live at the boundary.
6. **make failure testable.** invalid commands, truncated journals, duplicate messages, and restart paths are deliberate cases.

## what “done” looks like

a reviewer can:

1. read the matching rules and invariants;
2. build the project with one documented command;
3. run unit, property, differential, sanitizer, and fuzz tests;
4. replay a fixed event stream and reproduce the same checksum;
5. run a pinned benchmark workload and reproduce the report format;
6. inspect profiles and decision records for each meaningful optimization; and
7. understand where the design stops being production-ready.

## plan

- [`ROADMAP.md`](ROADMAP.md) — implementation phases, deliverables, and acceptance criteria.
- [`LEARNING.md`](LEARNING.md) — what each phase is meant to teach and the questions the finished project should answer.

the first code milestone will establish the C++20 build, sanitizers, domain types, command/event model, and executable specification. no latency claims until there is a correct baseline.

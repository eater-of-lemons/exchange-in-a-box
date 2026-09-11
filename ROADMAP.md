# Roadmap

Each phase should end in a small reviewable commit or pull request. Do not optimize ahead of the current phase: the project is meant to preserve the reasoning trail, not only the final code.

## Phase 0 — specify the exchange

**Build**

- Define tick price, quantity, order ID, client ID, sequence number, and timestamp semantics.
- Write rules for price-time priority, crossing, partial fills, cancel, and replace.
- Define command rejection reasons and the order lifecycle state machine.
- List core invariants and create hand-worked matching examples.
- Record initial architecture decisions, including integer prices and a single-writer core.

**Deliverables**

- `docs/SPEC.md`
- `docs/INVARIANTS.md`
- architecture decision records in `docs/decisions/`
- golden input/output examples under `testdata/`

**Acceptance**

A reader can determine the exact outcome of every supported command without reading C++.

## Phase 1 — build a boring, safe skeleton

**Build**

- C++20 CMake project with pinned test and benchmark dependencies.
- Debug, release, AddressSanitizer, UndefinedBehaviorSanitizer, and coverage presets.
- Strong domain types for prices, quantities, IDs, commands, and events.
- A command-line runner that accepts a fixed event stream and prints events.
- CI for build, tests, formatting, and sanitizers.

**Acceptance**

A clean clone configures, builds, and runs tests through documented commands on Linux and macOS.

## Phase 2 — correctness-first reference book

**Build**

- One-symbol limit order book using simple standard-library containers.
- Bid/ask ordering, FIFO queues at each price, and O(1)-by-ID cancellation where practical.
- GTC limit orders first, then IOC.
- New, cancel, and replace with explicit priority-loss behavior.
- Execution and market-data events emitted by the core.

**Acceptance**

All golden examples pass, book invariants are checked after every command in debug builds, and the implementation makes no performance claims.

## Phase 3 — attack correctness

**Build**

- Unit tests for boundaries and order lifecycle transitions.
- Property tests over generated command sequences.
- A deliberately slow reference model for differential testing.
- Fuzz targets for command decoding and engine transitions.
- Sanitizer runs for generated and fuzzed workloads.

**Properties to enforce**

- Bids never cross asks after matching completes.
- Visible quantity equals the sum of resting order quantities.
- Filled plus remaining quantity never exceeds submitted quantity.
- IDs and sequence numbers obey their uniqueness/ordering rules.
- Events conserve quantity and follow legal state transitions.
- Replay of the same commands produces the same events and checksum.

**Acceptance**

A long seeded random run matches the reference model, and failures print a minimal reproducible sequence.

## Phase 4 — journal, replay, and recovery

**Build**

- Versioned append-only command/event format with checksums.
- Deterministic replay tool.
- Snapshot format and snapshot-plus-tail recovery.
- Behavior for duplicate, missing, corrupt, and truncated records.
- State checksum and replay verification command.

**Acceptance**

Kill the process at selected write points, restart it, and recover to the last valid sequence without inventing or duplicating executions.

## Phase 5 — establish an honest baseline

**Build**

- Benchmark harness with fixed seeds and named workloads:
  - balanced flow;
  - cancel-heavy flow;
  - deep book;
  - crossing burst;
  - adversarial hot price level.
- Report throughput and p50/p95/p99/p99.9 latency, not only an average.
- Capture CPU, OS, compiler, flags, frequency policy, warmup, and run count.
- Collect profiles, cache/branch counters where available, and flamegraphs.

**Acceptance**

Another person on the same environment can reproduce the report shape and understand its limitations.

## Phase 6 — optimize from evidence

**Possible experiments, not pre-decided solutions**

- Data-oriented order and price-level layout.
- Stable object pools or arena allocation.
- Intrusive FIFO lists.
- Flat/ordered price-level indexes.
- Reduced copying and tighter event representation.
- Branch and cache behavior improvements.

For every accepted optimization:

1. preserve the reference implementation;
2. state the bottleneck and hypothesis;
3. add or retain a correctness test;
4. report before/after distributions on the same workload; and
5. record memory and complexity trade-offs.

**Acceptance**

Every optimization has profile evidence and no semantic divergence from the reference model.

## Phase 7 — boundaries, backpressure, and concurrency

**Build**

- Keep matching single-writer; move ingress and egress to explicit boundaries.
- Add a versioned binary wire format and gateway process.
- Use bounded queues with documented ownership and backpressure behavior.
- Separate receive, sequence/match, journal, and publish concerns.
- Measure coordinated omission and queueing delay separately from engine service time.

**Acceptance**

Load beyond capacity degrades according to a documented policy rather than silently growing memory or reordering commands.

## Phase 8 — multi-symbol operation and final report

**Build**

- Shard independent symbols while preserving per-symbol order.
- Add operational metrics, structured logs, and fault-injection scenarios.
- Publish architecture diagrams, benchmark tables, profiles, and known limitations.
- Write two technical notes:
  - “what a matching engine must never get wrong”;
  - “benchmarking without lying to yourself.”

**Acceptance**

The repository supports a reproducible correctness demonstration, recovery demonstration, and benchmark run, with honest boundaries around every result.

## Suggested implementation rhythm

For each phase:

1. write the rule or hypothesis;
2. add the test or measurement method;
3. implement the smallest correct change;
4. inspect failure modes;
5. document the result and trade-off; and
6. only then move to the next phase.

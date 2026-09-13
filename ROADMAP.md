# roadmap

each phase should end in a small reviewable commit or pull request. do not optimize ahead of the current phase: the project is meant to preserve the reasoning trail, not only the final code.

## phase 0 — specify the exchange

**build**

- define tick price, quantity, order ID, client ID, sequence number, and timestamp semantics.
- write rules for price-time priority, crossing, partial fills, cancel, and replace.
- define command rejection reasons and the order lifecycle state machine.
- list core invariants and create hand-worked matching examples.
- record initial architecture decisions, including integer prices and a single-writer core.

**deliverables**

- `docs/SPEC.md`
- `docs/INVARIANTS.md`
- architecture decision records in `docs/decisions/`
- golden input/output examples under `testdata/`

**acceptance**

a reader can determine the exact outcome of every supported command without reading C++.

## phase 1 — build a boring, safe skeleton

**build**

- C++20 CMake project with pinned test and benchmark dependencies.
- debug, release, AddressSanitizer, UndefinedBehaviorSanitizer, and coverage presets.
- strong domain types for prices, quantities, IDs, commands, and events.
- a command-line runner that accepts a fixed event stream and prints events.
- CI for build, tests, formatting, and sanitizers.

**acceptance**

a clean clone configures, builds, and runs tests through documented commands on Linux and macOS.

## phase 2 — correctness-first reference book

**build**

- one-symbol limit order book using simple standard-library containers.
- bid/ask ordering, FIFO queues at each price, and O(1)-by-ID cancellation where practical.
- GTC limit orders first, then IOC.
- new, cancel, and replace with explicit priority-loss behavior.
- execution and market-data events emitted by the core.

**acceptance**

all golden examples pass, book invariants are checked after every command in debug builds, and the implementation makes no performance claims.

## phase 3 — attack correctness

**build**

- unit tests for boundaries and order lifecycle transitions.
- property tests over generated command sequences.
- a deliberately slow reference model for differential testing.
- fuzz targets for command decoding and engine transitions.
- sanitizer runs for generated and fuzzed workloads.

**properties to enforce**

- bids never cross asks after matching completes.
- visible quantity equals the sum of resting order quantities.
- filled plus remaining quantity never exceeds submitted quantity.
- IDs and sequence numbers obey their uniqueness/ordering rules.
- events conserve quantity and follow legal state transitions.
- replay of the same commands produces the same events and checksum.

**acceptance**

a long seeded random run matches the reference model, and failures print a minimal reproducible sequence.

## phase 4 — journal, replay, and recovery

**build**

- versioned append-only command/event format with checksums.
- deterministic replay tool.
- snapshot format and snapshot-plus-tail recovery.
- behavior for duplicate, missing, corrupt, and truncated records.
- state checksum and replay verification command.

**acceptance**

kill the process at selected write points, restart it, and recover to the last valid sequence without inventing or duplicating executions.

## phase 5 — establish an honest baseline

**build**

- benchmark harness with fixed seeds and named workloads:
  - balanced flow;
  - cancel-heavy flow;
  - deep book;
  - crossing burst;
  - adversarial hot price level.
- report throughput and p50/p95/p99/p99.9 latency, not only an average.
- capture CPU, OS, compiler, flags, frequency policy, warmup, and run count.
- collect profiles, cache/branch counters where available, and flamegraphs.

**acceptance**

another person on the same environment can reproduce the report shape and understand its limitations.

## phase 6 — optimize from evidence

**possible experiments, not pre-decided solutions**

- data-oriented order and price-level layout.
- stable object pools or arena allocation.
- intrusive FIFO lists.
- flat/ordered price-level indexes.
- reduced copying and tighter event representation.
- branch and cache behavior improvements.

for every accepted optimization:

1. preserve the reference implementation;
2. state the bottleneck and hypothesis;
3. add or retain a correctness test;
4. report before/after distributions on the same workload; and
5. record memory and complexity trade-offs.

**acceptance**

every optimization has profile evidence and no semantic divergence from the reference model.

## phase 7 — boundaries, backpressure, and concurrency

**build**

- keep matching single-writer; move ingress and egress to explicit boundaries.
- add a versioned binary wire format and gateway process.
- use bounded queues with documented ownership and backpressure behavior.
- separate receive, sequence/match, journal, and publish concerns.
- measure coordinated omission and queueing delay separately from engine service time.

**acceptance**

load beyond capacity degrades according to a documented policy rather than silently growing memory or reordering commands.

## phase 8 — multi-symbol operation and final report

**build**

- shard independent symbols while preserving per-symbol order.
- add operational metrics, structured logs, and fault-injection scenarios.
- publish architecture diagrams, benchmark tables, profiles, and known limitations.
- write two technical notes:
  - “what a matching engine must never get wrong”;
  - “benchmarking without lying to yourself.”

**acceptance**

the repository supports a reproducible correctness demonstration, recovery demonstration, and benchmark run, with honest boundaries around every result.

## suggested implementation rhythm

for each phase:

1. write the rule or hypothesis;
2. add the test or measurement method;
3. implement the smallest correct change;
4. inspect failure modes;
5. document the result and trade-off; and
6. only then move to the next phase.

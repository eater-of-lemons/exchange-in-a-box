# Learning plan

This project is useful only if it changes how you reason about systems. The matching engine is the vehicle; the real subject is correctness and performance under strict ordering constraints.

## 1. Market microstructure and exchange semantics

Learn to explain:

- Why price-time priority is a policy, not merely a container choice.
- When two orders cross and how partial fills affect both lifecycles.
- Why cancel/replace usually loses priority and which fields can change safely.
- The difference between order acknowledgements, rejects, executions, and book updates.
- How GTC and IOC behavior changes the event sequence.
- Why deterministic sequencing matters more than wall-clock timestamps inside the core.
- Which real exchange features are intentionally absent and why they are difficult.

**Proof of learning:** an executable specification, legal state-transition table, and hand-worked examples whose output matches the engine.

## 2. Invariants and state-machine design

Learn to turn vague requirements into properties that survive arbitrary event sequences:

- no crossed resting book after matching;
- conservation of quantity;
- FIFO ordering within a price level;
- valid order lifecycle transitions;
- uniqueness and monotonicity rules;
- deterministic events and state checksums.

You should understand why example-based unit tests are necessary but insufficient, and when property, model-based, differential, and fuzz testing find different classes of bugs.

**Proof of learning:** generated sequences compare against a slow model and shrink to a minimal counterexample when they fail.

## 3. C++ systems engineering

Learn through evidence rather than folklore:

- ownership and lifetime design in a long-lived mutable data structure;
- value semantics versus stable references;
- integer domain types that prevent unit and sign errors;
- iterator/reference invalidation across standard containers;
- memory layout, padding, locality, and cache lines;
- allocation behavior on a hot path;
- branch behavior and data-dependent latency;
- when custom allocators or intrusive structures earn their complexity;
- how compiler options, link-time optimization, and debug checks alter results.

**Proof of learning:** documented data-layout diagrams, profiles, and before/after measurements that preserve identical behavior.

## 4. Performance measurement

Learn why “it handles a million orders per second” is not a useful statement by itself.

Be able to explain:

- throughput versus service time versus end-to-end latency;
- why p99 and p99.9 can matter more than the mean;
- warmup, CPU affinity, frequency scaling, page faults, and noisy neighbours;
- workload shape and why a cancel-heavy deep book differs from a crossing burst;
- coordinated omission and hidden queueing delay;
- the limits of wall-clock timers and cycle counters;
- how to use profiles, hardware counters, and flamegraphs;
- why benchmark hardware, compiler, flags, seed, and repetitions belong in the report.

**Proof of learning:** a reproducible benchmark harness and an optimization log in which each accepted change starts from a measured bottleneck.

## 5. Event-driven architecture and recovery

Learn how a deterministic core fits into a larger live system:

- commands versus facts/events;
- sequencing and total order;
- append-only journals and versioned schemas;
- idempotency, duplicate input, and replay;
- snapshots plus journal-tail recovery;
- checksums and corruption/truncation handling;
- single-writer ownership and where concurrency belongs;
- bounded queues, backpressure, and overload policy.

**Proof of learning:** crash/fault tests recover to the final valid sequence without duplicate or missing executions.

## 6. Technical judgment

Top engineering work is not the longest feature list. Practice deciding:

- what must be specified now;
- what can remain a non-goal;
- what should be simple until profiling proves otherwise;
- where determinism is worth more than parallelism;
- when an optimization's maintenance cost is not justified;
- how to state limitations without weakening the work.

**Proof of learning:** short architecture decision records that include context, alternatives, decision, and consequences.

## Questions you should answer comfortably at the end

1. What are the core invariants, and where are they enforced?
2. What exactly happens when an order partially crosses several price levels?
3. Which replace operations lose queue priority, and why?
4. Why did you choose the first data structures?
5. What did the first profile show?
6. Which optimization improved p99 but hurt memory or maintainability?
7. How do you know the optimized engine is semantically equivalent to the reference model?
8. What workload produces the worst tail latency, and why?
9. How does the system behave when input exceeds capacity?
10. What happens if the journal ends halfway through a record?
11. How do you replay without generating duplicate external side effects?
12. Why is the matching core single-writer?
13. What would have to change for active-active operation?
14. Which parts are exchange policy and which are implementation detail?
15. Which performance claims are valid only on your test machine?

## What a strong public result looks like

| Artifact | Signal |
| --- | --- |
| precise specification | you can resolve ambiguity before coding |
| reference engine | you value clarity and correctness |
| property + differential + fuzz tests | you can test beyond happy paths |
| deterministic journal/replay | you understand production recovery |
| reproducible benchmark suite | you measure instead of guessing |
| profile-led optimization history | you understand modern C++ performance |
| decision records and limitations | you exercise engineering judgment |
| concise technical write-ups | you can communicate difficult systems |

The best interview story is not “I wrote a fast order book.” It is: **“I specified the semantics, built a trustworthy reference, attacked it with generated tests, measured the baseline, found a real bottleneck, changed the design, and proved what improved without changing behavior.”**

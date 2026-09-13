# learning plan

this project is useful only if it changes how you reason about systems. the matching engine is the vehicle; the real subject is correctness and performance under strict ordering constraints.

## 1. market microstructure and exchange semantics

learn to explain:

- why price-time priority is a policy, not merely a container choice.
- when two orders cross and how partial fills affect both lifecycles.
- why cancel/replace usually loses priority and which fields can change safely.
- the difference between order acknowledgements, rejects, executions, and book updates.
- how GTC and IOC behavior changes the event sequence.
- why deterministic sequencing matters more than wall-clock timestamps inside the core.
- which real exchange features are intentionally absent and why they are difficult.

**proof of learning:** an executable specification, legal state-transition table, and hand-worked examples whose output matches the engine.

## 2. invariants and state-machine design

learn to turn vague requirements into properties that survive arbitrary event sequences:

- no crossed resting book after matching;
- conservation of quantity;
- FIFO ordering within a price level;
- valid order lifecycle transitions;
- uniqueness and monotonicity rules;
- deterministic events and state checksums.

you should understand why example-based unit tests are necessary but insufficient, and when property, model-based, differential, and fuzz testing find different classes of bugs.

**proof of learning:** generated sequences compare against a slow model and shrink to a minimal counterexample when they fail.

## 3. C++ systems engineering

learn through evidence rather than folklore:

- ownership and lifetime design in a long-lived mutable data structure;
- value semantics versus stable references;
- integer domain types that prevent unit and sign errors;
- iterator/reference invalidation across standard containers;
- memory layout, padding, locality, and cache lines;
- allocation behavior on a hot path;
- branch behavior and data-dependent latency;
- when custom allocators or intrusive structures earn their complexity;
- how compiler options, link-time optimization, and debug checks alter results.

**proof of learning:** documented data-layout diagrams, profiles, and before/after measurements that preserve identical behavior.

## 4. performance measurement

learn why “it handles a million orders per second” is not a useful statement by itself.

be able to explain:

- throughput versus service time versus end-to-end latency;
- why p99 and p99.9 can matter more than the mean;
- warmup, CPU affinity, frequency scaling, page faults, and noisy neighbours;
- workload shape and why a cancel-heavy deep book differs from a crossing burst;
- coordinated omission and hidden queueing delay;
- the limits of wall-clock timers and cycle counters;
- how to use profiles, hardware counters, and flamegraphs;
- why benchmark hardware, compiler, flags, seed, and repetitions belong in the report.

**proof of learning:** a reproducible benchmark harness and an optimization log in which each accepted change starts from a measured bottleneck.

## 5. event-driven architecture and recovery

learn how a deterministic core fits into a larger live system:

- commands versus facts/events;
- sequencing and total order;
- append-only journals and versioned schemas;
- idempotency, duplicate input, and replay;
- snapshots plus journal-tail recovery;
- checksums and corruption/truncation handling;
- single-writer ownership and where concurrency belongs;
- bounded queues, backpressure, and overload policy.

**proof of learning:** crash/fault tests recover to the final valid sequence without duplicate or missing executions.

## 6. technical judgment

top engineering work is not the longest feature list. practice deciding:

- what must be specified now;
- what can remain a non-goal;
- what should be simple until profiling proves otherwise;
- where determinism is worth more than parallelism;
- when an optimization's maintenance cost is not justified;
- how to state limitations without weakening the work.

**proof of learning:** short architecture decision records that include context, alternatives, decision, and consequences.

## questions you should answer comfortably at the end

1. what are the core invariants, and where are they enforced?
2. what exactly happens when an order partially crosses several price levels?
3. which replace operations lose queue priority, and why?
4. why did you choose the first data structures?
5. what did the first profile show?
6. which optimization improved p99 but hurt memory or maintainability?
7. how do you know the optimized engine is semantically equivalent to the reference model?
8. what workload produces the worst tail latency, and why?
9. how does the system behave when input exceeds capacity?
10. what happens if the journal ends halfway through a record?
11. how do you replay without generating duplicate external side effects?
12. why is the matching core single-writer?
13. what would have to change for active-active operation?
14. which parts are exchange policy and which are implementation detail?
15. which performance claims are valid only on your test machine?

## what a strong public result looks like

| artifact | signal |
| --- | --- |
| precise specification | you can resolve ambiguity before coding |
| reference engine | you value clarity and correctness |
| property + differential + fuzz tests | you can test beyond happy paths |
| deterministic journal/replay | you understand production recovery |
| reproducible benchmark suite | you measure instead of guessing |
| profile-led optimization history | you understand modern C++ performance |
| decision records and limitations | you exercise engineering judgment |
| concise technical write-ups | you can communicate difficult systems |

the best interview story is not “i wrote a fast order book.” it is: **“i specified the semantics, built a trustworthy reference, attacked it with generated tests, measured the baseline, found a real bottleneck, changed the design, and proved what improved without changing behavior.”**

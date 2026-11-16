# Scoring rubric

Score one named scarce asset across all five factors. Use integers unless the evidence genuinely falls between anchors; half-points are allowed, but false precision is not. A high factor score is never a substitute for a cash-flow assumption.

For every factor record the evidence date, source label, confidence, downgrade trigger, and the scenario variable affected by that trigger.

## F1 — Irreplaceability

Ask whether customers can achieve substantially the same economic outcome without the asset.

| Score | Anchor |
|---|---|
| 1 | Interchangeable commodity; many equivalent substitutes |
| 2 | Differentiated, but substitution is practical with modest cost or delay |
| 3 | Meaningful qualification, integration, or performance advantage |
| 4 | Critical-path asset with costly redesign, requalification, or ecosystem switching |
| 5 | No practical substitute for the relevant workload or regulated use case |

Distinguish technical uniqueness from customer dependence. Brand affection alone does not establish irreplaceability.

## F2 — Replication time

Estimate the time for a capable, funded competitor to reach useful commercial parity—not the time to announce capacity.

| Score | Replication time |
|---|---|
| 1 | Less than 1 year |
| 2 | 1 to less than 2 years |
| 3 | 2 to less than 3 years |
| 4 | 3 to less than 5 years |
| 5 | 5 years or more, or blocked by a durable legal/physical constraint |

Include permitting, tooling, qualification, yield learning, software/ecosystem adoption, and customer validation where relevant. Do not count management's construction timetable as commercial parity without evidence.

## F3 — Supply concentration

Score the number and comparability of suppliers that can meet the same customer requirement.

| Score | Anchor |
|---|---|
| 1 | Fragmented supply with many credible equivalents |
| 2 | Roughly 5–10 credible suppliers and low switching friction |
| 3 | Roughly 3–5 suppliers at useful parity |
| 4 | Three-player or similarly concentrated structure with differentiated capabilities |
| 5 | Monopoly/duopoly, exclusive right, or singular bottleneck at useful scale |

Use the relevant capacity slice, not an unrelated company-wide market-share statistic.

## F4 — Throughput tightness and rent capture

Score both present supply-demand tightness and the issuer's demonstrated ability to convert it into durable economics.

| Score | Anchor |
|---|---|
| 1 | Oversupply, weak utilization, falling prices, or adverse contract resets |
| 2 | Broadly balanced; little pricing power or backlog protection |
| 3 | Moderate backlog, utilization, or spot-price evidence with ordinary cancellation risk |
| 4 | Constrained capacity plus enforceable pricing/volume protection or sustained margin evidence |
| 5 | Severe allocation or multi-year, economically binding commitments with demonstrated rent capture |

Examine deposits, cancellation rights, price reopeners, customer concentration, and at least four quarters of gross-margin or unit-economics evidence. A large non-binding backlog is not automatically a high score.

If scarcity exists but rents accrue to customers, suppliers, governments, or employees, lower F4 or reflect the leakage in scenario cash conversion/margins. Do not create a second, undocumented "effective SM."

## F5 — Demand durability

Score the diversity and persistence of end demand after allowing for substitution and customer economics.

| Score | Anchor |
|---|---|
| 1 | One-off, policy-only, speculative, or visibly contracting demand |
| 2 | Primarily cyclical or dependent on one short-lived program |
| 3 | One credible multi-year driver or several correlated drivers |
| 4 | Multiple independent drivers with at least a three-year evidence base |
| 5 | Secular, multi-cycle demand with broad end-market and customer support |

Count independent economic drivers, not different names for the same budget pool.

## Derived diagnostics

```text
Structural SM = (F1 + F2 + F3 + F4 + F5) / 5
Duration score D = (F2 + F5) / 2
```

`D` summarizes structural persistence for comparison and can seed a base-case duration assumption. It is not a forecast fact. Each valuation scenario must state its own duration, which may differ from `D` when justified.

Classify the asset separately as `fast`, `slow`, or `mixed`:

- `fast`: capacity or demand can adjust within roughly two years;
- `slow`: physical, legal, qualification, or ecosystem constraints commonly take three or more years;
- `mixed`: different layers adjust on materially different clocks.

This classification informs downside design; it never switches a haircut on or off. In particular, lowering F4 cannot mechanically increase fair value.

## Cross-checks

Before finalizing scores, test:

- **scope consistency:** every score refers to the same scarce asset;
- **earnings consistency:** the EPS or segment cash flow belongs to that asset;
- **rent consistency:** a high F4 has margin, contract, or realized-price support;
- **duration consistency:** high F2/F5 claims have observable evidence and dated downgrade triggers;
- **capital independence:** identify whether sustaining scarcity requires issuer funding, customer prepayments, government support, or external capital; model that funding risk separately;
- **positioning:** record crowding separately from intrinsic value.


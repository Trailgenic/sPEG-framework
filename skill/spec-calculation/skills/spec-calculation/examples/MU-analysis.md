# sPEG Analysis: MU (Micron Technology)

**Position:** Long (core / high-conviction)
**Date:** 2026-05-29
**Analyst:** Mike Ye

> Canonical worked example for the sPEG skill. MU is the framework's archetypal case: a business the market still prices as a commodity cyclical (low forward P/E) whose earnings are bounded by a structurally scarce input (HBM). It is also the archetypal **trap** for the formula — the raw consensus growth number is a cycle-peak figure that, fed in directly, produces a misleadingly tiny sPEG. This example shows the Growth Input Discipline and the mandatory Sensitivity step doing their job.

## Thesis Statement

MU's earnings are bounded by HBM (high-bandwidth memory) capacity, which is structurally scarce: calendar-2026 HBM is sold out on pre-agreed price *and* volume, supply is a three-player oligopoly, and no AI accelerator ships without it. The market still prices MU on a commodity-DRAM exit multiple, not recognizing the HBM franchise as structural scarcity.

## Validity Gates

- NTM EPS > 0 ✓
- Forward 3-yr growth > 0 ✓
- Scarcity Multiplier ≥ 2 (scores 4.5 below) ✓
- Not financial/commodity-without-scarcity/distressed ✓ (memory is commodity-*adjacent*, but the HBM franchise carries identifiable structural scarcity — in-scope)

Gates pass. Proceed.

## Inputs

- **Forward P/E:** ~13 (price ÷ NTM consensus EPS)
- **Forward EPS Growth (3-yr CAGR, normalized): 40%** — NORMALIZED. Raw consensus shows ~75% in the hot forward year decelerating toward ~20% by year 3; the un-normalized peak (75) is a cycle-peak figure and is capped/averaged to a 40% 3-yr CAGR per the Growth Input Discipline. The raw 75 is carried only as a sensitivity upper bound.
- **Data source:** web search / consensus aggregates, as of 2026-05-29

## Scarcity Multiplier Scoring

### Factor 1: Irreplaceability — 5/5
No AI accelerator runs without HBM; there is no architectural substitute for high-bandwidth memory in the GPU/XPU stack within a 3-year horizon. Replacement would require redesigning the accelerator memory interface.
**Downgrade trigger:** A credible non-HBM memory architecture (e.g., a processing-in-memory or optical-interconnect alternative) is qualified into a flagship accelerator.

### Factor 2: Replication Timeline — 4/5
HBM stacking, TSV, and yield know-how plus the qualification cycle take 3-5 years for a new entrant; the only credible peers (Samsung, SK Hynix) already exist and are capacity-gated. Not a 5 because those two peers are real and active, not theoretical.
**Downgrade trigger:** A fourth manufacturer qualifies HBM at a hyperscaler, or a current peer doubles HBM capacity ahead of schedule.

### Factor 3: Supply Concentration — 5/5
HBM is a three-player oligopoly (Micron, SK Hynix, Samsung) with material capacity and yield differentiation. Functionally a tight, capacity-constrained structure.
**Downgrade trigger:** Any new entrant takes measurable HBM share, or a peer's capacity expansion visibly loosens the structure.

### Factor 4: Throughput Control — 5/5
Calendar-2026 HBM is sold out on pre-agreed price and volume (LTA-style regime); management has stated they can meet only ~50%-two-thirds of demand. Fulfillment well below 60%, expansion capex-gated 18+ months out. Textbook 5.
**Downgrade trigger:** New fabs (Idaho/NY/Singapore) come online and the demand-supply gap narrows; or any quarter where MU reports it is no longer capacity-constrained.

### Factor 5: Demand Durability — 4/5
The question per the new factor: when MU's HBM bottleneck is alleviated (Idaho/NY/Singapore fabs come online), does demand persist or evaporate? HBM demand rides secular AI compute with multiple independent drivers — training, inference, sovereign, enterprise — so it is durable across the visible 3-year horizon and largely grows into new supply rather than collapsing with the shortage. Scored 4 not 5 because there is real sensitivity to the AI-capex cycle maturing: if hyperscaler capex genuinely rolled over, HBM demand would soften even with the bottleneck intact. This is the honest cyclical caveat, now scored explicitly rather than buried.
**Downgrade trigger:** AI-capex deceleration signal (hyperscaler guidance cut), OR HBM demand persisting only at the shortage and softening visibly as fabs ramp — either drops durability toward 3.

**Note for the framework:** under the old "Downstream Dependency" factor MU also scored 4, so the total is unchanged (23/25, SM 4.6). That is the expected result for a genuinely *structural* name — dependency and durability converge. The new factor earns its keep on *cyclical* names, where Downstream Dependency would have scored 4-5 (customers need it now) but Demand Durability correctly scores 2 (the need is a cycle-peak artifact), compressing their Multiplier and raising their sPEG away from a false "unpriced scarcity" reading.

**Total: 23/25 → Scarcity Multiplier = 4.6**

## sPEG Calculation

sPEG = 13 ÷ (40 × 4.6) = 13 ÷ 184 = **0.07**

## Sensitivity

| Scenario | Growth% | SM | sPEG | Tier |
|---|---|---|---|---|
| Base (normalized) | 40 | 4.6 | 0.07 | Scarcity unpriced |
| Growth −30% | 28 | 4.6 | 0.10 | Unpriced / high-conviction edge |
| Growth +30% | 52 | 4.6 | 0.05 | Scarcity unpriced |
| SM −0.5 | 40 | 4.1 | 0.08 | Scarcity unpriced |
| SM +0.5 | 40 | 5.0 (cap) | 0.07 | Scarcity unpriced |
| Uncapped peak growth | 75 | 4.6 | 0.04 | Scarcity unpriced (upper bound only) |

**Robustness:** ROBUST. Across the full plausible range (sPEG 0.05–0.10 normalized; 0.04 only on the uncapped peak), MU never leaves the highest-conviction tier. The conviction does NOT hinge on the aggressive growth assumption — even haircutting growth to 28% keeps it at 0.10. This is what separates a real signal from a cyclical artifact: the un-normalized 0.04 looks more dramatic but adds no information, because the normalized 0.07 already clears the threshold with margin.

## Interpretation

sPEG ~0.07 (robust 0.05–0.10) → **highest-conviction tier: scarcity premium effectively unpriced.** The market is applying a ~13x commodity-DRAM multiple to a franchise whose HBM throughput is contractually locked and structurally short. The mispricing is the gap between commodity pricing and a 4.6 Scarcity Multiplier.

The honest caveat the framework forces into view: the risk here is NOT valuation, it is **cycle timing**. The scarcity is real and currently severe, but Factor 4 carries the seed of its own reversal — the new fabs that resolve the shortage are the same event that compresses the Multiplier. This is why the falsifier hierarchy leads with capacity, not demand.

## Falsifier Hierarchy

Ranked by lead time and impact:
1. **HBM LTA contract language / pricing-regime change** — Lead time: ~0-1 quarters. The earliest, most observable signal; any shift from pre-agreed price/volume to spot exposure cracks Factor 4 first.
2. **MU reports it is no longer capacity-constrained** — Lead time: 0-1 quarters. Direct Factor 4 reversal; the demand-supply gap narrowing is the cycle-timing tell.
3. **Peer capacity expansion ahead of schedule (Samsung/SK Hynix HBM)** — Lead time: 1-2 quarters. Hits Factor 3.
4. **Fourth-entrant HBM qualification** — Lead time: 2-4 quarters. Hits Factors 1, 2, 3 together.
5. **Non-HBM memory architecture qualified into a flagship accelerator** — Lead time: 3+ quarters. The slow structural Factor 1 risk.

## Position Sizing Implication

The robust highest-conviction tier supports a core weight within a concentrated 9-11 name book. The constraint on sizing is not the sPEG (which says size up) but the cycle-timing risk in the falsifier hierarchy — position structure should match the lifecycle phase, with the capacity-driven falsifiers (#1, #2) as the active exit watch rather than any valuation level.

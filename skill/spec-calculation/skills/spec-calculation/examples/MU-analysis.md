# sPEG Analysis: MU (Micron Technology)

**Position:** Long
**Date:** 2026-05-19
**Analyst:** Mike Ye

## Thesis Statement

MU's HBM exposure is structurally scarce, governed by multi-year fixed-price contracts in a three-player oligopoly with downstream AI dependency — but the market is pricing MU as commodity DRAM with cyclical earnings, leaving the scarcity premium completely unpriced.

## Inputs

- Forward P/E: ~11x (FY27 consensus EPS basis)
- Forward EPS Growth (FY26-FY28 CAGR): ~25%
- Data source: Street consensus; illustrative figures pending refresh from live financial data

## Scarcity Multiplier Scoring

### Factor 1: Irreplaceability — 5/5
HBM is the only memory architecture qualified for AI training at scale. No substitute exists for high-bandwidth, low-latency stacked DRAM in current Nvidia/AMD/custom-silicon roadmaps. CXL and HBF are not credible replacements on a 3-year horizon. Without HBM, AI training throughput collapses.
**Downgrade trigger:** CXL or HBF receives a Nvidia qualification credit on a production silicon roadmap.

### Factor 2: Replication Timeline — 4/5
HBM4 qualification cycles run 24-36 months from process start to volume Nvidia validation. The only reason this isn't a 5: Samsung is closer to closing the gap than Hynix was three years ago, and process maturity could compress the next cycle.
**Downgrade trigger:** Samsung HBM4 yield parity announcement with credible volume validation.

### Factor 3: Supply Concentration — 4/5
Three qualified suppliers (Hynix, Samsung, Micron). Hynix dominant, Micron third but qualified on H200/B200. Would be 5/5 if it were a two-player structure; the third entrant prevents pure pricing power but preserves oligopoly economics.
**Downgrade trigger:** Samsung wins exclusive Nvidia HBM4 slot, collapsing the 3-player premise.

### Factor 4: Throughput Control — 5/5
LTA-governed with fixed-price multi-year terms; industry fulfillment running near 50%. This is the defining factor of the thesis — capacity is bound by EUV tool allocation and HBM packaging throughput, both capex-gated 18+ months out. Direct demand-supply mismatch with contractual lock-in.
**Downgrade trigger:** LTA re-opener clause invoked anywhere in the industry; emergence of "customer flexibility" language replacing "fixed pricing" in disclosures.

### Factor 5: Downstream Dependency — 5/5
Nvidia/AMD/hyperscaler AI capex is structurally dependent on HBM throughput. Without HBM scale-up, the training infrastructure thesis collapses. Inverse of normal supplier-customer power — the supplier holds the bottleneck.
**Downgrade trigger:** Hyperscaler cohort capex cut greater than 15% (cohort-level, not single-name).

**Total: 23/25 → Scarcity Multiplier = 4.6**

## sPEG Calculation

sPEG = 11 / (25 × 4.6) = **0.096**

## Interpretation

sPEG below 0.1 places this position in the highest conviction tier — the scarcity premium is completely unpriced. The market is treating MU's earnings as commodity-cyclical DRAM, ignoring that HBM exposure is contractually bound, three-player concentrated, and structurally dependent on AI capex continuing.

The framework signals this is a long opportunity where the principal risk is not "growth disappoints" but rather "scarcity factor degrades." The thesis is operationally falsifiable: when downgrade triggers fire, the multiplier compresses and the position thesis updates mechanically.

## Falsifier Hierarchy

Ranked by lead time and impact:

1. **LTA renegotiation language** (Factor 4 → 4) — Lead time: 1-2 quarters. Watch hyperscaler 10-Q disclosures and MU earnings call language. Earliest and cleanest signal that the contract regime is cracking.

2. **Hynix or Samsung wins exclusive Nvidia HBM4 slot** (Factor 3 → 3) — Lead time: 6-12 months from qualification announcement. Structural-collapse signal; the three-player premise dies.

3. **Hyperscaler cohort capex cut >15%** (Factor 5 → 4) — Lead time: 2-3 quarters. Slowest but most impactful demand-side shock.

4. **Samsung HBM4 yield parity** (Factor 2 → 3) — Replication timeline compression.

5. **CXL/HBF qualification credit** (Factor 1 → 4) — Long-term irreplaceability degradation.

## Scenario-Weighted Targets

- **Bull** (Scarcity Multiplier holds at 4.6): $375-475, 35% probability
- **Base** (one factor degrades to 3.5): $235-310, 45% probability
- **Bear** (two factors degrade to 2.5): $110-165, 20% probability

Probability-weighted target: **~$269**

## Exit Discipline

Hybrid stop: Either Falsifier #1 or #3 fires (immediate full exit) OR -30% price stop from cost basis (staged 50%/50% at -30% and -35%).

## Position Sizing Implication

At current price, the conviction tier supports a 5-6% portfolio weight with attention to volatility (50-day realized vol ~45%). Higher concentration risk is real given the bear case (~$135) represents ~40% downside from spot. The asymmetry of the sPEG signal favors range exposure rather than maximum concentration.

---

*This worked example demonstrates the canonical application of the sPEG framework. For f

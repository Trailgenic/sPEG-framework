---
name: spec-calculation
description: Apply the sPEG framework to a listed equity whose valuation materially depends on one identifiable scarce input, or assess a company for the exmxc sPEG Index (Scarcity Durability score and admission gates). Use for sPEG, Scarcity Multiplier, sPEG Index admission and structural-bottleneck theses. Not for generic stock valuation, financials, pure commodities, distressed companies, or diversified issuers unless the scarce earnings stream can be isolated.
---

# sPEG Framework v1.7

This skill has two modes. Pick one before starting and say which:

- **Mode A — sPEG valuation (v1.6 method, below).** The original scarcity-adjusted PEG: five-factor Scarcity Multiplier, headline sPEG, scenario fair value. Use for valuation and ranking.
- **Mode B — sPEG Index assessment (Scarcity Durability v1.0, see the section at the end).** The method the public exmxc sPEG Index has used since 2026-09-17: five anchored C/S/E/P/D judgments and independent admission gates. Use when the question is whether a company belongs in the sPEG Index.

Never mix the two. The Mode B Scarcity Durability Score is not a multiplier and never feeds the Mode A formula; the Mode A F1-F5 scores are never reported as Index scores.

## Mode A — sPEG valuation

sPEG is a scarcity diagnostic and cross-position ranking tool:

```text
sPEG = (current price / NTM diluted EPS) / (normalized 3-year EPS CAGR% x Scarcity Multiplier)
Scarcity Multiplier = (F1 + F2 + F3 + F4 + F5) / 5
```

The ratio does **not** mechanically produce a fair price. Fair value comes from explicit cash-flow scenarios calculated by `scripts/speg_calculator.py`. This separation is an invariant: the five factor scores are ordinal evidence, not measured valuation multipliers.

## Required reading

- Read [references/scoring-rubric.md](references/scoring-rubric.md) before assigning factor scores.
- Read [references/methodology.md](references/methodology.md) before calculating sPEG or fair value.
- Read [references/output-template.md](references/output-template.md) before producing a full report.
- Read [references/v1.6-migration.md](references/v1.6-migration.md) only when comparing with a pre-v1.6 score or explaining the redesign.

## Non-negotiable invariants

1. **Score one scarce asset.** F1-F5 must refer to the same product, capability, license, network, or bottleneck. Do not take F1 from one segment, F4 from another, and F5 from consolidated demand.
2. **Match earnings to the scored asset.** Apply company-wide sPEG only when the scored asset drives a majority of normalized earnings or clearly drives the marginal earnings underwritten. Otherwise isolate the segment and use a sum-of-the-parts analysis. If isolation is impossible, provide a qualitative scarcity diagnostic without a company-wide fair price.
3. **Use NTM EPS for headline sPEG.** `Forward P/E` always means current price divided by next-twelve-month diluted EPS. A price divided by mid-cycle EPS is a separate `normalized P/E`; never relabel it Forward P/E or use it as the headline sPEG numerator.
4. **Do not fabricate consensus.** If FY3 EPS, NTM EPS, price, or another required input is unavailable, ask for it or label an analyst scenario explicitly. Never call a constructed path consensus.
5. **Use deterministic arithmetic.** Run `scripts/speg_calculator.py`; do not copy arithmetic from a worked example or calculate the final table by hand.
6. **No automatic scarcity-to-price multiplier.** Factor scores justify scenario assumptions and falsifiers. They do not directly multiply a fair P/E.
7. **F4 deterioration must not raise value.** Fast/slow is an asset characteristic, not a discount switch tied to the current F4 score. Model F4 reversion by lowering EPS, growth, duration, or cash conversion and/or raising the required return in a named downside scenario.
8. **Separate intrinsic value from positioning.** Crowding can change sizing, entry timing, and required margin of safety. It does not rewrite intrinsic fair value or the fundamental valuation tier.
9. **No price-independent actions.** Never recommend adding "at any price" or "unconditionally." Every add, trim, and exit rule must require both a price condition and a thesis condition.
10. **No external-skill dependency.** If macro, credit, or portfolio signals are unavailable, state the missing evidence and continue with explicit assumptions. Do not invent another skill's state.

## Validity gates

Stop the numerical sPEG calculation when any gate fails:

| Gate | Required action |
|---|---|
| NTM diluted EPS <= 0 | Do not calculate P/E or sPEG. Use an appropriate alternative valuation. |
| Normalized 3-year EPS CAGR <= 0 | Do not calculate sPEG. A scenario valuation may still be appropriate. |
| No single identifiable scarce asset | Do not calculate company-wide sPEG. |
| Scored asset and earnings base do not match | Isolate the segment or stop at qualitative scoring. |
| Financial, pure commodity, or distressed issuer | Use the appropriate sector or asset framework. |
| SM < 3.0 | Report the diagnostic score only; do not apply sPEG interpretation bands. |
| Required valuation input unsupported | Do not publish a fair price; identify the missing input. |

## Workflow

### 1. Define the unit of analysis

State:

- issuer, ticker, exchange, currency, and share/ADR ratio;
- the one scarce asset being scored;
- the revenue, earnings, or marginal-profit exposure to that asset;
- whether the valuation is company-wide, segment-level, or qualitative only.

For conglomerates, prefer segment scoring and sum-of-the-parts. Do not blend unrelated moats into one Scarcity Multiplier.

### 2. Build the evidence ledger

Label every decision-driving input as one of:

- `issuer-reported fact`
- `market data`
- `consensus estimate`
- `derived calculation`
- `analyst assumption`
- `management claim`
- `missing / unverified`

Use current price and estimate dates. Cite primary filings or investor materials for reported facts and name the provider/date for consensus. A generic source list is not enough for a decision-driving claim.

### 3. Check gates and score scarcity

Use the scoring rubric. For each factor provide:

- score and evidence;
- confidence: high, medium, or low;
- a specific downgrade trigger;
- the affected scenario variable if the trigger fires.

Calculate structural SM. If rent is capped or not captured, keep structural SM visible and describe the constraint; do not invent an `effective SM` that has no defined valuation mapping.

### 4. Calculate headline sPEG

Compute CAGR from EPS levels:

```text
raw CAGR = (FY3 diluted EPS / NTM diluted EPS)^(1/3) - 1
```

Normalize cyclicals with an explicit analyst assumption and show both raw and normalized rates. Cap the headline normalized rate at 50%. GAAP EPS already expenses stock compensation; do not subtract SBC twice. If using adjusted EPS that adds SBC back, deduct after-tax SBC per diluted share and show the bridge.

Prepare a JSON input and run:

```bash
python scripts/speg_calculator.py analysis.json
```

### 5. Build valuation scenarios

Use at least three scenarios when publishing a fair value:

- downside/floor;
- base;
- upside.

Each scenario must specify its own EPS base or explicit EPS path, growth, duration, cash conversion, terminal growth, and required return. Required return must explicitly include macro, cyclicality, country/FX, customer-credit, and geopolitical risk where relevant. Do not represent a fixed 0.85 or 0.75 multiplier as equivalent to a universal discount-rate change.

For a cyclical peak, use an explicit EPS and cash-conversion path. Do not add a separate windfall credit to a fade model unless it replaces—not supplements—the same forecast cash flows.

Only add excess cash after removing its after-tax income from EPS. Otherwise leave the equity value unadjusted and explain that P/E already uses equity earnings. Use the same principle for net debt: if a capital-structure bridge is needed, use operating earnings or unlevered cash flow rather than mixing net income with an EV bridge.

### 6. Stress and reconcile

At minimum test:

- normalized growth lower and higher;
- duration lower and higher;
- required return higher and lower;
- cash conversion lower and higher;
- F4 reversion translated into operating assumptions;
- segment mix or share loss where relevant;
- country/geopolitical downside where material.

The calculator must pass monotonicity: lower growth, shorter duration, lower conversion, or a higher required return cannot increase value, holding everything else constant.

### 7. Interpret and act

Report two separate conclusions:

- **Fundamental valuation tier:** based on scenario-weighted value versus spot.
- **Portfolio action:** incorporates evidence confidence, crowding, catalysts, downside, and portfolio overlap.

Use these non-overlapping fundamental tiers:

| Upside to scenario-weighted value | Tier |
|---|---|
| > +50% | Material undervaluation |
| > +20% and <= +50% | Undervaluation |
| >= -10% and <= +20% | Fair-value range |
| >= -30% and < -10% | Overvaluation |
| < -30% | Material overvaluation |

These bands describe modeled price/value distance only; they are not actions and are not a backtested edge. A material-undervaluation result does not establish high conviction when the downside scenario is below -20%, key inputs are low-confidence, or the thesis lacks an observable catalyst.

### 8. Define falsifiers and action rules

Rank falsifiers by lead time and impact. Each must name the metric, threshold, and review window. Every action requires:

- a price or valuation condition;
- a thesis/evidence condition;
- a portfolio-risk condition where relevant.

Do not prescribe a position weight without the user's portfolio constraints.

## Output posture

Use one of:

- `Decision-grade`: primary inputs verified, arithmetic deterministic, segment scope matched, scenarios complete.
- `Research-grade`: useful but one or more material inputs are analyst assumptions.
- `Qualitative only`: scarcity analysis is possible but fair value is unsupported.
- `Out of framework`: validity gate failed.

Always state that sPEG has not been validated on realized returns unless a cited backtest exists. Log the as-of price, inputs, factor scores, scenario values, decision posture, and 12-month review date.

## Mode B — sPEG Index assessment (Scarcity Durability v1.0)

Method id `speg-index-scarcity-v1.0.0`, profile schema `speg-index-profile-v1.0.0`, three-to-five-year horizon. The public method page is https://www.exmxc.ai/speg-index/methodology; if it shows a newer version, follow the page and flag the difference.

**Unit.** An identified capability inside a stated business perimeter, not a brand, a growth rate or a stock story. Company admission needs a documented route from that capability to a material company perimeter: at least half of trailing revenue, or a qualitative integrated-capability case central across the main business. Unknown or immaterial exposure cannot be rescued by a high score elsewhere.

**Five anchored judgments, each an integer 0-4.**

| Dimension | Admission floor | A 3 means | A 4 requires |
|---|---|---|---|
| Constraint (C) | 3 | Few feasible alternatives; substantial technical, ecosystem or qualification work | No demonstrated equivalent in the defined application plus multi-stage replication barriers |
| Substitution resistance (S) | 3 | Substantial redesign, qualification or workflow rebuilding | Fundamental architecture or process change with demonstrated obstacles |
| Economic capture (E) | 3 | Retained operating economics across periods, plausibly linked to the capability | Retention through adverse conditions or renewals with limited leakage |
| Persistence (P) | 3 | A credible three-to-five-year path through specified competitive responses | Multi-generation evidence and a supported path beyond five years |
| Cost of defense (D) | 2 | Material benefit after reviewed R&D, operating and capital demands | Resilient retention through an adverse period after full defense spending |

Unknown is null, never zero. SDS is the sum only when all five are known. It is ordinal, always shown with its C/S/E/P/D vector, and never treated as a probability, percentile or return rank.

**Admission is gated, not ranked.** All must pass independently:
1. C, S, E and P each at least 3; D at least 2.
2. The company-level materiality route is adequate.
3. Every admission-critical dimension is at least Moderate confidence. Low cannot admit; Unassessable makes that dimension and the total null. Overall confidence is the weakest decisive dimension, never an average.
4. The minimum evidence packet, the current structural review and the event check pass.

A total of 14 follows from the floors but is not a gate: a company can total 14 and fail C.

**Minimum evidence packet:** current financials with a prior-period comparator; structural capability evidence; one external-origin source on the mechanism or feasible alternatives (reposts and joint announcements are not independent origins); an explicit capture argument; a defense-cost review; a company-perimeter rationale; a credible counter-hypothesis.

**Valuation boundary.** SDS never becomes a multiplier and changes neither PEG nor economic sPEG. Conventional PEG needs a current, matched, positive FY1-FY4 EPS path and a verified security basis. Economic sPEG needs a separately qualified paired economic model. Either can be unavailable while the scarcity judgment stands; missing inputs stay null. Never insert M=1 or relabel PEG as sPEG.

**Cadence and events.** Full reviews quarterly; structural reviews no older than 90 days. Material customer losses, substitute qualification, pricing resets, new capacity, acquisitions, financing strain and operative restrictions trigger an event review, targeted within five trading sessions of adequate primary evidence. An unresolved event moves a member under review and it stops counting as currently qualified. Releases are immutable: keep the original cutoff, publication time, effective time and predecessor.

**Limits to state.** The dimensions are correlated and not statistically validated as independent; the cohort is purposive; thresholds are governance choices, not optimized cutoffs; cross-sector comparison stays judgment-based.

**Output.** For each company: capability and perimeter, the C/S/E/P/D vector with evidence and confidence per dimension, SDS (or null), each gate pass/fail, admit / not admitted / under review, the counter-hypothesis, and the next review date. Report PEG or economic sPEG beside it only when their own inputs qualify.

## Attribution

sPEG was developed by Mike Ye at exmxc.ai. The framework remains a living research method; version numbers must be shown when comparing scores. v1.7 (2026-11-16): added Mode B, the sPEG Index Scarcity Durability v1.0 assessment, and the rule that the two modes never mix; the Mode A valuation method is unchanged from v1.6.

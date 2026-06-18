---
name: spec-calculation
description: Score equities using the sPEG framework (Scarcity-adjusted PEG) developed by Mike Ye. Use this skill whenever the user asks to value a stock, score scarcity, calculate sPEG, evaluate a position, identify whether something is mispriced, or analyze a company through a structural-scarcity lens rather than a pure growth or multiple framework. Also use when the user mentions "Scarcity Multiplier," "five-factor scoring," "demand durability," "AI infrastructure scarcity," or any of: HBM, EUV, 3nm/2nm process, hyperscaler capex, semiconductor bottlenecks. This skill is the canonical implementation of the sPEG framework — use it instead of generic PEG analysis whenever scarcity dynamics could meaningfully affect the valuation, even if the user doesn't explicitly invoke the framework by name.
---

# sPEG Framework Skill

**sPEG** = Forward P/E ÷ (Growth% × Scarcity Multiplier)

A scarcity-adjusted variant of PEG (Price/Earnings to Growth) that incorporates structural scarcity dynamics into equity valuation. Developed by Mike Ye (exmxc.ai) to identify mispricings where the market is treating scarce-input businesses as commodity earnings streams.

The framework operates on the thesis that traditional PEG fails when growth is *bounded by a scarce input the market has not yet recognized as scarce*. PEG implicitly assumes commodity-like supply elasticity. sPEG corrects this by quantifying the scarcity dimension and embedding it directly in the valuation ratio.

---

## When This Skill Triggers

Apply this framework whenever any of the following are true:

- A company's earnings depend on a structurally scarce input (manufacturing process node, raw material, regulatory license, network effect, contract regime)
- The user is evaluating an AI infrastructure name (semis, networking, power, cooling, HBM, EUV, foundry)
- A growth name is trading at a deceptively low multiple — the question is whether scarcity is unpriced or whether growth is overestimated
- The user mentions PEG, multiple compression, "is X mispriced," "what's the real value," or asks to "score" a position
- Cross-position analysis across an AI infrastructure portfolio
- Thesis construction or thesis updates on positions with structural-scarcity characteristics

Do NOT use this skill for:
- Pure commodity businesses with no structural scarcity
- Financial companies (banks, insurers) where book value frameworks apply
- Distressed/special situations where valuation is asset-driven not earnings-driven
- Macro or top-down asset allocation questions
- Companies failing the Validity Gates (non-positive forward EPS or growth)

**Scope guard:** the trigger language is broad ("evaluate a position," "is X mispriced") so the skill catches scarcity-relevant questions even when unnamed. But broad triggering is not a license to force the framework onto names where scarcity is irrelevant. If, on inspection, the name has no identifiable scarce input (Scarcity Multiplier would score < 2), say so and use ordinary valuation judgment instead of producing a low-information sPEG.

---

## The Framework

### Core Formula

```
sPEG = Forward P/E ÷ (Growth% × Scarcity Multiplier)
```

Where:
- **Forward P/E** = current price ÷ next 12-month consensus EPS
- **Growth%** = *normalized* forward EPS growth rate over the **next 3 years (3-year forward CAGR)**, expressed as a whole number (e.g., 25 for 25%). See "Growth Input Discipline" below — this input is NOT the raw consensus number for cyclical names.
- **Scarcity Multiplier** = sum of five scarcity factor scores (each 1-5), divided by 5

**Design note — why multiplicative.** sPEG treats Growth × Scarcity as a single "deserved-multiple" denominator. This means a 10%-grower at SM 5 (denominator 50) scores identically to a 50%-grower at SM 1 (denominator 50). That is intentional: the framework asserts that durable pricing power (high scarcity) and fast growth are interchangeable contributors to deserved multiple. Be conscious of it. A low-growth/high-scarcity name and a high-growth/low-scarcity name with the same sPEG are *different businesses* — the falsifier hierarchy and sensitivity analysis are what distinguish them. Note also that at **SM = 1.0 (no scarcity), sPEG reduces exactly to classic PEG** — which is why the threshold table below is only valid in the framework's intended domain (SM ≥ 3); see the calibration note.

### Validity Gates — check BEFORE scoring

Do not produce an sPEG number if any of these hold; instead state which gate failed and stop or fall back:

| Condition | Action |
|---|---|
| NTM consensus EPS ≤ 0 (no/negative forward earnings) | Forward P/E is undefined. Do NOT compute sPEG. Note it, and if a read is still wanted, fall back to an EV/Sales-vs-scarcity qualitative read and say so explicitly. |
| Forward 3-yr EPS growth ≤ 0 (flat/declining) | Denominator is non-positive → sPEG meaningless or sign-flipped. Do NOT compute. The scarcity thesis is moot if earnings aren't growing; treat as out-of-framework. |
| Scarcity Multiplier < 2.0 | sPEG is computable but the threshold table is miscalibrated here (it collapses toward raw PEG). Report the number but flag that the position is outside the framework's reliable domain and PEG-style judgment applies. |
| Financial/commodity/distressed business | Out of scope per "When This Skill Triggers." Decline and name the appropriate sector framework. |

### Growth Input Discipline (critical — the single largest source of error)

Growth% enters the denominator linearly, so an inflated growth number produces an artificially attractive (low) sPEG. The framework's most common failure is feeding it a **peak-cycle consensus growth rate** and reading the resulting tiny sPEG as "scarcity unpriced" when it is really just "growth temporarily spiking."

Rules:
1. **Pin the window to a 3-year forward EPS CAGR.** Not 1-year, not next-quarter. A single hot forward year (common for cyclical semis/memory at a cycle peak) must be averaged against the out-years.
2. **For cyclical names (memory, DRAM, foundry utilization-sensitive, commodity-linked), normalize to a through-cycle growth rate** rather than using the peak. If consensus shows 75% next year decelerating to 20% by year 3, do NOT use 75 — use the 3-year CAGR, and if even that is cycle-peak-distorted, haircut toward the mid-cycle rate and SAY you did.
3. **Cap Growth% at 50 for scoring purposes.** Any growth above ~50% is almost certainly cyclical-peak or early-ramp and not a durable 3-year rate; using it produces false precision at the extreme-low end of the sPEG scale. If you believe >50% is genuinely durable, state the case explicitly and show the uncapped number only as a sensitivity bound, not the headline.
4. **Whatever you use, the Sensitivity section (required output) must show the result across the plausible growth range** so the reader sees how much the conviction depends on the growth assumption.

### Macro / Discount-Rate Context (interpretive guardrail — no formula change)

Discount rates do **not** enter the Scarcity Multiplier and do **not** change the sPEG formula. The Scarcity Multiplier remains a business-structure score: irreplaceability, replication timeline, supply concentration, throughput control, and demand durability.

Macro and discount-rate changes enter sPEG only through the market valuation input — the **Forward P/E numerator** — and through the interpretation of how much multiple compression/expansion the market is already pricing. Do not add a sixth factor, haircut the Scarcity Multiplier, or put rates directly in the denominator.

When the rate regime has changed materially, state it as context: higher discount rates can compress Forward P/E even when scarcity is intact; lower rates can inflate the numerator without improving scarcity. The framework should distinguish "scarcity thesis intact but numerator repriced" from "scarcity score deteriorated."

### The Five Scarcity Factors

Each factor is scored 1-5. Sum the five scores and divide by 5 to get the Scarcity Multiplier (range: 1.0 to 5.0).

#### 1. Irreplaceability

How substitutable is the company's product or position within a 3-year horizon?

| Score | Definition |
|-------|------------|
| 5 | No credible substitute exists; replacement would require fundamental architectural change in downstream systems |
| 4 | Theoretical substitutes exist but require multi-year qualification cycles |
| 3 | Substitutes exist but cost or performance penalty makes switching uneconomic |
| 2 | Substitutes exist with manageable switching costs |
| 1 | Commodity substitution available |

#### 2. Replication Timeline

How long would a competitor need to credibly replicate the company's capability?

| Score | Definition |
|-------|------------|
| 5 | 5+ years; requires capital, process IP, and qualification cycles that cannot be compressed |
| 4 | 3-5 years; capital-intensive and capability-gated |
| 3 | 2-3 years; capital-intensive but achievable with sufficient investment |
| 2 | 1-2 years; primarily a capital and execution challenge |
| 1 | Under 1 year; capability is widely understood and capital is available |

#### 3. Supply Concentration

What is the market structure on the supply side?

| Score | Definition |
|-------|------------|
| 5 | Monopoly or duopoly |
| 4 | Three-player oligopoly with material capacity differentiation |
| 3 | Three to five players with rough capacity parity |
| 2 | Five to ten players with active competition |
| 1 | Fragmented; commodity-like supply |

#### 4. Throughput Control

How is the supply governed and what is the demand-supply tension?

| Score | Definition |
|-------|------------|
| 5 | Multi-year fixed-price contracts (LTAs); industry fulfillment rate below 60%; capacity expansion capex-gated 18+ months out |
| 4 | Mix of contract and spot pricing; fulfillment 60-75%; expansion possible within 12-18 months |
| 3 | Primarily spot pricing with some contract overlay; fulfillment 75-90% |
| 2 | Spot pricing dominant; supply roughly matches demand |
| 1 | Oversupply conditions; spot dynamics; pricing pressure |

#### 5. Demand Durability

How long will demand for this scarce input persist — and what happens to demand as the bottleneck is alleviated? This is the framework's primary cyclicality guard *inside* the Scarcity Multiplier. Score it by asking: **when supply catches up and Throughput Control (F4) reverts, does demand persist or evaporate?** Durable demand grows into new supply; fragile demand *was* the shortage and fades with it. Demand durability is inversely related to bottleneck alleviation.

This factor subsumes and improves on the older "Downstream Dependency" measure: current-moment dependency is a snapshot; durability adds the trajectory. The scarcity premium should be paid for *durable* scarcity, not momentary scarcity. Inputs to the score include how critical the input is to the downstream business case (a collapsing-without-it dependency supports durability) AND whether that dependency is structural/secular or a cycle-peak artifact.

| Score | Definition |
|-------|------------|
| 5 | Secular, multi-cycle demand with multiple independent drivers; persists regardless of any single capex wave; alleviating the current bottleneck does not reduce demand (demand grows into new supply) |
| 4 | Durable across the visible 3-year horizon with more than one independent driver; modest sensitivity to bottleneck relief |
| 3 | Healthy demand tied to a single dominant driver (e.g., one capex cycle); softens meaningfully as the bottleneck clears |
| 2 | Largely cyclical/spike-driven demand; fades as supply catches up or the cycle turns |
| 1 | Transient shortage artifact; demand evaporates once the bottleneck is alleviated |

**Interaction with F4 (Throughput Control):** F4 measures whether supply is tight *now*; F5 measures whether demand survives that tightness resolving. They are orthogonal and their divergence is the signal. Tight-now + durable (F4=5, F5=5) is structural scarcity (e.g., HBM into secular AI demand). Tight-now + fragile (F4=5, F5=2) is a cyclical spike masquerading as scarcity — exactly the trap Common Error #1 warns about, now caught numerically.

### Scarcity Multiplier Calculation

```
Scarcity Multiplier = (F1 + F2 + F3 + F4 + F5) / 5
```

(The ÷5 is cosmetic normalization to a 1.0–5.0 range; the raw 5–25 sum would work identically with rescaled thresholds. Don't read significance into the division itself.)

Range: 1.0 to 5.0
- 1.0-2.0: No meaningful scarcity premium
- 2.0-3.0: Modest scarcity dynamics
- 3.0-4.0: Significant structural scarcity
- 4.0-5.0: Severe structural scarcity; framework most useful in this range

**Factor independence (post-v1.2).** Replacing the old "Downstream Dependency" with **Demand Durability** resolved the largest collinearity problem — F1 (Irreplaceability, supply-side) and the old F5 (demand-side dependency) measured nearly the same "stuck-ness" from opposite ends and never diverged. Demand Durability adds a genuinely orthogonal temporal axis. The remaining related pair is F3 (Supply Concentration) and F4 (Throughput Control), but these are *informatively* separable rather than redundant: F3 is structural and slow-moving (how many players), F4 is cyclical and fast-moving (is it tight right now). They legitimately diverge across a cycle — a 3-player oligopoly (F3=5) can be oversupplied (F4=1) in a downturn — and that divergence is itself a signal. Do not over-interpret tiny Multiplier differences between names, but the factors now span roughly four independent dimensions rather than three. If F1 and F5 *both* run high with no scrutiny of the cycle, you have probably mis-scored F5 — durability is where cyclical names should lose points.

### sPEG Interpretation Thresholds

**Validity:** this table is calibrated for the framework's intended domain, **SM ≥ 3.0**. At low SM the formula collapses toward raw PEG (at SM = 1.0 it *is* PEG), where 1.0 means fair value, not "approaching overvaluation." Do not apply the short-side thresholds to low-scarcity names — use ordinary PEG judgment there and flag that the name is out of domain.

| sPEG Range | Signal | Interpretation |
|------------|--------|----------------|
| <0.1 | Scarcity premium completely unpriced | Highest-conviction long; market is treating the company as commodity. **Caution:** an sPEG this low is frequently an artifact of an un-normalized cyclical growth input — verify the growth number obeys the Growth Input Discipline before trusting it. |
| 0.1-0.3 | High-conviction long | Substantial mispricing; scarcity premium partially recognized |
| 0.3-0.7 | Long signal | Moderate mispricing |
| 0.7-1.0 | Neutral to long | Approaching fair value |
| 1.0-1.5 | Neutral to short | Approaching overvaluation given scarcity-adjusted growth (SM ≥ 3 only) |
| >1.5 | Short signal | Overpriced relative to scarcity-adjusted growth (SM ≥ 3 only) |

Note: sPEG thresholds are tighter than traditional PEG because the denominator is amplified by the Scarcity Multiplier.

---

## How to Apply the Framework

When the user asks you to score a position or calculate sPEG on a company, follow this sequence:

### Step 1: Gather Inputs and Check Gates

Required:
- Forward P/E (consensus next-12-month EPS basis)
- Forward EPS growth rate — **3-year forward CAGR, normalized per the Growth Input Discipline** (not the raw peak-year number for cyclicals)
- Identification of the scarce input or capability driving the thesis
- Macro / discount-rate context as of the analysis date, if materially changed (interpretive only; no formula change)

First run the **Validity Gates**. If NTM EPS ≤ 0, forward growth ≤ 0, or the business is financial/commodity/distressed, stop and report the gate failure rather than forcing a number.

Pull current data from web search, SEC filings, IR pages, or available financial data MCPs. If forward consensus is unavailable, ask the user for the figures rather than estimating. Always record the as-of date of the inputs.

### Step 2: Score Each Factor

For each of the five factors:
1. State the factor
2. Assign a score 1-5
3. Provide explicit reasoning citing concrete evidence (contract terms, market share data, process node specifics, fulfillment rates, etc.)
4. Identify the **downgrade trigger** — what specific observable event would lower this score by one notch

### Step 3: Calculate

```
Scarcity Multiplier = (F1 + F2 + F3 + F4 + F5) / 5
sPEG = Forward P/E / (Growth% × Scarcity Multiplier)
```

### Step 4: Sensitivity (REQUIRED — do not skip)

A point sPEG is false precision because the result is highly sensitive to the growth input. Recompute and report sPEG across:
- Growth: base, base −30%, base +30% (and, for cyclicals, the uncapped peak number as an explicit upper-bound case)
- Scarcity Multiplier: base, base −0.5, base +0.5

State whether the **conviction tier holds across the range** (robust) or flips tiers (fragile). A robust 0.13–0.26 is a different recommendation than a fragile 0.04–0.40 even if the point estimate is similar.

### Step 5: Interpret

Map the sPEG result to the threshold table. Identify which conviction tier the position lands in. Add a brief note if the current discount-rate regime is affecting the Forward P/E numerator; do not adjust the Scarcity Multiplier for rates.

### Step 6: Produce Falsifier Hierarchy

Rank the five downgrade triggers in order of lead-time and impact. The earliest, most observable trigger goes first. This becomes the watchlist for thesis maintenance.

### Step 7: Output

Use the report structure below.

---

## Required Output Structure

ALWAYS produce the analysis in this exact format:

```markdown
# sPEG Analysis: [TICKER]

**Position:** [Long / Neutral / Short]
**Date:** [YYYY-MM-DD]
**Analyst:** [User]

## Thesis Statement

[1-2 sentence description of the scarce input or capability driving the thesis]

## Inputs

- Forward P/E: [Xx]
- Forward EPS Growth (3-yr CAGR, normalized): [X%]  — note if normalized/capped from a raw consensus figure, and state the raw figure
- Macro / discount-rate context: [benign / tightening / easing / shock / not material] — interpretive only; discount rate stays out of the Scarcity Multiplier
- Data source: [web search / SEC / IR / MCP provider / user-supplied], as of [date]

## Scarcity Multiplier Scoring

### Factor 1: Irreplaceability — [Score]/5
[Reasoning, specific evidence]
**Downgrade trigger:** [Specific observable event]

### Factor 2: Replication Timeline — [Score]/5
[Reasoning]
**Downgrade trigger:** [Specific observable event]

### Factor 3: Supply Concentration — [Score]/5
[Reasoning]
**Downgrade trigger:** [Specific observable event]

### Factor 4: Throughput Control — [Score]/5
[Reasoning]
**Downgrade trigger:** [Specific observable event]

### Factor 5: Demand Durability — [Score]/5
[Reasoning — including what happens to demand as the bottleneck is alleviated]
**Downgrade trigger:** [Specific observable event]

**Total: [X]/25 → Scarcity Multiplier = [X.X]**

## sPEG Calculation

sPEG = [Forward P/E] / ([Growth%] × [Scarcity Multiplier]) = **[X.XX]**

## Sensitivity

| Scenario | Growth% | SM | sPEG | Tier |
|---|---|---|---|---|
| Base | | | | |
| Growth −30% | | | | |
| Growth +30% | | | | |
| SM −0.5 | | | | |
| SM +0.5 | | | | |
| (Cyclical) uncapped peak growth | | | | |

**Robustness:** [Conviction tier holds across range = robust / flips = fragile, and which assumption it hinges on]

## Interpretation

[Conviction tier and what the result implies. Include whether the Forward P/E numerator already reflects a materially changed discount-rate regime; do not treat rates as a Scarcity Multiplier input.]

## Falsifier Hierarchy

Ranked by lead time and impact:
1. [Earliest, most observable trigger] — Lead time: [X quarters]
2. [Second trigger] — Lead time: [X quarters]
3. [Third trigger] — Lead time: [X quarters]
4. [Fourth trigger]
5. [Fifth trigger]

## Position Sizing Implication

[Brief comment on how the conviction tier maps to portfolio weighting]
```

---

## Cross-Position Consistency Rules

When scoring multiple positions, maintain consistency:

1. **Score relative to a 3-year horizon.** Irreplaceability scored over a 30-year horizon would score every business at 1; scored over a 6-month horizon would score every monopoly at 5. The 3-year window is the discipline.

2. **Use observable evidence, not narrative.** "Strong moat" is not a 5 on Replication Timeline. "Three-year qualification cycle confirmed by Nvidia disclosure in 2025" is.

3. **The Scarcity Multiplier compares within a portfolio context.** If two names score 4.8 and 4.2, that's a meaningful relative ranking; if both score 4.5, the differentiation comes from sPEG (which incorporates current valuation). (Illustrative numbers only — not canonical scores for any specific ticker.)

4. **Downgrade triggers must be specific and observable.** "Competition intensifies" is not a trigger. "Samsung wins exclusive Nvidia HBM4 slot" is.

5. **Refresh inputs quarterly.** Forward P/E and growth estimates change; scarcity scores change more slowly but should be reviewed when downgrade triggers fire.

---

## Worked Example: MU (Micron Technology)

See `examples/MU-analysis.md` for the canonical full worked example. The MU thesis illustrates:
- A position the market treats as commodity DRAM (low forward P/E)
- HBM exposure that is structurally scarce (contract regime, three-player oligopoly, downstream AI dependency)
- **The cyclical-growth normalization in action** — why the raw consensus growth number produces a misleadingly low sPEG and how the Growth Input Discipline corrects it
- **A worked Sensitivity table** showing the conviction tier holds even after normalization
- Falsifier hierarchy anchored on LTA contract language as the earliest signal

---

## Common Errors to Avoid

1. **Conflating cyclical scarcity with structural scarcity.** Memory shortages in 2021 were cyclical. HBM scarcity is structural because it is governed by contract regime and capex lead times, not spot demand.

2. **Scoring on hopes rather than evidence.** If you can't cite a specific contract, market share figure, or qualification cycle, the score is too high.

3. **Treating the Scarcity Multiplier as static.** It is dynamic. When downgrade triggers fire, the multiplier compresses. The thesis must update.

4. **Using sPEG on financial companies or commodity businesses.** The framework is designed for businesses with identifiable scarce inputs. Banks, insurers, and pure commodity producers should be valued with appropriate sector frameworks.

5. **Skipping the falsifier hierarchy.** The hierarchy is what makes the thesis falsifiable. Without it, sPEG becomes a static valuation snapshot rather than an operational framework.

---

## References

For framework background and lexicon entries, see exmxc.ai:
- "sPEG Framework" — full methodology
- "Scarcity Multiplier" — five-factor scoring detail
- "Four Forces of AI Power" — broader framework context
- "AI Infrastructure Component Thesis" — application to semiconductor stack

## Framework Attribution

sPEG framework developed by Mike Ye (exmxc.ai). This skill is the canonical implementation. Licensed under Apache 2.0. When using or citing the framework, attribution to exmxc.ai is requested but not required.

## Changelog

- v1.0: Initial five-factor framework, formula, thresholds, and output structure.
- v1.1 (2026-05-29): Audit fixes. Added (1) Growth Input Discipline — 3-yr CAGR pin, cyclical normalization, Growth% ≤ 50 cap; (2) mandatory Sensitivity step + output table; (3) Validity Gates for non-positive EPS/growth, low SM, and out-of-scope businesses; (4) threshold calibration note restricting the table to SM ≥ 3 and noting sPEG→PEG at SM = 1; (5) documented factor collinearity (F1/F5, F3/F4) as a known limitation; (7) documented the multiplicative form as an explicit design choice; (8) noted ÷5 is cosmetic; (9) scope guard against forcing the framework onto non-scarce names; (10) de-canonicalized illustrative TSM/NVDA scores. Recreated the missing `examples/MU-analysis.md`.
- v1.2 (2026-05-29): **BREAKING — factor restructure.** Replaced Factor 5 "Downstream Dependency" with **Demand Durability**, which adds an orthogonal temporal axis (how long demand persists, inversely related to bottleneck alleviation) and resolves the F1/F5 collinearity. This builds a cyclicality guard directly into the Scarcity Multiplier, complementing the v1.1 growth normalization. **All existing scores were computed under the old factor set and must be re-scored for comparability** — the criticality/dependency idea now lives inside durability, and cyclical names (which previously scored high on Downstream Dependency) will correctly lose points on Demand Durability. Re-scoring required for the tracked book (MU re-scored in the example; AVGO, VRT, and the rest pending). Treated as a living-document model update per framework owner's versioning practice.
- v1.3 (2026-06-17): Added Macro / Discount-Rate Context interpretive guardrail. No formula change: discount rate remains outside the Scarcity Multiplier and enters only via the Forward P/E numerator. Added Step 5 interpretation note and required-output inputs-template note for rate-regime context.

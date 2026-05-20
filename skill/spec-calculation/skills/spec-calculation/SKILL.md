---
name: spec-calculation
description: Score equities using the sPEG framework (Scarcity-adjusted PEG) developed by Mike Ye. Use this skill whenever the user asks to value a stock, score scarcity, calculate sPEG, evaluate a position, identify whether something is mispriced, or analyze a company through a structural-scarcity lens rather than a pure growth or multiple framework. Also use when the user mentions "Scarcity Multiplier," "five-factor scoring," "AI infrastructure scarcity," or any of: HBM, EUV, 3nm/2nm process, hyperscaler capex, semiconductor bottlenecks. This skill is the canonical implementation of the sPEG framework — use it instead of generic PEG analysis whenever scarcity dynamics could meaningfully affect the valuation, even if the user doesn't explicitly invoke the framework by name.
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

---

## The Framework

### Core Formula

```
sPEG = Forward P/E ÷ (Growth% × Scarcity Multiplier)
```

Where:
- **Forward P/E** = current price ÷ next 12-month consensus EPS
- **Growth%** = forward EPS growth rate (next 2-3 years CAGR), expressed as a whole number (e.g., 25 for 25%)
- **Scarcity Multiplier** = sum of five scarcity factor scores (each 1-5), divided by 5

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

#### 5. Downstream Dependency

How dependent are downstream customers on this supply for their own value creation?

| Score | Definition |
|-------|------------|
| 5 | Downstream business case collapses without this input; supplier holds the bottleneck in the value chain |
| 4 | Critical input but with workaround paths that degrade economics |
| 3 | Important input but downstream value creation is preserved with substitution |
| 2 | One input among many; substitution preserves downstream economics |
| 1 | Optional or interchangeable input |

### Scarcity Multiplier Calculation

```
Scarcity Multiplier = (F1 + F2 + F3 + F4 + F5) / 5
```

Range: 1.0 to 5.0
- 1.0-2.0: No meaningful scarcity premium
- 2.0-3.0: Modest scarcity dynamics
- 3.0-4.0: Significant structural scarcity
- 4.0-5.0: Severe structural scarcity; framework most useful in this range

### sPEG Interpretation Thresholds

| sPEG Range | Signal | Interpretation |
|------------|--------|----------------|
| <0.1 | Scarcity premium completely unpriced | Highest-conviction long; market is treating the company as commodity |
| 0.1-0.3 | High-conviction long | Substantial mispricing; scarcity premium partially recognized |
| 0.3-0.7 | Long signal | Moderate mispricing |
| 0.7-1.0 | Neutral to long | Approaching fair value |
| 1.0-1.5 | Neutral to short | Approaching overvaluation given scarcity-adjusted growth |
| >1.5 | Short signal | Overpriced relative to scarcity-adjusted growth |

Note: sPEG thresholds are tighter than traditional PEG because the denominator is amplified by the Scarcity Multiplier.

---

## How to Apply the Framework

When the user asks you to score a position or calculate sPEG on a company, follow this sequence:

### Step 1: Gather Inputs

Required:
- Forward P/E (consensus next-12-month EPS basis)
- Forward EPS growth rate (consensus 2-3 year CAGR)
- Identification of the scarce input or capability driving the thesis

Pull current data from SEC filings, IR pages, or available financial data MCPs. If forward consensus is unavailable, ask the user for the figures rather than estimating.

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

### Step 4: Interpret

Map the sPEG result to the threshold table. Identify which conviction tier the position lands in.

### Step 5: Produce Falsifier Hierarchy

Rank the five downgrade triggers in order of lead-time and impact. The earliest, most observable trigger goes first. This becomes the watchlist for thesis maintenance.

### Step 6: Output

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
- Forward EPS Growth (Y1-Y3 CAGR): [X%]
- Data source: [SEC / IR / MCP provider / user-supplied]

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

### Factor 5: Downstream Dependency — [Score]/5
[Reasoning]
**Downgrade trigger:** [Specific observable event]

**Total: [X]/25 → Scarcity Multiplier = [X.X]**

## sPEG Calculation

sPEG = [Forward P/E] / ([Growth%] × [Scarcity Multiplier]) = **[X.XX]**

## Interpretation

[Conviction tier and what the result implies]

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

3. **The Scarcity Multiplier compares within a portfolio context.** If TSM scores 4.8 and NVDA scores 4.2, that's a meaningful relative ranking. If both score 4.5, the differentiation comes from sPEG (which incorporates current valuation).

4. **Downgrade triggers must be specific and observable.** "Competition intensifies" is not a trigger. "Samsung wins exclusive Nvidia HBM4 slot" is.

5. **Refresh inputs quarterly.** Forward P/E and growth estimates change; scarcity scores change more slowly but should be reviewed when downgrade triggers fire.

---

## Worked Example: MU (Micron Technology)

See `examples/MU-analysis.md` for the canonical full worked example. The MU thesis illustrates:
- A position the market treats as commodity DRAM (low forward P/E)
- HBM exposure that is structurally scarce (contract regime, three-player oligopoly, downstream AI dependency)
- Resulting sPEG well below 0.1 — the scarcity premium is completely unpriced
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

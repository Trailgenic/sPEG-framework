# Full-report template

Use this structure for a decision-grade or research-grade report. Omit no required field; say `missing / unverified` instead of filling a gap with an estimate.

## Header

- Issuer / ticker / exchange:
- Security and ADR ratio:
- Currency:
- Price and timestamp:
- Framework version: sPEG v1.6
- Decision posture: Decision-grade / Research-grade / Qualitative only / Out of framework
- Valuation scope: company-wide / segment SOTP / qualitative
- Scored scarce asset:
- Earnings exposure to scored asset:

## Executive conclusion

In five lines or fewer state structural SM, headline sPEG, scenario-value range, weighted value and fundamental tier, and the largest unresolved risk. Keep portfolio action separate.

## Validity gates

| Gate | Result | Evidence or implication |
|---|---|---|
| Positive NTM diluted EPS |  |  |
| Positive normalized 3-year growth |  |  |
| One identifiable scarce asset |  |  |
| Earnings match the asset |  |  |
| In-scope issuer |  |  |
| SM at least 3 for interpretation |  |  |
| Valuation inputs supported |  |  |

## Evidence ledger

| Input or claim | Value | Label | Source and date | Confidence |
|---|---:|---|---|---|
| Price |  | market data |  |  |
| NTM diluted EPS |  | consensus / assumption |  |  |
| FY3 diluted EPS |  | consensus / assumption |  |  |
| Normalized CAGR |  | derived / assumption |  |  |
| Cash conversion |  | reported / derived / assumption |  |  |
| Required return |  | analyst assumption |  |  |

Add every other decision-driving item. Cite claims inline; do not rely on an undifferentiated source list.

## Scarcity scorecard

| Factor | Score | Evidence | Confidence | Downgrade trigger | Scenario variable affected |
|---|---:|---|---|---|---|
| F1 Irreplaceability |  |  |  |  |  |
| F2 Replication time |  |  |  |  |  |
| F3 Supply concentration |  |  |  |  |  |
| F4 Tightness and rent capture |  |  |  |  |  |
| F5 Demand durability |  |  |  |  |  |

Report structural SM, D = (F2 + F5) / 2, and fast/slow/mixed classification. Discuss capital independence and rent leakage separately.

## Ratio calculation

| Metric | Value | Formula or bridge |
|---|---:|---|
| Forward P/E |  | Price / NTM diluted EPS |
| Raw 3-year EPS CAGR |  | (FY3 / NTM)^(1/3) - 1 |
| Normalized CAGR |  | Show bridge if different |
| Scoring growth |  | min(normalized CAGR%, 50) |
| Structural SM |  | mean(F1:F5) |
| Headline sPEG |  | Forward P/E / (growth% x SM) |

If relevant, show normalized P/E separately. Never label it Forward P/E.

## Scenario valuation

| Scenario | EPS path / growth | Duration | Conversion | Terminal growth | Required return | Weight | Fair value | Upside vs spot |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Downside |  |  |  |  |  |  |  |  |
| Base |  |  |  |  |  |  |  |  |
| Upside |  |  |  |  |  |  |  |  |

Explain each scenario as a coherent operating state. Show calculator output, weighted value if used, and the fundamental valuation tier. State the downside explicitly.

## What spot appears to imply

Use a stated reverse-valuation sensitivity—such as growth, duration, or cash conversion—to describe what must be true for spot price to be supported. Label the result as model-implied, not market fact.

## Sensitivities and falsifiers

| Rank | Metric | Threshold | Review window | Lead time | Valuation consequence |
|---:|---|---|---|---|---|
| 1 |  |  |  |  |  |

Include lower/higher growth, duration, conversion, and required return; an F4 operating reversion; share/mix loss; and geopolitical risk where material.

## Decision

- Fundamental valuation tier:
- Evidence confidence:
- Crowding / positioning:
- Catalyst and expected timing:
- Portfolio action, if portfolio constraints are known:
- Why action differs from—or matches—the fundamental tier:

Every add/trim/exit rule must combine a price condition, thesis condition, and relevant portfolio-risk condition. Never use “at any price” or “unconditionally.”

## Audit log

- Input file:
- Calculator version:
- Run timestamp:
- Review date:
- Unvalidated-framework disclosure: sPEG has not been validated on realized returns unless a cited backtest exists.


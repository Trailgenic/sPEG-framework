# Calculation and valuation methodology

This document defines the reproducible arithmetic for sPEG v1.6. `scripts/speg_calculator.py` is the executable specification.

## 1. Scope and input record

Create a dated input record containing:

- issuer, security, exchange, currency, share/ADR ratio, and price timestamp;
- one named scarce asset and the earnings stream it supports;
- NTM diluted EPS and FY3 diluted EPS on the same accounting basis;
- F1–F5 scores from the scoring rubric;
- at least three valuation scenarios for a publishable fair value;
- a source label, source/date, and confidence for every decision-driving input.

Company-wide valuation is valid only if the asset drives most normalized earnings or clearly drives the marginal earnings underwritten. Otherwise isolate segment cash flow and value the residual business separately. If that cannot be done credibly, stop at a qualitative diagnostic.

## 2. Headline sPEG

Use the following definitions exactly:

```text
Forward P/E = current price / NTM diluted EPS
Raw 3-year CAGR% = 100 x [(FY3 diluted EPS / NTM diluted EPS)^(1/3) - 1]
Scoring growth% = min(normalized 3-year EPS CAGR%, 50)
SM = mean(F1, F2, F3, F4, F5)
sPEG = Forward P/E / (Scoring growth% x SM)
```

The growth term uses percentage points: 20% is entered as `20`, not `0.20`. Report raw CAGR and normalized CAGR. Any normalization is an `analyst assumption` with a bridge and sensitivity.

Headline sPEG is invalid when NTM EPS or normalized growth is non-positive. When SM is below 3.0, report it as `diagnostic only` and do not use interpretation bands.

Do not substitute a mid-cycle EPS denominator for NTM EPS. If useful, show `normalized P/E = price / mid-cycle EPS` as a separate supplemental statistic.

## 3. Accounting consistency

- Use diluted per-share values and a consistent share class.
- GAAP EPS already includes stock-based compensation. Do not subtract SBC again.
- If adjusted EPS adds SBC back, subtract after-tax SBC per diluted share and reconcile to the adjusted figure.
- If aggregating free cash flow across years or peers, aggregate dollars first and divide by aggregate earnings. Do not average ratios with incompatible denominators.
- Do not combine nominal EPS growth with a real discount rate.
- Record currency conversion and ADR ratio explicitly.

## 4. Scenario valuation

The calculator converts equity EPS to cash available to equity using a scenario cash-conversion rate and discounts it at a nominal required return:

```text
cash_t = EPS_t x cash_conversion_t
PV forecast = sum[cash_t / (1 + r)^t]
terminal value_T = cash_T x (1 + g_terminal) / (r - g_terminal)
fair operating value = PV forecast + PV terminal
```

Require `r > g_terminal`. Required return must state how it reflects macro/cycle, country/FX, customer-credit, and geopolitical risk where material. A fixed price haircut is not interchangeable with a discount-rate change because it does not affect timing or terminal value consistently.

### Generated-fade mode

Use for normalized businesses with a defensible smooth path:

- `eps_base` is NTM EPS, treated as year 1;
- `duration_score` must be 1–5 and creates `duration + 1` persistence years;
- growth above 25% is capped after year 3;
- growth then fades linearly over five years to terminal growth;
- cash conversion recovers linearly on a fixed five-year clock, independent of duration;
- half-point duration values interpolate between the two adjacent integer valuations.

Generated-fade growth must be at least terminal growth. Use an explicit EPS path when near-term growth is below terminal growth. This keeps duration defined as persistence of above-terminal economics. The duration convention is a modeling choice, not empirical truth. Sensitize it.

### Explicit-path mode

Use for cyclicals, loss of share, step changes, regulatory events, capacity ramps, or other non-smooth outcomes. Supply annual `eps_path` and a matching `cash_conversion_path`, or a single conversion value. The last explicit year anchors terminal value.

Do not add a separate windfall credit for cash flows already included in either path. Doing so double counts the same economics.

## 5. Cash and capital structure

P/E uses equity earnings, which normally include net interest income or expense. Therefore:

- add `excess_cash_per_share` only when after-tax net interest attributable to that cash has been removed from the EPS path;
- set `eps_excludes_net_interest: true` to certify that adjustment;
- do not subtract net debt from a value derived from net income. If an enterprise-value bridge is necessary, switch to an unlevered operating-cash-flow method.

Document trapped cash, taxes, minimum operating cash, and convertibility limits before calling cash “excess.”

## 6. Scenario design and weighting

A fair-value report needs downside, base, and upside scenarios. Each must carry a coherent joint state, not independent best/worst values pasted together. State:

- EPS base or annual path;
- growth and persistence;
- cash conversion;
- terminal growth and required return;
- operational narrative and falsifier;
- weight, if using a weighted value.

Weights are optional. If supplied, every scenario needs one and they must sum to 1. Treat weights as analyst assumptions. Show all stand-alone values so the weighted output cannot conceal a weak downside.

## 7. Stress tests and invariants

Holding other inputs constant, fair value must not rise when:

- growth falls;
- duration shortens;
- cash conversion falls;
- required return rises.

F4 is an ordinal observation and is not passed directly into the valuation engine. Translate an F4 downgrade into named operating changes—for example a lower EPS path, shorter duration, lower conversion, or higher required return. This eliminates the prior paradox in which weaker throughput could remove a cycle haircut and increase value.

Run a segment-mix/share-loss case and country/geopolitical case when material. If any monotonicity test fails, do not publish the valuation.

## 8. Reproducible run

Prepare UTF-8 JSON and run:

```bash
python scripts/speg_calculator.py analysis.json
```

The calculator returns the ratio diagnostic, stand-alone scenario values, and an optional weighted value. Preserve the input JSON, output JSON, calculator version, price timestamp, and review date with the report.

Do not hand-edit calculator output. If an assumption changes, update the input and rerun.

`examples/synthetic-input.json` and `examples/synthetic-output.json` provide a no-live-data smoke test. Regenerate the output after any calculator change and compare it before packaging.

---
name: convergence-signal-read
description: Pull and evaluate convergence signals for the AI Infrastructure Component Thesis v2 framework. Trigger when the user asks for a "convergence read", "signal check", "convergence signals", "credit signal", "private credit check", "BDC check", "capex check", "cloud growth check", "energy signal", "IPO signal check", "demand broadening check", or asks how close the exit ladder is to firing. Returns structured per-signal readings, breach status, and exit ladder guidance per the v2 framework, including the v1.3 rates / discount-rate regime category.
---

# Convergence Signal Read

This skill operationalizes the AI Infrastructure Component Thesis v2 convergence-exit framework. When Mike asks for a signal check, Claude executes the procedures in this file to pull fresh data, compare against v2's thresholds, and return a structured read.

The skill is the doctrine. Follow it precisely. Don't substitute your own judgment about what counts as a breach — use the thresholds defined here. Add commentary alongside the data, but never replace the data with commentary.

## When to invoke this skill

Trigger phrases (case-insensitive):
- "run the convergence read", "convergence read", "signal read"
- "check signals", "check convergence", "convergence check"
- "[category] signal", e.g. "credit signal", "capex signal", "energy signal", "cloud growth signal", "IPO signal", "demand broadening signal"
- "how close are we to convergence"
- "is the exit ladder firing"
- "full read", "morning read" (in the context of portfolio signals)

For a category-specific request (e.g. "credit signal only"), run only that section. For an unqualified request, run all seven categories.

## Default output structure

Always return results in this format:

```
## Convergence Read — [date]

### [Category 1]
| Signal | Current | Threshold | Breach | Direction |
|---|---|---|---|---|
| ... | ... | ... | Yes/No | ↑/↓/→ |

Commentary: [1-3 sentences on what the readings imply through v2's lens]

### [Category 2]
...

### Aggregate
- Categories with breaches: N of 6 tally-eligible categories (out of 7 total categories)
- Convergence trigger fires at: 2+ categories with at least one tally-eligible breach in the trailing 14 days
- Status: [Quiet | Watch | Warning | Convergence Firing]
- Exit ladder action: [None | Pre-position cash buffer | Begin Layer 1 trim | Full exit ladder per v2]
```

Status definitions:
- **Quiet**: 0 categories breached
- **Watch**: 1 category breached
- **Warning**: 2 categories breached, but breaches are weak (just over threshold)
- **Convergence Firing**: 2+ tally-eligible categories with at least one breach, or any single severe breach (>50% past threshold)

Exit ladder mapping per v2:
- Quiet → no action
- Watch → no action, note which category for monitoring
- Warning → pre-position: build cash buffer toward 30-40%
- Convergence Firing → execute v2 exit ladder in order: (1) DRAM/MU first, (2) ALAB/COHR, (3) NVDA/AVGO, (4) TSM/ADI, (5) VRT/TLN/CEG last

## Signal Category 1: Credit

**Source**: Web search (primary). The FRED API has been unreliable in practice — direct API/CSV fetches are frequently blocked and require a key. Do NOT default to the FRED API. Use web search for the current values instead. The FRED series IDs below are retained as reference/search terms, not as an API instruction.

**Method**: web search for the current readings. Do not attempt `api.stlouisfed.org` or `fredgraph.csv` fetches as the first move — they fail. If a web search surfaces a fetchable FRED series *page* (e.g. `fred.stlouisfed.org/series/BAMLH0A0HYM2`), that page can be fetched for the recent value table, but lead with search.

**Signals to pull**:

**Two tiers**: liquid-market signals (1a) are daily-marked and gate the exit ladder directly. Private-credit signals (1b) are quarterly, manager-marked, and lag by construction — they are an **amber early-warning channel, not a hard breach gate** (see "Private-credit handling" below). Never let a 1b reading alone trip Convergence Firing.

**1a — Liquid-market credit signals** (hard breach, daily-marked):

| Signal | FRED series | Threshold | Logic |
|---|---|---|---|
| IG-HY spread 2-week delta | BAMLH0A0HYM2 minus BAMLC0A0CM | +50 bps over 14 days | Breach if 2-week increase > 50 bps |
| Credit card 90+ DPD (NY Fed account-based) | NY Fed Quarterly Report on Household Debt and Credit, credit-card balances 90+ days delinquent by account | >14.0% | Breach if latest NY Fed account-based reading > 14.0% |
| DRCCLACBS commercial-bank sentinel | DRCCLACBS | Display-only sentinel @4.5% | Do not use as delinquency breach gate; display only, flag if >4.5% |
| HY OAS single-day spike | BAMLH0A0HYM2 | +100 bps in one day | Breach if any single-day move > 100 bps in trailing 14 days |

**1b — Private-credit / BDC signals** (amber early-warning, quarterly-marked):

| Signal | Source | Amber threshold | Logic |
|---|---|---|---|
| BDC aggregate unrealised losses as % of NAV | SEC 10-Q filings / Reuters-style BDC aggregates | >3.0% sustained, OR sharp QoQ acceleration (>0.75pp) | Amber flag; baseline Q1 2026 = 2.35% (worst since Q2 2022) |
| PIK interest as % of total interest income (trend) | BDC filings | Rising QoQ for 2+ consecutive quarters | Amber — deteriorating cash quality of earnings |
| Non-traded BDC redemption gating | Web search / news | Any new gate or redemption restriction | Amber — forced-seller / liquidity-event risk |

**Baseline (refreshed 2026-06-12 from Reuters analysis of 51 BDCs):** aggregate unrealised losses 2.35% of NAV (steepest since Q2 2022); PIK income ~$477M (+2% QoQ, below early-2025 peak ~$633M); named stress: Investcorp Credit Mgmt BDC 16.8% of NAV, FS KKR 6.7%, Blue Owl Tech Finance 6.5%. Earlier-2026 redemption gates at BlackRock / Morgan Stanley / Cliffwater non-traded vehicles. Cited driver includes AI-related pressure on software valuations straining 2021-vintage LBOs.

**Procedure**:
1. Web search for the current HY OAS: query "ICE BofA US High Yield OAS today" or "BAMLH0A0HYM2 current value". The reading is a percentage (e.g. 2.82%).
2. Web search for the current IG OAS: query "ICE BofA US Corporate OAS today" or "BAMLC0A0CM current value".
3. Web search for the latest value ~14 days prior if the search results include a recent history/chart table; otherwise run a second search like "high yield spread 2 weeks ago" or pull a recent chart page. Compute the IG-HY spread (HY − IG) and the 14-day delta.
4. From the history shown in results, estimate the largest single-day HY OAS move in the trailing 14 days (these rarely exceed a few bps absent a shock; only flag if a search surfaces a clear spike).
5. Web search for credit-card delinquency: "NY Fed Quarterly Report household debt credit card 90 days delinquent account based latest". Use the NY Fed account-based 90+ DPD reading for the hard gate. Also pull "DRCCLACBS latest" only as a display-only commercial-bank sentinel; flag the sentinel if it is above 4.5%, but do not count it as a breach gate.
6. Compare each to the 1a thresholds, populate the table.
7. Direction arrow: from the search results' recent trend (↑ rising, ↓ falling, → flat within ±5%).
8. If web search returns stale or conflicting numbers, note the as-of date in the row and flag it — do not present a stale reading as current.
9. **For 1b (private credit)**: this updates quarterly, not per-read. On a routine read between quarters, carry forward the last baseline and note "no new BDC data since [date]". On/after a quarter-end filing window (mid-Feb, mid-May, mid-Aug, mid-Nov), web search "BDC unrealised losses NAV [quarter]", "private credit PIK interest [quarter]", and "BDC redemption gate [month year]" to refresh. Compare to the prior baseline and update the direction.

**Private-credit handling (critical)**:
- 1b signals are **amber-class**. An amber flag does NOT count toward the "categories breached" tally that drives Convergence Firing. It is logged as a monitoring flag within Credit.
- The migration tell — the moment private-credit stress becomes a *hard* signal — is when it shows up in the **liquid** market, i.e. when signal 1a (HY OAS / IG-HY spread) begins to widen. Watch for 1b-amber + 1a-rising occurring together; that combination is the genuine warning and should be called out explicitly.
- Rationale: private credit is manager-marked quarterly and lags. It is the best early-warning channel for a financing/liquidity shock (the primary non-demand risk to the AI-infra thesis), but its quarterly cadence and smoothed marks make it unsuitable as a hard exit-ladder trigger on its own.

**Note on delinquency units and source**: The hard delinquency gate is the NY Fed account-based credit-card 90+ DPD series. DRCCLACBS reports system-wide commercial-bank delinquency and is demoted to a display-only sentinel at 4.5%; do not substitute it for the NY Fed hard gate. When quoting spread changes, report basis points (bps). If the source gives percentage-point changes, convert pp to bps by multiplying by 100 (0.50pp = 50 bps).

**Commentary template**: "Credit markets are [tight/normal/loose]. [Spread direction]. [Any flag if a single 1a signal is close to threshold even if not breached.] Private credit (1b): [amber/clear] — [BDC NAV-loss reading vs. baseline, PIK trend, any new gates]. [If 1b amber AND 1a rising, call out the migration explicitly.]"

## Signal Category 2: Capex (Hyperscaler)

**Source**: SEC EDGAR (https://data.sec.gov/submissions/CIK{cik}.json) for filings list, then fetch the 8-K or press release content

**Companies to monitor**:
- Microsoft (MSFT): CIK 0000789019
- Meta (META): CIK 0001326801
- Alphabet (GOOGL): CIK 0001652044
- Amazon (AMZN): CIK 0001018724
- Oracle (ORCL): CIK 0001341439 (Oracle has elevated AI-infra exposure)

**Signals to evaluate**:

| Signal | Threshold | Logic |
|---|---|---|
| 2026 capex guidance trim at any hyperscaler | Any negative revision | Breach |
| 2027 forward guidance below 2026 levels | Any guidance below 2026 print | Breach |
| Capex/revenue ratio expansion (not compression) | Q-over-Q ratio rising at any name | Breach |

**Procedure**:
1. For each hyperscaler, fetch the latest 8-K or quarterly earnings release dated within the last 90 days
2. EDGAR endpoint: `https://data.sec.gov/submissions/CIK{padded_cik}.json` returns recent filings
3. Look for the 8-K filed nearest the most recent earnings date
4. Pull the press release attachment (typically EX-99.1)
5. Extract: stated capex for the just-reported quarter, forward guidance for the current fiscal year, any forward statements about the next fiscal year
6. Compare to the prior quarter's filing for direction
7. For Oracle specifically, note any RPO/backlog changes and capacity commentary

**Important**: Earnings dates matter. Q1 2026 earnings cycle for hyperscalers was Apr-May 2026. Q2 2026 earnings cycle will be late July 2026 — that's when v2 flags as a key window. If we're between cycles, note when the next earnings date is and what would trigger a breach.

**Commentary template**: "Hyperscaler capex posture remains [expansionary/stable/compressing]. [Specific names with notable changes]. [Days until next reporting cycle]."

## Signal Category 3: Cloud Growth

**Source**: Same filings as Capex (the segment growth rates are disclosed in the same press releases)

**Signals to evaluate**:

| Signal | Threshold | Logic |
|---|---|---|
| AWS YoY revenue growth | <20% | Breach |
| Azure YoY revenue growth | <28% | Breach (Azure typically reports a constant-currency number; use that one) |
| GCP YoY revenue growth | <30% | Breach |
| Concentration deceleration | Single provider dropping >5pp faster than sector avg | Breach |

**Procedure**:
1. From the same hyperscaler filings pulled in Capex, extract segment growth rates:
   - AMZN press release → AWS net sales YoY %
   - MSFT press release → "Intelligent Cloud" or specifically Azure growth (often quoted in the earnings call commentary as a separate number)
   - GOOGL press release → Google Cloud revenue YoY %
2. Compare to thresholds
3. Compute average growth across the three; flag any single provider whose deceleration is >5pp below the average
4. Pull backlog/RPO figures if disclosed (AWS $244B as of recent print, Azure $80B+, Oracle $523B per v2 baseline)

**Commentary template**: "Cloud growth posture: [strong/decelerating/inflecting]. [Name-by-name 1-line read]. [Backlog trend if material]."

## Signal Category 4: Energy

**Source**: EIA API (https://api.eia.gov/v2/) for wholesale hub prices; compare all-in delivered power cost against hub LMP when evaluating AI data-center economics

**API key**: when needed, ask Mike for the EIA key.

**Signals to evaluate**:

| Signal | Threshold | Logic |
|---|---|---|
| PJM West hub sustained price | >$80/MWh for 5 trading days | Breach |
| All-in delivered power cost vs hub LMP | All-in cost materially above hub LMP for AI data-center loads | Flag; breach only if sustained premium confirms economics are impaired |
| ERCOT North hub sustained price | >$80/MWh for 5 trading days | Breach |
| CAISO (NP15 or SP15) sustained price | >$100/MWh for 5 trading days | Breach |

**Procedure**:
1. EIA wholesale electricity endpoint: `/v2/electricity/wholesale-prices/data?api_key={KEY}&frequency=daily&data[0]=price`
2. Facet by hub (PJM West, ERCOT North, NP15)
3. Pull the trailing 10 trading days
4. Count days at or above threshold
5. Separately note whether all-in delivered power cost materially exceeds the hub LMP for AI data-center loads; use hub LMP as the market reference and call out transmission, congestion, capacity, or tariff adders when available
6. Note that EIA's wholesale data is updated bi-weekly with daily resolution — the most recent prints may be 5-10 days old
7. If EIA returns nothing useful, fall back to web search for "PJM West hub LMP [date]" or similar

**Commentary template**: "Power prices [calm/tight/breaking]. [Note if grid stress narrative is in news]. [Note any politically-sensitive utility commentary]."

## Signal Category 5: IPO Calendar

**Source**: web search

**Companies to track**: SpaceX, Anthropic, OpenAI

**Signals to evaluate**:

| Signal | Threshold | Logic |
|---|---|---|
| SpaceX IPO pricing/news | Any pricing announcement | Note (this is the calendar anchor per v2) |
| Anthropic S-1 filing | Filing event | Note |
| OpenAI IPO movement | Any pricing or filing event | Note |
| Day-one pop on any of the above | <18% pop or breaking issue = breach; [18%, 20%) = flag; ≥20% = clear | Breach/flag — regime change signal |

**Procedure**:
1. Web search: "SpaceX IPO news [current month] [current year]"
2. Web search: "Anthropic IPO S-1 filing [current month] [current year]"
3. Web search: "OpenAI IPO news [current month] [current year]"
4. Look for: filing announcements, roadshow news, pricing dates, day-one trading
5. Classify materiality: filing event, pricing event, trading event, or noise
6. For any trading event, fetch the day-one price action and compute pop vs issue price. Classify <18% pop or a broken issue as a breach, [18%,20%) as a marginal flag, and ≥20% as clear.

**Commentary template**: "IPO calendar: [quiet/active]. [Specific events with dates]. [If any IPO has priced, note pop size and v2 implication: clear ≥20%, marginal flag [18%,20%), breach <18% or broken issue]."

## Signal Category 6: Demand-Broadening (positive signals — extend the cycle)

**Source**: NVDA, AVGO, VRT earnings transcripts via SEC EDGAR

**Signals to evaluate** (these are anti-convergence signals; presence is bullish for cycle duration):

| Signal | Logic |
|---|---|
| NVDA sovereign AI revenue YoY | Tripling YoY = strong; flat or decelerating = caution |
| AVGO XPU customer roster | Expanding beyond 6 named = strong; concentration increasing = caution |
| Enterprise direct deployments (Lilly-class) | Scaling to multi-billion quarters = strong |
| New customer cohorts (defense, energy, healthcare) | Emergence = strong |
| VRT customer mix | Hyperscalers becoming smaller share = strong |

**Procedure**:
1. Pull NVDA most recent earnings release from EDGAR (CIK 0001045810)
2. Pull AVGO (CIK 0001730168)
3. Pull VRT (CIK 0001674101)
4. Extract any commentary on sovereign revenue, customer mix, new cohorts
5. Compare to v2's baseline: NVDA sovereign was $30B+ in FY26 tripling YoY; AVGO had 6 named XPU customers
6. Note direction of travel

**Commentary template**: "Demand-broadening: [accelerating/stable/decelerating]. [Specific data points]. [Net impact on v2 convergence timing — extends, holds, or compresses the window]."

## Signal Category 7: Rates / Discount-Rate Regime

**Source**: Federal Reserve communications, Treasury yield curve data, SOFR/futures-implied policy path, and web search for current Fed leadership / FOMC regime news.

**Tally eligibility**: Category 7 is tally-eligible. A breach counts toward the aggregate categories-with-breaches total.

**Signals to evaluate**:

| Signal | Threshold | Logic |
|---|---|---|
| Fed/FOMC regime shift | Explicitly hawkish discount-rate regime change, including Warsh FOMC leadership/news as of 2026-06-17 | Breach |
| 10-year Treasury 14-day delta | +50 bps over 14 days | Breach if the 10-year yield rises by >50 bps over 14 days |
| Real-rate shock | +35 bps in 10-year real yield over 14 days | Breach if the real discount rate reprices sharply higher |
| Forward policy path repricing | Futures-implied path shifts >50 bps tighter over 14 days | Breach if expected policy rate path materially tightens |

**Units convention**: Quote rate and spread moves in **basis points (bps)**. When a source reports percentage-point moves, convert pp to bps by multiplying by 100 (0.25pp = 25 bps; 0.50pp = 50 bps).

**Procedure**:
1. Web search current Fed/FOMC leadership and policy-regime news. Treat a hawkish regime event, including the 2026-06-17 Warsh FOMC signal, as a breach.
2. Pull the current 10-year Treasury yield and the value roughly 14 days prior; compute the delta in bps.
3. Pull 10-year real yield / TIPS if available and compute the 14-day delta in bps.
4. Pull SOFR/fed-funds futures or market-implied policy-path commentary; compute or summarize the 14-day repricing in bps.
5. Mark stale or inferred data explicitly. Do not fill a missing rate path with guesswork.

**Commentary template**: "Rates / discount-rate regime: [benign/tightening/shock]. [Specific rate-path or regime evidence]. [Implication for AI-infra long-duration multiples]."

## Aggregating to convergence status

After running all seven categories:

1. Count tally-eligible categories with at least one breach. Six of the seven categories are tally-eligible: Categories 1a, 2, 3, 4, 5 breach rows, and 7. Private-credit 1b amber flags are not hard breach gates, and Category 6 Demand-Broadening is an anti-convergence category unless it is collapsing.
2. Count severe breaches (>50% past threshold)
3. Note any demand-broadening evidence that contradicts capex/cloud breaches
4. Map to status:
   - 0 categories breached → Quiet
   - 1 category breached → Watch
   - 2 categories breached, both within 25% of threshold → Warning
   - 2+ tally-eligible categories breached, any severe, OR demand-broadening collapsing → Convergence Firing

5. Map status to v2 exit ladder action and recite the order

## How to handle missing data

- If a web search returns nothing useful, retry once with a reworded query. If still failing, note "data unavailable" in the row and continue.
- Never fabricate readings. Never substitute estimates for real values without flagging.
- If most of a category's signals are unavailable, mark the category as "unknown" not "no breach".
- Credit (Cat 1) is web-search-first; do not block on the FRED API. The EIA energy data (Cat 4) may also fall back to web search per that section.

## Output discipline

- Always include the date the read was performed
- Always show the threshold next to the reading
- Always show direction of travel, not just absolute level
- Keep commentary tight: 1-3 sentences per category
- Never editorialize beyond what v2 framework would say
- If a signal is close to threshold but not breached, flag it explicitly: "Within 10% of threshold — monitor next reading"

## What this skill does NOT do

- Does not make trade recommendations beyond v2's defined exit ladder
- Does not provide outlook commentary beyond signal-based analysis
- Does not interpret signals through any framework other than v2
- Does not skip categories without explicit user instruction
- Does not run when the user is asking general portfolio questions — only when explicit signal-check trigger phrases appear

## Update procedure

This skill encodes v2 framework signals and thresholds as of June 17, 2026. If v2 evolves (per Mike's living-document notes), update the threshold values and signal definitions in this file. Do not change the structure or output format without explicit instruction.

Framework owner: Mike Ye. Co-cognition partner: Claude.

**Changelog**:
- v1.0 (2026-05-17): Initial six-category framework.
- v1.1 (2026-05-29): Split Category 1 into 1a (liquid-market, hard breach) and 1b (private-credit/BDC, amber early-warning). Added BDC NAV-loss, PIK-trend, and redemption-gate sub-signals with Q1 2026 baseline (2.35% of NAV). 1b is amber-class and does not trip Convergence Firing alone; migration tell is 1b-amber co-occurring with 1a-widening.
- v1.2 (2026-05-29): Switched Category 1 credit data sourcing from FRED API (unreliable / key-gated / frequently blocked) to web-search-first. FRED series IDs retained as reference/search terms only.
- v1.3 (2026-06-17): Added tally-eligible Category 7 Rates / Discount-Rate Regime, including Warsh FOMC breach handling. Updated aggregation to six tally-eligible categories out of seven total categories. Added explicit bps units convention (pp → bps ×100). Resolved delinquency gate to NY Fed account-based 90+ DPD and demoted DRCCLACBS to display-only sentinel @4.5%. Refreshed private-credit baseline to 2026-06-12. Added energy all-in-cost-vs-hub-LMP rule. Added IPO day-one pop marginal band ([18%,20%) = flag; <18% or broken issue = breach).

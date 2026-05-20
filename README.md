# sPEG Framework

A scarcity-adjusted PEG framework for equity analysis. Open-source skill for Claude Code, Cowork, and the broader Claude ecosystem.

**Developed by [Mike Ye](https://exmxc.ai)** — former VP of Strategic Planning & Acquisitions at Penske Media Corporation (Rolling Stone, Billboard, SXSW, Variety, Robb Report), now operating a portfolio of AI-native ventures.

---

## What is sPEG?
sPEG = Forward P/E ÷ (Growth% × Scarcity Multiplier)

Traditional PEG (Price/Earnings to Growth) assumes commodity-like supply elasticity. It breaks down when a company's growth is bounded by a structurally scarce input the market has not yet recognized as scarce.

**sPEG** corrects this by introducing the **Scarcity Multiplier** — a five-factor score (Irreplaceability, Replication Timeline, Supply Concentration, Throughput Control, Downstream Dependency) that quantifies how much of a company's growth is gated by structural scarcity.

The result: a single ratio that exposes mispricings traditional PEG misses, particularly in AI infrastructure, semiconductors, and capacity-constrained industries.

---

## Why This Exists

In the AI infrastructure era, the most valuable companies often *look* expensive on traditional multiples (NVDA) or *look* cheap on traditional multiples (MU) — and both readings are wrong because neither incorporates the structural scarcity of the inputs they control or depend on.

sPEG was developed to surface these mispricings systematically. The MU thesis included in this repo demonstrates the framework producing a sPEG of 0.096 — well below the 0.1 threshold that signals "scarcity premium completely unpriced."

The framework is published as a Claude skill so any analyst, PM, or independent investor can apply it consistently across positions and time, with full methodology transparency.

---

## Installation

### Claude Code

```bash
claude plugin marketplace add Trailgenic/sPEG-framework
claude plugin install spec-calculation@sPEG-framework
```

### Cowork

In Cowork, open **Settings → Plugins → Add plugin** and paste:
https://github.com/Trailgenic/sPEG-framework

### Manual

Drop the `skill/spec-calculation/` directory into your skills folder (`~/.claude/skills/` or your user skills directory).

---

## Usage

Once installed, the skill fires automatically when you mention sPEG, scarcity scoring, or ask Claude to evaluate a position for structural mispricing. You can also invoke it explicitly:
"Run a sPEG analysis on TSMC"
"Score Micron with the Scarcity Multiplier framework"
"Is ASML mispriced under sPEG?"

Claude will produce a structured analysis following the canonical template (see `skill/spec-calculation/SKILL.md` for the full output format).

---

## The Framework

### The Five Scarcity Factors

Each scored 1-5, summed and divided by 5 to produce a Scarcity Multiplier (range 1.0-5.0):

1. **Irreplaceability** — Can the company's product be substituted within 3 years?
2. **Replication Timeline** — How long for a competitor to credibly replicate?
3. **Supply Concentration** — Market structure on the supply side?
4. **Throughput Control** — Contract regime, fulfillment rates, capex lead times
5. **Downstream Dependency** — How critical is this input to downstream value creation?

### sPEG Thresholds

| sPEG | Signal |
|------|--------|
| <0.1 | Scarcity premium completely unpriced |
| 0.1-0.3 | High-conviction long |
| 0.3-0.7 | Long signal |
| 0.7-1.0 | Neutral to long |
| 1.0-1.5 | Neutral to short |
| >1.5 | Short signal |

Full methodology: [`skill/spec-calculation/SKILL.md`](skill/spec-calculation/SKILL.md)

---

## Worked Example: MU (Micron)

A full canonical analysis is included at [`skill/spec-calculation/examples/MU-analysis.md`](skill/spec-calculation/examples/MU-analysis.md).

Key result: MU sPEG = 0.096, driven by a Scarcity Multiplier of 4.6 on its HBM exposure. The thesis is structured with falsifier hierarchies, scenario-weighted targets, and explicit downgrade triggers per scarcity factor.

This is a real position with full transparency — published as a worked example, not as investment advice.

---

## Disclaimer

This framework is published for analytical use. It does **not** constitute investment, legal, tax, or accounting advice. The MU example reflects the author's personal analysis on a personal position and should not be interpreted as a recommendation. All outputs require independent verification by qualified financial professionals before being used in decision-making.

---

## License

[Apache License 2.0](LICENSE) — free for commercial and personal use; attribution to Mike Ye (exmxc.ai) requested but not required.

---

## Citation

If you use the sPEG framework in published work:

> Ye, Mike. "sPEG: Scarcity-Adjusted PEG Framework for Equity Analysis." exmxc.ai, 2026. https://github.com/Trailgenic/sPEG-framework

---

## Contributing

Framework refinements and additional worked examples welcome via pull request. The core methodology (five factors, 1-5 scale, sPEG formula) is locked at v1.0 — major framework evolution will be versioned as v2.0 with explicit migration notes.

For substantive framework dialogue, contact via [exmxc.ai](https://exmxc.ai).

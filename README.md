# sPEG Framework

A scarcity-adjusted PEG framework for equity analysis, published as an open-source skill. Current version: **v1.7**.

**Developed by [Mike Ye](https://www.exmxc.ai/about-us/mike-ye)**, an M&A and corporate development executive and the founder of [exmxc](https://www.exmxc.ai), the research institution building information assets on the AI economy through AI Lattice and Strategic Signal.

---

## What is sPEG?

```text
sPEG = (current price / NTM diluted EPS) / (normalized 3-year EPS CAGR% x Scarcity Multiplier)
Scarcity Multiplier = (F1 + F2 + F3 + F4 + F5) / 5
```

Traditional PEG assumes commodity-like supply. It breaks down when a company's growth is bounded by a structurally scarce input. sPEG adds a **Scarcity Multiplier**, a five-factor score for one identified scarce asset:

1. **Irreplaceability:** can the asset be substituted?
2. **Replication time:** how long would a credible replica take?
3. **Supply concentration:** how many viable suppliers are there?
4. **Throughput tightness and rent capture:** is supply tight now, and does the holder keep the economics?
5. **Demand durability:** how long does demand for the asset persist?

Each factor is scored 1 to 5 against the rubric in [`references/scoring-rubric.md`](skill/spec-calculation/skills/spec-calculation/references/scoring-rubric.md).

**sPEG is a diagnostic, not a price target.** The factor scores are ordinal evidence. Fair value comes from explicit downside, base and upside cash-flow scenarios, calculated by the included deterministic calculator. The resulting tiers describe the distance between price and modeled value only. They are not buy or sell signals.

## Two modes

- **Mode A: sPEG valuation.** The five-factor Scarcity Multiplier, the headline sPEG, and scenario fair value.
- **Mode B: sPEG Index assessment.** The Scarcity Durability method used by the [exmxc sPEG Index](https://www.exmxc.ai/speg-index) since September 2026. It makes five anchored judgments (Constraint, Substitution resistance, Economic capture, Persistence, Cost of defense) and applies independent admission gates. The Scarcity Durability Score is never used as a multiplier. Method: [sPEG Index methodology](https://www.exmxc.ai/speg-index/methodology).

The two modes are never mixed.

---

## Contents

```text
skill/spec-calculation/skills/spec-calculation/
  SKILL.md                      workflow, invariants, validity gates, both modes
  references/scoring-rubric.md  F1-F5 anchors and cross-checks
  references/methodology.md     sPEG and scenario valuation
  references/output-template.md report structure
  references/v1.6-migration.md  what changed from earlier versions
  scripts/speg_calculator.py    deterministic arithmetic
  scripts/test_speg_calculator.py
  examples/synthetic-input.json, synthetic-output.json
```

Run the calculator and its tests:

```bash
cd skill/spec-calculation/skills/spec-calculation
python scripts/speg_calculator.py examples/synthetic-input.json
python -m pytest scripts/test_speg_calculator.py
```

The example uses synthetic inputs. It is not an analysis of any real company.

---

## Installation

The skill uses the open Agent Skills format (a `SKILL.md` with reference files and scripts).

As a plugin marketplace:

```bash
claude plugin marketplace add Trailgenic/sPEG-framework
claude plugin install spec-calculation@sPEG-framework
```

Manually: copy `skill/spec-calculation/skills/spec-calculation/` into your skills folder.

Example requests: "Run a sPEG analysis on TSMC", "Score Micron's HBM exposure with the Scarcity Multiplier", "Does Synopsys pass the sPEG Index admission gates?"

---

## Versions

- **v1.7 (2026-11-16):** added Mode B, the sPEG Index Scarcity Durability assessment. Mode A is unchanged from v1.6.
- **v1.6:** breaking change. Fair value now comes from cash-flow scenarios, with no score-to-price multiplier. Valuation tiers no longer use action language. See [`v1.6-migration.md`](skill/spec-calculation/skills/spec-calculation/references/v1.6-migration.md).
- **v1.2:** replaced Downstream Dependency with Demand Durability as the fifth factor.
- **v1.0:** initial five-factor framework.

Scores computed under different versions are not comparable without re-scoring.

---

## Disclaimer

This framework is published for analytical use. It is not investment, legal, tax or accounting advice. sPEG has not been validated on realized returns. All outputs require independent verification before they are used in any decision.

## License

[Apache License 2.0](LICENSE). Attribution to Mike Ye (exmxc.ai) is requested but not required.

## Citation

> Ye, Mike. "sPEG: Scarcity-Adjusted PEG Framework for Equity Analysis." exmxc.ai, 2026. https://github.com/Trailgenic/sPEG-framework

## References

- [sPEG (Scarcity-Adjusted PEG)](https://www.exmxc.ai/lexicon/speg-scarcity-adjusted-peg): definition
- [sPEG Index](https://www.exmxc.ai/speg-index) and [methodology](https://www.exmxc.ai/speg-index/methodology)
- [sPEG Doctrine](https://www.exmxc.ai/leadership-doctrine/scarcity-adjusted-peg-speg-doctrine)
- [Four Forces of AI Power](https://www.exmxc.ai/lexicon/four-forces-of-ai-power): the broader framework sPEG applies

## Contributing

Refinements and additional examples are welcome by pull request. Breaking methodology changes are versioned with migration notes.

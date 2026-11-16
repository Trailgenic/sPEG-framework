#!/usr/bin/env python3
"""Regression and invariant tests for the sPEG v1.6 calculator."""

from __future__ import annotations

import copy
import unittest

from speg_calculator import InputError, calculate, compute_speg, tier, value_scenario


def base_ratio() -> dict:
    return {
        "price": 100.0,
        "ntm_eps": 5.0,
        "fy3_eps": 8.64,
        "normalized_growth_pct": 20.0,
        "factors": [4, 4, 4, 4, 4],
    }


def base_scenario() -> dict:
    return {
        "name": "base",
        "eps_base": 5.0,
        "growth_pct": 20.0,
        "duration_score": 4.0,
        "cash_conversion_start": 0.8,
        "cash_conversion_terminal": 0.9,
        "terminal_growth_pct": 3.0,
        "required_return_pct": 10.0,
    }


class RatioTests(unittest.TestCase):
    def test_headline_uses_ntm_eps(self) -> None:
        result = compute_speg(base_ratio())
        self.assertAlmostEqual(result["forward_pe_ntm"], 20.0)
        self.assertAlmostEqual(result["raw_cagr_pct"], 20.0, places=6)
        self.assertAlmostEqual(result["scarcity_multiplier"], 4.0)
        self.assertAlmostEqual(result["speg"], 0.25)

    def test_growth_cap(self) -> None:
        payload = base_ratio()
        payload["normalized_growth_pct"] = 80.0
        result = compute_speg(payload)
        self.assertEqual(result["scoring_growth_pct"], 50.0)
        self.assertTrue(result["growth_cap_applied"])

    def test_validity_gates(self) -> None:
        for field in ("ntm_eps", "normalized_growth_pct"):
            payload = base_ratio()
            payload[field] = 0
            with self.assertRaises(InputError):
                compute_speg(payload)

    def test_low_sm_is_diagnostic_only(self) -> None:
        payload = base_ratio()
        payload["factors"] = [2, 2, 2, 2, 2]
        self.assertEqual(compute_speg(payload)["interpretation_domain"], "diagnostic-only-sm-below-3")


class ValuationInvariantTests(unittest.TestCase):
    def value(self, **changes: float) -> float:
        scenario = base_scenario()
        scenario.update(changes)
        return value_scenario(scenario, 100.0)["fair_value_per_share"]

    def test_growth_is_monotonic(self) -> None:
        self.assertLess(self.value(growth_pct=15.0), self.value(growth_pct=20.0))

    def test_duration_is_monotonic(self) -> None:
        self.assertLess(self.value(duration_score=3.0), self.value(duration_score=4.0))

    def test_conversion_is_monotonic(self) -> None:
        self.assertLess(self.value(cash_conversion_start=0.7), self.value(cash_conversion_start=0.8))

    def test_required_return_is_inverse_monotonic(self) -> None:
        self.assertLess(self.value(required_return_pct=12.0), self.value(required_return_pct=10.0))

    def test_monotonicity_parameter_sweep(self) -> None:
        for growth in (5.0, 10.0, 25.0, 50.0, 80.0):
            self.assertLess(
                self.value(growth_pct=growth, duration_score=2.0),
                self.value(growth_pct=growth, duration_score=4.0),
            )
        for duration in (1.0, 2.5, 4.0, 5.0):
            self.assertLess(
                self.value(growth_pct=10.0, duration_score=duration),
                self.value(growth_pct=20.0, duration_score=duration),
            )
        for required_return in (7.0, 9.0, 12.0, 18.0):
            self.assertLess(
                self.value(required_return_pct=required_return, cash_conversion_start=0.5),
                self.value(required_return_pct=required_return, cash_conversion_start=0.9),
            )
        for growth in (5.0, 20.0, 60.0):
            self.assertLess(
                self.value(growth_pct=growth, required_return_pct=14.0),
                self.value(growth_pct=growth, required_return_pct=10.0),
            )

    def test_f4_alone_cannot_raise_value(self) -> None:
        low_f4 = base_ratio()
        high_f4 = base_ratio()
        low_f4["factors"][3] = 2
        high_f4["factors"][3] = 5
        low_f4["scenarios"] = [base_scenario()]
        high_f4["scenarios"] = [base_scenario()]
        low_value = calculate(low_f4)["scenarios"][0]["fair_value_per_share"]
        high_value = calculate(high_f4)["scenarios"][0]["fair_value_per_share"]
        self.assertEqual(low_value, high_value)

    def test_explicit_path(self) -> None:
        scenario = {
            "name": "cyclical",
            "eps_path": [5.0, 4.0, 3.0],
            "cash_conversion_path": [0.8, 0.75, 0.7],
            "cash_conversion_terminal": 0.8,
            "terminal_growth_pct": 2.0,
            "required_return_pct": 12.0,
        }
        lower = value_scenario(scenario, 100.0)["fair_value_per_share"]
        stronger = copy.deepcopy(scenario)
        stronger["eps_path"][-1] = 4.0
        higher = value_scenario(stronger, 100.0)["fair_value_per_share"]
        self.assertLess(lower, higher)

    def test_excess_cash_requires_interest_bridge(self) -> None:
        scenario = base_scenario()
        scenario["excess_cash_per_share"] = 10.0
        with self.assertRaises(InputError):
            value_scenario(scenario, 100.0)
        scenario["eps_excludes_net_interest"] = True
        self.assertAlmostEqual(
            value_scenario(scenario, 100.0)["fair_value_per_share"], self.value() + 10.0
        )

    def test_invalid_discount_inputs_fail(self) -> None:
        for changes in (
            {"required_return_pct": 0.0},
            {"required_return_pct": 3.0, "terminal_growth_pct": 3.0},
            {"terminal_growth_pct": -100.0},
            {"growth_pct": 2.0, "terminal_growth_pct": 3.0},
        ):
            scenario = base_scenario()
            scenario.update(changes)
            with self.assertRaises(InputError):
                value_scenario(scenario, 100.0)


class AggregationTests(unittest.TestCase):
    def test_weighted_value(self) -> None:
        payload = base_ratio()
        first = base_scenario()
        second = base_scenario()
        first.update({"name": "one", "weight": 0.25})
        second.update({"name": "two", "growth_pct": 10.0, "weight": 0.75})
        payload["scenarios"] = [first, second]
        result = calculate(payload)
        expected = sum(s["fair_value_per_share"] * s["weight"] for s in result["scenarios"])
        self.assertAlmostEqual(result["weighted"]["fair_value_per_share"], expected)

    def test_partial_weights_fail(self) -> None:
        payload = base_ratio()
        first = base_scenario()
        second = base_scenario()
        first.update({"name": "one", "weight": 1.0})
        second.update({"name": "two"})
        payload["scenarios"] = [first, second]
        with self.assertRaises(InputError):
            calculate(payload)

    def test_tier_boundaries_do_not_overlap(self) -> None:
        self.assertEqual(tier(0.50), "undervaluation")
        self.assertEqual(tier(0.20), "fair-value-range")
        self.assertEqual(tier(-0.10), "fair-value-range")
        self.assertEqual(tier(-0.30), "overvaluation")
        self.assertEqual(tier(-0.300001), "material-overvaluation")


if __name__ == "__main__":
    unittest.main()

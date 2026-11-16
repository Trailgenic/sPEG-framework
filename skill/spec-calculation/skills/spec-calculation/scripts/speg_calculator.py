#!/usr/bin/env python3
"""Deterministic sPEG ratio and scenario valuation calculator (v1.6)."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


class InputError(ValueError):
    pass


def _number(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise InputError(f"{name} must be numeric")
    value = float(value)
    if not math.isfinite(value):
        raise InputError(f"{name} must be finite")
    return value


def _fraction(value: Any, name: str, *, positive: bool = False) -> float:
    value = _number(value, name)
    lower_ok = value > 0 if positive else value >= 0
    if not lower_ok or value > 1:
        bound = "(0, 1]" if positive else "[0, 1]"
        raise InputError(f"{name} must be in {bound}")
    return value


def _scores(values: Any) -> list[float]:
    if not isinstance(values, list) or len(values) != 5:
        raise InputError("factors must contain exactly five scores")
    result = [_number(value, f"factors[{i}]") for i, value in enumerate(values)]
    if any(value < 1 or value > 5 for value in result):
        raise InputError("factor scores must be between 1 and 5")
    return result


def tier(upside: float) -> str:
    if upside > 0.50:
        return "material-undervaluation"
    if upside > 0.20:
        return "undervaluation"
    if upside >= -0.10:
        return "fair-value-range"
    if upside >= -0.30:
        return "overvaluation"
    return "material-overvaluation"


def compute_speg(payload: dict[str, Any]) -> dict[str, Any]:
    price = _number(payload.get("price"), "price")
    ntm_eps = _number(payload.get("ntm_eps"), "ntm_eps")
    fy3_eps = _number(payload.get("fy3_eps"), "fy3_eps")
    factors = _scores(payload.get("factors"))
    if price <= 0:
        raise InputError("price must be positive")
    if ntm_eps <= 0:
        raise InputError("NTM EPS validity gate failed: ntm_eps must be positive")
    if fy3_eps <= 0:
        raise InputError("growth validity gate failed: fy3_eps must be positive")

    raw_growth = (fy3_eps / ntm_eps) ** (1 / 3) - 1
    normalized_growth = payload.get("normalized_growth_pct", raw_growth * 100)
    normalized_growth = _number(normalized_growth, "normalized_growth_pct")
    if normalized_growth <= 0:
        raise InputError("growth validity gate failed: normalized growth must be positive")
    scoring_growth = min(normalized_growth, 50.0)
    forward_pe = price / ntm_eps
    sm = sum(factors) / 5
    speg = forward_pe / (scoring_growth * sm)
    return {
        "forward_pe_ntm": forward_pe,
        "raw_cagr_pct": raw_growth * 100,
        "normalized_growth_pct": normalized_growth,
        "scoring_growth_pct": scoring_growth,
        "growth_cap_applied": normalized_growth > 50,
        "scarcity_multiplier": sm,
        "duration_score": (factors[1] + factors[4]) / 2,
        "speg": speg,
        "interpretation_domain": "in-domain" if sm >= 3 else "diagnostic-only-sm-below-3",
    }


def _conversion_path(start: float, terminal: float, years: int, recovery_years: int = 5) -> list[float]:
    """Recover conversion on a fixed clock so duration cannot delay recovery."""
    if recovery_years < 1:
        raise InputError("conversion recovery years must be positive")
    return [start + (terminal - start) * min(i, recovery_years) / recovery_years for i in range(years)]


def _value_explicit(s: dict[str, Any]) -> tuple[float, dict[str, Any]]:
    eps_path_raw = s.get("eps_path")
    if not isinstance(eps_path_raw, list) or not eps_path_raw:
        raise InputError("eps_path must be a non-empty list")
    eps_path = [_number(value, f"eps_path[{i}]") for i, value in enumerate(eps_path_raw)]
    if any(value < 0 for value in eps_path):
        raise InputError("eps_path cannot contain negative EPS")

    conversion_raw = s.get("cash_conversion_path", s.get("cash_conversion_start"))
    if isinstance(conversion_raw, list):
        if len(conversion_raw) != len(eps_path):
            raise InputError("cash_conversion_path must match eps_path length")
        conversions = [_fraction(value, f"cash_conversion_path[{i}]") for i, value in enumerate(conversion_raw)]
    else:
        conversion = _fraction(conversion_raw, "cash_conversion_start")
        conversions = [conversion] * len(eps_path)

    r = _number(s.get("required_return_pct"), "required_return_pct") / 100
    tg = _number(s.get("terminal_growth_pct", 3), "terminal_growth_pct") / 100
    terminal_conversion = _fraction(s.get("cash_conversion_terminal", conversions[-1]), "cash_conversion_terminal")
    if r <= 0:
        raise InputError("required return must be positive")
    if tg <= -1:
        raise InputError("terminal growth must be greater than -100%")
    if r <= tg:
        raise InputError("required return must exceed terminal growth")

    pv = sum(eps * conv / ((1 + r) ** year) for year, (eps, conv) in enumerate(zip(eps_path, conversions), start=1))
    terminal_cash = eps_path[-1] * (1 + tg) * terminal_conversion
    terminal_value = terminal_cash / (r - tg)
    pv_terminal = terminal_value / ((1 + r) ** len(eps_path))
    return pv + pv_terminal, {
        "method": "explicit-eps-path",
        "forecast_years": len(eps_path),
        "pv_forecast_cash": pv,
        "pv_terminal": pv_terminal,
    }


def _fade_value_integer(
    eps_base: float,
    growth: float,
    duration_score: int,
    required_return: float,
    terminal_growth: float,
    conversion_start: float,
    conversion_terminal: float,
) -> tuple[float, dict[str, Any]]:
    persistence_years = duration_score + 1
    eps_values = [eps_base]
    for year in range(2, persistence_years + 1):
        applied_growth = growth if year <= 3 else min(growth, 0.25)
        eps_values.append(eps_values[-1] * (1 + applied_growth))

    fade_start = growth if persistence_years < 3 else min(growth, 0.25)
    for fade_year in range(1, 6):
        fade_growth = fade_start + (terminal_growth - fade_start) * fade_year / 5
        eps_values.append(eps_values[-1] * (1 + fade_growth))

    conversions = _conversion_path(conversion_start, conversion_terminal, len(eps_values))
    pv = sum(eps * conv / ((1 + required_return) ** year) for year, (eps, conv) in enumerate(zip(eps_values, conversions), start=1))
    terminal_cash = eps_values[-1] * (1 + terminal_growth) * conversion_terminal
    terminal_value = terminal_cash / (required_return - terminal_growth)
    pv_terminal = terminal_value / ((1 + required_return) ** len(eps_values))
    return pv + pv_terminal, {
        "method": "generated-fade",
        "persistence_years": persistence_years,
        "forecast_years": len(eps_values),
        "pv_forecast_cash": pv,
        "pv_terminal": pv_terminal,
    }


def _value_fade(s: dict[str, Any]) -> tuple[float, dict[str, Any]]:
    eps_base = _number(s.get("eps_base"), "eps_base")
    growth = _number(s.get("growth_pct"), "growth_pct") / 100
    duration = _number(s.get("duration_score"), "duration_score")
    required_return = _number(s.get("required_return_pct"), "required_return_pct") / 100
    terminal_growth = _number(s.get("terminal_growth_pct", 3), "terminal_growth_pct") / 100
    conversion_start = _fraction(s.get("cash_conversion_start"), "cash_conversion_start")
    conversion_terminal = _fraction(s.get("cash_conversion_terminal", 0.9), "cash_conversion_terminal")

    if eps_base <= 0:
        raise InputError("eps_base must be positive")
    if growth <= -1:
        raise InputError("growth_pct must be greater than -100")
    if duration < 1 or duration > 5:
        raise InputError("duration_score must be between 1 and 5")
    if required_return <= 0:
        raise InputError("required return must be positive")
    if terminal_growth <= -1:
        raise InputError("terminal growth must be greater than -100%")
    if required_return <= terminal_growth:
        raise InputError("required return must exceed terminal growth")
    if growth < terminal_growth:
        raise InputError("generated-fade growth must be at least terminal growth; use an explicit EPS path")

    low = math.floor(duration)
    high = math.ceil(duration)
    low_value, low_meta = _fade_value_integer(
        eps_base, growth, low, required_return, terminal_growth, conversion_start, conversion_terminal
    )
    if low == high:
        return low_value, low_meta
    high_value, high_meta = _fade_value_integer(
        eps_base, growth, high, required_return, terminal_growth, conversion_start, conversion_terminal
    )
    weight = duration - low
    return low_value * (1 - weight) + high_value * weight, {
        "method": "generated-fade-interpolated",
        "duration_low": low,
        "duration_high": high,
        "interpolation_weight": weight,
        "low_case": low_meta,
        "high_case": high_meta,
    }


def value_scenario(s: dict[str, Any], price: float) -> dict[str, Any]:
    name = s.get("name")
    if not isinstance(name, str) or not name.strip():
        raise InputError("each scenario requires a non-empty name")
    value, details = _value_explicit(s) if "eps_path" in s else _value_fade(s)

    excess_cash = _number(s.get("excess_cash_per_share", 0), "excess_cash_per_share")
    if excess_cash and s.get("eps_excludes_net_interest") is not True:
        raise InputError("excess_cash_per_share requires eps_excludes_net_interest=true")
    fair_value = value + excess_cash
    upside = fair_value / price - 1
    result = {
        "name": name,
        "operating_value_per_share": value,
        "excess_cash_per_share": excess_cash,
        "fair_value_per_share": fair_value,
        "upside": upside,
        "tier": tier(upside),
        "details": details,
    }
    if "weight" in s:
        result["weight"] = _fraction(s["weight"], "weight")
    return result


def calculate(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise InputError("input root must be an object")
    ratio = compute_speg(payload)
    scenarios_raw = payload.get("scenarios", [])
    if not isinstance(scenarios_raw, list):
        raise InputError("scenarios must be a list")
    price = _number(payload.get("price"), "price")
    scenarios = [value_scenario(s, price) for s in scenarios_raw]
    output: dict[str, Any] = {"version": "1.6.0", "ratio": ratio, "scenarios": scenarios}

    weights = [s.get("weight") for s in scenarios]
    if scenarios and any(weight is not None for weight in weights):
        if any(weight is None for weight in weights):
            raise InputError("either every scenario has a weight or none does")
        total = sum(float(weight) for weight in weights)
        if not math.isclose(total, 1.0, abs_tol=1e-9):
            raise InputError("scenario weights must sum to 1")
        weighted_value = sum(s["fair_value_per_share"] * s["weight"] for s in scenarios)
        weighted_upside = weighted_value / price - 1
        output["weighted"] = {
            "fair_value_per_share": weighted_value,
            "upside": weighted_upside,
            "tier": tier(weighted_upside),
        }
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Path to an sPEG v1.6 JSON input")
    parser.add_argument("--compact", action="store_true", help="Print compact JSON")
    args = parser.parse_args()
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        result = calculate(payload)
    except (OSError, json.JSONDecodeError, InputError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=None if args.compact else 2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

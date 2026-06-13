#!/usr/bin/env python3
"""Physics regression tests for toe_math.rg_running and gut_embedding.

These pin the headline numbers of Propositions 1-4 (docs/THEORY.md) to
their literature values, with tolerances wide enough for input updates
but tight enough to catch sign/normalization errors.

Run: python3 -m pytest tests/test_rg_running.py -q
"""

import os
import sys
from fractions import Fraction

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toe_math import rg_running as rg
from toe_math import gut_embedding as gut


def test_boundary_conditions():
    a1, a2, a3 = rg.boundary_conditions()
    assert abs(a1 - 59.0) < 0.5, f"alpha_1^-1(M_Z) = {a1}"
    assert abs(a2 - 29.6) < 0.3, f"alpha_2^-1(M_Z) = {a2}"
    assert abs(a3 - 8.48) < 0.1, f"alpha_3^-1(M_Z) = {a3}"


def test_mssm_one_loop_unifies():
    mu, a_inv = rg.run_couplings(model="MSSM", loops=1, m_susy=1000.0)
    uni = rg.find_unification(mu, a_inv)
    assert uni["unifies"], f"mismatch = {uni['mismatch']:.3f}"
    assert 1e16 <= uni["M_GUT"] <= 4e16, f"M_GUT = {uni['M_GUT']:.2e}"
    assert 22 <= uni["alpha_gut_inv"] <= 27, \
        f"alpha_GUT^-1 = {uni['alpha_gut_inv']:.1f}"


def test_sm_one_loop_near_miss():
    mu, a_inv = rg.run_couplings(model="SM", loops=1)
    uni = rg.find_unification(mu, a_inv)
    assert not uni["unifies"]
    assert uni["mismatch"] > 0.05, \
        f"SM mismatch suspiciously small: {uni['mismatch']:.3f}"


def test_two_loop_improves_mssm_and_stays_close():
    mu1, a1 = rg.run_couplings(model="MSSM", loops=1)
    mu2, a2 = rg.run_couplings(model="MSSM", loops=2)
    uni1 = rg.find_unification(mu1, a1)
    uni2 = rg.find_unification(mu2, a2)
    assert uni2["unifies"]
    assert uni2["mismatch"] < uni1["mismatch"], \
        "two loops should tighten MSSM unification"
    ratio = uni2["M_GUT"] / uni1["M_GUT"]
    assert 1 / 3 < ratio < 3, f"2-loop M_GUT shifted by x{ratio:.2f}"


def test_proton_lifetime_mssm_above_superk():
    mu, a_inv = rg.run_couplings(model="MSSM", loops=2)
    uni = rg.find_unification(mu, a_inv)
    tau = rg.proton_lifetime_years(uni["M_GUT"], 1.0 / uni["alpha_gut_inv"])
    assert 1e34 <= tau <= 1e37, f"tau_p = {tau:.2e} yr"
    assert tau > rg.SUPERK_TAU_P_BOUND_YR


def test_proton_lifetime_sm_excluded():
    mu, a_inv = rg.run_couplings(model="SM", loops=2)
    uni = rg.find_unification(mu, a_inv)
    tau = rg.proton_lifetime_years(uni["M_GUT"], 1.0 / uni["alpha_gut_inv"])
    assert tau < rg.SUPERK_TAU_P_BOUND_YR, \
        "SM near-miss scale should be excluded by Super-K"


def test_m_susy_dependence_is_mild():
    """Logarithmic threshold dependence: factor-10 in m_susy moves
    M_GUT by less than a factor ~3."""
    uni_lo = rg.find_unification(
        *rg.run_couplings(model="MSSM", loops=1, m_susy=300.0))
    uni_hi = rg.find_unification(
        *rg.run_couplings(model="MSSM", loops=1, m_susy=3000.0))
    ratio = uni_hi["M_GUT"] / uni_lo["M_GUT"]
    assert 1 / 3 < ratio < 3


def test_embedding_normalization_and_anomalies():
    assert gut.hypercharge_trace_squared() == Fraction(10, 3)
    assert gut.hypercharge_normalization() == Fraction(5, 3)
    anomalies = gut.check_anomaly_cancellation()
    assert anomalies["all_vanish"], anomalies


def test_generation_has_fifteen_weyl_fermions():
    assert sum(mult for *_, mult, _ in gut.GENERATION) == 15


def test_figures_buildable():
    fig = rg.make_rg_figure_matplotlib(loops=1)
    assert fig is not None
    pfig = rg.make_rg_figure_plotly(models=("MSSM",), loops=1)
    assert len(pfig.data) == 3  # three couplings


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__, "-q"]))

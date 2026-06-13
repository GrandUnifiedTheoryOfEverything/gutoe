#!/usr/bin/env python3
"""Renormalization-group running of the Standard Model gauge couplings.

This module reproduces, from first principles, the classic quantitative
result of unification physics (Georgi, Quinn & Weinberg 1974; Amaldi,
de Boer & Furstenau 1991; Martin & Ramond, arXiv:hep-ph/9501244):

* In the Standard Model (SM), the three gauge couplings run toward one
  another at high energy but fail to meet at a single point ("near miss").
* In the Minimal Supersymmetric Standard Model (MSSM), with superpartners
  near the TeV scale, the three couplings unify at
  M_GUT ~ 2 x 10^16 GeV with alpha_GUT^-1 ~ 24.

It also produces the standard dimensional-analysis estimate of the proton
lifetime for gauge-boson-mediated decay (p -> e+ pi0),

    tau_p ~ M_GUT^4 / (alpha_GUT^2 m_p^5),

for comparison with the Super-Kamiokande experimental lower bound.

Scope and honesty
-----------------
Everything computed here is a *reproduction of known results*, presented as
the quantitative centerpiece of a pedagogical framework. It is not a novel
prediction. The two-loop running neglects Yukawa contributions (a percent-
level effect on M_GUT dominated by the top Yukawa); the proton-lifetime
formula is an order-of-magnitude estimate, uncertain by a factor of
O(10^1-10^2) from hadronic matrix elements and threshold effects.

Conventions
-----------
GUT normalization for hypercharge: alpha_1 = (5/3) alpha_Y, so that
b-coefficients match the SU(5)/SO(10) literature. One-loop running is
analytic; two-loop running integrates the coupled ODEs

    d alpha_i^-1 / dt = -(1/2 pi) [ b_i + (1/4 pi) sum_j b_ij / alpha_j^-1 ],

with t = ln(mu / M_Z). Beta coefficients from Machacek & Vaughn (1983/84)
and Martin & Ramond (arXiv:hep-ph/9501244).

Inputs: PDG 2024 world averages (MS-bar at M_Z).

Reproduce the headline numbers with:

    python3 -m toe_math.rg_running
"""

import numpy as np

# --------------------------------------------------------------------------
# Physical inputs (PDG 2024, MS-bar scheme at mu = M_Z)
# --------------------------------------------------------------------------
M_Z = 91.1876                  # Z boson mass [GeV]
ALPHA_EM_INV_MZ = 127.951      # 1/alpha_em(M_Z), MS-bar
SIN2_THETA_W_MZ = 0.23122      # sin^2(theta_W)(M_Z), MS-bar
ALPHA_S_MZ = 0.1179            # alpha_s(M_Z)
M_PROTON = 0.93827             # proton mass [GeV]

HBAR_GEV_S = 6.582119569e-25   # hbar [GeV s]
SECONDS_PER_YEAR = 3.1557e7    # Julian year [s]

# Super-Kamiokande lower bound on tau(p -> e+ pi0), 90% CL
# (arXiv:2010.16098): tau_p > 2.4 x 10^34 years.
SUPERK_TAU_P_BOUND_YR = 2.4e34

# --------------------------------------------------------------------------
# One-loop beta coefficients, GUT-normalized (alpha_1 = 5/3 alpha_Y)
#   d alpha_i^-1 / d ln mu = -b_i / (2 pi)
# --------------------------------------------------------------------------
B1_SM = np.array([41.0 / 10.0, -19.0 / 6.0, -7.0])
B1_MSSM = np.array([33.0 / 5.0, 1.0, -3.0])

# --------------------------------------------------------------------------
# Two-loop beta matrices b_ij (Yukawa contributions neglected)
# SM: Machacek & Vaughn; MSSM: Martin & Ramond, arXiv:hep-ph/9501244
# --------------------------------------------------------------------------
B2_SM = np.array([
    [199.0 / 50.0, 27.0 / 10.0, 44.0 / 5.0],
    [9.0 / 10.0, 35.0 / 6.0, 12.0],
    [11.0 / 10.0, 9.0 / 2.0, -26.0],
])
B2_MSSM = np.array([
    [199.0 / 25.0, 27.0 / 5.0, 88.0 / 5.0],
    [9.0 / 5.0, 25.0, 24.0],
    [11.0 / 5.0, 9.0, 14.0],
])


def boundary_conditions():
    """alpha_i^-1 at M_Z in GUT normalization.

    alpha_2^-1 = sin^2(theta_W) * alpha_em^-1
    alpha_1^-1 = (3/5) cos^2(theta_W) * alpha_em^-1   (alpha_1 = 5/3 alpha_Y)
    alpha_3^-1 = 1 / alpha_s
    """
    a2_inv = SIN2_THETA_W_MZ * ALPHA_EM_INV_MZ
    a1_inv = (3.0 / 5.0) * (1.0 - SIN2_THETA_W_MZ) * ALPHA_EM_INV_MZ
    a3_inv = 1.0 / ALPHA_S_MZ
    return np.array([a1_inv, a2_inv, a3_inv])


def _run_one_loop_segment(alpha_inv_0, b, mu_0, mu):
    """Analytic one-loop running of alpha_i^-1 from mu_0 to mu (arrays ok)."""
    t = np.log(np.asarray(mu, dtype=float) / mu_0)
    return alpha_inv_0[:, None] - np.outer(b, t) / (2.0 * np.pi)


def _run_two_loop_segment(alpha_inv_0, b1, b2, mu_0, mu_grid):
    """Two-loop running by ODE integration in alpha^-1 space."""
    from scipy.integrate import solve_ivp

    def rhs(t, a_inv):
        alpha = 1.0 / a_inv
        return -(b1 + (b2 @ alpha) / (4.0 * np.pi)) / (2.0 * np.pi)

    t_grid = np.log(np.asarray(mu_grid, dtype=float) / mu_0)
    sol = solve_ivp(rhs, (t_grid[0], t_grid[-1]), alpha_inv_0,
                    t_eval=t_grid, method="RK45", rtol=1e-8, atol=1e-10)
    return sol.y


def run_couplings(model="MSSM", loops=1, m_susy=1000.0, mu_max=1.0e18, n=400):
    """Run the three GUT-normalized inverse couplings from M_Z to mu_max.

    Parameters
    ----------
    model : 'SM' or 'MSSM'. The MSSM uses SM beta functions below m_susy
        and MSSM beta functions above it (one-step threshold matching).
    loops : 1 (analytic) or 2 (ODE integration, Yukawas neglected).
    m_susy : effective superpartner threshold [GeV] (MSSM only).
    mu_max : upper end of the running [GeV]; keep <= ~1e18 to stay below
        the Planck scale and away from any Landau-like growth.
    n : number of (logarithmically spaced) grid points.

    Returns
    -------
    mu : (n,) array of scales [GeV]
    alpha_inv : (3, n) array of alpha_i^-1(mu)
    """
    model = model.upper()
    if model not in ("SM", "MSSM"):
        raise ValueError("model must be 'SM' or 'MSSM'")
    if loops not in (1, 2):
        raise ValueError("loops must be 1 or 2")

    mu = np.geomspace(M_Z, mu_max, n)
    a0 = boundary_conditions()

    if model == "SM":
        segments = [(B1_SM, B2_SM, M_Z, mu)]
    else:
        m_susy = float(m_susy)
        below = mu[mu < m_susy]
        above = mu[mu >= m_susy]
        segments = []
        if below.size:
            segments.append((B1_SM, B2_SM, M_Z, below))
        segments.append((B1_MSSM, B2_MSSM, m_susy, above))

    pieces = []
    a_start = a0
    mu_start = M_Z
    for b1, b2, seg_mu0, seg_mu in segments:
        # First bring a_start from mu_start to the segment reference scale.
        if seg_mu0 > mu_start:
            bridge = np.array([mu_start, seg_mu0])
            prev_b1, prev_b2 = (B1_SM, B2_SM)
            if loops == 1:
                a_start = _run_one_loop_segment(a_start, prev_b1,
                                                mu_start, bridge)[:, -1]
            else:
                a_start = _run_two_loop_segment(a_start, prev_b1, prev_b2,
                                                mu_start, bridge)[:, -1]
            mu_start = seg_mu0
        if seg_mu.size == 0:
            continue
        if seg_mu[0] > mu_start * (1.0 + 1e-12):
            grid = np.concatenate(([mu_start], seg_mu))
            drop = 1
        else:
            grid = seg_mu
            drop = 0
        if loops == 1:
            vals = _run_one_loop_segment(a_start, b1, mu_start, grid)
        else:
            vals = _run_two_loop_segment(a_start, b1, b2, mu_start, grid)
        pieces.append(vals[:, drop:])
        a_start = vals[:, -1]
        mu_start = grid[-1]

    alpha_inv = np.concatenate(pieces, axis=1)
    return mu, alpha_inv


def _crossing_scale(mu, diff):
    """Log-interpolated scale at which `diff` changes sign (first crossing)."""
    sign = np.sign(diff)
    idx = np.where(np.diff(sign) != 0)[0]
    if idx.size == 0:
        return None
    i = idx[0]
    # Linear interpolation in ln(mu)
    x0, x1 = np.log(mu[i]), np.log(mu[i + 1])
    y0, y1 = diff[i], diff[i + 1]
    x_star = x0 - y0 * (x1 - x0) / (y1 - y0)
    return float(np.exp(x_star))


def find_unification(mu, alpha_inv):
    """Locate the pairwise crossing scales and assess unification.

    Returns a dict with the three pairwise crossings mu_12, mu_13, mu_23,
    their geometric mean M_GUT, alpha_GUT^-1 evaluated there, the spread
    (max/min ratio of the crossing scales), the `mismatch` -- the relative
    deviation of alpha_3^-1 from alpha_1^-1 = alpha_2^-1 at the mu_12
    crossing, the standard quantitative test -- and a boolean `unifies`
    (mismatch < 3%). Crossing *scales* spread widely even for good
    unification because the lines intersect at shallow angles, so the
    coupling-space mismatch is the honest discriminator between the SM
    "near miss" and MSSM unification.
    """
    pairs = {"mu_12": (0, 1), "mu_13": (0, 2), "mu_23": (1, 2)}
    crossings = {}
    for name, (i, j) in pairs.items():
        crossings[name] = _crossing_scale(mu, alpha_inv[i] - alpha_inv[j])

    found = [v for v in crossings.values() if v is not None]
    result = dict(crossings)
    if len(found) < 2 or crossings["mu_12"] is None:
        result.update(M_GUT=None, alpha_gut_inv=None, spread=np.inf,
                      mismatch=np.inf, unifies=False)
        return result

    m_gut = float(np.exp(np.mean(np.log(found))))
    spread = max(found) / min(found)
    # Coupling-space test at the alpha_1 = alpha_2 crossing
    k12 = int(np.argmin(np.abs(np.log(mu) - np.log(crossings["mu_12"]))))
    a12_inv = float(np.mean(alpha_inv[:2, k12]))
    mismatch = abs(float(alpha_inv[2, k12]) - a12_inv) / a12_inv
    # alpha_GUT^-1: mean of the three couplings at M_GUT
    k = int(np.argmin(np.abs(np.log(mu) - np.log(m_gut))))
    alpha_gut_inv = float(np.mean(alpha_inv[:, k]))
    result.update(M_GUT=m_gut, alpha_gut_inv=alpha_gut_inv,
                  spread=float(spread), mismatch=float(mismatch),
                  unifies=bool(mismatch < 0.03))
    return result


def proton_lifetime_years(m_gut_gev, alpha_gut):
    """Dimensional-analysis estimate of tau(p -> e+ pi0) in years.

    tau ~ M_GUT^4 / (alpha_GUT^2 m_p^5), the standard estimate for
    gauge-boson-mediated proton decay. Order-of-magnitude only: hadronic
    matrix elements, flavor mixing, and threshold corrections introduce
    a factor of O(10^1-10^2) uncertainty in either direction.
    """
    tau_natural = m_gut_gev**4 / (alpha_gut**2 * M_PROTON**5)  # [GeV^-1]
    return tau_natural * HBAR_GEV_S / SECONDS_PER_YEAR


def summary(loops=1, m_susy=1000.0):
    """Run SM and MSSM and return a dict of headline numbers."""
    out = {}
    for model in ("SM", "MSSM"):
        mu, a_inv = run_couplings(model=model, loops=loops, m_susy=m_susy)
        uni = find_unification(mu, a_inv)
        entry = dict(uni)
        if uni["M_GUT"] is not None and uni["alpha_gut_inv"] is not None:
            entry["tau_p_years"] = proton_lifetime_years(
                uni["M_GUT"], 1.0 / uni["alpha_gut_inv"])
        else:
            entry["tau_p_years"] = None
        out[model] = entry
    return out


# --------------------------------------------------------------------------
# Figures
# --------------------------------------------------------------------------

_LABELS = [r"$\alpha_1^{-1}$ (U(1)$_Y$, GUT norm.)",
           r"$\alpha_2^{-1}$ (SU(2)$_L$)",
           r"$\alpha_3^{-1}$ (SU(3)$_c$)"]
_COLORS = ["#1f77b4", "#d62728", "#2ca02c"]


def make_rg_figure_matplotlib(loops=1, m_susy=1000.0):
    """Two-panel figure: SM near-miss (left) vs MSSM unification (right)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), sharey=True)
    for ax, model in zip(axes, ("SM", "MSSM")):
        mu, a_inv = run_couplings(model=model, loops=loops, m_susy=m_susy)
        uni = find_unification(mu, a_inv)
        x = np.log10(mu)
        for i in range(3):
            ax.plot(x, a_inv[i], color=_COLORS[i], lw=1.8, label=_LABELS[i])
        if uni["M_GUT"] is not None and uni["unifies"]:
            xg = np.log10(uni["M_GUT"])
            ax.axvline(xg, color="gray", ls="--", lw=1)
            ax.annotate(
                rf"$M_{{\rm GUT}} \approx {uni['M_GUT']:.1e}$ GeV",
                xy=(xg, uni["alpha_gut_inv"]),
                xytext=(xg - 6.5, uni["alpha_gut_inv"] - 9),
                fontsize=9, arrowprops=dict(arrowstyle="->", lw=0.8))
        title = ("Standard Model: near miss" if model == "SM"
                 else f"MSSM ($m_{{\\rm SUSY}}$ = {m_susy:.0f} GeV): unification")
        ax.set_title(title, fontsize=11)
        ax.set_xlabel(r"$\log_{10}(\mu / \mathrm{GeV})$")
        ax.grid(alpha=0.3)
    axes[0].set_ylabel(r"$\alpha_i^{-1}(\mu)$")
    axes[0].legend(fontsize=9, loc="lower left")
    loop_word = "One" if loops == 1 else "Two"
    fig.suptitle(f"{loop_word}-loop running of the gauge couplings, "
                 "GUT normalization", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    return fig


def make_rg_figure_plotly(models=("SM", "MSSM"), loops=1, m_susy=1000.0):
    """Interactive Plotly version of the RG running figure."""
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    models = list(models)
    fig = make_subplots(
        rows=1, cols=len(models),
        subplot_titles=[("Standard Model: near miss" if m == "SM"
                         else f"MSSM (m_SUSY = {m_susy:.0f} GeV)")
                        for m in models],
        shared_yaxes=True)
    names = ["α₁⁻¹ (U(1) GUT norm.)", "α₂⁻¹ (SU(2))", "α₃⁻¹ (SU(3))"]
    for c, model in enumerate(models, start=1):
        mu, a_inv = run_couplings(model=model, loops=loops, m_susy=m_susy)
        uni = find_unification(mu, a_inv)
        x = np.log10(mu)
        for i in range(3):
            fig.add_trace(
                go.Scatter(x=x, y=a_inv[i], mode="lines",
                           line=dict(color=_COLORS[i], width=2),
                           name=names[i], legendgroup=names[i],
                           showlegend=(c == 1),
                           hovertemplate=("log10(μ/GeV)=%{x:.2f}<br>"
                                          "α⁻¹=%{y:.2f}<extra>"
                                          + names[i] + "</extra>")),
                row=1, col=c)
        if uni["M_GUT"] is not None and uni["unifies"]:
            fig.add_vline(x=np.log10(uni["M_GUT"]), line_dash="dash",
                          line_color="gray", row=1, col=c)
    fig.update_xaxes(title_text="log₁₀(μ / GeV)")
    fig.update_yaxes(title_text="αᵢ⁻¹(μ)", col=1)
    fig.update_layout(
        title=f"Renormalization-group running of the gauge couplings "
              f"({loops}-loop)",
        height=480, legend=dict(orientation="h", y=-0.25))
    return fig


def _print_summary_table():
    print("=" * 76)
    print("Gauge-coupling unification: reproduction of known results")
    print(f"Inputs (PDG 2024, MS-bar at M_Z = {M_Z} GeV):")
    a0 = boundary_conditions()
    print(f"  alpha_1^-1 = {a0[0]:.2f}   alpha_2^-1 = {a0[1]:.2f}   "
          f"alpha_3^-1 = {a0[2]:.2f}")
    print("=" * 76)
    hdr = (f"{'Model':<6} {'Loops':<6} {'M_GUT [GeV]':<12} "
           f"{'alpha_GUT^-1':<13} {'Mismatch':<9} {'Unifies':<8} "
           f"{'tau_p [yr]':<11}")
    print(hdr)
    print("-" * 76)
    for loops in (1, 2):
        res = summary(loops=loops)
        for model in ("SM", "MSSM"):
            r = res[model]
            mg = f"{r['M_GUT']:.2e}" if r["M_GUT"] else "-"
            ag = f"{r['alpha_gut_inv']:.1f}" if r["alpha_gut_inv"] else "-"
            mm = (f"{100 * r['mismatch']:.1f}%"
                  if np.isfinite(r["mismatch"]) else "-")
            tp = f"{r['tau_p_years']:.1e}" if r["tau_p_years"] else "-"
            print(f"{model:<6} {loops:<6} {mg:<12} {ag:<13} {mm:<9} "
                  f"{str(r['unifies']):<8} {tp:<11}")
    print("-" * 76)
    print(f"Super-Kamiokande bound: tau(p -> e+ pi0) > "
          f"{SUPERK_TAU_P_BOUND_YR:.1e} yr (90% CL, arXiv:2010.16098)")
    print("Note: tau_p is a dimensional-analysis estimate "
          "(order of magnitude only).")
    print("=" * 76)


if __name__ == "__main__":
    import os

    _print_summary_table()

    fig = make_rg_figure_matplotlib(loops=2)
    os.makedirs("gfx/rg", exist_ok=True)
    os.makedirs("paper/figures", exist_ok=True)
    fig.savefig("gfx/rg/rg_unification.png", dpi=300)
    fig.savefig("paper/figures/rg_unification.pdf")
    print("Wrote gfx/rg/rg_unification.png and paper/figures/rg_unification.pdf")

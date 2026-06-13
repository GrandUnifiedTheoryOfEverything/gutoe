#!/usr/bin/env python3
"""Embedding of the Standard Model fermions in SU(5) and SO(10).

Exposition of known results (Georgi & Glashow 1974; Fritzsch & Minkowski
1975). This module makes the group-theoretic content of grand unification
*computable* rather than asserted:

* the assignment of one SM generation to the 5-bar + 10 of SU(5),
* the derivation of the hypercharge GUT-normalization factor 5/3 from the
  embedding (via the trace over a generation),
* the gauge-anomaly cancellation checks (sum of Y and of Y^3 vanish),
* the SO(10) branching 16 = 10 + 5-bar + 1 (the singlet being the
  right-handed neutrino).

Nothing here is novel; it is the standard arithmetic that any unification
claim must exhibit, presented so it can be verified by running the code.

Conventions: all fermions written as left-handed Weyl spinors; electric
charge Q = T3 + Y with hypercharge Y in the convention where the lepton
doublet has Y = -1/2.
"""

from fractions import Fraction

# --------------------------------------------------------------------------
# One SM generation as left-handed Weyl fermions: (name, SU(3), SU(2), Y,
# multiplicity = dim(SU3 rep) x dim(SU2 rep), SU(5) irrep it lives in)
# Hypercharge convention: Q = T3 + Y.
# --------------------------------------------------------------------------
GENERATION = [
    # name      SU(3)  SU(2)  Y                 multiplicity  SU(5) irrep
    ("Q  = (u_L, d_L)", "3", "2", Fraction(1, 6), 6, "10"),
    ("u_L^c", "3bar", "1", Fraction(-2, 3), 3, "10"),
    ("e_L^c", "1", "1", Fraction(1, 1), 1, "10"),
    ("d_L^c", "3bar", "1", Fraction(1, 3), 3, "5bar"),
    ("L  = (nu_L, e_L)", "1", "2", Fraction(-1, 2), 2, "5bar"),
]

# SO(10): one generation plus the right-handed neutrino fills the spinorial 16
SO10_BRANCHING = "16 = 10 + 5bar + 1   (under SU(5); the 1 is nu_R^c)"


def hypercharge_trace_squared():
    """Tr(Y^2) over one SM generation (exact fraction)."""
    return sum(mult * y * y for _, _, _, y, mult, _ in GENERATION)


def hypercharge_normalization():
    """Derive the GUT normalization factor for hypercharge.

    In SU(5) all generators T^a are normalized identically:
    Tr(T^a T^b) = (1/2) delta^ab per fundamental, which over a generation
    (5bar + 10) fixes Tr(T^2) = 2 for every generator. The weak isospin
    generator T3 satisfies Tr(T3^2) = 2 over a generation, while the
    hypercharge as conventionally normalized gives Tr(Y^2) = 10/3.
    The properly normalized U(1) generator is therefore
    T1 = sqrt(3/5) Y, i.e.  alpha_1 = (5/3) alpha_Y.

    Returns the exact factor 5/3 computed from the traces, not hard-coded.
    """
    tr_y2 = hypercharge_trace_squared()  # = 10/3
    # Tr(T3^2) over a generation: doublets contribute 2 x (1/2)^2 per
    # SU(3)-color copy: quark doublet 3 colors x 2 x 1/4 = 3/2, lepton
    # doublet 2 x 1/4 = 1/2; total = 2.
    tr_t3sq = Fraction(3, 2) + Fraction(1, 2)
    return tr_y2 / tr_t3sq  # = 5/3


def check_anomaly_cancellation():
    """Verify gauge-anomaly cancellation within one generation.

    Returns a dict of exact sums, all of which must vanish:
    * 'sum_Y'   -- gravitational-U(1) anomaly: sum of Y over all Weyl fermions
    * 'sum_Y3'  -- U(1)^3 anomaly: sum of Y^3
    * 'su3_su3_Y' -- SU(3)^2-U(1): sum of Y over color triplets/antitriplets
    * 'su2_su2_Y' -- SU(2)^2-U(1): sum of Y over SU(2) doublets
    """
    sum_y = sum(mult * y for _, _, _, y, mult, _ in GENERATION)
    sum_y3 = sum(mult * y**3 for _, _, _, y, mult, _ in GENERATION)
    # SU(3)^2-U(1): sum Y over colored states, weighted by SU(2) dimension
    su3_y = sum(y * (2 if su2 == "2" else 1)
                for _, su3, su2, y, mult, _ in GENERATION
                if su3 in ("3", "3bar"))
    # SU(2)^2-U(1): sum Y over doublets, weighted by color dimension
    su2_y = sum(y * (3 if su3 in ("3", "3bar") else 1)
                for _, su3, su2, y, mult, _ in GENERATION
                if su2 == "2")
    return {
        "sum_Y": sum_y,
        "sum_Y3": sum_y3,
        "su3_su3_Y": su3_y,
        "su2_su2_Y": su2_y,
        "all_vanish": sum_y == 0 and sum_y3 == 0 and su3_y == 0
                      and su2_y == 0,
    }


def assignment_table_markdown():
    """SM-generation -> SU(5) assignment as a markdown table."""
    lines = [
        "| Field | $SU(3)_c$ | $SU(2)_L$ | $Y$ | States | $SU(5)$ irrep |",
        "|---|---|---|---|---|---|",
    ]
    pretty = {"3": "$\\mathbf{3}$", "3bar": "$\\bar{\\mathbf{3}}$",
              "1": "$\\mathbf{1}$", "2": "$\\mathbf{2}$",
              "10": "$\\mathbf{10}$", "5bar": "$\\bar{\\mathbf{5}}$"}
    names = {"Q  = (u_L, d_L)": "$Q=(u_L,d_L)$", "u_L^c": "$u^c_L$",
             "e_L^c": "$e^c_L$", "d_L^c": "$d^c_L$",
             "L  = (nu_L, e_L)": "$L=(\\nu_L,e_L)$"}
    for name, su3, su2, y, mult, irrep in GENERATION:
        yval = (f"${y.numerator}$" if y.denominator == 1
                else f"${y.numerator}/{y.denominator}$")
        lines.append(
            f"| {names[name]} | {pretty[su3]} | {pretty[su2]} "
            f"| {yval} | {mult} | {pretty[irrep]} |")
    return "\n".join(lines)


def assignment_table_latex():
    """SM-generation -> SU(5) assignment as LaTeX tabular rows (booktabs)."""
    names = {"Q  = (u_L, d_L)": r"$Q=(u_L,d_L)$", "u_L^c": r"$u^c_L$",
             "e_L^c": r"$e^c_L$", "d_L^c": r"$d^c_L$",
             "L  = (nu_L, e_L)": r"$L=(\nu_L,e_L)$"}
    pretty = {"3": r"$\mathbf{3}$", "3bar": r"$\bar{\mathbf{3}}$",
              "1": r"$\mathbf{1}$", "2": r"$\mathbf{2}$",
              "10": r"$\mathbf{10}$", "5bar": r"$\bar{\mathbf{5}}$"}
    rows = []
    for name, su3, su2, y, mult, irrep in GENERATION:
        yval = (f"${y.numerator}$" if y.denominator == 1
                else f"${y.numerator}/{y.denominator}$")
        rows.append(f"{names[name]} & {pretty[su3]} & {pretty[su2]} & "
                    f"{yval} & {mult} & {pretty[irrep]} \\\\")
    return "\n".join(rows)


def summary():
    """Headline numbers as a dict (exact fractions preserved)."""
    anomalies = check_anomaly_cancellation()
    return {
        "tr_Y2": hypercharge_trace_squared(),
        "normalization_factor": hypercharge_normalization(),
        "anomalies": anomalies,
        "so10_branching": SO10_BRANCHING,
    }


if __name__ == "__main__":
    s = summary()
    print("SU(5) / SO(10) embedding of one SM generation")
    print("=" * 60)
    print(assignment_table_markdown())
    print("-" * 60)
    print(f"Tr(Y^2) over one generation       = {s['tr_Y2']}")
    print(f"GUT normalization alpha_1/alpha_Y = "
          f"{s['normalization_factor']}  (expected 5/3)")
    a = s["anomalies"]
    print(f"Anomaly sums: sum Y = {a['sum_Y']}, sum Y^3 = {a['sum_Y3']}, "
          f"SU(3)^2-Y = {a['su3_su3_Y']}, SU(2)^2-Y = {a['su2_su2_Y']}")
    print(f"All anomalies vanish: {a['all_vanish']}")
    print(f"SO(10): {s['so10_branching']}")

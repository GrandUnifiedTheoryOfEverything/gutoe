#!/usr/bin/env python3
"""Formal presentation of the composite action (single source of truth).

This module holds the LaTeX text, glossary, and formal statements
(Definition / Remark / Proposition) used by the Streamlit app, the
documentation, and the paper, so the three surfaces cannot drift apart.

The framing follows the independent academic evaluation of this project:
the master equation is presented as a *Definition* (an organizing
framework), never as a theorem of unification. The quantitative content
lives in the Propositions, which are reproductions of known results,
verifiable by running toe_math/rg_running.py and toe_math/gut_embedding.py.
"""

# --------------------------------------------------------------------------
# The composite action, as a single KaTeX/LaTeX-compatible aligned block.
# KaTeX (used by Streamlit's st.latex) supports `aligned`, not `align`.
# --------------------------------------------------------------------------
MASTER_EQUATION_ALIGNED = r"""
\begin{aligned}
S \;&=\; S_{\text{gravity}} \;+\; S_{\text{matter}} \;+\; S_{\text{gauge}}
\;+\; S_{\text{quantum}}\\[10pt]
S_{\text{gravity}} \;&=\; \frac{1}{16\pi G}\int d^4x\,\sqrt{-g}\,
\left(R - 2\Lambda\right)\\[6pt]
S_{\text{matter}} \;&=\; \int d^4x\,\sqrt{-g}\,
\Bigl[\,\bar{\psi}\bigl(i\gamma^{\mu}D_{\mu}-m\bigr)\psi
\;+\; \bigl(D_{\mu}\phi\bigr)^{\!\dagger}\bigl(D^{\mu}\phi\bigr)
- V(\phi)\Bigr]\\[6pt]
S_{\text{gauge}} \;&=\; -\frac{1}{4}\int d^4x\,\sqrt{-g}\,
F_{\mu\nu}^{a}F^{a\,\mu\nu}\\[6pt]
S_{\text{quantum}} \;&=\; \sum_{n=1}^{\infty}\hbar^{n}\,S_{n}
\qquad\text{(loop expansion)}
\end{aligned}
"""

# Per-line fallback for renderers that cannot handle the aligned block
MASTER_EQUATION_LINES = [
    r"S = S_{\text{gravity}} + S_{\text{matter}} + S_{\text{gauge}} + S_{\text{quantum}}",
    r"S_{\text{gravity}} = \frac{1}{16\pi G}\int d^4x\,\sqrt{-g}\,(R - 2\Lambda)",
    r"S_{\text{matter}} = \int d^4x\,\sqrt{-g}\,\left[\bar{\psi}(i\gamma^{\mu}D_{\mu}-m)\psi + (D_{\mu}\phi)^{\dagger}(D^{\mu}\phi) - V(\phi)\right]",
    r"S_{\text{gauge}} = -\frac{1}{4}\int d^4x\,\sqrt{-g}\,F_{\mu\nu}^{a}F^{a\,\mu\nu}",
    r"S_{\text{quantum}} = \sum_{n=1}^{\infty}\hbar^{n} S_{n}",
]

HIGGS_POTENTIAL = r"V(\phi) = -\mu^2|\phi|^2 + \lambda|\phi|^4"
FIELD_STRENGTH = (r"F_{\mu\nu}^{a} = \partial_{\mu}A_{\nu}^{a} "
                  r"- \partial_{\nu}A_{\mu}^{a} "
                  r"+ g f^{abc}A_{\mu}^{b}A_{\nu}^{c}")

# --------------------------------------------------------------------------
# Symbol glossary: (latex, name, units / dimensions, first appears in)
# --------------------------------------------------------------------------
GLOSSARY = [
    {"symbol": r"$S$", "name": "Action", "units": r"dimensionless (units of $\hbar$)", "appears": "Definition 1"},
    {"symbol": r"$g_{\mu\nu}$, $g$", "name": "Metric tensor; its determinant", "units": "dimensionless", "appears": r"$S_{\text{gravity}}$"},
    {"symbol": r"$R$", "name": "Ricci scalar curvature", "units": r"$\mathrm{m}^{-2}$", "appears": r"$S_{\text{gravity}}$"},
    {"symbol": r"$\Lambda$", "name": "Cosmological constant", "units": r"$1.1056\times10^{-52}\ \mathrm{m}^{-2}$ (Planck 2018)", "appears": r"$S_{\text{gravity}}$"},
    {"symbol": r"$G$", "name": "Newton's gravitational constant", "units": r"$6.674\times10^{-11}\ \mathrm{m^3\,kg^{-1}\,s^{-2}}$", "appears": r"$S_{\text{gravity}}$"},
    {"symbol": r"$\psi$, $\bar{\psi}$", "name": "Dirac fermion field and its adjoint", "units": r"$[\psi] = \mathrm{(mass)}^{3/2}$ (natural units)", "appears": r"$S_{\text{matter}}$"},
    {"symbol": r"$\gamma^{\mu}$", "name": "Dirac matrices (curved-space)", "units": "dimensionless", "appears": r"$S_{\text{matter}}$"},
    {"symbol": r"$D_{\mu}$", "name": "Gauge- and spacetime-covariant derivative", "units": r"$\mathrm{(mass)}^{1}$", "appears": r"$S_{\text{matter}}$"},
    {"symbol": r"$m$", "name": "Fermion mass", "units": r"$\mathrm{GeV}$", "appears": r"$S_{\text{matter}}$"},
    {"symbol": r"$\phi$", "name": "Higgs doublet (scalar field)", "units": r"$[\phi] = \mathrm{(mass)}^{1}$", "appears": r"$S_{\text{matter}}$"},
    {"symbol": r"$V(\phi)$", "name": "Higgs potential $-\mu^2|\phi|^2+\lambda|\phi|^4$", "units": r"$\mathrm{(mass)}^{4}$", "appears": r"$S_{\text{matter}}$"},
    {"symbol": r"$F^{a}_{\mu\nu}$", "name": "Yang–Mills field-strength tensor", "units": r"$\mathrm{(mass)}^{2}$", "appears": r"$S_{\text{gauge}}$"},
    {"symbol": r"$A^{a}_{\mu}$", "name": "Gauge potential, adjoint index $a$", "units": r"$\mathrm{(mass)}^{1}$", "appears": r"$S_{\text{gauge}}$"},
    {"symbol": r"$f^{abc}$", "name": "Gauge-group structure constants", "units": "dimensionless", "appears": r"$S_{\text{gauge}}$"},
    {"symbol": r"$\hbar$", "name": "Reduced Planck constant (loop-counting parameter)", "units": r"$1.0546\times10^{-34}\ \mathrm{J\,s}$", "appears": r"$S_{\text{quantum}}$"},
    {"symbol": r"$S_{n}$", "name": "$n$-loop effective-action correction", "units": "dimensionless", "appears": r"$S_{\text{quantum}}$"},
    {"symbol": r"$\alpha_i$", "name": r"Gauge couplings $g_i^2/4\pi$, $i=1,2,3$ (GUT norm.: $\alpha_1=\tfrac{5}{3}\alpha_Y$)", "units": "dimensionless", "appears": "Proposition 1"},
    {"symbol": r"$M_{\mathrm{GUT}}$", "name": "Gauge-coupling unification scale", "units": r"$\approx 2\times10^{16}\ \mathrm{GeV}$ (MSSM)", "appears": "Proposition 2"},
]

# --------------------------------------------------------------------------
# Formal statements
# --------------------------------------------------------------------------
DEFINITION_TEXT = (
    "**Definition 1 (Composite action; organizing framework).** "
    "Let $S$ denote the sum of the four sector actions displayed above: "
    "the Einstein–Hilbert action with cosmological constant, the matter "
    "action (Dirac fermions and the Higgs doublet, minimally coupled to "
    "gravity and the gauge fields), the Yang–Mills gauge action for "
    "$SU(3)_c \\times SU(2)_L \\times U(1)_Y$, and the formal loop "
    "expansion of quantum corrections. $S$ *organizes* the standard "
    "actions of fundamental physics in a single expression. It is a "
    "definition, not a theorem: the sum carries no unifying dynamics "
    "beyond that of its parts, and each term is a transcription of an "
    "established, separately tested action."
)

REMARK_GRAVITY_PROGRAMS = (
    "**Remark 1 (The gravity sector: one action, several research "
    "programs).** Only the Einstein–Hilbert action enters the composite "
    "action $S$. The loop-quantum-gravity (Ashtekar-variable) and "
    "string-theoretic (NS–NS effective) gravitational actions, which "
    "earlier versions of this project listed alongside it, are *mutually "
    "exclusive* candidate UV completions: they live in different "
    "dimensions (4 vs. 10), use different fundamental variables (metric "
    "vs. triad–connection vs. string fields), and belong to competing "
    "research programs. They are presented in this project as alternative "
    "proposals to be compared — never summed. A genuine unified theory "
    "must select or derive one and recover the others' regimes as limits; "
    "that derivation does not exist here or, to date, anywhere in the "
    "literature."
)

PROPOSITION_RG = (
    "**Proposition 1 (Standard Model near-miss).** With PDG 2024 inputs "
    "at $M_Z$ and one- or two-loop running, the three GUT-normalized "
    "inverse couplings $\\alpha_i^{-1}(\\mu)$ of the SM approach one "
    "another at high scales but fail to meet: at the "
    "$\\alpha_1=\\alpha_2$ crossing the relative deviation of "
    "$\\alpha_3^{-1}$ exceeds 10%. *Proof: by computation; run* "
    "`python3 -m toe_math.rg_running`.\n\n"
    "**Proposition 2 (MSSM unification).** With superpartners at "
    "$m_{\\mathrm{SUSY}} \\approx 1$ TeV, the three couplings unify to "
    "within 2.3% (one loop) and 0.7% (two loops) at "
    "$M_{\\mathrm{GUT}} \\approx 1.3\\text{–}1.5 \\times 10^{16}$ GeV "
    "with $\\alpha_{\\mathrm{GUT}}^{-1} \\approx 25$. This reproduces "
    "Amaldi–de Boer–Fürstenau (1991) and Martin–Ramond "
    "(hep-ph/9501244). *Proof: by computation, as above.*\n\n"
    "**Proposition 3 (Proton-lifetime estimate).** The dimensional "
    "estimate $\\tau_p \\sim M_{\\mathrm{GUT}}^4 / (\\alpha_{\\mathrm{GUT}}^2 "
    "m_p^5)$ for gauge-mediated $p \\to e^+\\pi^0$ gives "
    "$\\tau_p \\sim 10^{35\\text{–}36}$ yr for the MSSM unification point "
    "— above the Super-Kamiokande bound "
    "$\\tau_p > 2.4\\times10^{34}$ yr — while the SM near-miss scale "
    "($\\sim 10^{14\\text{–}15}$ GeV) would imply "
    "$\\tau_p \\sim 10^{30\\text{–}31}$ yr, *excluded* by four orders of "
    "magnitude. This order-of-magnitude argument is the classic reason "
    "minimal non-supersymmetric SU(5) is ruled out. "
    "*Proof: by computation, as above; order-of-magnitude only.*"
)

WHAT_IT_IS_NOT = (
    "**What this equation is — and is not.** The composite action is an "
    "*additive juxtaposition* of separately established actions. It does "
    "not unify them: there is no single gauge group from which the forces "
    "emerge (Definition 1), no derived inter-sector couplings, and no "
    "resolution of the perturbative non-renormalizability of gravity "
    "(Goroff–Sagnotti 1986). Writing $S = A + B + C + D$ is the starting "
    "point of every field-theory course, not a theory of everything. The "
    "quantitative content of this project lies in the Propositions — "
    "reproductions of known unification physics — and in the open "
    "problems it states honestly. See the Conclusion & Assessment page."
)

OPEN_PROBLEMS = [
    "Specify a single unifying gauge group and derive the embedding of "
    "all three generations, including the Yukawa sector and mixing "
    "angles, rather than exhibiting the one-generation group theory.",
    "Derive (not assert) the inter-sector couplings: the matter–gravity, "
    "gauge–gravity, and scalar-sector interactions must follow from one "
    "principle.",
    "Confront gravitational non-renormalizability: the Goroff–Sagnotti "
    "two-loop divergence must be cured by a finiteness mechanism (string "
    "theory), a fixed point (asymptotic safety), or another demonstrated "
    "mechanism.",
    "Demonstrate that exactly one gravitational UV completion is "
    "selected, with the others recovered or excluded in appropriate "
    "limits (cf. Remark 1).",
    "Produce at least one quantitative, falsifiable prediction beyond "
    "those of the constituent theories (a proton-decay lifetime with "
    "controlled hadronic uncertainties, a superpartner mass, a measurable "
    "coupling deviation).",
]

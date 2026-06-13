# The Composite Action: Formal Presentation

This document states the formal content of the project: what is defined,
what is computed, and what remains open. Citation keys refer to
[REFERENCES.md](REFERENCES.md). Everything quantitative here can be
reproduced by running the code indicated in each proof.

## 1. Notation and conventions

- Metric signature $(-,+,+,+)$; spacetime dimension 4 unless stated.
- Natural units $\hbar = c = 1$ in field-theoretic expressions; SI values
  are given for constants where dimensional checks matter.
- Hypercharge convention $Q = T_3 + Y$; GUT normalization
  $\alpha_1 = \tfrac{5}{3}\,\alpha_Y$ (derived in
  [GUT_EMBEDDING.md](GUT_EMBEDDING.md), not assumed).
- Physical constants:
  - $G = 6.674\,30\times10^{-11}\ \mathrm{m^3\,kg^{-1}\,s^{-2}}$ [PDG2024]
  - $c = 299\,792\,458\ \mathrm{m\,s^{-1}}$ (exact)
  - $\hbar = 1.054\,571\,817\times10^{-34}\ \mathrm{J\,s}$ (exact)
  - $\Lambda = 1.1056\times10^{-52}\ \mathrm{m^{-2}}$ [Planck2018] —
    note the units; a dimensionless $\Lambda$ is meaningless.

## 2. Definitions

**Definition 1 (Composite action; organizing framework).**

$$S \;=\; S_{\text{gravity}} + S_{\text{matter}} + S_{\text{gauge}} + S_{\text{quantum}}$$

with the four sector actions given by Definitions 2–5. $S$ *organizes*
the standard actions of fundamental physics in a single expression. It is
a definition, not a theorem: the sum carries no unifying dynamics beyond
that of its parts, each term being a transcription of an established,
separately tested action. (See "What this is not" in
[CONCLUSION.md](CONCLUSION.md).)

**Definition 2 (Gravity sector: Einstein–Hilbert).** [PeskinSchroeder; PDG2024]

$$S_{\text{gravity}} = \frac{1}{16\pi G}\int d^4x\,\sqrt{-g}\,(R - 2\Lambda)$$

**Definition 3 (Matter sector: Dirac and Higgs in curved spacetime).**

$$S_{\text{matter}} = \int d^4x\,\sqrt{-g}\left[\bar{\psi}\left(i\gamma^\mu D_\mu - m\right)\psi + (D_\mu\phi)^\dagger(D^\mu\phi) - V(\phi)\right]$$

with the symmetry-breaking potential
$V(\phi) = -\mu^2|\phi|^2 + \lambda|\phi|^4$, $\mu^2, \lambda > 0$,
vacuum expectation value $v = \sqrt{\mu^2/\lambda}$.

**Definition 4 (Gauge sector: Yang–Mills for $SU(3)_c\times SU(2)_L\times U(1)_Y$).**

$$S_{\text{gauge}} = -\frac{1}{4}\int d^4x\,\sqrt{-g}\,F^a_{\mu\nu}F^{a\,\mu\nu},\qquad F^a_{\mu\nu} = \partial_\mu A^a_\nu - \partial_\nu A^a_\mu + g f^{abc}A^b_\mu A^c_\nu$$

**Definition 5 (Quantum sector: formal loop expansion).**

$$Z = \int \mathcal{D}\phi\; e^{iS[\phi]},\qquad S_{\text{quantum}} = \sum_{n=1}^{\infty}\hbar^n S_n$$

This is the *organizing statement* of perturbative quantum corrections.
It presupposes a perturbatively consistent theory — precisely what the
gravity sector lacks (Open Problem 3).

## 3. Remark on the gravity sector

**Remark 1 (One action, several research programs).** Only the
Einstein–Hilbert action (Definition 2) enters the composite action $S$.
The loop-quantum-gravity (Ashtekar-variable) action and the
string-theoretic (NS–NS sector) effective action, which earlier versions
of this project listed as parallel "formulations" of $S_{\text{gravity}}$,
are **mutually exclusive candidate UV completions**: they live in
different dimensions (4 vs. 10), are built on different fundamental
variables (metric vs. triad–connection vs. string fields), and belong to
competing research programs [Rovelli2004; Polchinski1998]. They are
presented in this project as alternatives to be compared — never summed.
A genuine unified theory must select or derive one and recover the
others' regimes as limits; that derivation does not exist here or, to
date, anywhere in the literature.

## 4. Propositions (reproductions of known results)

The following are the quantitative content of this project. Each is a
*reproduction* of an established result, with the computation included in
the repository so the proof is a program run, not an assertion.

**Proposition 1 (Standard Model near-miss).** With PDG 2024 inputs at
$M_Z$ ($\alpha_{em}^{-1} = 127.951$, $\sin^2\theta_W = 0.23122$,
$\alpha_s = 0.1179$, MS-bar) and one- or two-loop running with
$b^{SM} = (41/10,\, -19/6,\, -7)$, the three GUT-normalized inverse
couplings approach one another at high scales but fail to meet: at the
$\alpha_1 = \alpha_2$ crossing, $\alpha_3^{-1}$ deviates by **13.1%
(one loop) / 11.5% (two loops)** — an order of magnitude beyond
experimental uncertainty.
*Proof:* by computation — `python3 -m toe_math.rg_running`. ∎

**Proposition 2 (MSSM unification).** With superpartners at
$m_{\mathrm{SUSY}} = 1$ TeV and $b^{MSSM} = (33/5,\, 1,\, -3)$
[DimopoulosGeorgi1981; MartinRamond1995], the couplings unify to within
**2.3% (one loop) / 0.7% (two loops)** at

$$M_{\mathrm{GUT}} \approx 1.3\text{–}1.5\times10^{16}\ \mathrm{GeV},\qquad \alpha_{\mathrm{GUT}}^{-1} \approx 25,$$

reproducing [Amaldi1991; MartinRamond1995].
*Proof:* by computation, as above. ∎

**Proposition 3 (Proton-lifetime estimate).** The dimensional estimate
for gauge-boson-mediated $p\to e^+\pi^0$,

$$\tau_p \sim \frac{M_{\mathrm{GUT}}^4}{\alpha_{\mathrm{GUT}}^2\, m_p^5},$$

gives $\tau_p \sim 10^{35\text{–}36}$ yr at the MSSM unification point —
consistent with the Super-Kamiokande bound
$\tau_p > 2.4\times10^{34}$ yr [SuperK2020] — while the SM near-miss
scale ($\sim 10^{14\text{–}15}$ GeV) would imply
$\tau_p \sim 10^{30\text{–}31}$ yr, **excluded by four orders of
magnitude**. This is the classic argument ruling out minimal
non-supersymmetric SU(5). The estimate is order-of-magnitude only:
hadronic matrix elements and threshold corrections contribute factors of
$O(10^{1\text{–}2})$ in either direction.
*Proof:* by computation, as above. ∎

**Proposition 4 (Embedding arithmetic).** One SM generation fits exactly
into $\bar{\mathbf{5}}\oplus\mathbf{10}$ of SU(5); the hypercharge
normalization $\alpha_1 = \tfrac{5}{3}\alpha_Y$ follows from
$\mathrm{Tr}(Y^2) = 10/3$ over a generation; all four gauge-anomaly sums
vanish; and the SO(10) spinor branches as
$\mathbf{16} = \mathbf{10}\oplus\bar{\mathbf{5}}\oplus\mathbf{1}$ (the
singlet being the right-handed neutrino) [GeorgiGlashow1974;
FritzschMinkowski1975].
*Proof:* by computation — `python3 -m toe_math.gut_embedding`. ∎

## 5. Open problems

What would be required for this framework to rise from organized
compilation to scientific theory (after [Evaluation2026], §6.4):

1. **Unifying group with full matter dynamics.** Specify a single gauge
   group and derive the embedding of all three generations *including
   the Yukawa sector and mixing angles*, not only the one-generation
   group theory of Proposition 4.
2. **Derived inter-sector couplings.** The matter–gravity,
   gauge–gravity, and scalar-sector interactions must follow from one
   principle rather than be assembled.
3. **Gravitational non-renormalizability.** The two-loop divergence of
   quantized Einstein gravity [GoroffSagnotti1986; tHooftVeltman1974]
   must be cured by a demonstrated mechanism — finiteness (string
   theory), a non-trivial fixed point (asymptotic safety), or otherwise.
4. **Selection in the gravity sector.** Exactly one UV completion must
   be selected, with the others recovered or excluded in appropriate
   limits (Remark 1).
5. **A novel falsifiable prediction.** At least one quantitative
   prediction beyond those of the constituent theories: a proton
   lifetime with controlled hadronic uncertainties, a superpartner mass,
   or a measurable coupling deviation. Note that ATLAS already excludes
   gluinos below 2.3 TeV and squarks below 1.85 TeV in simplified models
   [ATLAS2020], constraining the $m_{\mathrm{SUSY}}$ window that makes
   Proposition 2 work.

## 6. Where everything lives

| Content | Code | Document |
|---|---|---|
| Composite action, glossary | `toe_math/master_equation.py` | this file |
| RG running, unification, $\tau_p$ | `toe_math/rg_running.py` | [RG_UNIFICATION.md](RG_UNIFICATION.md) |
| SU(5)/SO(10) embedding | `toe_math/gut_embedding.py` | [GUT_EMBEDDING.md](GUT_EMBEDDING.md) |
| Honest assessment | — | [CONCLUSION.md](CONCLUSION.md) |
| Compiled paper | `paper/gutoe.tex` | `paper/gutoe.pdf` |

# Gauge-Coupling Unification: Methods and Results

The quantitative centerpiece of this project: a from-scratch reproduction
of the renormalization-group analysis showing that the three Standard
Model gauge couplings *nearly* unify in the SM and *do* unify in the
MSSM. Citations refer to [REFERENCES.md](REFERENCES.md). Reproduce every
number here with:

```bash
python3 -m toe_math.rg_running
```

![RG unification](../gfx/rg/rg_unification.png)

## 1. Inputs

PDG 2024 world averages, MS-bar scheme at $\mu = M_Z = 91.1876$ GeV
[PDG2024]:

| Quantity | Value |
|---|---|
| $\alpha_{em}^{-1}(M_Z)$ | 127.951 |
| $\sin^2\theta_W(M_Z)$ | 0.23122 |
| $\alpha_s(M_Z)$ | 0.1179 |

## 2. GUT normalization and boundary conditions

The SU(5)/SO(10) embedding fixes $\alpha_1 = \tfrac{5}{3}\alpha_Y$ — the
factor is *derived* from $\mathrm{Tr}(Y^2)$ over one generation in
[GUT_EMBEDDING.md](GUT_EMBEDDING.md). The inverse couplings at $M_Z$ are

$$\alpha_1^{-1} = \tfrac{3}{5}\cos^2\theta_W\,\alpha_{em}^{-1} = 59.02,\qquad \alpha_2^{-1} = \sin^2\theta_W\,\alpha_{em}^{-1} = 29.58,\qquad \alpha_3^{-1} = \alpha_s^{-1} = 8.48.$$

## 3. Running

**One loop (analytic).**
$\alpha_i^{-1}(\mu) = \alpha_i^{-1}(M_Z) - \frac{b_i}{2\pi}\ln\frac{\mu}{M_Z}$, with

| | $b_1$ | $b_2$ | $b_3$ |
|---|---|---|---|
| SM | 41/10 | −19/6 | −7 |
| MSSM | 33/5 | 1 | −3 |

**Two loops (numerical).** The coupled system
$\frac{d\alpha_i^{-1}}{d\ln\mu} = -\frac{1}{2\pi}\bigl[b_i + \frac{1}{4\pi}\sum_j b_{ij}\,\alpha_j\bigr]$
is integrated with the standard matrices $b_{ij}$ [MachacekVaughn;
MartinRamond1995]; Yukawa contributions are neglected (a percent-level
effect dominated by the top Yukawa).

**Threshold matching.** For the MSSM, SM beta functions are used from
$M_Z$ to $m_{\mathrm{SUSY}}$ (default 1 TeV) and MSSM beta functions
above — one-step matching.

## 4. Unification criterion

Crossing *scales* of the pairwise intersections spread widely even for
good unification, because the lines cross at shallow angles. The honest
discriminator is the **coupling-space mismatch**: the relative deviation
of $\alpha_3^{-1}$ from $\alpha_1^{-1} = \alpha_2^{-1}$ at their
crossing. We call the couplings unified when the mismatch is below 3%.

## 5. Results

| Model | Loops | $M_{\mathrm{GUT}}$ [GeV] | $\alpha_{\mathrm{GUT}}^{-1}$ | Mismatch | Unifies | $\tau_p$ [yr] |
|---|---|---|---|---|---|---|
| SM | 1 | 6.2×10¹⁴ | 41.9 | 13.1% | no | 7.5×10³⁰ |
| MSSM | 1 | 1.5×10¹⁶ | 25.7 | 2.3% | **yes** | 1.0×10³⁶ |
| SM | 2 | 3.8×10¹⁴ | 41.7 | 11.5% | no | 1.0×10³⁰ |
| MSSM | 2 | 1.3×10¹⁶ | 25.1 | 0.7% | **yes** | 4.5×10³⁵ |

($M_{\mathrm{GUT}}$ = geometric mean of the three pairwise crossing
scales; $\tau_p$ from the dimensional estimate of Proposition 3.)

**Confrontation with experiment.** Super-Kamiokande:
$\tau(p\to e^+\pi^0) > 2.4\times10^{34}$ yr [SuperK2020]. The MSSM
unification point survives; the SM near-miss scale is excluded by four
orders of magnitude — the classic demise of minimal non-SUSY SU(5).
Conversely, ATLAS limits (gluino > 2.3 TeV in simplified models
[ATLAS2020]) squeeze the $m_{\mathrm{SUSY}}$ assumption from below; the
interactive app exposes $m_{\mathrm{SUSY}}$ as a parameter so the reader
can see the (mild, logarithmic) sensitivity.

## 6. Honest scope

This reproduces [Amaldi1991] and [MartinRamond1995]. It is included
because any project speaking about unification must *compute* the one
thing that is computable at this level — not as a claim of novelty.

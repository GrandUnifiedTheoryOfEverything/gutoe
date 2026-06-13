# Embedding the Standard Model in SU(5) and SO(10)

Exposition of known results [GeorgiGlashow1974; FritzschMinkowski1975] —
the group-theoretic arithmetic that any unification claim must exhibit,
made computable. Reproduce every number with:

```bash
python3 -m toe_math.gut_embedding
```

Citations refer to [REFERENCES.md](REFERENCES.md). Conventions:
left-handed Weyl fermions, $Q = T_3 + Y$.

## 1. One generation in SU(5)

| Field | $SU(3)_c$ | $SU(2)_L$ | $Y$ | States | $SU(5)$ irrep |
|---|---|---|---|---|---|
| $Q=(u_L,d_L)$ | $\mathbf{3}$ | $\mathbf{2}$ | $1/6$ | 6 | $\mathbf{10}$ |
| $u^c_L$ | $\bar{\mathbf{3}}$ | $\mathbf{1}$ | $-2/3$ | 3 | $\mathbf{10}$ |
| $e^c_L$ | $\mathbf{1}$ | $\mathbf{1}$ | $1$ | 1 | $\mathbf{10}$ |
| $d^c_L$ | $\bar{\mathbf{3}}$ | $\mathbf{1}$ | $1/3$ | 3 | $\bar{\mathbf{5}}$ |
| $L=(\nu_L,e_L)$ | $\mathbf{1}$ | $\mathbf{2}$ | $-1/2$ | 2 | $\bar{\mathbf{5}}$ |

Fifteen Weyl fermions fill $\bar{\mathbf{5}}\oplus\mathbf{10}$ exactly —
no state left over, none missing.

## 2. The hypercharge normalization, derived

In SU(5) all generators are normalized identically, so over one
generation $\mathrm{Tr}(T^2)$ must be equal for $T_3$ and for the
properly normalized hypercharge generator $T_1$:

$$\mathrm{Tr}(Y^2) = 6\cdot\tfrac{1}{36} + 3\cdot\tfrac{4}{9} + 1 + 3\cdot\tfrac{1}{9} + 2\cdot\tfrac{1}{4} = \tfrac{10}{3},\qquad \mathrm{Tr}(T_3^2) = 2.$$

Hence $T_1 = \sqrt{3/5}\,Y$ and

$$\alpha_1 = \tfrac{5}{3}\,\alpha_Y.$$

This is the factor used (and required) by the RG analysis in
[RG_UNIFICATION.md](RG_UNIFICATION.md) — derived, not assumed.

## 3. Anomaly cancellation

All four gauge-anomaly sums vanish within one generation (exact
fractions, computed in `toe_math/gut_embedding.py`):

| Anomaly | Sum | Value |
|---|---|---|
| grav–$U(1)$ | $\sum Y$ | 0 |
| $U(1)^3$ | $\sum Y^3$ | 0 |
| $SU(3)^2$–$U(1)$ | $\sum_{\text{colored}} Y$ | 0 |
| $SU(2)^2$–$U(1)$ | $\sum_{\text{doublets}} Y$ | 0 |

## 4. SO(10)

The spinorial $\mathbf{16}$ of SO(10) branches under SU(5) as

$$\mathbf{16} = \mathbf{10} \oplus \bar{\mathbf{5}} \oplus \mathbf{1},$$

accommodating one full generation *plus a right-handed neutrino* (the
singlet) — the natural seed of the seesaw mechanism
[FritzschMinkowski1975].

## 5. What this does and does not establish

This arithmetic shows the SM *fits* in SU(5)/SO(10) — a necessary
condition for grand unification and the reason GUTs are taken seriously.
It does **not** establish unification: that requires the dynamical
content listed as Open Problems in [THEORY.md](THEORY.md) (Yukawa sector,
symmetry breaking, proton-decay rates with controlled uncertainties).

# Appendix: Schumann Resonances as a Classical EM-Cavity Demonstration

**Scope.** This appendix documents `toe_math/schumann.py`, a
self-contained demonstration of *classical* electrodynamics: the
standing-wave resonances of the Earth–ionosphere spherical cavity, with
fundamental mode near 7.83 Hz.

**Why it is quarantined here.** Schumann resonances are real, well
understood, and entirely classical geophysics. They have **no bearing on
fundamental unification**: they play no role in the composite action,
the gauge-coupling analysis, or any other claim in this project. The
independent evaluation [Evaluation2026] correctly identified their
earlier placement alongside the unification material as a category error
(compounded by the topic's entanglement with pseudoscientific
"consciousness" claims in popular culture, which this project does not
endorse in any form). The module is retained solely as a clean worked
example of a spherical-waveguide eigenvalue problem.

## The physics

An idealized model treats the space between the conducting Earth
(radius $a \approx 6371$ km) and the ionosphere as a thin spherical
cavity. The transverse-magnetic eigenfrequencies are

$$f_n = \frac{c}{2\pi a}\sqrt{n(n+1)},\qquad n = 1, 2, 3, \ldots$$

giving the idealized series 10.6, 18.4, 26.0, 33.5 Hz. Observed peaks
(7.83, 14.3, 20.8, 27.3, 33.8 Hz) sit lower because the real ionosphere
is a lossy, finitely conducting boundary; the module includes the
standard empirical correction.

## Usage

```python
from toe_math.schumann import SchumannResonance  # see module for API
```

The module computes the eigenfrequency series, plots spectra, and renders
the cavity geometry. See the docstrings in `toe_math/schumann.py`.

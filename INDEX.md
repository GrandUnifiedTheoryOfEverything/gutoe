# Repository Index

Top-level map of the GUToE repository. Full details: [README.md](README.md)
and [docs/index.md](docs/index.md).

## Entry points

| Command | What it does |
|---|---|
| `streamlit run streamlit_app.py` | The interactive application (`gutoeUIUX.py` is an equivalent shim) |
| `python3 -m toe_math.rg_running` | RG unification analysis + proton lifetime (the quantitative centerpiece) |
| `python3 -m toe_math.gut_embedding` | SU(5)/SO(10) embedding arithmetic |
| `bash paper/build.sh` | Compile the typeset paper to `paper/gutoe.pdf` |
| `python3 -m pytest tests/ -q` | Physics regression tests and app smoke tests |

## Layout

- `toe_math/` — physics computations (`rg_running.py`,
  `gut_embedding.py`, `master_equation.py`; `schumann.py` is a
  classical-EM appendix unrelated to unification)
- `visualization/plotly_4d.py` — interactive 4D figures (projection and
  slicing techniques)
- `docs/` — canonical documentation; start at `docs/index.md`
- `paper/` — the typeset paper
- `unified/`, `core/`, `component_formulas/` — modular formula API
  (legacy layers used by the app's Formulas page)
- `gfx/` — generated graphics (`gfx/rg/` holds the RG figure)
- `docs/legacy/` — pre-2026 documentation, preserved unmodified

## Python API (legacy)

```python
from unified.toe_unified import ToEUnified

api = ToEUnified()
formulas = api.list_formulas()
api.generate_visualization('4d_spacetime_curvature')
```

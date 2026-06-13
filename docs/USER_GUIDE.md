# User Guide

How to install, run, and reproduce everything in this project.

## 1. Installation

Requirements: Python 3.10+, and (only for building the paper) a LaTeX
distribution providing `pdflatex`/`latexmk`.

```bash
git clone https://github.com/GrandUnifiedTheoryOfEverything/gutoe.git
cd gutoe
pip install -r requirements.txt        # Streamlit app only
pip install -r requirements-full.txt   # all three UIs, export, PDF tooling
```

`requirements.txt` is kept minimal on purpose: it is what the deployed
Streamlit Cloud app builds from. The Dash dashboard and NiceGUI Control
Room need `requirements-full.txt`.

## 2. The interactive applications (three deliveries, one physics core)

All three UIs compute from the same modules (`toe_math/`), so they
cannot disagree with each other, the tests, or the paper.

| Delivery | Command | Character |
|---|---|---|
| **Streamlit explorer** | `streamlit run streamlit_app.py` | Page-based reference UI (details below) |
| **Dash dashboard** | `python3 dash_app.py` → port 8050 | Panel layout for side-by-side scientific reading; live RG metrics; two pure-D3.js panels (SVG tesseract you can steer by dragging, force-directed structure map of the composite action) |
| **NiceGUI Control Room** | `python3 nicegui_app.py` → port 8051 | A recursive concept tree: every concept expands into its component parts with increasing complexity, terminating in interactive moments driven by knobs and levers. The Basic/Advanced/Expert menu controls instrumentation depth; Expert mode turns the PDG inputs (α_em⁻¹, sin²θ_W, α_s) into levers for sensitivity exploration |

(`streamlit run gutoeUIUX.py` is an equivalent compatibility entry
point.) The Streamlit app serves these pages:

| Page | Content |
|---|---|
| Home | What the project is (and is not), sample visualization |
| Master Equation | The composite action as a formal Definition, full aligned display, symbol glossary |
| Gauge Unification (RG) | Interactive 1-/2-loop running, $m_{\mathrm{SUSY}}$ slider, $M_{\mathrm{GUT}}$, $\alpha_{\mathrm{GUT}}^{-1}$, proton lifetime vs. Super-K |
| Formulas | The catalog of sector actions with LaTeX rendering |
| Visualizations | Interactive Plotly figures, including the genuine-4D tesseract projection and w-slice animations |
| Documentation | Links to all documents; LaTeX/PDF generation tools |
| Conclusion & Assessment | The honest assessment (renders `docs/CONCLUSION.md`) |
| References & About | Bibliography and project information |

## 3. Reproducing the quantitative results

The two computations behind the Propositions of
[THEORY.md](THEORY.md):

```bash
# RG running, unification scale, proton lifetime (writes figures too)
python3 -m toe_math.rg_running

# SU(5)/SO(10) embedding tables, 5/3 normalization, anomaly sums
python3 -m toe_math.gut_embedding
```

Expected headline output: MSSM two-loop unification at
$M_{\mathrm{GUT}} \approx 1.3\times10^{16}$ GeV with 0.7% mismatch;
SM near-miss at 11–13%; $\tau_p \sim 10^{35\text{–}36}$ yr (MSSM) vs.
the Super-K bound $2.4\times10^{34}$ yr.

Tests:

```bash
python3 -m pytest tests/test_rg_running.py -q
```

## 4. Building the paper

```bash
bash paper/build.sh        # runs latexmk; output: paper/gutoe.pdf
```

If `pdflatex` is not installed: `sudo apt-get install texlive-latex-extra
latexmk` (Debian/Ubuntu), or compile `paper/gutoe.tex` with any LaTeX
toolchain. The RG figure it includes is produced by
`python3 -m toe_math.rg_running`.

## 5. Project layout

```
gutoe/
├── streamlit_app.py        # the interactive application (canonical)
├── gutoeUIUX.py            # compatibility shim for the same app
├── toe_math/               # physics computations
│   ├── rg_running.py       #   RG unification + proton lifetime
│   ├── gut_embedding.py    #   SU(5)/SO(10) group theory
│   ├── master_equation.py  #   formal presentation (single source)
│   ├── toe.py, toe_formulas.py
│   └── schumann.py         #   classical EM appendix (see docs/appendices/)
├── visualization/
│   └── plotly_4d.py        # interactive 4D figures (projection + slicing)
├── docs/                   # canonical documentation (see index.md)
│   ├── THEORY.md, RG_UNIFICATION.md, GUT_EMBEDDING.md
│   ├── CONCLUSION.md, REFERENCES.md
│   ├── appendices/, legacy/
├── paper/                  # the compiled academic paper
├── unified/, core/, component_formulas/   # modular API (legacy layers)
└── gfx/                    # generated graphics (gfx/rg/ holds the RG figure)
```

## 6. Troubleshooting

- **`ModuleNotFoundError: plotly`** — `pip install plotly kaleido`.
- **App starts but a page errors** — run
  `python3 -m pytest tests/test_app_pages.py -q` to localize it.
- **`latexmk: command not found`** — install a LaTeX distribution
  (section 4) or skip the paper; the same content is in `docs/`.
- The legacy PDF-generation agents (`unified/agents/`) are known to be
  fragile with complex math; the supported path to a typeset document is
  `paper/build.sh`. The full pre-2026 user guide (covering the legacy
  exploration scripts) is preserved at
  [legacy/USER_GUIDE.md](legacy/USER_GUIDE.md).

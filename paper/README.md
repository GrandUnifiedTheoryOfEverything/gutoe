# The paper

`gutoe.tex` — *A Computational Framework for the Composite Action of
Fundamental Physics, with a Reproduction of Gauge-Coupling Unification*.

## Build

```bash
# 1. Generate the RG figure (writes paper/figures/rg_unification.pdf)
python3 -m toe_math.rg_running

# 2. Compile (requires pdflatex; latexmk preferred)
bash paper/build.sh        # output: paper/gutoe.pdf
```

If no LaTeX toolchain is installed: `sudo apt-get install
texlive-latex-extra latexmk` (Debian/Ubuntu), or compile `gutoe.tex`
with any LaTeX distribution.

The paper's content mirrors `docs/THEORY.md` (definitions, remark,
propositions, open problems) and `docs/RG_UNIFICATION.md` (methods and
results); the markdown documents are canonical for day-to-day reading,
the paper is the typeset artifact.

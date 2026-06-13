#!/usr/bin/env bash
# Build the GUToE paper. Output: paper/gutoe.pdf
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v latexmk >/dev/null 2>&1; then
    if ! command -v pdflatex >/dev/null 2>&1; then
        echo "No LaTeX toolchain found."
        echo "Install one, e.g.:  sudo apt-get install texlive-latex-extra latexmk"
        echo "Then re-run: bash paper/build.sh"
        exit 0
    fi
    echo "latexmk not found; falling back to two pdflatex passes."
    pdflatex -interaction=nonstopmode gutoe.tex
    pdflatex -interaction=nonstopmode gutoe.tex
else
    latexmk -pdf -interaction=nonstopmode gutoe.tex
fi

echo "Built: $(pwd)/gutoe.pdf"

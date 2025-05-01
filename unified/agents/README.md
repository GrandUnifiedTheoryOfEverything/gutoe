# Theory of Everything - Agents

This directory contains specialized agents for the Theory of Everything package.

## Available Agents

- **LaTeXAgent**: Generates LaTeX documentation for formulas
- **PDFAgent**: Generates PDF documentation for formulas
- **AgentTools**: Core agent functionality

## Usage

### LaTeX Agent

```python
from theoryofeverything.agents import LaTeXAgent

# Create a LaTeX agent
agent = LaTeXAgent(output_dir="gfx/latex")

# Generate LaTeX for a formula
latex = agent.generate_latex(formula="unified_action", include_components=True)

# Save the LaTeX to a file
output_path = agent.save_latex(latex, "unified_action.tex")
```

### PDF Agent

The PDF Agent supports two methods of PDF generation:

1. **LaTeX-based PDF Generation**: When LaTeX (pdflatex) is installed, the PDF agent uses it to generate high-quality PDFs with professional typesetting of mathematical equations.

2. **ReportLab Fallback**: When LaTeX is not available, the PDF agent automatically falls back to using ReportLab with improved equation rendering through Unicode conversion.

```python
from theoryofeverything.agents import PDFAgent

# Create a PDF agent
agent = PDFAgent(output_dir="gfx/pdf")

# Method 1: Generate a PDF directly from a formula
output_path = agent.generate_pdf(
    formula="unified_action",
    output="unified_action.pdf",
    include_components=True,
    include_visualizations=True
)

# Method 2: Generate a PDF from LaTeX content
from theoryofeverything.agents import LaTeXAgent
latex_agent = LaTeXAgent(output_dir="gfx/latex")
latex_content = latex_agent.generate_latex(formula="unified_action")

output_path = agent.generate_pdf_from_latex(
    latex_content=latex_content,
    output="unified_action_from_latex.pdf"
)
```

### Command-line Usage

```bash
# Generate LaTeX documentation
python -m theoryofeverything.agents.latexagent --formula unified_action --output unified_action.tex

# Generate PDF documentation (using LaTeX if available, ReportLab otherwise)
python -m theoryofeverything.agents.pdfagent --formula unified_action --output unified_action.pdf --include-visualizations

# Generate a comprehensive PDF documentation for the entire project
python create_documentation.py  # Creates docs/theory_of_everything_documentation.pdf
```

### Output Directories

By default, the agents output files to the following directories:

- **LaTeX Agent**: `gfx/latex/`
- **PDF Agent**: `gfx/pdf/`

You can specify custom output directories using the `output_dir` parameter when creating the agents or the `--output-dir` command-line argument.

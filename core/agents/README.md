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

```python
from theoryofeverything.agents import PDFAgent

# Create a PDF agent
agent = PDFAgent(output_dir="gfx/pdf")

# Generate a PDF for a formula
output_path = agent.generate_pdf(
    formula="unified_action",
    output="unified_action.pdf",
    include_components=True,
    include_visualizations=True
)
```

### Command-line Usage

```bash
# Generate LaTeX documentation
python -m theoryofeverything.agents.latexagent --formula unified_action --output unified_action.tex

# Generate PDF documentation
python -m theoryofeverything.agents.pdfagent --formula unified_action --output unified_action.pdf --include-visualizations
```

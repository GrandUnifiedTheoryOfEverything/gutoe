# Theory of Everything Package

This directory contains the main Python package for the Theory of Everything.

## Structure

- `__init__.py`: Main package initialization
- `toe_unified.py`: Unified API combining all modules
- `cli.py`: Command-line interface
- `core/`: Core functionality
- `formulas/`: Formula tools
- `visualization/`: Visualization tools
- `agents/`: Specialized agents for LaTeX and PDF generation

## Usage

```python
from theoryofeverything import ToEUnified

# Create an instance of the API
api = ToEUnified()

# List available formulas
formulas = api.list_formulas()

# Generate a visualization
api.generate_visualization('4d_spacetime_curvature')
```

For more detailed usage, see the main README.md file in the project root.

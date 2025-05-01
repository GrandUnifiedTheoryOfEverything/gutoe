# Theory of Everything - Formulas

This directory contains formula tools for the Theory of Everything package.

## Available Formulas

- **Gravity Action**: Einstein-Hilbert action and extensions
- **Matter Action**: Fermion fields and Higgs field
- **Gauge Action**: Yang-Mills action and supersymmetric gauge fields
- **Quantum Corrections**: Path integral formulation and loop corrections
- **Unified Action**: Combined action for the Theory of Everything

## Usage

```python
from theoryofeverything.formulas import FormulaTools

# Create a formula tools instance
formula_tools = FormulaTools()

# List available formulas
formulas = formula_tools.list_formulas()
for name, description in formulas.items():
    print(f"{name}: {description}")

# Get a formula
formula = formula_tools.get_formula('unified_action')
print(formula)

# Explore a formula and its components
exploration = formula_tools.explore_formula('unified_action')
print(exploration)

# Compare formulas
comparison = formula_tools.compare_formulas(['gravity_action', 'matter_action'])
print(comparison)

# Search for formulas
results = formula_tools.search_formulas('quantum')
print(results)

# Export a formula to LaTeX
latex = formula_tools.export_formula_to_latex('unified_action')
print(latex)
```

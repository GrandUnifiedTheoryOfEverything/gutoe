#!/usr/bin/env python3
"""
Test script for the Theory of Everything formula functionality
"""

import os
import sys
import json

# Add the parent directory to the path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the formula module
try:
    from toe_formulas import FormulaTools
    from toe_core import ToECore
    print("Successfully imported FormulaTools")
except ImportError as e:
    print(f"Error importing FormulaTools: {e}")
    sys.exit(1)

# Test the formula functionality
try:
    # Create an instance of the core and formula tools
    core = ToECore(output_dir="tests/formula_output")
    formula_tools = FormulaTools(core=core)
    print("Successfully created FormulaTools instance")
    
    # Test listing formulas
    print("\nTesting formula listing...")
    formulas = formula_tools.list_formulas()
    print(f"Found {len(formulas)} formulas:")
    for name, description in formulas.items():
        print(f"  - {name}: {description}")
    
    # Test getting a formula
    print("\nTesting formula retrieval...")
    for name in formulas:
        formula = formula_tools.get_formula(name)
        print(f"  - {name}: {formula['name']}")
    
    # Test exploring a formula
    print("\nTesting formula exploration...")
    exploration = formula_tools.explore_formula("unified_action")
    print(f"Formula: {exploration['formula']['name']}")
    print("Components:")
    for component in exploration['components']:
        print(f"  - {component['name']}")
    
    # Test comparing formulas
    print("\nTesting formula comparison...")
    comparison = formula_tools.compare_formulas(["gravity_action", "matter_action"])
    print("Common components:")
    for component in comparison.get('common_components', []):
        print(f"  - {component}")
    
    # Test searching formulas
    print("\nTesting formula search...")
    search_results = formula_tools.search_formulas("gravity")
    print(f"Found {len(search_results)} results:")
    for name, score in search_results.items():
        print(f"  - {name} (score: {score})")
    
    # Test getting formula dependencies
    print("\nTesting formula dependencies...")
    dependencies = formula_tools.get_formula_dependencies("unified_action")
    print("Direct dependencies:")
    for dep in dependencies['direct_dependencies']:
        print(f"  - {dep}")
    
    # Test exporting to LaTeX
    print("\nTesting LaTeX export...")
    latex = formula_tools.export_formula_to_latex("unified_action")
    print(f"LaTeX export length: {len(latex)} characters")
    
    print("\nAll tests passed!")
except Exception as e:
    print(f"\nError: {str(e)}")
    sys.exit(1)

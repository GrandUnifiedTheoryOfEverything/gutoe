#!/usr/bin/env python3
"""
Test script for the Theory of Everything LaTeX agent
"""

import os
import sys
import json

# Add the parent directory to the path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the LaTeX agent
try:
    from latexagent import LaTeXAgent
    print("Successfully imported LaTeXAgent")
except ImportError as e:
    print(f"Error importing LaTeXAgent: {e}")
    sys.exit(1)

# Test the LaTeX agent
try:
    # Create an instance of the LaTeX agent
    latex_agent = LaTeXAgent(output_dir="tests/latex_output")
    print("Successfully created LaTeXAgent instance")
    
    # Test generating LaTeX for a formula
    print("\nTesting LaTeX generation for a formula...")
    latex_content = latex_agent.generate_latex("unified_action", include_components=True)
    print(f"Generated LaTeX content length: {len(latex_content)} characters")
    
    # Test saving LaTeX content
    print("\nTesting saving LaTeX content...")
    output_path = latex_agent.save_latex(latex_content, "unified_action_test.tex")
    print(f"LaTeX content saved to: {output_path}")
    
    # Test generating LaTeX for all formulas
    print("\nTesting LaTeX generation for all formulas...")
    all_latex_content = latex_agent.generate_latex(formula=None, include_components=True)
    print(f"Generated LaTeX content length: {len(all_latex_content)} characters")
    
    # Test saving all LaTeX content
    print("\nTesting saving all LaTeX content...")
    all_output_path = latex_agent.save_latex(all_latex_content, "all_formulas_test.tex")
    print(f"All LaTeX content saved to: {all_output_path}")
    
    print("\nAll tests passed!")
except Exception as e:
    print(f"\nError: {str(e)}")
    sys.exit(1)

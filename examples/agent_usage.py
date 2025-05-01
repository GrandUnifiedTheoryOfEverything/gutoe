#!/usr/bin/env python3
"""
Agent usage example for the Theory of Everything
"""

import os
import sys
import json

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from theoryofeverything import ToEUnified, LaTeXAgent, PDFAgent

def main():
    """Main function"""
    # Create an instance of the API with agent mode enabled
    api = ToEUnified(agent_mode=True)

    # Explore the Theory of Everything
    print("Exploring the Theory of Everything...")
    exploration = api.explore_theory()
    print(json.dumps(exploration, indent=2))

    # Generate a visualization for a formula
    print("\nGenerating a visualization for a formula...")
    result = api.generate_visualization_for_formula("gravity_action")
    print(json.dumps(result, indent=2))

    # Extract insights
    print("\nExtracting insights...")
    insights = api.extract_insights(formula_name="gravity_action")
    print(json.dumps(insights, indent=2))

    # Generate LaTeX documentation
    print("\nGenerating LaTeX documentation...")
    latex_agent = LaTeXAgent()
    latex_content = latex_agent.generate_latex(formula="unified_action", include_components=True)
    latex_file = latex_agent.save_latex(latex_content, "gfx/latex/unified_action.tex")
    print(f"LaTeX file saved to: {latex_file}")

    # Generate PDF documentation
    print("\nGenerating PDF documentation...")
    pdf_agent = PDFAgent()
    pdf_file = pdf_agent.generate_pdf(formula="unified_action", output="gfx/pdf/unified_action.pdf", include_visualizations=True)
    print(f"PDF file saved to: {pdf_file}")

    print("\nDone!")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test script for the LaTeX agent
"""

import os
import sys
sys.path.append('.')
from unified.agents.latexagent import LaTeXAgent

def test_latex_agent():
    """Test the LaTeX agent functionality"""
    print("Testing LaTeX Agent...")

    # Create the LaTeX agent
    latex_agent = LaTeXAgent(output_dir="gfx/latex")

    # Test template loading
    templates = latex_agent._load_templates()
    if not templates:
        print("❌ Failed to load templates")
        return False

    print(f"✅ Successfully loaded {len(templates)} templates")

    # Test LaTeX generation for a simple formula
    formula_name = "unified_action"

    # Note: The LaTeX agent gets formula data from the formula tools
    # We're just testing the method call here
    latex_content = latex_agent.generate_latex(formula=formula_name, include_components=False)
    if not latex_content:
        print("❌ Failed to generate LaTeX content")
        return False

    print("✅ Successfully generated LaTeX content")

    # Test saving LaTeX to a file
    output_file = latex_agent.save_latex(latex_content, f"{formula_name}_test.tex")
    if not output_file or not os.path.exists(output_file):
        print(f"❌ Failed to save LaTeX file: {output_file}")
        return False

    print(f"✅ Successfully saved LaTeX file: {output_file}")

    # Test LaTeX generation with components
    latex_content_with_components = latex_agent.generate_latex(
        formula=formula_name,
        include_components=True
    )

    if not latex_content_with_components:
        print("❌ Failed to generate LaTeX content with components")
        return False

    print("✅ Successfully generated LaTeX content with components")

    # Test saving LaTeX with components to a file
    output_file_with_components = latex_agent.save_latex(
        latex_content_with_components,
        f"{formula_name}_with_components_test.tex"
    )

    if not output_file_with_components or not os.path.exists(output_file_with_components):
        print(f"❌ Failed to save LaTeX file with components: {output_file_with_components}")
        return False

    print(f"✅ Successfully saved LaTeX file with components: {output_file_with_components}")

    print("All LaTeX agent tests passed!")
    return True

if __name__ == "__main__":
    # Create output directory if it doesn't exist
    os.makedirs("gfx/latex", exist_ok=True)

    # Run the test
    success = test_latex_agent()

    # Exit with appropriate status code
    sys.exit(0 if success else 1)

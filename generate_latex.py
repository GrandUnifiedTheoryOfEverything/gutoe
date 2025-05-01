#!/usr/bin/env python3
"""
Generate a LaTeX file with a known formula
"""

import os
import json
from unified.agents.latexagent import LaTeXAgent

def main():
    """Main function"""
    # Create the output directories
    os.makedirs("gfx/latex", exist_ok=True)
    os.makedirs("gfx/pdf", exist_ok=True)
    
    # Create a formula
    formula_name = "unified_action"
    formula_data = {
        "name": "Unified Action (Master Equation)",
        "description": "The total action is composed of four main parts: gravity, matter, gauge fields, and quantum corrections.",
        "latex": "S=S_{gravity}+S_{matter}+S_{gauge}+S_{quantum}",
        "components": [
            {
                "name": "Gravity Action",
                "latex": "S_{gravity} = \\frac{1}{16\\pi G} \\int d^4x \\, \\sqrt{-g} \\, (R - 2\\Lambda)",
                "description": "The Einstein-Hilbert action describes classical gravity in terms of spacetime curvature."
            },
            {
                "name": "Matter Action",
                "latex": "S_{matter} = \\int d^4x \\, \\sqrt{-g} \\, \\bar{\\psi} (i \\gamma^\\mu D_\\mu - m) \\psi",
                "description": "The Dirac action describes fermions (matter particles) in curved spacetime."
            }
        ]
    }
    
    # Create the LaTeX agent
    latex_agent = LaTeXAgent(output_dir="gfx/latex")
    
    # Generate LaTeX content
    latex_content = f"""
\\documentclass{{article}}
\\usepackage{{amsmath}}
\\usepackage{{amssymb}}
\\usepackage{{amsfonts}}
\\begin{{document}}

\\section*{{{formula_data['name']}}}

{formula_data['description']}

\\begin{{align}}
{formula_data['latex']}
\\end{{align}}

\\section*{{Components}}

"""
    
    for component in formula_data['components']:
        latex_content += f"""
\\subsection*{{{component['name']}}}

{component['description']}

\\begin{{align}}
{component['latex']}
\\end{{align}}
"""
    
    latex_content += "\\end{document}"
    
    # Save the LaTeX content to a file
    output_file = latex_agent.save_latex(latex_content, f"{formula_name}_direct.tex")
    print(f"LaTeX file saved to: {output_file}")
    
    # Check if the file exists
    if os.path.exists(output_file):
        print(f"File size: {os.path.getsize(output_file)} bytes")
        with open(output_file, 'r') as f:
            print(f"First 100 characters: {f.read(100)}")
    else:
        print(f"Error: File not found: {output_file}")

if __name__ == "__main__":
    main()

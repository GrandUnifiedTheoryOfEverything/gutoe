#!/usr/bin/env python3
"""
Generate a PDF file with a known formula
"""

import os
import sys
import importlib.util
from unified.agents.pdfagent import PDFAgent
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
    latex_file = latex_agent.save_latex(latex_content, f"{formula_name}_direct.tex")
    print(f"LaTeX file saved to: {latex_file}")
    
    # Create the PDF agent
    pdf_agent = PDFAgent(output_dir="gfx/pdf")
    
    # Generate PDF from LaTeX content
    pdf_file = pdf_agent.generate_pdf_from_latex(latex_content=latex_content, output=f"gfx/pdf/{formula_name}_direct.pdf")
    print(f"PDF file saved to: {pdf_file}")
    
    # Check if the file exists
    if pdf_file.startswith("Error:"):
        print(f"Error generating PDF: {pdf_file}")
    elif os.path.exists(pdf_file):
        print(f"PDF file size: {os.path.getsize(pdf_file)} bytes")
    else:
        print(f"Error: PDF file not found: {pdf_file}")

if __name__ == "__main__":
    main()

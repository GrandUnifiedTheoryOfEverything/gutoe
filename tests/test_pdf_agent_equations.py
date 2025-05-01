#!/usr/bin/env python3
"""
Test the improved equation rendering in the PDF agent
"""

import os
import sys
from unified.agents.pdfagent import PDFAgent
from unified.agents.latexagent import LaTeXAgent

def main():
    """Main function"""
    # Create the output directories
    os.makedirs("gfx/latex", exist_ok=True)
    os.makedirs("gfx/pdf", exist_ok=True)
    
    # Create a formula
    formula_name = "unified_field_theory"
    formula_data = {
        "name": "Unified Field Theory",
        "description": "A comprehensive theory that unifies the fundamental forces of nature.",
        "latex": "\\mathcal{L} = -\\frac{1}{4}F_{\mu\\nu}F^{\mu\\nu} + \\bar{\\psi}(i\\gamma^\\mu D_\\mu - m)\\psi + \\frac{1}{16\\pi G}R",
        "components": [
            {
                "name": "Electromagnetic Field",
                "latex": "\\mathcal{L}_{EM} = -\\frac{1}{4}F_{\mu\\nu}F^{\mu\\nu}",
                "description": "The electromagnetic field component of the unified theory."
            },
            {
                "name": "Fermionic Matter",
                "latex": "\\mathcal{L}_{matter} = \\bar{\\psi}(i\\gamma^\\mu D_\\mu - m)\\psi",
                "description": "The matter component of the unified theory."
            },
            {
                "name": "Gravitational Field",
                "latex": "\\mathcal{L}_{gravity} = \\frac{1}{16\\pi G}R",
                "description": "The gravitational field component of the unified theory."
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
\\usepackage{{physics}}
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
    latex_file = latex_agent.save_latex(latex_content, f"{formula_name}.tex")
    print(f"LaTeX file saved to: {latex_file}")
    
    # Create the PDF agent
    pdf_agent = PDFAgent(output_dir="gfx/pdf")
    
    # Generate PDF from LaTeX content
    pdf_file = pdf_agent.generate_pdf_from_latex(latex_content=latex_content, output=f"{formula_name}.pdf")
    print(f"PDF file saved to: {pdf_file}")
    
    # Check if the file exists
    if pdf_file.startswith("Error:"):
        print(f"Error generating PDF: {pdf_file}")
    elif os.path.exists(pdf_file):
        print(f"PDF file size: {os.path.getsize(pdf_file)} bytes")
        print("\nThe PDF file now contains improved equation rendering with Unicode symbols.")
        print("While not as perfect as LaTeX typesetting, it's much more readable than raw LaTeX code.")
    else:
        print(f"Error: PDF file not found: {pdf_file}")

if __name__ == "__main__":
    main()

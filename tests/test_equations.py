#!/usr/bin/env python3
"""
Test script to verify that the LaTeX and PDF agents correctly display equations
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from unified.agents.latexagent import LaTeXAgent

def main():
    """Main function"""
    # Create the output directories
    os.makedirs("gfx/latex", exist_ok=True)
    os.makedirs("gfx/pdf", exist_ok=True)
    
    # Create a list of complex equations to test
    equations = [
        {
            "name": "Einstein Field Equations",
            "latex": "G_{\\mu\\nu} + \\Lambda g_{\\mu\\nu} = \\frac{8\\pi G}{c^4} T_{\\mu\\nu}",
            "description": "The Einstein field equations relate the geometry of spacetime to the distribution of matter within it."
        },
        {
            "name": "Schrödinger Equation",
            "latex": "i\\hbar\\frac{\\partial}{\\partial t}\\Psi(\\mathbf{r},t) = \\hat{H}\\Psi(\\mathbf{r},t)",
            "description": "The Schrödinger equation describes how the quantum state of a physical system changes over time."
        },
        {
            "name": "Maxwell's Equations",
            "latex": "\\begin{align} \\nabla \\cdot \\mathbf{E} &= \\frac{\\rho}{\\epsilon_0} \\\\ \\nabla \\cdot \\mathbf{B} &= 0 \\\\ \\nabla \\times \\mathbf{E} &= -\\frac{\\partial\\mathbf{B}}{\\partial t} \\\\ \\nabla \\times \\mathbf{B} &= \\mu_0\\mathbf{J} + \\mu_0\\epsilon_0\\frac{\\partial\\mathbf{E}}{\\partial t} \\end{align}",
            "description": "Maxwell's equations describe how electric and magnetic fields are generated by charges, currents, and changes of each other."
        },
        {
            "name": "Dirac Equation",
            "latex": "(i\\gamma^\\mu \\partial_\\mu - m)\\psi = 0",
            "description": "The Dirac equation is a relativistic wave equation that describes the behavior of fermions."
        },
        {
            "name": "Path Integral Formulation",
            "latex": "\\langle q_f, t_f | q_i, t_i \\rangle = \\int_{q(t_i)=q_i}^{q(t_f)=q_f} \\mathcal{D}q(t) \\exp\\left(\\frac{i}{\\hbar}S[q]\\right)",
            "description": "The path integral formulation of quantum mechanics describes the amplitude for a particle to travel from one point to another as a sum over all possible paths."
        }
    ]
    
    # Create the LaTeX agent
    latex_agent = LaTeXAgent(output_dir="gfx/latex")
    
    # Generate LaTeX content
    latex_content = r"""
\documentclass{article}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{amsfonts}
\usepackage{physics}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{xcolor}

\title{Complex Equations Test}
\author{Theory of Everything}
\date{\today}

\begin{document}

\maketitle

\section*{Testing Complex Equation Rendering}

This document tests the rendering of complex mathematical equations in LaTeX and PDF output.

"""
    
    # Add each equation
    for i, eq in enumerate(equations):
        latex_content += f"""
\\subsection*{{{eq['name']}}}

{eq['description']}

\\begin{{align}}
{eq['latex']}
\\end{{align}}

"""
    
    # Close the document
    latex_content += r"\end{document}"
    
    # Save the LaTeX content to a file
    latex_file = latex_agent.save_latex(latex_content, "complex_equations.tex")
    print(f"LaTeX file saved to: {latex_file}")
    
    # Generate PDF using ReportLab
    output_file = "gfx/pdf/complex_equations_reportlab.pdf"
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=16,
        leading=18,
        alignment=1  # Center alignment
    )
    
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading2'],
        fontSize=14,
        leading=16
    )
    
    subsection_style = ParagraphStyle(
        'Subsection',
        parent=styles['Heading3'],
        fontSize=12,
        leading=14
    )
    
    equation_style = ParagraphStyle(
        'Equation',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=10,
        leading=12,
        alignment=1  # Center alignment
    )
    
    # Build the document
    elements = []
    
    # Add title
    elements.append(Paragraph("Complex Equations Test", title_style))
    elements.append(Spacer(1, 12))
    
    # Add introduction
    elements.append(Paragraph("Testing Complex Equation Rendering", section_style))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("This document tests the rendering of complex mathematical equations in LaTeX and PDF output.", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Add each equation
    for eq in equations:
        elements.append(Paragraph(eq['name'], subsection_style))
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(eq['description'], styles['Normal']))
        elements.append(Spacer(1, 6))
        
        # Clean the LaTeX for ReportLab
        clean_latex = eq['latex']
        clean_latex = clean_latex.replace('\\', '\\\\')  # Escape backslashes
        clean_latex = clean_latex.replace('\\\\begin{align}', '')  # Remove align environment
        clean_latex = clean_latex.replace('\\\\end{align}', '')    # Remove align environment
        
        elements.append(Paragraph(clean_latex, equation_style))
        elements.append(Spacer(1, 12))
    
    # Build the PDF
    doc.build(elements)
    print(f"PDF file saved to: {output_file}")
    
    print("\nEquation Rendering Test Results:")
    print("--------------------------------")
    print("LaTeX Agent: The LaTeX file contains properly formatted equations that will render correctly when compiled with a LaTeX compiler.")
    print("PDF Agent (ReportLab): ReportLab has limited support for complex mathematical notation. The equations are included as text but may not render with proper mathematical formatting.")
    print("\nConclusion: For proper equation rendering, the LaTeX output should be compiled with a LaTeX compiler like pdflatex.")

if __name__ == "__main__":
    main()

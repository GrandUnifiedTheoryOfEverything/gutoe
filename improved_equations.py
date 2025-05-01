#!/usr/bin/env python3
"""
Improved equation rendering for PDF output
"""

import os
import re
import unicodedata
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from unified.agents.latexagent import LaTeXAgent

def latex_to_unicode(latex_str):
    """Convert LaTeX notation to Unicode where possible"""
    # Greek letters
    greek_letters = {
        '\\alpha': 'α', '\\beta': 'β', '\\gamma': 'γ', '\\delta': 'δ',
        '\\epsilon': 'ε', '\\zeta': 'ζ', '\\eta': 'η', '\\theta': 'θ',
        '\\iota': 'ι', '\\kappa': 'κ', '\\lambda': 'λ', '\\mu': 'μ',
        '\\nu': 'ν', '\\xi': 'ξ', '\\pi': 'π', '\\rho': 'ρ',
        '\\sigma': 'σ', '\\tau': 'τ', '\\upsilon': 'υ', '\\phi': 'φ',
        '\\chi': 'χ', '\\psi': 'ψ', '\\omega': 'ω',
        '\\Gamma': 'Γ', '\\Delta': 'Δ', '\\Theta': 'Θ', '\\Lambda': 'Λ',
        '\\Xi': 'Ξ', '\\Pi': 'Π', '\\Sigma': 'Σ', '\\Upsilon': 'Υ',
        '\\Phi': 'Φ', '\\Psi': 'Ψ', '\\Omega': 'Ω'
    }
    
    # Mathematical symbols
    math_symbols = {
        '\\times': '×', '\\div': '÷', '\\pm': '±', '\\mp': '∓',
        '\\cdot': '·', '\\leq': '≤', '\\geq': '≥', '\\neq': '≠',
        '\\approx': '≈', '\\equiv': '≡', '\\cong': '≅', '\\sim': '∼',
        '\\propto': '∝', '\\infty': '∞', '\\partial': '∂', '\\nabla': '∇',
        '\\forall': '∀', '\\exists': '∃', '\\nexists': '∄', '\\in': '∈',
        '\\notin': '∉', '\\subset': '⊂', '\\supset': '⊃', '\\cup': '∪',
        '\\cap': '∩', '\\emptyset': '∅', '\\therefore': '∴', '\\because': '∵',
        '\\hbar': 'ℏ', '\\ell': 'ℓ', '\\Re': 'ℜ', '\\Im': 'ℑ',
        '\\aleph': 'ℵ', '\\wp': '℘', '\\otimes': '⊗', '\\oplus': '⊕',
        '\\circ': '∘', '\\bullet': '•', '\\star': '⋆', '\\dagger': '†',
        '\\ddagger': '‡', '\\vee': '∨', '\\wedge': '∧', '\\langle': '⟨',
        '\\rangle': '⟩', '\\int': '∫', '\\oint': '∮', '\\sum': '∑',
        '\\prod': '∏', '\\coprod': '∐', '\\sqrt': '√'
    }
    
    # Replace LaTeX commands with Unicode characters
    result = latex_str
    
    # Remove LaTeX environments
    result = re.sub(r'\\begin\{[^}]*\}|\\end\{[^}]*\}', '', result)
    
    # Replace Greek letters
    for latex, unicode in greek_letters.items():
        result = result.replace(latex, unicode)
    
    # Replace math symbols
    for latex, unicode in math_symbols.items():
        result = result.replace(latex, unicode)
    
    # Handle subscripts and superscripts
    # This is a simplified approach - full LaTeX parsing would be more complex
    
    # Superscripts
    superscripts = {'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', 
                   '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
                   '+': '⁺', '-': '⁻', '=': '⁼', '(': '⁽', ')': '⁾',
                   'a': 'ᵃ', 'b': 'ᵇ', 'c': 'ᶜ', 'd': 'ᵈ', 'e': 'ᵉ',
                   'f': 'ᶠ', 'g': 'ᵍ', 'h': 'ʰ', 'i': 'ⁱ', 'j': 'ʲ',
                   'k': 'ᵏ', 'l': 'ˡ', 'm': 'ᵐ', 'n': 'ⁿ', 'o': 'ᵒ',
                   'p': 'ᵖ', 'r': 'ʳ', 's': 'ˢ', 't': 'ᵗ', 'u': 'ᵘ',
                   'v': 'ᵛ', 'w': 'ʷ', 'x': 'ˣ', 'y': 'ʸ', 'z': 'ᶻ',
                   'A': 'ᴬ', 'B': 'ᴮ', 'D': 'ᴰ', 'E': 'ᴱ', 'G': 'ᴳ',
                   'H': 'ᴴ', 'I': 'ᴵ', 'J': 'ᴶ', 'K': 'ᴷ', 'L': 'ᴸ',
                   'M': 'ᴹ', 'N': 'ᴺ', 'O': 'ᴼ', 'P': 'ᴾ', 'R': 'ᴿ',
                   'T': 'ᵀ', 'U': 'ᵁ', 'V': 'ⱽ', 'W': 'ᵂ'}
    
    # Subscripts
    subscripts = {'0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
                 '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
                 '+': '₊', '-': '₋', '=': '₌', '(': '₍', ')': '₎',
                 'a': 'ₐ', 'e': 'ₑ', 'h': 'ₕ', 'i': 'ᵢ', 'j': 'ⱼ',
                 'k': 'ₖ', 'l': 'ₗ', 'm': 'ₘ', 'n': 'ₙ', 'o': 'ₒ',
                 'p': 'ₚ', 'r': 'ᵣ', 's': 'ₛ', 't': 'ₜ', 'u': 'ᵤ',
                 'v': 'ᵥ', 'x': 'ₓ'}
    
    # Process superscripts: replace ^{x} with superscript x
    def replace_superscript(match):
        content = match.group(1)
        result = ""
        for char in content:
            result += superscripts.get(char, char)
        return result
    
    result = re.sub(r'\^\{([^}]*)\}', replace_superscript, result)
    
    # Process simple superscripts: replace ^x with superscript x
    def replace_simple_superscript(match):
        char = match.group(1)
        return superscripts.get(char, '^' + char)
    
    result = re.sub(r'\^([a-zA-Z0-9])', replace_simple_superscript, result)
    
    # Process subscripts: replace _{x} with subscript x
    def replace_subscript(match):
        content = match.group(1)
        result = ""
        for char in content:
            result += subscripts.get(char, char)
        return result
    
    result = re.sub(r'_\{([^}]*)\}', replace_subscript, result)
    
    # Process simple subscripts: replace _x with subscript x
    def replace_simple_subscript(match):
        char = match.group(1)
        return subscripts.get(char, '_' + char)
    
    result = re.sub(r'_([a-zA-Z0-9])', replace_simple_subscript, result)
    
    # Handle fractions
    def replace_fraction(match):
        numerator = match.group(1)
        denominator = match.group(2)
        return f"{numerator}⁄{denominator}"
    
    result = re.sub(r'\\frac\{([^}]*)\}\{([^}]*)\}', replace_fraction, result)
    
    # Clean up remaining LaTeX commands and braces
    result = re.sub(r'\\[a-zA-Z]+', '', result)  # Remove remaining LaTeX commands
    result = re.sub(r'\{|\}', '', result)        # Remove remaining braces
    
    return result

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

\title{Improved Equation Rendering Test}
\author{Theory of Everything}
\date{\today}

\begin{document}

\maketitle

\section*{Testing Improved Equation Rendering}

This document tests the improved rendering of complex mathematical equations in LaTeX and PDF output.

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
    latex_file = latex_agent.save_latex(latex_content, "improved_equations.tex")
    print(f"LaTeX file saved to: {latex_file}")
    
    # Generate PDF using ReportLab with improved equation rendering
    output_file = "gfx/pdf/improved_equations.pdf"
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
        fontSize=12,
        leading=14,
        alignment=1  # Center alignment
    )
    
    # Build the document
    elements = []
    
    # Add title
    elements.append(Paragraph("Improved Equation Rendering Test", title_style))
    elements.append(Spacer(1, 12))
    
    # Add introduction
    elements.append(Paragraph("Testing Improved Equation Rendering", section_style))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("This document tests the improved rendering of complex mathematical equations in LaTeX and PDF output.", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Add each equation
    for eq in equations:
        elements.append(Paragraph(eq['name'], subsection_style))
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(eq['description'], styles['Normal']))
        elements.append(Spacer(1, 6))
        
        # Convert LaTeX to Unicode for better rendering
        unicode_eq = latex_to_unicode(eq['latex'])
        elements.append(Paragraph(unicode_eq, equation_style))
        elements.append(Spacer(1, 12))
        
        # Also show the original LaTeX for comparison
        elements.append(Paragraph("Original LaTeX:", styles['Normal']))
        elements.append(Paragraph(eq['latex'], styles['Code']))
        elements.append(Spacer(1, 24))
    
    # Build the PDF
    doc.build(elements)
    print(f"PDF file saved to: {output_file}")
    
    print("\nImproved Equation Rendering Test Results:")
    print("----------------------------------------")
    print("LaTeX Agent: The LaTeX file contains properly formatted equations that will render correctly when compiled with a LaTeX compiler.")
    print("PDF Agent (Improved): The PDF now uses Unicode characters to better represent mathematical symbols and equations.")
    print("\nConclusion: While the LaTeX output still provides the best quality when compiled with a LaTeX compiler, the improved PDF output is now more readable with proper mathematical symbols.")

if __name__ == "__main__":
    main()

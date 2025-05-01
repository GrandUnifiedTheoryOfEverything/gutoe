#!/usr/bin/env python3
"""
Test the LaTeX to Unicode converter
"""

import os
import sys
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

# LaTeX to Unicode converter
def latex_to_unicode(latex_str):
    """
    Convert LaTeX notation to Unicode for better readability
    """
    # Greek letters (lowercase and uppercase)
    greek_map = {
        '\\alpha': 'α', '\\beta': 'β', '\\gamma': 'γ', '\\delta': 'δ',
        '\\epsilon': 'ε', '\\varepsilon': 'ε', '\\zeta': 'ζ', '\\eta': 'η', 
        '\\theta': 'θ', '\\vartheta': 'ϑ', '\\iota': 'ι', '\\kappa': 'κ',
        '\\lambda': 'λ', '\\mu': 'μ', '\\nu': 'ν', '\\xi': 'ξ', '\\pi': 'π',
        '\\varpi': 'ϖ', '\\rho': 'ρ', '\\varrho': 'ϱ', '\\sigma': 'σ',
        '\\varsigma': 'ς', '\\tau': 'τ', '\\upsilon': 'υ', '\\phi': 'φ',
        '\\varphi': 'φ', '\\chi': 'χ', '\\psi': 'ψ', '\\omega': 'ω',
        '\\Gamma': 'Γ', '\\Delta': 'Δ', '\\Theta': 'Θ', '\\Lambda': 'Λ',
        '\\Xi': 'Ξ', '\\Pi': 'Π', '\\Sigma': 'Σ', '\\Upsilon': 'Υ',
        '\\Phi': 'Φ', '\\Psi': 'Ψ', '\\Omega': 'Ω'
    }
    
    # Mathematical operators and symbols
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
        '\\prod': '∏', '\\coprod': '∐', '\\sqrt': '√', '\\surd': '√',
        '\\top': '⊤', '\\bot': '⊥', '\\|': '‖', '\\angle': '∠',
        '\\triangle': '△', '\\backslash': '\\', '\\prime': '′',
        '\\rightarrow': '→', '\\leftarrow': '←', '\\leftrightarrow': '↔',
        '\\Rightarrow': '⇒', '\\Leftarrow': '⇐', '\\Leftrightarrow': '⇔',
        '\\uparrow': '↑', '\\downarrow': '↓', '\\updownarrow': '↕',
        '\\mapsto': '↦', '\\to': '→', '\\perp': '⊥'
    }
    
    # Clean up the LaTeX string
    result = latex_str
    
    # Remove LaTeX environments
    result = re.sub(r'\\begin\{[^}]*\}|\\end\{[^}]*\}', '', result)
    
    # Replace alignment markers in equations
    result = result.replace('&=', '=').replace('&', '')
    
    # Replace line breaks in equations
    result = result.replace('\\\\', ', ')
    
    # Replace Greek letters
    for latex, unicode in greek_map.items():
        result = result.replace(latex, unicode)
    
    # Replace math symbols
    for latex, unicode in math_symbols.items():
        result = result.replace(latex, unicode)
    
    # Handle superscripts and subscripts
    # Superscripts
    superscripts = {
        '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵',
        '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹', '+': '⁺', '-': '⁻',
        '=': '⁼', '(': '⁽', ')': '⁾', 'i': 'ⁱ', 'n': 'ⁿ',
        'a': 'ᵃ', 'b': 'ᵇ', 'c': 'ᶜ', 'd': 'ᵈ', 'e': 'ᵉ', 'f': 'ᶠ',
        'g': 'ᵍ', 'h': 'ʰ', 'j': 'ʲ', 'k': 'ᵏ', 'l': 'ˡ', 'm': 'ᵐ',
        'o': 'ᵒ', 'p': 'ᵖ', 'r': 'ʳ', 's': 'ˢ', 't': 'ᵗ', 'u': 'ᵘ',
        'v': 'ᵛ', 'w': 'ʷ', 'x': 'ˣ', 'y': 'ʸ', 'z': 'ᶻ'
    }
    
    # Subscripts
    subscripts = {
        '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄', '5': '₅',
        '6': '₆', '7': '₇', '8': '₈', '9': '₉', '+': '₊', '-': '₋',
        '=': '₌', '(': '₍', ')': '₎', 'a': 'ₐ', 'e': 'ₑ', 'i': 'ᵢ',
        'j': 'ⱼ', 'o': 'ₒ', 'r': 'ᵣ', 'u': 'ᵤ', 'v': 'ᵥ', 'x': 'ₓ'
    }
    
    # Process superscripts with braces: ^{...}
    def replace_superscript(match):
        content = match.group(1)
        result = ""
        for char in content:
            result += superscripts.get(char, char)
        return result
    
    result = re.sub(r'\^\{([^{}]*)\}', replace_superscript, result)
    
    # Process simple superscripts: ^x
    def replace_simple_superscript(match):
        char = match.group(1)
        return superscripts.get(char, '^' + char)
    
    result = re.sub(r'\^([a-zA-Z0-9])', replace_simple_superscript, result)
    
    # Process subscripts with braces: _{...}
    def replace_subscript(match):
        content = match.group(1)
        result = ""
        for char in content:
            result += subscripts.get(char, char)
        return result
    
    result = re.sub(r'_\{([^{}]*)\}', replace_subscript, result)
    
    # Process simple subscripts: _x
    def replace_simple_subscript(match):
        char = match.group(1)
        return subscripts.get(char, '_' + char)
    
    result = re.sub(r'_([a-zA-Z0-9])', replace_simple_subscript, result)
    
    # Handle fractions
    def replace_fraction(match):
        numerator = match.group(1)
        denominator = match.group(2)
        return f"({numerator})⁄({denominator})"
    
    result = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', replace_fraction, result)
    
    # Handle nested fractions
    while '\\frac{' in result:
        result = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', replace_fraction, result)
    
    # Handle square roots
    def replace_sqrt(match):
        content = match.group(1)
        return f"√({content})"
    
    result = re.sub(r'\\sqrt\{([^{}]*)\}', replace_sqrt, result)
    
    # Clean up remaining LaTeX commands and braces
    result = re.sub(r'\\[a-zA-Z]+', '', result)  # Remove remaining LaTeX commands
    result = re.sub(r'\{|\}', '', result)        # Remove remaining braces
    
    return result

def main():
    """Test the LaTeX to Unicode converter and generate a PDF with improved equation rendering"""
    # Create the output directory
    os.makedirs("gfx/pdf", exist_ok=True)
    
    # Define some complex equations to test
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
        },
        {
            "name": "Unified Field Theory",
            "latex": "\\mathcal{L} = -\\frac{1}{4}F_{\\mu\\nu}F^{\\mu\\nu} + \\bar{\\psi}(i\\gamma^\\mu D_\\mu - m)\\psi + \\frac{1}{16\\pi G}R",
            "description": "A comprehensive theory that unifies the fundamental forces of nature."
        }
    ]
    
    # Print the LaTeX to Unicode conversion results
    print("LaTeX to Unicode Conversion Examples")
    print("====================================")
    print()
    
    for eq in equations:
        print(f"Equation: {eq['name']}")
        print(f"Description: {eq['description']}")
        print(f"LaTeX: {eq['latex']}")
        unicode_eq = latex_to_unicode(eq['latex'])
        print(f"Unicode: {unicode_eq}")
        print()
    
    # Create a PDF document with the converted equations
    output_file = "gfx/pdf/improved_equations.pdf"
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=16,
        leading=18,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=14,
        leading=16
    )
    
    equation_style = ParagraphStyle(
        'Equation',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=12,
        leading=14,
        alignment=TA_CENTER
    )
    
    # Build the document
    elements = []
    
    # Add title
    elements.append(Paragraph("Improved Mathematical Equation Rendering", title_style))
    elements.append(Spacer(1, 12))
    
    # Add introduction
    elements.append(Paragraph("This document demonstrates improved rendering of complex mathematical equations in PDF output using Unicode conversion.", styles['Normal']))
    elements.append(Spacer(1, 24))
    
    # Process each equation
    for eq in equations:
        # Add equation name
        elements.append(Paragraph(eq['name'], heading_style))
        elements.append(Spacer(1, 6))
        
        # Add description
        elements.append(Paragraph(eq['description'], styles['Normal']))
        elements.append(Spacer(1, 6))
        
        # Add original LaTeX
        elements.append(Paragraph("LaTeX:", styles['Normal']))
        elements.append(Paragraph(eq['latex'], styles['Code']))
        elements.append(Spacer(1, 6))
        
        # Add improved Unicode rendering
        elements.append(Paragraph("Improved Rendering:", styles['Normal']))
        unicode_eq = latex_to_unicode(eq['latex'])
        elements.append(Paragraph(unicode_eq, equation_style))
        elements.append(Spacer(1, 24))
    
    # Build the PDF
    try:
        doc.build(elements)
        print(f"PDF with improved equation rendering saved to: {output_file}")
        print(f"File size: {os.path.getsize(output_file)} bytes")
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
    
    print("\nThe improved LaTeX to Unicode conversion provides better rendering of complex mathematical equations.")

if __name__ == "__main__":
    main()

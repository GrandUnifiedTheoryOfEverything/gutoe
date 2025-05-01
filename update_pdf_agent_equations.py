#!/usr/bin/env python3
"""
Update the PDF agent to use improved equation rendering
"""

import os
import sys
import re

def main():
    """Main function"""
    # Create the latex_to_unicode function
    latex_to_unicode_code = """
def latex_to_unicode(latex_str):
    \"\"\"Convert LaTeX notation to Unicode where possible\"\"\"
    # Greek letters
    greek_letters = {
        '\\\\alpha': 'α', '\\\\beta': 'β', '\\\\gamma': 'γ', '\\\\delta': 'δ',
        '\\\\epsilon': 'ε', '\\\\zeta': 'ζ', '\\\\eta': 'η', '\\\\theta': 'θ',
        '\\\\iota': 'ι', '\\\\kappa': 'κ', '\\\\lambda': 'λ', '\\\\mu': 'μ',
        '\\\\nu': 'ν', '\\\\xi': 'ξ', '\\\\pi': 'π', '\\\\rho': 'ρ',
        '\\\\sigma': 'σ', '\\\\tau': 'τ', '\\\\upsilon': 'υ', '\\\\phi': 'φ',
        '\\\\chi': 'χ', '\\\\psi': 'ψ', '\\\\omega': 'ω',
        '\\\\Gamma': 'Γ', '\\\\Delta': 'Δ', '\\\\Theta': 'Θ', '\\\\Lambda': 'Λ',
        '\\\\Xi': 'Ξ', '\\\\Pi': 'Π', '\\\\Sigma': 'Σ', '\\\\Upsilon': 'Υ',
        '\\\\Phi': 'Φ', '\\\\Psi': 'Ψ', '\\\\Omega': 'Ω'
    }
    
    # Mathematical symbols
    math_symbols = {
        '\\\\times': '×', '\\\\div': '÷', '\\\\pm': '±', '\\\\mp': '∓',
        '\\\\cdot': '·', '\\\\leq': '≤', '\\\\geq': '≥', '\\\\neq': '≠',
        '\\\\approx': '≈', '\\\\equiv': '≡', '\\\\cong': '≅', '\\\\sim': '∼',
        '\\\\propto': '∝', '\\\\infty': '∞', '\\\\partial': '∂', '\\\\nabla': '∇',
        '\\\\forall': '∀', '\\\\exists': '∃', '\\\\nexists': '∄', '\\\\in': '∈',
        '\\\\notin': '∉', '\\\\subset': '⊂', '\\\\supset': '⊃', '\\\\cup': '∪',
        '\\\\cap': '∩', '\\\\emptyset': '∅', '\\\\therefore': '∴', '\\\\because': '∵',
        '\\\\hbar': 'ℏ', '\\\\ell': 'ℓ', '\\\\Re': 'ℜ', '\\\\Im': 'ℑ',
        '\\\\aleph': 'ℵ', '\\\\wp': '℘', '\\\\otimes': '⊗', '\\\\oplus': '⊕',
        '\\\\circ': '∘', '\\\\bullet': '•', '\\\\star': '⋆', '\\\\dagger': '†',
        '\\\\ddagger': '‡', '\\\\vee': '∨', '\\\\wedge': '∧', '\\\\langle': '⟨',
        '\\\\rangle': '⟩', '\\\\int': '∫', '\\\\oint': '∮', '\\\\sum': '∑',
        '\\\\prod': '∏', '\\\\coprod': '∐', '\\\\sqrt': '√'
    }
    
    # Replace LaTeX commands with Unicode characters
    result = latex_str
    
    # Remove LaTeX environments
    result = re.sub(r'\\\\begin\\{[^}]*\\}|\\\\end\\{[^}]*\\}', '', result)
    
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
        result = \"\"
        for char in content:
            result += superscripts.get(char, char)
        return result
    
    result = re.sub(r'\\\\^\\{([^}]*)\\}', replace_superscript, result)
    
    # Process simple superscripts: replace ^x with superscript x
    def replace_simple_superscript(match):
        char = match.group(1)
        return superscripts.get(char, '^' + char)
    
    result = re.sub(r'\\\\^([a-zA-Z0-9])', replace_simple_superscript, result)
    
    # Process subscripts: replace _{x} with subscript x
    def replace_subscript(match):
        content = match.group(1)
        result = \"\"
        for char in content:
            result += subscripts.get(char, char)
        return result
    
    result = re.sub(r'_\\{([^}]*)\\}', replace_subscript, result)
    
    # Process simple subscripts: replace _x with subscript x
    def replace_simple_subscript(match):
        char = match.group(1)
        return subscripts.get(char, '_' + char)
    
    result = re.sub(r'_([a-zA-Z0-9])', replace_simple_subscript, result)
    
    # Handle fractions
    def replace_fraction(match):
        numerator = match.group(1)
        denominator = match.group(2)
        return f\"{numerator}⁄{denominator}\"
    
    result = re.sub(r'\\\\frac\\{([^}]*)\\}\\{([^}]*)\\}', replace_fraction, result)
    
    # Clean up remaining LaTeX commands and braces
    result = re.sub(r'\\\\[a-zA-Z]+', '', result)  # Remove remaining LaTeX commands
    result = re.sub(r'\\{|\\}', '', result)        # Remove remaining braces
    
    return result
"""
    
    # Read the PDF agent file
    with open('unified/agents/pdfagent.py', 'r') as f:
        content = f.read()
    
    # Add the latex_to_unicode function
    import_pattern = r'import os\nimport sys\nimport json\nimport shutil\nimport tempfile\nimport argparse\nimport subprocess\nimport importlib.util'
    import_replacement = r'import os\nimport sys\nimport json\nimport shutil\nimport tempfile\nimport argparse\nimport subprocess\nimport importlib.util\nimport re\n\n' + latex_to_unicode_code
    
    # Apply the replacement
    updated_content = re.sub(import_pattern, import_replacement, content)
    
    # Update the ReportLab PDF generation to use the latex_to_unicode function
    pdf_pattern = r'                            # Parse the LaTeX content\n                            title_match = re.search\(r\'\\\\section\\*\\{(.*?)\\}\', latex_content\)\n                            title = title_match.group\(1\) if title_match else "Theory of Everything"\n                            \n                            # Extract formulas\n                            formulas = re.findall\(r\'\\\\begin\\{align\\}(.*?)\\\\end\\{align\\}\', latex_content, re.DOTALL\)'
    pdf_replacement = r'                            # Parse the LaTeX content\n                            title_match = re.search(r\'\\\\section\\*\\{(.*?)\\}\', latex_content)\n                            title = title_match.group(1) if title_match else "Theory of Everything"\n                            \n                            # Extract formulas\n                            formulas = re.findall(r\'\\\\begin\\{align\\}(.*?)\\\\end\\{align\\}\', latex_content, re.DOTALL)\n                            \n                            # Convert formulas to Unicode for better rendering\n                            unicode_formulas = [latex_to_unicode(formula) for formula in formulas]'
    
    # Apply the replacement
    updated_content = re.sub(pdf_pattern, pdf_replacement, updated_content)
    
    # Update the formula rendering in the PDF
    formula_pattern = r'                            # Add formulas\n                            for formula in formulas:\n                                elements.append\(Paragraph\(formula, formula_style\)\)\n                                elements.append\(Spacer\(1, 12\)\)'
    formula_replacement = r'                            # Add formulas\n                            for formula in unicode_formulas:\n                                elements.append(Paragraph(formula, formula_style))\n                                elements.append(Spacer(1, 12))'
    
    # Apply the replacement
    updated_content = re.sub(formula_pattern, formula_replacement, updated_content)
    
    # Write the updated content back to the file
    with open('unified/agents/pdfagent.py', 'w') as f:
        f.write(updated_content)
    
    print("Updated PDF agent to use improved equation rendering")

if __name__ == "__main__":
    main()

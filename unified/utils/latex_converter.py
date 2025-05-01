#!/usr/bin/env python3
"""
LaTeX to Unicode converter for improved equation rendering
"""

import re

def latex_to_unicode(latex_str):
    """
    Convert LaTeX notation to Unicode for better readability
    
    Parameters:
    -----------
    latex_str : str
        LaTeX string to convert
        
    Returns:
    --------
    str
        Unicode representation of the LaTeX string
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

# Test the function if run directly
if __name__ == "__main__":
    test_equations = [
        "G_{\\mu\\nu} + \\Lambda g_{\\mu\\nu} = \\frac{8\\pi G}{c^4} T_{\\mu\\nu}",
        "i\\hbar\\frac{\\partial}{\\partial t}\\Psi(\\mathbf{r},t) = \\hat{H}\\Psi(\\mathbf{r},t)",
        "\\nabla \\cdot \\mathbf{E} = \\frac{\\rho}{\\epsilon_0}",
        "(i\\gamma^\\mu \\partial_\\mu - m)\\psi = 0",
        "\\mathcal{L} = -\\frac{1}{4}F_{\\mu\\nu}F^{\\mu\\nu} + \\bar{\\psi}(i\\gamma^\\mu D_\\mu - m)\\psi + \\frac{1}{16\\pi G}R"
    ]
    
    print("LaTeX to Unicode Conversion Examples")
    print("====================================")
    print()
    
    for eq in test_equations:
        print(f"LaTeX: {eq}")
        unicode_eq = latex_to_unicode(eq)
        print(f"Unicode: {unicode_eq}")
        print()

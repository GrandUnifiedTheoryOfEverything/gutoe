#!/usr/bin/env python3
"""
LaTeX Formula Renderer

This module provides specialized functions for rendering mathematical formulas
in PDF documents using LaTeX for professional typesetting.
"""

import os
import tempfile
import subprocess
from reportlab.lib.units import inch
from reportlab.platypus import Image as ReportLabImage, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from PIL import Image

class LaTeXFormulaRenderer:
    """
    Specialized renderer for mathematical formulas using LaTeX

    This class provides methods for rendering complex mathematical formulas
    with professional typesetting using LaTeX.
    """

    def __init__(self, output_dir="gfx/pdf/formulas"):
        """
        Initialize the LaTeX formula renderer

        Parameters:
        -----------
        output_dir : str
            Directory to save formula images (will be created if it doesn't exist)
        """
        self.output_dir = output_dir

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # LaTeX template for formulas
        self.formula_template = r"""
\documentclass[preview,border=10pt]{standalone}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{amsfonts}
\usepackage{mathtools}
\usepackage{xcolor}
\usepackage{physics}
\begin{document}
\begin{align}
%s
\end{align}
\end{document}
"""

    def render_formula(self, formula_name, formula_latex):
        """
        Render a mathematical formula as an image using LaTeX

        Parameters:
        -----------
        formula_name : str
            Name of the formula (used for the output file name)
        formula_latex : str
            LaTeX representation of the formula

        Returns:
        --------
        str
            Path to the saved formula image
        """
        # Define the output file
        output_file = os.path.join(self.output_dir, f"{formula_name.lower().replace(' ', '_')}.png")

        # Create a temporary directory for LaTeX files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create the LaTeX file
            tex_file = os.path.join(temp_dir, "formula.tex")
            with open(tex_file, "w") as f:
                f.write(self.formula_template % formula_latex)

            # Compile the LaTeX file to PDF
            try:
                subprocess.run(
                    ["pdflatex", "-interaction=nonstopmode", "-output-directory", temp_dir, tex_file],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True
                )

                # Convert PDF to PNG
                pdf_file = os.path.join(temp_dir, "formula.pdf")
                subprocess.run(
                    ["convert", "-density", "300", pdf_file, "-quality", "90", output_file],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True
                )
            except subprocess.CalledProcessError:
                # If LaTeX or convert fails, create a simple image with error message
                self._create_error_image(output_file, formula_name)

        return output_file

    def _create_error_image(self, output_file, formula_name):
        """Create a simple error image if LaTeX compilation fails"""
        img = Image.new('RGB', (800, 100), color=(255, 255, 255))
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("DejaVuSerif.ttf", 16)
        except IOError:
            font = ImageFont.load_default()

        error_message = f"Error rendering formula: {formula_name}"
        draw.text((20, 40), error_message, fill=(255, 0, 0), font=font)
        img.save(output_file)

    def create_formula_image(self, formula_dict):
        """
        Create an image for a formula with proper LaTeX rendering

        Parameters:
        -----------
        formula_dict : dict
            Dictionary containing formula information:
            - name: Name of the formula
            - latex: LaTeX representation of the formula
            - description: Description of the formula

        Returns:
        --------
        str
            Path to the saved formula image
        """
        # Extract formula information
        name = formula_dict["name"]

        # Get the appropriate LaTeX formula
        if "latex" in formula_dict:
            latex = formula_dict["latex"]
        else:
            # Use predefined LaTeX formulas for common equations
            latex = self._get_predefined_latex(name)

        # Render the formula
        return self.render_formula(name, latex)

    def _get_predefined_latex(self, name):
        """Get predefined LaTeX formula for common equations"""
        formulas = {
            "Master Equation": r"S = S_{\text{gravity}} + S_{\text{matter}} + S_{\text{gauge}} + S_{\text{quantum}}",

            "Gravity Action": r"S_{\text{gravity}} = \frac{1}{16\pi G} \int d^4x \sqrt{-g} (R - 2\Lambda)",

            "Matter Action": r"S_{\text{matter}} = \int d^4x \sqrt{-g} \bar{\psi}(i\gamma^\mu D_\mu - m)\psi",

            "Gauge Field Action": r"S_{\text{gauge}} = -\frac{1}{4} \int d^4x \sqrt{-g} F_{\mu\nu}^a F^{\mu\nu}_a",

            "Quantum Corrections": r"S_{\text{quantum}} = \sum_{n=1}^{\infty} \hbar^n S_n",

            "Maxwell's Equations": r"\begin{cases} \nabla \cdot \vec{E} = \frac{\rho}{\varepsilon_0} \\ \nabla \cdot \vec{B} = 0 \\ \nabla \times \vec{E} = -\frac{\partial \vec{B}}{\partial t} \\ \nabla \times \vec{B} = \mu_0 \vec{J} + \mu_0 \varepsilon_0 \frac{\partial \vec{E}}{\partial t} \end{cases}",

            "Einstein Field Equations": r"G_{\mu\nu} = R_{\mu\nu} - \frac{1}{2}Rg_{\mu\nu} = \frac{8\pi G}{c^4}T_{\mu\nu}",

            "Schrödinger Equation": r"i\hbar\frac{\partial}{\partial t}\Psi(\vec{r},t) = \hat{H}\Psi(\vec{r},t) = \left[-\frac{\hbar^2}{2m}\nabla^2 + V(\vec{r},t)\right]\Psi(\vec{r},t)",

            "Dirac Equation": r"(i\gamma^\mu \partial_\mu - m)\psi = 0",

            "Standard Model Lagrangian": r"\mathcal{L}_{\text{SM}} = \mathcal{L}_{\text{gauge}} + \mathcal{L}_{\text{fermion}} + \mathcal{L}_{\text{Higgs}} + \mathcal{L}_{\text{Yukawa}}"
        }

        return formulas.get(name, r"\text{Formula not available: } " + name)

def create_formula_paragraph(formula_dict, renderer, styles):
    """
    Create a paragraph for a formula with proper LaTeX rendering

    Parameters:
    -----------
    formula_dict : dict
        Dictionary containing formula information:
        - name: Name of the formula
        - latex: LaTeX representation of the formula (optional)
        - description: Description of the formula
    renderer : LaTeXFormulaRenderer
        LaTeX formula renderer instance
    styles : dict
        Dictionary of paragraph styles

    Returns:
    --------
    list
        List of reportlab elements for the formula
    """
    elements = []

    # Add the formula name
    elements.append(Paragraph(formula_dict["name"], styles["heading2"]))

    # Create the formula image
    formula_image_path = renderer.create_formula_image(formula_dict)

    # Add the formula image
    elements.append(ReportLabImage(formula_image_path, width=6*inch, height=1.5*inch))

    # Add the description
    elements.append(Paragraph(formula_dict["description"], styles["normal"]))
    elements.append(Spacer(1, 0.2*inch))

    return elements

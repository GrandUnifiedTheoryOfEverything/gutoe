#!/usr/bin/env python3
"""
Math Formula Renderer

This module provides specialized functions for rendering mathematical formulas
in PDF documents with proper subscripts, superscripts, and special symbols.
"""

import os
import io
import tempfile
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.units import inch
from reportlab.platypus import Image as ReportLabImage, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER

class MathFormulaRenderer:
    """
    Specialized renderer for mathematical formulas
    
    This class provides methods for rendering complex mathematical formulas
    with proper subscripts, superscripts, and special symbols.
    """
    
    def __init__(self, output_dir="docs/pdf/formulas"):
        """
        Initialize the math formula renderer
        
        Parameters:
        -----------
        output_dir : str
            Directory to save formula images (will be created if it doesn't exist)
        """
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Load fonts
        try:
            self.main_font = ImageFont.truetype("DejaVuSerif.ttf", 24)
            self.sub_font = ImageFont.truetype("DejaVuSerif.ttf", 16)
            self.symbol_font = ImageFont.truetype("DejaVuSansMono.ttf", 24)
        except IOError:
            # Fallback to default font
            self.main_font = ImageFont.load_default()
            self.sub_font = ImageFont.load_default()
            self.symbol_font = ImageFont.load_default()
    
    def render_formula(self, formula_name, formula_text):
        """
        Render a mathematical formula as an image
        
        Parameters:
        -----------
        formula_name : str
            Name of the formula (used for the output file name)
        formula_text : str
            Text representation of the formula
            
        Returns:
        --------
        str
            Path to the saved formula image
        """
        # Define the output file
        output_file = os.path.join(self.output_dir, f"{formula_name.lower().replace(' ', '_')}.png")
        
        # Create a drawing
        width, height = 800, 100
        img = Image.new('RGB', (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        # Replace special symbols
        formula_text = self._replace_special_symbols(formula_text)
        
        # Draw the formula
        draw.text((20, height // 2 - 12), formula_text, fill=(0, 0, 0), font=self.main_font)
        
        # Save the image
        img.save(output_file)
        
        return output_file
    
    def _replace_special_symbols(self, text):
        """
        Replace special symbols in the formula text
        
        Parameters:
        -----------
        text : str
            Formula text with special symbol placeholders
            
        Returns:
        --------
        str
            Formula text with proper special symbols
        """
        # Replace common special symbols
        replacements = {
            "∫": "∫",
            "√": "√",
            "π": "π",
            "γ": "γ",
            "μ": "μ",
            "ν": "ν",
            "ψ": "ψ",
            "ψ̄": "ψ̄",
            "Λ": "Λ",
            "∞": "∞",
            "ℏ": "ℏ",
            "∑": "∑"
        }
        
        for placeholder, symbol in replacements.items():
            text = text.replace(placeholder, symbol)
        
        return text
    
    def create_formula_image(self, formula_dict):
        """
        Create an image for a formula with proper rendering
        
        Parameters:
        -----------
        formula_dict : dict
            Dictionary containing formula information:
            - name: Name of the formula
            - equation: Equation text
            - description: Description of the formula
            
        Returns:
        --------
        str
            Path to the saved formula image
        """
        # Extract formula information
        name = formula_dict["name"]
        equation = formula_dict["equation"]
        
        # Define the output file
        output_file = os.path.join(self.output_dir, f"{name.lower().replace(' ', '_')}.png")
        
        # Create a drawing
        width, height = 800, 100
        img = Image.new('RGB', (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        # Draw the equation
        if name == "Master Equation":
            self._draw_master_equation(draw, width, height)
        elif name == "Gravity Action":
            self._draw_gravity_action(draw, width, height)
        elif name == "Matter Action":
            self._draw_matter_action(draw, width, height)
        elif name == "Gauge Field Action":
            self._draw_gauge_field_action(draw, width, height)
        elif name == "Quantum Corrections":
            self._draw_quantum_corrections(draw, width, height)
        else:
            # Generic equation drawing
            draw.text((20, height // 2 - 12), equation, fill=(0, 0, 0), font=self.main_font)
        
        # Save the image
        img.save(output_file)
        
        return output_file
    
    def _draw_master_equation(self, draw, width, height):
        """Draw the master equation"""
        # S = S_gravity + S_matter + S_gauge + S_quantum
        x, y = 20, height // 2 - 12
        
        # Draw "S = "
        draw.text((x, y), "S = ", fill=(0, 0, 0), font=self.main_font)
        x += 50
        
        # Draw "S"
        draw.text((x, y), "S", fill=(0, 0, 0), font=self.main_font)
        
        # Draw "gravity" subscript
        draw.text((x + 15, y + 10), "gravity", fill=(0, 0, 0), font=self.sub_font)
        x += 80
        
        # Draw " + S"
        draw.text((x, y), " + S", fill=(0, 0, 0), font=self.main_font)
        x += 40
        
        # Draw "matter" subscript
        draw.text((x + 15, y + 10), "matter", fill=(0, 0, 0), font=self.sub_font)
        x += 80
        
        # Draw " + S"
        draw.text((x, y), " + S", fill=(0, 0, 0), font=self.main_font)
        x += 40
        
        # Draw "gauge" subscript
        draw.text((x + 15, y + 10), "gauge", fill=(0, 0, 0), font=self.sub_font)
        x += 80
        
        # Draw " + S"
        draw.text((x, y), " + S", fill=(0, 0, 0), font=self.main_font)
        x += 40
        
        # Draw "quantum" subscript
        draw.text((x + 15, y + 10), "quantum", fill=(0, 0, 0), font=self.sub_font)
    
    def _draw_gravity_action(self, draw, width, height):
        """Draw the gravity action equation"""
        # S_gravity = 1/(16πG) ∫d^4x √(-g) (R - 2Λ)
        x, y = 20, height // 2 - 12
        
        # Draw "S"
        draw.text((x, y), "S", fill=(0, 0, 0), font=self.main_font)
        
        # Draw "gravity" subscript
        draw.text((x + 15, y + 10), "gravity", fill=(0, 0, 0), font=self.sub_font)
        x += 80
        
        # Draw " = 1/(16πG) "
        draw.text((x, y), " = 1/(16πG) ", fill=(0, 0, 0), font=self.main_font)
        x += 120
        
        # Draw "∫d"
        draw.text((x, y), "∫d", fill=(0, 0, 0), font=self.main_font)
        x += 30
        
        # Draw "4" superscript
        draw.text((x, y - 10), "4", fill=(0, 0, 0), font=self.sub_font)
        x += 15
        
        # Draw "x √(-g) (R - 2Λ)"
        draw.text((x, y), "x √(-g) (R - 2Λ)", fill=(0, 0, 0), font=self.main_font)
    
    def _draw_matter_action(self, draw, width, height):
        """Draw the matter action equation"""
        # S_matter = ∫d^4x √(-g) ψ̄(iγ^μD_μ - m)ψ
        x, y = 20, height // 2 - 12
        
        # Draw "S"
        draw.text((x, y), "S", fill=(0, 0, 0), font=self.main_font)
        
        # Draw "matter" subscript
        draw.text((x + 15, y + 10), "matter", fill=(0, 0, 0), font=self.sub_font)
        x += 80
        
        # Draw " = "
        draw.text((x, y), " = ", fill=(0, 0, 0), font=self.main_font)
        x += 30
        
        # Draw "∫d"
        draw.text((x, y), "∫d", fill=(0, 0, 0), font=self.main_font)
        x += 30
        
        # Draw "4" superscript
        draw.text((x, y - 10), "4", fill=(0, 0, 0), font=self.sub_font)
        x += 15
        
        # Draw "x √(-g) "
        draw.text((x, y), "x √(-g) ", fill=(0, 0, 0), font=self.main_font)
        x += 80
        
        # Draw "ψ̄"
        draw.text((x, y), "ψ̄", fill=(0, 0, 0), font=self.main_font)
        x += 20
        
        # Draw "(iγ"
        draw.text((x, y), "(iγ", fill=(0, 0, 0), font=self.main_font)
        x += 30
        
        # Draw "μ" superscript
        draw.text((x, y - 10), "μ", fill=(0, 0, 0), font=self.sub_font)
        x += 15
        
        # Draw "D"
        draw.text((x, y), "D", fill=(0, 0, 0), font=self.main_font)
        x += 15
        
        # Draw "μ" subscript
        draw.text((x, y + 10), "μ", fill=(0, 0, 0), font=self.sub_font)
        x += 15
        
        # Draw " - m)ψ"
        draw.text((x, y), " - m)ψ", fill=(0, 0, 0), font=self.main_font)
    
    def _draw_gauge_field_action(self, draw, width, height):
        """Draw the gauge field action equation"""
        # S_gauge = -1/4 ∫d^4x √(-g) F_μν^a F^μν_a
        x, y = 20, height // 2 - 12
        
        # Draw "S"
        draw.text((x, y), "S", fill=(0, 0, 0), font=self.main_font)
        
        # Draw "gauge" subscript
        draw.text((x + 15, y + 10), "gauge", fill=(0, 0, 0), font=self.sub_font)
        x += 80
        
        # Draw " = -1/4 "
        draw.text((x, y), " = -1/4 ", fill=(0, 0, 0), font=self.main_font)
        x += 70
        
        # Draw "∫d"
        draw.text((x, y), "∫d", fill=(0, 0, 0), font=self.main_font)
        x += 30
        
        # Draw "4" superscript
        draw.text((x, y - 10), "4", fill=(0, 0, 0), font=self.sub_font)
        x += 15
        
        # Draw "x √(-g) "
        draw.text((x, y), "x √(-g) ", fill=(0, 0, 0), font=self.main_font)
        x += 80
        
        # Draw "F"
        draw.text((x, y), "F", fill=(0, 0, 0), font=self.main_font)
        x += 15
        
        # Draw "μν" subscript
        draw.text((x, y + 10), "μν", fill=(0, 0, 0), font=self.sub_font)
        x += 25
        
        # Draw "a" superscript
        draw.text((x, y - 10), "a", fill=(0, 0, 0), font=self.sub_font)
        x += 15
        
        # Draw "F"
        draw.text((x, y), "F", fill=(0, 0, 0), font=self.main_font)
        x += 15
        
        # Draw "μν" superscript
        draw.text((x, y - 10), "μν", fill=(0, 0, 0), font=self.sub_font)
        x += 25
        
        # Draw "a" subscript
        draw.text((x, y + 10), "a", fill=(0, 0, 0), font=self.sub_font)
    
    def _draw_quantum_corrections(self, draw, width, height):
        """Draw the quantum corrections equation"""
        # S_quantum = ∑_{n=1}^∞ ℏ^n S_n
        x, y = 20, height // 2 - 12
        
        # Draw "S"
        draw.text((x, y), "S", fill=(0, 0, 0), font=self.main_font)
        
        # Draw "quantum" subscript
        draw.text((x + 15, y + 10), "quantum", fill=(0, 0, 0), font=self.sub_font)
        x += 80
        
        # Draw " = "
        draw.text((x, y), " = ", fill=(0, 0, 0), font=self.main_font)
        x += 30
        
        # Draw "∑"
        draw.text((x, y), "∑", fill=(0, 0, 0), font=self.main_font)
        x += 20
        
        # Draw "n=1" subscript
        draw.text((x, y + 10), "n=1", fill=(0, 0, 0), font=self.sub_font)
        x += 30
        
        # Draw "∞" superscript
        draw.text((x, y - 10), "∞", fill=(0, 0, 0), font=self.sub_font)
        x += 15
        
        # Draw " ℏ"
        draw.text((x, y), " ℏ", fill=(0, 0, 0), font=self.main_font)
        x += 20
        
        # Draw "n" superscript
        draw.text((x, y - 10), "n", fill=(0, 0, 0), font=self.sub_font)
        x += 15
        
        # Draw "S"
        draw.text((x, y), "S", fill=(0, 0, 0), font=self.main_font)
        x += 15
        
        # Draw "n" subscript
        draw.text((x, y + 10), "n", fill=(0, 0, 0), font=self.sub_font)

def create_formula_paragraph(formula_dict, renderer, styles):
    """
    Create a paragraph for a formula with proper rendering
    
    Parameters:
    -----------
    formula_dict : dict
        Dictionary containing formula information:
        - name: Name of the formula
        - equation: Equation text
        - description: Description of the formula
    renderer : MathFormulaRenderer
        Math formula renderer instance
    styles : dict
        Dictionary of paragraph styles
        
    Returns:
    --------
    list
        List of reportlab elements for the formula
    """
    elements = []
    
    # Add the formula name
    elements.append(Paragraph(formula_dict["name"], styles["heading"]))
    
    # Create the formula image
    formula_image_path = renderer.create_formula_image(formula_dict)
    
    # Add the formula image
    elements.append(ReportLabImage(formula_image_path, width=6*inch, height=1*inch))
    
    # Add the description
    elements.append(Paragraph(formula_dict["description"], styles["normal"]))
    elements.append(Paragraph("<br/>", styles["normal"]))
    
    return elements

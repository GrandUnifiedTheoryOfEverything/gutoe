#!/usr/bin/env python3
"""
Generate a PDF file using ReportLab
"""

import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

def main():
    """Main function"""
    # Create the output directory
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
    
    # Create a PDF document
    output_file = f"gfx/pdf/{formula_name}_reportlab.pdf"
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create a custom style for formulas
    formula_style = ParagraphStyle(
        'Formula',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=12,
        leading=14,
        alignment=1  # Center alignment
    )
    
    # Create a custom style for titles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=16,
        leading=18,
        alignment=1  # Center alignment
    )
    
    # Create a custom style for sections
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading2'],
        fontSize=14,
        leading=16
    )
    
    # Build the document
    elements = []
    
    # Add title
    elements.append(Paragraph(formula_data['name'], title_style))
    elements.append(Spacer(1, 12))
    
    # Add description
    elements.append(Paragraph(formula_data['description'], styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Add formula
    elements.append(Paragraph(formula_data['latex'], formula_style))
    elements.append(Spacer(1, 24))
    
    # Add components
    elements.append(Paragraph("Components", section_style))
    elements.append(Spacer(1, 12))
    
    for component in formula_data['components']:
        elements.append(Paragraph(component['name'], styles['Heading3']))
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(component['description'], styles['Normal']))
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(component['latex'], formula_style))
        elements.append(Spacer(1, 12))
    
    # Build the PDF
    doc.build(elements)
    
    print(f"PDF file saved to: {output_file}")
    
    # Check if the file exists
    if os.path.exists(output_file):
        print(f"PDF file size: {os.path.getsize(output_file)} bytes")
    else:
        print(f"Error: PDF file not found: {output_file}")

if __name__ == "__main__":
    main()

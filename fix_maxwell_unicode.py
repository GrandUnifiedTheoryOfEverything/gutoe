#!/usr/bin/env python3
"""
Generate a PDF for Maxwell's Equations with proper Unicode subscripts
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

# Ensure the docs/pdf directory exists
os.makedirs("docs/pdf", exist_ok=True)

# Create a PDF document
doc = SimpleDocTemplate("docs/pdf/maxwell.pdf", pagesize=letter)

# Define styles
styles = getSampleStyleSheet()

# Create custom styles
title_style = ParagraphStyle(
    'Title',
    parent=styles['Title'],
    fontSize=20,
    alignment=TA_CENTER,
    spaceAfter=24
)

equation_style = ParagraphStyle(
    'Equation',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',  # Using Helvetica instead of Courier for better Unicode support
    fontSize=14,
    alignment=TA_CENTER,
    spaceBefore=6,
    spaceAfter=12
)

# Build the document
elements = []

# Add title
elements.append(Paragraph("Maxwell's Equations", title_style))
elements.append(Spacer(1, 24))

# Add equations with proper Unicode subscripts
# Using Unicode subscript zero (₀) directly
elements.append(Paragraph("Gauss's Law for Electricity:", styles['Heading2']))
elements.append(Paragraph("∇·E = ρ/ε₀", equation_style))
elements.append(Spacer(1, 18))

elements.append(Paragraph("Gauss's Law for Magnetism:", styles['Heading2']))
elements.append(Paragraph("∇·B = 0", equation_style))
elements.append(Spacer(1, 18))

elements.append(Paragraph("Faraday's Law of Induction:", styles['Heading2']))
elements.append(Paragraph("∇×E = -∂B/∂t", equation_style))
elements.append(Spacer(1, 18))

elements.append(Paragraph("Ampère's Law with Maxwell's Addition:", styles['Heading2']))
elements.append(Paragraph("∇×B = μ₀J + μ₀ε₀∂E/∂t", equation_style))

# Build the PDF
try:
    doc.build(elements)
    print(f"Maxwell's Equations PDF saved to: docs/pdf/maxwell.pdf")
    print(f"File size: {os.path.getsize('docs/pdf/maxwell.pdf')} bytes")
except Exception as e:
    print(f"Error generating PDF: {str(e)}")

print("Maxwell's Equations PDF generation complete.")

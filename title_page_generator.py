#!/usr/bin/env python3
"""
Title Page Generator

This module provides functions for generating professional title pages
with quantum graphics for scientific documents.
"""

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Paragraph, Spacer, Image, PageBreak
from quantum_graphics_generator import QuantumGraphicsGenerator

class TitlePageGenerator:
    """
    Title Page Generator
    
    This class provides methods for generating professional title pages
    with quantum graphics for scientific documents.
    """
    
    def __init__(self, output_dir="docs/pdf"):
        """
        Initialize the title page generator
        
        Parameters:
        -----------
        output_dir : str
            Directory to save title page elements (will be created if it doesn't exist)
        """
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize the quantum graphics generator
        self.quantum_generator = QuantumGraphicsGenerator()
    
    def generate_title_page(self, title, subtitle, author="", date="", document_type="Scientific Document"):
        """
        Generate a professional title page with quantum graphics
        
        Parameters:
        -----------
        title : str
            Title of the document
        subtitle : str
            Subtitle of the document
        author : str
            Author of the document
        date : str
            Date of the document
        document_type : str
            Type of document (e.g., "Scientific Document", "Research Paper", etc.)
            
        Returns:
        --------
        list
            List of reportlab elements for the title page
        """
        elements = []
        
        # Generate quantum background
        background_path = self.quantum_generator.generate_title_page_background()
        
        # Generate quantum wave function for decoration
        wave_function_path = self.quantum_generator.generate_wave_function(
            width=400, height=300, n=3, l=2, filename="title_wave_function.png")
        
        # Generate quantum field for decoration
        quantum_field_path = self.quantum_generator.generate_quantum_field(
            width=400, height=300, complexity=5, filename="title_quantum_field.png")
        
        # Create title page styles
        title_style = ParagraphStyle(
            'Title',
            fontName='Helvetica-Bold',
            fontSize=24,
            leading=30,
            alignment=TA_CENTER,
            textColor=colors.white,
            spaceAfter=24
        )
        
        subtitle_style = ParagraphStyle(
            'Subtitle',
            fontName='Helvetica',
            fontSize=18,
            leading=22,
            alignment=TA_CENTER,
            textColor=colors.white,
            spaceAfter=36
        )
        
        author_style = ParagraphStyle(
            'Author',
            fontName='Helvetica',
            fontSize=14,
            leading=18,
            alignment=TA_CENTER,
            textColor=colors.white,
            spaceAfter=12
        )
        
        date_style = ParagraphStyle(
            'Date',
            fontName='Helvetica',
            fontSize=12,
            leading=16,
            alignment=TA_CENTER,
            textColor=colors.white,
            spaceAfter=36
        )
        
        document_type_style = ParagraphStyle(
            'DocumentType',
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=18,
            alignment=TA_CENTER,
            textColor=colors.white,
            spaceAfter=12
        )
        
        # Create a function to add the background to the first page
        def add_title_background(canvas, doc):
            # Draw the background image
            canvas.saveState()
            canvas.drawImage(background_path, 0, 0, width=doc.pagesize[0], height=doc.pagesize[1])
            canvas.restoreState()
        
        # Add the title page elements
        elements.append(Spacer(1, 2*inch))  # Space at the top
        
        # Add the wave function image
        elements.append(Image(wave_function_path, width=3*inch, height=2.25*inch))
        elements.append(Spacer(1, 0.5*inch))
        
        # Add the title and subtitle
        elements.append(Paragraph(title, title_style))
        elements.append(Paragraph(subtitle, subtitle_style))
        
        # Add the quantum field image
        elements.append(Image(quantum_field_path, width=3*inch, height=2.25*inch))
        elements.append(Spacer(1, 0.5*inch))
        
        # Add the document type, author, and date
        elements.append(Paragraph(document_type, document_type_style))
        if author:
            elements.append(Paragraph(f"By: {author}", author_style))
        if date:
            elements.append(Paragraph(date, date_style))
        
        # Add a page break after the title page
        elements.append(PageBreak())
        
        return elements, add_title_background

# Main function for command-line usage
def main():
    """Main function for command-line usage"""
    generator = TitlePageGenerator()
    
    # Generate a sample title page
    elements, _ = generator.generate_title_page(
        title="Complete Theory of Everything",
        subtitle="A Unified Framework for Understanding the Universe",
        author="Theoretical Physics Department",
        date="2023",
        document_type="Scientific Research"
    )
    
    print("Title page elements generated successfully!")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
PDF Styling Enhancer

This module provides enhanced styling capabilities for PDF documents,
including professional themes, color schemes, and typography options.
"""

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

class PDFStylingEnhancer:
    """
    PDF Styling Enhancer
    
    This class provides methods for enhancing the styling of PDF documents:
    - Professional color schemes
    - Typography enhancements
    - Layout templates
    - Table styling
    """
    
    def __init__(self):
        """Initialize the PDF styling enhancer"""
        # Define color schemes
        self.color_schemes = {
            "professional": {
                "primary": colors.HexColor("#0066cc"),  # Blue
                "secondary": colors.HexColor("#4d4d4d"),  # Dark gray
                "accent": colors.HexColor("#ff9900"),  # Orange
                "background": colors.white,
                "text": colors.black
            },
            "scientific": {
                "primary": colors.HexColor("#006699"),  # Dark blue
                "secondary": colors.HexColor("#669900"),  # Green
                "accent": colors.HexColor("#cc3300"),  # Red
                "background": colors.HexColor("#f9f9f9"),  # Light gray
                "text": colors.HexColor("#333333")  # Dark gray
            },
            "elegant": {
                "primary": colors.HexColor("#333366"),  # Navy blue
                "secondary": colors.HexColor("#996633"),  # Brown
                "accent": colors.HexColor("#cc9900"),  # Gold
                "background": colors.HexColor("#f5f5f5"),  # Off-white
                "text": colors.HexColor("#1a1a1a")  # Very dark gray
            }
        }
        
        # Define font families
        self.font_families = {
            "serif": {
                "normal": "Times-Roman",
                "bold": "Times-Bold",
                "italic": "Times-Italic",
                "boldItalic": "Times-BoldItalic"
            },
            "sans-serif": {
                "normal": "Helvetica",
                "bold": "Helvetica-Bold",
                "italic": "Helvetica-Oblique",
                "boldItalic": "Helvetica-BoldOblique"
            },
            "monospace": {
                "normal": "Courier",
                "bold": "Courier-Bold",
                "italic": "Courier-Oblique",
                "boldItalic": "Courier-BoldOblique"
            }
        }
    
    def create_styled_paragraph_styles(self, color_scheme="professional", font_family="serif"):
        """
        Create a set of styled paragraph styles
        
        Parameters:
        -----------
        color_scheme : str
            Name of the color scheme to use
        font_family : str
            Name of the font family to use
            
        Returns:
        --------
        dict
            Dictionary of styled paragraph styles
        """
        # Get the base styles
        styles = getSampleStyleSheet()
        
        # Get the color scheme
        colors_dict = self.color_schemes.get(color_scheme, self.color_schemes["professional"])
        
        # Get the font family
        fonts_dict = self.font_families.get(font_family, self.font_families["serif"])
        
        # Create custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontName=fonts_dict["bold"],
            fontSize=24,
            leading=30,
            alignment=TA_CENTER,
            textColor=colors_dict["primary"],
            spaceAfter=24
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading1'],
            fontName=fonts_dict["bold"],
            fontSize=18,
            leading=22,
            alignment=TA_CENTER,
            textColor=colors_dict["secondary"],
            spaceAfter=12
        )
        
        heading1_style = ParagraphStyle(
            'CustomHeading1',
            parent=styles['Heading1'],
            fontName=fonts_dict["bold"],
            fontSize=16,
            leading=20,
            textColor=colors_dict["primary"],
            spaceBefore=12,
            spaceAfter=6
        )
        
        heading2_style = ParagraphStyle(
            'CustomHeading2',
            parent=styles['Heading2'],
            fontName=fonts_dict["bold"],
            fontSize=14,
            leading=18,
            textColor=colors_dict["secondary"],
            spaceBefore=10,
            spaceAfter=4
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontName=fonts_dict["normal"],
            fontSize=11,
            leading=14,
            alignment=TA_JUSTIFY,
            textColor=colors_dict["text"]
        )
        
        bullet_style = ParagraphStyle(
            'CustomBullet',
            parent=styles['Normal'],
            fontName=fonts_dict["normal"],
            fontSize=11,
            leading=14,
            leftIndent=20,
            firstLineIndent=0,
            bulletIndent=10,
            textColor=colors_dict["text"]
        )
        
        code_style = ParagraphStyle(
            'CustomCode',
            parent=styles['Code'],
            fontName=self.font_families["monospace"]["normal"],
            fontSize=9,
            leading=12,
            textColor=colors_dict["text"]
        )
        
        caption_style = ParagraphStyle(
            'CustomCaption',
            parent=styles['Normal'],
            fontName=fonts_dict["italic"],
            fontSize=9,
            leading=12,
            alignment=TA_CENTER,
            textColor=colors_dict["secondary"]
        )
        
        equation_style = ParagraphStyle(
            'CustomEquation',
            parent=styles['Normal'],
            fontName=fonts_dict["bold"],
            fontSize=12,
            leading=16,
            alignment=TA_CENTER,
            spaceBefore=8,
            spaceAfter=8,
            textColor=colors_dict["text"]
        )
        
        # Return the styles dictionary
        return {
            "title": title_style,
            "subtitle": subtitle_style,
            "heading1": heading1_style,
            "heading2": heading2_style,
            "normal": normal_style,
            "bullet": bullet_style,
            "code": code_style,
            "caption": caption_style,
            "equation": equation_style
        }
    
    def create_styled_table(self, data, column_widths=None, style_name="professional"):
        """
        Create a styled table
        
        Parameters:
        -----------
        data : list
            List of lists containing the table data
        column_widths : list, optional
            List of column widths
        style_name : str
            Name of the style to use
            
        Returns:
        --------
        Table
            Styled table
        """
        # Get the color scheme
        colors_dict = self.color_schemes.get(style_name, self.color_schemes["professional"])
        
        # Create the table
        table = Table(data, colWidths=column_widths)
        
        # Define the table style
        if style_name == "professional":
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors_dict["primary"]),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors_dict["text"]),
                ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f0f0")])
            ])
        elif style_name == "scientific":
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors_dict["primary"]),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors_dict["text"]),
                ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('BOX', (0, 0), (-1, -1), 1, colors_dict["primary"]),
                ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f0f0")])
            ])
        else:  # elegant
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors_dict["primary"]),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors_dict["text"]),
                ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('BOX', (0, 0), (-1, -1), 1, colors_dict["primary"]),
                ('LINEBELOW', (0, 0), (-1, 0), 1, colors_dict["accent"]),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ])
        
        # Apply the style
        table.setStyle(table_style)
        
        return table
    
    def create_bullet_list(self, items, style):
        """
        Create a bullet list
        
        Parameters:
        -----------
        items : list
            List of items
        style : ParagraphStyle
            Style to use for the list items
            
        Returns:
        --------
        list
            List of paragraphs with bullets
        """
        elements = []
        
        for item in items:
            bullet_text = f"• {item}"
            elements.append(Paragraph(bullet_text, style))
        
        return elements
    
    def create_numbered_list(self, items, style):
        """
        Create a numbered list
        
        Parameters:
        -----------
        items : list
            List of items
        style : ParagraphStyle
            Style to use for the list items
            
        Returns:
        --------
        list
            List of paragraphs with numbers
        """
        elements = []
        
        for i, item in enumerate(items):
            numbered_text = f"{i+1}. {item}"
            elements.append(Paragraph(numbered_text, style))
        
        return elements

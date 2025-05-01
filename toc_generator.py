#!/usr/bin/env python3
"""
Table of Contents Generator

This module provides functions for generating proper tables of contents
for PDF documents.
"""

import os
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import Paragraph, Spacer, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents

class TOCGenerator:
    """
    Table of Contents Generator

    This class provides methods for generating proper tables of contents
    for PDF documents.
    """

    def __init__(self):
        """Initialize the TOC generator"""
        pass

    def generate_toc(self, styles):
        """
        Generate a proper table of contents

        Parameters:
        -----------
        styles : dict
            Dictionary of paragraph styles

        Returns:
        --------
        tuple
            (TableOfContents object, list of elements for the TOC page)
        """
        elements = []

        # Create TOC styles
        toc_title_style = ParagraphStyle(
            'TOCTitle',
            fontName="Helvetica-Bold",
            fontSize=styles["heading1"].fontSize,
            leading=styles["heading1"].leading,
            alignment=TA_LEFT,
            spaceBefore=12,
            spaceAfter=24
        )

        toc_h1_style = ParagraphStyle(
            'TOCHeading1',
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            leftIndent=20,
            firstLineIndent=-20,
            spaceBefore=6,
            spaceAfter=6
        )

        toc_h2_style = ParagraphStyle(
            'TOCHeading2',
            fontName="Helvetica",
            fontSize=12,
            leading=16,
            leftIndent=40,
            firstLineIndent=-20,
            spaceBefore=4,
            spaceAfter=4
        )

        # Add a title for the TOC
        elements.append(Paragraph("Table of Contents", toc_title_style))
        elements.append(Spacer(1, 0.2*inch))

        # Create the TOC
        toc = TableOfContents()
        toc.levelStyles = [toc_h1_style, toc_h2_style]

        # Add the TOC to the elements
        elements.append(toc)
        elements.append(PageBreak())

        return toc, elements

    def register_section(self, toc, title, level=0):
        """
        Register a section in the table of contents

        Parameters:
        -----------
        toc : TableOfContents
            TableOfContents object
        title : str
            Title of the section
        level : int
            Level of the section (0 for top level)
        """
        # This is handled automatically by ReportLab when using the proper heading styles
        # Just make sure to use the proper heading styles for your sections
        pass

# Main function for command-line usage
def main():
    """Main function for command-line usage"""
    from reportlab.lib.styles import getSampleStyleSheet

    generator = TOCGenerator()

    # Generate a sample TOC
    styles = getSampleStyleSheet()
    toc, elements = generator.generate_toc(styles)

    print("TOC elements generated successfully!")

if __name__ == "__main__":
    main()

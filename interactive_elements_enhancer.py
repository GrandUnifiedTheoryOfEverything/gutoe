#!/usr/bin/env python3
"""
Interactive Elements Enhancer

This module provides enhanced interactive elements for PDF documents,
including hyperlinks, bookmarks, and interactive navigation.
"""

import os
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Spacer, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

class InteractiveElementsEnhancer:
    """
    Interactive Elements Enhancer

    This class provides methods for enhancing PDF documents with interactive elements:
    - Table of contents with hyperlinks
    - Bookmarks for navigation
    - Cross-references between sections
    - Interactive navigation elements
    """

    def __init__(self):
        """Initialize the interactive elements enhancer"""
        # Try to register additional fonts if available
        try:
            registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
            registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'))
            self.custom_fonts_available = True
        except:
            self.custom_fonts_available = False

    def create_table_of_contents(self, styles):
        """
        Create a table of contents

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

        # Add a title for the TOC
        elements.append(Paragraph("Table of Contents", styles["heading1"]))
        elements.append(Spacer(1, 0.2*inch))

        # Create TOC style
        toc_style = ParagraphStyle(
            'TOCHeading1',
            fontName=styles["heading1"].fontName,
            fontSize=styles["heading1"].fontSize - 2,
            leading=styles["heading1"].leading - 2,
            leftIndent=20,
            firstLineIndent=-20,
            spaceBefore=5,
            spaceAfter=5
        )

        # Create the TOC
        toc = TableOfContents()
        toc.levelStyles = [toc_style]

        elements.append(toc)
        elements.append(PageBreak())

        return toc, elements

    def create_bookmark_data(self, title, level=0):
        """
        Create bookmark data for PDF navigation

        Parameters:
        -----------
        title : str
            Title for the bookmark
        level : int
            Level of the bookmark (0 for top level)

        Returns:
        --------
        dict
            Bookmark data dictionary
        """
        return {
            'key': f"bookmark_{title.lower().replace(' ', '_')}",
            'title': title,
            'level': level
        }

    def create_section_header(self, title, styles, bookmark_level=0):
        """
        Create a section header with bookmark

        Parameters:
        -----------
        title : str
            Title for the section
        styles : dict
            Dictionary of paragraph styles
        bookmark_level : int
            Level of the bookmark (0 for top level)

        Returns:
        --------
        tuple
            (Paragraph object, bookmark data)
        """
        # Create the paragraph with an anchor
        anchor_name = f"section_{title.lower().replace(' ', '_')}"
        header_with_anchor = f'<a name="{anchor_name}"></a>{title}'
        paragraph = Paragraph(header_with_anchor, styles["heading1"])

        # Create bookmark data
        bookmark = self.create_bookmark_data(title, bookmark_level)

        return paragraph, bookmark

    def create_cross_reference(self, target_title, link_text, styles):
        """
        Create a cross-reference link to another section

        Parameters:
        -----------
        target_title : str
            Title of the target section
        link_text : str
            Text to display for the link
        styles : dict
            Dictionary of paragraph styles

        Returns:
        --------
        Paragraph
            Paragraph with hyperlink
        """
        anchor_name = f"section_{target_title.lower().replace(' ', '_')}"
        link = f'<a href="#{anchor_name}" color="blue">{link_text}</a>'
        return Paragraph(link, styles["normal"])

    def create_navigation_bar(self, sections, current_section, styles):
        """
        Create a navigation bar for the document

        Parameters:
        -----------
        sections : list
            List of section titles
        current_section : str
            Current section title
        styles : dict
            Dictionary of paragraph styles

        Returns:
        --------
        list
            List of elements for the navigation bar
        """
        elements = []

        # Create a navigation style
        nav_style = ParagraphStyle(
            'Navigation',
            fontName=styles["normal"].fontName,
            fontSize=styles["normal"].fontSize - 2,
            leading=styles["normal"].leading - 2,
            alignment=TA_CENTER,
            textColor=colors.blue
        )

        # Create the navigation links
        nav_links = []
        for section in sections:
            if section == current_section:
                # Current section is not a link
                nav_links.append(f"<b>{section}</b>")
            else:
                # Create a link to the section
                anchor_name = f"section_{section.lower().replace(' ', '_')}"
                nav_links.append(f'<a href="#{anchor_name}">{section}</a>')

        # Join the links with separators
        nav_text = " | ".join(nav_links)
        elements.append(Paragraph(nav_text, nav_style))
        elements.append(Spacer(1, 0.1*inch))

        return elements

    def create_footer_with_page_number(self, canvas, doc, text=""):
        """
        Create a footer with page number

        Parameters:
        -----------
        canvas : Canvas
            ReportLab canvas object
        doc : SimpleDocTemplate
            ReportLab document object
        text : str
            Additional text for the footer
        """
        canvas.saveState()

        # Set the font
        font_name = "DejaVuSans" if self.custom_fonts_available else "Helvetica"
        canvas.setFont(font_name, 9)

        # Draw the page number
        page_num = canvas.getPageNumber()
        page_text = f"Page {page_num}"
        if text:
            page_text = f"{text} | {page_text}"

        # Calculate position
        page_width = doc.pagesize[0]
        canvas.drawCentredString(page_width/2.0, 0.5*inch, page_text)

        canvas.restoreState()

    def create_external_link(self, url, text, styles):
        """
        Create an external hyperlink

        Parameters:
        -----------
        url : str
            URL for the hyperlink
        text : str
            Text to display for the link
        styles : dict
            Dictionary of paragraph styles

        Returns:
        --------
        Paragraph
            Paragraph with external hyperlink
        """
        link = f'<a href="{url}">{text}</a>'
        return Paragraph(link, styles["normal"])

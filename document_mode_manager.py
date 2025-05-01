#!/usr/bin/env python3
"""
Document Mode Manager

This module provides functions for managing different document modes
(academic, professional, resume, scientific) for PDF documents.
"""

import os
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

class DocumentModeManager:
    """
    Document Mode Manager
    
    This class provides methods for managing different document modes
    for PDF documents.
    """
    
    def __init__(self):
        """Initialize the document mode manager"""
        # Define available modes
        self.available_modes = [
            "academic", 
            "professional", 
            "scientific", 
            "resume", 
            "presentation"
        ]
    
    def get_mode_styles(self, mode="professional", base_font="Helvetica"):
        """
        Get styles for a specific document mode
        
        Parameters:
        -----------
        mode : str
            Document mode (academic, professional, scientific, resume, presentation)
        base_font : str
            Base font for the document
            
        Returns:
        --------
        dict
            Dictionary of paragraph styles for the mode
        """
        # Get base styles
        base_styles = getSampleStyleSheet()
        
        # Create a dictionary for the mode styles
        styles = {}
        
        # Add common styles
        styles["normal"] = base_styles["Normal"].clone("normal")
        styles["normal"].fontName = base_font
        
        # Configure mode-specific styles
        if mode == "academic":
            return self._get_academic_styles(base_styles, base_font)
        elif mode == "professional":
            return self._get_professional_styles(base_styles, base_font)
        elif mode == "scientific":
            return self._get_scientific_styles(base_styles, base_font)
        elif mode == "resume":
            return self._get_resume_styles(base_styles, base_font)
        elif mode == "presentation":
            return self._get_presentation_styles(base_styles, base_font)
        else:
            # Default to professional mode
            return self._get_professional_styles(base_styles, base_font)
    
    def _get_academic_styles(self, base_styles, base_font):
        """
        Get styles for academic mode
        
        Parameters:
        -----------
        base_styles : dict
            Base styles from getSampleStyleSheet()
        base_font : str
            Base font for the document
            
        Returns:
        --------
        dict
            Dictionary of paragraph styles for academic mode
        """
        styles = {}
        
        # Title and headings
        styles["title"] = ParagraphStyle(
            "Title",
            fontName=f"{base_font}-Bold",
            fontSize=16,
            leading=20,
            alignment=TA_CENTER,
            spaceAfter=12
        )
        
        styles["subtitle"] = ParagraphStyle(
            "Subtitle",
            fontName=base_font,
            fontSize=12,
            leading=16,
            alignment=TA_CENTER,
            spaceAfter=24
        )
        
        styles["heading1"] = ParagraphStyle(
            "Heading1",
            fontName=f"{base_font}-Bold",
            fontSize=14,
            leading=18,
            alignment=TA_LEFT,
            spaceBefore=12,
            spaceAfter=6
        )
        
        styles["heading2"] = ParagraphStyle(
            "Heading2",
            fontName=f"{base_font}-Bold",
            fontSize=12,
            leading=16,
            alignment=TA_LEFT,
            spaceBefore=10,
            spaceAfter=4
        )
        
        styles["heading3"] = ParagraphStyle(
            "Heading3",
            fontName=f"{base_font}-Bold",
            fontSize=11,
            leading=14,
            alignment=TA_LEFT,
            spaceBefore=8,
            spaceAfter=4
        )
        
        # Body text
        styles["normal"] = ParagraphStyle(
            "Normal",
            fontName=base_font,
            fontSize=10,
            leading=14,
            alignment=TA_JUSTIFY,
            firstLineIndent=18
        )
        
        # Abstract
        styles["abstract"] = ParagraphStyle(
            "Abstract",
            fontName=base_font,
            fontSize=10,
            leading=14,
            alignment=TA_JUSTIFY,
            leftIndent=36,
            rightIndent=36,
            spaceBefore=12,
            spaceAfter=12
        )
        
        # References
        styles["reference"] = ParagraphStyle(
            "Reference",
            fontName=base_font,
            fontSize=9,
            leading=12,
            alignment=TA_LEFT,
            leftIndent=18,
            firstLineIndent=-18
        )
        
        # Caption
        styles["caption"] = ParagraphStyle(
            "Caption",
            fontName=f"{base_font}-Oblique",
            fontSize=9,
            leading=12,
            alignment=TA_CENTER,
            spaceBefore=4,
            spaceAfter=12
        )
        
        # Equation
        styles["equation"] = ParagraphStyle(
            "Equation",
            fontName=base_font,
            fontSize=10,
            leading=14,
            alignment=TA_CENTER,
            spaceBefore=6,
            spaceAfter=6
        )
        
        # Bullet and numbered lists
        styles["bullet"] = ParagraphStyle(
            "Bullet",
            parent=base_styles["Normal"],
            fontName=base_font,
            fontSize=10,
            leading=14,
            leftIndent=18,
            bulletIndent=0
        )
        
        styles["numbered"] = ParagraphStyle(
            "Numbered",
            parent=base_styles["Normal"],
            fontName=base_font,
            fontSize=10,
            leading=14,
            leftIndent=18,
            bulletIndent=0
        )
        
        return styles
    
    def _get_professional_styles(self, base_styles, base_font):
        """
        Get styles for professional mode
        
        Parameters:
        -----------
        base_styles : dict
            Base styles from getSampleStyleSheet()
        base_font : str
            Base font for the document
            
        Returns:
        --------
        dict
            Dictionary of paragraph styles for professional mode
        """
        styles = {}
        
        # Title and headings
        styles["title"] = ParagraphStyle(
            "Title",
            fontName=f"{base_font}-Bold",
            fontSize=20,
            leading=24,
            alignment=TA_CENTER,
            spaceAfter=12,
            textColor=colors.darkblue
        )
        
        styles["subtitle"] = ParagraphStyle(
            "Subtitle",
            fontName=base_font,
            fontSize=14,
            leading=18,
            alignment=TA_CENTER,
            spaceAfter=24,
            textColor=colors.darkblue
        )
        
        styles["heading1"] = ParagraphStyle(
            "Heading1",
            fontName=f"{base_font}-Bold",
            fontSize=16,
            leading=20,
            alignment=TA_LEFT,
            spaceBefore=12,
            spaceAfter=6,
            textColor=colors.darkblue
        )
        
        styles["heading2"] = ParagraphStyle(
            "Heading2",
            fontName=f"{base_font}-Bold",
            fontSize=14,
            leading=18,
            alignment=TA_LEFT,
            spaceBefore=10,
            spaceAfter=4,
            textColor=colors.darkblue
        )
        
        styles["heading3"] = ParagraphStyle(
            "Heading3",
            fontName=f"{base_font}-Bold",
            fontSize=12,
            leading=16,
            alignment=TA_LEFT,
            spaceBefore=8,
            spaceAfter=4,
            textColor=colors.darkblue
        )
        
        # Body text
        styles["normal"] = ParagraphStyle(
            "Normal",
            fontName=base_font,
            fontSize=11,
            leading=15,
            alignment=TA_JUSTIFY
        )
        
        # Executive summary
        styles["summary"] = ParagraphStyle(
            "Summary",
            fontName=base_font,
            fontSize=11,
            leading=15,
            alignment=TA_JUSTIFY,
            leftIndent=36,
            rightIndent=36,
            spaceBefore=12,
            spaceAfter=12,
            borderWidth=1,
            borderColor=colors.lightgrey,
            borderPadding=6,
            borderRadius=6
        )
        
        # Caption
        styles["caption"] = ParagraphStyle(
            "Caption",
            fontName=f"{base_font}-Oblique",
            fontSize=10,
            leading=14,
            alignment=TA_CENTER,
            spaceBefore=4,
            spaceAfter=12
        )
        
        # Bullet and numbered lists
        styles["bullet"] = ParagraphStyle(
            "Bullet",
            parent=base_styles["Normal"],
            fontName=base_font,
            fontSize=11,
            leading=15,
            leftIndent=18,
            bulletIndent=0
        )
        
        styles["numbered"] = ParagraphStyle(
            "Numbered",
            parent=base_styles["Normal"],
            fontName=base_font,
            fontSize=11,
            leading=15,
            leftIndent=18,
            bulletIndent=0
        )
        
        # Equation
        styles["equation"] = ParagraphStyle(
            "Equation",
            fontName=base_font,
            fontSize=11,
            leading=15,
            alignment=TA_CENTER,
            spaceBefore=6,
            spaceAfter=6
        )
        
        return styles
    
    def _get_scientific_styles(self, base_styles, base_font):
        """
        Get styles for scientific mode
        
        Parameters:
        -----------
        base_styles : dict
            Base styles from getSampleStyleSheet()
        base_font : str
            Base font for the document
            
        Returns:
        --------
        dict
            Dictionary of paragraph styles for scientific mode
        """
        styles = {}
        
        # Title and headings
        styles["title"] = ParagraphStyle(
            "Title",
            fontName=f"{base_font}-Bold",
            fontSize=18,
            leading=22,
            alignment=TA_CENTER,
            spaceAfter=12
        )
        
        styles["subtitle"] = ParagraphStyle(
            "Subtitle",
            fontName=base_font,
            fontSize=14,
            leading=18,
            alignment=TA_CENTER,
            spaceAfter=24
        )
        
        styles["heading1"] = ParagraphStyle(
            "Heading1",
            fontName=f"{base_font}-Bold",
            fontSize=14,
            leading=18,
            alignment=TA_LEFT,
            spaceBefore=12,
            spaceAfter=6
        )
        
        styles["heading2"] = ParagraphStyle(
            "Heading2",
            fontName=f"{base_font}-Bold",
            fontSize=12,
            leading=16,
            alignment=TA_LEFT,
            spaceBefore=10,
            spaceAfter=4
        )
        
        styles["heading3"] = ParagraphStyle(
            "Heading3",
            fontName=f"{base_font}-Bold",
            fontSize=11,
            leading=14,
            alignment=TA_LEFT,
            spaceBefore=8,
            spaceAfter=4
        )
        
        # Body text
        styles["normal"] = ParagraphStyle(
            "Normal",
            fontName=base_font,
            fontSize=10,
            leading=14,
            alignment=TA_JUSTIFY
        )
        
        # Abstract
        styles["abstract"] = ParagraphStyle(
            "Abstract",
            fontName=base_font,
            fontSize=10,
            leading=14,
            alignment=TA_JUSTIFY,
            leftIndent=36,
            rightIndent=36,
            spaceBefore=12,
            spaceAfter=12
        )
        
        # Methods
        styles["methods"] = ParagraphStyle(
            "Methods",
            fontName=base_font,
            fontSize=9,
            leading=12,
            alignment=TA_JUSTIFY
        )
        
        # References
        styles["reference"] = ParagraphStyle(
            "Reference",
            fontName=base_font,
            fontSize=9,
            leading=12,
            alignment=TA_LEFT,
            leftIndent=18,
            firstLineIndent=-18
        )
        
        # Caption
        styles["caption"] = ParagraphStyle(
            "Caption",
            fontName=f"{base_font}-Oblique",
            fontSize=9,
            leading=12,
            alignment=TA_CENTER,
            spaceBefore=4,
            spaceAfter=12
        )
        
        # Equation
        styles["equation"] = ParagraphStyle(
            "Equation",
            fontName=base_font,
            fontSize=10,
            leading=14,
            alignment=TA_CENTER,
            spaceBefore=6,
            spaceAfter=6
        )
        
        # Bullet and numbered lists
        styles["bullet"] = ParagraphStyle(
            "Bullet",
            parent=base_styles["Normal"],
            fontName=base_font,
            fontSize=10,
            leading=14,
            leftIndent=18,
            bulletIndent=0
        )
        
        styles["numbered"] = ParagraphStyle(
            "Numbered",
            parent=base_styles["Normal"],
            fontName=base_font,
            fontSize=10,
            leading=14,
            leftIndent=18,
            bulletIndent=0
        )
        
        return styles
    
    def _get_resume_styles(self, base_styles, base_font):
        """
        Get styles for resume mode
        
        Parameters:
        -----------
        base_styles : dict
            Base styles from getSampleStyleSheet()
        base_font : str
            Base font for the document
            
        Returns:
        --------
        dict
            Dictionary of paragraph styles for resume mode
        """
        styles = {}
        
        # Name and contact
        styles["name"] = ParagraphStyle(
            "Name",
            fontName=f"{base_font}-Bold",
            fontSize=18,
            leading=22,
            alignment=TA_CENTER,
            spaceAfter=6
        )
        
        styles["contact"] = ParagraphStyle(
            "Contact",
            fontName=base_font,
            fontSize=10,
            leading=14,
            alignment=TA_CENTER,
            spaceAfter=12
        )
        
        # Section headings
        styles["section"] = ParagraphStyle(
            "Section",
            fontName=f"{base_font}-Bold",
            fontSize=12,
            leading=16,
            alignment=TA_LEFT,
            spaceBefore=12,
            spaceAfter=6,
            borderWidth=0,
            borderColor=colors.black,
            borderPadding=0,
            borderRadius=0,
            textColor=colors.black,
            backColor=colors.lightgrey
        )
        
        # Job title and company
        styles["job_title"] = ParagraphStyle(
            "JobTitle",
            fontName=f"{base_font}-Bold",
            fontSize=11,
            leading=15,
            alignment=TA_LEFT,
            spaceBefore=6,
            spaceAfter=2
        )
        
        styles["company"] = ParagraphStyle(
            "Company",
            fontName=f"{base_font}-Oblique",
            fontSize=10,
            leading=14,
            alignment=TA_LEFT,
            spaceAfter=2
        )
        
        styles["date_range"] = ParagraphStyle(
            "DateRange",
            fontName=base_font,
            fontSize=10,
            leading=14,
            alignment=TA_RIGHT,
            spaceAfter=2
        )
        
        # Body text
        styles["normal"] = ParagraphStyle(
            "Normal",
            fontName=base_font,
            fontSize=10,
            leading=14,
            alignment=TA_LEFT
        )
        
        # Bullet and numbered lists
        styles["bullet"] = ParagraphStyle(
            "Bullet",
            parent=base_styles["Normal"],
            fontName=base_font,
            fontSize=10,
            leading=14,
            leftIndent=18,
            bulletIndent=0
        )
        
        styles["numbered"] = ParagraphStyle(
            "Numbered",
            parent=base_styles["Normal"],
            fontName=base_font,
            fontSize=10,
            leading=14,
            leftIndent=18,
            bulletIndent=0
        )
        
        # Skills
        styles["skill_category"] = ParagraphStyle(
            "SkillCategory",
            fontName=f"{base_font}-Bold",
            fontSize=10,
            leading=14,
            alignment=TA_LEFT,
            spaceBefore=6,
            spaceAfter=2
        )
        
        styles["skill_list"] = ParagraphStyle(
            "SkillList",
            fontName=base_font,
            fontSize=10,
            leading=14,
            alignment=TA_LEFT,
            spaceAfter=4
        )
        
        return styles
    
    def _get_presentation_styles(self, base_styles, base_font):
        """
        Get styles for presentation mode
        
        Parameters:
        -----------
        base_styles : dict
            Base styles from getSampleStyleSheet()
        base_font : str
            Base font for the document
            
        Returns:
        --------
        dict
            Dictionary of paragraph styles for presentation mode
        """
        styles = {}
        
        # Title and headings
        styles["title"] = ParagraphStyle(
            "Title",
            fontName=f"{base_font}-Bold",
            fontSize=24,
            leading=28,
            alignment=TA_CENTER,
            spaceAfter=24,
            textColor=colors.darkblue
        )
        
        styles["subtitle"] = ParagraphStyle(
            "Subtitle",
            fontName=base_font,
            fontSize=18,
            leading=22,
            alignment=TA_CENTER,
            spaceAfter=36,
            textColor=colors.darkblue
        )
        
        styles["heading1"] = ParagraphStyle(
            "Heading1",
            fontName=f"{base_font}-Bold",
            fontSize=20,
            leading=24,
            alignment=TA_LEFT,
            spaceBefore=24,
            spaceAfter=12,
            textColor=colors.darkblue
        )
        
        styles["heading2"] = ParagraphStyle(
            "Heading2",
            fontName=f"{base_font}-Bold",
            fontSize=16,
            leading=20,
            alignment=TA_LEFT,
            spaceBefore=18,
            spaceAfter=8,
            textColor=colors.darkblue
        )
        
        # Body text
        styles["normal"] = ParagraphStyle(
            "Normal",
            fontName=base_font,
            fontSize=14,
            leading=18,
            alignment=TA_LEFT,
            spaceBefore=6,
            spaceAfter=6
        )
        
        # Bullet and numbered lists
        styles["bullet"] = ParagraphStyle(
            "Bullet",
            parent=base_styles["Normal"],
            fontName=base_font,
            fontSize=14,
            leading=18,
            leftIndent=36,
            bulletIndent=18,
            spaceBefore=4,
            spaceAfter=4
        )
        
        styles["numbered"] = ParagraphStyle(
            "Numbered",
            parent=base_styles["Normal"],
            fontName=base_font,
            fontSize=14,
            leading=18,
            leftIndent=36,
            bulletIndent=18,
            spaceBefore=4,
            spaceAfter=4
        )
        
        # Caption
        styles["caption"] = ParagraphStyle(
            "Caption",
            fontName=f"{base_font}-Oblique",
            fontSize=12,
            leading=16,
            alignment=TA_CENTER,
            spaceBefore=4,
            spaceAfter=12
        )
        
        # Equation
        styles["equation"] = ParagraphStyle(
            "Equation",
            fontName=base_font,
            fontSize=14,
            leading=18,
            alignment=TA_CENTER,
            spaceBefore=12,
            spaceAfter=12
        )
        
        return styles

# Main function for command-line usage
def main():
    """Main function for command-line usage"""
    manager = DocumentModeManager()
    
    # Print available modes
    print("Available document modes:")
    for mode in manager.available_modes:
        print(f"- {mode}")
    
    # Get styles for each mode
    for mode in manager.available_modes:
        styles = manager.get_mode_styles(mode)
        print(f"\nStyles for {mode} mode:")
        for style_name in styles:
            print(f"- {style_name}")

if __name__ == "__main__":
    main()

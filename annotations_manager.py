#!/usr/bin/env python3
"""
Annotations Manager

This module provides functions for adding annotations, bookmarks, and
other interactive elements to PDF documents.
"""

import os
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Flowable, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

class AnnotationBox(Flowable):
    """
    Annotation Box Flowable
    
    This class creates a flowable object that can be added to a PDF document
    and contains an annotation (note, highlight, etc.).
    """
    
    def __init__(self, width, height, text, annotation_type="note", 
                background_color=colors.lightgrey, border_color=colors.black,
                text_color=colors.black):
        """
        Initialize the annotation box
        
        Parameters:
        -----------
        width : float
            Width of the annotation box in points
        height : float
            Height of the annotation box in points
        text : str
            Text for the annotation
        annotation_type : str
            Type of annotation (note, highlight, comment)
        background_color : Color
            Background color for the annotation box
        border_color : Color
            Border color for the annotation box
        text_color : Color
            Text color for the annotation
        """
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.text = text
        self.annotation_type = annotation_type
        self.background_color = background_color
        self.border_color = border_color
        self.text_color = text_color
    
    def draw(self):
        """Draw the annotation box on the canvas"""
        # Draw the box
        self.canv.setFillColor(self.background_color)
        self.canv.setStrokeColor(self.border_color)
        self.canv.roundRect(0, 0, self.width, self.height, 5, fill=1, stroke=1)
        
        # Draw the annotation type icon
        self.canv.setFillColor(self.border_color)
        if self.annotation_type == "note":
            # Draw a note icon
            self.canv.circle(15, self.height - 15, 10, fill=1, stroke=0)
            self.canv.setFillColor(colors.white)
            self.canv.drawCentredString(15, self.height - 18, "N")
        elif self.annotation_type == "highlight":
            # Draw a highlight icon
            self.canv.setFillColor(colors.yellow)
            self.canv.rect(5, self.height - 25, 20, 20, fill=1, stroke=0)
            self.canv.setFillColor(self.border_color)
            self.canv.drawCentredString(15, self.height - 18, "H")
        elif self.annotation_type == "comment":
            # Draw a comment icon
            self.canv.setFillColor(colors.lightblue)
            self.canv.rect(5, self.height - 25, 20, 20, fill=1, stroke=0)
            self.canv.setFillColor(self.border_color)
            self.canv.drawCentredString(15, self.height - 18, "C")
        
        # Draw the text
        self.canv.setFillColor(self.text_color)
        self.canv.setFont("Helvetica", 10)
        
        # Split the text into lines
        text_lines = self._wrap_text(self.text, self.width - 40)
        
        # Draw each line
        y = self.height - 40
        for line in text_lines:
            self.canv.drawString(30, y, line)
            y -= 15
    
    def _wrap_text(self, text, width):
        """
        Wrap text to fit within a given width
        
        Parameters:
        -----------
        text : str
            Text to wrap
        width : float
            Width to wrap the text to
            
        Returns:
        --------
        list
            List of wrapped text lines
        """
        # Simple text wrapping
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if self.canv.stringWidth(test_line, "Helvetica", 10) <= width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines

class Bookmark(Flowable):
    """
    Bookmark Flowable
    
    This class creates a flowable object that can be added to a PDF document
    and contains a bookmark.
    """
    
    def __init__(self, text, level=0):
        """
        Initialize the bookmark
        
        Parameters:
        -----------
        text : str
            Text for the bookmark
        level : int
            Level of the bookmark (0 for top level)
        """
        Flowable.__init__(self)
        self.text = text
        self.level = level
        self.width = 0
        self.height = 0
    
    def draw(self):
        """Add the bookmark to the document"""
        # Add the bookmark to the document
        key = f"bookmark_{self.text.lower().replace(' ', '_')}"
        self.canv.bookmarkPage(key)
        self.canv.addOutlineEntry(self.text, key, self.level)

class AnnotationsManager:
    """
    Annotations Manager
    
    This class provides methods for adding annotations, bookmarks, and
    other interactive elements to PDF documents.
    """
    
    def __init__(self, output_dir="gfx/pdf/annotations"):
        """
        Initialize the annotations manager
        
        Parameters:
        -----------
        output_dir : str
            Directory to save annotation images (will be created if it doesn't exist)
        """
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
    
    def create_note_annotation(self, text, width=3*inch, height=1.5*inch):
        """
        Create a note annotation
        
        Parameters:
        -----------
        text : str
            Text for the annotation
        width : float
            Width of the annotation box
        height : float
            Height of the annotation box
            
        Returns:
        --------
        AnnotationBox
            Annotation box flowable
        """
        return AnnotationBox(
            width, height, text, "note", 
            colors.lightgrey, colors.darkblue, colors.black
        )
    
    def create_highlight_annotation(self, text, width=3*inch, height=1.5*inch):
        """
        Create a highlight annotation
        
        Parameters:
        -----------
        text : str
            Text for the annotation
        width : float
            Width of the annotation box
        height : float
            Height of the annotation box
            
        Returns:
        --------
        AnnotationBox
            Annotation box flowable
        """
        return AnnotationBox(
            width, height, text, "highlight", 
            colors.lightyellow, colors.orange, colors.black
        )
    
    def create_comment_annotation(self, text, width=3*inch, height=1.5*inch):
        """
        Create a comment annotation
        
        Parameters:
        -----------
        text : str
            Text for the annotation
        width : float
            Width of the annotation box
        height : float
            Height of the annotation box
            
        Returns:
        --------
        AnnotationBox
            Annotation box flowable
        """
        return AnnotationBox(
            width, height, text, "comment", 
            colors.lightblue, colors.blue, colors.black
        )
    
    def create_bookmark(self, text, level=0):
        """
        Create a bookmark
        
        Parameters:
        -----------
        text : str
            Text for the bookmark
        level : int
            Level of the bookmark (0 for top level)
            
        Returns:
        --------
        Bookmark
            Bookmark flowable
        """
        return Bookmark(text, level)
    
    def create_annotation_section(self, title, annotations):
        """
        Create a section with annotations
        
        Parameters:
        -----------
        title : str
            Title for the section
        annotations : list
            List of annotation flowables
            
        Returns:
        --------
        list
            List of flowables for the section
        """
        elements = []
        
        # Create a title style
        title_style = ParagraphStyle(
            "AnnotationTitle",
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=16,
            alignment=TA_LEFT,
            spaceBefore=12,
            spaceAfter=6,
            textColor=colors.darkblue
        )
        
        # Add the title
        elements.append(Paragraph(title, title_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # Add the annotations
        for annotation in annotations:
            elements.append(annotation)
            elements.append(Spacer(1, 0.2*inch))
        
        return elements

# Main function for command-line usage
def main():
    """Main function for command-line usage"""
    manager = AnnotationsManager()
    
    # Create sample annotations
    note = manager.create_note_annotation(
        "This is a note annotation. It can be used to add notes to the document."
    )
    
    highlight = manager.create_highlight_annotation(
        "This is a highlight annotation. It can be used to highlight important information."
    )
    
    comment = manager.create_comment_annotation(
        "This is a comment annotation. It can be used to add comments to the document."
    )
    
    # Create sample bookmarks
    bookmark1 = manager.create_bookmark("Section 1", 0)
    bookmark2 = manager.create_bookmark("Subsection 1.1", 1)
    
    print("Annotations and bookmarks created successfully!")

if __name__ == "__main__":
    main()

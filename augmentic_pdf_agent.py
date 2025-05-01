#!/usr/bin/env python3
"""
Augmentic PDF Agent

A standalone PDF generation agent that can be extracted to the Augmentic project
for interaction with other agents. This agent creates professional PDF documents
with enhanced styling, scientific display capabilities, and formula rendering.
"""

import os
import sys
import math
import tempfile
import subprocess
import argparse
from datetime import datetime
from io import BytesIO

# ReportLab imports for PDF generation
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table,
    TableStyle, Flowable, ListFlowable, ListItem
)
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Line, Rect, Circle, String
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF

# PIL for image processing
try:
    from PIL import Image as PILImage, ImageDraw, ImageFont, ImageFilter, ImageEnhance
except ImportError:
    print("Warning: PIL/Pillow not available. Some image features will be limited.")

# NumPy and Matplotlib for scientific charts (optional)
try:
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    from matplotlib import cm
    SCIENTIFIC_CHARTS_AVAILABLE = True
except ImportError:
    SCIENTIFIC_CHARTS_AVAILABLE = False
    print("Warning: NumPy/Matplotlib not available. Scientific charts will be limited.")

class PDFAgent:
    """
    Augmentic PDF Agent

    A standalone agent for creating professional PDF documents with enhanced styling,
    scientific display capabilities, and formula rendering.
    """

    def __init__(self, output_dir="gfx/pdf", title="Augmentic PDF Document"):
        """
        Initialize the PDF agent

        Parameters:
        -----------
        output_dir : str
            Directory to save PDF documents and assets
        title : str
            Default title for PDF documents
        """
        self.title = title
        self.output_dir = output_dir

        # Create output directories
        self.output_dir = output_dir
        self.docs_dir = os.path.join(output_dir, "docs")
        self.graphics_dir = os.path.join(output_dir, "graphics")
        self.formulas_dir = os.path.join(output_dir, "formulas")

        # Ensure all directories exist
        for directory in [output_dir, self.docs_dir, self.graphics_dir, self.formulas_dir]:
            os.makedirs(directory, exist_ok=True)

        # Initialize styles
        self.styles = self._create_default_styles()

    def _create_default_styles(self):
        """Create default styles for PDF documents"""
        styles = getSampleStyleSheet()

        # Enhance the default styles
        # Update existing styles
        styles['Title'].fontSize = 24
        styles['Title'].leading = 28
        styles['Title'].alignment = TA_CENTER
        styles['Title'].spaceAfter = 24
        styles['Title'].textColor = colors.darkblue

        styles['Heading1'].fontSize = 16
        styles['Heading1'].leading = 20
        styles['Heading1'].spaceBefore = 12
        styles['Heading1'].spaceAfter = 6
        styles['Heading1'].textColor = colors.darkblue

        styles['Heading2'].fontSize = 14
        styles['Heading2'].leading = 18
        styles['Heading2'].spaceBefore = 10
        styles['Heading2'].spaceAfter = 4
        styles['Heading2'].textColor = colors.darkblue

        styles['Normal'].fontSize = 11
        styles['Normal'].leading = 14
        styles['Normal'].spaceBefore = 6
        styles['Normal'].spaceAfter = 6

        # Define custom styles
        custom_styles = {
            'Subtitle': ParagraphStyle(
                name='Subtitle',
                parent=styles['Normal'],
                fontSize=18,
                leading=22,
                alignment=TA_CENTER,
                spaceAfter=12,
                textColor=colors.darkblue
            ),
            'Caption': ParagraphStyle(
                name='Caption',
                parent=styles['Normal'],
                fontSize=10,
                leading=12,
                alignment=TA_CENTER,
                fontName='Helvetica-Oblique',
                spaceBefore=4,
                spaceAfter=12
            ),
            'Code': ParagraphStyle(
                name='Code',
                parent=styles['Normal'],
                fontName='Courier',
                fontSize=9,
                leading=12,
                leftIndent=36,
                rightIndent=36,
                spaceBefore=6,
                spaceAfter=6
            ),
            'Bullet': ParagraphStyle(
                name='Bullet',
                parent=styles['Normal'],
                leftIndent=18,
                firstLineIndent=0,
                spaceBefore=3,
                spaceAfter=3,
                bulletIndent=0,
                bulletFontName='Symbol',
                bulletFontSize=10
            )
        }

        # Add or update custom styles
        for name, style in custom_styles.items():
            if name in styles:
                # Update existing style
                for attr, value in style.__dict__.items():
                    if attr != 'name' and not attr.startswith('_'):
                        setattr(styles[name], attr, value)
            else:
                # Add new style
                styles.add(style)

        return styles

    def set_style_theme(self, theme="professional"):
        """
        Set the style theme for the PDF document

        Parameters:
        -----------
        theme : str
            Style theme to use (professional, scientific, elegant)
        """
        if theme == "professional":
            self.styles["Title"].textColor = colors.darkblue
            self.styles["Heading1"].textColor = colors.darkblue
            self.styles["Heading2"].textColor = colors.darkblue
        elif theme == "scientific":
            self.styles["Title"].textColor = colors.black
            self.styles["Heading1"].textColor = colors.black
            self.styles["Heading2"].textColor = colors.black
        elif theme == "elegant":
            self.styles["Title"].textColor = colors.darkgreen
            self.styles["Heading1"].textColor = colors.darkgreen
            self.styles["Heading2"].textColor = colors.darkgreen

    def create_pdf(self, content, filename="document.pdf", title=None, author=None, subject=None):
        """
        Create a PDF document with the given content

        Parameters:
        -----------
        content : dict
            Dictionary containing the document content:
            - title: Document title
            - subtitle: Document subtitle (optional)
            - sections: List of sections, each containing:
              - title: Section title
              - content: Section content (text, lists, tables, images, etc.)
        filename : str
            Name of the output file
        title : str
            Document title (overrides content['title'])
        author : str
            Document author
        subject : str
            Document subject

        Returns:
        --------
        str
            Path to the saved PDF document
        """
        # Define the output file
        output_file = os.path.join(self.docs_dir, filename)

        # Create a PDF document
        doc = SimpleDocTemplate(
            output_file,
            pagesize=letter,
            title=title or content.get('title', self.title),
            author=author or "Augmentic PDF Agent",
            subject=subject or "Generated Document",
            leftMargin=0.5*inch,
            rightMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )

        # Build the document
        elements = []

        # Add title and subtitle
        if 'title' in content:
            elements.append(Paragraph(content['title'], self.styles["Title"]))

        if 'subtitle' in content:
            elements.append(Paragraph(content['subtitle'], self.styles["Subtitle"]))

        elements.append(Spacer(1, 0.25*inch))

        # Add sections
        for section in content.get('sections', []):
            # Add section title
            if 'title' in section:
                elements.append(Paragraph(section['title'], self.styles["Heading1"]))

            # Add page break if requested
            if 'page_break' in section and section['page_break']:
                elements.append(PageBreak())
                continue

            # Add section content
            if 'text' in section:
                elements.append(Paragraph(section['text'], self.styles["Normal"]))

            # Add bullet lists
            if 'bullet_list' in section:
                elements.extend(self._create_bullet_list(section['bullet_list']))

            # Add tables
            if 'table' in section:
                elements.append(self._create_table(section['table']))
                if 'table_caption' in section:
                    elements.append(Paragraph(section['table_caption'], self.styles["Caption"]))

            # Add images
            if 'image' in section:
                img_path = section['image']
                if os.path.exists(img_path):
                    img_width = section.get('image_width', 6*inch)
                    img_height = section.get('image_height', 4*inch)
                    elements.append(Image(img_path, width=img_width, height=img_height))
                    if 'image_caption' in section:
                        elements.append(Paragraph(section['image_caption'], self.styles["Caption"]))

            # Add charts
            if 'chart' in section and SCIENTIFIC_CHARTS_AVAILABLE:
                chart_data = section['chart']
                chart_path = self._create_chart(
                    chart_data['type'],
                    chart_data['data'],
                    chart_data.get('title', ''),
                    chart_data.get('x_label', ''),
                    chart_data.get('y_label', '')
                )
                if chart_path:
                    img_width = section.get('chart_width', 6*inch)
                    img_height = section.get('chart_height', 4*inch)
                    elements.append(Image(chart_path, width=img_width, height=img_height))
                    if 'chart_caption' in section:
                        elements.append(Paragraph(section['chart_caption'], self.styles["Caption"]))

            # Add formulas
            if 'formula' in section:
                formula = section['formula']
                formula_path = self._create_formula_image(
                    formula['name'],
                    formula['equation'],
                    formula.get('description', '')
                )
                if formula_path:
                    elements.append(Image(formula_path, width=6*inch, height=1.5*inch))
                    if 'description' in formula:
                        elements.append(Paragraph(formula['description'], self.styles["Normal"]))

            # Add code blocks
            if 'code' in section:
                elements.append(Paragraph(section['code'], self.styles["Code"]))

            # Add text after bullets if provided
            if 'text_after_bullets' in section:
                elements.append(Paragraph(section['text_after_bullets'], self.styles["Normal"]))

            # Add spacer after each section
            elements.append(Spacer(1, 0.2*inch))

        # Define a function for the footer with page numbers
        def add_page_numbers(canvas, doc):
            canvas.saveState()
            canvas.setFont('Helvetica', 9)
            page_num = canvas.getPageNumber()
            text = f"Page {page_num}"
            canvas.drawRightString(doc.pagesize[0] - 0.5*inch, 0.5*inch, text)
            canvas.restoreState()

        # Build the PDF
        try:
            doc.build(elements, onFirstPage=add_page_numbers, onLaterPages=add_page_numbers)
            print(f"PDF document saved to: {output_file}")
            return output_file
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            return None

    def _create_bullet_list(self, items):
        """Create a bullet list from the given items"""
        elements = []
        for item in items:
            if isinstance(item, str):
                elements.append(Paragraph(f"• {item}", self.styles["Bullet"]))
            elif isinstance(item, dict) and 'text' in item:
                elements.append(Paragraph(f"• {item['text']}", self.styles["Bullet"]))
                # Handle nested lists
                if 'subitems' in item:
                    for subitem in item['subitems']:
                        elements.append(Paragraph(f"  - {subitem}", self.styles["Bullet"]))
        return elements

    def _create_table(self, data, col_widths=None):
        """Create a table from the given data"""
        if not data:
            return None

        # Calculate column widths if not provided
        if col_widths is None:
            table_width = 7*inch  # Default table width
            col_widths = [table_width / len(data[0])] * len(data[0])

        # Create the table
        table = Table(data, colWidths=col_widths)

        # Add style
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ])
        table.setStyle(style)

        return table

    def _create_chart(self, chart_type, data, title="", x_label="", y_label=""):
        """Create a chart image from the given data"""
        if not SCIENTIFIC_CHARTS_AVAILABLE:
            return None

        # Create a unique filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{chart_type}_{title.lower().replace(' ', '_')}_{timestamp}.png"
        output_file = os.path.join(self.graphics_dir, filename)

        # Create figure
        plt.figure(figsize=(8, 6), dpi=100)

        if chart_type == "line":
            # Create line chart
            for series in data:
                x_values = [point[0] for point in series["data"]]
                y_values = [point[1] for point in series["data"]]
                plt.plot(x_values, y_values, label=series["name"], linewidth=2)

            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.title(title)
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.legend()

        elif chart_type == "bar":
            # Create bar chart
            categories = [item["category"] for item in data]
            values = [item["value"] for item in data]

            plt.bar(categories, values, color='skyblue', edgecolor='navy')
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.title(title)
            plt.grid(True, axis='y', linestyle='--', alpha=0.7)

        elif chart_type == "pie":
            # Create pie chart
            categories = [item["category"] for item in data]
            values = [item["value"] for item in data]

            plt.pie(values, labels=categories, autopct='%1.1f%%',
                   shadow=True, startangle=90,
                   colors=plt.cm.Paired.colors)
            plt.axis('equal')
            plt.title(title)

        elif chart_type == "scatter":
            # Create scatter plot
            for series in data:
                x_values = [point[0] for point in series["data"]]
                y_values = [point[1] for point in series["data"]]
                plt.scatter(x_values, y_values, label=series["name"], s=50, alpha=0.7)

            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.title(title)
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.legend()

        # Save the figure
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()

        return output_file

    def _create_formula_image(self, name, equation, description=""):
        """Create an image for a mathematical formula"""
        # Create a unique filename
        filename = f"{name.lower().replace(' ', '_')}.png"
        output_file = os.path.join(self.formulas_dir, filename)

        # Create a simple image with the formula text
        try:
            # Create a blank image
            img = PILImage.new('RGB', (800, 150), color=(255, 255, 255))
            draw = ImageDraw.Draw(img)

            # Try to load a font
            try:
                font = ImageFont.truetype("Arial", 16)
                small_font = ImageFont.truetype("Arial", 12)
            except:
                font = ImageFont.load_default()
                small_font = ImageFont.load_default()

            # Draw the formula name
            draw.text((20, 20), name, fill=(0, 0, 0), font=font)

            # Draw the equation
            draw.text((20, 60), equation, fill=(0, 0, 0), font=font)

            # Draw the description if provided
            if description:
                draw.text((20, 100), description, fill=(100, 100, 100), font=small_font)

            # Save the image
            img.save(output_file)

            return output_file
        except Exception as e:
            print(f"Error creating formula image: {str(e)}")
            return None

    def create_scientific_document(self, title, content, filename="scientific_document.pdf"):
        """
        Create a scientific document with the given content

        Parameters:
        -----------
        title : str
            Document title
        content : dict
            Dictionary containing the document content
        filename : str
            Name of the output file

        Returns:
        --------
        str
            Path to the saved PDF document
        """
        # Set scientific style theme
        self.set_style_theme("scientific")

        # Create document structure
        doc_content = {
            "title": title,
            "subtitle": content.get("subtitle", ""),
            "sections": []
        }

        # Add abstract if provided
        if "abstract" in content:
            doc_content["sections"].append({
                "title": "Abstract",
                "text": content["abstract"]
            })

        # Add introduction if provided
        if "introduction" in content:
            doc_content["sections"].append({
                "title": "Introduction",
                "text": content["introduction"]
            })

        # Add methods if provided
        if "methods" in content:
            doc_content["sections"].append({
                "title": "Methods",
                "text": content["methods"]
            })

        # Add results if provided
        if "results" in content:
            results_section = {
                "title": "Results",
                "text": content["results"]
            }

            # Add charts if provided
            if "charts" in content:
                for i, chart in enumerate(content["charts"]):
                    results_section[f"chart_{i}"] = chart
                    results_section[f"chart_caption_{i}"] = chart.get("caption", f"Figure {i+1}")

            doc_content["sections"].append(results_section)

        # Add discussion if provided
        if "discussion" in content:
            doc_content["sections"].append({
                "title": "Discussion",
                "text": content["discussion"]
            })

        # Add conclusion if provided
        if "conclusion" in content:
            doc_content["sections"].append({
                "title": "Conclusion",
                "text": content["conclusion"]
            })

        # Add references if provided
        if "references" in content:
            references_section = {
                "title": "References",
            }

            if isinstance(content["references"], list):
                references_section["bullet_list"] = content["references"]
            else:
                references_section["text"] = content["references"]

            doc_content["sections"].append(references_section)

        # Create the PDF document
        return self.create_pdf(
            doc_content,
            filename=filename,
            title=title,
            subject="Scientific Document"
        )

    def create_report(self, title, content, filename="report.pdf"):
        """
        Create a professional report with the given content

        Parameters:
        -----------
        title : str
            Report title
        content : dict
            Dictionary containing the report content
        filename : str
            Name of the output file

        Returns:
        --------
        str
            Path to the saved PDF document
        """
        # Set professional style theme
        self.set_style_theme("professional")

        # Create document structure
        doc_content = {
            "title": title,
            "subtitle": content.get("subtitle", ""),
            "sections": []
        }

        # Add executive summary if provided
        if "executive_summary" in content:
            doc_content["sections"].append({
                "title": "Executive Summary",
                "text": content["executive_summary"]
            })

        # Add main sections
        for section in content.get("sections", []):
            doc_content["sections"].append(section)

        # Add conclusion if provided
        if "conclusion" in content:
            doc_content["sections"].append({
                "title": "Conclusion",
                "text": content["conclusion"]
            })

        # Add appendices if provided
        if "appendices" in content:
            for i, appendix in enumerate(content["appendices"]):
                doc_content["sections"].append({
                    "title": f"Appendix {chr(65+i)}: {appendix.get('title', '')}",
                    "text": appendix.get("text", "")
                })

        # Create the PDF document
        return self.create_pdf(
            doc_content,
            filename=filename,
            title=title,
            subject="Professional Report"
        )

def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(description="Augmentic PDF Agent")
    parser.add_argument("--title", type=str, default="Augmentic PDF Document",
                        help="Document title")
    parser.add_argument("--output", type=str, default="document.pdf",
                        help="Output filename")
    parser.add_argument("--type", type=str, default="document",
                        choices=["document", "scientific", "report"],
                        help="Document type")
    parser.add_argument("--content", type=str, default=None,
                        help="JSON file containing document content")

    args = parser.parse_args()

    # Create PDF agent
    agent = PDFAgent()

    # Create sample content if no content file is provided
    if args.content is None:
        content = {
            "title": args.title,
            "subtitle": "Generated by Augmentic PDF Agent",
            "sections": [
                {
                    "title": "Introduction",
                    "text": "This is a sample document generated by the Augmentic PDF Agent."
                },
                {
                    "title": "Features",
                    "text": "The Augmentic PDF Agent provides the following features:",
                    "bullet_list": [
                        "Professional document styling",
                        "Scientific charts and diagrams",
                        "Mathematical formula rendering",
                        "Tables and lists",
                        "Interactive with other agents"
                    ]
                },
                {
                    "title": "Conclusion",
                    "text": "This document demonstrates the capabilities of the Augmentic PDF Agent."
                }
            ]
        }
    else:
        # Load content from JSON file
        import json
        with open(args.content, 'r') as f:
            content = json.load(f)

    # Create the appropriate document type
    if args.type == "scientific":
        agent.create_scientific_document(args.title, content, args.output)
    elif args.type == "report":
        agent.create_report(args.title, content, args.output)
    else:
        agent.create_pdf(content, args.output)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Enhanced PDF Agent with Graphics Support

This module provides an enhanced PDF agent with graphics capabilities,
improved formula rendering, and better display of mathematical equations.
"""

import os
import io
import math
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle
from reportlab.graphics.shapes import Drawing, Circle, Rect, Line, Polygon, String
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPM
from PIL import Image as PILImage, ImageDraw, ImageFont

class EnhancedPDFAgent:
    """
    Enhanced PDF Agent with Graphics Support
    
    This class provides methods for generating PDFs with advanced features:
    - Improved formula rendering with proper subscripts and superscripts
    - Graphics capabilities for diagrams and charts
    - Better display of mathematical equations
    - Support for custom styling and formatting
    """
    
    def __init__(self, output_dir="docs/pdf"):
        """
        Initialize the enhanced PDF agent
        
        Parameters:
        -----------
        output_dir : str
            Directory to save PDF output (will be created if it doesn't exist)
        """
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Create graphics directory if it doesn't exist
        self.graphics_dir = os.path.join(output_dir, "graphics")
        os.makedirs(self.graphics_dir, exist_ok=True)
    
    def generate_complete_theory_pdf(self):
        """
        Generate an improved PDF for the Complete Theory of Everything
        with proper formula display and graphics
        
        Returns:
        --------
        str
            Path to the saved PDF file
        """
        # Define the output file
        output_file = os.path.join(self.output_dir, "Complete_Theory_of_Everything_ToE.pdf")
        
        # Create a PDF document
        doc = SimpleDocTemplate(output_file, pagesize=letter)
        
        # Define styles
        styles = getSampleStyleSheet()
        
        # Create custom styles
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Title'],
            fontSize=18,
            leading=22,
            alignment=TA_CENTER,
            spaceAfter=20
        )
        
        heading_style = ParagraphStyle(
            'Heading',
            parent=styles['Heading2'],
            fontSize=14,
            leading=18,
            spaceBefore=12,
            spaceAfter=6
        )
        
        normal_style = ParagraphStyle(
            'Normal',
            parent=styles['Normal'],
            fontSize=11,
            leading=14,
            alignment=TA_JUSTIFY
        )
        
        equation_style = ParagraphStyle(
            'Equation',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=16,
            alignment=TA_CENTER,
            spaceBefore=8,
            spaceAfter=8
        )
        
        # Build the document
        elements = []
        
        # Add title
        elements.append(Paragraph("Complete Theory of Everything (ToE)", title_style))
        elements.append(Spacer(1, 10))
        
        # Add introduction
        elements.append(Paragraph("Introduction", heading_style))
        elements.append(Paragraph(
            "The Complete Theory of Everything (ToE) is a comprehensive framework that aims to unify all fundamental "
            "forces and explain all physical phenomena in the universe. This document provides a detailed overview of "
            "the theory, its mathematical foundations, and its implications for our understanding of reality.", 
            normal_style))
        elements.append(Spacer(1, 10))
        
        # Add a conceptual diagram of the unified theory
        elements.append(Paragraph("Conceptual Overview", heading_style))
        elements.append(Paragraph(
            "The following diagram illustrates the conceptual framework of the Complete Theory of Everything, "
            "showing how it unifies the fundamental forces and integrates different physical theories:", 
            normal_style))
        elements.append(Spacer(1, 6))
        
        # Create a conceptual diagram
        diagram_path = self._create_unified_theory_diagram()
        elements.append(Image(diagram_path, width=5*inch, height=3*inch))
        elements.append(Spacer(1, 10))
        
        # Add mathematical foundation
        elements.append(Paragraph("Mathematical Foundation", heading_style))
        elements.append(Paragraph(
            "The Complete Theory of Everything is built upon a sophisticated mathematical framework that integrates "
            "concepts from quantum field theory, general relativity, and advanced geometry.", 
            normal_style))
        elements.append(Spacer(1, 6))
        
        # Add key equations
        elements.append(Paragraph("Key Equations", heading_style))
        
        equations = [
            {
                "name": "Master Equation",
                "equation": "S = S<sub>gravity</sub> + S<sub>matter</sub> + S<sub>gauge</sub> + S<sub>quantum</sub>",
                "description": "The total action is composed of four main parts: gravity, matter, gauge fields, and quantum corrections."
            },
            {
                "name": "Gravity Action",
                "equation": "S<sub>gravity</sub> = 1/(16πG) ∫d<sup>4</sup>x √(-g) (R - 2Λ)",
                "description": "The Einstein-Hilbert action describes classical gravity in terms of spacetime curvature."
            },
            {
                "name": "Matter Action",
                "equation": "S<sub>matter</sub> = ∫d<sup>4</sup>x √(-g) ψ̄(iγ<sup>μ</sup>D<sub>μ</sub> - m)ψ",
                "description": "The Dirac action describes fermions (matter particles) in curved spacetime."
            },
            {
                "name": "Gauge Field Action",
                "equation": "S<sub>gauge</sub> = -1/4 ∫d<sup>4</sup>x √(-g) F<sub>μν</sub><sup>a</sup>F<sup>μν</sup><sub>a</sub>",
                "description": "The Yang-Mills action describes non-Abelian gauge fields that mediate the strong and weak forces."
            },
            {
                "name": "Quantum Corrections",
                "equation": "S<sub>quantum</sub> = ∑<sub>n=1</sub><sup>∞</sup> ℏ<sup>n</sup>S<sub>n</sub>",
                "description": "Quantum corrections account for quantum fluctuations and virtual particles in quantum field theory."
            }
        ]
        
        for equation in equations:
            elements.append(Paragraph(equation["name"], heading_style))
            elements.append(Paragraph(equation["equation"], equation_style))
            elements.append(Paragraph(equation["description"], normal_style))
            elements.append(Spacer(1, 8))
        
        # Add a chart showing the relative strengths of fundamental forces
        elements.append(Paragraph("Fundamental Forces", heading_style))
        elements.append(Paragraph(
            "The Complete Theory of Everything unifies the four fundamental forces of nature. "
            "The following chart shows their relative strengths at different energy scales:", 
            normal_style))
        elements.append(Spacer(1, 6))
        
        # Create a chart of fundamental forces
        chart_path = self._create_forces_chart()
        elements.append(Image(chart_path, width=5*inch, height=3*inch))
        elements.append(Spacer(1, 10))
        
        # Add implications
        elements.append(Paragraph("Implications", heading_style))
        elements.append(Paragraph(
            "The Complete Theory of Everything has profound implications for our understanding of the universe:", 
            normal_style))
        elements.append(Spacer(1, 6))
        
        implications = [
            "Unification of all fundamental forces",
            "Explanation of dark matter and dark energy",
            "Resolution of the black hole information paradox",
            "Prediction of new particles and phenomena",
            "Consistent description of the early universe"
        ]
        
        for i, implication in enumerate(implications):
            elements.append(Paragraph(f"{i+1}. {implication}", normal_style))
            elements.append(Spacer(1, 4))
        
        # Add a diagram of the universe's evolution
        elements.append(Paragraph("Universe Evolution", heading_style))
        elements.append(Paragraph(
            "The Complete Theory of Everything provides a consistent description of the universe's evolution "
            "from the Big Bang to the present day:", 
            normal_style))
        elements.append(Spacer(1, 6))
        
        # Create a diagram of the universe's evolution
        evolution_path = self._create_universe_evolution_diagram()
        elements.append(Image(evolution_path, width=6*inch, height=3*inch))
        elements.append(Spacer(1, 10))
        
        # Add conclusion
        elements.append(Paragraph("Conclusion", heading_style))
        elements.append(Paragraph(
            "The Complete Theory of Everything represents a significant advancement in theoretical physics, "
            "providing a unified framework for understanding the fundamental nature of reality. While further "
            "research and experimental verification are needed, this theory offers a promising path toward "
            "a complete understanding of the physical universe.", 
            normal_style))
        
        # Build the PDF
        try:
            doc.build(elements)
            print(f"Enhanced Complete Theory of Everything PDF saved to: {output_file}")
            return output_file
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            return None
    
    def _create_unified_theory_diagram(self):
        """
        Create a diagram illustrating the unified theory concept
        
        Returns:
        --------
        str
            Path to the saved diagram image
        """
        # Define the output file
        output_file = os.path.join(self.graphics_dir, "unified_theory_diagram.png")
        
        # Create a drawing
        width, height = 500, 300
        img = PILImage.new('RGB', (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        # Draw the central "Unified Theory" circle
        center_x, center_y = width // 2, height // 2
        radius = 50
        draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), 
                     fill=(100, 149, 237), outline=(0, 0, 0))
        
        # Draw the four fundamental forces as smaller circles around the central circle
        force_radius = 30
        force_distance = 120
        forces = [
            {"name": "Gravity", "angle": 45, "color": (255, 165, 0)},
            {"name": "Electromagnetism", "angle": 135, "color": (50, 205, 50)},
            {"name": "Strong Force", "angle": 225, "color": (220, 20, 60)},
            {"name": "Weak Force", "angle": 315, "color": (138, 43, 226)}
        ]
        
        # Try to load a font
        try:
            font = ImageFont.truetype("Arial", 12)
        except IOError:
            font = ImageFont.load_default()
        
        # Draw each force and connect it to the central circle
        for force in forces:
            angle_rad = math.radians(force["angle"])
            force_x = center_x + int(force_distance * math.cos(angle_rad))
            force_y = center_y + int(force_distance * math.sin(angle_rad))
            
            # Draw the force circle
            draw.ellipse((force_x - force_radius, force_y - force_radius, 
                          force_x + force_radius, force_y + force_radius), 
                         fill=force["color"], outline=(0, 0, 0))
            
            # Draw the connecting line
            draw.line((center_x, center_y, force_x, force_y), fill=(0, 0, 0), width=2)
            
            # Add the force name
            text_width = draw.textlength(force["name"], font=font)
            draw.text((force_x - text_width // 2, force_y - 6), force["name"], fill=(0, 0, 0), font=font)
        
        # Add the "Unified Theory" text to the central circle
        text = "Unified Theory"
        text_width = draw.textlength(text, font=font)
        draw.text((center_x - text_width // 2, center_y - 6), text, fill=(0, 0, 0), font=font)
        
        # Save the image
        img.save(output_file)
        
        return output_file
    
    def _create_forces_chart(self):
        """
        Create a chart showing the relative strengths of fundamental forces
        
        Returns:
        --------
        str
            Path to the saved chart image
        """
        # Define the output file
        output_file = os.path.join(self.graphics_dir, "forces_chart.png")
        
        # Create a drawing
        width, height = 500, 300
        img = PILImage.new('RGB', (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        # Define the chart area
        margin = 50
        chart_width = width - 2 * margin
        chart_height = height - 2 * margin
        
        # Draw the axes
        draw.line((margin, height - margin, width - margin, height - margin), fill=(0, 0, 0), width=2)  # x-axis
        draw.line((margin, margin, margin, height - margin), fill=(0, 0, 0), width=2)  # y-axis
        
        # Try to load a font
        try:
            font = ImageFont.truetype("Arial", 12)
            small_font = ImageFont.truetype("Arial", 10)
        except IOError:
            font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Add axis labels
        draw.text((width // 2 - 50, height - 30), "Energy Scale (GeV)", fill=(0, 0, 0), font=font)
        draw.text((10, height // 2 - 50), "Relative Strength", fill=(0, 0, 0), font=font)
        
        # Define the data points for each force
        # x-axis: log(Energy) from 0 to 15
        # y-axis: log(Strength) relative to strong force
        x_points = [0, 3, 6, 9, 12, 15]
        
        strong_force = [(x, 0) for x in x_points]  # Constant at 1 (log=0)
        em_force = [(x, -2 + x/15) for x in x_points]  # Increases with energy
        weak_force = [(x, -4 + 2*x/15) for x in x_points]  # Increases faster
        gravity = [(x, -40 + 3*x/15) for x in x_points]  # Very weak but increases fastest
        
        # Scale the data points to the chart area
        def scale_point(point):
            x, y = point
            scaled_x = margin + (x / 15) * chart_width
            scaled_y = height - margin - ((y + 40) / 40) * chart_height
            return (scaled_x, scaled_y)
        
        strong_force_scaled = [scale_point(p) for p in strong_force]
        em_force_scaled = [scale_point(p) for p in em_force]
        weak_force_scaled = [scale_point(p) for p in weak_force]
        gravity_scaled = [scale_point(p) for p in gravity]
        
        # Draw the lines for each force
        draw.line(strong_force_scaled, fill=(220, 20, 60), width=2)  # Strong force (red)
        draw.line(em_force_scaled, fill=(50, 205, 50), width=2)  # EM force (green)
        draw.line(weak_force_scaled, fill=(138, 43, 226), width=2)  # Weak force (purple)
        draw.line(gravity_scaled, fill=(255, 165, 0), width=2)  # Gravity (orange)
        
        # Add x-axis labels
        for i, x in enumerate(x_points):
            x_pos = margin + (x / 15) * chart_width
            draw.line((x_pos, height - margin, x_pos, height - margin + 5), fill=(0, 0, 0), width=1)
            draw.text((x_pos - 5, height - margin + 10), str(10**x), fill=(0, 0, 0), font=small_font)
        
        # Add a legend
        legend_x = margin + 20
        legend_y = margin + 20
        legend_spacing = 20
        
        # Strong force
        draw.line((legend_x, legend_y, legend_x + 30, legend_y), fill=(220, 20, 60), width=2)
        draw.text((legend_x + 40, legend_y - 6), "Strong Force", fill=(0, 0, 0), font=font)
        
        # EM force
        draw.line((legend_x, legend_y + legend_spacing, legend_x + 30, legend_y + legend_spacing), 
                  fill=(50, 205, 50), width=2)
        draw.text((legend_x + 40, legend_y + legend_spacing - 6), "Electromagnetism", fill=(0, 0, 0), font=font)
        
        # Weak force
        draw.line((legend_x, legend_y + 2 * legend_spacing, legend_x + 30, legend_y + 2 * legend_spacing), 
                  fill=(138, 43, 226), width=2)
        draw.text((legend_x + 40, legend_y + 2 * legend_spacing - 6), "Weak Force", fill=(0, 0, 0), font=font)
        
        # Gravity
        draw.line((legend_x, legend_y + 3 * legend_spacing, legend_x + 30, legend_y + 3 * legend_spacing), 
                  fill=(255, 165, 0), width=2)
        draw.text((legend_x + 40, legend_y + 3 * legend_spacing - 6), "Gravity", fill=(0, 0, 0), font=font)
        
        # Add a unification point
        unification_x = margin + (15 / 15) * chart_width
        unification_y = height - margin - ((0 + 40) / 40) * chart_height
        draw.ellipse((unification_x - 5, unification_y - 5, unification_x + 5, unification_y + 5), 
                     fill=(0, 0, 0), outline=(0, 0, 0))
        draw.text((unification_x - 40, unification_y - 20), "Unification", fill=(0, 0, 0), font=font)
        
        # Save the image
        img.save(output_file)
        
        return output_file
    
    def _create_universe_evolution_diagram(self):
        """
        Create a diagram showing the evolution of the universe
        
        Returns:
        --------
        str
            Path to the saved diagram image
        """
        # Define the output file
        output_file = os.path.join(self.graphics_dir, "universe_evolution.png")
        
        # Create a drawing
        width, height = 600, 300
        img = PILImage.new('RGB', (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        # Try to load a font
        try:
            font = ImageFont.truetype("Arial", 12)
            small_font = ImageFont.truetype("Arial", 10)
        except IOError:
            font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Draw the timeline
        margin = 50
        timeline_y = height // 2
        draw.line((margin, timeline_y, width - margin, timeline_y), fill=(0, 0, 0), width=2)
        
        # Define the key events in the universe's evolution
        events = [
            {"name": "Big Bang", "time": "0 s", "x_pos": 0.0, "description": "Unified forces"},
            {"name": "Inflation", "time": "10⁻³⁵ s", "x_pos": 0.1, "description": "Rapid expansion"},
            {"name": "Quark Era", "time": "10⁻¹² s", "x_pos": 0.2, "description": "Quarks form"},
            {"name": "Nucleosynthesis", "time": "3 min", "x_pos": 0.3, "description": "Nuclei form"},
            {"name": "Recombination", "time": "380,000 yr", "x_pos": 0.5, "description": "Atoms form"},
            {"name": "First Stars", "time": "100 million yr", "x_pos": 0.7, "description": "Stars ignite"},
            {"name": "Present Day", "time": "13.8 billion yr", "x_pos": 1.0, "description": "Current state"}
        ]
        
        # Draw each event on the timeline
        timeline_width = width - 2 * margin
        for event in events:
            x_pos = margin + event["x_pos"] * timeline_width
            
            # Draw a marker on the timeline
            draw.ellipse((x_pos - 5, timeline_y - 5, x_pos + 5, timeline_y + 5), 
                         fill=(0, 0, 255), outline=(0, 0, 0))
            
            # Draw the event name above the timeline
            draw.text((x_pos - 20, timeline_y - 30), event["name"], fill=(0, 0, 0), font=font)
            
            # Draw the time below the timeline
            draw.text((x_pos - 15, timeline_y + 10), event["time"], fill=(0, 0, 0), font=small_font)
            
            # Draw the description below the time
            draw.text((x_pos - 30, timeline_y + 30), event["description"], fill=(0, 0, 0), font=small_font)
        
        # Add a title
        title = "Evolution of the Universe"
        draw.text((width // 2 - 80, 20), title, fill=(0, 0, 0), font=font)
        
        # Save the image
        img.save(output_file)
        
        return output_file

# Main function for command-line usage
def main():
    """Main function for command-line usage"""
    agent = EnhancedPDFAgent()
    agent.generate_complete_theory_pdf()

if __name__ == "__main__":
    main()

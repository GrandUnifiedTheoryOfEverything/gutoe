#!/usr/bin/env python3
"""
Scientific Display Enhancer

This module provides enhanced scientific display capabilities for PDF documents,
including improved formula rendering, scientific charts, and data visualization.
"""

import os
import io
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.units import inch
from reportlab.platypus import Image as ReportLabImage, Paragraph, Spacer, Table
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Circle, Rect, Line, Polygon, String
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics import renderPM

class ScientificDisplayEnhancer:
    """
    Scientific Display Enhancer
    
    This class provides methods for enhancing scientific displays in PDF documents:
    - Advanced formula rendering
    - Scientific charts and graphs
    - Data visualization
    - Molecular structures
    """
    
    def __init__(self, output_dir="docs/pdf/scientific"):
        """
        Initialize the scientific display enhancer
        
        Parameters:
        -----------
        output_dir : str
            Directory to save scientific display images (will be created if it doesn't exist)
        """
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Load fonts
        try:
            self.main_font = ImageFont.truetype("DejaVuSerif.ttf", 24)
            self.sub_font = ImageFont.truetype("DejaVuSerif.ttf", 16)
            self.symbol_font = ImageFont.truetype("DejaVuSansMono.ttf", 24)
        except IOError:
            # Fallback to default font
            self.main_font = ImageFont.load_default()
            self.sub_font = ImageFont.load_default()
            self.symbol_font = ImageFont.load_default()
    
    def create_scientific_chart(self, chart_type, data, title, x_label, y_label, width=500, height=300):
        """
        Create a scientific chart
        
        Parameters:
        -----------
        chart_type : str
            Type of chart to create (line, bar, pie)
        data : dict or list
            Data for the chart
        title : str
            Title of the chart
        x_label : str
            Label for the x-axis
        y_label : str
            Label for the y-axis
        width : int
            Width of the chart
        height : int
            Height of the chart
            
        Returns:
        --------
        str
            Path to the saved chart image
        """
        # Define the output file
        output_file = os.path.join(self.output_dir, f"{title.lower().replace(' ', '_')}.png")
        
        if chart_type == "line":
            return self._create_line_chart(data, title, x_label, y_label, width, height, output_file)
        elif chart_type == "bar":
            return self._create_bar_chart(data, title, x_label, y_label, width, height, output_file)
        elif chart_type == "pie":
            return self._create_pie_chart(data, title, width, height, output_file)
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")
    
    def _create_line_chart(self, data, title, x_label, y_label, width, height, output_file):
        """Create a line chart"""
        # Create a drawing
        img = Image.new('RGB', (width, height), color=(255, 255, 255))
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
        draw.text((width // 2 - 20, height - 20), x_label, fill=(0, 0, 0), font=font)
        draw.text((10, height // 2 - 20), y_label, fill=(0, 0, 0), font=font)
        
        # Add title
        draw.text((width // 2 - 50, 10), title, fill=(0, 0, 0), font=font)
        
        # Process the data
        colors_list = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 165, 0), (128, 0, 128)]
        
        # Find the min and max values for scaling
        all_x = []
        all_y = []
        for series in data:
            all_x.extend([point[0] for point in series["data"]])
            all_y.extend([point[1] for point in series["data"]])
        
        min_x = min(all_x)
        max_x = max(all_x)
        min_y = min(all_y)
        max_y = max(all_y)
        
        # Add some padding
        x_range = max_x - min_x
        y_range = max_y - min_y
        min_x -= 0.05 * x_range
        max_x += 0.05 * x_range
        min_y -= 0.05 * y_range
        max_y += 0.05 * y_range
        
        # Scale function
        def scale_point(point):
            x, y = point
            scaled_x = margin + ((x - min_x) / (max_x - min_x)) * chart_width
            scaled_y = height - margin - ((y - min_y) / (max_y - min_y)) * chart_height
            return (scaled_x, scaled_y)
        
        # Draw each data series
        for i, series in enumerate(data):
            color = colors_list[i % len(colors_list)]
            points = [scale_point(point) for point in series["data"]]
            
            # Draw the line
            draw.line(points, fill=color, width=2)
            
            # Draw points
            for point in points:
                draw.ellipse((point[0] - 3, point[1] - 3, point[0] + 3, point[1] + 3), fill=color, outline=(0, 0, 0))
        
        # Add a legend
        legend_x = margin + 20
        legend_y = margin + 20
        legend_spacing = 20
        
        for i, series in enumerate(data):
            color = colors_list[i % len(colors_list)]
            draw.line((legend_x, legend_y + i * legend_spacing, legend_x + 30, legend_y + i * legend_spacing), 
                      fill=color, width=2)
            draw.text((legend_x + 40, legend_y + i * legend_spacing - 6), series["name"], fill=(0, 0, 0), font=font)
        
        # Save the image
        img.save(output_file)
        
        return output_file
    
    def _create_bar_chart(self, data, title, x_label, y_label, width, height, output_file):
        """Create a bar chart"""
        # Create a drawing
        img = Image.new('RGB', (width, height), color=(255, 255, 255))
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
        draw.text((width // 2 - 20, height - 20), x_label, fill=(0, 0, 0), font=font)
        draw.text((10, height // 2 - 20), y_label, fill=(0, 0, 0), font=font)
        
        # Add title
        draw.text((width // 2 - 50, 10), title, fill=(0, 0, 0), font=font)
        
        # Process the data
        categories = [item["category"] for item in data]
        values = [item["value"] for item in data]
        colors_list = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 165, 0), (128, 0, 128)]
        
        # Find the max value for scaling
        max_value = max(values)
        
        # Calculate bar width
        bar_width = chart_width / len(data)
        bar_margin = bar_width * 0.1
        
        # Draw each bar
        for i, (category, value) in enumerate(zip(categories, values)):
            # Calculate bar position and size
            bar_x = margin + i * bar_width + bar_margin
            bar_height = (value / max_value) * chart_height
            bar_y = height - margin - bar_height
            
            # Draw the bar
            color = colors_list[i % len(colors_list)]
            draw.rectangle((bar_x, bar_y, bar_x + bar_width - 2 * bar_margin, height - margin), 
                           fill=color, outline=(0, 0, 0))
            
            # Add the category label
            text_width = draw.textlength(category, font=small_font)
            draw.text((bar_x + (bar_width - 2 * bar_margin) / 2 - text_width / 2, 
                       height - margin + 5), category, fill=(0, 0, 0), font=small_font)
            
            # Add the value
            value_str = str(value)
            text_width = draw.textlength(value_str, font=small_font)
            draw.text((bar_x + (bar_width - 2 * bar_margin) / 2 - text_width / 2, 
                       bar_y - 15), value_str, fill=(0, 0, 0), font=small_font)
        
        # Save the image
        img.save(output_file)
        
        return output_file
    
    def _create_pie_chart(self, data, title, width, height, output_file):
        """Create a pie chart"""
        # Create a drawing
        img = Image.new('RGB', (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        # Try to load a font
        try:
            font = ImageFont.truetype("Arial", 12)
            small_font = ImageFont.truetype("Arial", 10)
        except IOError:
            font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Add title
        draw.text((width // 2 - 50, 10), title, fill=(0, 0, 0), font=font)
        
        # Process the data
        categories = [item["category"] for item in data]
        values = [item["value"] for item in data]
        colors_list = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 165, 0), (128, 0, 128)]
        
        # Calculate total
        total = sum(values)
        
        # Calculate angles
        angles = [value / total * 360 for value in values]
        
        # Draw the pie
        center_x = width // 2
        center_y = height // 2
        radius = min(width, height) // 3
        
        start_angle = 0
        for i, (category, value, angle) in enumerate(zip(categories, values, angles)):
            # Calculate end angle
            end_angle = start_angle + angle
            
            # Draw the slice
            color = colors_list[i % len(colors_list)]
            draw.pieslice((center_x - radius, center_y - radius, center_x + radius, center_y + radius), 
                          start_angle, end_angle, fill=color, outline=(0, 0, 0))
            
            # Calculate the position for the label
            label_angle = math.radians(start_angle + angle / 2)
            label_x = center_x + int((radius + 20) * math.cos(label_angle))
            label_y = center_y + int((radius + 20) * math.sin(label_angle))
            
            # Add the category and value label
            percentage = value / total * 100
            label = f"{category}: {percentage:.1f}%"
            text_width = draw.textlength(label, font=small_font)
            draw.text((label_x - text_width / 2, label_y - 5), label, fill=(0, 0, 0), font=small_font)
            
            # Update the start angle for the next slice
            start_angle = end_angle
        
        # Add a legend
        legend_x = width - 150
        legend_y = height // 2 - len(data) * 10
        legend_spacing = 20
        
        for i, (category, value) in enumerate(zip(categories, values)):
            color = colors_list[i % len(colors_list)]
            draw.rectangle((legend_x, legend_y + i * legend_spacing, legend_x + 15, legend_y + i * legend_spacing + 15), 
                           fill=color, outline=(0, 0, 0))
            percentage = value / total * 100
            draw.text((legend_x + 20, legend_y + i * legend_spacing), 
                      f"{category}: {percentage:.1f}%", fill=(0, 0, 0), font=small_font)
        
        # Save the image
        img.save(output_file)
        
        return output_file
    
    def create_molecular_structure(self, molecule_data, title, width=500, height=300):
        """
        Create a molecular structure diagram
        
        Parameters:
        -----------
        molecule_data : dict
            Dictionary containing atoms and bonds
        title : str
            Title of the diagram
        width : int
            Width of the diagram
        height : int
            Height of the diagram
            
        Returns:
        --------
        str
            Path to the saved diagram image
        """
        # Define the output file
        output_file = os.path.join(self.output_dir, f"{title.lower().replace(' ', '_')}.png")
        
        # Create a drawing
        img = Image.new('RGB', (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        # Try to load a font
        try:
            font = ImageFont.truetype("Arial", 12)
            atom_font = ImageFont.truetype("Arial", 14)
        except IOError:
            font = ImageFont.load_default()
            atom_font = ImageFont.load_default()
        
        # Add title
        draw.text((width // 2 - 50, 10), title, fill=(0, 0, 0), font=font)
        
        # Process the molecule data
        atoms = molecule_data["atoms"]
        bonds = molecule_data["bonds"]
        
        # Define atom colors
        atom_colors = {
            "C": (0, 0, 0),      # Black
            "H": (128, 128, 128), # Gray
            "O": (255, 0, 0),    # Red
            "N": (0, 0, 255),    # Blue
            "S": (255, 255, 0),  # Yellow
            "P": (255, 165, 0),  # Orange
            "F": (0, 255, 0),    # Green
            "Cl": (0, 255, 0),   # Green
            "Br": (165, 42, 42), # Brown
            "I": (148, 0, 211)   # Purple
        }
        
        # Calculate the center and scale
        center_x = width // 2
        center_y = height // 2
        scale = min(width, height) // 4
        
        # Draw bonds
        for bond in bonds:
            atom1_idx = bond["atom1"]
            atom2_idx = bond["atom2"]
            bond_type = bond.get("type", "single")
            
            atom1 = atoms[atom1_idx]
            atom2 = atoms[atom2_idx]
            
            # Calculate positions
            x1 = center_x + int(atom1["x"] * scale)
            y1 = center_y + int(atom1["y"] * scale)
            x2 = center_x + int(atom2["x"] * scale)
            y2 = center_y + int(atom2["y"] * scale)
            
            # Draw the bond
            if bond_type == "single":
                draw.line((x1, y1, x2, y2), fill=(0, 0, 0), width=2)
            elif bond_type == "double":
                # Calculate perpendicular offset
                dx = x2 - x1
                dy = y2 - y1
                length = math.sqrt(dx*dx + dy*dy)
                offset = 3
                
                # Normalize and perpendicular
                dx /= length
                dy /= length
                perp_x = -dy
                perp_y = dx
                
                # Draw two lines
                draw.line((x1 + perp_x * offset, y1 + perp_y * offset, 
                           x2 + perp_x * offset, y2 + perp_y * offset), fill=(0, 0, 0), width=2)
                draw.line((x1 - perp_x * offset, y1 - perp_y * offset, 
                           x2 - perp_x * offset, y2 - perp_y * offset), fill=(0, 0, 0), width=2)
            elif bond_type == "triple":
                # Calculate perpendicular offset
                dx = x2 - x1
                dy = y2 - y1
                length = math.sqrt(dx*dx + dy*dy)
                offset = 4
                
                # Normalize and perpendicular
                dx /= length
                dy /= length
                perp_x = -dy
                perp_y = dx
                
                # Draw three lines
                draw.line((x1, y1, x2, y2), fill=(0, 0, 0), width=2)
                draw.line((x1 + perp_x * offset, y1 + perp_y * offset, 
                           x2 + perp_x * offset, y2 + perp_y * offset), fill=(0, 0, 0), width=2)
                draw.line((x1 - perp_x * offset, y1 - perp_y * offset, 
                           x2 - perp_x * offset, y2 - perp_y * offset), fill=(0, 0, 0), width=2)
        
        # Draw atoms
        for atom in atoms:
            element = atom["element"]
            
            # Calculate position
            x = center_x + int(atom["x"] * scale)
            y = center_y + int(atom["y"] * scale)
            
            # Get atom color
            color = atom_colors.get(element, (0, 0, 0))
            
            # Draw the atom
            radius = 12 if element != "H" else 8
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), 
                         fill=color, outline=(0, 0, 0))
            
            # Add the element label
            text_width = draw.textlength(element, font=atom_font)
            text_color = (255, 255, 255) if element not in ["H", "S", "Cl"] else (0, 0, 0)
            draw.text((x - text_width / 2, y - 7), element, fill=text_color, font=atom_font)
        
        # Save the image
        img.save(output_file)
        
        return output_file
    
    def create_data_table(self, data, headers, title, width=500, height=None):
        """
        Create a data table image
        
        Parameters:
        -----------
        data : list
            List of lists containing the table data
        headers : list
            List of column headers
        title : str
            Title of the table
        width : int
            Width of the table
        height : int, optional
            Height of the table
            
        Returns:
        --------
        str
            Path to the saved table image
        """
        # Define the output file
        output_file = os.path.join(self.output_dir, f"{title.lower().replace(' ', '_')}.png")
        
        # Calculate the height if not provided
        if height is None:
            height = 50 + (len(data) + 1) * 30
        
        # Create a drawing
        img = Image.new('RGB', (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        # Try to load a font
        try:
            font = ImageFont.truetype("Arial", 12)
            header_font = ImageFont.truetype("Arial-Bold", 12)
        except IOError:
            font = ImageFont.load_default()
            header_font = ImageFont.load_default()
        
        # Add title
        draw.text((width // 2 - 50, 10), title, fill=(0, 0, 0), font=font)
        
        # Calculate column width
        col_width = width / len(headers)
        
        # Draw headers
        for i, header in enumerate(headers):
            x = i * col_width + col_width / 2
            y = 40
            text_width = draw.textlength(header, font=header_font)
            draw.text((x - text_width / 2, y), header, fill=(0, 0, 0), font=header_font)
        
        # Draw header separator
        draw.line((0, 60, width, 60), fill=(0, 0, 0), width=2)
        
        # Draw data
        for i, row in enumerate(data):
            for j, cell in enumerate(row):
                x = j * col_width + col_width / 2
                y = 70 + i * 30
                text = str(cell)
                text_width = draw.textlength(text, font=font)
                draw.text((x - text_width / 2, y), text, fill=(0, 0, 0), font=font)
            
            # Draw row separator
            draw.line((0, 70 + (i + 1) * 30 - 5, width, 70 + (i + 1) * 30 - 5), 
                      fill=(200, 200, 200), width=1)
        
        # Draw table border
        draw.rectangle((0, 30, width - 1, height - 1), outline=(0, 0, 0), width=2)
        
        # Save the image
        img.save(output_file)
        
        return output_file

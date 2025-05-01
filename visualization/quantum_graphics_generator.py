#!/usr/bin/env python3
"""
Quantum Graphics Generator

This module provides functions for generating quantum-themed graphics
for use in scientific documents.
"""

import os
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

class QuantumGraphicsGenerator:
    """
    Quantum Graphics Generator
    
    This class provides methods for generating quantum-themed graphics:
    - Wave function visualizations
    - Quantum field visualizations
    - Title page backgrounds
    """
    
    def __init__(self, output_dir="docs/pdf/quantum_graphics"):
        """
        Initialize the quantum graphics generator
        
        Parameters:
        -----------
        output_dir : str
            Directory to save quantum graphics (will be created if it doesn't exist)
        """
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_wave_function(self, width=800, height=600, n=3, l=2, filename="wave_function.png"):
        """
        Generate a hydrogen-like wave function visualization
        
        Parameters:
        -----------
        width : int
            Width of the image
        height : int
            Height of the image
        n : int
            Principal quantum number
        l : int
            Angular momentum quantum number
        filename : str
            Name of the output file
            
        Returns:
        --------
        str
            Path to the saved image
        """
        # Define the output file
        output_file = os.path.join(self.output_dir, filename)
        
        # Create figure
        fig = plt.figure(figsize=(width/100, height/100), dpi=100)
        ax = fig.add_subplot(111, projection='3d')
        
        # Create grid
        theta = np.linspace(0, np.pi, 100)
        phi = np.linspace(0, 2*np.pi, 100)
        theta, phi = np.meshgrid(theta, phi)
        
        # Calculate wave function (simplified)
        r = 1.0
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)
        
        # Calculate spherical harmonic (simplified)
        if l == 0:
            # s orbital
            c = 1.0
        elif l == 1:
            # p orbital
            c = np.cos(theta)
        elif l == 2:
            # d orbital
            c = (3 * np.cos(theta)**2 - 1)
        else:
            # Higher orbitals (simplified)
            c = np.sin(l * theta) * np.cos(l * phi)
        
        # Scale by radial function (simplified)
        c = c * np.exp(-r/n) * (2*r/n)**(l)
        
        # Normalize
        c = c / np.max(np.abs(c))
        
        # Plot
        surf = ax.plot_surface(x, y, z, facecolors=cm.viridis(c), alpha=0.7)
        
        # Remove axes for cleaner look
        ax.set_axis_off()
        
        # Set view angle
        ax.view_init(elev=30, azim=45)
        
        # Save the figure
        plt.savefig(output_file, bbox_inches='tight', transparent=True)
        plt.close()
        
        return output_file
    
    def generate_quantum_field(self, width=800, height=600, complexity=5, filename="quantum_field.png"):
        """
        Generate a quantum field visualization
        
        Parameters:
        -----------
        width : int
            Width of the image
        height : int
            Height of the image
        complexity : int
            Complexity of the field (1-10)
        filename : str
            Name of the output file
            
        Returns:
        --------
        str
            Path to the saved image
        """
        # Define the output file
        output_file = os.path.join(self.output_dir, filename)
        
        # Create figure
        fig = plt.figure(figsize=(width/100, height/100), dpi=100)
        ax = fig.add_subplot(111)
        
        # Create grid
        x = np.linspace(-5, 5, 100)
        y = np.linspace(-5, 5, 100)
        X, Y = np.meshgrid(x, y)
        
        # Generate quantum field (simplified)
        Z = np.zeros_like(X)
        for i in range(complexity):
            freq = random.uniform(0.5, 2.0)
            phase = random.uniform(0, 2*np.pi)
            amplitude = random.uniform(0.5, 1.0)
            direction = random.uniform(0, 2*np.pi)
            Z += amplitude * np.sin(freq * (X*np.cos(direction) + Y*np.sin(direction)) + phase)
        
        # Normalize
        Z = Z / np.max(np.abs(Z))
        
        # Plot
        contour = ax.contourf(X, Y, Z, 50, cmap='viridis')
        ax.streamplot(X, Y, np.gradient(Z, axis=1), np.gradient(Z, axis=0), 
                     color='white', linewidth=0.5, density=1.5, arrowsize=0.5)
        
        # Remove axes for cleaner look
        ax.set_axis_off()
        
        # Save the figure
        plt.savefig(output_file, bbox_inches='tight', transparent=True)
        plt.close()
        
        return output_file
    
    def generate_title_page_background(self, width=800, height=1100, filename="title_background.png"):
        """
        Generate a quantum-themed background for a title page
        
        Parameters:
        -----------
        width : int
            Width of the image
        height : int
            Height of the image
        filename : str
            Name of the output file
            
        Returns:
        --------
        str
            Path to the saved image
        """
        # Define the output file
        output_file = os.path.join(self.output_dir, filename)
        
        # Create a blank image with a dark blue background
        img = Image.new('RGBA', (width, height), color=(5, 10, 30, 255))
        draw = ImageDraw.Draw(img)
        
        # Add quantum field lines
        num_lines = 100
        for i in range(num_lines):
            # Random starting point
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            
            # Random length and angle
            length = random.randint(50, 200)
            angle = random.uniform(0, 2 * math.pi)
            
            # Calculate end point
            x2 = x1 + length * math.cos(angle)
            y2 = y1 + length * math.sin(angle)
            
            # Random control point for curve
            cx = (x1 + x2) / 2 + random.uniform(-50, 50)
            cy = (y1 + y2) / 2 + random.uniform(-50, 50)
            
            # Random color (blue/cyan/purple hues)
            r = random.randint(20, 100)
            g = random.randint(100, 200)
            b = random.randint(180, 255)
            a = random.randint(30, 100)
            
            # Draw curved line
            self._draw_curved_line(draw, (x1, y1), (cx, cy), (x2, y2), 
                                  fill=(r, g, b, a), width=2)
        
        # Add quantum particles
        num_particles = 50
        for i in range(num_particles):
            x = random.randint(0, width)
            y = random.randint(0, height)
            radius = random.randint(2, 8)
            
            # Random color (brighter than lines)
            r = random.randint(100, 255)
            g = random.randint(150, 255)
            b = random.randint(200, 255)
            a = random.randint(150, 255)
            
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), 
                         fill=(r, g, b, a))
        
        # Apply a slight blur for a smoother look
        img = img.filter(ImageFilter.GaussianBlur(radius=1))
        
        # Save the image
        img.save(output_file)
        
        return output_file
    
    def _draw_curved_line(self, draw, p1, p2, p3, fill=(255, 255, 255, 255), width=1):
        """
        Draw a quadratic Bezier curve
        
        Parameters:
        -----------
        draw : ImageDraw
            PIL ImageDraw object
        p1 : tuple
            Start point (x, y)
        p2 : tuple
            Control point (x, y)
        p3 : tuple
            End point (x, y)
        fill : tuple
            RGBA color
        width : int
            Line width
        """
        # Number of segments to approximate the curve
        segments = 100
        
        # Generate points along the curve
        points = []
        for t in range(segments + 1):
            t = t / segments
            # Quadratic Bezier formula
            x = (1-t)**2 * p1[0] + 2*(1-t)*t * p2[0] + t**2 * p3[0]
            y = (1-t)**2 * p1[1] + 2*(1-t)*t * p2[1] + t**2 * p3[1]
            points.append((x, y))
        
        # Draw the curve as a series of line segments
        if len(points) > 1:
            draw.line(points, fill=fill, width=width)

# Main function for command-line usage
def main():
    """Main function for command-line usage"""
    generator = QuantumGraphicsGenerator()
    
    # Generate quantum graphics
    generator.generate_wave_function()
    generator.generate_quantum_field()
    generator.generate_title_page_background()
    
    print("Quantum graphics generated successfully!")

if __name__ == "__main__":
    main()

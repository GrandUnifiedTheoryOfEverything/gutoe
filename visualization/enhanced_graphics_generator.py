#!/usr/bin/env python3
"""
Enhanced Graphics Generator

This module provides functions for generating high-quality graphics
for PDF documents with professional styling.
"""

import os
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors as mcolors
import matplotlib.patheffects as path_effects
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance, ImageOps

class EnhancedGraphicsGenerator:
    """
    Enhanced Graphics Generator
    
    This class provides methods for generating high-quality graphics
    for PDF documents with professional styling.
    """
    
    def __init__(self, output_dir="gfx/pdf/graphics"):
        """
        Initialize the enhanced graphics generator
        
        Parameters:
        -----------
        output_dir : str
            Directory to save graphics (will be created if it doesn't exist)
        """
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Set up matplotlib style for professional plots
        plt.style.use('seaborn-v0_8-whitegrid')
        
        # Define color schemes
        self.color_schemes = {
            "professional": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"],
            "scientific": ["#4878d0", "#ee854a", "#6acc64", "#d65f5f", "#956cb4", "#8c613c"],
            "elegant": ["#324b7c", "#d3791e", "#497a3a", "#b23939", "#6b4c9a", "#775144"]
        }
    
    def create_unified_theory_diagram(self, style="professional", filename="unified_theory_diagram.png"):
        """
        Create a high-quality diagram illustrating the unified theory concept
        
        Parameters:
        -----------
        style : str
            Style theme to use (professional, scientific, elegant)
        filename : str
            Name of the output file
            
        Returns:
        --------
        str
            Path to the saved diagram image
        """
        # Define the output file
        output_file = os.path.join(self.output_dir, filename)
        
        # Get color scheme
        colors = self.color_schemes.get(style, self.color_schemes["professional"])
        
        # Create figure with high resolution
        fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
        
        # Set background color
        fig.patch.set_facecolor('#f8f9fa')
        ax.set_facecolor('#f8f9fa')
        
        # Create central node for unified theory
        central_x, central_y = 0.5, 0.5
        central_radius = 0.15
        central_circle = plt.Circle((central_x, central_y), central_radius, 
                                   color=colors[0], alpha=0.8, zorder=10)
        ax.add_patch(central_circle)
        
        # Add central text with shadow effect
        central_text = ax.text(central_x, central_y, "Unified\nTheory", 
                              ha='center', va='center', fontsize=14, 
                              fontweight='bold', color='white', zorder=11)
        central_text.set_path_effects([
            path_effects.Stroke(linewidth=3, foreground='black', alpha=0.3),
            path_effects.Normal()
        ])
        
        # Define the four fundamental forces
        forces = [
            {"name": "Gravity", "angle": 45, "color": colors[1]},
            {"name": "Electromagnetism", "angle": 135, "color": colors[2]},
            {"name": "Strong Force", "angle": 225, "color": colors[3]},
            {"name": "Weak Force", "angle": 315, "color": colors[4]}
        ]
        
        # Draw each force and connect it to the central circle
        for force in forces:
            angle_rad = math.radians(force["angle"])
            force_distance = 0.3
            force_x = central_x + force_distance * math.cos(angle_rad)
            force_y = central_y + force_distance * math.sin(angle_rad)
            force_radius = 0.08
            
            # Draw the force circle
            force_circle = plt.Circle((force_x, force_y), force_radius, 
                                     color=force["color"], alpha=0.8, zorder=5)
            ax.add_patch(force_circle)
            
            # Draw the connecting line with gradient
            self._draw_gradient_line(ax, central_x, central_y, force_x, force_y, 
                                    colors[0], force["color"], linewidth=3, alpha=0.6, zorder=1)
            
            # Add the force name with shadow effect
            force_text = ax.text(force_x, force_y, force["name"], 
                                ha='center', va='center', fontsize=10, 
                                fontweight='bold', color='white', zorder=6)
            force_text.set_path_effects([
                path_effects.Stroke(linewidth=2, foreground='black', alpha=0.3),
                path_effects.Normal()
            ])
        
        # Add decorative elements
        self._add_decorative_elements(ax, central_x, central_y, 0.4, 20, colors, zorder=0)
        
        # Set axis limits and remove ticks
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Add title
        title = ax.text(0.5, 0.95, "Unified Theory of Fundamental Forces", 
                       ha='center', va='center', fontsize=16, 
                       fontweight='bold', color=colors[0])
        title.set_path_effects([
            path_effects.Stroke(linewidth=3, foreground='white', alpha=0.8),
            path_effects.Normal()
        ])
        
        # Save the figure with tight layout and high quality
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
        plt.close()
        
        return output_file
    
    def create_universe_evolution_diagram(self, style="professional", filename="universe_evolution.png"):
        """
        Create a high-quality diagram showing the evolution of the universe
        
        Parameters:
        -----------
        style : str
            Style theme to use (professional, scientific, elegant)
        filename : str
            Name of the output file
            
        Returns:
        --------
        str
            Path to the saved diagram image
        """
        # Define the output file
        output_file = os.path.join(self.output_dir, filename)
        
        # Get color scheme
        colors = self.color_schemes.get(style, self.color_schemes["professional"])
        
        # Create figure with high resolution
        fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
        
        # Set background color with gradient
        background = np.zeros((100, 100, 3))
        for i in range(100):
            for j in range(100):
                # Create a dark blue to black gradient
                background[i, j, 0] = 0.05 + 0.1 * (j / 100)  # R
                background[i, j, 1] = 0.05 + 0.1 * (j / 100)  # G
                background[i, j, 2] = 0.1 + 0.2 * (j / 100)   # B
        
        ax.imshow(background, extent=[0, 1, 0, 1], aspect='auto', zorder=-1)
        
        # Define the key events in the universe's evolution
        events = [
            {"name": "Big Bang", "time": "0 s", "x_pos": 0.05, "description": "Unified forces", "color": colors[0]},
            {"name": "Inflation", "time": "10⁻³⁵ s", "x_pos": 0.15, "description": "Rapid expansion", "color": colors[1]},
            {"name": "Quark Era", "time": "10⁻¹² s", "x_pos": 0.25, "description": "Quarks form", "color": colors[2]},
            {"name": "Nucleosynthesis", "time": "3 min", "x_pos": 0.35, "description": "Nuclei form", "color": colors[3]},
            {"name": "Recombination", "time": "380,000 yr", "x_pos": 0.55, "description": "Atoms form", "color": colors[4]},
            {"name": "First Stars", "time": "100 million yr", "x_pos": 0.75, "description": "Stars ignite", "color": colors[5]},
            {"name": "Present Day", "time": "13.8 billion yr", "x_pos": 0.95, "description": "Current state", "color": colors[0]}
        ]
        
        # Draw the timeline
        timeline_y = 0.5
        ax.plot([0.05, 0.95], [timeline_y, timeline_y], color='white', linewidth=3, alpha=0.8, zorder=2)
        
        # Add stars in the background
        self._add_stars(ax, 200, zorder=0)
        
        # Draw each event on the timeline
        for i, event in enumerate(events):
            x_pos = event["x_pos"]
            
            # Draw a marker on the timeline
            marker = plt.Circle((x_pos, timeline_y), 0.02, 
                               color=event["color"], alpha=0.9, zorder=3)
            ax.add_patch(marker)
            
            # Add glow effect
            glow = plt.Circle((x_pos, timeline_y), 0.03, 
                             color=event["color"], alpha=0.3, zorder=2)
            ax.add_patch(glow)
            
            # Draw the event name above the timeline with shadow effect
            event_text = ax.text(x_pos, timeline_y + 0.08, event["name"], 
                                ha='center', va='center', fontsize=10, 
                                fontweight='bold', color='white', zorder=4)
            event_text.set_path_effects([
                path_effects.Stroke(linewidth=2, foreground='black', alpha=0.5),
                path_effects.Normal()
            ])
            
            # Draw the time below the timeline
            time_text = ax.text(x_pos, timeline_y - 0.08, event["time"], 
                               ha='center', va='center', fontsize=8, 
                               color='white', alpha=0.9, zorder=4)
            time_text.set_path_effects([
                path_effects.Stroke(linewidth=1, foreground='black', alpha=0.5),
                path_effects.Normal()
            ])
            
            # Draw the description below the time
            desc_text = ax.text(x_pos, timeline_y - 0.15, event["description"], 
                               ha='center', va='center', fontsize=8, 
                               color='white', alpha=0.7, zorder=4)
            desc_text.set_path_effects([
                path_effects.Stroke(linewidth=1, foreground='black', alpha=0.5),
                path_effects.Normal()
            ])
            
            # Add connecting lines between events
            if i < len(events) - 1:
                next_x = events[i+1]["x_pos"]
                self._draw_gradient_line(ax, x_pos, timeline_y, next_x, timeline_y, 
                                        event["color"], events[i+1]["color"], 
                                        linewidth=3, alpha=0.8, zorder=1)
        
        # Set axis limits and remove ticks
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        # Add title
        title = ax.text(0.5, 0.9, "Evolution of the Universe", 
                       ha='center', va='center', fontsize=16, 
                       fontweight='bold', color='white')
        title.set_path_effects([
            path_effects.Stroke(linewidth=3, foreground='black', alpha=0.5),
            path_effects.Normal()
        ])
        
        # Save the figure with tight layout and high quality
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='black')
        plt.close()
        
        return output_file
    
    def create_particle_interaction_diagram(self, style="professional", filename="particle_interaction.png"):
        """
        Create a high-quality diagram showing particle interactions
        
        Parameters:
        -----------
        style : str
            Style theme to use (professional, scientific, elegant)
        filename : str
            Name of the output file
            
        Returns:
        --------
        str
            Path to the saved diagram image
        """
        # Define the output file
        output_file = os.path.join(self.output_dir, filename)
        
        # Get color scheme
        colors = self.color_schemes.get(style, self.color_schemes["professional"])
        
        # Create figure with high resolution
        fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
        
        # Set background color
        fig.patch.set_facecolor('#f8f9fa')
        ax.set_facecolor('#f8f9fa')
        
        # Define the particles and their positions
        particles = [
            {"name": "e⁻", "x": 0.2, "y": 0.2, "color": colors[0]},
            {"name": "e⁻", "x": 0.2, "y": 0.8, "color": colors[0]},
            {"name": "γ", "x": 0.5, "y": 0.5, "color": colors[1]},
            {"name": "e⁺", "x": 0.8, "y": 0.2, "color": colors[2]},
            {"name": "e⁺", "x": 0.8, "y": 0.8, "color": colors[2]}
        ]
        
        # Define the connections between particles
        connections = [
            {"from": 0, "to": 2, "style": "solid"},
            {"from": 1, "to": 2, "style": "solid"},
            {"from": 2, "to": 3, "style": "solid"},
            {"from": 2, "to": 4, "style": "solid"}
        ]
        
        # Draw the connections
        for conn in connections:
            p1 = particles[conn["from"]]
            p2 = particles[conn["to"]]
            
            if conn["style"] == "solid":
                self._draw_gradient_line(ax, p1["x"], p1["y"], p2["x"], p2["y"], 
                                        p1["color"], p2["color"], linewidth=3, alpha=0.8, zorder=1)
            elif conn["style"] == "wavy":
                self._draw_wavy_line(ax, p1["x"], p1["y"], p2["x"], p2["y"], 
                                    p1["color"], p2["color"], linewidth=2, alpha=0.8, zorder=1)
        
        # Draw the particles
        for p in particles:
            # Draw particle circle
            particle = plt.Circle((p["x"], p["y"]), 0.05, 
                                 color=p["color"], alpha=0.8, zorder=5)
            ax.add_patch(particle)
            
            # Add glow effect
            glow = plt.Circle((p["x"], p["y"]), 0.08, 
                             color=p["color"], alpha=0.3, zorder=4)
            ax.add_patch(glow)
            
            # Add particle name with shadow effect
            particle_text = ax.text(p["x"], p["y"], p["name"], 
                                   ha='center', va='center', fontsize=12, 
                                   fontweight='bold', color='white', zorder=6)
            particle_text.set_path_effects([
                path_effects.Stroke(linewidth=2, foreground='black', alpha=0.3),
                path_effects.Normal()
            ])
        
        # Add annotations
        ax.text(0.1, 0.1, "Incoming electron", fontsize=10, ha='center', va='center')
        ax.text(0.1, 0.9, "Incoming electron", fontsize=10, ha='center', va='center')
        ax.text(0.9, 0.1, "Outgoing positron", fontsize=10, ha='center', va='center')
        ax.text(0.9, 0.9, "Outgoing positron", fontsize=10, ha='center', va='center')
        ax.text(0.5, 0.4, "Virtual photon", fontsize=10, ha='center', va='center')
        
        # Set axis limits and remove ticks
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Add title
        title = ax.text(0.5, 0.95, "Electron-Positron Annihilation", 
                       ha='center', va='center', fontsize=16, 
                       fontweight='bold', color=colors[0])
        title.set_path_effects([
            path_effects.Stroke(linewidth=3, foreground='white', alpha=0.8),
            path_effects.Normal()
        ])
        
        # Save the figure with tight layout and high quality
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
        plt.close()
        
        return output_file
    
    def _draw_gradient_line(self, ax, x1, y1, x2, y2, color1, color2, linewidth=2, alpha=1.0, zorder=1):
        """Draw a line with gradient color"""
        # Create gradient color array
        n_points = 100
        x = np.linspace(x1, x2, n_points)
        y = np.linspace(y1, y2, n_points)
        
        # Convert colors to RGB arrays
        c1 = mcolors.to_rgb(color1)
        c2 = mcolors.to_rgb(color2)
        
        # Create gradient
        for i in range(n_points-1):
            t = i / (n_points-1)
            color = (1-t) * np.array(c1) + t * np.array(c2)
            ax.plot(x[i:i+2], y[i:i+2], color=color, linewidth=linewidth, alpha=alpha, zorder=zorder)
    
    def _draw_wavy_line(self, ax, x1, y1, x2, y2, color1, color2, linewidth=2, alpha=1.0, zorder=1, n_waves=10):
        """Draw a wavy line with gradient color"""
        # Create gradient color array
        n_points = 100
        t = np.linspace(0, 1, n_points)
        
        # Create wavy line
        dx = x2 - x1
        dy = y2 - y1
        dist = np.sqrt(dx**2 + dy**2)
        
        # Perpendicular direction
        px = -dy / dist
        py = dx / dist
        
        # Amplitude of the wave
        amplitude = 0.02
        
        # Create the wavy line points
        x = x1 + t * dx + amplitude * np.sin(2 * np.pi * n_waves * t) * px
        y = y1 + t * dy + amplitude * np.sin(2 * np.pi * n_waves * t) * py
        
        # Convert colors to RGB arrays
        c1 = mcolors.to_rgb(color1)
        c2 = mcolors.to_rgb(color2)
        
        # Draw the wavy line with gradient color
        for i in range(n_points-1):
            t_val = i / (n_points-1)
            color = (1-t_val) * np.array(c1) + t_val * np.array(c2)
            ax.plot(x[i:i+2], y[i:i+2], color=color, linewidth=linewidth, alpha=alpha, zorder=zorder)
    
    def _add_decorative_elements(self, ax, center_x, center_y, radius, n_elements, colors, zorder=0):
        """Add decorative elements around a center point"""
        for i in range(n_elements):
            angle = 2 * np.pi * i / n_elements
            distance = radius * (0.8 + 0.2 * np.random.random())
            x = center_x + distance * np.cos(angle)
            y = center_y + distance * np.sin(angle)
            
            # Random size and color
            size = 0.01 + 0.02 * np.random.random()
            color = random.choice(colors)
            
            # Add a small circle
            circle = plt.Circle((x, y), size, color=color, alpha=0.3, zorder=zorder)
            ax.add_patch(circle)
    
    def _add_stars(self, ax, n_stars, zorder=0):
        """Add stars to the background"""
        for _ in range(n_stars):
            x = np.random.random()
            y = np.random.random()
            size = 0.002 + 0.003 * np.random.random()
            alpha = 0.3 + 0.7 * np.random.random()
            
            # Add a small white circle
            star = plt.Circle((x, y), size, color='white', alpha=alpha, zorder=zorder)
            ax.add_patch(star)
            
            # Add glow for some stars
            if np.random.random() > 0.7:
                glow = plt.Circle((x, y), size * 2, color='white', alpha=alpha * 0.3, zorder=zorder)
                ax.add_patch(glow)

# Main function for command-line usage
def main():
    """Main function for command-line usage"""
    generator = EnhancedGraphicsGenerator()
    
    # Generate enhanced graphics
    generator.create_unified_theory_diagram()
    generator.create_universe_evolution_diagram()
    generator.create_particle_interaction_diagram()
    
    print("Enhanced graphics generated successfully!")

if __name__ == "__main__":
    main()

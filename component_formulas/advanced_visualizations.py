#!/usr/bin/env python3
"""
Advanced Visualizations for the Theory of Everything

This module provides enhanced 3D and 4D visualizations for the Theory of Everything,
with a focus on representing multi-dimensional spaces and complex physical phenomena.

The visualizations include:
1. 4D Spacetime Curvature
2. Quantum Foam in 3D
3. String Theory Extra Dimensions
4. 4D Higgs Field Dynamics
5. Gauge Field Configurations in Higher Dimensions
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm, colors
import matplotlib.animation as animation
from matplotlib.widgets import Slider
import sympy as sp
from sympy import symbols, Matrix, Eq, latex, sqrt, exp, I
from scipy.integrate import quad, solve_ivp
from scipy.spatial import Delaunay
import matplotlib.patches as patches


class AdvancedVisualizations:
    """
    Advanced visualization techniques for the Theory of Everything,
    focusing on 3D and 4D representations of multi-dimensional spaces.
    """

    def __init__(self):
        """Initialize the advanced visualizations"""
        self.c = 299792458  # Speed of light
        self.G = 6.67430e-11  # Gravitational constant
        self.hbar = 1.054571817e-34  # Reduced Planck constant

    def visualize_4d_spacetime_curvature(self, mass=1.0, grid_size=20):
        """
        Visualize 4D spacetime curvature using a 3D projection with time as color

        Parameters:
        -----------
        mass : float
            Mass of the central object (in solar masses)
        grid_size : int
            Size of the grid for visualization
        """
        # Create a grid of points
        x = np.linspace(-10, 10, grid_size)
        y = np.linspace(-10, 10, grid_size)
        X, Y = np.meshgrid(x, y)

        # Calculate Schwarzschild metric for a black hole
        # g_tt = -(1 - 2GM/rc²)
        r = np.sqrt(X**2 + Y**2 + 0.1**2)  # Add small constant to avoid division by zero
        M = mass * 1.989e30  # Convert solar masses to kg
        Rs = 2 * self.G * M / (self.c**2)  # Schwarzschild radius
        
        # Calculate time component of the metric (g_tt)
        g_tt = -(1 - Rs/r)
        
        # Calculate spatial curvature (simplified)
        Z = -Rs / (2 * r)
        
        # Create 3D plot with time component as color
        fig = plt.figure(figsize=(14, 12))
        ax = fig.add_subplot(111, projection='3d')
        
        # Create a custom colormap for the time dimension
        norm = colors.Normalize(vmin=np.min(g_tt), vmax=0)
        
        # Plot the surface with time as color
        surf = ax.plot_surface(X, Y, Z, facecolors=cm.viridis(norm(g_tt)),
                              linewidth=0, antialiased=True)
        
        # Add a color bar for the time dimension
        cbar = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cm.viridis), 
                           ax=ax, shrink=0.5, aspect=10)
        cbar.set_label('Time Dilation (g_tt)', fontsize=12)
        
        # Add a wireframe to show the flat space for comparison
        ax.plot_wireframe(X, Y, np.zeros_like(Z), color='gray', alpha=0.3, linewidth=0.5)
        
        # Add labels
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        ax.set_zlabel('Curvature', fontsize=12)
        ax.set_title('4D Spacetime Curvature (3D projection with time as color)', fontsize=14)
        
        # Add text explaining the visualization
        plt.figtext(0.02, 0.02, 
                   "This visualization shows 4D spacetime around a massive object.\n"
                   "The 3D surface represents spatial curvature, while the color\n"
                   "represents time dilation (the 4th dimension).", fontsize=10)
        
        plt.tight_layout()
        plt.show()

    def visualize_quantum_foam_3d(self, grid_size=30, amplitude=0.5, frequency=2.0):
        """
        Visualize quantum foam in 3D with enhanced detail

        Parameters:
        -----------
        grid_size : int
            Size of the grid for visualization
        amplitude : float
            Amplitude of quantum fluctuations
        frequency : float
            Frequency of quantum fluctuations
        """
        # Create a grid of points
        x = np.linspace(-5, 5, grid_size)
        y = np.linspace(-5, 5, grid_size)
        z = np.linspace(-5, 5, grid_size)
        
        # Create a 3D grid
        X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
        
        # Calculate quantum foam fluctuations (simplified model)
        # In reality, quantum foam would involve complex quantum field theory calculations
        
        # Generate random phases for different frequency components
        np.random.seed(42)  # For reproducibility
        phases = 2 * np.pi * np.random.random((3, 3, 3))
        
        # Calculate quantum fluctuations with multiple frequency components
        foam = np.zeros_like(X)
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    foam += amplitude * (1.0/(i+j+k+1)) * np.sin(frequency*(i+1)*X + phases[i,j,k]) * \
                            np.sin(frequency*(j+1)*Y + phases[i,j,k]) * \
                            np.sin(frequency*(k+1)*Z + phases[i,j,k])
        
        # Create an isosurface of the quantum foam
        fig = plt.figure(figsize=(14, 12))
        ax = fig.add_subplot(111, projection='3d')
        
        # Create a custom colormap
        custom_cmap = plt.cm.viridis
        
        # Plot the isosurface using voxels
        # We'll create a binary mask for the isosurface
        foam_mask = (foam > 0.2 * amplitude)
        
        # Color based on the foam value
        colors = custom_cmap((foam - np.min(foam)) / (np.max(foam) - np.min(foam)))
        
        # Plot only a subset of voxels for better visibility
        step = 2
        ax.voxels(foam_mask[::step,::step,::step], 
                 facecolors=colors[::step,::step,::step],
                 edgecolor='k', alpha=0.7, linewidth=0.1)
        
        # Add labels
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        ax.set_zlabel('Z', fontsize=12)
        ax.set_title('3D Quantum Foam Visualization', fontsize=14)
        
        # Add text explaining the visualization
        plt.figtext(0.02, 0.02, 
                   "This visualization shows quantum foam - the quantum fluctuations\n"
                   "of spacetime at the Planck scale. The foam represents the\n"
                   "probabilistic nature of spacetime at quantum scales.", fontsize=10)
        
        plt.tight_layout()
        plt.show()

    def visualize_string_worldsheet_3d(self, time_steps=50, oscillation_modes=3):
        """
        Visualize a string worldsheet in 3D with time evolution

        Parameters:
        -----------
        time_steps : int
            Number of time steps to visualize
        oscillation_modes : int
            Number of oscillation modes to include
        """
        # Create figure
        fig = plt.figure(figsize=(14, 12))
        ax = fig.add_subplot(111, projection='3d')
        
        # String parameters
        string_length = 2.0
        tension = 1.0
        
        # Create sigma (position along string)
        sigma = np.linspace(0, string_length, 100)
        
        # Create time steps
        time = np.linspace(0, 2, time_steps)
        
        # Generate random amplitudes and phases for oscillation modes
        np.random.seed(42)  # For reproducibility
        amplitudes = 0.2 * np.random.random(oscillation_modes)
        phases = 2 * np.pi * np.random.random(oscillation_modes)
        
        # Calculate string oscillations for each time step
        worldsheet = []
        
        for t in time:
            # Calculate string position at this time
            X = np.zeros_like(sigma)
            Y = np.zeros_like(sigma)
            
            # Add oscillation modes
            for n in range(1, oscillation_modes + 1):
                X += amplitudes[n-1] * np.sin(n * np.pi * sigma / string_length) * \
                     np.cos(n * np.pi * np.sqrt(tension) * t + phases[n-1])
                Y += amplitudes[n-1] * np.sin(n * np.pi * sigma / string_length) * \
                     np.sin(n * np.pi * np.sqrt(tension) * t + phases[n-1])
            
            # Add to worldsheet
            worldsheet.append((sigma, X, Y, t))
        
        # Plot the worldsheet
        for i in range(len(worldsheet) - 1):
            sigma, X, Y, t = worldsheet[i]
            
            # Plot the string at this time
            ax.plot(sigma, X, Y, 'b-', alpha=0.5 * (i / len(worldsheet)))
            
            # Connect to next time step
            if i < len(worldsheet) - 1:
                next_sigma, next_X, next_Y, next_t = worldsheet[i + 1]
                
                # Connect a few points along the string to the next time step
                for j in range(0, len(sigma), 10):
                    ax.plot([sigma[j], next_sigma[j]], 
                           [X[j], next_X[j]], 
                           [Y[j], next_Y[j]], 
                           'g-', alpha=0.2)
        
        # Plot the final string position
        sigma, X, Y, t = worldsheet[-1]
        ax.plot(sigma, X, Y, 'r-', linewidth=2, label='Final String Position')
        
        # Add labels
        ax.set_xlabel('σ (String Position)', fontsize=12)
        ax.set_ylabel('X', fontsize=12)
        ax.set_zlabel('Y', fontsize=12)
        ax.set_title('3D String Worldsheet Visualization', fontsize=14)
        ax.legend()
        
        # Add text explaining the visualization
        plt.figtext(0.02, 0.02, 
                   "This visualization shows a string worldsheet in 3D.\n"
                   "The string evolves through time, with multiple oscillation modes.\n"
                   "The worldsheet represents the string's path through spacetime.", fontsize=10)
        
        plt.tight_layout()
        plt.show()

    def visualize_extra_dimensions_3d(self, num_dimensions=6, grid_size=20):
        """
        Visualize extra dimensions from string theory in 3D

        Parameters:
        -----------
        num_dimensions : int
            Total number of dimensions to represent
        grid_size : int
            Size of the grid for visualization
        """
        # Create figure
        fig = plt.figure(figsize=(14, 12))
        ax = fig.add_subplot(111, projection='3d')
        
        # Create a grid for the 3 visible dimensions
        theta = np.linspace(0, 2 * np.pi, grid_size)
        phi = np.linspace(0, np.pi, grid_size)
        Theta, Phi = np.meshgrid(theta, phi)
        
        # Create a sphere for the visible dimensions
        R_visible = 3.0
        X_visible = R_visible * np.sin(Phi) * np.cos(Theta)
        Y_visible = R_visible * np.sin(Phi) * np.sin(Theta)
        Z_visible = R_visible * np.cos(Phi)
        
        # Plot the visible dimensions as a transparent sphere
        ax.plot_surface(X_visible, Y_visible, Z_visible, color='blue', alpha=0.1,
                       linewidth=0, antialiased=True)
        
        # Create Calabi-Yau manifold for extra dimensions (simplified representation)
        # In reality, Calabi-Yau manifolds are 6-dimensional and very complex
        
        # Create a grid for the extra dimensions
        u = np.linspace(0, 2 * np.pi, grid_size)
        v = np.linspace(0, 2 * np.pi, grid_size)
        U, V = np.meshgrid(u, v)
        
        # Create multiple Calabi-Yau manifolds at different points
        num_points = 10
        np.random.seed(42)  # For reproducibility
        
        for _ in range(num_points):
            # Random position on the visible sphere
            theta_pos = np.random.uniform(0, 2 * np.pi)
            phi_pos = np.random.uniform(0, np.pi)
            
            # Calculate position in Cartesian coordinates
            x_pos = R_visible * np.sin(phi_pos) * np.cos(theta_pos)
            y_pos = R_visible * np.sin(phi_pos) * np.sin(theta_pos)
            z_pos = R_visible * np.cos(phi_pos)
            
            # Create a small Calabi-Yau manifold at this position (simplified as a complex shape)
            R_extra = 0.5
            
            # Create a complex shape to represent the extra dimensions
            X_extra = x_pos + R_extra * (np.sin(U) * np.cos(V) + 0.5 * np.sin(2*U) * np.cos(3*V))
            Y_extra = y_pos + R_extra * (np.sin(U) * np.sin(V) + 0.5 * np.sin(3*U) * np.sin(2*V))
            Z_extra = z_pos + R_extra * (np.cos(U) + 0.5 * np.sin(V) * np.cos(U))
            
            # Plot the extra dimensions with a different color for each manifold
            cmap = plt.cm.viridis
            color = cmap(np.random.random())
            
            ax.plot_surface(X_extra, Y_extra, Z_extra, color=color, alpha=0.7,
                           linewidth=0, antialiased=True)
        
        # Add labels
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        ax.set_zlabel('Z', fontsize=12)
        ax.set_title(f'3D Visualization of {num_dimensions}D Space', fontsize=14)
        
        # Add text explaining the visualization
        plt.figtext(0.02, 0.02, 
                   f"This visualization represents a {num_dimensions}-dimensional space.\n"
                   "The large transparent sphere represents our visible 3D space.\n"
                   "The small complex shapes represent the extra dimensions\n"
                   "compactified at each point in our 3D space.", fontsize=10)
        
        plt.tight_layout()
        plt.show()

    def visualize_4d_higgs_field(self, grid_size=30):
        """
        Visualize the 4D Higgs field with symmetry breaking

        Parameters:
        -----------
        grid_size : int
            Size of the grid for visualization
        """
        # Create figure
        fig = plt.figure(figsize=(14, 12))
        
        # Create a 2D grid for the real and imaginary parts of the Higgs field
        phi_real = np.linspace(-2, 2, grid_size)
        phi_imag = np.linspace(-2, 2, grid_size)
        Phi_real, Phi_imag = np.meshgrid(phi_real, phi_imag)
        
        # Higgs potential parameters
        mu2 = 1.0  # Quadratic coefficient (positive for symmetry breaking)
        lambda_ = 0.5  # Quartic coefficient
        
        # Calculate Higgs potential: V(φ) = -μ²|φ|² + λ|φ|⁴
        Phi_squared = Phi_real**2 + Phi_imag**2
        V = -mu2 * Phi_squared + lambda_ * Phi_squared**2
        
        # Create 3D plot for the Mexican hat potential
        ax1 = fig.add_subplot(121, projection='3d')
        
        # Plot the Mexican hat potential
        surf1 = ax1.plot_surface(Phi_real, Phi_imag, V, cmap=cm.viridis, alpha=0.8,
                               linewidth=0, antialiased=True)
        
        # Add a color bar
        fig.colorbar(surf1, ax=ax1, shrink=0.5, aspect=10, label='Potential Energy')
        
        # Add labels
        ax1.set_xlabel('Re(φ)', fontsize=12)
        ax1.set_ylabel('Im(φ)', fontsize=12)
        ax1.set_zlabel('V(φ)', fontsize=12)
        ax1.set_title('Higgs Potential (Mexican Hat)', fontsize=14)
        
        # Create a 3D plot for the 4D visualization (3D + color)
        ax2 = fig.add_subplot(122, projection='3d')
        
        # Create a circle at the minimum of the potential
        theta = np.linspace(0, 2*np.pi, 100)
        v = np.sqrt(mu2 / (2 * lambda_))  # Vacuum expectation value
        circle_x = v * np.cos(theta)
        circle_y = v * np.sin(theta)
        circle_z = np.zeros_like(theta)
        
        # Plot the circle of minima
        ax2.plot(circle_x, circle_y, circle_z, 'r-', linewidth=3, label='Potential Minima')
        
        # Create a 3D vector field to represent the Higgs field in 4D
        # The 4th dimension (field magnitude) is represented by color
        
        # Create a grid of points in 3D space
        x = np.linspace(-1.5, 1.5, 8)
        y = np.linspace(-1.5, 1.5, 8)
        z = np.linspace(-1.5, 1.5, 8)
        X, Y, Z = np.meshgrid(x, y, z)
        
        # Calculate the Higgs field at each point (simplified model)
        # In reality, this would involve solving field equations
        
        # Distance from origin
        R = np.sqrt(X**2 + Y**2 + Z**2)
        
        # Field direction (normalized position vector)
        U = X / np.maximum(R, 0.1)  # Avoid division by zero
        V = Y / np.maximum(R, 0.1)
        W = Z / np.maximum(R, 0.1)
        
        # Field magnitude (approaches v at large distances)
        Magnitude = v * (1 - np.exp(-R))
        
        # Create a custom colormap for the field magnitude
        norm = colors.Normalize(vmin=0, vmax=v)
        
        # Plot the vector field
        ax2.quiver(X, Y, Z, U, V, W, length=0.2, normalize=True, 
                  color=plt.cm.plasma(norm(Magnitude.flatten())), alpha=0.8)
        
        # Add a color bar for the field magnitude
        cbar = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=plt.cm.plasma), 
                           ax=ax2, shrink=0.5, aspect=10)
        cbar.set_label('Higgs Field Magnitude (4th Dimension)', fontsize=10)
        
        # Add labels
        ax2.set_xlabel('X', fontsize=12)
        ax2.set_ylabel('Y', fontsize=12)
        ax2.set_zlabel('Z', fontsize=12)
        ax2.set_title('4D Higgs Field Visualization', fontsize=14)
        ax2.legend()
        
        # Add text explaining the visualization
        plt.figtext(0.02, 0.02, 
                   "This visualization shows the 4D Higgs field.\n"
                   "Left: The Mexican hat potential in the complex φ plane.\n"
                   "Right: The Higgs field in 3D space, with the 4th dimension\n"
                   "(field magnitude) represented by color.", fontsize=10)
        
        plt.tight_layout()
        plt.show()

    def visualize_gauge_field_4d(self, grid_size=10):
        """
        Visualize a 4D gauge field configuration

        Parameters:
        -----------
        grid_size : int
            Size of the grid for visualization
        """
        # Create figure
        fig = plt.figure(figsize=(14, 12))
        ax = fig.add_subplot(111, projection='3d')
        
        # Create a grid of points in 3D space
        x = np.linspace(-2, 2, grid_size)
        y = np.linspace(-2, 2, grid_size)
        z = np.linspace(-2, 2, grid_size)
        X, Y, Z = np.meshgrid(x, y, z)
        
        # Calculate a non-Abelian gauge field configuration (simplified model)
        # In reality, this would involve solving Yang-Mills equations
        
        # Distance from origin
        R = np.sqrt(X**2 + Y**2 + Z**2)
        
        # Angle in xy-plane
        Theta = np.arctan2(Y, X)
        
        # Create a magnetic monopole-like configuration
        # Field components (simplified non-Abelian field)
        Bx = X * Z / (R**3 + 0.1)
        By = Y * Z / (R**3 + 0.1)
        Bz = (Z**2 - X**2 - Y**2) / (R**3 + 0.1)
        
        # Field strength (4th dimension)
        B_strength = np.sqrt(Bx**2 + By**2 + Bz**2)
        
        # Create a custom colormap for the field strength
        norm = colors.Normalize(vmin=0, vmax=np.max(B_strength))
        
        # Plot the vector field
        ax.quiver(X, Y, Z, Bx, By, Bz, length=0.2, normalize=True,
                 color=plt.cm.viridis(norm(B_strength.flatten())), alpha=0.8)
        
        # Add a color bar for the field strength
        cbar = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=plt.cm.viridis), 
                           ax=ax, shrink=0.5, aspect=10)
        cbar.set_label('Field Strength (4th Dimension)', fontsize=12)
        
        # Add a sphere at the origin to represent the source
        u = np.linspace(0, 2 * np.pi, 20)
        v = np.linspace(0, np.pi, 20)
        x_sphere = 0.2 * np.outer(np.cos(u), np.sin(v))
        y_sphere = 0.2 * np.outer(np.sin(u), np.sin(v))
        z_sphere = 0.2 * np.outer(np.ones(np.size(u)), np.cos(v))
        
        ax.plot_surface(x_sphere, y_sphere, z_sphere, color='red', alpha=0.8)
        
        # Add labels
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        ax.set_zlabel('Z', fontsize=12)
        ax.set_title('4D Non-Abelian Gauge Field Visualization', fontsize=14)
        
        # Add text explaining the visualization
        plt.figtext(0.02, 0.02, 
                   "This visualization shows a 4D non-Abelian gauge field.\n"
                   "The arrows represent the field direction in 3D space,\n"
                   "while the color represents the field strength (4th dimension).\n"
                   "This configuration is similar to a magnetic monopole in SU(2) gauge theory.", fontsize=10)
        
        plt.tight_layout()
        plt.show()


def demonstrate_advanced_visualizations():
    """Demonstrate the advanced visualizations"""
    print("\n===== Advanced 3D and 4D Visualizations =====\n")
    
    # Create an instance of the advanced visualizations
    advanced_vis = AdvancedVisualizations()
    
    # Ask user which visualization to show
    print("Select a visualization to display:")
    print("1. 4D Spacetime Curvature")
    print("2. Quantum Foam in 3D")
    print("3. String Worldsheet in 3D")
    print("4. Extra Dimensions (String Theory)")
    print("5. 4D Higgs Field")
    print("6. 4D Gauge Field Configuration")
    print("0. Exit")
    
    choice = input("\nEnter your choice (0-6): ")
    
    if choice == '1':
        advanced_vis.visualize_4d_spacetime_curvature()
    elif choice == '2':
        advanced_vis.visualize_quantum_foam_3d()
    elif choice == '3':
        advanced_vis.visualize_string_worldsheet_3d()
    elif choice == '4':
        advanced_vis.visualize_extra_dimensions_3d()
    elif choice == '5':
        advanced_vis.visualize_4d_higgs_field()
    elif choice == '6':
        advanced_vis.visualize_gauge_field_4d()
    elif choice == '0':
        return
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    demonstrate_advanced_visualizations()

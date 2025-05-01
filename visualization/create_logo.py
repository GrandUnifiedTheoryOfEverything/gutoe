#!/usr/bin/env python3
"""
Create a logo for the Theory of Everything project
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

def create_logo():
    """Create a logo for the Theory of Everything project"""
    # Create a figure
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Create a sphere
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = 1 * np.outer(np.cos(u), np.sin(v))
    y = 1 * np.outer(np.sin(u), np.sin(v))
    z = 1 * np.outer(np.ones(np.size(u)), np.cos(v))
    
    # Plot the sphere
    ax.plot_surface(x, y, z, color='b', alpha=0.3)
    
    # Create a torus
    R, r = 1.5, 0.3
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, 2 * np.pi, 100)
    u, v = np.meshgrid(u, v)
    x = (R + r * np.cos(v)) * np.cos(u)
    y = (R + r * np.cos(v)) * np.sin(u)
    z = r * np.sin(v)
    
    # Plot the torus
    ax.plot_surface(x, y, z, color='r', alpha=0.3)
    
    # Add some particles
    n_particles = 50
    phi = np.random.uniform(0, 2 * np.pi, n_particles)
    theta = np.random.uniform(0, np.pi, n_particles)
    r = np.random.uniform(0.5, 2.0, n_particles)
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    
    # Plot the particles
    ax.scatter(x, y, z, c='y', s=20)
    
    # Add some field lines
    n_lines = 20
    phi = np.random.uniform(0, 2 * np.pi, n_lines)
    theta = np.random.uniform(0, np.pi, n_lines)
    for i in range(n_lines):
        t = np.linspace(0, 2, 100)
        x = t * np.sin(theta[i]) * np.cos(phi[i])
        y = t * np.sin(theta[i]) * np.sin(phi[i])
        z = t * np.cos(theta[i])
        ax.plot(x, y, z, 'g-', alpha=0.5)
    
    # Remove axes
    ax.set_axis_off()
    
    # Set equal aspect ratio
    ax.set_box_aspect([1, 1, 1])
    
    # Add title
    ax.set_title("Theory of Everything", fontsize=16)
    
    # Save the logo
    os.makedirs("gfx", exist_ok=True)
    plt.savefig("gfx/toe_logo.png", dpi=300, bbox_inches="tight", transparent=True)
    plt.close()
    
    print("Logo created: gfx/toe_logo.png")

if __name__ == "__main__":
    create_logo()

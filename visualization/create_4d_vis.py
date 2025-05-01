#!/usr/bin/env python3
"""
Create advanced 4D visualizations for the Theory of Everything project
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

def create_4d_animation(output_dir="gfx/4d", filename="4d_spacetime_evolution.gif"):
    """Create a 4D animation of spacetime evolution"""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create a figure
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Set up grid
    grid_size = 20
    x = np.linspace(-5, 5, grid_size)
    y = np.linspace(-5, 5, grid_size)
    X, Y = np.meshgrid(x, y)
    
    # Function to update the plot for each frame
    def update(frame):
        ax.clear()
        
        # Calculate time-dependent spacetime curvature
        time = frame / 10.0  # Time parameter
        r = np.sqrt(X**2 + Y**2 + 0.1**2)  # Add small constant to avoid division by zero
        
        # Simulate a gravitational wave passing through
        Z = np.sin(r - time) / r
        
        # Plot the surface with time as color
        surf = ax.plot_surface(X, Y, Z, cmap=cm.viridis,
                              linewidth=0, antialiased=True)
        
        # Add labels
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'4D Spacetime Evolution (t = {time:.1f})')
        ax.set_zlim(-1, 1)
        
        return [surf]
    
    # Create the animation
    ani = animation.FuncAnimation(fig, update, frames=30, interval=100, blit=False)
    
    # Save the animation
    output_path = os.path.join(output_dir, filename)
    ani.save(output_path, writer='pillow', fps=10)
    
    plt.close()
    
    print(f"4D animation created: {output_path}")
    return output_path

def create_4d_projection(output_dir="gfx/4d", filename="4d_hypercube_projection.png"):
    """Create a 4D hypercube projection"""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create a figure
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Define the vertices of a 4D hypercube
    vertices_4d = np.array([
        [1, 1, 1, 1], [1, 1, 1, -1], [1, 1, -1, 1], [1, 1, -1, -1],
        [1, -1, 1, 1], [1, -1, 1, -1], [1, -1, -1, 1], [1, -1, -1, -1],
        [-1, 1, 1, 1], [-1, 1, 1, -1], [-1, 1, -1, 1], [-1, 1, -1, -1],
        [-1, -1, 1, 1], [-1, -1, 1, -1], [-1, -1, -1, 1], [-1, -1, -1, -1]
    ])
    
    # Define a 4D to 3D projection matrix (perspective projection)
    # Project from 4D to 3D by dividing by (w + distance)
    distance = 4
    vertices_3d = np.zeros((16, 3))
    for i, v in enumerate(vertices_4d):
        w = v[3]
        scale = 1 / (w + distance)
        vertices_3d[i] = v[:3] * scale
    
    # Plot the vertices
    ax.scatter(vertices_3d[:, 0], vertices_3d[:, 1], vertices_3d[:, 2], c='r', s=50)
    
    # Define the edges of the hypercube
    edges = []
    for i in range(16):
        for j in range(i+1, 16):
            # Connect vertices that differ in exactly one coordinate
            diff = np.sum(np.abs(vertices_4d[i] - vertices_4d[j]))
            if diff == 2:  # In a hypercube, connected vertices differ by 2 in 4D space
                edges.append((i, j))
    
    # Plot the edges
    for i, j in edges:
        ax.plot([vertices_3d[i, 0], vertices_3d[j, 0]],
                [vertices_3d[i, 1], vertices_3d[j, 1]],
                [vertices_3d[i, 2], vertices_3d[j, 2]], 'b-')
    
    # Add labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('4D Hypercube Projection')
    
    # Set equal aspect ratio
    ax.set_box_aspect([1, 1, 1])
    
    # Save the figure
    output_path = os.path.join(output_dir, filename)
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    
    print(f"4D projection created: {output_path}")
    return output_path

def create_4d_quantum_field(output_dir="gfx/4d", filename="4d_quantum_field.png"):
    """Create a 4D quantum field visualization"""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create a figure
    fig = plt.figure(figsize=(12, 10))
    
    # Create a 2x2 grid of 3D plots to represent different slices of 4D
    titles = ['W = -1.0', 'W = -0.33', 'W = 0.33', 'W = 1.0']
    w_values = [-1.0, -0.33, 0.33, 1.0]
    
    for i, (title, w) in enumerate(zip(titles, w_values)):
        ax = fig.add_subplot(2, 2, i+1, projection='3d')
        
        # Set up grid
        grid_size = 20
        x = np.linspace(-3, 3, grid_size)
        y = np.linspace(-3, 3, grid_size)
        X, Y = np.meshgrid(x, y)
        
        # Calculate quantum field with w-dependence
        R = np.sqrt(X**2 + Y**2 + w**2)
        Z = np.sin(5*R) / R
        
        # Plot the surface
        surf = ax.plot_surface(X, Y, Z, cmap=cm.plasma,
                              linewidth=0, antialiased=True)
        
        # Add labels
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(title)
        ax.set_zlim(-1, 1)
    
    # Add a main title
    plt.suptitle('4D Quantum Field Visualization', fontsize=16)
    plt.tight_layout()
    
    # Save the figure
    output_path = os.path.join(output_dir, filename)
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    
    print(f"4D quantum field created: {output_path}")
    return output_path

if __name__ == "__main__":
    # Create all 4D visualizations
    create_4d_animation()
    create_4d_projection()
    create_4d_quantum_field()

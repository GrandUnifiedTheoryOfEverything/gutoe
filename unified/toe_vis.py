#!/usr/bin/env python3
"""
Theory of Everything - Visualization Tools

This module provides tools for visualizing the Theory of Everything,
with a focus on 3D and 4D representations.
"""

import os
import json
from .toe_core import ToECore, load_json_safely


class VisualizationTools:
    """
    Tools for generating visualizations
    """
    
    def __init__(self, core=None):
        """
        Initialize the visualization tools
        
        Parameters:
        -----------
        core : ToECore or None
            Core API instance (will create a new one if None)
        """
        self.core = core if core is not None else ToECore()

        # Define available visualizations
        self.available_visualizations = {
            '4d_spacetime_curvature': {
                'description': 'Visualize 4D spacetime around massive objects',
                'parameters': {
                    'mass': {
                        'description': 'Mass of the central object (in solar masses)',
                        'type': 'float',
                        'default': 1.0,
                        'min': 0.1,
                        'max': 10.0
                    },
                    'grid_size': {
                        'description': 'Size of the grid for visualization',
                        'type': 'int',
                        'default': 20,
                        'min': 10,
                        'max': 50
                    },
                    'output_dir': {
                        'description': 'Directory to save the visualization',
                        'type': 'string',
                        'default': 'gfx/3d'
                    }
                }
            },
            'quantum_foam_3d': {
                'description': 'Visualize quantum foam in 3D',
                'parameters': {
                    'grid_size': {
                        'description': 'Size of the grid for visualization',
                        'type': 'int',
                        'default': 20,
                        'min': 10,
                        'max': 30
                    },
                    'amplitude': {
                        'description': 'Amplitude of quantum fluctuations',
                        'type': 'float',
                        'default': 0.5,
                        'min': 0.1,
                        'max': 1.0
                    },
                    'frequency': {
                        'description': 'Frequency of quantum fluctuations',
                        'type': 'float',
                        'default': 2.0,
                        'min': 0.5,
                        'max': 5.0
                    },
                    'output_dir': {
                        'description': 'Directory to save the visualization',
                        'type': 'string',
                        'default': 'gfx/3d'
                    }
                }
            },
            'extra_dimensions_3d': {
                'description': 'Visualize extra dimensions in 3D',
                'parameters': {
                    'num_dimensions': {
                        'description': 'Total number of dimensions to represent',
                        'type': 'int',
                        'default': 10,
                        'min': 4,
                        'max': 11
                    },
                    'grid_size': {
                        'description': 'Size of the grid for visualization',
                        'type': 'int',
                        'default': 20,
                        'min': 10,
                        'max': 30
                    },
                    'output_dir': {
                        'description': 'Directory to save the visualization',
                        'type': 'string',
                        'default': 'gfx/3d'
                    }
                }
            },
            '4d_higgs_field': {
                'description': 'Visualize the 4D Higgs field',
                'parameters': {
                    'grid_size': {
                        'description': 'Size of the grid for visualization',
                        'type': 'int',
                        'default': 30,
                        'min': 10,
                        'max': 50
                    },
                    'output_dir': {
                        'description': 'Directory to save the visualization',
                        'type': 'string',
                        'default': 'gfx/3d'
                    }
                }
            },
            'gauge_field_4d': {
                'description': 'Visualize a 4D gauge field configuration',
                'parameters': {
                    'grid_size': {
                        'description': 'Size of the grid for visualization',
                        'type': 'int',
                        'default': 10,
                        'min': 5,
                        'max': 20
                    },
                    'output_dir': {
                        'description': 'Directory to save the visualization',
                        'type': 'string',
                        'default': 'gfx/3d'
                    }
                }
            }
        }

    def list_visualizations(self):
        """
        List all available visualizations

        Returns:
        --------
        dict
            Dictionary mapping visualization names to descriptions
        """
        return {name: info['description'] for name, info in self.available_visualizations.items()}

    def get_visualization_info(self, visualization_name):
        """
        Get information about a visualization

        Parameters:
        -----------
        visualization_name : str
            Name of the visualization

        Returns:
        --------
        dict
            Dictionary containing information about the visualization
        """
        if visualization_name not in self.available_visualizations:
            raise ValueError(f"Unknown visualization: {visualization_name}. "
                           f"Available visualizations: {list(self.available_visualizations.keys())}")

        return self.available_visualizations[visualization_name]

    def get_visualization_parameters(self, visualization_name):
        """
        Get the parameters for a visualization

        Parameters:
        -----------
        visualization_name : str
            Name of the visualization

        Returns:
        --------
        dict
            Dictionary mapping parameter names to parameter information
        """
        info = self.get_visualization_info(visualization_name)
        return info.get('parameters', {})

    def validate_parameters(self, visualization_name, params):
        """
        Validate parameters for a visualization

        Parameters:
        -----------
        visualization_name : str
            Name of the visualization
        params : dict
            Parameters to validate

        Returns:
        --------
        dict
            Dictionary mapping parameter names to validation results
        """
        param_info = self.get_visualization_parameters(visualization_name)
        results = {}

        for name, info in param_info.items():
            if name not in params:
                # Parameter not provided, use default
                results[name] = {
                    'valid': True,
                    'value': info['default'],
                    'message': f"Using default value: {info['default']}"
                }
                continue

            value = params[name]

            # Check type
            if info['type'] == 'int':
                try:
                    value = int(value)
                except (ValueError, TypeError):
                    results[name] = {
                        'valid': False,
                        'value': info['default'],
                        'message': f"Invalid integer value: {value}. Using default: {info['default']}"
                    }
                    continue
            elif info['type'] == 'float':
                try:
                    value = float(value)
                except (ValueError, TypeError):
                    results[name] = {
                        'valid': False,
                        'value': info['default'],
                        'message': f"Invalid float value: {value}. Using default: {info['default']}"
                    }
                    continue

            # Check range
            if 'min' in info and value < info['min']:
                results[name] = {
                    'valid': False,
                    'value': info['min'],
                    'message': f"Value {value} is below minimum {info['min']}. Using minimum value."
                }
                continue

            if 'max' in info and value > info['max']:
                results[name] = {
                    'valid': False,
                    'value': info['max'],
                    'message': f"Value {value} is above maximum {info['max']}. Using maximum value."
                }
                continue

            # Parameter is valid
            results[name] = {
                'valid': True,
                'value': value,
                'message': f"Valid value: {value}"
            }

        return results

    def generate_visualization(self, visualization_name, params=None, show=False):
        """
        Generate a visualization

        Parameters:
        -----------
        visualization_name : str
            Name of the visualization to generate
        params : dict or None
            Parameters for the visualization (if None, will use defaults)
        show : bool
            Whether to display the visualization (default: False)

        Returns:
        --------
        str
            Path to the saved visualization
        """
        if visualization_name not in self.available_visualizations:
            raise ValueError(f"Unknown visualization: {visualization_name}. "
                           f"Available visualizations: {list(self.available_visualizations.keys())}")

        # Validate parameters
        if params is None:
            params = {}

        validation = self.validate_parameters(visualization_name, params)
        validated_params = {name: result['value'] for name, result in validation.items()}

        # Define the script to generate the visualization
        script = self._get_visualization_script(visualization_name, validated_params, show)

        # Run the script
        result = self.core.run_with_math_safety(
            self.core.run_script_safely,
            script,
            args=[]
        )

        # Parse the result
        try:
            return result.strip()
        except:
            return f"Error generating visualization: {result}"

    def _get_visualization_script(self, visualization_name, params, show):
        """
        Get the script to generate a visualization

        Parameters:
        -----------
        visualization_name : str
            Name of the visualization
        params : dict
            Validated parameters for the visualization
        show : bool
            Whether to display the visualization

        Returns:
        --------
        str
            Script to generate the visualization
        """
        # Common imports and setup
        script = """
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm, colors

# Get the output directory from parameters or use default
output_dir = params.get('output_dir', 'gfx/3d')

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
"""

        # Add visualization-specific code
        if visualization_name == '4d_spacetime_curvature':
            script += self._get_spacetime_curvature_script(params, show)
        elif visualization_name == 'quantum_foam_3d':
            script += self._get_quantum_foam_script(params, show)
        elif visualization_name == 'extra_dimensions_3d':
            script += self._get_extra_dimensions_script(params, show)
        elif visualization_name == '4d_higgs_field':
            script += self._get_higgs_field_script(params, show)
        elif visualization_name == 'gauge_field_4d':
            script += self._get_gauge_field_script(params, show)

        return script

    def _get_spacetime_curvature_script(self, params, show):
        """Get the script for the 4D spacetime curvature visualization"""
        mass = params.get('mass', 1.0)
        grid_size = params.get('grid_size', 20)

        return f"""
# Parameters
mass = {mass}  # Mass of the central object (in solar masses)
grid_size = {grid_size}  # Size of the grid for visualization
c = 299792458  # Speed of light
G = 6.67430e-11  # Gravitational constant

# Create a grid of points
x = np.linspace(-10, 10, grid_size)
y = np.linspace(-10, 10, grid_size)
X, Y = np.meshgrid(x, y)

# Calculate Schwarzschild metric for a black hole
r = np.sqrt(X**2 + Y**2 + 0.1**2)  # Add small constant to avoid division by zero
M = mass * 1.989e30  # Convert solar masses to kg
Rs = 2 * G * M / (c**2)  # Schwarzschild radius

# Calculate time component of the metric (g_tt)
g_tt = -(1 - Rs/r)

# Calculate spatial curvature (simplified)
Z = -Rs / (2 * r)

# Create 3D plot with time component as color
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Create a custom colormap for the time dimension
min_val = np.min(g_tt)
max_val = np.max(g_tt)
norm = colors.Normalize(vmin=min_val, vmax=max_val)

# Plot the surface with time as color
surf = ax.plot_surface(X, Y, Z, facecolors=cm.viridis(norm(g_tt)),
                      linewidth=0, antialiased=True)

# Add a color bar for the time dimension
cbar = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cm.viridis),
                   ax=ax, shrink=0.5, aspect=10)
cbar.set_label('Time Dilation (g_tt)', fontsize=10)

# Add labels
ax.set_xlabel('X', fontsize=10)
ax.set_ylabel('Y', fontsize=10)
ax.set_zlabel('Curvature', fontsize=10)
ax.set_title('4D Spacetime Curvature', fontsize=12)

# Save the visualization
save_path = os.path.join(output_dir, '4d_spacetime_curvature.png')
plt.savefig(save_path, dpi=300, bbox_inches='tight')

# Show the visualization if requested
if {show}:
    plt.show()
else:
    plt.close()

# Print the path to the saved visualization
print(save_path)
"""

    def _get_quantum_foam_script(self, params, show):
        """Get the script for the quantum foam visualization"""
        grid_size = params.get('grid_size', 20)
        amplitude = params.get('amplitude', 0.5)
        frequency = params.get('frequency', 2.0)

        return f"""
# Parameters
grid_size = {grid_size}  # Size of the grid for visualization
amplitude = {amplitude}  # Amplitude of quantum fluctuations
frequency = {frequency}  # Frequency of quantum fluctuations

# Create a simplified quantum foam visualization
# In a real implementation, this would be a 3D voxel visualization

# Create a 2D grid for simplicity
x = np.linspace(-5, 5, grid_size)
y = np.linspace(-5, 5, grid_size)
X, Y = np.meshgrid(x, y)

# Generate random phases
np.random.seed(42)  # For reproducibility
phases = 2 * np.pi * np.random.random((3, 3))

# Calculate quantum fluctuations with multiple frequency components
Z = np.zeros_like(X)
for i in range(3):
    for j in range(3):
        Z += amplitude * (1.0/(i+j+1)) * np.sin(frequency*(i+1)*X + phases[i,j]) * \
             np.sin(frequency*(j+1)*Y + phases[i,j])

# Create a 3D surface plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
surf = ax.plot_surface(X, Y, Z, cmap=cm.viridis,
                      linewidth=0, antialiased=True)

# Add a color bar
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)

# Add labels
ax.set_xlabel('X', fontsize=10)
ax.set_ylabel('Y', fontsize=10)
ax.set_zlabel('Quantum Fluctuations', fontsize=10)
ax.set_title('Quantum Foam Visualization', fontsize=12)

# Save the visualization
save_path = os.path.join(output_dir, 'quantum_foam_3d.png')
plt.savefig(save_path, dpi=300, bbox_inches='tight')

# Show the visualization if requested
if {show}:
    plt.show()
else:
    plt.close()

# Print the path to the saved visualization
print(save_path)
"""

    def _get_extra_dimensions_script(self, params, show):
        """Get the script for the extra dimensions visualization"""
        num_dimensions = params.get('num_dimensions', 10)
        grid_size = params.get('grid_size', 20)

        return f"""
# Parameters
num_dimensions = {num_dimensions}  # Total number of dimensions to represent
grid_size = {grid_size}  # Size of the grid for visualization

# Create a simplified extra dimensions visualization
# In a real implementation, this would be a more complex 3D visualization

# Create a sphere for the visible dimensions
theta = np.linspace(0, 2 * np.pi, grid_size)
phi = np.linspace(0, np.pi, grid_size)
theta, phi = np.meshgrid(theta, phi)

r = 2 + 0.5 * np.sin(3 * theta) * np.sin(4 * phi)  # Add some variation to represent extra dimensions

x = r * np.sin(phi) * np.cos(theta)
y = r * np.sin(phi) * np.sin(theta)
z = r * np.cos(phi)

# Create a 3D surface plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
surf = ax.plot_surface(x, y, z, cmap=cm.viridis,
                      linewidth=0, antialiased=True)

# Add a color bar
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label='Extra Dimensions')

# Add labels
ax.set_xlabel('X', fontsize=10)
ax.set_ylabel('Y', fontsize=10)
ax.set_zlabel('Z', fontsize=10)
ax.set_title(f'{num_dimensions}D Space Visualization', fontsize=12)

# Save the visualization
save_path = os.path.join(output_dir, 'extra_dimensions_3d.png')
plt.savefig(save_path, dpi=300, bbox_inches='tight')

# Show the visualization if requested
if {show}:
    plt.show()
else:
    plt.close()

# Print the path to the saved visualization
print(save_path)
"""

    def _get_higgs_field_script(self, params, show):
        """Get the script for the Higgs field visualization"""
        grid_size = params.get('grid_size', 30)

        return f"""
# Parameters
grid_size = {grid_size}  # Size of the grid for visualization

# Create a simplified Higgs field visualization
# In a real implementation, this would be a more complex 3D visualization

# Create a 2D grid for the Mexican hat potential
x = np.linspace(-2, 2, grid_size)
y = np.linspace(-2, 2, grid_size)
X, Y = np.meshgrid(x, y)

# Calculate the Higgs potential (Mexican hat)
R2 = X**2 + Y**2
V = (R2 - 1)**2

# Create a 3D surface plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
surf = ax.plot_surface(X, Y, V, cmap=cm.viridis,
                      linewidth=0, antialiased=True)

# Add a color bar
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label='Potential Energy')

# Add labels
ax.set_xlabel('Re(φ)', fontsize=10)
ax.set_ylabel('Im(φ)', fontsize=10)
ax.set_zlabel('V(φ)', fontsize=10)
ax.set_title('Higgs Potential (Mexican Hat)', fontsize=12)

# Save the visualization
save_path = os.path.join(output_dir, '4d_higgs_field.png')
plt.savefig(save_path, dpi=300, bbox_inches='tight')

# Show the visualization if requested
if {show}:
    plt.show()
else:
    plt.close()

# Print the path to the saved visualization
print(save_path)
"""

    def _get_gauge_field_script(self, params, show):
        """Get the script for the gauge field visualization"""
        grid_size = params.get('grid_size', 10)

        return f"""
# Parameters
grid_size = {grid_size}  # Size of the grid for visualization

# Create a simplified gauge field visualization
# In a real implementation, this would be a more complex 3D visualization

# Create a 3D grid
x = np.linspace(-2, 2, grid_size)
y = np.linspace(-2, 2, grid_size)
z = np.linspace(-2, 2, grid_size)
X, Y, Z = np.meshgrid(x, y, z)

# Calculate a simple vector field (magnetic dipole)
R = np.sqrt(X**2 + Y**2 + Z**2)
R3 = np.maximum(R**3, 0.001)  # Avoid division by zero

# Magnetic dipole field components
Bx = 3 * X * Z / R3
By = 3 * Y * Z / R3
Bz = (3 * Z**2 - R**2) / R3

# Create a 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot the vector field (subsample for clarity)
stride = 2
ax.quiver(X[::stride, ::stride, ::stride],
         Y[::stride, ::stride, ::stride],
         Z[::stride, ::stride, ::stride],
         Bx[::stride, ::stride, ::stride],
         By[::stride, ::stride, ::stride],
         Bz[::stride, ::stride, ::stride],
         length=0.5, normalize=True, color='b')

# Add labels
ax.set_xlabel('X', fontsize=10)
ax.set_ylabel('Y', fontsize=10)
ax.set_zlabel('Z', fontsize=10)
ax.set_title('Gauge Field Visualization', fontsize=12)

# Save the visualization
save_path = os.path.join(output_dir, 'gauge_field_4d.png')
plt.savefig(save_path, dpi=300, bbox_inches='tight')

# Show the visualization if requested
if {show}:
    plt.show()
else:
    plt.close()

# Print the path to the saved visualization
print(save_path)
"""

    def batch_generate_visualizations(self, visualization_configs):
        """
        Generate multiple visualizations in batch

        Parameters:
        -----------
        visualization_configs : list
            List of dictionaries, each containing 'name' and 'params' keys

        Returns:
        --------
        dict
            Dictionary mapping visualization names to file paths
        """
        results = {}

        for config in visualization_configs:
            name = config.get('name')
            params = config.get('params', {})
            show = config.get('show', False)

            if name not in self.available_visualizations:
                results[name] = f"Error: Unknown visualization: {name}"
                continue

            try:
                path = self.generate_visualization(name, params, show)
                results[name] = path
            except Exception as e:
                results[name] = f"Error: {str(e)}"

        return results

    def suggest_parameters(self, visualization_name):
        """
        Suggest parameters for a visualization

        Parameters:
        -----------
        visualization_name : str
            Name of the visualization

        Returns:
        --------
        dict
            Dictionary mapping parameter names to suggested values
        """
        if visualization_name not in self.available_visualizations:
            raise ValueError(f"Unknown visualization: {visualization_name}. "
                           f"Available visualizations: {list(self.available_visualizations.keys())}")

        param_info = self.get_visualization_parameters(visualization_name)
        suggestions = {}

        for name, info in param_info.items():
            # Use the default value as the primary suggestion
            suggestions[name] = {
                'default': info['default'],
                'description': info['description'],
                'type': info['type']
            }

            # Add range information if available
            if 'min' in info:
                suggestions[name]['min'] = info['min']
            if 'max' in info:
                suggestions[name]['max'] = info['max']

            # Add some alternative suggestions based on the parameter type
            if info['type'] == 'int':
                if 'min' in info and 'max' in info:
                    # Suggest some values within the range
                    range_size = info['max'] - info['min']
                    step = max(1, range_size // 4)
                    alternatives = [
                        info['min'],
                        info['min'] + step,
                        info['default'],
                        info['max'] - step,
                        info['max']
                    ]
                    # Remove duplicates and sort
                    alternatives = sorted(set(alternatives))
                    suggestions[name]['alternatives'] = alternatives
            elif info['type'] == 'float':
                if 'min' in info and 'max' in info:
                    # Suggest some values within the range
                    range_size = info['max'] - info['min']
                    step = range_size / 4
                    alternatives = [
                        info['min'],
                        info['min'] + step,
                        info['default'],
                        info['max'] - step,
                        info['max']
                    ]
                    # Remove duplicates and sort
                    alternatives = sorted(set(alternatives))
                    suggestions[name]['alternatives'] = alternatives

        return suggestions

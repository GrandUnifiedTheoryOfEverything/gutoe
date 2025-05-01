# Theory of Everything - Visualization

This directory contains visualization tools for the Theory of Everything package.

## Available Visualizations

- **4D Spacetime Curvature**: Visualize 4D spacetime around massive objects
- **Quantum Foam 3D**: Visualize quantum foam in 3D
- **Extra Dimensions 3D**: Visualize extra dimensions in 3D
- **4D Higgs Field**: Visualize the 4D Higgs field
- **Gauge Field 4D**: Visualize a 4D gauge field configuration

## Usage

```python
from theoryofeverything.visualization import VisualizationTools

# Create a visualization tools instance
vis_tools = VisualizationTools()

# List available visualizations
visualizations = vis_tools.list_visualizations()
for name, description in visualizations.items():
    print(f"{name}: {description}")

# Get parameters for a visualization
params = vis_tools.get_visualization_parameters('4d_spacetime_curvature')
print(params)

# Generate a visualization
path = vis_tools.generate_visualization(
    '4d_spacetime_curvature',
    params={'mass': 2.0, 'grid_size': 30, 'output_dir': 'gfx/3d'},
    show=False
)
print(f"Visualization saved to: {path}")
```

## Output Directories

By default, visualizations are saved to the following directories:

- **2D Visualizations**: `gfx/2d/`
- **3D Visualizations**: `gfx/3d/`
- **4D Visualizations**: `gfx/4d/`

You can customize the output directory by passing the `output_dir` parameter to the visualization functions.

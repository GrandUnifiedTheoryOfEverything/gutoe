#!/usr/bin/env python3
"""
Test script for the Theory of Everything visualization functionality
"""

import os
import sys
import json

# Add the parent directory to the path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the visualization module
try:
    from toe_vis import VisualizationTools
    from toe_core import ToECore
    print("Successfully imported VisualizationTools")
except ImportError as e:
    print(f"Error importing VisualizationTools: {e}")
    sys.exit(1)

# Test the visualization functionality
try:
    # Create an instance of the core and visualization tools
    core = ToECore(output_dir="tests/vis_output")
    vis_tools = VisualizationTools(core=core)
    print("Successfully created VisualizationTools instance")
    
    # Test listing visualizations
    print("\nTesting visualization listing...")
    visualizations = vis_tools.list_visualizations()
    print(f"Found {len(visualizations)} visualizations:")
    for name, description in visualizations.items():
        print(f"  - {name}: {description}")
    
    # Test getting visualization information
    print("\nTesting visualization information...")
    for name in visualizations:
        info = vis_tools.get_visualization_info(name)
        print(f"  - {name}: {len(info['parameters'])} parameters")
    
    # Test parameter validation
    print("\nTesting parameter validation...")
    params = {"mass": 2.0, "grid_size": 15}
    validation = vis_tools.validate_parameters("4d_spacetime_curvature", params)
    print("Validation results:")
    for param_name, result in validation.items():
        print(f"  - {param_name}: {'Valid' if result['valid'] else 'Invalid'} ({result['value']})")
    
    # Test parameter suggestions
    print("\nTesting parameter suggestions...")
    suggestions = vis_tools.suggest_parameters("4d_spacetime_curvature")
    print("Suggested parameters:")
    for param_name, info in suggestions.items():
        print(f"  - {param_name}: {info['default']} ({info['description']})")
        if 'alternatives' in info:
            print(f"    Alternatives: {info['alternatives']}")
    
    # Test generating a simple visualization
    print("\nTesting visualization generation...")
    print("Generating a simple visualization (this may take a moment)...")
    params = {"grid_size": 10}  # Use a small grid for faster testing
    vis_path = vis_tools.generate_visualization("4d_spacetime_curvature", params)
    print(f"Visualization saved to: {vis_path}")
    
    print("\nAll tests passed!")
except Exception as e:
    print(f"\nError: {str(e)}")
    sys.exit(1)

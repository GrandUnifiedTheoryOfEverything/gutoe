#!/usr/bin/env python3
"""
Simple test script for the Theory of Everything API
"""

import os
import sys
import json

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the API
try:
    from toe_api import ToEAPI
    print("Successfully imported ToEAPI")
except ImportError as e:
    print(f"Error importing ToEAPI: {e}")
    sys.exit(1)

# Create an instance of the API
try:
    api = ToEAPI(output_dir="test_visualizations")
    print("Successfully created ToEAPI instance")
except Exception as e:
    print(f"Error creating ToEAPI instance: {e}")
    sys.exit(1)

# Test listing visualizations
try:
    visualizations = api.list_visualizations()
    print(f"Available visualizations: {list(visualizations.keys())}")
except Exception as e:
    print(f"Error listing visualizations: {e}")

# Test getting a formula
try:
    formula = api.get_formula("unified_action")
    print(f"Successfully retrieved formula: {formula['name']}")
except Exception as e:
    print(f"Error getting formula: {e}")

# Test generating a simple visualization
try:
    print("Generating 4D spacetime curvature visualization...")
    vis_path = api.generate_visualization("4d_spacetime_curvature", {"grid_size": 10})
    print(f"Successfully generated visualization: {vis_path}")
except Exception as e:
    print(f"Error generating visualization: {e}")

print("Test completed")

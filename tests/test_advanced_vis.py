#!/usr/bin/env python3
"""
Test script for advanced visualizations
"""

import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Avoid conflicts with Python's built-in math module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Import directly from the file to avoid package issues
    from component_formulas.advanced_visualizations import AdvancedVisualizations
    print("Successfully imported advanced visualizations module")

    # Create an instance of the advanced visualizations
    advanced_vis = AdvancedVisualizations()

    # Display menu
    print("\n===== Advanced 3D and 4D Visualizations =====\n")
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
        sys.exit(0)
    else:
        print("Invalid choice.")

except ImportError as e:
    print(f"Error importing advanced visualizations: {e}")
    print("Make sure you have the correct directory structure and all dependencies installed.")
    sys.exit(1)

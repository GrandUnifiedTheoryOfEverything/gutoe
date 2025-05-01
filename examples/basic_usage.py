#!/usr/bin/env python3
"""
Basic usage example for the Theory of Everything
"""

import os
import sys
import json

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from theoryofeverything import ToEUnified

def main():
    """Main function"""
    # Create an instance of the API
    api = ToEUnified()

    # List available formulas
    print("Available formulas:")
    formulas = api.list_formulas()
    for name, description in formulas.items():
        print(f"  {name}: {description}")

    # List available visualizations
    print("\nAvailable visualizations:")
    visualizations = api.list_visualizations()
    for name, description in visualizations.items():
        print(f"  {name}: {description}")

    # Generate a visualization
    print("\nGenerating a visualization...")
    path = api.generate_visualization('4d_spacetime_curvature')
    print(f"Visualization saved to: {path}")

    print("\nDone!")

if __name__ == "__main__":
    main()

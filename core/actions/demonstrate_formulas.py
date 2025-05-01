#!/usr/bin/env python3
"""
Demonstration script for the Theory of Everything formula visualization.

This script provides a simple way to run the formula visualization module
directly from the command line.
"""

import sys
import os

# Add the parent directory to the path if running from the script's directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from math.toe_formulas import demonstrate_toe_formulas
except ImportError:
    print("Error: Could not import the toe_formulas module.")
    print("Make sure you have the correct directory structure and all dependencies installed.")
    sys.exit(1)

if __name__ == "__main__":
    print("=" * 80)
    print("GRAND UNIFIED THEORY OF EVERYTHING - FORMULA VISUALIZATION")
    print("=" * 80)
    print("\nThis script demonstrates the visualization of all formulas in the Theory of Everything.")
    print("You will be able to explore and visualize the mathematical foundations of the theory.")
    print("\nPress Enter to continue...")
    input()
    
    # Run the demonstration
    demonstrate_toe_formulas()
    
    print("\nThank you for exploring the Grand Unified Theory of Everything!")

#!/usr/bin/env python3
"""
Explore the Theory of Everything Formulas

This script provides a simple way to run the unified action interface
and explore all component formulas of the Theory of Everything.
"""

import sys
import os

# Add the current directory to the path if running from the script's directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# Also add the parent directory in case the script is in a subdirectory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from component_formulas.unified_action import main_menu
except ImportError:
    print("Error: Could not import the unified_action module.")
    print("Make sure you have the correct directory structure and all dependencies installed.")
    sys.exit(1)

if __name__ == "__main__":
    print("=" * 80)
    print("GRAND UNIFIED THEORY OF EVERYTHING - FORMULA EXPLORER")
    print("=" * 80)
    print("\nThis script allows you to explore all component formulas of the Theory of Everything.")
    print("You will be able to visualize and interact with the mathematical foundations of the theory.")
    print("\nPress Enter to continue...")
    input()

    # Run the main menu
    main_menu()

    print("\nThank you for exploring the Grand Unified Theory of Everything!")

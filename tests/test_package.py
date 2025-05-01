#!/usr/bin/env python3
"""
Test script for the Theory of Everything package
"""

import os
import sys
from theoryofeverything import ToEUnified

def main():
    """Main function"""
    print("Testing the Theory of Everything package...")
    
    # Create an instance of the API
    api = ToEUnified()
    
    # List available formulas
    print("\nAvailable formulas:")
    formulas = api.list_formulas()
    for name, description in formulas.items():
        print(f"  {name}: {description}")
    
    # List available visualizations
    print("\nAvailable visualizations:")
    visualizations = api.list_visualizations()
    for name, description in visualizations.items():
        print(f"  {name}: {description}")
    
    print("\nPackage test completed successfully!")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test script to check if the ToEUnified class has a list_formulas method
"""

import os
import sys

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Try to import the ToE modules
try:
    from toe_unified import ToEUnified
    print("Successfully imported ToEUnified")
except ImportError as e:
    print(f"Error importing ToEUnified: {e}")
    sys.exit(1)

# Create an instance of ToEUnified
try:
    api = ToEUnified()
    print("Successfully created ToEUnified instance")
except Exception as e:
    print(f"Error creating ToEUnified instance: {e}")
    sys.exit(1)

# Check if the list_formulas method exists
try:
    print("Checking if list_formulas method exists...")
    if hasattr(api, 'list_formulas'):
        print("list_formulas method exists")
        
        # Try to call the list_formulas method
        try:
            print("Calling list_formulas method...")
            formulas = api.list_formulas()
            print("Successfully called list_formulas method")
            print(f"Returned {len(formulas)} formulas")
            
            # Print the formulas
            print("Available formulas:")
            for name, description in formulas.items():
                print(f"  {name}: {description}")
        except Exception as e:
            print(f"Error calling list_formulas method: {e}")
    else:
        print("list_formulas method does not exist")
        
        # Print the available methods
        print("Available methods:")
        for method in dir(api):
            if not method.startswith('_'):
                print(f"  {method}")
except Exception as e:
    print(f"Error checking if list_formulas method exists: {e}")
    sys.exit(1)

#!/usr/bin/env python3
"""
Test script for the Theory of Everything core module
"""

import os
import sys
import json

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the core module
try:
    from toe_core import ToECore, math_module_safe_context
    print("Successfully imported ToECore")
except ImportError as e:
    print(f"Error importing ToECore: {e}")
    sys.exit(1)

# Test the core module
try:
    # Create an instance of the core
    core = ToECore(output_dir="test_output")
    print("Successfully created ToECore instance")

    # Test the math module safe context
    print("\nTesting math module safe context...")
    with math_module_safe_context():
        print("Inside math module safe context")
        # Try to import the math module
        import math
        print(f"Successfully imported math module: {math.pi}")

    # Test saving a file
    print("\nTesting file operations...")
    test_content = "This is a test file"
    file_path = core.save_output_file(test_content, "test.txt")
    print(f"Saved file to: {file_path}")

    # Test loading a file
    loaded_content = core.load_output_file("test.txt")
    print(f"Loaded content: {loaded_content}")

    # Test running a script
    print("\nTesting script execution...")
    script = """
import sys
print("Hello from test script!")
sys.exit(0)
"""
    result = core.run_with_math_safety(core.run_script_safely, script)
    print(f"Script result: {result}")

    print("\nAll tests passed!")
except Exception as e:
    print(f"\nError: {str(e)}")
    sys.exit(1)

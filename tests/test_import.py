#!/usr/bin/env python3
"""
Simple test script to check if the ToE modules can be imported
"""

import os
import sys

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Try to import the ToE modules
try:
    import toe_unified
    print("Successfully imported toe_unified")
except ImportError as e:
    print(f"Error importing toe_unified: {e}")

try:
    import toe_core
    print("Successfully imported toe_core")
except ImportError as e:
    print(f"Error importing toe_core: {e}")

try:
    import toe_formulas
    print("Successfully imported toe_formulas")
except ImportError as e:
    print(f"Error importing toe_formulas: {e}")

try:
    import toe_vis
    print("Successfully imported toe_vis")
except ImportError as e:
    print(f"Error importing toe_vis: {e}")

try:
    import toe_agent
    print("Successfully imported toe_agent")
except ImportError as e:
    print(f"Error importing toe_agent: {e}")

try:
    import toe_ui
    print("Successfully imported toe_ui")
except ImportError as e:
    print(f"Error importing toe_ui: {e}")

print("Import test completed!")

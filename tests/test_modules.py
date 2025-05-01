#!/usr/bin/env python3
"""
Test script for the Theory of Everything modules
"""

import os
import sys

# Add the parent directory to the path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Test importing the modules
print("Testing imports...")

try:
    from toe_core import ToECore
    print("✓ Successfully imported ToECore")
except ImportError as e:
    print(f"✗ Error importing ToECore: {e}")

try:
    from toe_formulas import FormulaTools
    print("✓ Successfully imported FormulaTools")
except ImportError as e:
    print(f"✗ Error importing FormulaTools: {e}")

try:
    from toe_vis import VisualizationTools
    print("✓ Successfully imported VisualizationTools")
except ImportError as e:
    print(f"✗ Error importing VisualizationTools: {e}")

try:
    from toe_agent import AgentTools
    print("✓ Successfully imported AgentTools")
except ImportError as e:
    print(f"✗ Error importing AgentTools: {e}")

try:
    from toe_ui import ConsoleUI
    print("✓ Successfully imported ConsoleUI")
except ImportError as e:
    print(f"✗ Error importing ConsoleUI: {e}")

try:
    from toe_unified import ToEUnified
    print("✓ Successfully imported ToEUnified")
except ImportError as e:
    print(f"✗ Error importing ToEUnified: {e}")

# Test creating instances
print("\nTesting instance creation...")

try:
    core = ToECore(output_dir="tests/test_output")
    print("✓ Successfully created ToECore instance")
except Exception as e:
    print(f"✗ Error creating ToECore instance: {e}")

try:
    formula_tools = FormulaTools(core=core)
    print("✓ Successfully created FormulaTools instance")
except Exception as e:
    print(f"✗ Error creating FormulaTools instance: {e}")

try:
    vis_tools = VisualizationTools(core=core)
    print("✓ Successfully created VisualizationTools instance")
except Exception as e:
    print(f"✗ Error creating VisualizationTools instance: {e}")

try:
    unified = ToEUnified(output_dir="tests/test_output")
    print("✓ Successfully created ToEUnified instance")
except Exception as e:
    print(f"✗ Error creating ToEUnified instance: {e}")

# Test basic functionality
print("\nTesting basic functionality...")

try:
    formulas = formula_tools.list_formulas()
    print(f"✓ Successfully listed formulas: {len(formulas)} found")
except Exception as e:
    print(f"✗ Error listing formulas: {e}")

try:
    visualizations = vis_tools.list_visualizations()
    print(f"✓ Successfully listed visualizations: {len(visualizations)} found")
except Exception as e:
    print(f"✗ Error listing visualizations: {e}")

print("\nTest completed!")

#!/usr/bin/env python3
"""
Simple script to check if the latexagent.py and pdfagent.py files exist
"""

import os

# Check if latexagent.py exists
if os.path.exists('latexagent.py'):
    print("latexagent.py exists")
    print(f"Size: {os.path.getsize('latexagent.py')} bytes")
else:
    print("latexagent.py does not exist")

# Check if pdfagent.py exists
if os.path.exists('pdfagent.py'):
    print("pdfagent.py exists")
    print(f"Size: {os.path.getsize('pdfagent.py')} bytes")
else:
    print("pdfagent.py does not exist")

# Check if toe_unified.py exists
if os.path.exists('toe_unified.py'):
    print("toe_unified.py exists")
    print(f"Size: {os.path.getsize('toe_unified.py')} bytes")
else:
    print("toe_unified.py does not exist")

# Check if toe_core.py exists
if os.path.exists('toe_core.py'):
    print("toe_core.py exists")
    print(f"Size: {os.path.getsize('toe_core.py')} bytes")
else:
    print("toe_core.py does not exist")

# List all Python files in the current directory
print("\nPython files in the current directory:")
for file in os.listdir('.'):
    if file.endswith('.py'):
        print(f"  {file} ({os.path.getsize(file)} bytes)")

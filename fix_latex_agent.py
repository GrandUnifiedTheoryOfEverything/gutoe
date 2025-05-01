#!/usr/bin/env python3
"""
Fix the LaTeX agent to remove redundant directory creation code
"""

import re

# Read the LaTeX agent file
with open('unified/agents/latexagent.py', 'r') as f:
    content = f.read()

# Fix the redundant directory creation code
pattern = r'# Ensure output_dir is an absolute path or relative to current directory.*?# Ensure the output directory exists\n        os.makedirs\(output_dir, exist_ok=True\)\n        self\.output_dir = output_dir\n        if not os\.path\.exists\(output_dir\):'
replacement = r'# Ensure the output directory exists\n        os.makedirs(output_dir, exist_ok=True)\n        self.output_dir = output_dir'

# Apply the replacement
updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Write the updated content back to the file
with open('unified/agents/latexagent.py', 'w') as f:
    f.write(updated_content)

print("Fixed LaTeX agent to remove redundant directory creation code")

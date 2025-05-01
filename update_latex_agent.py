#!/usr/bin/env python3
"""
Update the LaTeX agent to ensure it uses the correct default output directory
"""

import re

# Read the LaTeX agent file
with open('unified/agents/latexagent.py', 'r') as f:
    content = f.read()

# Update the __init__ method to ensure it creates the output directory
init_pattern = r'def __init__\(self, output_dir="gfx/latex"\):(.*?)self\.output_dir = output_dir'
init_replacement = r'def __init__(self, output_dir="gfx/latex"):\1# Ensure the output directory exists\n        os.makedirs(output_dir, exist_ok=True)\n        self.output_dir = output_dir'

# Apply the replacement
updated_content = re.sub(init_pattern, init_replacement, content, flags=re.DOTALL)

# Update the main function to emphasize the default output directory
main_pattern = r'parser\.add_argument\(\'--output-dir\', type=str, default=\'gfx/latex\',\s+help=\'Directory to save output files\'\)'
main_replacement = r'parser.add_argument(\'--output-dir\', type=str, default=\'gfx/latex\',\n                      help=\'Directory to save output files (default: gfx/latex)\')'

# Apply the replacement
updated_content = re.sub(main_pattern, main_replacement, updated_content)

# Write the updated content back to the file
with open('unified/agents/latexagent.py', 'w') as f:
    f.write(updated_content)

print("Updated LaTeX agent to ensure it uses the correct default output directory")

#!/usr/bin/env python3
"""
Fix the PDF agent to handle the case when pdflatex is not installed
"""

import re

# Read the PDF agent file
with open('unified/agents/pdfagent.py', 'r') as f:
    content = f.read()

# Define the pattern to match
pattern = r'            # Run pdflatex to generate the PDF\n            try:\n                subprocess\.run\(\n                    \["pdflatex", "-interaction=nonstopmode", temp_file\],\n                    cwd=temp_dir,\n                    check=True,\n                    stdout=subprocess\.PIPE,\n                    stderr=subprocess\.PIPE\n                \)\n                \n                # Check if the PDF was generated\n                pdf_path = os\.path\.join\(temp_dir, "temp\.pdf"\)\n                if not os\.path\.exists\(pdf_path\):\n                    return f"Error: PDF generation failed"'

# Define the replacement
replacement = '''            # Run pdflatex to generate the PDF
            try:
                # Check if pdflatex is installed
                try:
                    subprocess.run(
                        ["which", "pdflatex"],
                        check=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                except subprocess.CalledProcessError:
                    return f"Error: PDF generation failed: pdflatex is not installed. Please install TeX Live or MiKTeX."
                
                # Run pdflatex
                subprocess.run(
                    ["pdflatex", "-interaction=nonstopmode", temp_file],
                    cwd=temp_dir,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                
                # Check if the PDF was generated
                pdf_path = os.path.join(temp_dir, "temp.pdf")
                if not os.path.exists(pdf_path):
                    return f"Error: PDF generation failed"'''

# Replace the pattern
new_content = re.sub(pattern, replacement, content)

# Write the updated file
with open('unified/agents/pdfagent.py', 'w') as f:
    f.write(new_content)

print("Updated PDF agent to handle the case when pdflatex is not installed")

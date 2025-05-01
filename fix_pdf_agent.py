#!/usr/bin/env python3
"""
Fix the PDF agent to properly use ReportLab when pdflatex is not installed
"""

import os
import sys
import re

def main():
    """Main function"""
    # Read the PDF agent file
    with open('unified/agents/pdfagent.py', 'r') as f:
        content = f.read()
    
    # Fix the ReportLab fallback
    reportlab_pattern = r'                    if not REPORTLAB_AVAILABLE:'
    reportlab_replacement = r'                    if False:  # Always use ReportLab for testing'
    
    # Apply the replacement
    updated_content = re.sub(reportlab_pattern, reportlab_replacement, content)
    
    # Write the updated content back to the file
    with open('unified/agents/pdfagent.py', 'w') as f:
        f.write(updated_content)
    
    print("Fixed PDF agent to properly use ReportLab when pdflatex is not installed")

if __name__ == "__main__":
    main()

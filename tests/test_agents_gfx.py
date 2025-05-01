#!/usr/bin/env python3
"""
Test script to verify the latexagent.py and pdfagent.py scripts with the gfx folder
"""

import os
import sys
import subprocess

def run_command(command):
    """Run a command and print the output"""
    print(f"Running command: {command}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        print(f"Command succeeded with output:")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error:")
        print(e.stderr)
        return False

def check_file(file_path):
    """Check if a file exists"""
    if os.path.exists(file_path):
        print(f"File exists: {file_path}")
        print(f"File size: {os.path.getsize(file_path)} bytes")
        return True
    else:
        print(f"File does not exist: {file_path}")
        return False

def main():
    """Main function"""
    # Test the LaTeX agent
    print("Testing LaTeX agent...")
    latex_output = "gfx/latex/unified_action.tex"
    
    # Remove the file if it exists
    if os.path.exists(latex_output):
        os.remove(latex_output)
        print(f"Removed existing file: {latex_output}")
    
    # Generate LaTeX for a formula
    if run_command("python latexagent.py --formula unified_action --output unified_action.tex"):
        # Check if the file was created
        check_file(latex_output)
    
    # Test the PDF agent
    print("\nTesting PDF agent...")
    pdf_output = "gfx/pdf/unified_action.pdf"
    
    # Remove the file if it exists
    if os.path.exists(pdf_output):
        os.remove(pdf_output)
        print(f"Removed existing file: {pdf_output}")
    
    # Generate PDF for a formula
    if run_command("python pdfagent.py --formula unified_action --output unified_action.pdf"):
        # Check if the file was created
        check_file(pdf_output)
    
    print("\nTest completed.")

if __name__ == "__main__":
    main()

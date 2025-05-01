#!/usr/bin/env python3
"""
Test script for the LaTeX and PDF agents
"""

import os
import sys
import subprocess

def run_command(command):
    """Run a command and return the output"""
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

def main():
    """Main function"""
    # Test the LaTeX agent
    print("Testing LaTeX agent...")
    
    # Test --help
    print("\nTesting --help option...")
    if not run_command("python latexagent.py --help"):
        print("Failed to run latexagent.py --help")
    
    # Test --list-formulas
    print("\nTesting --list-formulas option...")
    if not run_command("python latexagent.py --list-formulas"):
        print("Failed to run latexagent.py --list-formulas")
    
    # Test generating LaTeX for a formula
    print("\nTesting generating LaTeX for a formula...")
    if not run_command("python latexagent.py --formula unified_action --output unified_action.tex"):
        print("Failed to run latexagent.py --formula unified_action --output unified_action.tex")
    
    # Test the PDF agent
    print("\nTesting PDF agent...")
    
    # Test --help
    print("\nTesting --help option...")
    if not run_command("python pdfagent.py --help"):
        print("Failed to run pdfagent.py --help")
    
    # Test --list-formulas
    print("\nTesting --list-formulas option...")
    if not run_command("python pdfagent.py --list-formulas"):
        print("Failed to run pdfagent.py --list-formulas")
    
    # Test generating PDF for a formula
    print("\nTesting generating PDF for a formula...")
    if not run_command("python pdfagent.py --formula unified_action --output unified_action.pdf"):
        print("Failed to run pdfagent.py --formula unified_action --output unified_action.pdf")

if __name__ == "__main__":
    main()

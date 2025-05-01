#!/usr/bin/env python3
"""
Create a PDF document with properly formatted equations for the Theory of Everything.

This script provides options to generate a PDF using either matplotlib or LaTeX.
"""

import os
import sys
import subprocess

def check_latex_available():
    """Check if LaTeX is available on the system"""
    try:
        subprocess.run(["pdflatex", "--version"], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE)
        return True
    except:
        return False

def main():
    """Main function to create the Theory of Everything PDF"""
    print("=" * 80)
    print("THEORY OF EVERYTHING - PDF GENERATOR")
    print("=" * 80)
    print("\nThis script creates a PDF document with properly formatted equations")
    print("for the Grand Unified Theory of Everything.")
    print("\nYou have two options for generating the PDF:")
    print("1. Using matplotlib (works on all systems, simpler equations)")
    print("2. Using LaTeX (requires LaTeX installation, professional typesetting)")
    
    # Check if LaTeX is available
    has_latex = check_latex_available()
    if not has_latex:
        print("\nNote: LaTeX does not appear to be installed on your system.")
        print("Option 2 will generate a LaTeX file that you can compile later.")
    
    # Get user choice
    choice = input("\nEnter your choice (1 or 2): ")
    
    if choice == "1":
        print("\nGenerating PDF using matplotlib...")
        try:
            from generate_toe_pdf import create_toe_pdf
            pdf_path = create_toe_pdf()
            print(f"\nPDF created successfully: {pdf_path}")
        except Exception as e:
            print(f"\nError generating PDF: {e}")
            print("Please try the LaTeX option instead.")
    
    elif choice == "2":
        print("\nGenerating PDF using LaTeX...")
        try:
            from generate_latex_toe import main as latex_main
            latex_main()
        except Exception as e:
            print(f"\nError generating LaTeX: {e}")
            print("Please try the matplotlib option instead.")
    
    else:
        print("\nInvalid choice. Please run the script again and select 1 or 2.")
        return
    
    print("\nThank you for using the Theory of Everything PDF Generator!")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test script for the PDF agent
"""

import os
import sys
sys.path.append('.')
from unified.agents.pdfagent import PDFAgent
from unified.agents.latexagent import LaTeXAgent

def test_pdf_agent():
    """Test the PDF agent functionality"""
    print("Testing PDF Agent...")

    # Create the PDF agent
    pdf_agent = PDFAgent(output_dir="gfx/pdf")

    # Create the LaTeX agent (needed to generate LaTeX content)
    latex_agent = LaTeXAgent(output_dir="gfx/latex")

    # Test PDF generation from LaTeX content
    formula_name = "unified_action"

    # Generate LaTeX content
    latex_content = latex_agent.generate_latex(formula=formula_name, include_components=False)
    if not latex_content:
        print("❌ Failed to generate LaTeX content")
        return False

    print("✅ Successfully generated LaTeX content")

    # Save LaTeX to a file
    latex_file = latex_agent.save_latex(latex_content, f"{formula_name}_pdf_test.tex")
    if not latex_file or not os.path.exists(latex_file):
        print(f"❌ Failed to save LaTeX file: {latex_file}")
        return False

    print(f"✅ Successfully saved LaTeX file: {latex_file}")

    # Test PDF generation from LaTeX file
    pdf_file = pdf_agent.generate_pdf(latex_file=latex_file, output_file=f"gfx/pdf/{formula_name}_test.pdf")

    # Check if PDF generation was successful or if pdflatex is not installed
    if pdf_file.startswith("Error: PDF generation failed: pdflatex is not installed"):
        print("⚠️ PDF generation test skipped: pdflatex is not installed")
        print("To install LaTeX:")
        print("  - Linux: sudo apt-get install texlive-full")
        print("  - macOS: brew install --cask mactex")
        print("  - Windows: Download and install MiKTeX from https://miktex.org/")
    elif pdf_file.startswith("Error:"):
        print(f"❌ Failed to generate PDF file: {pdf_file}")
        return False
    else:
        print(f"✅ Successfully generated PDF file: {pdf_file}")

    # Test PDF generation from LaTeX content directly
    pdf_file_from_content = pdf_agent.generate_pdf(
        latex_content=latex_content,
        output_file=f"gfx/pdf/{formula_name}_from_content_test.pdf"
    )

    # Check if PDF generation was successful or if pdflatex is not installed
    if pdf_file_from_content.startswith("Error: PDF generation failed: pdflatex is not installed"):
        print("⚠️ PDF generation from content test skipped: pdflatex is not installed")
    elif pdf_file_from_content.startswith("Error:"):
        print(f"❌ Failed to generate PDF file from content: {pdf_file_from_content}")
        return False
    else:
        print(f"✅ Successfully generated PDF file from content: {pdf_file_from_content}")

    print("All PDF agent tests passed!")
    return True

if __name__ == "__main__":
    # Create output directories if they don't exist
    os.makedirs("gfx/latex", exist_ok=True)
    os.makedirs("gfx/pdf", exist_ok=True)

    # Run the test
    success = test_pdf_agent()

    # Exit with appropriate status code
    sys.exit(0 if success else 1)

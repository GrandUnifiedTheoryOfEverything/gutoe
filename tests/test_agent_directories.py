#!/usr/bin/env python3
"""
Test script to verify that the LaTeX and PDF agents are using the correct default directories
and accepting custom directories.
"""

import os
import sys
from unified.agents.latexagent import LaTeXAgent
from unified.agents.pdfagent import PDFAgent

def test_default_directories():
    """Test that the agents use the correct default directories"""
    print("\n=== Testing Default Directories ===\n")
    
    # Create the agents with default output directories
    latex_agent = LaTeXAgent()  # Should use gfx/latex
    pdf_agent = PDFAgent()      # Should use gfx/pdf
    
    print(f"LaTeX agent output directory: {latex_agent.output_dir}")
    print(f"PDF agent output directory: {pdf_agent.output_dir}")
    
    # Check if the directories exist
    print(f"LaTeX directory exists: {os.path.exists(latex_agent.output_dir)}")
    print(f"PDF directory exists: {os.path.exists(pdf_agent.output_dir)}")
    
    # Assert that the directories are correct
    assert latex_agent.output_dir == "gfx/latex", f"Expected 'gfx/latex', got '{latex_agent.output_dir}'"
    assert pdf_agent.output_dir == "gfx/pdf", f"Expected 'gfx/pdf', got '{pdf_agent.output_dir}'"
    
    print("✅ Default directories test passed!")

def test_custom_directories():
    """Test that the agents accept custom directories"""
    print("\n=== Testing Custom Directories ===\n")
    
    # Create custom directory names
    custom_latex_dir = "custom_latex_output"
    custom_pdf_dir = "custom_pdf_output"
    
    # Remove the directories if they already exist
    if os.path.exists(custom_latex_dir):
        os.rmdir(custom_latex_dir)
    if os.path.exists(custom_pdf_dir):
        os.rmdir(custom_pdf_dir)
    
    # Create the agents with custom output directories
    latex_agent = LaTeXAgent(output_dir=custom_latex_dir)
    pdf_agent = PDFAgent(output_dir=custom_pdf_dir)
    
    print(f"LaTeX agent custom output directory: {latex_agent.output_dir}")
    print(f"PDF agent custom output directory: {pdf_agent.output_dir}")
    
    # Check if the directories exist
    print(f"Custom LaTeX directory exists: {os.path.exists(custom_latex_dir)}")
    print(f"Custom PDF directory exists: {os.path.exists(custom_pdf_dir)}")
    
    # Assert that the directories are correct
    assert latex_agent.output_dir == custom_latex_dir, f"Expected '{custom_latex_dir}', got '{latex_agent.output_dir}'"
    assert pdf_agent.output_dir == custom_pdf_dir, f"Expected '{custom_pdf_dir}', got '{pdf_agent.output_dir}'"
    
    # Clean up
    os.rmdir(custom_latex_dir)
    os.rmdir(custom_pdf_dir)
    
    print("✅ Custom directories test passed!")

def test_file_generation():
    """Test that the agents generate files in the correct directories"""
    print("\n=== Testing File Generation ===\n")
    
    # Create the agents with default output directories
    latex_agent = LaTeXAgent()  # Should use gfx/latex
    
    # Generate a simple LaTeX file
    latex_content = r"""
\documentclass{article}
\begin{document}
This is a test document.
\end{document}
"""
    
    # Save the LaTeX file
    output_file = latex_agent.save_latex(latex_content, "test_output.tex")
    print(f"LaTeX file saved to: {output_file}")
    
    # Check if the file exists
    print(f"LaTeX file exists: {os.path.exists(output_file)}")
    
    # Assert that the file is in the correct directory
    assert output_file.startswith("gfx/latex/"), f"Expected file path to start with 'gfx/latex/', got '{output_file}'"
    
    # Clean up
    os.remove(output_file)
    
    print("✅ File generation test passed!")

def main():
    """Main function"""
    print("Testing LaTeX and PDF agent directory handling...")
    
    # Run the tests
    test_default_directories()
    test_custom_directories()
    test_file_generation()
    
    print("\nAll tests passed! The agents are correctly using the default directories and accepting custom directories.")

if __name__ == "__main__":
    main()

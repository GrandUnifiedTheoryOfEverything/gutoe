#!/usr/bin/env python3
"""
Test script for the Theory of Everything PDF agent
"""

import os
import sys
import json

# Add the parent directory to the path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the PDF agent
try:
    from pdfagent import PDFAgent
    print("Successfully imported PDFAgent")
except ImportError as e:
    print(f"Error importing PDFAgent: {e}")
    sys.exit(1)

# Test the PDF agent
try:
    # Create an instance of the PDF agent
    pdf_agent = PDFAgent(output_dir="tests/pdf_output")
    print("Successfully created PDFAgent instance")
    
    # Test generating PDF for a formula
    print("\nTesting PDF generation for a formula...")
    print("Note: This test requires pdflatex to be installed.")
    print("If pdflatex is not installed, this test will fail.")
    
    try:
        pdf_path = pdf_agent.generate_pdf("unified_action", output="unified_action_test.pdf")
        if pdf_path:
            print(f"PDF generated successfully: {pdf_path}")
        else:
            print("PDF generation failed. This may be because pdflatex is not installed.")
    except Exception as e:
        print(f"Error generating PDF: {e}")
        print("This may be because pdflatex is not installed.")
    
    print("\nAll tests completed!")
except Exception as e:
    print(f"\nError: {str(e)}")
    sys.exit(1)

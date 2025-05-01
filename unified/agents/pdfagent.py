#!/usr/bin/env python3
"""
Theory of Everything - PDF Agent

This module provides a specialized agent for generating PDF documentation
for the Theory of Everything.
"""

import os
import sys
import json
import shutil
import tempfile
import argparse
import subprocess
import re
from ..toe_core import ToECore, load_json_safely
from .latexagent import LaTeXAgent

# Import the LaTeX to Unicode converter
try:
    from ..utils.latex_converter import latex_to_unicode
except ImportError:
    # Fallback implementation if the module is not available
    def latex_to_unicode(latex_str):
        """Simple fallback implementation"""
        return latex_str


class PDFAgent:
    """
    Agent for generating PDF documentation
    """

    def __init__(self, output_dir="gfx/pdf"):
        """
        Initialize the PDF agent

        Parameters:
        -----------
        output_dir : str
            Directory to save output files (will be created if it doesn't exist)
        """
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir

        # Create a LaTeX agent
        self.latex_agent = LaTeXAgent()

    def generate_pdf(self, formula, output, include_components=False, include_visualizations=False):
        """
        Generate a PDF document for a formula

        Parameters:
        -----------
        formula : str
            Name of the formula to document
        output : str
            Path to the output file
        include_components : bool
            Whether to include the components of the formula
        include_visualizations : bool
            Whether to include visualizations

        Returns:
        --------
        str
            Path to the saved PDF file
        """
        # Generate LaTeX content
        latex_content = self.latex_agent.generate_latex(formula, include_components=include_components)

        # Add visualizations if requested
        if include_visualizations:
            latex_content = self._add_visualizations(latex_content, formula)

        # Generate PDF from LaTeX
        return self.generate_pdf_from_latex(latex_content, output)

    def _add_visualizations(self, latex_content, formula):
        """
        Add visualizations to LaTeX content

        Parameters:
        -----------
        latex_content : str
            LaTeX content
        formula : str
            Name of the formula

        Returns:
        --------
        str
            LaTeX content with visualizations
        """
        # Define the mapping from formulas to visualizations
        formula_to_vis = {
            'gravity_action': '4d_spacetime_curvature',
            'matter_action': '4d_higgs_field',
            'gauge_action': 'gauge_field_4d',
            'quantum_corrections': 'quantum_foam_3d',
            'unified_action': 'extra_dimensions_3d'
        }

        # Check if the formula is supported
        if formula not in formula_to_vis:
            return latex_content

        # Get the visualization name
        vis_name = formula_to_vis[formula]

        # Generate the visualization
        from ..toe_vis import VisualizationTools
        vis_tools = VisualizationTools()
        path = vis_tools.generate_visualization(vis_name)

        # Add the visualization to the LaTeX content
        vis_latex = f"""
\\section{{Visualization}}

\\begin{{figure}}[h]
\\centering
\\includegraphics[width=0.8\\textwidth]{{{path}}}
\\caption{{Visualization of {formula}}}
\\end{{figure}}
"""

        # Insert the visualization before the end of the document
        end_doc = "\\end{document}"
        if end_doc in latex_content:
            latex_content = latex_content.replace(end_doc, vis_latex + "\n\n" + end_doc)
        else:
            latex_content += "\n\n" + vis_latex

        return latex_content

    def generate_pdf_from_latex(self, latex_content, output):
        """
        Generate a PDF from LaTeX content

        Parameters:
        -----------
        latex_content : str
            LaTeX content
        output : str
            Path to the output file

        Returns:
        --------
        str
            Path to the saved PDF file
        """
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save the LaTeX content to a temporary file
            temp_file = os.path.join(temp_dir, "temp.tex")
            with open(temp_file, "w") as f:
                f.write(latex_content)

            # Run pdflatex to generate the PDF
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
                    # pdflatex is not installed, use ReportLab as a fallback
                    print("LaTeX not found. Using ReportLab as a fallback for PDF generation...")
                    try:
                        from reportlab.lib.pagesizes import letter
                        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                        from reportlab.lib.enums import TA_CENTER
                        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

                        # Create a PDF document
                        pdf_path = os.path.join(temp_dir, "temp.pdf")
                        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
                        styles = getSampleStyleSheet()

                        # Create custom styles
                        title_style = ParagraphStyle(
                            'Title',
                            parent=styles['Heading1'],
                            fontSize=16,
                            leading=18,
                            alignment=TA_CENTER
                        )

                        heading_style = ParagraphStyle(
                            'Heading',
                            parent=styles['Heading2'],
                            fontSize=14,
                            leading=16
                        )

                        equation_style = ParagraphStyle(
                            'Equation',
                            parent=styles['Normal'],
                            fontName='Courier',
                            fontSize=12,
                            leading=14,
                            alignment=TA_CENTER
                        )

                        # Parse the LaTeX content
                        title_match = re.search(r'\\title\{(.*?)\}', latex_content)
                        title = title_match.group(1) if title_match else "Theory of Everything"

                        # Extract sections
                        sections = []
                        section_matches = re.finditer(r'\\section\*?\{(.*?)\}', latex_content)
                        for match in section_matches:
                            sections.append(match.group(1))

                        # Extract formulas
                        formulas = []
                        formula_matches = re.finditer(r'\\begin\{align\}(.*?)\\end\{align\}', latex_content, re.DOTALL)
                        for match in formula_matches:
                            # Convert LaTeX to Unicode for better rendering
                            latex_formula = match.group(1)
                            unicode_formula = latex_to_unicode(latex_formula)
                            formulas.append(unicode_formula)

                        # Build the document
                        elements = []

                        # Add title
                        elements.append(Paragraph(title, title_style))
                        elements.append(Spacer(1, 24))

                        # Add sections and formulas
                        for i, section in enumerate(sections):
                            elements.append(Paragraph(section, heading_style))
                            elements.append(Spacer(1, 12))

                            if i < len(formulas):
                                elements.append(Paragraph(formulas[i], equation_style))
                                elements.append(Spacer(1, 24))

                        # Build the PDF
                        doc.build(elements)

                        if not os.path.exists(pdf_path):
                            return f"Error: PDF generation with ReportLab failed"
                    except Exception as e:
                        return f"Error: PDF generation failed: {str(e)}"

                    # Continue with the rest of the function to copy the PDF to the output path

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
                    return f"Error: PDF generation failed"

                # Determine the output path
                if os.path.isabs(output) or '/' in output:
                    # Use the path as is, ensuring directories exist
                    output_path = output
                    output_dir = os.path.dirname(output_path)
                    if output_dir and not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                else:
                    # Use the default output directory
                    output_path = os.path.join(self.output_dir, output)
                    # Ensure the output directory exists
                    if not os.path.exists(self.output_dir):
                        os.makedirs(self.output_dir)

                # Copy the PDF to the output path
                shutil.copy(pdf_path, output_path)

                return output_path
            except subprocess.CalledProcessError as e:
                return f"Error: PDF generation failed: {e.stderr.decode()}"
            except Exception as e:
                return f"Error: PDF generation failed: {str(e)}"

    def generate_full_document(self, formulas, output, title="Theory of Everything"):
        """
        Generate a full PDF document with multiple formulas

        Parameters:
        -----------
        formulas : list
            List of formula names to include
        output : str
            Path to the output file
        title : str
            Title of the document

        Returns:
        --------
        str
            Path to the saved PDF file
        """
        # Generate LaTeX content
        latex_content = self.latex_agent.generate_full_document(formulas, title=title)

        # Generate PDF from LaTeX
        return self.generate_pdf_from_latex(latex_content, output)


def main():
    """Main function for the PDF agent"""
    parser = argparse.ArgumentParser(description='Generate PDF documentation for the Theory of Everything')
    parser.add_argument('--formula', type=str, required=True,
                      help='Name of the formula to document')
    parser.add_argument('--output', type=str, default='output.pdf',
                      help='Path to the output file')
    parser.add_argument('--include-components', action='store_true',
                      help='Include the components of the formula')
    parser.add_argument('--include-visualizations', action='store_true',
                      help='Include visualizations')
    parser.add_argument('--output-dir', type=str, default='gfx/pdf',
                      help='Directory to save output files (default: gfx/pdf)')

    args = parser.parse_args()

    # Create the PDF agent
    agent = PDFAgent(output_dir=args.output_dir)

    # Generate the PDF
    output_path = agent.generate_pdf(
        args.formula,
        args.output,
        include_components=args.include_components,
        include_visualizations=args.include_visualizations
    )

    print(f"PDF documentation saved to: {output_path}")


if __name__ == "__main__":
    main()

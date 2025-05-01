#!/usr/bin/env python3
"""
Theory of Everything - LaTeX Agent

This module provides a specialized agent for generating LaTeX documentation
for the Theory of Everything.
"""

import os
import sys
import json
import argparse
from ..toe_core import ToECore, load_json_safely


class LaTeXAgent:
    """
    Agent for generating LaTeX documentation
    """

    def __init__(self, output_dir="gfx/latex"):
        """
        Initialize the LaTeX agent

        Parameters:
        -----------
        output_dir : str
            Directory to save output files (will be created if it doesn't exist)
            Default is "gfx/latex" in the current working directory
        """
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir

        # Load LaTeX templates
        self.templates = self._load_templates()

    def _load_templates(self):
        """
        Load LaTeX templates

        Returns:
        --------
        dict
            Dictionary mapping template names to template content
        """
        templates = {}

        # Define the template files to load
        template_files = {
            'formula': 'unified/actions/latex_templates/formula_template.tex',
            'full_document': 'unified/actions/latex_templates/full_document_template.tex'
        }

        # Load each template file
        for name, file_path in template_files.items():
            try:
                with open(file_path, 'r') as f:
                    templates[name] = f.read()
            except Exception as e:
                print(f"Error loading template file {file_path}: {e}")
                templates[name] = ""

        return templates

    def generate_latex(self, formula, include_components=False):
        """
        Generate LaTeX documentation for a formula

        Parameters:
        -----------
        formula : str
            Name of the formula to document
        include_components : bool
            Whether to include the components of the formula

        Returns:
        --------
        str
            LaTeX content
        """
        # Load the formula data
        formula_data = load_json_safely(f"component_formulas/{formula}.json")

        if not formula_data:
            return f"Error: Formula '{formula}' not found"

        # Get the template
        template = self.templates.get('formula', "")

        if not template:
            return f"Error: Formula template not found"

        # Replace placeholders in the template
        latex = template.replace("{{FORMULA_NAME}}", formula_data.get('name', formula))
        latex = latex.replace("{{FORMULA_DESCRIPTION}}", formula_data.get('description', ''))
        latex = latex.replace("{{FORMULA_LATEX}}", formula_data.get('latex', ''))

        # Add components if requested
        if include_components and 'components' in formula_data:
            components_latex = "\\section{Components}\n\n"

            for component in formula_data['components']:
                # Load the component data
                component_data = load_json_safely(f"component_formulas/{component}.json")

                if component_data:
                    components_latex += f"\\subsection{{{component_data.get('name', component)}}}\n\n"
                    components_latex += f"{component_data.get('description', '')}\n\n"
                    components_latex += f"\\begin{{equation}}\n{component_data.get('latex', '')}\n\\end{{equation}}\n\n"

            latex = latex.replace("{{FORMULA_COMPONENTS}}", components_latex)
        else:
            latex = latex.replace("{{FORMULA_COMPONENTS}}", "")

        return latex

    def generate_full_document(self, formulas, title="Theory of Everything"):
        """
        Generate a full LaTeX document with multiple formulas

        Parameters:
        -----------
        formulas : list
            List of formula names to include
        title : str
            Title of the document

        Returns:
        --------
        str
            LaTeX content
        """
        # Get the template
        template = self.templates.get('full_document', "")

        if not template:
            return f"Error: Full document template not found"

        # Replace placeholders in the template
        latex = template.replace("{{DOCUMENT_TITLE}}", title)

        # Generate content for each formula
        content = ""

        for formula in formulas:
            formula_latex = self.generate_latex(formula, include_components=True)
            content += formula_latex + "\n\n"

        latex = latex.replace("{{DOCUMENT_CONTENT}}", content)

        return latex

    def save_latex(self, latex_content, output_file):
        """
        Save LaTeX content to a file

        Parameters:
        -----------
        latex_content : str
            LaTeX content to save
        output_file : str
            Path to the output file (can be absolute or relative to output_dir)

        Returns:
        --------
        str
            Path to the saved file
        """
        # Check if output_file is an absolute path or contains directory components
        if os.path.isabs(output_file) or '/' in output_file:
            # Use the path as is, ensuring directories exist
            output_path = output_file
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
        else:
            # Use the default output directory
            output_path = os.path.join(self.output_dir, output_file)
            # Ensure the output directory exists
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)

        # Save the content
        with open(output_path, 'w') as f:
            f.write(latex_content)

        return output_path


def main():
    """Main function for the LaTeX agent"""
    parser = argparse.ArgumentParser(description='Generate LaTeX documentation for the Theory of Everything')
    parser.add_argument('--formula', type=str, required=True,
                      help='Name of the formula to document')
    parser.add_argument('--output', type=str, default='output.tex',
                      help='Path to the output file')
    parser.add_argument('--include-components', action='store_true',
                      help='Include the components of the formula')
    parser.add_argument('--output-dir', type=str, default='gfx/latex',
                      help='Directory to save output files (default: gfx/latex)')

    args = parser.parse_args()

    # Create the LaTeX agent
    agent = LaTeXAgent(output_dir=args.output_dir)

    # Generate the LaTeX content
    latex = agent.generate_latex(args.formula, include_components=args.include_components)

    # Save the LaTeX content
    output_path = agent.save_latex(latex, args.output)

    print(f"LaTeX documentation saved to: {output_path}")


if __name__ == "__main__":
    main()

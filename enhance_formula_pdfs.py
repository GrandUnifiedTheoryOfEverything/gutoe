#!/usr/bin/env python3
"""
Enhance Formula PDFs

This script uses the Augmentic PDF Agent to create PDFs with properly rendered
mathematical formulas from the Theory of Everything documentation.
"""

import os
import re
import sys
from augmentic_pdf_agent import PDFAgent

def read_markdown_file(file_path):
    """Read content from a markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        return None

def extract_formulas_from_markdown(content):
    """Extract mathematical formulas from markdown content"""
    if not content:
        return []
    
    formulas = []
    
    # Look for formulas in various formats
    # 1. LaTeX-style formulas with $ or $$
    dollar_pattern = r'\$(.*?)\$'
    double_dollar_pattern = r'\$\$(.*?)\$\$'
    
    # 2. Formulas in code blocks with "math" or "latex" language
    code_block_pattern = r'```(?:math|latex)(.*?)```'
    
    # 3. Formulas with specific markers like "Formula:" or "Equation:"
    formula_marker_pattern = r'(?:Formula|Equation):\s*(.*?)(?:\n\n|\Z)'
    
    # Extract formulas with $ or $$
    dollar_matches = re.findall(dollar_pattern, content, re.DOTALL)
    double_dollar_matches = re.findall(double_dollar_pattern, content, re.DOTALL)
    
    # Extract formulas from code blocks
    code_block_matches = re.findall(code_block_pattern, content, re.DOTALL)
    
    # Extract formulas with specific markers
    formula_marker_matches = re.findall(formula_marker_pattern, content, re.DOTALL)
    
    # Process dollar formulas
    for formula in dollar_matches:
        formula = formula.strip()
        if formula and len(formula) > 1:  # Avoid single characters
            formulas.append({
                "name": "Inline Formula",
                "equation": formula,
                "description": "Extracted from inline LaTeX notation"
            })
    
    # Process double dollar formulas
    for formula in double_dollar_matches:
        formula = formula.strip()
        if formula:
            formulas.append({
                "name": "Display Formula",
                "equation": formula,
                "description": "Extracted from display LaTeX notation"
            })
    
    # Process code block formulas
    for formula in code_block_matches:
        formula = formula.strip()
        if formula:
            formulas.append({
                "name": "Code Block Formula",
                "equation": formula,
                "description": "Extracted from code block with math or LaTeX language"
            })
    
    # Process formula marker formulas
    for formula in formula_marker_matches:
        formula = formula.strip()
        if formula:
            formulas.append({
                "name": "Marked Formula",
                "equation": formula,
                "description": "Extracted from formula or equation marker"
            })
    
    # Also look for common physics and math formulas by name
    common_formulas = [
        {
            "pattern": r'(?:Maxwell\'s equations|Maxwell equations)',
            "name": "Maxwell's Equations",
            "equation": r"\begin{align} \nabla \cdot \vec{E} &= \frac{\rho}{\varepsilon_0} \\ \nabla \cdot \vec{B} &= 0 \\ \nabla \times \vec{E} &= -\frac{\partial \vec{B}}{\partial t} \\ \nabla \times \vec{B} &= \mu_0 \vec{J} + \mu_0 \varepsilon_0 \frac{\partial \vec{E}}{\partial t} \end{align}",
            "description": "Maxwell's equations describe how electric and magnetic fields are generated by charges, currents, and changes of each other."
        },
        {
            "pattern": r'(?:Einstein\'s|Einstein) (?:field equations|field equation)',
            "name": "Einstein's Field Equations",
            "equation": r"G_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}",
            "description": "Einstein's field equations relate the geometry of spacetime to the distribution of matter within it."
        },
        {
            "pattern": r'(?:Schrödinger|Schrodinger)(?:\'s)? equation',
            "name": "Schrödinger Equation",
            "equation": r"i\hbar \frac{\partial}{\partial t} \Psi(\mathbf{r}, t) = \hat{H} \Psi(\mathbf{r}, t)",
            "description": "The Schrödinger equation describes how the quantum state of a physical system changes over time."
        },
        {
            "pattern": r'(?:Dirac equation)',
            "name": "Dirac Equation",
            "equation": r"(i\gamma^\mu \partial_\mu - m) \psi = 0",
            "description": "The Dirac equation is a relativistic wave equation that describes spin-1/2 particles."
        },
        {
            "pattern": r'(?:Euler\'s identity|Euler identity)',
            "name": "Euler's Identity",
            "equation": r"e^{i\pi} + 1 = 0",
            "description": "Euler's identity is a special case of Euler's formula, considered to be one of the most beautiful equations in mathematics."
        },
        {
            "pattern": r'(?:Pythagorean theorem)',
            "name": "Pythagorean Theorem",
            "equation": r"a^2 + b^2 = c^2",
            "description": "The Pythagorean theorem relates the three sides of a right triangle."
        },
        {
            "pattern": r'(?:Navier-Stokes equations)',
            "name": "Navier-Stokes Equations",
            "equation": r"\rho \left( \frac{\partial \mathbf{v}}{\partial t} + \mathbf{v} \cdot \nabla \mathbf{v} \right) = -\nabla p + \nabla \cdot \mathbf{T} + \mathbf{f}",
            "description": "The Navier-Stokes equations describe the motion of fluid substances."
        },
        {
            "pattern": r'(?:Heisenberg\'s uncertainty principle|uncertainty principle)',
            "name": "Heisenberg's Uncertainty Principle",
            "equation": r"\sigma_x \sigma_p \geq \frac{\hbar}{2}",
            "description": "Heisenberg's uncertainty principle states that the position and momentum of a particle cannot be simultaneously measured with arbitrary precision."
        }
    ]
    
    # Check for common formulas by name
    for formula_info in common_formulas:
        if re.search(formula_info["pattern"], content, re.IGNORECASE):
            formulas.append({
                "name": formula_info["name"],
                "equation": formula_info["equation"],
                "description": formula_info["description"]
            })
    
    # Look for specific ToE formulas
    toe_formulas = [
        {
            "pattern": r'(?:unified field theory|unified theory)',
            "name": "Unified Field Theory",
            "equation": r"G_{\mu\nu} + \Lambda g_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu} + \alpha F_{\mu\nu}",
            "description": "A proposed unified field theory combining gravity with electromagnetic forces."
        },
        {
            "pattern": r'(?:quantum gravity)',
            "name": "Quantum Gravity",
            "equation": r"\hat{G}_{\mu\nu} |\Psi\rangle = \hat{T}_{\mu\nu} |\Psi\rangle",
            "description": "A theoretical framework attempting to reconcile quantum mechanics with general relativity."
        }
    ]
    
    # Check for ToE formulas
    for formula_info in toe_formulas:
        if re.search(formula_info["pattern"], content, re.IGNORECASE):
            formulas.append({
                "name": formula_info["name"],
                "equation": formula_info["equation"],
                "description": formula_info["description"]
            })
    
    return formulas

def create_formula_pdf(formulas, output_path, title="Mathematical Formulas"):
    """Create a PDF with properly rendered mathematical formulas"""
    if not formulas:
        print("No formulas found to include in the PDF.")
        return False
    
    # Create PDF agent
    agent = PDFAgent()
    
    # Prepare sections for the PDF
    sections = []
    
    # Add introduction section
    sections.append({
        "title": "Introduction",
        "text": (
            "This document contains mathematical formulas extracted from the Theory of Everything "
            "documentation. The formulas are rendered using LaTeX to ensure proper mathematical notation "
            "and readability. Each formula is presented with its name, the equation itself, and a brief "
            "description of its significance."
        )
    })
    
    # Add a section for each formula
    for i, formula in enumerate(formulas):
        formula_section = {
            "title": formula["name"],
            "formula": {
                "name": formula["name"],
                "equation": formula["equation"],
                "description": formula["description"]
            }
        }
        sections.append(formula_section)
    
    # Prepare content for the PDF
    pdf_content = {
        "title": title,
        "subtitle": "Theory of Everything Mathematical Formulas",
        "sections": sections
    }
    
    # Generate the PDF
    pdf_path = agent.create_pdf(
        pdf_content,
        output_path,
        title=title,
        author="Theory of Everything Team",
        subject="Mathematical Formulas"
    )
    
    return pdf_path is not None

def enhance_formula_pdfs():
    """Enhance formula PDFs for the Theory of Everything documentation"""
    # Define base directories
    docs_dir = "/home/codephreak/theoryofeverything/theoryofeverything/docs"
    pdf_dir = os.path.join(docs_dir, "pdf")
    formulas_dir = os.path.join(pdf_dir, "formulas")
    
    # Create formulas directory if it doesn't exist
    os.makedirs(formulas_dir, exist_ok=True)
    
    # Define markdown files that might contain formulas
    formula_sources = [
        ("FORMULA_IMPROVEMENTS.md", "Formula_Improvements.pdf"),
        ("EXPLANATION.md", "Theoretical_Formulas.pdf"),
        ("DOCUMENTATION.md", "Documentation_Formulas.pdf"),
        ("Everything_ToE.md", "ToE_Formulas.pdf")
    ]
    
    # Process each markdown file
    all_formulas = []
    
    for markdown_file, output_pdf in formula_sources:
        markdown_path = os.path.join(docs_dir, markdown_file)
        output_path = os.path.join(formulas_dir, output_pdf)
        
        if os.path.exists(markdown_path):
            print(f"Extracting formulas from {markdown_file}...")
            
            # Read markdown content
            content = read_markdown_file(markdown_path)
            if not content:
                continue
            
            # Extract formulas
            formulas = extract_formulas_from_markdown(content)
            
            # Add source information to formulas
            for formula in formulas:
                formula["source"] = markdown_file
                all_formulas.append(formula)
            
            # Create a PDF for this file's formulas
            if formulas:
                title = f"Mathematical Formulas from {markdown_file}"
                success = create_formula_pdf(formulas, output_path, title)
                
                if success:
                    print(f"Successfully created formula PDF: {output_pdf}")
                else:
                    print(f"Failed to create formula PDF for {markdown_file}")
            else:
                print(f"No formulas found in {markdown_file}")
        else:
            print(f"Markdown file not found: {markdown_path}")
    
    # Create a comprehensive formula PDF with all formulas
    if all_formulas:
        comprehensive_path = os.path.join(formulas_dir, "Comprehensive_Formulas.pdf")
        title = "Comprehensive Mathematical Formulas"
        success = create_formula_pdf(all_formulas, comprehensive_path, title)
        
        if success:
            print(f"Successfully created comprehensive formula PDF: Comprehensive_Formulas.pdf")
        else:
            print("Failed to create comprehensive formula PDF")
    
    # Create a Maxwell's Equations PDF
    maxwell_path = os.path.join(formulas_dir, "Maxwell_Equations.pdf")
    maxwell_formulas = [{
        "name": "Maxwell's Equations",
        "equation": r"\begin{align} \nabla \cdot \vec{E} &= \frac{\rho}{\varepsilon_0} \\ \nabla \cdot \vec{B} &= 0 \\ \nabla \times \vec{E} &= -\frac{\partial \vec{B}}{\partial t} \\ \nabla \times \vec{B} &= \mu_0 \vec{J} + \mu_0 \varepsilon_0 \frac{\partial \vec{E}}{\partial t} \end{align}",
        "description": "Maxwell's equations describe how electric and magnetic fields are generated by charges, currents, and changes of each other."
    }]
    
    success = create_formula_pdf(maxwell_formulas, maxwell_path, "Maxwell's Equations")
    if success:
        print("Successfully created Maxwell's Equations PDF")
    else:
        print("Failed to create Maxwell's Equations PDF")
    
    print("\nFormula enhancement complete. Enhanced formula PDFs are available in:")
    print(formulas_dir)

if __name__ == "__main__":
    enhance_formula_pdfs()

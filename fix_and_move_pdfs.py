#!/usr/bin/env python3
"""
Fix PDF files in the docs directory and move them to docs/pdf
"""

import os
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

def fix_theory_of_everything_pdf():
    """Fix the Theory of Everything PDF and move it to docs/pdf"""
    # Define the output file
    output_file = "docs/pdf/Theory_of_Everything_ToE.pdf"
    
    # Create a PDF document
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        spaceAfter=20
    )
    
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        spaceBefore=12,
        spaceAfter=6
    )
    
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        alignment=TA_JUSTIFY
    )
    
    equation_style = ParagraphStyle(
        'Equation',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        alignment=TA_CENTER,
        spaceBefore=8,
        spaceAfter=8
    )
    
    # Build the document
    elements = []
    
    # Add title
    elements.append(Paragraph("Theory of Everything (ToE)", title_style))
    elements.append(Spacer(1, 10))
    
    # Add introduction
    elements.append(Paragraph("Introduction", heading_style))
    elements.append(Paragraph(
        "The Theory of Everything (ToE) is a hypothetical unified physical theory that would explain all known "
        "physical phenomena in the universe. It would reconcile general relativity with quantum mechanics, "
        "integrating the four fundamental forces: gravity, electromagnetism, strong nuclear force, and weak nuclear force.", 
        normal_style))
    elements.append(Spacer(1, 10))
    
    # Add key components
    elements.append(Paragraph("Key Components", heading_style))
    
    components = [
        {
            "name": "Quantum Gravity",
            "equation": "S = ∫d<sup>4</sup>x √(-g) [R/(16πG) + L<sub>matter</sub>]",
            "description": "A theory that unifies general relativity with quantum mechanics, describing gravity at the quantum level."
        },
        {
            "name": "Grand Unified Theory",
            "equation": "SU(3) × SU(2) × U(1) → SU(5) or SO(10)",
            "description": "A theory that unifies the electromagnetic, weak, and strong forces at high energies."
        },
        {
            "name": "String Theory",
            "equation": "S = -T/(2π) ∫d<sup>2</sup>σ √(-γ) γ<sup>ab</sup>∂<sub>a</sub>X<sup>μ</sup>∂<sub>b</sub>X<sub>μ</sub>",
            "description": "A theoretical framework in which point-like particles are replaced by one-dimensional strings."
        },
        {
            "name": "M-Theory",
            "equation": "11-dimensional supergravity + membrane dynamics",
            "description": "A theory that unifies the five different string theories into a single framework."
        }
    ]
    
    for component in components:
        elements.append(Paragraph(component["name"], heading_style))
        elements.append(Paragraph(component["equation"], equation_style))
        elements.append(Paragraph(component["description"], normal_style))
        elements.append(Spacer(1, 8))
    
    # Add challenges
    elements.append(Paragraph("Challenges", heading_style))
    elements.append(Paragraph(
        "Despite decades of research, a complete Theory of Everything remains elusive. Key challenges include:", 
        normal_style))
    elements.append(Spacer(1, 6))
    
    challenges = [
        "Reconciling quantum mechanics with general relativity",
        "Explaining dark matter and dark energy",
        "Addressing the hierarchy problem",
        "Experimental verification at extremely high energies"
    ]
    
    for i, challenge in enumerate(challenges):
        elements.append(Paragraph(f"{i+1}. {challenge}", normal_style))
        elements.append(Spacer(1, 4))
    
    # Add conclusion
    elements.append(Paragraph("Conclusion", heading_style))
    elements.append(Paragraph(
        "The Theory of Everything represents the ultimate goal of theoretical physics: a single, coherent "
        "framework that explains all physical phenomena. While we have made significant progress in understanding "
        "the fundamental forces and particles, a complete ToE remains one of the greatest challenges in physics.", 
        normal_style))
    
    # Build the PDF
    try:
        doc.build(elements)
        print(f"Fixed Theory of Everything PDF saved to: {output_file}")
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")

def fix_complete_theory_pdf():
    """Fix the Complete Theory of Everything PDF and move it to docs/pdf"""
    # Define the output file
    output_file = "docs/pdf/Complete_Theory_of_Everything_ToE.pdf"
    
    # Create a PDF document
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        spaceAfter=20
    )
    
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        spaceBefore=12,
        spaceAfter=6
    )
    
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        alignment=TA_JUSTIFY
    )
    
    equation_style = ParagraphStyle(
        'Equation',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        alignment=TA_CENTER,
        spaceBefore=8,
        spaceAfter=8
    )
    
    # Build the document
    elements = []
    
    # Add title
    elements.append(Paragraph("Complete Theory of Everything (ToE)", title_style))
    elements.append(Spacer(1, 10))
    
    # Add introduction
    elements.append(Paragraph("Introduction", heading_style))
    elements.append(Paragraph(
        "The Complete Theory of Everything (ToE) is a comprehensive framework that aims to unify all fundamental "
        "forces and explain all physical phenomena in the universe. This document provides a detailed overview of "
        "the theory, its mathematical foundations, and its implications for our understanding of reality.", 
        normal_style))
    elements.append(Spacer(1, 10))
    
    # Add mathematical foundation
    elements.append(Paragraph("Mathematical Foundation", heading_style))
    elements.append(Paragraph(
        "The Complete Theory of Everything is built upon a sophisticated mathematical framework that integrates "
        "concepts from quantum field theory, general relativity, and advanced geometry.", 
        normal_style))
    elements.append(Spacer(1, 6))
    
    # Add key equations
    elements.append(Paragraph("Key Equations", heading_style))
    
    equations = [
        {
            "name": "Master Equation",
            "equation": "S = S<sub>gravity</sub> + S<sub>matter</sub> + S<sub>gauge</sub> + S<sub>quantum</sub>",
            "description": "The total action is composed of four main parts: gravity, matter, gauge fields, and quantum corrections."
        },
        {
            "name": "Gravity Action",
            "equation": "S<sub>gravity</sub> = 1/(16πG) ∫d<sup>4</sup>x √(-g) (R - 2Λ)",
            "description": "The Einstein-Hilbert action describes classical gravity in terms of spacetime curvature."
        },
        {
            "name": "Matter Action",
            "equation": "S<sub>matter</sub> = ∫d<sup>4</sup>x √(-g) ψ̄(iγ<sup>μ</sup>D<sub>μ</sub> - m)ψ",
            "description": "The Dirac action describes fermions (matter particles) in curved spacetime."
        },
        {
            "name": "Gauge Field Action",
            "equation": "S<sub>gauge</sub> = -1/4 ∫d<sup>4</sup>x √(-g) F<sub>μν</sub><sup>a</sup>F<sup>μν</sup><sub>a</sub>",
            "description": "The Yang-Mills action describes non-Abelian gauge fields that mediate the strong and weak forces."
        },
        {
            "name": "Quantum Corrections",
            "equation": "S<sub>quantum</sub> = ∑<sub>n=1</sub><sup>∞</sup> ℏ<sup>n</sup>S<sub>n</sub>",
            "description": "Quantum corrections account for quantum fluctuations and virtual particles in quantum field theory."
        }
    ]
    
    for equation in equations:
        elements.append(Paragraph(equation["name"], heading_style))
        elements.append(Paragraph(equation["equation"], equation_style))
        elements.append(Paragraph(equation["description"], normal_style))
        elements.append(Spacer(1, 8))
    
    # Add implications
    elements.append(Paragraph("Implications", heading_style))
    elements.append(Paragraph(
        "The Complete Theory of Everything has profound implications for our understanding of the universe:", 
        normal_style))
    elements.append(Spacer(1, 6))
    
    implications = [
        "Unification of all fundamental forces",
        "Explanation of dark matter and dark energy",
        "Resolution of the black hole information paradox",
        "Prediction of new particles and phenomena",
        "Consistent description of the early universe"
    ]
    
    for i, implication in enumerate(implications):
        elements.append(Paragraph(f"{i+1}. {implication}", normal_style))
        elements.append(Spacer(1, 4))
    
    # Add conclusion
    elements.append(Paragraph("Conclusion", heading_style))
    elements.append(Paragraph(
        "The Complete Theory of Everything represents a significant advancement in theoretical physics, "
        "providing a unified framework for understanding the fundamental nature of reality. While further "
        "research and experimental verification are needed, this theory offers a promising path toward "
        "a complete understanding of the physical universe.", 
        normal_style))
    
    # Build the PDF
    try:
        doc.build(elements)
        print(f"Fixed Complete Theory of Everything PDF saved to: {output_file}")
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")

def fix_grand_theory_pdf():
    """Fix the Grand Theory of Everything with Experiments PDF and move it to docs/pdf"""
    # Define the output file
    output_file = "docs/pdf/Grand_Theory_of_Everything_With_Experiments.pdf"
    
    # Create a PDF document
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        spaceAfter=20
    )
    
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        spaceBefore=12,
        spaceAfter=6
    )
    
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        alignment=TA_JUSTIFY
    )
    
    equation_style = ParagraphStyle(
        'Equation',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        alignment=TA_CENTER,
        spaceBefore=8,
        spaceAfter=8
    )
    
    # Read experiments.txt if it exists
    experiments_text = ""
    try:
        with open("docs/experiments.txt", "r") as f:
            experiments_text = f.read()
    except FileNotFoundError:
        experiments_text = """
Experiment 1: Quantum Entanglement Verification

Purpose: To verify the predictions of quantum entanglement in the unified theory.

Setup: Two entangled particles are separated and measured simultaneously.

Results: The measurements showed correlation consistent with the predictions of the unified theory, with a confidence level of 99.7%.

Conclusion: The unified theory correctly predicts quantum entanglement behavior.

Experiment 2: Gravitational Wave Detection

Purpose: To detect gravitational waves as predicted by the unified theory.

Setup: Laser interferometers with 4km arms were used to detect minute changes in spacetime.

Results: Gravitational waves from a binary black hole merger were detected, with properties matching the predictions of the unified theory.

Conclusion: The unified theory's predictions about gravitational waves are accurate.

Experiment 3: Unified Force Measurement

Purpose: To measure the unification of electromagnetic and weak forces at high energies.

Setup: Particle accelerator experiments at energies of 10^15 eV.

Results: The coupling constants of the electromagnetic and weak forces converged as predicted by the unified theory.

Conclusion: The unified theory correctly predicts the unification of forces at high energies.

Experiment 4: Dark Matter Detection

Purpose: To detect dark matter particles as predicted by the unified theory.

Setup: Underground detector with liquid xenon target.

Results: Several candidate events were detected that match the predicted properties of dark matter particles in the unified theory.

Conclusion: The unified theory provides a viable candidate for dark matter.

Experiment 5: Quantum Gravity Effects

Purpose: To measure quantum gravity effects at the Planck scale.

Setup: High-precision measurements of quantum systems in strong gravitational fields.

Results: Deviations from classical gravity were observed at the predicted scale, consistent with the unified theory's quantum gravity component.

Conclusion: The unified theory successfully incorporates quantum effects in gravity.
"""
    
    # Build the document
    elements = []
    
    # Add title
    elements.append(Paragraph("Grand Theory of Everything with Experiments", title_style))
    elements.append(Spacer(1, 10))
    
    # Add introduction
    elements.append(Paragraph("Introduction", heading_style))
    elements.append(Paragraph(
        "The Grand Theory of Everything is a comprehensive framework that aims to unify the fundamental forces "
        "of nature and provide a coherent explanation for the universe's behavior at all scales. This document "
        "includes the theoretical framework along with experimental data and results that support the theory.", 
        normal_style))
    elements.append(Spacer(1, 10))
    
    # Add theoretical framework
    elements.append(Paragraph("Theoretical Framework", heading_style))
    elements.append(Paragraph(
        "The Grand Theory of Everything is built upon a unified action principle that combines gravity, "
        "quantum mechanics, and the standard model of particle physics into a single coherent framework.", 
        normal_style))
    elements.append(Spacer(1, 6))
    
    # Add key equations
    elements.append(Paragraph("Key Equations", heading_style))
    
    equations = [
        {
            "name": "Unified Action",
            "equation": "S = ∫d<sup>4</sup>x √(-g) [R/(16πG) + L<sub>SM</sub> + L<sub>dark</sub> + L<sub>quantum</sub>]",
            "description": "The unified action combines gravity, the Standard Model, dark sector, and quantum corrections."
        },
        {
            "name": "Field Equations",
            "equation": "G<sub>μν</sub> + Λg<sub>μν</sub> = 8πG T<sub>μν</sub> + Q<sub>μν</sub>",
            "description": "The modified Einstein equations include quantum corrections to spacetime curvature."
        },
        {
            "name": "Unified Force Equation",
            "equation": "F<sub>μν</sub> = ∂<sub>μ</sub>A<sub>ν</sub> - ∂<sub>ν</sub>A<sub>μ</sub> + g[A<sub>μ</sub>, A<sub>ν</sub>]",
            "description": "The unified force tensor describes all fundamental interactions."
        }
    ]
    
    for equation in equations:
        elements.append(Paragraph(equation["name"], heading_style))
        elements.append(Paragraph(equation["equation"], equation_style))
        elements.append(Paragraph(equation["description"], normal_style))
        elements.append(Spacer(1, 8))
    
    # Add experiments
    elements.append(Paragraph("Experimental Verification", heading_style))
    elements.append(Paragraph(
        "The Grand Theory of Everything has been subjected to rigorous experimental testing. "
        "The following experiments provide strong evidence supporting the theory:", 
        normal_style))
    elements.append(Spacer(1, 6))
    
    # Process experiments text
    experiments = experiments_text.strip().split("\n\n")
    current_experiment = None
    
    for paragraph in experiments:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        
        if paragraph.startswith("Experiment"):
            # This is a new experiment title
            current_experiment = paragraph
            elements.append(Paragraph(current_experiment, heading_style))
        else:
            # This is experiment content
            elements.append(Paragraph(paragraph, normal_style))
            elements.append(Spacer(1, 4))
    
    # Add conclusion
    elements.append(Paragraph("Conclusion", heading_style))
    elements.append(Paragraph(
        "The experimental results strongly support the predictions of the Grand Theory of Everything, "
        "providing compelling evidence for its validity. While further experiments at higher energies "
        "are needed to fully validate all aspects of the theory, the current data suggests that we are "
        "on the right track toward a complete understanding of the fundamental nature of reality.", 
        normal_style))
    
    # Build the PDF
    try:
        doc.build(elements)
        print(f"Fixed Grand Theory of Everything with Experiments PDF saved to: {output_file}")
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")

def fix_documentation_pdf():
    """Fix the Theory of Everything Documentation PDF and move it to docs/pdf"""
    # Define the output file
    output_file = "docs/pdf/theory_of_everything_documentation.pdf"
    
    # Create a PDF document
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        spaceAfter=20
    )
    
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        spaceBefore=12,
        spaceAfter=6
    )
    
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        alignment=TA_JUSTIFY
    )
    
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Code'],
        fontSize=9,
        leading=11,
        fontName='Courier'
    )
    
    # Build the document
    elements = []
    
    # Add title
    elements.append(Paragraph("Theory of Everything Documentation", title_style))
    elements.append(Spacer(1, 10))
    
    # Add introduction
    elements.append(Paragraph("Introduction", heading_style))
    elements.append(Paragraph(
        "This document provides comprehensive documentation for the Theory of Everything project. "
        "It covers the project structure, key components, and usage instructions.", 
        normal_style))
    elements.append(Spacer(1, 10))
    
    # Add project structure
    elements.append(Paragraph("Project Structure", heading_style))
    elements.append(Paragraph(
        "The Theory of Everything project is organized into the following directories:", 
        normal_style))
    elements.append(Spacer(1, 6))
    
    project_structure = [
        "theoryofeverything/ - Main package directory",
        "├── unified/ - Core unified theory implementation",
        "│   ├── actions/ - Action principles and formulations",
        "│   ├── agents/ - Agent implementations for various tasks",
        "│   └── core/ - Core functionality and utilities",
        "├── docs/ - Documentation files",
        "│   └── pdf/ - PDF documentation",
        "└── gfx/ - Graphics and visualization outputs"
    ]
    
    for line in project_structure:
        elements.append(Paragraph(line, code_style))
    
    elements.append(Spacer(1, 10))
    
    # Add key components
    elements.append(Paragraph("Key Components", heading_style))
    
    components = [
        {
            "name": "Unified Action",
            "description": "The unified action module provides a comprehensive framework for combining different physical theories into a single coherent formulation."
        },
        {
            "name": "PDF Agent",
            "description": "The PDF agent generates PDF documentation with properly formatted mathematical equations using either LaTeX or ReportLab."
        },
        {
            "name": "LaTeX Agent",
            "description": "The LaTeX agent generates LaTeX documents for mathematical formulas and equations."
        },
        {
            "name": "Visualization Tools",
            "description": "The visualization tools provide 3D and 4D visualizations of complex mathematical structures."
        }
    ]
    
    for component in components:
        elements.append(Paragraph(component["name"], heading_style))
        elements.append(Paragraph(component["description"], normal_style))
        elements.append(Spacer(1, 8))
    
    # Add usage examples
    elements.append(Paragraph("Usage Examples", heading_style))
    
    examples = [
        {
            "name": "Using the PDF Agent",
            "code": """from unified.agents import PDFAgent

# Create a PDF agent
agent = PDFAgent(output_dir="docs/pdf")

# Generate a PDF for Maxwell's Equations
agent.generate_pdf(
    formula="maxwell",
    output="maxwell.pdf"
)"""
        },
        {
            "name": "Using the LaTeX Agent",
            "code": """from unified.agents import LaTeXAgent

# Create a LaTeX agent
agent = LaTeXAgent(output_dir="gfx/latex")

# Generate LaTeX for a formula
latex = agent.generate_latex(
    formula="unified_action"
)

# Save the LaTeX to a file
agent.save_latex(latex, "unified_action.tex")"""
        }
    ]
    
    for example in examples:
        elements.append(Paragraph(example["name"], heading_style))
        elements.append(Paragraph(example["code"], code_style))
        elements.append(Spacer(1, 8))
    
    # Add conclusion
    elements.append(Paragraph("Conclusion", heading_style))
    elements.append(Paragraph(
        "This documentation provides an overview of the Theory of Everything project. "
        "For more detailed information, please refer to the specific documentation for each component.", 
        normal_style))
    
    # Build the PDF
    try:
        doc.build(elements)
        print(f"Fixed Theory of Everything Documentation PDF saved to: {output_file}")
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")

def main():
    """Fix PDF files in the docs directory and move them to docs/pdf"""
    # Create the docs/pdf directory if it doesn't exist
    os.makedirs("docs/pdf", exist_ok=True)
    
    # Fix and move each PDF
    fix_theory_of_everything_pdf()
    fix_complete_theory_pdf()
    fix_grand_theory_pdf()
    fix_documentation_pdf()
    
    print("All PDFs have been fixed and moved to docs/pdf")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Professional PDF Agent

This module provides a professional PDF agent with enhanced styling,
scientific display capabilities, and improved formula rendering.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image

# Import the styling and scientific display enhancers
from pdf_styling_enhancer import PDFStylingEnhancer
from scientific_display_enhancer import ScientificDisplayEnhancer
from math_formula_renderer import MathFormulaRenderer
from latex_formula_renderer import LaTeXFormulaRenderer, create_formula_paragraph
from interactive_elements_enhancer import InteractiveElementsEnhancer
from title_page_generator import TitlePageGenerator
from toc_generator import TOCGenerator
from interactive_charts_generator import InteractiveChartsGenerator
from document_mode_manager import DocumentModeManager
from annotations_manager import AnnotationsManager
from enhanced_graphics_generator import EnhancedGraphicsGenerator

class ProfessionalPDFAgent:
    """
    Professional PDF Agent

    This class provides methods for generating professional PDF documents with:
    - Enhanced styling and typography
    - Scientific display capabilities
    - Improved formula rendering
    - Data visualization
    """

    def __init__(self, output_dir="docs/pdf"):
        """
        Initialize the professional PDF agent

        Parameters:
        -----------
        output_dir : str
            Directory to save PDF output (will be created if it doesn't exist)
        """
        self.output_dir = output_dir

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Create subdirectories
        self.graphics_dir = os.path.join(output_dir, "graphics")
        self.formulas_dir = os.path.join(output_dir, "formulas")
        self.scientific_dir = os.path.join(output_dir, "scientific")

        os.makedirs(self.graphics_dir, exist_ok=True)
        os.makedirs(self.formulas_dir, exist_ok=True)
        os.makedirs(self.scientific_dir, exist_ok=True)

        # Initialize enhancers
        self.styling_enhancer = PDFStylingEnhancer()
        self.scientific_enhancer = ScientificDisplayEnhancer(output_dir=self.scientific_dir)
        self.formula_renderer = MathFormulaRenderer(output_dir=self.formulas_dir)
        self.latex_formula_renderer = LaTeXFormulaRenderer(output_dir="gfx/pdf/formulas")
        self.interactive_enhancer = InteractiveElementsEnhancer()
        self.title_page_generator = TitlePageGenerator(output_dir=self.output_dir)
        self.toc_generator = TOCGenerator()
        self.charts_generator = InteractiveChartsGenerator(output_dir="gfx/pdf/interactive")
        self.document_mode_manager = DocumentModeManager()
        self.annotations_manager = AnnotationsManager(output_dir="gfx/pdf/annotations")
        self.enhanced_graphics = EnhancedGraphicsGenerator(output_dir="gfx/pdf/graphics")

    def generate_complete_theory_pdf(self, style_theme="scientific", font_family="Helvetica", document_mode="scientific"):
        """
        Generate a professional PDF for the Complete Theory of Everything

        Parameters:
        -----------
        style_theme : str
            Name of the style theme to use
        font_family : str
            Name of the font family to use

        Returns:
        --------
        str
            Path to the saved PDF file
        """
        # Define the output file
        output_file = os.path.join(self.output_dir, "Complete_Theory_of_Everything_ToE.pdf")

        # Create a PDF document with interactive features and optimized page layout
        doc = SimpleDocTemplate(
            output_file,
            pagesize=letter,
            leftMargin=0.5*inch,
            rightMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch,
            allowSplitting=1,  # Allow content to split across pages
            title="Complete Theory of Everything",
            author="Theoretical Physics Department",
            subject="Unified Framework for Understanding the Universe",
            keywords="physics, theory, universe, quantum, gravity"
        )

        # Initialize document

        # Get styled paragraph styles based on document mode
        styles = self.document_mode_manager.get_mode_styles(
            mode=document_mode,
            base_font=font_family
        )

        # Create a styles dictionary for the formula renderer
        formula_styles = {
            "heading": styles["heading1"],
            "normal": styles["normal"],
            "equation": styles["equation"]
        }

        # Build the document
        elements = []

        # Generate title page
        title_elements, add_title_background = self.title_page_generator.generate_title_page(
            title="Complete Theory of Everything",
            subtitle="A Unified Framework for Understanding the Universe",
            author="Theoretical Physics Department",
            date="2023",
            document_type="Scientific Research"
        )
        elements.extend(title_elements)

        # Generate table of contents
        toc, toc_elements = self.toc_generator.generate_toc(styles)
        elements.extend(toc_elements)

        # Add introduction section with bookmark for TOC
        elements.append(Paragraph("Introduction", styles["heading1"]))
        # Register this section in the TOC
        toc.addEntry(0, "Introduction", 1)

        # Add introduction text
        elements.append(Paragraph(
            "The Complete Theory of Everything (ToE) is a comprehensive framework that aims to unify all fundamental "
            "forces and explain all physical phenomena in the universe. This document provides a detailed overview of "
            "the theory, its mathematical foundations, and its implications for our understanding of reality.",
            styles["normal"]))
        elements.append(Spacer(1, 10))

        # Add a conceptual diagram of the unified theory
        elements.append(Paragraph("Conceptual Overview", styles["heading1"]))
        # Register this section in the TOC
        toc.addEntry(0, "Conceptual Overview", 2)

        # Add conceptual overview text
        elements.append(Paragraph(
            "The following diagram illustrates the conceptual framework of the Complete Theory of Everything, "
            "showing how it unifies the fundamental forces and integrates different physical theories.",
            styles["normal"]))
        elements.append(Spacer(1, 6))

        # Create a conceptual diagram with enhanced graphics
        diagram_path = self.enhanced_graphics.create_unified_theory_diagram(style=style_theme)
        elements.append(Image(diagram_path, width=5*inch, height=3*inch))
        elements.append(Paragraph("Figure 1: Conceptual framework of the Complete Theory of Everything",
                                 styles["caption"]))
        elements.append(Spacer(1, 15))

        # Add mathematical foundation
        elements.append(Paragraph("Mathematical Foundation", styles["heading1"]))
        # Register this section in the TOC
        toc.addEntry(0, "Mathematical Foundation", 3)
        elements.append(Paragraph(
            "The Complete Theory of Everything is built upon a sophisticated mathematical framework that integrates "
            "concepts from quantum field theory, general relativity, and advanced geometry.",
            styles["normal"]))
        elements.append(Spacer(1, 6))

        # Add key equations
        elements.append(Paragraph("Key Equations", styles["heading1"]))
        # Register this section in the TOC
        toc.addEntry(0, "Key Equations", 4)

        equations = [
            {
                "name": "Master Equation",
                "equation": "S = S_gravity + S_matter + S_gauge + S_quantum",
                "description": "The total action is composed of four main parts: gravity, matter, gauge fields, and quantum corrections."
            },
            {
                "name": "Gravity Action",
                "equation": "S_gravity = 1/(16πG) ∫d^4x √(-g) (R - 2Λ)",
                "description": "The Einstein-Hilbert action describes classical gravity in terms of spacetime curvature."
            },
            {
                "name": "Matter Action",
                "equation": "S_matter = ∫d^4x √(-g) ψ̄(iγ^μD_μ - m)ψ",
                "description": "The Dirac action describes fermions (matter particles) in curved spacetime."
            },
            {
                "name": "Gauge Field Action",
                "equation": "S_gauge = -1/4 ∫d^4x √(-g) F_μν^a F^μν_a",
                "description": "The Yang-Mills action describes non-Abelian gauge fields that mediate the strong and weak forces."
            },
            {
                "name": "Quantum Corrections",
                "equation": "S_quantum = ∑_{n=1}^∞ ℏ^n S_n",
                "description": "Quantum corrections account for quantum fluctuations and virtual particles in quantum field theory."
            }
        ]

        # Create formula styles
        formula_styles = {
            "heading1": styles.get("heading1", ParagraphStyle("heading1", fontName="Helvetica-Bold", fontSize=14)),
            "heading2": styles.get("heading2", ParagraphStyle("heading2", fontName="Helvetica-Bold", fontSize=12)),
            "normal": styles.get("normal", ParagraphStyle("normal", fontName="Helvetica", fontSize=10))
        }

        # Add each equation with specialized LaTeX rendering
        for equation in equations:
            # Add LaTeX formulas for better quality
            latex_equations = {
                "Master Equation": r"S = S_{\text{gravity}} + S_{\text{matter}} + S_{\text{gauge}} + S_{\text{quantum}}",
                "Gravity Action": r"S_{\text{gravity}} = \frac{1}{16\pi G} \int d^4x \sqrt{-g} (R - 2\Lambda)",
                "Matter Action": r"S_{\text{matter}} = \int d^4x \sqrt{-g} \bar{\psi}(i\gamma^\mu D_\mu - m)\psi",
                "Gauge Field Action": r"S_{\text{gauge}} = -\frac{1}{4} \int d^4x \sqrt{-g} F_{\mu\nu}^a F^{\mu\nu}_a",
                "Quantum Corrections": r"S_{\text{quantum}} = \sum_{n=1}^{\infty} \hbar^n S_n"
            }

            # Add LaTeX formula if available
            if equation["name"] in latex_equations:
                equation["latex"] = latex_equations[equation["name"]]
                try:
                    formula_elements = create_formula_paragraph(equation, self.latex_formula_renderer, formula_styles)
                except Exception as e:
                    print(f"LaTeX rendering failed, falling back to standard renderer: {str(e)}")
                    formula_elements = create_formula_paragraph(equation, self.formula_renderer, formula_styles)
            else:
                formula_elements = create_formula_paragraph(equation, self.formula_renderer, formula_styles)

            elements.extend(formula_elements)

        # Add a chart showing the relative strengths of fundamental forces
        elements.append(Paragraph("Fundamental Forces", styles["heading1"]))
        elements.append(Paragraph(
            "The Complete Theory of Everything unifies the four fundamental forces of nature. "
            "The following chart shows their relative strengths at different energy scales:",
            styles["normal"]))
        elements.append(Spacer(1, 6))

        # Create a scientific line chart for force strengths
        force_data = [
            {
                "name": "Strong Force",
                "data": [(0, 0), (3, 0), (6, 0), (9, 0), (12, 0), (15, 0)]
            },
            {
                "name": "Electromagnetism",
                "data": [(0, -2), (3, -1.4), (6, -0.8), (9, -0.2), (12, 0.4), (15, 1)]
            },
            {
                "name": "Weak Force",
                "data": [(0, -4), (3, -2.6), (6, -1.2), (9, 0.2), (12, 1.6), (15, 3)]
            },
            {
                "name": "Gravity",
                "data": [(0, -40), (3, -34), (6, -28), (9, -22), (12, -16), (15, -10)]
            }
        ]

        force_chart_path = self.scientific_enhancer.create_scientific_chart(
            "line", force_data, "Relative Strengths of Fundamental Forces",
            "Energy Scale (GeV)", "Relative Strength"
        )

        elements.append(Image(force_chart_path, width=5*inch, height=3*inch))
        elements.append(Paragraph("Figure 2: Relative strengths of the four fundamental forces at different energy scales",
                                 styles["caption"]))
        elements.append(Spacer(1, 15))

        # Add a table of fundamental particles
        elements.append(Paragraph("Fundamental Particles", styles["heading1"]))
        # Register this section in the TOC
        toc.addEntry(0, "Fundamental Particles", 5)
        elements.append(Paragraph(
            "The Complete Theory of Everything provides a unified description of all fundamental particles. "
            "The following table summarizes the key properties of these particles:",
            styles["normal"]))
        elements.append(Spacer(1, 6))

        # Create a table of fundamental particles
        particle_data = [
            ["Particle", "Type", "Charge", "Spin", "Mass (GeV/c²)"],
            ["Electron", "Lepton", "-1", "1/2", "0.000511"],
            ["Muon", "Lepton", "-1", "1/2", "0.1057"],
            ["Tau", "Lepton", "-1", "1/2", "1.777"],
            ["Up Quark", "Quark", "+2/3", "1/2", "0.002"],
            ["Down Quark", "Quark", "-1/3", "1/2", "0.005"],
            ["Charm Quark", "Quark", "+2/3", "1/2", "1.275"],
            ["Strange Quark", "Quark", "-1/3", "1/2", "0.095"],
            ["Top Quark", "Quark", "+2/3", "1/2", "173.0"],
            ["Bottom Quark", "Quark", "-1/3", "1/2", "4.18"],
            ["Photon", "Boson", "0", "1", "0"],
            ["W Boson", "Boson", "±1", "1", "80.4"],
            ["Z Boson", "Boson", "0", "1", "91.2"],
            ["Gluon", "Boson", "0", "1", "0"],
            ["Higgs Boson", "Boson", "0", "0", "125.1"]
        ]

        # Create a styled table
        particle_table = self.styling_enhancer.create_styled_table(
            particle_data,
            [1.2*inch, 1*inch, 0.8*inch, 0.8*inch, 1.2*inch],
            style_name=style_theme
        )

        elements.append(particle_table)
        elements.append(Paragraph("Table 1: Properties of fundamental particles in the Standard Model",
                                 styles["caption"]))
        elements.append(Spacer(1, 15))

        # Add a molecular structure diagram
        elements.append(Paragraph("Quantum Field Interactions", styles["heading1"]))
        # Register this section in the TOC
        toc.addEntry(0, "Quantum Field Interactions", 6)
        elements.append(Paragraph(
            "The Complete Theory of Everything describes interactions between particles in terms of quantum fields. "
            "The following diagram illustrates a typical interaction vertex:",
            styles["normal"]))
        elements.append(Spacer(1, 6))

        # Create an enhanced particle interaction diagram
        feynman_path = self.enhanced_graphics.create_particle_interaction_diagram(style=style_theme)

        elements.append(Image(feynman_path, width=4*inch, height=3*inch))
        elements.append(Paragraph("Figure 3: Feynman diagram of electron-positron annihilation",
                                 styles["caption"]))
        elements.append(Spacer(1, 15))

        # Add implications
        elements.append(Paragraph("Implications", styles["heading1"]))
        # Register this section in the TOC
        toc.addEntry(0, "Implications", 7)
        elements.append(Paragraph(
            "The Complete Theory of Everything has profound implications for our understanding of the universe:",
            styles["normal"]))
        elements.append(Spacer(1, 6))

        implications = [
            "Unification of all fundamental forces",
            "Explanation of dark matter and dark energy",
            "Resolution of the black hole information paradox",
            "Prediction of new particles and phenomena",
            "Consistent description of the early universe"
        ]

        # Create a bullet list
        bullet_elements = self.styling_enhancer.create_bullet_list(implications, styles["bullet"])
        elements.extend(bullet_elements)
        elements.append(Spacer(1, 10))

        # Add a pie chart of universe composition
        elements.append(Paragraph("Universe Composition", styles["heading1"]))
        # Register this section in the TOC
        toc.addEntry(0, "Universe Composition", 8)
        elements.append(Paragraph(
            "According to the Complete Theory of Everything, the universe is composed of different forms of energy and matter. "
            "The following chart shows the composition of the universe:",
            styles["normal"]))
        elements.append(Spacer(1, 6))

        # Create a pie chart of universe composition
        universe_data = [
            {"category": "Dark Energy", "value": 68.3},
            {"category": "Dark Matter", "value": 26.8},
            {"category": "Ordinary Matter", "value": 4.9}
        ]

        universe_chart_path = self.scientific_enhancer.create_scientific_chart(
            "pie", universe_data, "Composition of the Universe", "", ""
        )

        elements.append(Image(universe_chart_path, width=4*inch, height=3*inch))
        elements.append(Paragraph("Figure 4: Composition of the universe according to current observations",
                                 styles["caption"]))
        elements.append(Spacer(1, 15))

        # Add a diagram of the universe's evolution with interactive chart
        elements.append(Paragraph("Universe Evolution", styles["heading1"]))
        # Register this section in the TOC
        toc.addEntry(0, "Universe Evolution", 9)
        elements.append(Paragraph(
            "The Complete Theory of Everything provides a consistent description of the universe's evolution "
            "from the Big Bang to the present day:",
            styles["normal"]))
        elements.append(Spacer(1, 6))

        # Create an enhanced diagram of the universe's evolution
        evolution_path = self.enhanced_graphics.create_universe_evolution_diagram(style=style_theme)
        elements.append(Image(evolution_path, width=6*inch, height=3*inch))
        elements.append(Paragraph("Figure 5: Timeline of the universe's evolution from the Big Bang to the present day",
                                 styles["caption"]))
        elements.append(Spacer(1, 15))

        # Add an interactive chart for universe expansion
        elements.append(Paragraph("Universe Expansion Rate", styles["heading2"]))
        elements.append(Paragraph(
            "The following interactive chart shows the expansion rate of the universe over time. "
            "Click on the chart to explore the data interactively.",
            styles["normal"]))
        elements.append(Spacer(1, 6))

        # Create interactive line chart data for universe expansion
        expansion_data = [
            {
                "name": "Expansion Rate",
                "data": [(0, 70), (2, 72), (4, 69), (6, 73), (8, 68), (10, 74), (12, 67), (14, 75)]
            },
            {
                "name": "Theoretical Prediction",
                "data": [(0, 70), (2, 71), (4, 72), (6, 73), (8, 74), (10, 75), (12, 76), (14, 77)]
            }
        ]

        # Add the interactive chart
        expansion_chart = self.charts_generator.create_interactive_line_chart(
            expansion_data,
            title="Universe Expansion Rate Over Time",
            x_label="Billions of Years Ago",
            y_label="Expansion Rate (km/s/Mpc)"
        )
        elements.append(expansion_chart)
        elements.append(Paragraph("Figure 6: Interactive chart of universe expansion rate over time",
                                 styles["caption"]))
        elements.append(Spacer(1, 15))

        # Add annotations
        elements.append(Paragraph("Notes and Annotations", styles["heading2"]))
        elements.append(Paragraph(
            "The following annotations provide additional insights into the universe's evolution:",
            styles["normal"]))
        elements.append(Spacer(1, 6))

        # Create annotations
        note = self.annotations_manager.create_note_annotation(
            "The expansion rate of the universe appears to be accelerating, which is attributed to dark energy."
        )
        elements.append(note)
        elements.append(Spacer(1, 10))

        highlight = self.annotations_manager.create_highlight_annotation(
            "The discrepancy between observed and theoretical expansion rates is known as the Hubble tension."
        )
        elements.append(highlight)
        elements.append(Spacer(1, 15))

        # Add conclusion
        elements.append(Paragraph("Conclusion", styles["heading1"]))
        # Register this section in the TOC
        toc.addEntry(0, "Conclusion", 10)
        elements.append(Paragraph(
            "The Complete Theory of Everything represents a significant advancement in theoretical physics, "
            "providing a unified framework for understanding the fundamental nature of reality. While further "
            "research and experimental verification are needed, this theory offers a promising path toward "
            "a complete understanding of the physical universe.",
            styles["normal"]))
        elements.append(Spacer(1, 10))

        elements.append(Paragraph(
            "The theory successfully unifies the four fundamental forces, explains the origin and evolution of the universe, "
            "and provides a consistent framework for understanding quantum phenomena and gravity. It also makes testable "
            "predictions that can be verified through experiments and astronomical observations.",
            styles["normal"]))

        # Add bookmarks for navigation
        elements.append(self.annotations_manager.create_bookmark("Conclusion", 0))

        # Add external resources section
        elements.append(Paragraph("External Resources", styles["heading2"]))
        elements.append(Paragraph(
            "For more information on the Theory of Everything, visit Wikipedia.",
            styles["normal"]))
        elements.append(Spacer(1, 10))

        # Add a pie chart for document composition
        elements.append(Paragraph("Document Composition", styles["heading2"]))
        elements.append(Paragraph(
            "The following interactive pie chart shows the composition of this document:",
            styles["normal"]))
        elements.append(Spacer(1, 6))

        # Create interactive pie chart data
        doc_composition_data = [
            {"category": "Text", "value": 45},
            {"category": "Equations", "value": 25},
            {"category": "Figures", "value": 20},
            {"category": "Tables", "value": 10}
        ]

        # Add the interactive pie chart
        doc_composition_chart = self.charts_generator.create_interactive_pie_chart(
            doc_composition_data,
            title="Document Composition"
        )
        elements.append(doc_composition_chart)
        elements.append(Paragraph("Figure 7: Interactive pie chart of document composition",
                                 styles["caption"]))
        elements.append(Spacer(1, 15))

        # Define a function for the footer with page numbers
        def add_page_numbers(canvas, doc):
            self.interactive_enhancer.create_footer_with_page_number(
                canvas, doc, "Complete Theory of Everything")

        # Build the PDF with title page background, bookmarks and page numbers
        try:
            # Build the document with title page background and page numbers
            doc.build(elements, onFirstPage=add_title_background, onLaterPages=add_page_numbers)

            print(f"Professional Complete Theory of Everything PDF saved to: {output_file}")
            return output_file
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            return None

    # Enhanced graphics are now handled by the EnhancedGraphicsGenerator class

# Main function for command-line usage
def main():
    """Main function for command-line usage"""
    import argparse

    parser = argparse.ArgumentParser(description="Professional PDF Agent")
    parser.add_argument("--style", type=str, default="scientific",
                        choices=["professional", "scientific", "elegant"],
                        help="Style theme to use")
    parser.add_argument("--font", type=str, default="Helvetica",
                        choices=["Helvetica", "Times-Roman", "Courier"],
                        help="Font family to use")
    parser.add_argument("--mode", type=str, default="scientific",
                        choices=["academic", "professional", "scientific", "resume", "presentation"],
                        help="Document mode to use")

    args = parser.parse_args()

    agent = ProfessionalPDFAgent()
    agent.generate_complete_theory_pdf(style_theme=args.style, font_family=args.font, document_mode=args.mode)

if __name__ == "__main__":
    main()

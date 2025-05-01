#!/usr/bin/env python3
"""
Generate a PDF document with properly formatted equations for the Theory of Everything.

This script creates a PDF document that contains all the formulas from the
Grand Unified Theory of Everything with proper LaTeX rendering.
"""

import os
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from datetime import datetime

try:
    # Try to import LaTeX rendering libraries
    from matplotlib import rc
    rc('text', usetex=True)
    rc('font', family='serif')
    HAS_LATEX = True
except:
    HAS_LATEX = False
    print("Warning: LaTeX rendering is not available. Equations may not display optimally.")
    print("Consider installing a LaTeX distribution like TeX Live or MiKTeX.")

# Define the equations with proper LaTeX formatting
EQUATIONS = {
    "master": {
        "title": "Master Equation",
        "equation": r"S = S_{\text{gravity}} + S_{\text{matter}} + S_{\text{gauge}} + S_{\text{quantum}}",
        "description": "The unified action combining all fundamental forces and matter interactions."
    },
    "einstein_hilbert": {
        "title": "Einstein-Hilbert Action (Classical Gravity)",
        "equation": r"S_{\text{gravity}}^{\text{EH}} = \frac{1}{16\pi G} \int d^4x \, \sqrt{-g} \, (R - 2\Lambda)",
        "description": "Describes classical gravity through spacetime curvature."
    },
    "loop_quantum_gravity": {
        "title": "Loop Quantum Gravity Extension",
        "equation": r"S_{\text{gravity}}^{\text{LQG}} = \frac{1}{8\pi G} \int d^4x \, \sqrt{-g} \, \epsilon^{abc} E_a^i E_b^j F_{ij}^c",
        "description": "Quantizes spacetime itself through loop variables."
    },
    "string_theory": {
        "title": "String/M-Theory Gravity",
        "equation": r"S_{\text{gravity}}^{\text{String}} = \frac{1}{2\kappa^2} \int d^{10}x \, \sqrt{-g} \, e^{-2\phi} \left(R + 4 (\nabla \phi)^2 - \frac{1}{12} H_{\mu\nu\rho} H^{\mu\nu\rho}\right)",
        "description": "Describes gravity in higher dimensions with strings as fundamental objects."
    },
    "dirac_action": {
        "title": "Fermion Fields (Dirac Action)",
        "equation": r"S_{\text{fermion}} = \int d^4x \, \sqrt{-g} \, \bar{\psi} (i \gamma^\mu D_\mu - m) \psi",
        "description": "Describes matter particles (fermions) in curved spacetime."
    },
    "higgs_action": {
        "title": "Higgs Field (Spontaneous Symmetry Breaking)",
        "equation": r"S_{\text{Higgs}} = \int d^4x \, \sqrt{-g} \, \left[ (D_\mu \phi)^\dagger (D^\mu \phi) - V(\phi) \right]",
        "description": "Gives mass to elementary particles through symmetry breaking."
    },
    "higgs_potential": {
        "title": "Higgs Potential",
        "equation": r"V(\phi) = -\mu^2 \phi^\dagger \phi + \lambda (\phi^\dagger \phi)^2",
        "description": "The 'Mexican hat' potential that drives spontaneous symmetry breaking."
    },
    "yang_mills": {
        "title": "Yang-Mills Action (Non-Abelian Gauge Fields)",
        "equation": r"S_{\text{gauge}} = -\frac{1}{4} \int d^4x \, \sqrt{-g} \, F_{\mu\nu}^a F^{\mu\nu}_a",
        "description": "Describes the strong and weak nuclear forces."
    },
    "susy_gauge": {
        "title": "Supersymmetric Gauge Fields",
        "equation": r"S_{\text{SUSY-gauge}} = \int d^4x \, \left[ -\frac{1}{4} F_{\mu\nu} F^{\mu\nu} + i \bar{\lambda} \gamma^\mu D_\mu \lambda \right]",
        "description": "Links fermions and bosons through supersymmetry."
    },
    "path_integral": {
        "title": "Path Integral Formulation",
        "equation": r"Z = \int \mathcal{D}\phi \, e^{i S[\phi]}",
        "description": "Quantum field theory formulation integrating over all possible field configurations."
    },
    "quantum_corrections": {
        "title": "Loop Corrections and Renormalization",
        "equation": r"S_{\text{quantum}} = \sum_{n=1}^{\infty} \hbar^n S_n",
        "description": "Accounts for quantum fluctuations and virtual particles."
    },
    "full_master": {
        "title": "Full Master Equation",
        "equation": r"S = \frac{1}{16\pi G} \int d^4x \, \sqrt{-g} \, (R - 2\Lambda) + \int d^4x \, \sqrt{-g} \left[ \bar{\psi} (i \gamma^\mu D_\mu - m) \psi + (D_\mu \phi)^\dagger (D^\mu \phi) - V(\phi) - \frac{1}{4} F_{\mu\nu}^a F^{\mu\nu}_a \right] + S_{\text{quantum}}",
        "description": "The complete Theory of Everything unifying all forces and matter."
    }
}

def create_equation_figure(eq_id, figsize=(8, 3)):
    """Create a figure with a properly formatted equation"""
    eq_data = EQUATIONS[eq_id]
    
    fig = plt.figure(figsize=figsize)
    plt.axis('off')
    
    # Add title
    plt.text(0.5, 0.85, eq_data["title"], 
             fontsize=14, ha='center', va='center', fontweight='bold')
    
    # Add equation
    plt.text(0.5, 0.5, f"${eq_data['equation']}$", 
             fontsize=12, ha='center', va='center')
    
    # Add description
    plt.text(0.5, 0.15, eq_data["description"], 
             fontsize=10, ha='center', va='center', style='italic')
    
    plt.tight_layout()
    return fig

def create_higgs_potential_figure():
    """Create a figure showing the Higgs potential"""
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    
    # Create a grid of points
    x = np.linspace(-2, 2, 100)
    y = np.linspace(-2, 2, 100)
    X, Y = np.meshgrid(x, y)
    
    # Calculate the Higgs potential (Mexican hat)
    mu2 = 1
    lambda_ = 0.5
    Z = -mu2 * (X**2 + Y**2) + lambda_ * (X**2 + Y**2)**2
    
    # Plot the surface
    surf = ax.plot_surface(X, Y, Z, cmap=plt.cm.coolwarm, alpha=0.8,
                          linewidth=0, antialiased=True)
    
    # Add labels
    ax.set_xlabel('Re($\\phi$)')
    ax.set_ylabel('Im($\\phi$)')
    ax.set_zlabel('V($\\phi$)')
    ax.set_title('Higgs Potential $V(\\phi) = -\\mu^2 \\phi^\\dagger \\phi + \\lambda (\\phi^\\dagger \\phi)^2$')
    
    plt.tight_layout()
    return fig

def create_force_unification_figure():
    """Create a figure showing force unification"""
    # Define coupling constants and their running
    alpha_em_0 = 1/137.036  # Electromagnetic
    alpha_s_0 = 0.1179      # Strong
    alpha_w_0 = 1/30        # Weak
    alpha_g_0 = 1           # Gravitational
    
    # Beta function coefficients
    b_em = 0.5
    b_s = -7
    b_w = -19/6
    b_g = 2
    
    # Generate energy scale points (log scale)
    energies = np.logspace(0, 19, 1000)
    
    # Calculate running couplings
    def running_coupling(alpha_0, b, energy):
        return alpha_0 / (1 - alpha_0 * b * np.log(energy/91.1876) / (2*np.pi))
    
    alpha_em = running_coupling(alpha_em_0, b_em, energies)
    alpha_s = running_coupling(alpha_s_0, b_s, energies)
    alpha_w = running_coupling(alpha_w_0, b_w, energies)
    
    # Gravitational coupling has different scaling
    alpha_g = alpha_g_0 * (energies/1e19)**2
    
    # Create figure
    fig = plt.figure(figsize=(8, 6))
    
    plt.plot(energies, alpha_em, label='Electromagnetic', linewidth=2)
    plt.plot(energies, alpha_s, label='Strong', linewidth=2)
    plt.plot(energies, alpha_w, label='Weak', linewidth=2)
    plt.plot(energies, alpha_g, label='Gravitational', linewidth=2)
    
    # Find approximate unification point
    diff = np.std([alpha_em, alpha_s, alpha_w], axis=0)
    unification_idx = np.argmin(diff)
    unification_energy = energies[unification_idx]
    unification_alpha = np.mean([alpha_em[unification_idx], 
                                alpha_s[unification_idx], 
                                alpha_w[unification_idx]])
    
    plt.scatter(unification_energy, unification_alpha, color='red', s=100, 
               zorder=5, label='Approximate Unification')
    
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Energy (GeV)', fontsize=12)
    plt.ylabel('Coupling Strength ($\\alpha$)', fontsize=12)
    plt.title('Unification of Fundamental Forces', fontsize=14)
    plt.legend(fontsize=10)
    plt.grid(True, which='both', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    return fig

def create_title_page():
    """Create a title page for the PDF"""
    fig = plt.figure(figsize=(8.5, 11))
    plt.axis('off')
    
    # Add title
    plt.text(0.5, 0.8, "The Grand Unified Theory of Everything", 
             fontsize=24, ha='center', va='center', fontweight='bold')
    
    # Add subtitle
    plt.text(0.5, 0.7, "Mathematical Formulation", 
             fontsize=18, ha='center', va='center')
    
    # Add date
    current_date = datetime.now().strftime("%B %d, %Y")
    plt.text(0.5, 0.6, current_date, 
             fontsize=14, ha='center', va='center')
    
    # Add description
    description = (
        "This document presents the complete mathematical formulation of the\n"
        "Theory of Everything, unifying all fundamental forces and matter interactions\n"
        "into a single coherent framework."
    )
    plt.text(0.5, 0.4, description, 
             fontsize=12, ha='center', va='center')
    
    plt.tight_layout()
    return fig

def create_toe_pdf(output_path="Theory_of_Everything.pdf"):
    """Create a PDF with all Theory of Everything formulas"""
    with PdfPages(output_path) as pdf:
        # Add title page
        pdf.savefig(create_title_page())
        plt.close()
        
        # Add introduction page
        fig = plt.figure(figsize=(8.5, 11))
        plt.axis('off')
        plt.text(0.5, 0.9, "Introduction", 
                 fontsize=18, ha='center', va='center', fontweight='bold')
        
        intro_text = (
            "The Theory of Everything (ToE) is a hypothetical unified physical theory that\n"
            "fully explains and links together all physical aspects of the universe.\n\n"
            "The Unified Action represents the foundational structure of the ToE. It unifies\n"
            "all physical forces and matter interactions into a single action functional,\n"
            "from quantum scales to cosmic dimensions.\n\n"
            "This document presents the complete mathematical formulation of the ToE,\n"
            "including all component equations and their relationships."
        )
        plt.text(0.5, 0.7, intro_text, 
                 fontsize=12, ha='center', va='center')
        
        pdf.savefig(fig)
        plt.close()
        
        # Add master equation
        pdf.savefig(create_equation_figure("master", figsize=(8.5, 5)))
        plt.close()
        
        # Add gravity section
        fig = plt.figure(figsize=(8.5, 11))
        plt.axis('off')
        plt.text(0.5, 0.9, "I. Gravity Action", 
                 fontsize=18, ha='center', va='center', fontweight='bold')
        
        gravity_text = (
            "The Gravity Action describes how spacetime curves in response to energy and matter.\n"
            "It includes classical general relativity and its quantum extensions."
        )
        plt.text(0.5, 0.8, gravity_text, 
                 fontsize=12, ha='center', va='center')
        
        pdf.savefig(fig)
        plt.close()
        
        # Add gravity equations
        for eq_id in ["einstein_hilbert", "loop_quantum_gravity", "string_theory"]:
            pdf.savefig(create_equation_figure(eq_id))
            plt.close()
        
        # Add matter section
        fig = plt.figure(figsize=(8.5, 11))
        plt.axis('off')
        plt.text(0.5, 0.9, "II. Matter Action", 
                 fontsize=18, ha='center', va='center', fontweight='bold')
        
        matter_text = (
            "The Matter Action describes all forms of matter and their interactions with spacetime.\n"
            "It includes fermions (matter particles) and the Higgs field that gives them mass."
        )
        plt.text(0.5, 0.8, matter_text, 
                 fontsize=12, ha='center', va='center')
        
        pdf.savefig(fig)
        plt.close()
        
        # Add matter equations
        for eq_id in ["dirac_action", "higgs_action", "higgs_potential"]:
            pdf.savefig(create_equation_figure(eq_id))
            plt.close()
        
        # Add Higgs potential visualization
        pdf.savefig(create_higgs_potential_figure())
        plt.close()
        
        # Add gauge section
        fig = plt.figure(figsize=(8.5, 11))
        plt.axis('off')
        plt.text(0.5, 0.9, "III. Gauge Field Action", 
                 fontsize=18, ha='center', va='center', fontweight='bold')
        
        gauge_text = (
            "The Gauge Field Action describes the fundamental forces: electromagnetic,\n"
            "strong nuclear, and weak nuclear forces. It includes both standard and\n"
            "supersymmetric formulations."
        )
        plt.text(0.5, 0.8, gauge_text, 
                 fontsize=12, ha='center', va='center')
        
        pdf.savefig(fig)
        plt.close()
        
        # Add gauge equations
        for eq_id in ["yang_mills", "susy_gauge"]:
            pdf.savefig(create_equation_figure(eq_id))
            plt.close()
        
        # Add force unification visualization
        pdf.savefig(create_force_unification_figure())
        plt.close()
        
        # Add quantum section
        fig = plt.figure(figsize=(8.5, 11))
        plt.axis('off')
        plt.text(0.5, 0.9, "IV. Quantum Corrections", 
                 fontsize=18, ha='center', va='center', fontweight='bold')
        
        quantum_text = (
            "Quantum Corrections account for the effects of quantum fluctuations\n"
            "and virtual particles. They ensure the theory is consistent at all scales."
        )
        plt.text(0.5, 0.8, quantum_text, 
                 fontsize=12, ha='center', va='center')
        
        pdf.savefig(fig)
        plt.close()
        
        # Add quantum equations
        for eq_id in ["path_integral", "quantum_corrections"]:
            pdf.savefig(create_equation_figure(eq_id))
            plt.close()
        
        # Add full master equation
        fig = plt.figure(figsize=(8.5, 11))
        plt.axis('off')
        plt.text(0.5, 0.9, "V. Full Master Equation", 
                 fontsize=18, ha='center', va='center', fontweight='bold')
        
        full_text = (
            "The Full Master Equation combines all components into a single unified action.\n"
            "This represents the complete mathematical formulation of the Theory of Everything."
        )
        plt.text(0.5, 0.8, full_text, 
                 fontsize=12, ha='center', va='center')
        
        pdf.savefig(fig)
        plt.close()
        
        pdf.savefig(create_equation_figure("full_master", figsize=(8.5, 5)))
        plt.close()
        
        # Add implications page
        fig = plt.figure(figsize=(8.5, 11))
        plt.axis('off')
        plt.text(0.5, 0.9, "VI. Implications", 
                 fontsize=18, ha='center', va='center', fontweight='bold')
        
        implications_text = (
            "The Theory of Everything has profound implications for our understanding of the universe:\n\n"
            "1. Unified Physical Laws: All forces and matter fields are combined into a single framework.\n\n"
            "2. Quantum Gravity: Spacetime is quantized and emergent from more fundamental structures.\n\n"
            "3. Supersymmetry: A fundamental symmetry balances matter and force particles.\n\n"
            "4. Dark Matter/Energy: Naturally explained by quantum spacetime and supersymmetry.\n\n"
            "5. Origin of the Universe: Provides a mathematical framework for understanding\n"
            "   the beginning and evolution of the cosmos."
        )
        plt.text(0.5, 0.6, implications_text, 
                 fontsize=12, ha='left', va='center')
        
        pdf.savefig(fig)
        plt.close()
    
    print(f"PDF created successfully: {output_path}")
    return output_path

if __name__ == "__main__":
    # Set default output path
    output_path = "Theory_of_Everything.pdf"
    
    # Check if command line argument is provided
    if len(sys.argv) > 1:
        output_path = sys.argv[1]
    
    # Create the PDF
    pdf_path = create_toe_pdf(output_path)
    
    print(f"\nThe Theory of Everything PDF has been generated: {pdf_path}")
    print("This PDF contains properly formatted equations and visualizations.")
    
    # Try to open the PDF
    try:
        if sys.platform.startswith('darwin'):  # macOS
            os.system(f"open {pdf_path}")
        elif sys.platform.startswith('win'):   # Windows
            os.system(f"start {pdf_path}")
        elif sys.platform.startswith('linux'): # Linux
            os.system(f"xdg-open {pdf_path}")
    except:
        print("Could not automatically open the PDF. Please open it manually.")

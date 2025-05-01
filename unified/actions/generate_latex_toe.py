#!/usr/bin/env python3
"""
Generate a LaTeX document with properly formatted equations for the Theory of Everything.

This script creates a LaTeX document that contains all the formulas from the
Grand Unified Theory of Everything with proper LaTeX rendering, then compiles it to PDF.
"""

import os
import sys
import subprocess
from datetime import datetime

# LaTeX document template
LATEX_TEMPLATE = r"""
\documentclass[12pt]{article}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{xcolor}
\usepackage{geometry}
\usepackage{fancyhdr}
\usepackage{tikz}
\usepackage{float}

\geometry{margin=1in}
\hypersetup{colorlinks=true, linkcolor=blue, urlcolor=blue}

\title{\Huge \textbf{The Grand Unified Theory of Everything}\\
\Large Mathematical Formulation}
\author{}
\date{\today}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{Theory of Everything}
\fancyhead[R]{\thepage}
\fancyfoot[C]{\textcopyright\ \the\year}

\begin{document}

\maketitle
\thispagestyle{empty}

\begin{abstract}
This document presents the complete mathematical formulation of the Theory of Everything, 
unifying all fundamental forces and matter interactions into a single coherent framework.
The equations presented here represent the most comprehensive attempt to describe all 
physical phenomena within a unified mathematical structure.
\end{abstract}

\newpage
\tableofcontents
\newpage

\section{Introduction}

The Theory of Everything (ToE) is a hypothetical unified physical theory that fully explains 
and links together all physical aspects of the universe. Finding a ToE is one of the major 
unsolved problems in physics.

The Unified Action represents the foundational structure of the ToE. It unifies all physical 
forces and matter interactions into a single action functional, from quantum scales to cosmic 
dimensions.

\section{Master Equation}

The total action $S$ is composed of four main parts:

\begin{equation}
S = S_{\text{gravity}} + S_{\text{matter}} + S_{\text{gauge}} + S_{\text{quantum}}
\end{equation}

Where:
\begin{itemize}
\item $S_{\text{gravity}}$ → Quantum gravity action
\item $S_{\text{matter}}$ → Matter field action
\item $S_{\text{gauge}}$ → Gauge field (force) action
\item $S_{\text{quantum}}$ → Quantum corrections
\end{itemize}

\section{Gravity Action $S_{\text{gravity}}$}

The Gravity Action describes how spacetime curves in response to energy and matter. It includes 
classical general relativity and its quantum extensions.

\subsection{Einstein-Hilbert Action (Classical Gravity)}

\begin{equation}
S_{\text{gravity}}^{\text{EH}} = \frac{1}{16\pi G} \int d^4x \, \sqrt{-g} \, (R - 2\Lambda)
\end{equation}

Where:
\begin{itemize}
\item $G$ is Newton's gravitational constant
\item $g$ is the determinant of the metric tensor
\item $R$ is the Ricci scalar curvature
\item $\Lambda$ is the cosmological constant
\end{itemize}

\subsection{Loop Quantum Gravity (LQG) Extension}

\begin{equation}
S_{\text{gravity}}^{\text{LQG}} = \frac{1}{8\pi G} \int d^4x \, \sqrt{-g} \, \epsilon^{abc} E_a^i E_b^j F_{ij}^c
\end{equation}

Where:
\begin{itemize}
\item $E_a^i$ are the densitized triads (gravitational electric field)
\item $F_{ij}^c$ is the curvature of the Ashtekar connection
\item $\epsilon^{abc}$ is the Levi-Civita symbol
\end{itemize}

\subsection{String/M-Theory Gravity}

\begin{equation}
S_{\text{gravity}}^{\text{String}} = \frac{1}{2\kappa^2} \int d^{10}x \, \sqrt{-g} \, e^{-2\phi} \left(R + 4 (\nabla \phi)^2 - \frac{1}{12} H_{\mu\nu\rho} H^{\mu\nu\rho}\right)
\end{equation}

Where:
\begin{itemize}
\item $\kappa$ is related to the string tension
\item $\phi$ is the dilaton field
\item $H_{\mu\nu\rho}$ is the field strength of the Kalb-Ramond field
\item Integration is over 10 dimensions
\end{itemize}

\section{Matter Action $S_{\text{matter}}$}

The Matter Action describes all forms of matter and their interactions with spacetime. It includes 
fermions (matter particles) and the Higgs field that gives them mass.

\subsection{Fermion Fields (Dirac Action)}

\begin{equation}
S_{\text{fermion}} = \int d^4x \, \sqrt{-g} \, \bar{\psi} (i \gamma^\mu D_\mu - m) \psi
\end{equation}

Where:
\begin{itemize}
\item $\psi$ is the fermion field
\item $\bar{\psi}$ is the Dirac adjoint
\item $\gamma^\mu$ are the Dirac gamma matrices
\item $D_\mu$ is the covariant derivative
\item $m$ is the mass
\end{itemize}

\subsection{Higgs Field (Spontaneous Symmetry Breaking)}

\begin{equation}
S_{\text{Higgs}} = \int d^4x \, \sqrt{-g} \, \left[ (D_\mu \phi)^\dagger (D^\mu \phi) - V(\phi) \right]
\end{equation}

Where:
\begin{itemize}
\item $\phi$ is the Higgs field
\item $D_\mu$ is the covariant derivative
\item $V(\phi)$ is the Higgs potential
\end{itemize}

The Higgs potential has the form:

\begin{equation}
V(\phi) = -\mu^2 \phi^\dagger \phi + \lambda (\phi^\dagger \phi)^2
\end{equation}

This "Mexican hat" potential drives spontaneous symmetry breaking, giving mass to elementary particles.

\begin{figure}[H]
\centering
\begin{tikzpicture}
\draw[->] (-3,0) -- (3,0) node[right] {Re($\phi$)};
\draw[->] (0,-1) -- (0,3) node[above] {$V(\phi)$};
\draw[domain=-2.5:2.5,smooth,variable=\x,blue,thick] plot ({\x},{-1+\x*\x});
\draw[fill=red] (-1,0) circle (0.1);
\draw[fill=red] (1,0) circle (0.1);
\node at (0,-1.5) {Cross-section of the Higgs potential};
\end{tikzpicture}
\caption{Cross-section of the Higgs "Mexican hat" potential showing the degenerate vacuum states}
\end{figure}

\section{Gauge Field Action $S_{\text{gauge}}$}

The Gauge Field Action describes the fundamental forces: electromagnetic, strong nuclear, and weak 
nuclear forces. It includes both standard and supersymmetric formulations.

\subsection{Yang-Mills Action (Non-Abelian Gauge Fields)}

\begin{equation}
S_{\text{gauge}} = -\frac{1}{4} \int d^4x \, \sqrt{-g} \, F_{\mu\nu}^a F^{\mu\nu}_a
\end{equation}

Where:
\begin{itemize}
\item $F_{\mu\nu}^a$ is the field strength tensor
\item $a$ is the gauge group index
\end{itemize}

\subsection{Supersymmetric Gauge Fields}

\begin{equation}
S_{\text{SUSY-gauge}} = \int d^4x \, \left[ -\frac{1}{4} F_{\mu\nu} F^{\mu\nu} + i \bar{\lambda} \gamma^\mu D_\mu \lambda \right]
\end{equation}

Where:
\begin{itemize}
\item $\lambda$ is the gaugino (supersymmetric partner of gauge boson)
\item $\bar{\lambda}$ is its Dirac adjoint
\end{itemize}

\section{Quantum Corrections $S_{\text{quantum}}$}

Quantum Corrections account for the effects of quantum fluctuations and virtual particles. They 
ensure the theory is consistent at all scales.

\subsection{Path Integral Formulation}

\begin{equation}
Z = \int \mathcal{D}\phi \, e^{i S[\phi]}
\end{equation}

Where:
\begin{itemize}
\item $Z$ is the partition function
\item $\mathcal{D}\phi$ represents integration over all possible field configurations
\item $S[\phi]$ is the action functional
\end{itemize}

\subsection{Loop Corrections and Renormalization}

\begin{equation}
S_{\text{quantum}} = \sum_{n=1}^{\infty} \hbar^n S_n
\end{equation}

Where:
\begin{itemize}
\item $\hbar$ is the reduced Planck constant
\item $S_n$ represents $n$-loop corrections
\end{itemize}

\section{Full Master Equation}

The Full Master Equation combines all components into a single unified action. This represents the 
complete mathematical formulation of the Theory of Everything.

\begin{equation}
\begin{split}
S = \frac{1}{16\pi G} \int d^4x \, \sqrt{-g} \, (R - 2\Lambda) + \\
\int d^4x \, \sqrt{-g} \left[ \bar{\psi} (i \gamma^\mu D_\mu - m) \psi + (D_\mu \phi)^\dagger (D^\mu \phi) - V(\phi) - \frac{1}{4} F_{\mu\nu}^a F^{\mu\nu}_a \right] + \\
S_{\text{quantum}}
\end{split}
\end{equation}

\section{Force Unification}

One of the key predictions of the Theory of Everything is the unification of all fundamental forces 
at high energies. The coupling constants of the electromagnetic, weak, and strong forces converge 
at approximately $10^{16}$ GeV, with gravity joining at the Planck scale ($10^{19}$ GeV).

\begin{figure}[H]
\centering
\begin{tikzpicture}
\draw[->] (0,0) -- (10,0) node[right] {Energy (GeV)};
\draw[->] (0,0) -- (0,6) node[above] {Coupling Strength ($\alpha$)};

\node at (1,-0.5) {$10^2$};
\node at (5,-0.5) {$10^{10}$};
\node at (9,-0.5) {$10^{19}$};

\draw[blue,thick] (1,4) .. controls (3,2.5) and (6,1.5) .. (8,1);
\draw[red,thick] (1,0.5) .. controls (3,1) and (6,1.5) .. (8,1);
\draw[green,thick] (1,2) .. controls (3,1.5) and (6,1.5) .. (8,1);
\draw[purple,thick] (1,0.1) .. controls (5,0.2) and (7,0.5) .. (9,1);

\draw[fill=black] (8,1) circle (0.1);

\node[blue] at (1.5,4.3) {Strong};
\node[green] at (1.5,2.3) {Weak};
\node[red] at (1.5,0.8) {Electromagnetic};
\node[purple] at (2,0.3) {Gravitational};
\node at (8,0.5) {Unification};

\end{tikzpicture}
\caption{Unification of fundamental forces at high energies}
\end{figure}

\section{Implications}

The Theory of Everything has profound implications for our understanding of the universe:

\begin{enumerate}
\item \textbf{Unified Physical Laws:} All forces and matter fields are combined into a single framework.

\item \textbf{Quantum Gravity:} Spacetime is quantized and emergent from more fundamental structures.

\item \textbf{Supersymmetry:} A fundamental symmetry balances matter and force particles.

\item \textbf{Dark Matter/Energy:} Naturally explained by quantum spacetime and supersymmetry.

\item \textbf{Origin of the Universe:} Provides a mathematical framework for understanding the beginning and evolution of the cosmos.
\end{enumerate}

\section{Conclusion}

The Grand Unified Theory of Everything presented in this document represents the most comprehensive 
mathematical framework for understanding all physical phenomena. By unifying gravity, matter, gauge 
fields, and quantum effects, it provides a complete description of the universe from the smallest 
quantum scales to the largest cosmic structures.

While experimental verification of the complete theory remains challenging, various components have 
found support in existing observations and experiments. Future advances in high-energy physics, 
cosmology, and quantum gravity may provide further tests of this unified framework.

\end{document}
"""

def create_latex_file(output_dir="."):
    """Create a LaTeX file with all Theory of Everything formulas"""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Define file paths
    tex_file = os.path.join(output_dir, "Theory_of_Everything.tex")
    
    # Write LaTeX content to file
    with open(tex_file, "w") as f:
        f.write(LATEX_TEMPLATE)
    
    print(f"LaTeX file created: {tex_file}")
    return tex_file

def compile_latex_to_pdf(tex_file):
    """Compile LaTeX file to PDF using pdflatex"""
    try:
        # Run pdflatex twice to resolve references
        for _ in range(2):
            subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_file], 
                          cwd=os.path.dirname(tex_file),
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
        
        # Get the PDF file path
        pdf_file = tex_file.replace(".tex", ".pdf")
        
        if os.path.exists(pdf_file):
            print(f"PDF successfully created: {pdf_file}")
            return pdf_file
        else:
            print("PDF compilation failed.")
            return None
    except Exception as e:
        print(f"Error compiling LaTeX: {e}")
        print("Make sure you have a LaTeX distribution installed (e.g., TeX Live or MiKTeX).")
        return None

def main():
    """Main function to create and compile the LaTeX document"""
    print("Generating Theory of Everything LaTeX document...")
    
    # Create LaTeX file
    tex_file = create_latex_file()
    
    # Check if pdflatex is available
    try:
        subprocess.run(["pdflatex", "--version"], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE)
        has_pdflatex = True
    except:
        has_pdflatex = False
    
    if has_pdflatex:
        print("\nCompiling LaTeX to PDF...")
        pdf_file = compile_latex_to_pdf(tex_file)
        
        if pdf_file and os.path.exists(pdf_file):
            print("\nThe Theory of Everything PDF has been generated successfully!")
            
            # Try to open the PDF
            try:
                if sys.platform.startswith('darwin'):  # macOS
                    os.system(f"open {pdf_file}")
                elif sys.platform.startswith('win'):   # Windows
                    os.system(f"start {pdf_file}")
                elif sys.platform.startswith('linux'): # Linux
                    os.system(f"xdg-open {pdf_file}")
            except:
                print("Could not automatically open the PDF. Please open it manually.")
    else:
        print("\nLaTeX compilation is not available. The LaTeX file has been created,")
        print("but you will need to compile it manually using a LaTeX editor or compiler.")
        print("You can install a LaTeX distribution like TeX Live or MiKTeX to compile the document.")

if __name__ == "__main__":
    main()

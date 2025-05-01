#!/usr/bin/env python3
"""
Scientific Content Generator

This script generates sample scientific content for the Augmentic PDF Agent.
"""

import json
from augmentic_pdf_agent import PDFAgent

# Create sample scientific content
scientific_content = {
    "title": "Quantum Field Theory and the Standard Model",
    "subtitle": "A Comprehensive Overview",
    "abstract": (
        "This document provides a comprehensive overview of Quantum Field Theory (QFT) "
        "and the Standard Model of particle physics. We discuss the theoretical foundations, "
        "mathematical formalism, and experimental evidence supporting these frameworks. "
        "Additionally, we explore recent developments and open questions in the field."
    ),
    "introduction": (
        "Quantum Field Theory (QFT) represents one of the most successful theoretical frameworks "
        "in modern physics, providing a unified description of three of the four fundamental forces: "
        "electromagnetism, the weak nuclear force, and the strong nuclear force. The Standard Model, "
        "built upon QFT principles, has successfully predicted numerous particles and phenomena, "
        "including the Higgs boson discovered in 2012.\n\n"
        "This document explores the key concepts, mathematical formalism, and experimental evidence "
        "supporting QFT and the Standard Model. We also discuss current limitations and open questions "
        "that motivate ongoing research in theoretical physics."
    ),
    "methods": (
        "Our analysis employs both theoretical and experimental approaches to understand QFT and "
        "the Standard Model. On the theoretical side, we utilize the mathematical formalism of "
        "Lagrangian field theory, gauge symmetry, and renormalization. Experimentally, we review "
        "evidence from particle accelerators, particularly the Large Hadron Collider (LHC) at CERN, "
        "which has provided crucial validation for many aspects of the Standard Model."
    ),
    "results": (
        "The Standard Model successfully accounts for a wide range of phenomena in particle physics. "
        "It correctly predicts the existence and properties of fundamental particles, including quarks, "
        "leptons, and gauge bosons. The discovery of the Higgs boson in 2012 confirmed a key prediction "
        "of the Standard Model and provided insight into the origin of mass.\n\n"
        "Quantum Field Theory has also enabled precise calculations of particle interactions, with "
        "predictions matching experimental measurements to remarkable accuracy. For example, the "
        "theoretical prediction for the electron's magnetic moment agrees with experimental measurements "
        "to more than ten decimal places, representing one of the most precisely tested theories in science."
    ),
    "discussion": (
        "Despite its successes, the Standard Model faces several challenges. It does not incorporate "
        "gravity, the fourth fundamental force, suggesting the need for a more comprehensive theory. "
        "Additionally, it does not explain dark matter, dark energy, or the observed matter-antimatter "
        "asymmetry in the universe.\n\n"
        "Various extensions and alternatives to the Standard Model have been proposed, including "
        "supersymmetry, string theory, and loop quantum gravity. These approaches aim to address the "
        "limitations of the current framework while preserving its successful predictions."
    ),
    "conclusion": (
        "Quantum Field Theory and the Standard Model represent remarkable achievements in theoretical "
        "physics, providing a coherent framework for understanding fundamental particles and their "
        "interactions. While these theories have been extensively validated by experimental evidence, "
        "they also point to deeper structures and principles that remain to be discovered.\n\n"
        "Future research will likely focus on addressing the limitations of the Standard Model, "
        "particularly the integration of gravity and the explanation of cosmological phenomena. "
        "These efforts may lead to a more comprehensive 'Theory of Everything' that unifies all "
        "fundamental forces and provides a complete description of nature at its most fundamental level."
    ),
    "references": [
        "Weinberg, S. (1995). The Quantum Theory of Fields. Cambridge University Press.",
        "Peskin, M. E., & Schroeder, D. V. (1995). An Introduction to Quantum Field Theory. Westview Press.",
        "Griffiths, D. (2008). Introduction to Elementary Particles. Wiley-VCH.",
        "Schwartz, M. D. (2014). Quantum Field Theory and the Standard Model. Cambridge University Press.",
        "ATLAS Collaboration. (2012). Observation of a new particle in the search for the Standard Model Higgs boson with the ATLAS detector at the LHC. Physics Letters B, 716(1), 1-29.",
        "CMS Collaboration. (2012). Observation of a new boson at a mass of 125 GeV with the CMS experiment at the LHC. Physics Letters B, 716(1), 30-61."
    ]
}

# Create PDF agent and generate scientific document
if __name__ == "__main__":
    agent = PDFAgent()
    pdf_path = agent.create_scientific_document(
        scientific_content["title"],
        scientific_content,
        "quantum_field_theory.pdf"
    )
    print(f"Scientific document created: {pdf_path}")

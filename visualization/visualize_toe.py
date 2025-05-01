#!/usr/bin/env python3
"""
Theory of Everything Visualization Interface

This script provides a unified interface for visualizing various aspects of the
Theory of Everything, including quantum gravity, unified forces, and Schumann resonances.
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Import the Theory of Everything modules
try:
    # First try to import as a relative import
    from .math.toe import TheoryOfEverything, QuantumGeometry, UnifiedForces, demonstrate_visualizations
    from .math.schumann import SchumannResonance, demonstrate_schumann_visualizations
    from .math.toe_formulas import ToEFormulas, demonstrate_toe_formulas
except (ImportError, ValueError):
    # If that fails, try direct import (when running the script directly)
    try:
        # Try importing from a local directory named 'math'
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from math.toe import TheoryOfEverything, QuantumGeometry, UnifiedForces, demonstrate_visualizations
        from math.schumann import SchumannResonance, demonstrate_schumann_visualizations
        from math.toe_formulas import ToEFormulas, demonstrate_toe_formulas
    except ImportError:
        # If that fails, try importing the modules directly
        import toe as toe_module
        import schumann as schumann_module
        import toe_formulas as formulas_module

        TheoryOfEverything = toe_module.TheoryOfEverything
        QuantumGeometry = toe_module.QuantumGeometry
        UnifiedForces = toe_module.UnifiedForces
        demonstrate_visualizations = toe_module.demonstrate_visualizations

        SchumannResonance = schumann_module.SchumannResonance
        demonstrate_schumann_visualizations = schumann_module.demonstrate_schumann_visualizations

        ToEFormulas = formulas_module.ToEFormulas
        demonstrate_toe_formulas = formulas_module.demonstrate_toe_formulas


def main_menu():
    """Display the main menu for the Theory of Everything visualization interface"""
    while True:
        print("\n" + "="*50)
        print("   THEORY OF EVERYTHING VISUALIZATION SUITE")
        print("="*50 + "\n")

        print("This application provides visualizations for various aspects of")
        print("the Theory of Everything, from quantum gravity to unified forces.\n")

        print("Select a visualization category:")
        print("1. Theory of Everything Formulas")
        print("2. Fundamental Forces and Unification")
        print("3. Quantum Gravity and Spacetime")
        print("4. Schumann Resonances")
        print("5. Exit\n")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            demonstrate_toe_formulas()
        elif choice == '2':
            forces_menu()
        elif choice == '3':
            quantum_menu()
        elif choice == '4':
            demonstrate_schumann_visualizations()
        elif choice == '5':
            print("\nExiting the Theory of Everything Visualization Suite...")
            break
        else:
            print("\nInvalid choice. Please try again.")


def forces_menu():
    """Display the menu for force unification visualizations"""
    uf = UnifiedForces()
    toe = TheoryOfEverything()

    print("\n" + "-"*50)
    print("   FUNDAMENTAL FORCES VISUALIZATIONS")
    print("-"*50 + "\n")

    print("Select a visualization:")
    print("1. Force Unification across Energy Scales")
    print("2. Relative Strengths of Fundamental Forces")
    print("3. Return to Main Menu\n")

    choice = input("Enter your choice (1-3): ")

    if choice == '1':
        uf.visualize_coupling_unification()
    elif choice == '2':
        uf.visualize_force_strength_comparison()
    elif choice == '3':
        return
    else:
        print("\nInvalid choice. Returning to Forces menu.")
        forces_menu()


def quantum_menu():
    """Display the menu for quantum gravity visualizations"""
    toe = TheoryOfEverything()
    qg = QuantumGeometry()

    print("\n" + "-"*50)
    print("   QUANTUM GRAVITY VISUALIZATIONS")
    print("-"*50 + "\n")

    print("Select a visualization:")
    print("1. Spacetime Curvature Due to Mass")
    print("2. Quantum Foam - Spacetime Fluctuations")
    print("3. Quantum Corrections to Classical Action")
    print("4. Quantum Metric Eigenspectrum")
    print("5. Return to Main Menu\n")

    choice = input("Enter your choice (1-5): ")

    if choice == '1':
        toe.visualize_spacetime_curvature()
    elif choice == '2':
        qg.visualize_quantum_foam()
    elif choice == '3':
        toe.visualize_quantum_corrections()
    elif choice == '4':
        qg.visualize_quantum_metric_eigenspectrum()
    elif choice == '5':
        return
    else:
        print("\nInvalid choice. Returning to Quantum menu.")
        quantum_menu()


if __name__ == "__main__":
    # Check if matplotlib is in interactive mode
    if not plt.isinteractive():
        plt.ion()  # Turn on interactive mode for better user experience

    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nExiting due to user interrupt...")
    except Exception as e:
        print(f"\n\nAn error occurred: {e}")
    finally:
        # Make sure to close all plots when exiting
        plt.close('all')
        print("\nThank you for exploring the Theory of Everything!")

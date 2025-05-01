#!/usr/bin/env python3
"""
Gauge Field Action Component of the Theory of Everything

This module implements the two main components of the Gauge Field Action:
1. Yang-Mills Action (Non-Abelian Gauge Fields)
2. Supersymmetric Gauge Fields

Each component is implemented as a separate class with methods for calculating
the action, field equations, and visualizing the results.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import sympy as sp
from sympy import symbols, Matrix, Eq, latex, sqrt, exp, I
from scipy.integrate import quad, solve_ivp
from scipy.sparse.linalg import eigs

class YangMillsAction:
    """
    Implementation of the Yang-Mills Action for non-Abelian gauge fields.

    The Yang-Mills action is given by:
    S_gauge = -(1/4) ∫ d^4x √(-g) F_μν^a F^μν_a

    Where:
    - g is the determinant of the metric tensor
    - F_μν^a is the field strength tensor
    - a is the gauge group index
    """

    def __init__(self):
        """Initialize the Yang-Mills Action"""
        self.c = 299792458    # Speed of light
        self.hbar = 1.054571817e-34  # Reduced Planck constant

        # Gauge coupling constants
        self.g_strong = 1.0  # Strong force coupling
        self.g_weak = 0.65   # Weak force coupling
        self.g_em = 0.31     # Electromagnetic force coupling

        # Initialize symbolic variables
        self.init_symbols()

    def init_symbols(self):
        """Initialize symbolic variables for calculations"""
        self.x, self.y, self.z, self.t = symbols('x y z t')
        self.g = symbols('g')  # Metric determinant
        self.F_munu = symbols('F_{\\mu\\nu}^a')  # Field strength tensor
        self.F_munu_up = symbols('F^{\\mu\\nu}_a')  # Field strength with raised indices

        # Define the action symbolically
        self.action_symbolic = -sp.Rational(1, 4) * sp.Integral(
            sp.sqrt(-self.g) * self.F_munu * self.F_munu_up,
            (self.x, self.y, self.z, self.t)
        )
        # Note: The correct form is -1/4 ∫d⁴x √(-g) F_μν^a F^μν_a
        # For SU(3): F_μν^a = ∂_μA_ν^a - ∂_νA_μ^a + g f^abc A_μ^b A_ν^c

    def field_strength_tensor(self, A, mu, nu, a, gauge_group='SU(3)'):
        """
        Calculate the field strength tensor F_μν^a

        Parameters:
        -----------
        A : numpy.ndarray
            The gauge field
        mu, nu : int
            Spacetime indices
        a : int
            Gauge group index
        gauge_group : str
            The gauge group ('U(1)', 'SU(2)', or 'SU(3)')

        Returns:
        --------
        float or numpy.ndarray
            The field strength tensor component
        """
        # This is a simplified calculation
        # In reality, would involve structure constants and proper derivatives

        # For U(1) (electromagnetic)
        if gauge_group == 'U(1)':
            # F_μν = ∂_μ A_ν - ∂_ν A_μ
            return 0.0  # Placeholder

        # For SU(2) (weak force)
        elif gauge_group == 'SU(2)':
            # F_μν^a = ∂_μ A_ν^a - ∂_ν A_μ^a + g ε^abc A_μ^b A_ν^c
            return 0.0  # Placeholder

        # For SU(3) (strong force)
        elif gauge_group == 'SU(3)':
            # F_μν^a = ∂_μ A_ν^a - ∂_ν A_μ^a + g f^abc A_μ^b A_ν^c
            return 0.0  # Placeholder

        else:
            raise ValueError(f"Unsupported gauge group: {gauge_group}")

    def visualize_field_strength(self, grid_size=20):
        """
        Visualize the field strength of a gauge field

        Parameters:
        -----------
        grid_size : int
            Size of the grid for visualization
        """
        # Create a grid of points
        x = np.linspace(-5, 5, grid_size)
        y = np.linspace(-5, 5, grid_size)
        X, Y = np.meshgrid(x, y)

        # Create a simple gauge field configuration (magnetic monopole)
        # This is just for visualization purposes
        r = np.sqrt(X**2 + Y**2 + 0.1**2)  # Add small constant to avoid division by zero
        Bx = X / r**3
        By = Y / r**3

        # Calculate field strength (magnitude of B field)
        B_magnitude = np.sqrt(Bx**2 + By**2)

        # Create the plot
        plt.figure(figsize=(12, 10))

        # Plot the vector field
        plt.streamplot(X, Y, Bx, By, density=1.5, color=B_magnitude,
                      cmap=plt.cm.viridis, linewidth=1.5, arrowsize=1.5)

        # Add a color bar
        plt.colorbar(label='Field Strength')

        # Add labels
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Gauge Field Strength Visualization')
        plt.axis('equal')
        plt.grid(False)
        plt.tight_layout()
        plt.show()

    def visualize_force_unification(self, energy_range=(1, 1e19), points=1000):
        """
        Visualize the unification of gauge coupling constants

        Parameters:
        -----------
        energy_range : tuple
            Min and max energy in GeV
        points : int
            Number of points to calculate
        """
        # Define coupling constants and their running
        alpha_em_0 = 1/137.036  # Electromagnetic
        alpha_s_0 = 0.1179      # Strong
        alpha_w_0 = 1/30        # Weak

        # Beta function coefficients
        b_em = 0.5
        b_s = -7
        b_w = -19/6

        # Generate energy scale points (log scale)
        energies = np.logspace(np.log10(energy_range[0]), np.log10(energy_range[1]), points)

        # Calculate running couplings
        def running_coupling(alpha_0, b, energy):
            return alpha_0 / (1 - alpha_0 * b * np.log(energy/91.1876) / (2*np.pi))

        alpha_em = running_coupling(alpha_em_0, b_em, energies)
        alpha_s = running_coupling(alpha_s_0, b_s, energies)
        alpha_w = running_coupling(alpha_w_0, b_w, energies)

        # Plot the running coupling constants
        plt.figure(figsize=(12, 8))

        plt.plot(energies, alpha_em, label='Electromagnetic', linewidth=2)
        plt.plot(energies, alpha_s, label='Strong', linewidth=2)
        plt.plot(energies, alpha_w, label='Weak', linewidth=2)

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
        plt.title('Unification of Gauge Coupling Constants', fontsize=14)
        plt.legend(fontsize=10)
        plt.grid(True, which='both', linestyle='--', alpha=0.7)

        # Add annotation for unification point
        plt.annotate(f'Unification Energy: {unification_energy:.1e} GeV',
                    xy=(unification_energy, unification_alpha),
                    xytext=(unification_energy/100, unification_alpha*5),
                    arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
                    fontsize=10)

        plt.tight_layout()
        plt.show()

    def display_action(self):
        """Display the Yang-Mills Action in LaTeX format"""
        print("Yang-Mills Action (Non-Abelian Gauge Fields):")
        display_eq = f"S_{{gauge}} = -\\frac{{1}}{{4}} \\int d^4x \\, \\sqrt{{-g}} \\, F_{{\\mu\\nu}}^a F^{{\\mu\\nu}}_a"
        print(f"${display_eq}$")


class SupersymmetricGaugeAction:
    """
    Implementation of Supersymmetric Gauge Fields.

    The Supersymmetric Gauge action is given by:
    S_SUSY-gauge = ∫ d^4x [-1/4 F_μν F^μν + i λ̄γ^μ D_μλ]

    Where:
    - F_μν is the field strength tensor
    - λ is the gaugino (supersymmetric partner of gauge boson)
    - λ̄ is the Dirac adjoint
    - γ^μ are the Dirac gamma matrices
    - D_μ is the covariant derivative
    """

    def __init__(self):
        """Initialize the Supersymmetric Gauge Action"""
        self.c = 299792458    # Speed of light
        self.hbar = 1.054571817e-34  # Reduced Planck constant

        # Initialize symbolic variables
        self.init_symbols()

    def init_symbols(self):
        """Initialize symbolic variables for calculations"""
        self.x, self.y, self.z, self.t = symbols('x y z t')
        self.F_munu = symbols('F_{\\mu\\nu}')  # Field strength tensor
        self.F_munu_up = symbols('F^{\\mu\\nu}')  # Field strength with raised indices
        self.lambda_ = symbols('\\lambda')  # Gaugino field
        self.lambda_bar = symbols('\\bar{\\lambda}')  # Gaugino adjoint
        self.gamma = symbols('\\gamma^{\\mu}')  # Dirac gamma matrices
        self.D_mu = symbols('D_{\\mu}')  # Covariant derivative

        # Define the action symbolically
        self.action_symbolic = sp.Integral(
            -sp.Rational(1, 4) * self.F_munu * self.F_munu_up +
            I * self.lambda_bar * self.gamma * self.D_mu * self.lambda_,
            (self.x, self.y, self.z, self.t)
        )
        # Note: The correct form is ∫d⁴x [-1/4 F_μν F^μν + iλ̄γ^μ D_μλ]
        # where λ is the gaugino (supersymmetric partner of the gauge boson)

    def visualize_supersymmetry_multiplet(self):
        """Visualize a supersymmetry multiplet (gauge boson and gaugino)"""
        # Create figure
        plt.figure(figsize=(12, 8))

        # Create a simple representation of a SUSY multiplet
        # This is just a schematic visualization

        # Draw gauge boson (vector)
        plt.arrow(0, 0, 1, 0, head_width=0.1, head_length=0.1, fc='blue', ec='blue', linewidth=2)
        plt.text(0.5, 0.15, 'Gauge Boson (spin-1)', ha='center', fontsize=12)

        # Draw gaugino (fermion)
        theta = np.linspace(0, 2*np.pi, 100)
        x_circle = 0.5 + 0.1 * np.cos(theta)
        y_circle = -0.5 + 0.1 * np.sin(theta)
        plt.plot(x_circle, y_circle, 'r-', linewidth=2)
        plt.arrow(0.5, -0.5, 0.15, 0, head_width=0.05, head_length=0.05,
                 fc='red', ec='red', linewidth=1)
        plt.text(0.5, -0.7, 'Gaugino (spin-1/2)', ha='center', fontsize=12)

        # Draw SUSY transformation
        plt.arrow(0.2, -0.1, 0.2, -0.3, head_width=0.05, head_length=0.05,
                 fc='green', ec='green', linewidth=1.5, linestyle='--')
        plt.arrow(0.8, -0.4, -0.2, 0.3, head_width=0.05, head_length=0.05,
                 fc='green', ec='green', linewidth=1.5, linestyle='--')
        plt.text(0.3, -0.25, 'SUSY', color='green', fontsize=10, rotation=-60)
        plt.text(0.7, -0.25, 'SUSY', color='green', fontsize=10, rotation=60)

        # Set plot properties
        plt.xlim(-0.5, 1.5)
        plt.ylim(-1, 0.5)
        plt.axis('off')
        plt.title('Supersymmetry Multiplet: Gauge Boson and Gaugino', fontsize=14)
        plt.tight_layout()
        plt.show()

    def visualize_susy_breaking(self):
        """Visualize supersymmetry breaking through mass splitting"""
        # Create figure
        plt.figure(figsize=(12, 8))

        # Energy levels
        energy_levels = {
            'Unbroken SUSY': [1.0, 1.0],
            'Broken SUSY': [1.0, 1.5]
        }

        # Labels
        particles = ['Gauge Boson', 'Gaugino']
        colors = ['blue', 'red']

        # Plot energy levels
        x_positions = [0, 1]
        width = 0.3

        # Unbroken SUSY
        for i, (particle, energy) in enumerate(zip(particles, energy_levels['Unbroken SUSY'])):
            plt.bar(x_positions[0] - width/2 + i*width, energy, width,
                   color=colors[i], alpha=0.7, label=particle if x_positions[0] == 0 else "")
            plt.text(x_positions[0] - width/2 + i*width, energy + 0.05,
                    f"{energy:.1f}", ha='center', fontsize=10)

        # Broken SUSY
        for i, (particle, energy) in enumerate(zip(particles, energy_levels['Broken SUSY'])):
            plt.bar(x_positions[1] - width/2 + i*width, energy, width,
                   color=colors[i], alpha=0.7)
            plt.text(x_positions[1] - width/2 + i*width, energy + 0.05,
                    f"{energy:.1f}", ha='center', fontsize=10)

        # Add labels
        plt.xticks(x_positions, ['Unbroken SUSY', 'Broken SUSY'], fontsize=12)
        plt.ylabel('Mass (arbitrary units)', fontsize=12)
        plt.title('Supersymmetry Breaking: Mass Splitting in Multiplet', fontsize=14)
        plt.legend(fontsize=10)
        plt.grid(True, axis='y', alpha=0.3)
        plt.tight_layout()
        plt.show()

    def display_action(self):
        """Display the Supersymmetric Gauge Action in LaTeX format"""
        print("Supersymmetric Gauge Fields:")
        display_eq = f"S_{{SUSY-gauge}} = \\int d^4x \\, \\left[ -\\frac{{1}}{{4}} F_{{\\mu\\nu}} F^{{\\mu\\nu}} + i \\bar{{\\lambda}} \\gamma^\\mu D_\\mu \\lambda \\right]"
        print(f"${display_eq}$")


def demonstrate_gauge_actions():
    """Demonstrate the gauge field action components"""
    print("\n===== Gauge Field Action Components =====\n")

    # Create instances of each gauge action
    yang_mills = YangMillsAction()
    susy_gauge = SupersymmetricGaugeAction()

    # Display the actions
    yang_mills.display_action()
    print("\n")
    susy_gauge.display_action()

    # Ask user which visualization to show
    print("\nSelect a visualization to display:")
    print("1. Gauge Field Strength (Yang-Mills)")
    print("2. Force Unification (Yang-Mills)")
    print("3. Supersymmetry Multiplet (SUSY)")
    print("4. Supersymmetry Breaking (SUSY)")
    print("0. Exit")

    choice = input("\nEnter your choice (0-4): ")

    if choice == '1':
        yang_mills.visualize_field_strength()
    elif choice == '2':
        yang_mills.visualize_force_unification()
    elif choice == '3':
        susy_gauge.visualize_supersymmetry_multiplet()
    elif choice == '4':
        susy_gauge.visualize_susy_breaking()
    elif choice == '0':
        return
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    demonstrate_gauge_actions()

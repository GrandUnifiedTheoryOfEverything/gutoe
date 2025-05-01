#!/usr/bin/env python3
"""
Matter Action Component of the Theory of Everything

This module implements the two main components of the Matter Action:
1. Fermion Fields (Dirac Action)
2. Higgs Field (Spontaneous Symmetry Breaking)

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

class FermionAction:
    """
    Implementation of the Fermion Fields (Dirac Action).

    The Dirac action is given by:
    S_fermion = ∫ d^4x √(-g) ψ̄(iγ^μ D_μ - m)ψ

    Where:
    - g is the determinant of the metric tensor
    - ψ is the fermion field
    - ψ̄ is the Dirac adjoint
    - γ^μ are the Dirac gamma matrices
    - D_μ is the covariant derivative
    - m is the mass of the fermion
    """

    def __init__(self):
        """Initialize the Fermion Action"""
        self.c = 299792458    # Speed of light
        self.hbar = 1.054571817e-34  # Reduced Planck constant

        # Initialize symbolic variables and gamma matrices
        self.init_symbols()
        self.init_gamma_matrices()

    def init_symbols(self):
        """Initialize symbolic variables for calculations"""
        self.x, self.y, self.z, self.t = symbols('x y z t')
        self.g = symbols('g')  # Metric determinant
        self.psi = symbols('\\psi')  # Fermion field
        self.psi_bar = symbols('\\bar{\\psi}')  # Dirac adjoint
        self.gamma = symbols('\\gamma^{\\mu}')  # Dirac gamma matrices
        self.D_mu = symbols('D_{\\mu}')  # Covariant derivative
        self.m = symbols('m')  # Mass

        # Define the action symbolically
        self.action_symbolic = sp.Integral(
            sp.sqrt(-self.g) * self.psi_bar * (I * self.gamma * self.D_mu - self.m) * self.psi,
            (self.x, self.y, self.z, self.t)
        )
        # Note: The correct form is ∫d⁴x √(-g) ψ̄(iγᵘDᵤ - m)ψ

    def init_gamma_matrices(self):
        """Initialize the Dirac gamma matrices"""
        # Pauli matrices
        sigma_x = np.array([[0, 1], [1, 0]])
        sigma_y = np.array([[0, -1j], [1j, 0]])
        sigma_z = np.array([[1, 0], [0, -1]])

        # Dirac gamma matrices in the Dirac representation
        gamma0 = np.array([[1, 0, 0, 0],
                          [0, 1, 0, 0],
                          [0, 0, -1, 0],
                          [0, 0, 0, -1]])

        gamma1 = np.array([[0, 0, 0, 1],
                          [0, 0, 1, 0],
                          [0, -1, 0, 0],
                          [-1, 0, 0, 0]])

        gamma2 = np.array([[0, 0, 0, -1j],
                          [0, 0, 1j, 0],
                          [0, 1j, 0, 0],
                          [-1j, 0, 0, 0]])

        gamma3 = np.array([[0, 0, 1, 0],
                          [0, 0, 0, -1],
                          [-1, 0, 0, 0],
                          [0, 1, 0, 0]])

        self.gamma_matrices = [gamma0, gamma1, gamma2, gamma3]

    def dirac_equation(self, psi, x, m):
        """
        Compute the Dirac equation for a fermion field

        Parameters:
        -----------
        psi : numpy.ndarray
            The fermion field as a 4-component spinor
        x : numpy.ndarray
            The spacetime coordinates (t, x, y, z)
        m : float
            The mass of the fermion

        Returns:
        --------
        numpy.ndarray
            The result of applying the Dirac operator to psi
        """
        # Simplified implementation of the Dirac equation
        # In a real implementation, this would involve the covariant derivative
        result = np.zeros_like(psi, dtype=complex)

        # Apply the Dirac operator (iγ^μ∂_μ - m)
        for mu in range(4):
            # This is a simplified derivative calculation
            # In reality, would use proper numerical differentiation
            derivative = psi  # Placeholder
            result += 1j * np.dot(self.gamma_matrices[mu], derivative)

        result -= m * psi

        return result

    def visualize_spinor_field(self, grid_size=20):
        """
        Visualize a spinor field in 3D space

        Parameters:
        -----------
        grid_size : int
            Size of the grid for visualization
        """
        # Create a grid of points
        x = np.linspace(-5, 5, grid_size)
        y = np.linspace(-5, 5, grid_size)
        X, Y = np.meshgrid(x, y)

        # Create a simple spinor field (just for visualization)
        # In reality, spinor fields are complex 4-component objects
        amplitude = np.exp(-(X**2 + Y**2)/10)
        phase = np.arctan2(Y, X)
        Z_real = amplitude * np.cos(phase)
        Z_imag = amplitude * np.sin(phase)

        # Create 3D plot
        fig = plt.figure(figsize=(15, 7))

        # Real part
        ax1 = fig.add_subplot(121, projection='3d')
        surf1 = ax1.plot_surface(X, Y, Z_real, cmap=cm.viridis, alpha=0.8,
                               linewidth=0, antialiased=True)
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Re(ψ)')
        ax1.set_title('Real Part of Spinor Field')

        # Imaginary part
        ax2 = fig.add_subplot(122, projection='3d')
        surf2 = ax2.plot_surface(X, Y, Z_imag, cmap=cm.plasma, alpha=0.8,
                               linewidth=0, antialiased=True)
        ax2.set_xlabel('X')
        ax2.set_ylabel('Y')
        ax2.set_zlabel('Im(ψ)')
        ax2.set_title('Imaginary Part of Spinor Field')

        plt.tight_layout()
        plt.show()

    def visualize_dirac_sea(self, energy_range=(-10, 10), num_points=1000):
        """
        Visualize the Dirac sea of negative energy states

        Parameters:
        -----------
        energy_range : tuple
            Range of energies to visualize
        num_points : int
            Number of points in the visualization
        """
        # Create energy values
        energies = np.linspace(energy_range[0], energy_range[1], num_points)

        # Calculate density of states (simplified model)
        # In reality, this would involve solving the Dirac equation
        m = 1.0  # Mass in arbitrary units
        density = np.sqrt(energies**2 - m**2) * np.heaviside(np.abs(energies) - m, 0.5)

        # Create the plot
        plt.figure(figsize=(12, 8))

        # Plot positive energy states
        plt.fill_between(energies, 0, density, where=(energies > m),
                        color='blue', alpha=0.5, label='Particles')

        # Plot negative energy states (Dirac sea)
        plt.fill_between(energies, 0, density, where=(energies < -m),
                        color='red', alpha=0.5, label='Dirac Sea (Antiparticles)')

        # Plot the energy gap
        plt.axvspan(-m, m, color='gray', alpha=0.3, label='Energy Gap (2m)')

        # Add labels and legend
        plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
        plt.xlabel('Energy (mc²)')
        plt.ylabel('Density of States')
        plt.title('Dirac Sea of Negative Energy States')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    def display_action(self):
        """Display the Fermion Action in LaTeX format"""
        print("Fermion Fields (Dirac Action):")
        display_eq = f"S_{{fermion}} = \\int d^4x \\, \\sqrt{{-g}} \\, \\bar{{\\psi}} (i \\gamma^\\mu D_\\mu - m) \\psi"
        print(f"${display_eq}$")


class HiggsAction:
    """
    Implementation of the Higgs Field (Spontaneous Symmetry Breaking).

    The Higgs action is given by:
    S_Higgs = ∫ d^4x √(-g) [(D_μφ)†(D^μφ) - V(φ)]

    Where:
    - g is the determinant of the metric tensor
    - φ is the Higgs field
    - D_μ is the covariant derivative
    - V(φ) is the Higgs potential
    """

    def __init__(self):
        """Initialize the Higgs Action"""
        self.c = 299792458    # Speed of light
        self.hbar = 1.054571817e-34  # Reduced Planck constant

        # Higgs potential parameters
        self.mu2 = 1.0  # Quadratic coefficient (negative for symmetry breaking)
        self.lambda_ = 0.5  # Quartic coefficient

        # Initialize symbolic variables
        self.init_symbols()

    def init_symbols(self):
        """Initialize symbolic variables for calculations"""
        self.x, self.y, self.z, self.t = symbols('x y z t')
        self.g = symbols('g')  # Metric determinant
        self.phi = symbols('\\phi')  # Higgs field
        self.phi_dag = symbols('\\phi^\\dagger')  # Higgs field adjoint
        self.D_mu = symbols('D_{\\mu}')  # Covariant derivative
        self.D_mu_phi = symbols('(D_{\\mu}\\phi)')  # Covariant derivative of phi
        self.D_mu_phi_dag = symbols('(D_{\\mu}\\phi)^\\dagger')  # Adjoint
        self.V_phi = symbols('V(\\phi)')  # Higgs potential

        # Define the action symbolically
        self.action_symbolic = sp.Integral(
            sp.sqrt(-self.g) * (self.D_mu_phi_dag * self.D_mu_phi - self.V_phi),
            (self.x, self.y, self.z, self.t)
        )

    def higgs_potential(self, phi):
        """
        Calculate the Higgs potential V(φ) = -μ²|φ|² + λ|φ|⁴

        This is the famous "Mexican hat" potential that leads to spontaneous
        symmetry breaking when μ² > 0 and λ > 0.

        Parameters:
        -----------
        phi : complex or numpy.ndarray
            The Higgs field (can be complex scalar or array)

        Returns:
        --------
        float or numpy.ndarray
            The Higgs potential value(s)
        """
        phi_squared = np.abs(phi)**2
        return -self.mu2 * phi_squared + self.lambda_ * phi_squared**2

    def visualize_higgs_potential_1d(self):
        """Visualize the Higgs potential in 1D"""
        # Create phi values (real part only for simplicity)
        phi_values = np.linspace(-2, 2, 1000)

        # Calculate potential
        V = self.higgs_potential(phi_values)

        # Create the plot
        plt.figure(figsize=(12, 8))
        plt.plot(phi_values, V, 'b-', linewidth=2)

        # Mark the minima
        minima = np.sqrt(self.mu2 / (2 * self.lambda_))
        plt.plot([-minima, minima], [self.higgs_potential(-minima), self.higgs_potential(minima)],
                'ro', markersize=8)

        # Add labels
        plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
        plt.xlabel('$\\phi$ (Higgs field)')
        plt.ylabel('$V(\\phi)$ (Potential)')
        plt.title('Higgs Potential $V(\\phi) = -\\mu^2 |\\phi|^2 + \\lambda |\\phi|^4$')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    def visualize_higgs_potential_2d(self):
        """Visualize the Higgs potential in 2D (Mexican hat)"""
        # Create a grid of points
        x = np.linspace(-2, 2, 100)
        y = np.linspace(-2, 2, 100)
        X, Y = np.meshgrid(x, y)

        # Calculate the Higgs potential (Mexican hat)
        Z = self.higgs_potential(X + 1j*Y)

        # Create 3D plot
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')

        # Plot the surface
        surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, alpha=0.8,
                              linewidth=0, antialiased=True)

        # Add a color bar
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='Potential Energy')

        # Add labels
        ax.set_xlabel('Re($\\phi$)')
        ax.set_ylabel('Im($\\phi$)')
        ax.set_zlabel('$V(\\phi)$')
        ax.set_title('Higgs Potential $V(\\phi) = -\\mu^2 |\\phi|^2 + \\lambda |\\phi|^4$')

        plt.tight_layout()
        plt.show()

    def visualize_symmetry_breaking(self, time_steps=100, perturbation=0.1):
        """
        Visualize spontaneous symmetry breaking over time

        Parameters:
        -----------
        time_steps : int
            Number of time steps in the animation
        perturbation : float
            Size of the initial perturbation
        """
        # Create figure
        plt.figure(figsize=(12, 8))

        # Create a circle representing the potential minimum
        theta = np.linspace(0, 2*np.pi, 100)
        minima = np.sqrt(self.mu2 / (2 * self.lambda_))
        x_circle = minima * np.cos(theta)
        y_circle = minima * np.sin(theta)

        # Plot the potential minimum circle
        plt.plot(x_circle, y_circle, 'k--', alpha=0.5, label='Potential Minimum')

        # Initial position (slightly perturbed from unstable equilibrium)
        x0, y0 = perturbation, 0

        # Simulate the field rolling down to the minimum
        x_positions = []
        y_positions = []

        for t in range(time_steps):
            # Simple dynamics (not physically accurate, just for visualization)
            # In reality, would solve field equations

            # Current radius
            r = np.sqrt(x0**2 + y0**2)

            # Force towards the minimum (gradient of potential)
            if r < 1e-10:  # Avoid division by zero
                fx, fy = -perturbation, 0  # Small push in x direction
            else:
                force_magnitude = 2 * self.mu2 * r - 4 * self.lambda_ * r**3
                fx = force_magnitude * x0 / r
                fy = force_magnitude * y0 / r

            # Update position (simplified dynamics)
            x0 += 0.01 * fx
            y0 += 0.01 * fy

            # Store positions
            x_positions.append(x0)
            y_positions.append(y0)

        # Plot the trajectory
        plt.plot(x_positions, y_positions, 'r-', alpha=0.7, label='Field Evolution')
        plt.plot(x_positions[0], y_positions[0], 'go', label='Initial State')
        plt.plot(x_positions[-1], y_positions[-1], 'ro', label='Final State')

        # Add labels
        plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
        plt.xlabel('Re($\\phi$)')
        plt.ylabel('Im($\\phi$)')
        plt.title('Spontaneous Symmetry Breaking in the Higgs Field')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    def display_action(self):
        """Display the Higgs Action in LaTeX format"""
        print("Higgs Field (Spontaneous Symmetry Breaking):")
        display_eq = f"S_{{Higgs}} = \\int d^4x \\, \\sqrt{{-g}} \\, \\left[ (D_\\mu \\phi)^\\dagger (D^\\mu \\phi) - V(\\phi) \\right]"
        print(f"${display_eq}$")

        print("\nHiggs Potential:")
        display_eq = f"V(\\phi) = -\\mu^2 \\phi^\\dagger \\phi + \\lambda (\\phi^\\dagger \\phi)^2"
        print(f"${display_eq}$")


def demonstrate_matter_actions():
    """Demonstrate the matter action components"""
    print("\n===== Matter Action Components =====\n")

    # Create instances of each matter action
    fermion = FermionAction()
    higgs = HiggsAction()

    # Display the actions
    fermion.display_action()
    print("\n")
    higgs.display_action()

    # Ask user which visualization to show
    print("\nSelect a visualization to display:")
    print("1. Spinor Field (Fermion)")
    print("2. Dirac Sea (Fermion)")
    print("3. Higgs Potential 1D")
    print("4. Higgs Potential 2D (Mexican Hat)")
    print("5. Spontaneous Symmetry Breaking")
    print("0. Exit")

    choice = input("\nEnter your choice (0-5): ")

    if choice == '1':
        fermion.visualize_spinor_field()
    elif choice == '2':
        fermion.visualize_dirac_sea()
    elif choice == '3':
        higgs.visualize_higgs_potential_1d()
    elif choice == '4':
        higgs.visualize_higgs_potential_2d()
    elif choice == '5':
        higgs.visualize_symmetry_breaking()
    elif choice == '0':
        return
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    demonstrate_matter_actions()

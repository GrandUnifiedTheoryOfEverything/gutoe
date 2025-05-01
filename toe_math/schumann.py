#!/usr/bin/env python3
"""
Schumann Resonance Implementation

This module implements the Schumann resonance phenomenon, which are global
electromagnetic resonances in the Earth-ionosphere cavity. The module provides
methods for calculating resonant frequencies, visualizing resonance modes,
and creating 3D visualizations of the Earth-ionosphere cavity.

The Schumann resonances are a set of spectrum peaks in the extremely low
frequency (ELF) portion of the Earth's electromagnetic field spectrum,
occurring between 7.83 and 33.8 Hz.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from scipy import signal

class SchumannResonance:
    """Class for modeling and visualizing Schumann resonances.

    This class provides methods for calculating Schumann resonance frequencies,
    modeling wave amplitudes, and visualizing resonance modes in the Earth-ionosphere
    cavity.

    Attributes:
        earth_radius (float): Radius of the Earth in meters
        speed_of_light (float): Speed of light in m/s
        fundamental_freq (float): Fundamental Schumann resonance frequency in Hz
        resonance_modes (list): List of the first 5 Schumann resonance frequencies
    """

    def __init__(self):
        self.earth_radius = 6371000  # meters
        self.speed_of_light = 299792458  # m/s
        self.fundamental_freq = 7.83  # Hz
        self.resonance_modes = [7.83, 14.3, 20.8, 27.3, 33.8]  # First 5 modes

    def calculate_resonant_frequencies(self, n_modes):
        """Calculate resonant frequencies for n modes
        fn = f0 * √(n(n+1)) where f0 ≈ 7.83 Hz"""
        frequencies = []
        for n in range(1, n_modes + 1):
            fn = self.fundamental_freq * np.sqrt(n * (n + 1))
            frequencies.append(fn)
        return frequencies

    def wave_amplitude(self, time, frequency, damping=0.1):
        """Model wave amplitude with damping"""
        return np.exp(-damping * time) * np.sin(2 * np.pi * frequency * time)

    def plot_resonances(self, duration=1.0, sampling_rate=1000, modes=3, interactive=False):
        """Plot Schumann resonance modes

        Parameters:
        -----------
        duration : float
            Duration of the simulation in seconds
        sampling_rate : int
            Number of samples per second
        modes : int
            Number of modes to plot (default: 3)
        interactive : bool
            If True, creates an interactive plot with sliders for damping
        """
        t = np.linspace(0, duration, int(sampling_rate * duration))

        if interactive and plt.get_backend() != 'nbAgg':
            try:
                from ipywidgets import interact, FloatSlider
                import ipywidgets as widgets

                def update_plot(damping=0.1):
                    plt.figure(figsize=(12, 8))
                    for i, freq in enumerate(self.resonance_modes[:modes]):
                        amplitude = self.wave_amplitude(t, freq, damping)
                        plt.plot(t, amplitude + i*2, label=f'Mode {i+1}: {freq:.1f} Hz')

                    plt.title(f'Schumann Resonance Modes (Damping: {damping:.2f})')
                    plt.xlabel('Time (s)')
                    plt.ylabel('Amplitude (arbitrary units)')
                    plt.legend()
                    plt.grid(True)
                    plt.show()

                # Create interactive widget
                interact(update_plot,
                         damping=FloatSlider(min=0.01, max=0.5, step=0.01, value=0.1,
                                           description='Damping:'))
            except ImportError:
                print("Interactive mode requires ipywidgets. Falling back to static plot.")
                interactive = False

        if not interactive:
            plt.figure(figsize=(12, 8))
            for i, freq in enumerate(self.resonance_modes[:modes]):
                amplitude = self.wave_amplitude(t, freq)
                plt.plot(t, amplitude + i*2, label=f'Mode {i+1}: {freq:.1f} Hz')

            plt.title('Schumann Resonance Modes')
            plt.xlabel('Time (s)')
            plt.ylabel('Amplitude (arbitrary units)')
            plt.legend()
            plt.grid(True)
            plt.show()

    def plot_frequency_spectrum(self, duration=5.0, sampling_rate=1000, noise_level=0.1):
        """Plot the frequency spectrum of Schumann resonances with noise"""
        # Generate time series with all resonance modes and some noise
        t = np.linspace(0, duration, int(sampling_rate * duration))
        signal_combined = np.zeros_like(t)

        # Add each resonance mode
        for freq in self.resonance_modes:
            signal_combined += self.wave_amplitude(t, freq, damping=0.05)

        # Add random noise
        np.random.seed(42)  # For reproducibility
        noise = noise_level * np.random.normal(0, 1, len(t))
        signal_with_noise = signal_combined + noise

        # Compute frequency spectrum
        freqs, power = signal.welch(signal_with_noise, fs=sampling_rate,
                                   nperseg=int(sampling_rate), scaling='spectrum')

        # Plot the results
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

        # Time domain plot
        ax1.plot(t, signal_with_noise)
        ax1.set_title('Schumann Resonances with Noise (Time Domain)')
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Amplitude')
        ax1.grid(True)

        # Frequency domain plot
        ax2.semilogy(freqs, power)
        ax2.set_title('Power Spectrum')
        ax2.set_xlabel('Frequency (Hz)')
        ax2.set_ylabel('Power Spectral Density')
        ax2.set_xlim(0, 50)  # Focus on the Schumann resonance range
        ax2.grid(True)

        # Add vertical lines at the resonance frequencies
        for freq in self.resonance_modes:
            ax2.axvline(x=freq, color='r', linestyle='--', alpha=0.7)
            ax2.text(freq+0.5, np.max(power)/2, f'{freq} Hz',
                     rotation=90, verticalalignment='center')

        plt.tight_layout()
        plt.show()

    def visualize_earth_ionosphere_cavity(self):
        """Create a 3D visualization of the Earth-ionosphere cavity"""
        # Create a sphere for Earth
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')

        # Generate sphere coordinates
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 50)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))

        # Plot Earth
        earth = ax.plot_surface(x, y, z, color='blue', alpha=0.7, label='Earth')

        # Calculate ionosphere height ratio
        properties = self.cavity_properties()
        ionosphere_height_km = properties['cavity_height']
        height_ratio = 1 + ionosphere_height_km / (self.earth_radius / 1000)

        # Plot ionosphere (slightly transparent)
        ionosphere = ax.plot_surface(height_ratio*x, height_ratio*y, height_ratio*z,
                                    color='red', alpha=0.3, label='Ionosphere')

        # Add a standing wave visualization (simplified)
        theta = np.linspace(0, 2*np.pi, 100)
        wave_r = np.linspace(1, height_ratio, 20)
        wave_amplitude = 0.02  # Exaggerated for visibility

        for r in wave_r:
            wave_x = r * np.cos(theta)
            wave_y = r * np.sin(theta)
            wave_z = wave_amplitude * np.sin(8*theta) * (r-1)/(height_ratio-1)
            ax.plot(wave_x, wave_y, wave_z, color='yellow', alpha=0.5, linewidth=0.5)

        # Set plot limits and labels
        ax.set_xlim([-height_ratio*1.1, height_ratio*1.1])
        ax.set_ylim([-height_ratio*1.1, height_ratio*1.1])
        ax.set_zlim([-height_ratio*1.1, height_ratio*1.1])
        ax.set_title('Earth-Ionosphere Cavity (Schumann Resonance)')

        # Add text annotation
        ax.text(0, 0, -1.5, f'Earth Radius: 6371 km\nIonosphere Height: {ionosphere_height_km:.1f} km',
                fontsize=10, horizontalalignment='center')

        plt.tight_layout()
        plt.show()

    def cavity_properties(self):
        """Calculate Earth-ionosphere cavity properties"""
        wavelength = self.speed_of_light / self.fundamental_freq
        cavity_height = wavelength / 2
        return {
            'cavity_height': cavity_height / 1000,  # km
            'wavelength': wavelength / 1000,  # km
            'circumference': 2 * np.pi * self.earth_radius / 1000  # km
        }

def demonstrate_schumann_visualizations():
    """Demonstrate the visualization capabilities for Schumann resonances"""
    print("\n===== Schumann Resonance Visualization Suite =====\n")
    print("This module provides visualizations for Schumann resonances.")
    print("Select a visualization to display:\n")
    print("1. Basic Resonance Modes")
    print("2. Frequency Spectrum Analysis")
    print("3. Earth-Ionosphere Cavity 3D Visualization")
    print("4. All Visualizations (Warning: Opens multiple windows)")
    print("0. Exit")

    choice = input("\nEnter your choice (0-4): ")

    sr = SchumannResonance()

    # Print cavity properties in any case
    properties = sr.cavity_properties()
    print("\nEarth-Ionosphere Cavity Properties:")
    print(f"Approximate cavity height: {properties['cavity_height']:.2f} km")
    print(f"Fundamental wavelength: {properties['wavelength']:.2f} km")
    print(f"Earth circumference: {properties['circumference']:.2f} km")

    # Calculate and print first 5 resonant frequencies
    frequencies = sr.calculate_resonant_frequencies(5)
    print("\nSchumann Resonance Modes:")
    for i, freq in enumerate(frequencies):
        print(f"Mode {i+1}: {freq:.2f} Hz")

    # Show selected visualization
    if choice == '1':
        sr.plot_resonances(modes=5)
    elif choice == '2':
        sr.plot_frequency_spectrum()
    elif choice == '3':
        sr.visualize_earth_ionosphere_cavity()
    elif choice == '4':
        print("\nGenerating all visualizations...")
        sr.plot_resonances(modes=5)
        sr.plot_frequency_spectrum()
        sr.visualize_earth_ionosphere_cavity()
    elif choice == '0':
        print("Exiting...")
        return
    else:
        print("Invalid choice. Please run again and select a valid option.")


if __name__ == "__main__":
    demonstrate_schumann_visualizations()

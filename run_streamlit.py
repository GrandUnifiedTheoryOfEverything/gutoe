#!/usr/bin/env python3
"""
Run the Streamlit application for the Theory of Everything project
"""

import os
import sys
import subprocess

def main():
    """Main function"""
    # Check if Streamlit is installed
    try:
        import streamlit
        print("Streamlit is already installed.")
    except ImportError:
        print("Streamlit is not installed. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

    # Create the logo if it doesn't exist
    if not os.path.exists("gfx/toe_logo.png"):
        print("Creating logo...")
        subprocess.run([sys.executable, "create_logo.py"])

    # Create 4D visualizations if they don't exist
    if not os.path.exists("gfx/4d/4d_hypercube_projection.png") or \
       not os.path.exists("gfx/4d/4d_quantum_field.png") or \
       not os.path.exists("gfx/4d/4d_spacetime_evolution.gif"):
        print("Creating 4D visualizations...")
        subprocess.run([sys.executable, "create_4d_vis.py"])

    # Create the gfx subdirectories if they don't exist
    for subdir in ["2d", "3d", "4d", "latex", "pdf"]:
        os.makedirs(f"gfx/{subdir}", exist_ok=True)

    # Run the Streamlit application
    print("Starting Streamlit application...")
    subprocess.run(["streamlit", "run", "streamlit_app.py"])

if __name__ == "__main__":
    main()

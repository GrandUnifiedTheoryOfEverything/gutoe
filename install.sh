#!/bin/bash
# Install script for the Theory of Everything project
# This script sets up a Python virtual environment, installs requirements,
# and runs the Streamlit UI/UX application

# Set the script to exit on error
set -e

# Print colored messages
print_green() {
    echo -e "\e[32m$1\e[0m"
}

print_blue() {
    echo -e "\e[34m$1\e[0m"
}

print_red() {
    echo -e "\e[31m$1\e[0m"
}

print_yellow() {
    echo -e "\e[33m$1\e[0m"
}

# Display banner
print_blue "========================================================"
print_blue "  Theory of Everything - Installation and Setup Script  "
print_blue "========================================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    print_red "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d " " -f 2)
print_green "Found Python $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "toe" ]; then
    print_yellow "Creating Python virtual environment (toe)..."
    python3 -m venv toe
    print_green "Virtual environment created successfully!"
else
    print_yellow "Virtual environment already exists. Skipping creation."
fi

# Activate the virtual environment
print_yellow "Activating virtual environment..."
source toe/bin/activate
print_green "Virtual environment activated!"

# Install requirements
print_yellow "Installing required packages..."
pip install -r requirements.txt
print_green "Required packages installed successfully!"

# Check if LaTeX is installed
if ! command -v pdflatex &> /dev/null; then
    print_yellow "WARNING: LaTeX (pdflatex) is not installed. PDF generation will not work."
    print_yellow "To install LaTeX:"
    print_yellow "  - Linux: sudo apt-get install texlive-full"
    print_yellow "  - macOS: brew install --cask mactex"
    print_yellow "  - Windows: Download and install MiKTeX from https://miktex.org/"
else
    print_green "LaTeX (pdflatex) is installed. PDF generation will work correctly."
fi

# Create necessary directories
print_yellow "Creating necessary directories..."
mkdir -p gfx/2d gfx/3d gfx/4d gfx/latex gfx/pdf
print_green "Directories created successfully!"

# Generate logo if it doesn't exist
if [ ! -f "gfx/toe_logo.png" ]; then
    print_yellow "Generating logo..."
    python create_logo.py
    print_green "Logo generated successfully!"
fi

# Generate 4D visualizations if they don't exist
if [ ! -f "gfx/4d/4d_hypercube_projection.png" ] || [ ! -f "gfx/4d/4d_quantum_field.png" ] || [ ! -f "gfx/4d/4d_spacetime_evolution.gif" ]; then
    print_yellow "Generating 4D visualizations..."
    python create_4d_vis.py
    print_green "4D visualizations generated successfully!"
fi

# Run the Streamlit application
print_blue "========================================================"
print_blue "  Starting the Theory of Everything Streamlit UI/UX     "
print_blue "========================================================"
echo ""
print_yellow "Running Streamlit application..."
streamlit run streamlit_app.py

# Note: The script will end when the Streamlit application is closed

# Theory of Everything Explorer

A Streamlit application for exploring and visualizing the Theory of Everything.

## Features

- **Explore Formulas**: View and explore the mathematical formulas that make up the Theory of Everything
- **Generate Visualizations**: Create visualizations of various aspects of the theory
- **Generate Documentation**: Generate LaTeX and PDF documentation for the theory
- **Interactive Visualizations**: Interact with 3D and 4D visualizations of the theory

## Installation

1. Make sure you have Python 3.8+ installed
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

To run the application, simply execute:

```bash
python run_streamlit.py
```

Or directly with Streamlit:

```bash
streamlit run streamlit_app.py
```

## Pages

The application consists of several pages:

- **Home**: Overview of the Theory of Everything and the application
- **Formulas**: Explore the mathematical formulas that make up the theory
- **Visualizations**: Generate and interact with visualizations of the theory
- **Documentation**: Generate LaTeX and PDF documentation for the theory
- **About**: Information about the Theory of Everything project

## Visualizations

### Standard Visualizations

The application includes several standard visualizations:

- **4D Spacetime Curvature**: Visualize 4D spacetime around massive objects
- **Quantum Foam 3D**: Visualize quantum foam in 3D
- **Extra Dimensions 3D**: Visualize extra dimensions in 3D
- **4D Higgs Field**: Visualize the 4D Higgs field
- **Gauge Field 4D**: Visualize a 4D gauge field configuration

### Advanced 4D Visualizations

The application also includes advanced 4D visualizations:

- **4D Hypercube Projection**: Visualize a 4D hypercube (tesseract) projected into 3D space
- **4D Quantum Field**: Visualize a 4D quantum field as multiple 3D slices
- **4D Spacetime Evolution**: Visualize the evolution of spacetime in 4D with time as the fourth dimension

## Documentation

The application can generate LaTeX and PDF documentation for the theory. The documentation includes:

- Formula descriptions
- LaTeX representations
- Component formulas
- Visualizations (optional)

## Directory Structure

- **streamlit_app.py**: Main Streamlit application
- **create_logo.py**: Script to create the application logo
- **run_streamlit.py**: Script to run the application
- **requirements.txt**: Required packages
- **gfx/**: Directory for graphics and output files
  - **toe_logo.png**: Application logo
  - **2d/**: 2D visualizations
  - **3d/**: 3D visualizations
  - **4d/**: 4D visualizations
  - **latex/**: LaTeX documents
  - **pdf/**: PDF documents

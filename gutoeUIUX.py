#!/usr/bin/env python3
"""
Streamlit UI/UX for the Theory of Everything project

This application provides a user-friendly interface to explore and visualize
the Theory of Everything, showcasing all the functionality of the project.
"""

import os
import sys
import json
import base64
from io import BytesIO
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


# Import the Theory of Everything components
from unified.toe_unified import ToEUnified 
from unified.toe_formulas import FormulaTools
from unified.toe_vis import VisualizationTools

# Set page configuration
st.set_page_config(
    page_title="Theory of Everything Explorer",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Define functions for the application

def get_image_base64(img_path):
    """Get base64 encoded image for embedding in HTML"""
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def get_plot_base64(fig):
    """Get base64 encoded plot for embedding in HTML"""
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()

def display_formula(formula_name, formula_data):
    """Display a formula with its components"""
    st.subheader(f"{formula_data.get('name', formula_name)}")
    st.write(formula_data.get('description', 'No description available'))
    
    # Display the LaTeX formula
    latex = formula_data.get('latex', '')
    if latex:
        st.latex(latex)
    
    # Display components if available
    components = formula_data.get('components', [])
    if components:
        st.write("#### Components")
        for component in components:
            if isinstance(component, dict):
                # If component is a dictionary with name and latex
                if 'name' in component and 'latex' in component:
                    st.write(f"- **{component['name']}**")
                    st.latex(component['latex'])
                    if 'description' in component:
                        st.write(f"  {component['description']}")
                # If component is just a name reference
                elif isinstance(component, str):
                    st.write(f"- {component}")
            else:
                # Fallback for any other format
                st.write(f"- {component}")

def generate_visualization(vis_name, params=None):
    """Generate a visualization and display it"""
    vis_tools = VisualizationTools()

    if params is None:
        # Get default parameters
        param_info = vis_tools.get_visualization_parameters(vis_name)
        params = {name: info['default'] for name, info in param_info.items()}

    # Generate the visualization
    path = vis_tools.generate_visualization(vis_name, params, show=False)

    # Display the visualization
    if os.path.exists(path):
        st.image(path, caption=f"{vis_name} visualization")
        st.success(f"Visualization saved to: {path}")
    else:
        st.error(f"Failed to generate visualization: {path}")

def create_interactive_visualization(vis_name):
    """Create an interactive visualization using matplotlib"""
    if vis_name == '4d_spacetime_curvature':
        return create_spacetime_curvature_vis()
    elif vis_name == 'quantum_foam_3d':
        return create_quantum_foam_vis()
    elif vis_name == 'extra_dimensions_3d':
        return create_extra_dimensions_vis()
    elif vis_name == '4d_higgs_field':
        return create_higgs_field_vis()
    elif vis_name == 'gauge_field_4d':
        return create_gauge_field_vis()
    else:
        st.warning(f"No interactive visualization available for {vis_name}")
        return None

def create_spacetime_curvature_vis():
    """Create an interactive spacetime curvature visualization"""
    # Get user parameters
    mass = st.slider("Mass (solar masses)", 0.1, 10.0, 1.0, 0.1)
    grid_size = st.slider("Grid size", 10, 50, 20, 1)

    # Create the visualization
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Create a grid of points
    x = np.linspace(-10, 10, grid_size)
    y = np.linspace(-10, 10, grid_size)
    X, Y = np.meshgrid(x, y)

    # Calculate Schwarzschild metric for a black hole
    r = np.sqrt(X**2 + Y**2 + 0.1**2)  # Add small constant to avoid division by zero
    c = 299792458  # Speed of light
    G = 6.67430e-11  # Gravitational constant
    M = mass * 1.989e30  # Convert solar masses to kg
    Rs = 2 * G * M / (c**2)  # Schwarzschild radius

    # Calculate time component of the metric (g_tt)
    g_tt = -(1 - Rs/r)

    # Calculate spatial curvature (simplified)
    Z = -Rs / (2 * r)

    # Plot the surface with time as color
    surf = ax.plot_surface(X, Y, Z, cmap=cm.viridis,
                          linewidth=0, antialiased=True)

    # Add labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Curvature')
    ax.set_title('4D Spacetime Curvature')

    # Add a color bar
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label='Time Dilation')

    return fig

def create_quantum_foam_vis():
    """Create an interactive quantum foam visualization"""
    # Get user parameters
    amplitude = st.slider("Amplitude", 0.1, 1.0, 0.5, 0.1)
    frequency = st.slider("Frequency", 0.5, 5.0, 2.0, 0.1)
    grid_size = st.slider("Grid size", 10, 30, 20, 1)

    # Create the visualization
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Create a 2D grid
    x = np.linspace(-5, 5, grid_size)
    y = np.linspace(-5, 5, grid_size)
    X, Y = np.meshgrid(x, y)

    # Generate random phases
    np.random.seed(42)  # For reproducibility
    phases = 2 * np.pi * np.random.random((3, 3))

    # Calculate quantum fluctuations with multiple frequency components
    Z = np.zeros_like(X)
    for i in range(3):
        for j in range(3):
            Z += amplitude * (1.0/(i+j+1)) * np.sin(frequency*(i+1)*X + phases[i,j]) * \
                 np.sin(frequency*(j+1)*Y + phases[i,j])

    # Plot the surface
    surf = ax.plot_surface(X, Y, Z, cmap=cm.viridis,
                          linewidth=0, antialiased=True)

    # Add labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Quantum Fluctuations')
    ax.set_title('Quantum Foam Visualization')

    # Add a color bar
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)

    return fig

def create_extra_dimensions_vis():
    """Create an interactive extra dimensions visualization"""
    # Get user parameters
    num_dimensions = st.slider("Number of dimensions", 4, 11, 10, 1)
    grid_size = st.slider("Grid size", 10, 30, 20, 1)

    # Create the visualization
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Create a sphere for the visible dimensions
    theta = np.linspace(0, 2 * np.pi, grid_size)
    phi = np.linspace(0, np.pi, grid_size)
    theta, phi = np.meshgrid(theta, phi)

    # Add some variation to represent extra dimensions
    r = 2 + 0.5 * np.sin(3 * theta) * np.sin(4 * phi)

    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi)

    # Plot the surface
    surf = ax.plot_surface(x, y, z, cmap=cm.viridis,
                          linewidth=0, antialiased=True)

    # Add labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'{num_dimensions}D Space Visualization')

    # Add a color bar
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label='Extra Dimensions')

    return fig

def create_higgs_field_vis():
    """Create an interactive Higgs field visualization"""
    # Get user parameters
    grid_size = st.slider("Grid size", 10, 50, 30, 1)

    # Create the visualization
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Create a 2D grid for the Mexican hat potential
    x = np.linspace(-2, 2, grid_size)
    y = np.linspace(-2, 2, grid_size)
    X, Y = np.meshgrid(x, y)

    # Calculate the Higgs potential (Mexican hat)
    R2 = X**2 + Y**2
    V = (R2 - 1)**2

    # Plot the surface
    surf = ax.plot_surface(X, Y, V, cmap=cm.viridis,
                          linewidth=0, antialiased=True)

    # Add labels
    ax.set_xlabel('Re(φ)')
    ax.set_ylabel('Im(φ)')
    ax.set_zlabel('V(φ)')
    ax.set_title('Higgs Potential (Mexican Hat)')

    # Add a color bar
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label='Potential Energy')

    return fig

def create_gauge_field_vis():
    """Create an interactive gauge field visualization"""
    # Get user parameters
    grid_size = st.slider("Grid size", 5, 20, 10, 1)

    # Create the visualization
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Create a 3D grid
    x = np.linspace(-2, 2, grid_size)
    y = np.linspace(-2, 2, grid_size)
    z = np.linspace(-2, 2, grid_size)
    X, Y, Z = np.meshgrid(x, y, z)

    # Calculate a simple vector field (magnetic dipole)
    R = np.sqrt(X**2 + Y**2 + Z**2)
    R3 = np.maximum(R**3, 0.001)  # Avoid division by zero

    # Magnetic dipole field components
    Bx = 3 * X * Z / R3
    By = 3 * Y * Z / R3
    Bz = (3 * Z**2 - R**2) / R3

    # Plot the vector field (subsample for clarity)
    stride = 2
    ax.quiver(X[::stride, ::stride, ::stride],
             Y[::stride, ::stride, ::stride],
             Z[::stride, ::stride, ::stride],
             Bx[::stride, ::stride, ::stride],
             By[::stride, ::stride, ::stride],
             Bz[::stride, ::stride, ::stride],
             length=0.5, normalize=True, color='b')

    # Add labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Gauge Field Visualization')

    return fig

def generate_latex_pdf(formula_name, include_components=False, include_visualizations=False):
    """Generate LaTeX and PDF documentation for a formula"""
    try:
        from unified.agents.latexagent import LaTeXAgent
        from unified.agents.pdfagent import PDFAgent

        # Create the agents
        latex_agent = LaTeXAgent(output_dir="gfx/latex")
        pdf_agent = PDFAgent(output_dir="gfx/pdf")

        # Generate LaTeX
        latex_content = latex_agent.generate_latex(formula=formula_name, include_components=include_components)
        latex_file = latex_agent.save_latex(latex_content, f"{formula_name}.tex")

        # Generate PDF
        pdf_file = pdf_agent.generate_pdf(
            formula=formula_name,
            output=f"{formula_name}.pdf",
            include_components=include_components,
            include_visualizations=include_visualizations
        )

        return latex_file, pdf_file
    except Exception as e:
        st.error(f"Error generating documentation: {str(e)}")
        return None, None

# Main application
def ensure_directories():
    """Ensure all required directories exist"""
    # Create the gfx directory and subdirectories
    for directory in ["gfx", "gfx/2d", "gfx/3d", "gfx/4d", "gfx/latex", "gfx/pdf"]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            st.sidebar.info(f"Created directory: {directory}")

def main():
    """Main application function"""
    # Ensure all required directories exist
    ensure_directories()

    # Create the API
    api = ToEUnified(output_dir="gfx")

    # Sidebar
    st.sidebar.title("Theory of Everything Explorer")

    # Try to load the logo, use a placeholder if not found
    try:
        if os.path.exists("gfx/toe_logo.png"):
            st.sidebar.image("gfx/toe_logo.png", use_container_width=True)
        else:
            st.sidebar.info("Logo not found. Run create_logo.py to generate it.")
    except Exception as e:
        st.sidebar.warning(f"Could not load logo: {str(e)}")

    # Navigation
    page = st.sidebar.selectbox(
        "Navigation",
        ["Home", "Formulas", "Visualizations", "Documentation", "About"]
    )

    # Home page
    if page == "Home":
        st.title("🌌 Theory of Everything Explorer")
        st.markdown("""
        Welcome to the Theory of Everything Explorer! This application allows you to explore
        and visualize the Theory of Everything, a unified framework for physics that combines
        various physical theories into a single model.

        ### Features

        - **Explore Formulas**: View and explore the mathematical formulas that make up the Theory of Everything
        - **Generate Visualizations**: Create visualizations of various aspects of the theory
        - **Generate Documentation**: Generate LaTeX and PDF documentation for the theory
        - **Interactive Visualizations**: Interact with 3D and 4D visualizations of the theory

        Use the sidebar to navigate through the application.
        """)

        # Display a sample visualization
        st.subheader("Sample Visualization: 4D Spacetime Curvature")
        fig = create_spacetime_curvature_vis()
        st.pyplot(fig)

    # Formulas page
    elif page == "Formulas":
        st.title("📝 Theory of Everything Formulas")

        # List available formulas
        formulas = api.list_formulas()
        formula_name = st.selectbox("Select a formula", list(formulas.keys()))

        # Display the selected formula
        formula_data = api.get_formula(formula_name)
        display_formula(formula_name, formula_data)

        # Formula exploration
        if st.checkbox("Explore formula components"):
            exploration = api.explore_formula(formula_name)
            components = exploration.get('components', [])
            
            for component in components:
                st.markdown("---")
                if isinstance(component, dict) and 'name' in component and 'formula' in component:
                    # Component is a reference to another formula
                    display_formula(component['name'], component['formula'])
                elif isinstance(component, dict):
                    # Component is defined inline with a name
                    for name, data in component.items():
                        display_formula(name, data)
                else:
                    # Component is something else
                    st.write(component)

        # Formula comparison
        if st.checkbox("Compare with another formula"):
            other_formula = st.selectbox("Select another formula",
                                        [f for f in formulas.keys() if f != formula_name])

            comparison = api.compare_formulas([formula_name, other_formula])

            st.subheader("Common Components")
            common = comparison.get('common_components', [])
            if common:
                for component in common:
                    st.write(f"- {component}")
            else:
                st.write("No common components")

            st.subheader("Unique Components")
            unique = comparison.get('unique_components', {})
            for name, components in unique.items():
                st.write(f"**{name}**")
                if components:
                    for component in components:
                        st.write(f"- {component}")
                else:
                    st.write("No unique components")

    # Visualizations page
    elif page == "Visualizations":
        st.title("🔮 Theory of Everything Visualizations")

        # Create tabs for different visualization types
        viz_tab1, viz_tab2 = st.tabs(["Standard Visualizations", "Advanced 4D Visualizations"])

        with viz_tab1:
            # List available visualizations
            visualizations = api.list_visualizations()
            vis_name = st.selectbox("Select a visualization", list(visualizations.keys()))

            # Display visualization info
            vis_info = api.get_visualization_info(vis_name)
            st.write(vis_info.get('description', 'No description available'))

            # Visualization parameters
            st.subheader("Parameters")
            param_info = api.get_visualization_parameters(vis_name)

            # Create interactive visualization
            st.subheader("Interactive Visualization")
            fig = create_interactive_visualization(vis_name)
            if fig:
                st.pyplot(fig)

                # Save visualization
                if st.button("Save Visualization"):
                    # Get parameters from sliders
                    params = {}
                    if vis_name == '4d_spacetime_curvature':
                        params = {
                            'mass': st.session_state.get('mass', 1.0),
                            'grid_size': st.session_state.get('grid_size', 20)
                        }
                    elif vis_name == 'quantum_foam_3d':
                        params = {
                            'amplitude': st.session_state.get('amplitude', 0.5),
                            'frequency': st.session_state.get('frequency', 2.0),
                            'grid_size': st.session_state.get('grid_size', 20)
                        }
                    elif vis_name == 'extra_dimensions_3d':
                        params = {
                            'num_dimensions': st.session_state.get('num_dimensions', 10),
                            'grid_size': st.session_state.get('grid_size', 20)
                        }
                    elif vis_name == '4d_higgs_field':
                        params = {
                            'grid_size': st.session_state.get('grid_size', 30)
                        }
                    elif vis_name == 'gauge_field_4d':
                        params = {
                            'grid_size': st.session_state.get('grid_size', 10)
                        }

                    # Generate and save the visualization
                    generate_visualization(vis_name, params)
            else:
                # Generate static visualization
                generate_visualization(vis_name)

        with viz_tab2:
            st.header("Advanced 4D Visualizations")
            st.markdown("""
            These advanced visualizations represent 4-dimensional concepts in physics,
            showing how we can represent higher dimensions through various techniques.
            """)

            # Create a selection for different 4D visualizations
            advanced_vis = st.selectbox(
                "Select a 4D visualization",
                ["4D Hypercube Projection", "4D Quantum Field", "4D Spacetime Evolution"]
            )

            # Check if the visualization files exist, otherwise offer to create them
            if advanced_vis == "4D Hypercube Projection":
                file_path = "gfx/4d/4d_hypercube_projection.png"
                if os.path.exists(file_path):
                    st.image(file_path, caption="4D Hypercube Projection")
                    st.markdown("""
                    This visualization shows a projection of a 4D hypercube (tesseract) into 3D space.
                    The fourth dimension is represented through perspective projection.
                    """)
                else:
                    st.warning("Visualization not found. Click the button below to generate it.")
                    if st.button("Generate 4D Hypercube Projection"):
                        with st.spinner("Generating visualization..."):
                            try:
                                from create_4d_vis import create_4d_projection
                                file_path = create_4d_projection()
                                st.success(f"Visualization created: {file_path}")
                                st.image(file_path, caption="4D Hypercube Projection")
                            except Exception as e:
                                st.error(f"Error generating visualization: {str(e)}")

            elif advanced_vis == "4D Quantum Field":
                file_path = "gfx/4d/4d_quantum_field.png"
                if os.path.exists(file_path):
                    st.image(file_path, caption="4D Quantum Field")
                    st.markdown("""
                    This visualization shows a 4D quantum field represented as multiple 3D slices at different
                    values of the fourth dimension (W). Each slice shows how the field varies in 3D space
                    at a specific point in the fourth dimension.
                    """)
                else:
                    st.warning("Visualization not found. Click the button below to generate it.")
                    if st.button("Generate 4D Quantum Field"):
                        with st.spinner("Generating visualization..."):
                            try:
                                from create_4d_vis import create_4d_quantum_field
                                file_path = create_4d_quantum_field()
                                st.success(f"Visualization created: {file_path}")
                                st.image(file_path, caption="4D Quantum Field")
                            except Exception as e:
                                st.error(f"Error generating visualization: {str(e)}")

            elif advanced_vis == "4D Spacetime Evolution":
                file_path = "gfx/4d/4d_spacetime_evolution.gif"
                if os.path.exists(file_path):
                    st.image(file_path, caption="4D Spacetime Evolution")
                    st.markdown("""
                    This animation shows the evolution of spacetime in 4D, where the fourth dimension is time.
                    The surface represents a slice of spacetime that evolves over time, showing how gravitational
                    waves propagate through spacetime.
                    """)
                else:
                    st.warning("Animation not found. Click the button below to generate it.")
                    if st.button("Generate 4D Spacetime Evolution"):
                        with st.spinner("Generating animation (this may take a minute)..."):
                            try:
                                from create_4d_vis import create_4d_animation
                                file_path = create_4d_animation()
                                st.success(f"Animation created: {file_path}")
                                st.image(file_path, caption="4D Spacetime Evolution")
                            except Exception as e:
                                st.error(f"Error generating animation: {str(e)}")

    # Documentation page
    elif page == "Documentation":
        st.title("📚 Theory of Everything Documentation")

        # Select formula for documentation
        formulas = api.list_formulas()
        formula_name = st.selectbox("Select a formula", list(formulas.keys()))

        # Documentation options
        include_components = st.checkbox("Include components", value=True)
        include_visualizations = st.checkbox("Include visualizations", value=True)

        # Generate documentation
        if st.button("Generate Documentation"):
            with st.spinner("Generating documentation..."):
                latex_file, pdf_file = generate_latex_pdf(
                    formula_name,
                    include_components=include_components,
                    include_visualizations=include_visualizations
                )

                if latex_file and pdf_file:
                    st.success(f"LaTeX file saved to: {latex_file}")
                    st.success(f"PDF file saved to: {pdf_file}")

                    # Display PDF if available
                    if os.path.exists(pdf_file):
                        with open(pdf_file, "rb") as f:
                            pdf_bytes = f.read()

                        st.download_button(
                            label="Download PDF",
                            data=pdf_bytes,
                            file_name=f"{formula_name}.pdf",
                            mime="application/pdf"
                        )

                        # Display PDF in an iframe
                        pdf_display = f'<iframe src="data:application/pdf;base64,{base64.b64encode(pdf_bytes).decode()}" width="700" height="1000" type="application/pdf"></iframe>'
                        st.markdown(pdf_display, unsafe_allow_html=True)

    # About page
    elif page == "About":
        st.title("ℹ️ About the Theory of Everything")
        st.markdown("""
        ## Theory of Everything (ToE)

        The Theory of Everything is a unified framework for physics that combines various physical theories
        into a single model. It aims to provide a comprehensive explanation of all physical phenomena,
        from the smallest subatomic particles to the largest cosmic structures.

        ### Components

        The Theory of Everything consists of several key components:

        - **Gravity Action**: Einstein-Hilbert action and extensions
        - **Matter Action**: Fermion fields and Higgs field
        - **Gauge Action**: Yang-Mills action and supersymmetric gauge fields
        - **Quantum Corrections**: Path integral formulation and loop corrections
        - **Unified Action**: Combined action for the Theory of Everything

        ### Theoretical Implications

        The Theory of Everything has several profound implications:

        - **Unified Physical Laws**: All forces and matter fields are combined into a single framework
        - **Quantum Gravity**: Spacetime is quantized and emergent from more fundamental structures
        - **Supersymmetry**: A fundamental symmetry balances matter and force particles
        - **Dark Matter/Energy**: Quantum spacetime fluctuations and supersymmetric particles provide natural explanations
        - **Origin of the Universe**: The unified framework provides a mathematical basis for understanding cosmic origins

        ### Project Structure

        This project is organized into a modular structure:

        - **Core**: Core functionality used by all other modules
        - **Formulas**: Tools for working with mathematical formulas
        - **Visualization**: Tools for generating visualizations
        - **Agents**: Specialized agents for generating documentation

        ### Credits

        This project was developed by Professor Codephreak.
        """)

# Run the application
if __name__ == "__main__":
    main()

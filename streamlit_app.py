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

# Formal presentation content (single source of truth for the master
# equation, glossary, and propositions). Pure strings: cheap to import.
from toe_math import master_equation as master_eq

try:
    from version import VERSION
except ImportError:
    VERSION = "2.0.0"

# ---------------------------------------------------------------------------
# Boot-speed strategy: heavy libraries (matplotlib, plotly, sympy via the
# unified API) are imported lazily inside cached getters, so the landing
# page paints before any of them load and each page pays only for what it
# uses. Figure builders are cached so revisiting a page is instant.
# ---------------------------------------------------------------------------


@st.cache_resource(show_spinner=False)
def get_p4d():
    """Lazy, cached import of the Plotly 4D module (pulls in plotly)."""
    try:
        from visualization import plotly_4d
        return plotly_4d
    except ImportError:
        return None


def plotly_available():
    return get_p4d() is not None


@st.cache_resource(show_spinner="Loading formula engine…")
def get_api():
    """Lazy, cached construction of the unified API (pulls in sympy)."""
    from unified.toe_unified import ToEUnified
    return ToEUnified(output_dir="gfx")


@st.cache_data(show_spinner=False)
def cached_fig(name, **params):
    """Build a Plotly figure by name with caching (pickled by Streamlit,
    so repeat visits and unchanged sliders cost nothing)."""
    p4d = get_p4d()
    return getattr(p4d, name)(**params)


@st.cache_data(show_spinner=False)
def cached_rg(models, loops, m_susy):
    """RG running results + figure, cached per control setting."""
    from toe_math import rg_running as rg
    fig = rg.make_rg_figure_plotly(models=models, loops=loops,
                                   m_susy=m_susy)
    results = {}
    for model in models:
        mu, a_inv = rg.run_couplings(model=model, loops=loops,
                                     m_susy=m_susy)
        uni = rg.find_unification(mu, a_inv)
        tau = None
        if uni["M_GUT"] is not None:
            tau = rg.proton_lifetime_years(uni["M_GUT"],
                                           1.0 / uni["alpha_gut_inv"])
        results[model] = {**uni, "tau_p": tau}
    return fig, results

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
    from unified.toe_vis import VisualizationTools
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

def read_doc(name):
    """Read a markdown document from docs/, returning None if missing."""
    path = os.path.join("docs", name)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return f.read()
    return None


def create_interactive_visualization_plotly(vis_name):
    """Interactive Plotly visualization with parameter controls."""
    p4d = get_p4d()
    if vis_name == '4d_spacetime_curvature':
        mass = st.slider("Mass (solar masses)", 0.1, 10.0, 1.0, 0.1)
        grid = st.slider("Grid size", 10, 80, 40, 5)
        return p4d.spacetime_curvature_figure(mass=mass, grid=grid)
    elif vis_name == 'quantum_foam_3d':
        amplitude = st.slider("Amplitude", 0.1, 1.0, 0.5, 0.1)
        frequency = st.slider("Frequency", 0.5, 5.0, 2.0, 0.1)
        grid = st.slider("Grid size", 10, 80, 40, 5)
        return p4d.quantum_foam_figure(amplitude=amplitude,
                                       frequency=frequency, grid=grid)
    elif vis_name == 'extra_dimensions_3d':
        num_dimensions = st.slider("Number of dimensions", 4, 11, 10, 1)
        grid = st.slider("Grid size", 20, 100, 60, 5)
        return p4d.extra_dimensions_figure(num_dimensions=num_dimensions,
                                           grid=grid)
    elif vis_name == '4d_higgs_field':
        grid = st.slider("Grid size", 20, 100, 60, 5)
        return p4d.higgs_potential_figure(grid=grid)
    elif vis_name == 'gauge_field_4d':
        grid = st.slider("Grid size", 5, 12, 8, 1)
        return p4d.gauge_field_figure(grid=grid)
    return None


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
    import matplotlib.pyplot as plt
    from matplotlib import cm
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
    import matplotlib.pyplot as plt
    from matplotlib import cm
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
    import matplotlib.pyplot as plt
    from matplotlib import cm
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
    import matplotlib.pyplot as plt
    from matplotlib import cm
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
    import matplotlib.pyplot as plt
    from matplotlib import cm
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

    # Heavy resources are resolved lazily per page (see cached getters
    # at the top of this file).
    PLOTLY_AVAILABLE = plotly_available()
    p4d = get_p4d()

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

    # Navigation (key="page" lets the Home mission cards switch pages)
    page = st.sidebar.selectbox(
        "Navigation",
        ["Home", "Master Equation", "Gauge Unification (RG)", "Formulas",
         "Visualizations", "Documentation", "Conclusion & Assessment",
         "References & About"],
        key="page",
    )

    st.sidebar.caption(
        f"v{VERSION} — Streamlit delivery. Also available: the panel "
        "dashboard (`python3 dash_app.py`) and the Control Room "
        "(`python3 nicegui_app.py`).")

    if not PLOTLY_AVAILABLE:
        st.sidebar.warning("Plotly is not installed; interactive "
                           "visualizations are degraded. Run "
                           "`pip install plotly kaleido`.")

    # Home page — fast-painting animated landing with mission cards.
    # Everything above the fold is CSS/HTML and pre-rendered GIFs: no
    # physics or plotting library loads until a card is clicked.
    if page == "Home":
        st.markdown("""
        <style>
        @keyframes drift { from {background-position: 0 0;}
                           to {background-position: -900px 450px;} }
        @keyframes glow { 0%,100% {text-shadow: 0 0 18px #58a6ff66;}
                          50% {text-shadow: 0 0 34px #58a6ffcc;} }
        @keyframes rise { from {opacity:0; transform:translateY(14px);}
                          to {opacity:1; transform:translateY(0);} }
        .hero {
          position: relative; border-radius: 14px; overflow: hidden;
          padding: 2.6rem 2.4rem 2.2rem; margin-bottom: 1rem;
          background:
            radial-gradient(1.5px 1.5px at 40px 60px, #fff8, transparent),
            radial-gradient(1px 1px at 190px 120px, #fff5, transparent),
            radial-gradient(1.5px 1.5px at 320px 40px, #fff7, transparent),
            radial-gradient(1px 1px at 460px 160px, #fff4, transparent),
            radial-gradient(1.5px 1.5px at 610px 90px, #fff6, transparent),
            radial-gradient(1px 1px at 750px 30px, #fff5, transparent),
            linear-gradient(125deg, #0d1117 0%, #11192c 45%, #1a1033 100%);
          background-size: 900px 450px, 900px 450px, 900px 450px,
            900px 450px, 900px 450px, 900px 450px, cover;
          animation: drift 70s linear infinite;
          border: 1px solid #30363d;
        }
        .hero h1 {
          margin: 0 0 0.4rem; font-size: 2.1rem; color: #e6edf3;
          animation: glow 4.5s ease-in-out infinite;
        }
        .hero .eq {
          font-family: Georgia, 'Times New Roman', serif;
          font-size: 1.45rem; color: #79b8ff; letter-spacing: 1px;
          margin: 0.6rem 0 0.9rem; animation: rise 0.9s ease-out;
        }
        .hero p { color: #9aa4b2; max-width: 46rem; margin: 0;
                  animation: rise 1.2s ease-out; }
        .statline { display: flex; gap: 0.6rem; flex-wrap: wrap;
                    margin-top: 1.1rem; animation: rise 1.5s ease-out; }
        .stat {
          padding: 0.32rem 0.85rem; border-radius: 999px;
          font-size: 0.82rem; font-weight: 600;
          border: 1px solid #58a6ff55; color: #79b8ff;
          background: #58a6ff14; transition: all 0.25s ease;
        }
        .stat:hover { background: #58a6ff33; transform: translateY(-2px);
                      box-shadow: 0 4px 16px #58a6ff33; }
        .stat.ok { border-color: #3fb95055; color: #56d364;
                   background: #3fb95014; }
        .stat.ok:hover { background: #3fb95033;
                         box-shadow: 0 4px 16px #3fb95033; }
        /* mission cards: lift, glow, and animate the arrow on hover */
        div[data-testid="stButton"] > button {
          width: 100%; text-align: left; white-space: pre-line;
          border: 1px solid #30363d; border-radius: 12px;
          padding: 0.9rem 1rem; min-height: 7.2rem;
          background: #161b22; transition: all 0.22s ease;
        }
        div[data-testid="stButton"] > button:hover {
          transform: translateY(-4px); border-color: #58a6ff;
          box-shadow: 0 10px 28px #0009, 0 0 18px #58a6ff22;
        }
        div[data-testid="stButton"] > button:active {
          transform: translateY(-1px) scale(0.99);
        }
        </style>
        <div class="hero">
          <h1>Theory of Everything Explorer</h1>
          <div class="eq">S = S<sub>gravity</sub> + S<sub>matter</sub> +
            S<sub>gauge</sub> + S<sub>quantum</sub></div>
          <p>A pedagogical and computational framework for the composite
          action of fundamental physics. Not a theory of everything —
          and honest about it. The parts that can be computed are
          computed, live, on every page.</p>
          <div class="statline">
            <span class="stat ok">MSSM unification · 0.7% @ 2 loops</span>
            <span class="stat">M<sub>GUT</sub> ≈ 1.3×10¹⁶ GeV</span>
            <span class="stat ok">τ<sub>p</sub> ≈ 10³⁵·⁷ yr &gt; Super-K</span>
            <span class="stat">SM near-miss · 11.5%</span>
            <span class="stat">Λ = 1.1056×10⁻⁵² m⁻²</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Mission cards — click to jump straight into a page
        def _goto(target):
            st.session_state.page = target

        st.markdown("##### Choose your mission")
        cards = [
            ("🧭  Master Equation",
             "The composite action as a formal Definition —\n"
             "full aligned display and an 18-symbol glossary",
             "Master Equation"),
            ("⚡  Run the Unification",
             "Drive the RG running yourself: SM vs MSSM,\n"
             "1–2 loops, SUSY threshold, Super-K verdict",
             "Gauge Unification (RG)"),
            ("🔮  Enter the 4th Dimension",
             "Tesseract projection, hyperplane slicing,\n"
             "animated spacetime — all interactive",
             "Visualizations"),
            ("📐  Formula Catalog",
             "Every sector action with LaTeX rendering\n"
             "and component exploration",
             "Formulas"),
            ("⚖️  The Honest Verdict",
             "What this is, what it is not, and the\n"
             "independent evaluation, point by point",
             "Conclusion & Assessment"),
            ("📚  Documentation & Paper",
             "Formal docs, references, and the compiled\n"
             "LaTeX paper",
             "Documentation"),
        ]
        for row_start in (0, 3):
            cols = st.columns(3)
            for col, (title, blurb, target) in zip(
                    cols, cards[row_start:row_start + 3]):
                with col:
                    st.button(f"{title}\n\n{blurb}",
                              key=f"card-{target}",
                              on_click=_goto, args=(target,),
                              use_container_width=True)

        # A taste of the 4th dimension — pre-rendered, instant to serve
        st.markdown("##### The fourth dimension, three ways")
        g1, g2, g3 = st.columns(3)
        galleries = [
            (g1, "gfx/4d/tesseract_rotation.gif",
             "Projection: tesseract under double rotation"),
            (g2, "gfx/4d/clifford_torus.gif",
             "Stereographic: Clifford torus turning inside out"),
            (g3, "gfx/4d/field_w_sweep.gif",
             "Slicing: a field swept through w"),
        ]
        for col, path, caption in galleries:
            with col:
                if os.path.exists(path):
                    st.image(path, caption=caption,
                             use_container_width=True)

        with st.expander("Live demo: spacetime curvature near a point "
                         "mass (loads the plotting engine)"):
            if PLOTLY_AVAILABLE:
                st.plotly_chart(cached_fig("spacetime_curvature_figure"),
                                use_container_width=True)
            else:
                st.pyplot(create_spacetime_curvature_vis())

    # Master Equation page
    elif page == "Master Equation":
        st.title("The Composite Action")

        st.latex(master_eq.MASTER_EQUATION_ALIGNED)

        st.markdown(master_eq.DEFINITION_TEXT)
        st.warning(master_eq.WHAT_IT_IS_NOT)

        st.subheader("Symbol glossary")
        glossary_md = "| Symbol | Meaning | Units / value | Appears in |\n"
        glossary_md += "|---|---|---|---|\n"
        for entry in master_eq.GLOSSARY:
            glossary_md += (f"| {entry['symbol']} | {entry['name']} "
                            f"| {entry['units']} | {entry['appears']} |\n")
        st.markdown(glossary_md)

        st.subheader("The sectors, one by one")
        with st.expander("Gravity sector (Einstein–Hilbert) — and Remark 1"):
            st.latex(master_eq.MASTER_EQUATION_LINES[1])
            st.markdown(master_eq.REMARK_GRAVITY_PROGRAMS)
        with st.expander("Matter sector (Dirac + Higgs)"):
            st.latex(master_eq.MASTER_EQUATION_LINES[2])
            st.latex(master_eq.HIGGS_POTENTIAL)
            st.markdown("Fermions and the Higgs doublet, minimally coupled "
                        "to gravity through $\\sqrt{-g}$ and to the gauge "
                        "fields through the covariant derivative $D_\\mu$.")
        with st.expander("Gauge sector (Yang–Mills)"):
            st.latex(master_eq.MASTER_EQUATION_LINES[3])
            st.latex(master_eq.FIELD_STRENGTH)
            st.markdown("The Standard Model gauge group is "
                        "$SU(3)_c \\times SU(2)_L \\times U(1)_Y$. The "
                        "*unifying* group an actual GUT requires is the "
                        "subject of the **Gauge Unification (RG)** page.")
        with st.expander("Quantum sector (loop expansion)"):
            st.latex(master_eq.MASTER_EQUATION_LINES[4])
            st.markdown("The organizing statement of perturbative quantum "
                        "corrections. It presupposes a perturbatively "
                        "consistent theory — precisely what the gravity "
                        "sector lacks (Goroff–Sagnotti 1986); see Open "
                        "Problem 3 in docs/THEORY.md.")

        st.subheader("Propositions (computed, not asserted)")
        st.markdown(master_eq.PROPOSITION_RG)

    # Gauge Unification page
    elif page == "Gauge Unification (RG)":
        st.title("Gauge-Coupling Unification")
        st.markdown("""
        The quantitative centerpiece of this project: a from-scratch
        reproduction of the renormalization-group analysis showing the
        Standard Model couplings *nearly* meet, while their MSSM
        counterparts *unify*. Every number on this page is computed live by
        `toe_math/rg_running.py` (reproduce offline with
        `python3 -m toe_math.rg_running`).
        """)

        from toe_math import rg_running as rg

        col1, col2, col3 = st.columns(3)
        with col1:
            loops = st.radio("Loop order", [1, 2], index=1, horizontal=True)
        with col2:
            m_susy = st.select_slider(
                "SUSY threshold m_SUSY [GeV]",
                options=[300, 500, 750, 1000, 1500, 2000, 3000, 5000, 10000],
                value=1000)
        with col3:
            show = st.multiselect("Models", ["SM", "MSSM"],
                                  default=["SM", "MSSM"])

        results = {}
        if show:
            fig, results = cached_rg(tuple(show), loops, float(m_susy))
            st.plotly_chart(fig, use_container_width=True)

        for model in show:
            uni = results[model]
            st.subheader(f"{model} ({loops}-loop)")
            c1, c2, c3, c4 = st.columns(4)
            if uni["M_GUT"] is not None:
                c1.metric("M_GUT (geometric mean)", f"{uni['M_GUT']:.2e} GeV")
                c2.metric("α_GUT⁻¹", f"{uni['alpha_gut_inv']:.1f}")
                c3.metric("Mismatch at crossing",
                          f"{100 * uni['mismatch']:.1f}%")
                tau = uni["tau_p"]
                c4.metric("τ_p estimate", f"{tau:.1e} yr")
                if uni["unifies"]:
                    verdict = (f"Couplings unify (mismatch "
                               f"{100 * uni['mismatch']:.1f}% < 3%). ")
                    if tau > rg.SUPERK_TAU_P_BOUND_YR:
                        st.success(verdict + f"The proton-lifetime estimate "
                                   f"{tau:.1e} yr is above the "
                                   f"Super-Kamiokande bound "
                                   f"{rg.SUPERK_TAU_P_BOUND_YR:.1e} yr — "
                                   "not excluded.")
                    else:
                        st.error(verdict + f"But τ_p ≈ {tau:.1e} yr violates "
                                 f"the Super-K bound "
                                 f"{rg.SUPERK_TAU_P_BOUND_YR:.1e} yr — this "
                                 "scenario is excluded.")
                else:
                    st.error(f"No unification: α₃⁻¹ misses the α₁ = α₂ "
                             f"crossing by {100 * uni['mismatch']:.1f}%. "
                             f"The implied scale would give τ_p ≈ {tau:.1e} "
                             "yr — excluded by Super-Kamiokande "
                             "(the classic demise of minimal non-SUSY "
                             "SU(5)).")
        st.caption("τ_p ~ M_GUT⁴/(α_GUT² m_p⁵) is a dimensional-analysis "
                   "estimate, uncertain by 1–2 orders of magnitude from "
                   "hadronic matrix elements; comparisons are "
                   "order-of-magnitude only. Yukawa contributions to the "
                   "2-loop running are neglected.")

        with st.expander("Where does the 5/3 in α₁ come from? "
                         "(SU(5)/SO(10) embedding)"):
            from toe_math import gut_embedding as gut
            st.markdown("One Standard Model generation fits exactly into "
                        "$\\bar{\\mathbf{5}} \\oplus \\mathbf{10}$ of "
                        "SU(5):")
            st.markdown(gut.assignment_table_markdown())
            s = gut.summary()
            st.markdown(
                f"From this table, $\\mathrm{{Tr}}(Y^2) = {s['tr_Y2']}$ "
                f"over a generation while $\\mathrm{{Tr}}(T_3^2) = 2$, "
                f"forcing the normalization $\\alpha_1 = "
                f"\\tfrac{{{s['normalization_factor'].numerator}}}"
                f"{{{s['normalization_factor'].denominator}}}\\,"
                "\\alpha_Y$ used above — derived, not assumed. All four "
                "gauge-anomaly sums vanish: "
                f"$\\sum Y = {s['anomalies']['sum_Y']}$, "
                f"$\\sum Y^3 = {s['anomalies']['sum_Y3']}$, "
                f"$SU(3)^2$–$Y = {s['anomalies']['su3_su3_Y']}$, "
                f"$SU(2)^2$–$Y = {s['anomalies']['su2_su2_Y']}$. "
                "In SO(10) the spinor branches as $\\mathbf{16} = "
                "\\mathbf{10} \\oplus \\bar{\\mathbf{5}} \\oplus "
                "\\mathbf{1}$ — the singlet is the right-handed neutrino. "
                "Reproduce with `python3 -m toe_math.gut_embedding`; "
                "details in docs/GUT_EMBEDDING.md.")

    # Formulas page
    elif page == "Formulas":
        api = get_api()
        st.title("Formula Catalog")
        st.caption("Transcriptions of established sector actions; see the "
                   "Master Equation page for the formal presentation and "
                   "docs/THEORY.md for sources.")

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
        st.title("Visualizations")

        # Create tabs for different visualization types
        viz_tab1, viz_tab2 = st.tabs(["Standard Visualizations", "Advanced 4D Visualizations"])

        with viz_tab1:
            # List available visualizations
            api = get_api()
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
            if PLOTLY_AVAILABLE:
                fig = create_interactive_visualization_plotly(vis_name)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                    if st.button("Export as standalone HTML"):
                        os.makedirs("gfx/html", exist_ok=True)
                        html_path = f"gfx/html/{vis_name}.html"
                        fig.write_html(html_path)
                        st.success(f"Saved interactive figure to {html_path}")
                else:
                    generate_visualization(vis_name)
            else:
                fig = create_interactive_visualization(vis_name)
                if fig:
                    st.pyplot(fig)
                else:
                    generate_visualization(vis_name)

        with viz_tab2:
            st.header("Advanced 4D Visualizations")
            st.markdown("""
            Two honest techniques display four dimensions on a screen:
            **projection** (rotate in 4-space, then perspective-project to
            3D, exactly as 3D is projected to your 2D screen) and
            **slicing** (intersect with a hyperplane $w = $ const and sweep
            $w$). Each figure states which technique it uses. All are fully
            interactive: drag to rotate, scroll to zoom, press Play to
            animate.
            """)

            if not PLOTLY_AVAILABLE:
                st.error("These interactive figures require Plotly: "
                         "`pip install plotly kaleido`.")
            else:
                advanced_vis = st.selectbox(
                    "Select a 4D visualization",
                    ["4D Hypercube (projection)",
                     "4D Hypercube (slicing)",
                     "4D Quantum Field (slicing)",
                     "4D Spacetime Evolution (time animation)"]
                )

                if advanced_vis == "4D Hypercube (projection)":
                    st.plotly_chart(cached_fig("tesseract_figure"),
                                    use_container_width=True)
                    st.markdown("""
                    The 16 vertices and 32 edges of the tesseract
                    $\\{-1,1\\}^4$ under a *double rotation* (simultaneous
                    rotations in the $(x,w)$ and $(y,w)$ planes — a motion
                    with no 3D analogue), perspective-projected to 3D with
                    scale $d/(d-w)$. Vertex color encodes the 4th
                    coordinate $w$: the apparent "inner" and "outer" cubes
                    swap as the rotation carries vertices through $w$.
                    """)

                elif advanced_vis == "4D Hypercube (slicing)":
                    w = st.slider("Hyperplane position w", -1.5, 1.5, 0.0,
                                  0.05)
                    st.plotly_chart(cached_fig("tesseract_slice_figure", w=w),
                                    use_container_width=True)
                    st.markdown("""
                    The 3D cross-section of the tesseract with the
                    hyperplane $w = $ const. Because the tesseract is a
                    cube $\\times$ interval, every slice with $|w| \\le 1$
                    is the same unit cube, and the slice vanishes abruptly
                    at $|w| = 1$ — the 4D analogue of slicing a cube into
                    squares. Sweep the slider to *feel* the 4th dimension
                    as the sweep parameter.
                    """)

                elif advanced_vis == "4D Quantum Field (slicing)":
                    st.plotly_chart(cached_fig("quantum_field_4d_figure"),
                                    use_container_width=True)
                    st.markdown("""
                    A scalar field $f(x, y; w)$ on four coordinates,
                    displayed one hyperplane $w = $ const at a time. The
                    animation sweeps $w$, so the surface you see morphs as
                    the slice moves through the 4th dimension — each frame
                    is genuinely a different 4D location, not a camera
                    move.
                    """)

                else:  # 4D Spacetime Evolution
                    st.plotly_chart(cached_fig("spacetime_evolution_figure"),
                                    use_container_width=True)
                    st.markdown("""
                    Here the 4th coordinate is *time*: a curvature ripple
                    $h(x, y; t)$ propagates outward as the animation plays.
                    The camera is yours — rotate and zoom while it runs
                    (this replaces the old pre-rendered GIF whose viewpoint
                    was baked in).
                    """)

    # Documentation page
    elif page == "Documentation":
        st.title("Documentation")

        st.markdown("""
        The canonical documents (in `docs/`):

        | Document | Content |
        |---|---|
        | `THEORY.md` | Formal apparatus: Definitions, Remark on the gravity sector, Propositions, Open Problems |
        | `RG_UNIFICATION.md` | Methods and results of the gauge-coupling analysis |
        | `GUT_EMBEDDING.md` | SU(5)/SO(10) embedding, normalization, anomaly arithmetic |
        | `CONCLUSION.md` | Honest assessment (rendered on the Conclusion & Assessment page) |
        | `REFERENCES.md` | Bibliography (rendered on the References & About page) |
        | `USER_GUIDE.md` | Install, run, reproduce, build the paper |
        """)

        paper_pdf = os.path.join("paper", "gutoe.pdf")
        if os.path.exists(paper_pdf):
            with open(paper_pdf, "rb") as f:
                st.download_button(
                    label="Download the compiled paper (paper/gutoe.pdf)",
                    data=f.read(), file_name="gutoe.pdf",
                    mime="application/pdf")
        else:
            st.info("The typeset paper has not been built yet; run "
                    "`bash paper/build.sh` (requires LaTeX).")

        st.subheader("Per-formula LaTeX/PDF generation (legacy tooling)")

        # Select formula for documentation
        api = get_api()
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

    # Conclusion & Assessment page
    elif page == "Conclusion & Assessment":
        st.title("Conclusion & Assessment")
        conclusion = read_doc("CONCLUSION.md")
        if conclusion:
            st.markdown(conclusion)
        else:
            st.error("docs/CONCLUSION.md not found.")

    # References & About page
    elif page == "References & About":
        st.title("References & About")

        st.markdown("""
        ## About this project

        A pedagogical and computational framework that organizes the
        standard actions of fundamental physics, reproduces the classic
        gauge-coupling-unification computation, and presents the result —
        and its limits — with formal apparatus and citations. It does not
        claim to be, or to contain, a theory of everything; see the
        Conclusion & Assessment page.

        The project's structure follows an independent academic evaluation
        (PDF in the repository root) whose findings are addressed
        point-by-point in `docs/CONCLUSION.md`.

        ### Components

        - **Physics computations** (`toe_math/`): RG running and
          unification, SU(5)/SO(10) embedding, the formal master-equation
          presentation
        - **Interactive visualization** (`visualization/plotly_4d.py`):
          genuine 4D techniques (projection and slicing)
        - **Formula catalog** (`unified/`, `component_formulas/`):
          transcriptions of the established sector actions
        - **Documents** (`docs/`, `paper/`): the formal presentation and
          the compiled paper

        ### Credits

        Developed by Professor Codephreak (an AI-assisted project of
        Gregory L. Magnusson). Restructured in 2026 in response to the
        independent academic evaluation. The pre-2026 documentation is
        preserved in `docs/legacy/`.
        """)

        st.markdown("---")
        references = read_doc("REFERENCES.md")
        if references:
            st.markdown(references)
        else:
            st.error("docs/REFERENCES.md not found.")

# Run the application
if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Interactive Plotly visualizations, including genuine 4D techniques.

This module supplies the interactive (rotatable, zoomable, animated)
counterparts of the project's static matplotlib figures. Two honest
techniques are used to display four-dimensional objects on a screen:

* **Projection** -- a 4D object is rotated in 4-space (here, simultaneous
  rotations in the (x,w) and (y,w) planes) and then projected to 3D with
  a perspective map  p = d / (d - w), exactly as a 3D object is projected
  to a 2D screen. Used for the tesseract.
* **Slicing** -- a 4D object or field is intersected with the hyperplane
  w = const; sweeping the slice through w reveals the 4th dimension as an
  animation parameter. Used for the tesseract cross-section and the 4D
  scalar field.

Every figure states which technique it uses in its title/caption metadata
so the display never overstates what is being shown.

All functions return plotly.graph_objects.Figure and are safe to call in
or out of Streamlit.
"""

import numpy as np
import plotly.graph_objects as go

# --------------------------------------------------------------------------
# Tesseract (4D hypercube): vertices and edges
# --------------------------------------------------------------------------

def _tesseract_vertices():
    """The 16 vertices of {-1, 1}^4, shape (16, 4)."""
    verts = np.array([[(i >> k) & 1 for k in range(4)] for i in range(16)],
                     dtype=float)
    return 2.0 * verts - 1.0


def _tesseract_edges(verts):
    """Pairs of vertex indices at Hamming distance 1 (32 edges)."""
    edges = []
    n = len(verts)
    for i in range(n):
        for j in range(i + 1, n):
            if np.sum(np.abs(verts[i] - verts[j])) == 2.0:
                edges.append((i, j))
    return edges


def _rotate_4d(verts, theta):
    """Simultaneous (double) rotation in the (x,w) and (y,w) planes."""
    c, s = np.cos(theta), np.sin(theta)
    rot_xw = np.eye(4)
    rot_xw[0, 0], rot_xw[0, 3] = c, -s
    rot_xw[3, 0], rot_xw[3, 3] = s, c
    rot_yw = np.eye(4)
    rot_yw[1, 1], rot_yw[1, 3] = c, -s
    rot_yw[3, 1], rot_yw[3, 3] = s, c
    return verts @ rot_xw.T @ rot_yw.T


def _project_to_3d(verts4, d=3.0):
    """Perspective projection R^4 -> R^3: scale by d / (d - w)."""
    w = verts4[:, 3]
    scale = d / (d - w)
    return verts4[:, :3] * scale[:, None], w


def _edge_trace(verts3, edges):
    """None-separated Scatter3d line segments for the edge set."""
    xs, ys, zs = [], [], []
    for i, j in edges:
        xs += [verts3[i, 0], verts3[j, 0], None]
        ys += [verts3[i, 1], verts3[j, 1], None]
        zs += [verts3[i, 2], verts3[j, 2], None]
    line = dict(color="#4c78a8", width=4)
    return go.Scatter3d(x=xs, y=ys, z=zs, mode="lines", line=line,
                        hoverinfo="skip", showlegend=False)


def tesseract_figure(n_frames=60, d=3.0):
    """Animated double rotation of a tesseract, perspective-projected to 3D.

    Technique: 4D rotation + perspective projection (w -> point size/color).
    """
    verts = _tesseract_vertices()
    edges = _tesseract_edges(verts)
    thetas = np.linspace(0, 2 * np.pi, n_frames, endpoint=False)

    def traces(theta):
        v4 = _rotate_4d(verts, theta)
        v3, w = _project_to_3d(v4, d=d)
        edge = _edge_trace(v3, edges)
        marker = dict(size=6, color=w, colorscale="Viridis", cmin=-1.8,
                      cmax=1.8, colorbar=dict(title="w (4th coord)"))
        pts = go.Scatter3d(x=v3[:, 0], y=v3[:, 1], z=v3[:, 2],
                           mode="markers", marker=marker,
                           hovertemplate="w = %{marker.color:.2f}"
                                         "<extra>vertex</extra>",
                           showlegend=False)
        return [edge, pts]

    frames = [go.Frame(data=traces(th), name=f"{i}")
              for i, th in enumerate(thetas)]
    fig = go.Figure(data=traces(thetas[0]), frames=frames)

    fig.update_layout(
        title=("Tesseract (4D hypercube) under double rotation, "
               "perspective-projected to 3D — vertex color = 4th "
               "coordinate w"),
        scene=dict(
            xaxis_title="x", yaxis_title="y", zaxis_title="z",
            aspectmode="cube",
            xaxis=dict(range=[-2.5, 2.5]), yaxis=dict(range=[-2.5, 2.5]),
            zaxis=dict(range=[-2.5, 2.5])),
        height=620,
        updatemenus=[dict(
            type="buttons", showactive=False, y=0, x=0, xanchor="left",
            buttons=[
                dict(label="Play", method="animate",
                     args=[None, dict(frame=dict(duration=50, redraw=True),
                                      fromcurrent=True,
                                      transition=dict(duration=0))]),
                dict(label="Pause", method="animate",
                     args=[[None], dict(frame=dict(duration=0, redraw=False),
                                        mode="immediate")]),
            ])],
        sliders=[dict(
            currentvalue=dict(prefix="rotation step "),
            steps=[dict(method="animate", label=f"{i}",
                        args=[[f"{i}"],
                              dict(mode="immediate",
                                   frame=dict(duration=0, redraw=True),
                                   transition=dict(duration=0))])
                   for i in range(n_frames)])])
    return fig


def tesseract_slice_figure(w=0.0):
    """3D cross-section of the (unrotated) tesseract at hyperplane w=const.

    Technique: slicing. For |w| < 1 the section is the full unit cube; the
    edges of the tesseract that run along the w-axis pierce the hyperplane
    in 8 isolated points. Sweeping w moves the section through the solid.
    """
    fig = go.Figure()
    if abs(w) <= 1.0:
        cube3 = np.array([[x, y, z] for x in (-1, 1) for y in (-1, 1)
                          for z in (-1, 1)], dtype=float)
        edges = [(i, j) for i in range(8) for j in range(i + 1, 8)
                 if np.sum(np.abs(cube3[i] - cube3[j])) == 2.0]
        fig.add_trace(_edge_trace(cube3, edges))
        fig.add_trace(go.Scatter3d(
            x=cube3[:, 0], y=cube3[:, 1], z=cube3[:, 2], mode="markers",
            marker=dict(size=6, color="#d62728"), hoverinfo="skip",
            showlegend=False))
        note = (f"slice w = {w:+.2f}: the section is a cube "
                "(tesseract = cube × interval)")
    else:
        note = f"slice w = {w:+.2f}: outside the tesseract — empty section"
    fig.update_layout(
        title=f"Tesseract cross-section at w = {w:+.2f} — {note}",
        scene=dict(xaxis_title="x", yaxis_title="y", zaxis_title="z",
                   aspectmode="cube",
                   xaxis=dict(range=[-1.6, 1.6]),
                   yaxis=dict(range=[-1.6, 1.6]),
                   zaxis=dict(range=[-1.6, 1.6])),
        height=560)
    return fig


# --------------------------------------------------------------------------
# 4D scalar field: w-slice animation
# --------------------------------------------------------------------------

def quantum_field_4d_figure(grid=60, n_frames=30):
    """Scalar field f(x, y; w) displayed as a surface, animated over w.

    Technique: slicing — each frame is the field on the hyperplane
    w = const; the animation sweeps the 4th coordinate.
    """
    x = np.linspace(-3, 3, grid)
    y = np.linspace(-3, 3, grid)
    X, Y = np.meshgrid(x, y)
    ws = np.linspace(-2, 2, n_frames)

    def field(w):
        r2 = X**2 + Y**2
        return (np.exp(-0.3 * (r2 + w**2))
                * np.cos(2 * np.sqrt(r2 + w**2) - 1.5 * w)
                + 0.25 * np.exp(-0.5 * ((X - w)**2 + Y**2))
                * np.cos(3 * Y))

    zmax = 1.1
    frames = [go.Frame(
        data=[go.Surface(z=field(w), x=X, y=Y, colorscale="Viridis",
                         cmin=-zmax, cmax=zmax,
                         colorbar=dict(title="f(x,y;w)"))],
        name=f"{i}", layout=go.Layout(
            title=f"4D scalar field, slice w = {w:+.2f}"))
        for i, w in enumerate(ws)]
    fig = go.Figure(data=frames[0].data, frames=frames)
    fig.update_layout(
        title=f"4D scalar field, slice w = {ws[0]:+.2f}",
        scene=dict(xaxis_title="x", yaxis_title="y",
                   zaxis_title="f(x,y;w)", aspectmode="cube",
                   zaxis=dict(range=[-zmax, zmax])),
        height=620,
        updatemenus=[dict(
            type="buttons", showactive=False, y=0, x=0, xanchor="left",
            buttons=[
                dict(label="Play", method="animate",
                     args=[None, dict(frame=dict(duration=80, redraw=True),
                                      fromcurrent=True)]),
                dict(label="Pause", method="animate",
                     args=[[None], dict(frame=dict(duration=0, redraw=False),
                                        mode="immediate")])])],
        sliders=[dict(
            currentvalue=dict(prefix="w = "),
            steps=[dict(method="animate", label=f"{w:+.2f}",
                        args=[[f"{i}"],
                              dict(mode="immediate",
                                   frame=dict(duration=0, redraw=True))])
                   for i, w in enumerate(ws)])])
    return fig


# --------------------------------------------------------------------------
# Spacetime evolution: time animation of a propagating ripple
# --------------------------------------------------------------------------

def spacetime_evolution_figure(grid=70, n_frames=40):
    """Propagating curvature ripple h(x, y; t), animated over time.

    Technique: time is the 4th coordinate, displayed as animation. The
    interactive camera replaces the old pre-rendered GIF rotation.
    """
    x = np.linspace(-8, 8, grid)
    y = np.linspace(-8, 8, grid)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2) + 1e-9
    ts = np.linspace(0, 4 * np.pi, n_frames)

    def ripple(t):
        return np.sin(2.0 * R - t) / (1.0 + R)

    frames = [go.Frame(
        data=[go.Surface(z=ripple(t), x=X, y=Y, colorscale="RdBu",
                         cmin=-0.8, cmax=0.8,
                         colorbar=dict(title="h(x,y;t)"))],
        name=f"{i}")
        for i, t in enumerate(ts)]
    fig = go.Figure(data=frames[0].data, frames=frames)
    fig.update_layout(
        title="Spacetime ripple h(x, y; t) — time as the animation axis",
        scene=dict(xaxis_title="x", yaxis_title="y",
                   zaxis_title="amplitude", aspectmode="cube",
                   zaxis=dict(range=[-1, 1])),
        height=620,
        updatemenus=[dict(
            type="buttons", showactive=False, y=0, x=0, xanchor="left",
            buttons=[
                dict(label="Play", method="animate",
                     args=[None, dict(frame=dict(duration=60, redraw=True),
                                      fromcurrent=True)]),
                dict(label="Pause", method="animate",
                     args=[[None], dict(frame=dict(duration=0, redraw=False),
                                        mode="immediate")])])],
        sliders=[dict(
            currentvalue=dict(prefix="t = "),
            steps=[dict(method="animate", label=f"{t:.1f}",
                        args=[[f"{i}"],
                              dict(mode="immediate",
                                   frame=dict(duration=0, redraw=True))])
                   for i, t in enumerate(ts)])])
    return fig


# --------------------------------------------------------------------------
# Plotly counterparts of the in-app matplotlib visualizations
# --------------------------------------------------------------------------

def spacetime_curvature_figure(mass=1.0, grid=40):
    """Schwarzschild embedding-style curvature surface for a point mass."""
    x = np.linspace(-10, 10, grid)
    y = np.linspace(-10, 10, grid)
    X, Y = np.meshgrid(x, y)
    r = np.sqrt(X**2 + Y**2 + 0.1**2)
    c = 299792458.0
    G = 6.67430e-11
    M = mass * 1.989e30
    rs = 2 * G * M / c**2
    Z = -rs / (2 * r)
    fig = go.Figure(go.Surface(
        z=Z, x=X, y=Y, colorscale="Viridis",
        colorbar=dict(title="curvature ∝ −R_s/2r")))
    fig.update_layout(
        title=(f"Spacetime curvature around {mass:.1f} solar masses "
               f"(R_s = {rs:.2e} m; vertical axis schematic)"),
        scene=dict(xaxis_title="x", yaxis_title="y",
                   zaxis_title="curvature (schematic)",
                   aspectmode="cube"),
        height=560)
    return fig


def quantum_foam_figure(amplitude=0.5, frequency=2.0, grid=40, seed=42):
    """Multi-mode 'quantum foam' fluctuation surface (schematic)."""
    x = np.linspace(-5, 5, grid)
    y = np.linspace(-5, 5, grid)
    X, Y = np.meshgrid(x, y)
    rng = np.random.default_rng(seed)
    phases = 2 * np.pi * rng.random((3, 3))
    Z = np.zeros_like(X)
    for i in range(3):
        for j in range(3):
            Z += (amplitude / (i + j + 1)
                  * np.sin(frequency * (i + 1) * X + phases[i, j])
                  * np.sin(frequency * (j + 1) * Y + phases[i, j]))
    fig = go.Figure(go.Surface(z=Z, x=X, y=Y, colorscale="Viridis",
                               colorbar=dict(title="fluctuation")))
    fig.update_layout(
        title="Quantum foam (schematic multi-mode fluctuations)",
        scene=dict(xaxis_title="x", yaxis_title="y",
                   zaxis_title="amplitude", aspectmode="cube"),
        height=560)
    return fig


def extra_dimensions_figure(num_dimensions=10, grid=60):
    """Deformed sphere as a schematic of compactified extra dimensions."""
    theta = np.linspace(0, 2 * np.pi, grid)
    phi = np.linspace(0, np.pi, grid)
    theta, phi = np.meshgrid(theta, phi)
    bumps = max(num_dimensions - 3, 1)
    r = 2 + 0.5 * np.sin(bumps * theta) * np.sin((bumps + 1) * phi)
    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi)
    fig = go.Figure(go.Surface(x=x, y=y, z=z, surfacecolor=r,
                               colorscale="Viridis",
                               colorbar=dict(title="r(θ, φ)")))
    fig.update_layout(
        title=(f"Schematic of {num_dimensions}D space: deformations stand "
               "in for compactified dimensions"),
        scene=dict(xaxis_title="x", yaxis_title="y", zaxis_title="z",
                   aspectmode="cube"),
        height=560)
    return fig


def higgs_potential_figure(grid=60):
    """The Mexican-hat potential V(φ) = (|φ|² − 1)² over the complex plane."""
    x = np.linspace(-2, 2, grid)
    y = np.linspace(-2, 2, grid)
    X, Y = np.meshgrid(x, y)
    V = (X**2 + Y**2 - 1)**2
    fig = go.Figure(go.Surface(z=V, x=X, y=Y, colorscale="Viridis",
                               colorbar=dict(title="V(φ)")))
    fig.update_layout(
        title="Higgs potential V(φ) = (|φ|² − v²)², v = 1 (Mexican hat)",
        scene=dict(xaxis_title="Re(φ)", yaxis_title="Im(φ)",
                   zaxis_title="V(φ)", aspectmode="cube"),
        height=560)
    return fig


def gauge_field_figure(grid=8):
    """Magnetic-dipole vector field rendered with 3D cones."""
    lin = np.linspace(-2, 2, grid)
    X, Y, Z = np.meshgrid(lin, lin, lin)
    R = np.sqrt(X**2 + Y**2 + Z**2)
    R3 = np.maximum(R**3, 1e-3)
    Bx = 3 * X * Z / R3
    By = 3 * Y * Z / R3
    Bz = (3 * Z**2 - R**2) / R3
    norm = np.sqrt(Bx**2 + By**2 + Bz**2)
    norm = np.maximum(norm, 1e-9)
    fig = go.Figure(go.Cone(
        x=X.ravel(), y=Y.ravel(), z=Z.ravel(),
        u=(Bx / norm).ravel(), v=(By / norm).ravel(),
        w=(Bz / norm).ravel(),
        sizemode="absolute", sizeref=0.45, anchor="tail",
        colorscale="Blues", showscale=False))
    fig.update_layout(
        title="Gauge (magnetic dipole) field — unit vectors as cones",
        scene=dict(xaxis_title="x", yaxis_title="y", zaxis_title="z",
                   aspectmode="cube"),
        height=560)
    return fig


if __name__ == "__main__":
    # Smoke test: build every figure and report trace/frame counts.
    figs = {
        "tesseract": tesseract_figure(n_frames=12),
        "tesseract_slice": tesseract_slice_figure(0.3),
        "quantum_field_4d": quantum_field_4d_figure(grid=30, n_frames=8),
        "spacetime_evolution": spacetime_evolution_figure(grid=30,
                                                          n_frames=8),
        "spacetime_curvature": spacetime_curvature_figure(),
        "quantum_foam": quantum_foam_figure(),
        "extra_dimensions": extra_dimensions_figure(),
        "higgs_potential": higgs_potential_figure(),
        "gauge_field": gauge_field_figure(),
    }
    for name, fig in figs.items():
        print(f"{name:22s} traces={len(fig.data):2d} "
              f"frames={len(fig.frames):3d}")
    print("All Plotly figures constructed successfully.")

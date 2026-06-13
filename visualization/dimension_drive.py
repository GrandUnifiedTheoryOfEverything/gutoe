#!/usr/bin/env python3
"""DIMENSION DRIVE -- the interactive geometry deck of the Control Room.

Sci-fi skin, honest mathematics. Three instruments, each one an
interactive moment with full widget control and precision angle
readouts (0.1 degree):

  SPIN DECK   a triangle pivoting on a fixed point: play/pause, speed
              dial, step presets including the GOLDEN ANGLE
              (360(1 - 1/phi) = 137.5078 degrees) and Fibonacci turns;
              phyllotaxis stamp mode grows a sunflower spiral whose arm
              counts are Fibonacci numbers. Double the triangle into a
              square and spin that.

  XYZ DECK    mastery over 3D: a cube driven by three rotation-PLANE
              controls (xy, xz, yz). The deep fact on the panel: 3D
              rotations happen in planes; "axes" are just the planes'
              normals.

  ENGAGE 4D   from mastery of 3D, 4D can be expressed: the same panel
              gains exactly three more planes (xw, yw, zw) and the cube
              becomes the tesseract, perspective-projected. Nothing
              else changes -- that is the whole secret.

  MANDELBROT  iteration z <- z^2 + c with pan/zoom/depth widgets.
              Included as the canonical example of infinite structure
              from a one-line rule; it has nothing to do with
              unification and the panel says so.

Built for the NiceGUI app (nicegui_app.py); geometry shared with
visualization/spin_polygon.py and visualization/plotly_4d.py.
"""

import numpy as np
import plotly.graph_objects as go
from nicegui import ui

GOLDEN_ANGLE = 360.0 * (1.0 - 2.0 / (1.0 + np.sqrt(5.0)))   # 137.5078
FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

PLOTLY_DARK = dict(template="plotly_dark", paper_bgcolor="#0d1117",
                   plot_bgcolor="#0d1117")

TRIANGLE = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]])
SQUARE = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]])

PLANES = ["xy", "xz", "yz", "xw", "yw", "zw"]
AXIS_OF = {"xy": (0, 1), "xz": (0, 2), "yz": (1, 2),
           "xw": (0, 3), "yw": (1, 3), "zw": (2, 3)}


def _rot2(points, theta_deg, center=(0.0, 0.0)):
    t = np.radians(theta_deg)
    rot = np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
    c = np.asarray(center)
    return (points - c) @ rot.T + c


def _rot_nd(points, angles_deg):
    """Compose plane rotations (xy, xz, yz, xw, yw, zw) on 4D points."""
    rot = np.eye(4)
    for plane in PLANES:
        a = np.radians(angles_deg.get(plane, 0.0))
        if a == 0.0:
            continue
        i, j = AXIS_OF[plane]
        r = np.eye(4)
        r[i, i], r[i, j], r[j, i], r[j, j] = (np.cos(a), -np.sin(a),
                                              np.sin(a), np.cos(a))
        rot = r @ rot
    return points @ rot.T


def _segments_to_lines(verts, edges):
    """Edge list -> list of 2-point 4D polylines."""
    return [np.array([verts[i], verts[j]]) for i, j in edges]


def _shape_cube():
    """Cube embedded at w=0 (12 edges)."""
    verts = np.array([[(i >> k) & 1 for k in range(3)] + [0]
                      for i in range(8)], dtype=float)
    verts[:, :3] = verts[:, :3] * 2 - 1
    edges = [(i, j) for i in range(8) for j in range(i + 1, 8)
             if np.abs(verts[i] - verts[j]).sum() == 2.0]
    return dict(lines=_segments_to_lines(verts, edges), points=verts)


def _shape_tesseract():
    verts = np.array([[(i >> k) & 1 for k in range(4)]
                      for i in range(16)], dtype=float) * 2 - 1
    edges = [(i, j) for i in range(16) for j in range(i + 1, 16)
             if np.abs(verts[i] - verts[j]).sum() == 2.0]
    return dict(lines=_segments_to_lines(verts, edges), points=verts)


def _sphere_wireframe(radius=1.4, w=0.0, n_lat=5, n_lon=8, n_pts=48):
    """Lat/long wireframe of a 2-sphere living at 4D height w."""
    lines = []
    for k in range(1, n_lat + 1):                 # latitude circles
        phi = np.pi * k / (n_lat + 1)
        t = np.linspace(0, 2 * np.pi, n_pts)
        lines.append(np.stack([
            radius * np.sin(phi) * np.cos(t),
            radius * np.sin(phi) * np.sin(t),
            np.full_like(t, radius * np.cos(phi)),
            np.full_like(t, w)], axis=-1))
    for k in range(n_lon):                        # meridians
        lam = 2 * np.pi * k / n_lon
        t = np.linspace(0, np.pi, n_pts)
        lines.append(np.stack([
            radius * np.sin(t) * np.cos(lam),
            radius * np.sin(t) * np.sin(lam),
            radius * np.cos(t),
            np.full_like(t, w)], axis=-1))
    return lines


def _shape_globe():
    """A globe: 2-sphere wireframe at w = 0."""
    return dict(lines=_sphere_wireframe(), points=None)


def _shape_pyramid():
    """Pyramid built from a square and four triangles, apex along z.

    The 2D story made a circle from a spinning triangle and a square
    from two triangles; raising four triangles on the square makes the
    pyramid -- and spinning it sweeps the apex's circle in 3D."""
    base = np.array([[-1, -1, -0.8, 0], [1, -1, -0.8, 0],
                     [1, 1, -0.8, 0], [-1, 1, -0.8, 0]], dtype=float)
    apex = np.array([0.0, 0.0, 1.2, 0.0])
    verts = np.vstack([base, apex])
    edges = [(0, 1), (1, 2), (2, 3), (3, 0),
             (0, 4), (1, 4), (2, 4), (3, 4)]
    return dict(lines=_segments_to_lines(verts, edges), points=verts)


def _shape_glome():
    """The glome (3-sphere S^3): a family of 2-sphere slices at
    w_k = R cos(psi), radius R sin(psi) -- slicing and projection
    composed. Under an xw/yw/zw rotation the family deforms; that
    deformation IS the 4D rotation."""
    lines = []
    R = 1.5
    for psi in np.linspace(0.3, np.pi - 0.3, 4):
        lines += _sphere_wireframe(radius=R * np.sin(psi),
                                   w=R * np.cos(psi), n_lat=3, n_lon=6,
                                   n_pts=36)
    return dict(lines=lines, points=None)


def _shape_pyramid4():
    """The 4-pyramid: the 3D pyramid's construction repeated one
    dimension up -- a CUBE base with the apex raised along w."""
    cube = _shape_cube()
    apex = np.array([0.0, 0.0, 0.0, 1.6])
    verts = np.vstack([cube["points"], apex])
    lines = list(cube["lines"])
    for i in range(8):
        lines.append(np.array([verts[i], apex]))
    return dict(lines=lines, points=verts)


SHAPES_3D = {"Cube": _shape_cube, "Globe": _shape_globe,
             "Pyramid": _shape_pyramid}
SHAPES_4D = {"Tesseract": _shape_tesseract, "Glome (S³)": _shape_glome,
             "4-Pyramid (apex in w)": _shape_pyramid4}


# ---------------------------------------------------------------------------
# Instrument 1: SPIN DECK
# ---------------------------------------------------------------------------


def _spin_figure(state):
    fig = go.Figure()
    shape = TRIANGLE if state["shape"] in ("Triangle", "Doubled") \
        else SQUARE
    radius = np.sqrt(2.0) if state["shape"] == "Square" else 1.0

    # vertex-path circle
    t = np.linspace(0, 2 * np.pi, 120)
    fig.add_trace(go.Scatter(x=radius * np.cos(t), y=radius * np.sin(t),
                             mode="lines",
                             line=dict(color="#3fb950", width=1),
                             opacity=0.45, hoverinfo="skip",
                             showlegend=False))

    # phyllotaxis stamps (Vogel spiral when the step is the golden angle)
    if state["stamps"]:
        arr = np.array(state["stamps"])
        n = np.arange(1, len(arr) + 1)
        fig.add_trace(go.Scatter(
            x=arr[:, 0], y=arr[:, 1], mode="markers",
            marker=dict(size=5, color=n, colorscale="Viridis",
                        showscale=False),
            hoverinfo="skip", showlegend=False))

    # motion-blur ghosts
    if state["trails"]:
        for k, g in enumerate(state["ghost_thetas"]):
            poly = _rot2(shape, g)
            fig.add_trace(go.Scatter(
                x=np.append(poly[:, 0], poly[0, 0]),
                y=np.append(poly[:, 1], poly[0, 1]),
                mode="lines", fill="toself",
                fillcolor="rgba(88,166,255,0.10)",
                line=dict(width=0), hoverinfo="skip", showlegend=False))

    # the doubled twin (completes the square)
    if state["shape"] == "Doubled":
        twin = _rot2(_rot2(TRIANGLE, 180.0, center=(0.5, 0.5)),
                     state["theta"])
        fig.add_trace(go.Scatter(
            x=np.append(twin[:, 0], twin[0, 0]),
            y=np.append(twin[:, 1], twin[0, 1]),
            mode="lines", fill="toself",
            fillcolor="rgba(163,113,247,0.55)",
            line=dict(color="#a371f7", width=2),
            hoverinfo="skip", showlegend=False))

    poly = _rot2(shape, state["theta"])
    fig.add_trace(go.Scatter(
        x=np.append(poly[:, 0], poly[0, 0]),
        y=np.append(poly[:, 1], poly[0, 1]),
        mode="lines", fill="toself", fillcolor="rgba(88,166,255,0.75)",
        line=dict(color="#9ecbff", width=2),
        hoverinfo="skip", showlegend=False))
    fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers",
                             marker=dict(size=9, color="#f85149"),
                             hoverinfo="skip", showlegend=False))

    lim = 1.8
    fig.update_layout(height=440, margin=dict(l=10, r=10, t=10, b=10),
                      xaxis=dict(range=[-lim, lim], visible=False),
                      yaxis=dict(range=[-lim, lim], visible=False,
                                 scaleanchor="x"),
                      **PLOTLY_DARK)
    return fig


def build_spin_deck():
    state = dict(theta=0.0, speed=2.0, playing=False, shape="Triangle",
                 trails=True, ghost_thetas=[], stamps=[],
                 stamp_mode=False, revs=0)

    plot = ui.plotly(_spin_figure(state)).classes("w-full")
    readout = ui.label().classes("hud-readout")

    def refresh():
        plot.update_figure(_spin_figure(state))
        readout.text = (f"θ = {state['theta']:07.3f}°   "
                        f"Δθ = {state['speed']:.4f}°/tick   "
                        f"rev = {state['revs']}   "
                        f"stamps = {len(state['stamps'])}")

    def tick():
        if not state["playing"]:
            return
        prev = state["theta"]
        state["theta"] = (state["theta"] + state["speed"]) % 360.0
        if state["theta"] < prev:
            state["revs"] += 1
        n_ghost = int(min(14, 2 + state["speed"] / 2.5))
        state["ghost_thetas"] = [
            (state["theta"] - state["speed"] * k / 2.0) % 360
            for k in range(1, n_ghost)]
        if state["stamp_mode"]:
            n = len(state["stamps"]) + 1
            r = 0.10 * np.sqrt(n)              # Vogel: r = c sqrt(n)
            a = np.radians(state["theta"])
            if r < 1.7:
                state["stamps"].append((r * np.cos(a), r * np.sin(a)))
        angle_slider.value = round(state["theta"], 3)
        refresh()

    ui.timer(0.08, tick)

    with ui.row().classes("items-center gap-3 flex-wrap mt-1"):
        play_btn = ui.button(icon="play_arrow") \
            .props("round push glossy color=primary size=md ripple")

        def toggle_play():
            state["playing"] = not state["playing"]
            play_btn.props(f"icon={'pause' if state['playing'] else 'play_arrow'}")
        play_btn.on_click(toggle_play)

        def do_reset():
            state.update(theta=0.0, revs=0, ghost_thetas=[], stamps=[],
                         playing=False)
            play_btn.props("icon=play_arrow")
            angle_slider.value = 0.0
            refresh()
        ui.button(icon="restart_alt", on_click=do_reset) \
            .props("round push glossy color=secondary size=md ripple")

        shape_toggle = ui.toggle(["Triangle", "Doubled", "Square"],
                                 value="Triangle") \
            .props("rounded unelevated toggle-color=primary ripple")

        def set_shape(e):
            state["shape"] = e.value
            refresh()
        shape_toggle.on_value_change(set_shape)

        trails_sw = ui.switch("trails", value=True)
        trails_sw.on_value_change(
            lambda e: (state.update(trails=e.value), refresh()))
        stamp_sw = ui.switch("phyllotaxis stamps")
        stamp_sw.on_value_change(
            lambda e: state.update(stamp_mode=e.value))

    with ui.row().classes("items-end gap-8 flex-wrap mt-2"):
        with ui.column().classes("items-center"):
            speed_knob = ui.knob(2.0, min=0.1, max=60.0, step=0.1,
                                 show_value=True) \
                .props("size=64px color=primary track-color=grey-9")
            ui.label("Δθ per tick [°] — speed dial").classes(
                "text-xs text-gray-500")
            speed_knob.on_value_change(
                lambda e: state.update(speed=float(e.value)))
        with ui.column().classes("grow"):
            ui.label("step presets — the golden angle is "
                     "360(1−1/φ) = 137.5078°").classes(
                "text-xs text-gray-500")
            presets = {
                "1°": 1.0, "10°": 10.0, "45°": 45.0, "90°": 90.0,
                "φ 137.5078°": float(round(GOLDEN_ANGLE, 4)),
                "Fib 360/5=72°": 72.0, "Fib 360·8/13≈221.5°": 221.538,
            }
            preset_toggle = ui.toggle(list(presets), value="1°") \
                .props("rounded unelevated dense toggle-color=secondary "
                       "ripple no-caps")

            def set_preset(e):
                state["speed"] = presets[e.value]
                speed_knob.value = presets[e.value]
            preset_toggle.on_value_change(set_preset)

            angle_slider = ui.slider(min=0.0, max=360.0, step=0.001,
                                     value=0.0) \
                .props("label-always color=primary")
            ui.label("θ — exact angle [°] (drag while paused)").classes(
                "text-xs text-gray-500")

            def scrub(e):
                if not state["playing"]:
                    state["theta"] = float(e.value)
                    refresh()
            angle_slider.on_value_change(scrub)

    ui.markdown(
        "Set the speed dial to **φ** and switch on *phyllotaxis stamps*: "
        "the stamped vertices grow a sunflower-head spiral (Vogel's "
        "model, $r = c\\sqrt{n}$, $\\theta = n \\cdot 137.5078°$), and "
        "the visible spiral-arm counts are **Fibonacci numbers** "
        f"({', '.join(map(str, FIB[2:9]))}…) — the golden angle is the "
        "'most irrational' turn, so no two stamps ever align."
    ).classes("text-sm mt-2")
    refresh()


# ---------------------------------------------------------------------------
# Instrument 2: XYZ DECK -> ENGAGE 4D
# ---------------------------------------------------------------------------


def _project4(points4):
    w = points4[..., 3]
    scale = 3.0 / (3.0 - np.clip(w, -2.4, 2.4))
    return points4[..., :3] * scale[..., None], w


def _xyz_figure(state):
    registry = SHAPES_4D if state["four_d"] else SHAPES_3D
    builder = registry.get(state["shape"]) or next(iter(registry.values()))
    shape = builder()

    fig = go.Figure()
    xs, ys, zs, ws = [], [], [], []
    for line in shape["lines"]:
        pts = _rot_nd(line, state["angles"])
        v3, w = _project4(pts)
        xs += list(v3[:, 0]) + [None]
        ys += list(v3[:, 1]) + [None]
        zs += list(v3[:, 2]) + [None]
        ws += list(w) + [w[-1]]
    fig.add_trace(go.Scatter3d(
        x=xs, y=ys, z=zs, mode="lines",
        line=dict(color=ws, colorscale="Viridis", cmin=-1.8, cmax=1.8,
                  width=5),
        hoverinfo="skip", showlegend=False))

    if shape["points"] is not None:
        pts = _rot_nd(shape["points"], state["angles"])
        v3, w = _project4(pts)
        fig.add_trace(go.Scatter3d(
            x=v3[:, 0], y=v3[:, 1], z=v3[:, 2], mode="markers",
            marker=dict(size=5.5, color=w, colorscale="Viridis",
                        cmin=-1.8, cmax=1.8,
                        colorbar=dict(title="w") if state["four_d"]
                        else None),
            hovertemplate="w = %{marker.color:.3f}<extra></extra>",
            showlegend=False))

    lim = 2.6
    fig.update_layout(
        height=480, margin=dict(l=0, r=0, t=10, b=0),
        scene=dict(aspectmode="cube",
                   xaxis=dict(range=[-lim, lim], title="x"),
                   yaxis=dict(range=[-lim, lim], title="y"),
                   zaxis=dict(range=[-lim, lim], title="z")),
        uirevision="keep-camera", **PLOTLY_DARK)
    return fig


def build_xyz_deck():
    state = dict(angles={p: 0.0 for p in PLANES}, four_d=False,
                 auto={p: False for p in PLANES}, auto_speed=1.5,
                 shape="Cube")

    ui.markdown(
        "The honest secret of rotation: it never happens 'about an "
        "axis' — it happens **in a plane**. In 3D there are exactly "
        "three planes (*xy, xz, yz*); the familiar axes *z, y, x* are "
        "just their normals. Master these three controllers and you "
        "already own everything 4D will ask of you. The **pyramid** "
        "continues the 2D story — four triangles raised on the square; "
        "the **globe** is the shape every spin secretly sweeps."
    ).classes("text-sm")

    shape_toggle = ui.toggle(list(SHAPES_3D), value="Cube") \
        .props("rounded unelevated toggle-color=primary ripple no-caps")

    plot = ui.plotly(_xyz_figure(state)).classes("w-full")
    readout = ui.label().classes("hud-readout")

    def set_shape(e):
        if e.value is not None:
            state["shape"] = e.value
            refresh()
    shape_toggle.on_value_change(set_shape)

    sliders = {}

    def refresh():
        plot.update_figure(_xyz_figure(state))
        parts = [f"{p.upper()} {state['angles'][p]:07.3f}°"
                 for p in PLANES if state["four_d"] or "w" not in p]
        readout.text = "   ".join(parts)

    def make_slider_row(planes, note):
        with ui.row().classes("gap-6 flex-wrap items-end w-full") as row:
            for p in planes:
                with ui.column().classes("grow min-w-40"):
                    s = ui.slider(min=0.0, max=360.0, step=0.1,
                                  value=0.0) \
                        .props("label-always color="
                               + ("amber" if "w" in p else "primary"))
                    with ui.row().classes("items-center gap-2"):
                        ui.label(f"ROT-{p.upper()} [°]").classes(
                            "text-xs text-gray-500")
                        cb = ui.checkbox("auto")
                        cb.on_value_change(
                            lambda e, p=p: state["auto"].update({p: e.value}))
                    sliders[p] = s

                    def on_slide(e, p=p):
                        state["angles"][p] = float(e.value)
                        refresh()
                    s.on_value_change(on_slide)
            ui.label(note).classes("text-xs text-gray-600 w-full")
        return row

    make_slider_row(["xy", "xz", "yz"],
                    "three planes of 3D — drag, or tick auto and let "
                    "the drive fly")

    w_row = make_slider_row(["xw", "yw", "zw"],
                            "the three new planes of 4D — each mixes a "
                            "spatial axis with w; the double swap of "
                            "inner and outer cube IS the 4D rotation")
    w_row.set_visibility(False)

    explain = ui.markdown(
        "**4D ENGAGED.** The cube became the tesseract and the panel "
        "gained exactly three controls — *xw, yw, zw* — and nothing "
        "else. That is the entire upgrade from 3D to 4D rotation: "
        "$\\binom{3}{2} = 3$ planes became $\\binom{4}{2} = 6$. The "
        "projection is perspective, $p = d/(d-w)$ with $d = 3$; vertex "
        "color is the exact w-coordinate."
    ).classes("text-sm bg-[#1c2128] rounded p-3")
    explain.set_visibility(False)

    with ui.row().classes("items-center gap-4 mt-2"):
        engage = ui.button("ENGAGE 4D", icon="rocket_launch") \
            .props("push glossy color=deep-purple ripple size=lg")

        def toggle_4d():
            state["four_d"] = not state["four_d"]
            w_row.set_visibility(state["four_d"])
            explain.set_visibility(state["four_d"])
            # each 3D shape has its one-dimension-up counterpart
            registry = SHAPES_4D if state["four_d"] else SHAPES_3D
            names = list(registry)
            old = (list(SHAPES_3D) if state["four_d"]
                   else list(SHAPES_4D))
            idx = old.index(state["shape"]) if state["shape"] in old \
                else 0
            state["shape"] = names[idx]
            shape_toggle.options = names
            shape_toggle.value = names[idx]
            shape_toggle.update()
            engage.props(
                "push glossy ripple size=lg color="
                + ("negative" if state["four_d"] else "deep-purple"))
            engage.text = ("DISENGAGE — BACK TO 3D" if state["four_d"]
                           else "ENGAGE 4D")
            refresh()
        engage.on_click(toggle_4d)

        with ui.column().classes("items-center"):
            sp = ui.knob(1.5, min=0.1, max=10.0, step=0.1,
                         show_value=True) \
                .props("size=56px color=secondary track-color=grey-9")
            ui.label("auto-drive [°/tick]").classes(
                "text-xs text-gray-500")
            sp.on_value_change(
                lambda e: state.update(auto_speed=float(e.value)))

        def zero_all():
            for p in PLANES:
                state["angles"][p] = 0.0
                sliders[p].value = 0.0
            refresh()
        ui.button("zero all planes", icon="exposure_zero",
                  on_click=zero_all).props("push glossy ripple")

    def tick():
        moved = False
        for p, on in state["auto"].items():
            if on and (state["four_d"] or "w" not in p):
                state["angles"][p] = (state["angles"][p]
                                      + state["auto_speed"]) % 360
                sliders[p].value = round(state["angles"][p], 1)
                moved = True
        if moved:
            refresh()
    ui.timer(0.1, tick)
    refresh()


# ---------------------------------------------------------------------------
# Instrument 2b: SCENE DECK -- a true three.js scene (ui.scene)
# ---------------------------------------------------------------------------


def build_scene_deck():
    """Native three.js 3D via NiceGUI's ui.scene: orbit the camera with
    the mouse, drive the object with the plane dials. Each 3D rotation
    plane has a normal axis -- the labels show both, because that
    correspondence is exactly what 4D takes away."""
    state = dict(rx=0.0, ry=0.0, rz=0.0, shape="Cube",
                 auto=False, auto_speed=0.8)

    ui.markdown(
        "This deck is a **real 3D engine** (three.js through NiceGUI's "
        "`ui.scene`): drag to orbit, scroll to zoom — the camera is "
        "yours. The dials rotate the *object*, one plane at a time. "
        "Note the double labels: in 3D every rotation plane has a "
        "unique normal axis (yz↔x, xz↔y, xy↔z). That luxury is what "
        "4D removes — which is why the tesseract next door must be "
        "*projected*, not handed to the engine."
    ).classes("text-sm")

    scene_holder = dict(scene=None, group=None)

    def build_shape(scene):
        with scene.group() as grp:
            if state["shape"] == "Cube":
                scene.box(1.6, 1.6, 1.6).material("#58a6ff", 0.85)
            elif state["shape"] == "Globe":
                scene.sphere(1.1).material("#3fb950", 0.55)
                # equator + meridian rings so the spin is visible
                t = np.linspace(0, 2 * np.pi, 48)
                rings = [
                    [[1.15 * np.cos(a), 1.15 * np.sin(a), 0] for a in t],
                    [[1.15 * np.cos(a), 0, 1.15 * np.sin(a)] for a in t],
                ]
                for ring in rings:
                    for a, b in zip(ring[:-1], ring[1:]):
                        scene.line(a, b).material("#e6edf3")
            else:  # Pyramid: cylinder with 4 radial segments, apex r=0
                scene.cylinder(0.0, 1.3, 1.8, 4) \
                    .material("#a371f7", 0.85) \
                    .rotate(np.pi / 2, 0, np.pi / 4)
        return grp

    def rebuild():
        scene = scene_holder["scene"]
        scene.clear()
        with scene:
            scene.spot_light(distance=120, intensity=0.6) \
                .move(-4, 0, 6)
            # world axes, labeled by color
            scene.line([0, 0, 0], [2.6, 0, 0]).material("#f85149")
            scene.line([0, 0, 0], [0, 2.6, 0]).material("#3fb950")
            scene.line([0, 0, 0], [0, 0, 2.6]).material("#58a6ff")
            scene_holder["group"] = build_shape(scene)
        apply_rotation()

    def apply_rotation():
        grp = scene_holder["group"]
        if grp is not None:
            grp.rotate(np.radians(state["rx"]), np.radians(state["ry"]),
                       np.radians(state["rz"]))
        readout.text = (f"YZ(x) {state['rx']:07.3f}°   "
                        f"XZ(y) {state['ry']:07.3f}°   "
                        f"XY(z) {state['rz']:07.3f}°")

    with ui.scene(width=860, height=460, grid=True) \
            .classes("w-full rounded-lg") as scene:
        scene_holder["scene"] = scene

    readout = ui.label().classes("hud-readout")

    with ui.row().classes("items-center gap-4 flex-wrap mt-1"):
        shape_toggle = ui.toggle(["Cube", "Globe", "Pyramid"],
                                 value="Cube") \
            .props("rounded unelevated toggle-color=primary ripple")

        def set_shape(e):
            if e.value:
                state["shape"] = e.value
                rebuild()
        shape_toggle.on_value_change(set_shape)

        auto_sw = ui.switch("auto-orbit object")
        auto_sw.on_value_change(lambda e: state.update(auto=e.value))
        with ui.column().classes("items-center"):
            spd = ui.knob(0.8, min=0.1, max=6.0, step=0.1,
                          show_value=True) \
                .props("size=52px color=secondary track-color=grey-9")
            ui.label("auto [°/tick]").classes("text-xs text-gray-500")
            spd.on_value_change(
                lambda e: state.update(auto_speed=float(e.value)))

    sliders = {}
    with ui.row().classes("gap-6 flex-wrap items-end w-full mt-1"):
        for key, plane, axis in (("rx", "YZ", "x"), ("ry", "XZ", "y"),
                                 ("rz", "XY", "z")):
            with ui.column().classes("grow min-w-40"):
                s = ui.slider(min=0.0, max=360.0, step=0.1, value=0.0) \
                    .props("label-always color=primary")
                ui.label(f"plane {plane}  ↔  axis {axis}").classes(
                    "text-xs text-gray-500")

                def on_slide(e, key=key):
                    state[key] = float(e.value)
                    apply_rotation()
                s.on_value_change(on_slide)
                sliders[key] = s

    def tick():
        if state["auto"]:
            for key in ("rx", "ry", "rz"):
                state[key] = (state[key] + state["auto_speed"]) % 360
                sliders[key].value = round(state[key], 1)
            apply_rotation()
    ui.timer(0.1, tick)

    ui.timer(0.5, rebuild, once=True)   # build after the scene mounts


# ---------------------------------------------------------------------------
# Instrument 3: DRAW DECK -- pointer/touch drawing, then spin it
# ---------------------------------------------------------------------------

DRAW_W, DRAW_H = 860, 480
DRAW_COLORS = ["#58a6ff", "#3fb950", "#a371f7", "#f0883e", "#f85149"]


def _draw_bg_data_uri():
    """A dark grid background as a data URI (no file round-trip)."""
    import base64
    import io as _io

    from PIL import Image as _Image
    from PIL import ImageDraw as _ImageDraw
    img = _Image.new("RGB", (DRAW_W, DRAW_H), "#0d1117")
    d = _ImageDraw.Draw(img)
    for x in range(0, DRAW_W, 40):
        d.line([(x, 0), (x, DRAW_H)], fill="#161d27")
    for y in range(0, DRAW_H, 40):
        d.line([(0, y), (DRAW_W, y)], fill="#161d27")
    d.ellipse([DRAW_W / 2 - 3, DRAW_H / 2 - 3,
               DRAW_W / 2 + 3, DRAW_H / 2 + 3], fill="#f85149")
    buf = _io.BytesIO()
    img.save(buf, format="PNG")
    return ("data:image/png;base64,"
            + base64.b64encode(buf.getvalue()).decode())


def _strokes_svg(strokes, current, theta, connect):
    """Render all strokes (rotated by theta about canvas center) as
    glowing SVG polylines + pointer-connector dots."""
    cx, cy = DRAW_W / 2, DRAW_H / 2
    t = np.radians(theta)
    cos_t, sin_t = np.cos(t), np.sin(t)

    def xform(pts):
        a = np.asarray(pts, dtype=float)
        x = a[:, 0] - cx
        y = a[:, 1] - cy
        return np.stack([cx + x * cos_t - y * sin_t,
                         cy + x * sin_t + y * cos_t], axis=-1)

    parts = []
    for k, stroke in enumerate(list(strokes) + ([current] if current
                                                else [])):
        if len(stroke) < 1:
            continue
        color = DRAW_COLORS[k % len(DRAW_COLORS)]
        pts = xform(stroke)
        if connect and len(pts) > 2:
            pts = np.vstack([pts, pts[:1]])
        path = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        # glow underlay + bright line + connector dots
        parts.append(f'<polyline points="{path}" fill="none" '
                     f'stroke="{color}" stroke-width="7" '
                     f'stroke-opacity="0.25" stroke-linecap="round" '
                     f'stroke-linejoin="round" />')
        parts.append(f'<polyline points="{path}" fill="none" '
                     f'stroke="{color}" stroke-width="2.4" '
                     f'stroke-linecap="round" '
                     f'stroke-linejoin="round" />')
        for x, y in pts[::6]:
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" '
                         f'fill="{color}" fill-opacity="0.9" />')
    return "".join(parts)


def build_draw_deck():
    state = dict(strokes=[], current=None, theta=0.0, speed=0.0,
                 connect=False)

    ui.markdown(
        "Draw with mouse or touch — every pointer move becomes a "
        "connected point. Then hit **SPIN IT** and your sketch gets "
        "the triangle treatment: rotation about the fixed red point, "
        "with the exact angle on the readout."
    ).classes("text-sm")

    ii = ui.interactive_image(
        _draw_bg_data_uri(), cross=True,
        events=["pointerdown", "pointermove", "pointerup"]) \
        .classes("w-full rounded-lg")
    readout = ui.label().classes("hud-readout")

    def refresh():
        ii.content = _strokes_svg(state["strokes"], state["current"],
                                  state["theta"], state["connect"])
        n_pts = sum(len(s) for s in state["strokes"])
        readout.text = (f"θ = {state['theta']:07.3f}°   "
                        f"Δθ = {state['speed']:.2f}°/tick   "
                        f"strokes = {len(state['strokes'])}   "
                        f"points = {n_pts}")

    def on_pointer(e):
        x, y = float(e.image_x), float(e.image_y)
        if e.type == "pointerdown":
            state["current"] = [(x, y)]
        elif e.type == "pointermove" and state["current"] is not None:
            last = state["current"][-1]
            if (x - last[0]) ** 2 + (y - last[1]) ** 2 > 16:
                state["current"].append((x, y))
        elif e.type == "pointerup" and state["current"] is not None:
            if len(state["current"]) > 1:
                state["strokes"].append(state["current"])
            state["current"] = None
        refresh()
    ii.on_mouse(on_pointer)

    def tick():
        if state["speed"]:
            state["theta"] = (state["theta"] + state["speed"]) % 360
            refresh()
    ui.timer(0.06, tick)

    with ui.row().classes("items-center gap-3 flex-wrap mt-1"):
        spin_btn = ui.button("SPIN IT", icon="cyclone") \
            .props("push glossy color=primary ripple")

        def toggle_spin():
            state["speed"] = 3.0 if state["speed"] == 0.0 else 0.0
            spin_btn.text = "HOLD IT" if state["speed"] else "SPIN IT"
        spin_btn.on_click(toggle_spin)

        def faster():
            state["speed"] = min(40.0, max(state["speed"], 1.0) * 1.6)
            spin_btn.text = "HOLD IT"
        ui.button("faster", icon="speed", on_click=faster) \
            .props("push glossy ripple")

        connect_sw = ui.switch("connect ends (close the loops)")
        connect_sw.on_value_change(
            lambda e: (state.update(connect=e.value), refresh()))

        def undo():
            if state["strokes"]:
                state["strokes"].pop()
            refresh()
        ui.button("undo stroke", icon="undo", on_click=undo) \
            .props("push glossy ripple")

        def clear():
            state.update(strokes=[], current=None, theta=0.0, speed=0.0)
            spin_btn.text = "SPIN IT"
            refresh()
        ui.button("clear", icon="layers_clear", on_click=clear) \
            .props("push glossy color=negative ripple")

    refresh()


# ---------------------------------------------------------------------------
# Instrument 4: MANDELBROT MODE
# ---------------------------------------------------------------------------


def _mandelbrot(cx, cy, half_width, max_iter, nx=360, ny=270):
    x = np.linspace(cx - half_width, cx + half_width, nx)
    y = np.linspace(cy - half_width * ny / nx,
                    cy + half_width * ny / nx, ny)
    C = x[None, :] + 1j * y[:, None]
    Z = np.zeros_like(C)
    count = np.zeros(C.shape, dtype=float)
    alive = np.ones(C.shape, dtype=bool)
    for n in range(max_iter):
        Z[alive] = Z[alive] ** 2 + C[alive]
        escaped = alive & (np.abs(Z) > 2.0)
        # smooth (fractional) escape count for accurate banding
        count[escaped] = (n + 1
                          - np.log2(np.maximum(
                              np.log(np.abs(Z[escaped])), 1e-12)))
        alive &= ~escaped
    count[alive] = max_iter
    return x, y, count


def build_mandelbrot_deck():
    state = dict(cx=-0.5, cy=0.0, zoom=0.0, max_iter=120,
                 scale_name="Inferno")

    ui.markdown(
        "One rule, iterated: $z \\leftarrow z^2 + c$. Color is the "
        "(smooth) escape count — the accuracy dial below is the "
        "iteration depth. *Honesty panel: the Mandelbrot set has "
        "nothing to do with unification physics; it is here as the "
        "canonical demonstration that infinite structure can come from "
        "a one-line law.*"
    ).classes("text-sm")

    plot = ui.plotly(go.Figure()).classes("w-full")
    readout = ui.label().classes("hud-readout")

    def render():
        half = 1.6 / (2.0 ** state["zoom"])
        x, y, m = _mandelbrot(state["cx"], state["cy"], half,
                              int(state["max_iter"]))
        fig = go.Figure(go.Heatmap(
            x=x, y=y, z=m, colorscale=state["scale_name"],
            showscale=False,
            hovertemplate="c = %{x:.6f} %{y:+.6f}i<br>"
                          "escape = %{z:.1f}<extra></extra>"))
        fig.update_layout(height=460,
                          margin=dict(l=10, r=10, t=10, b=10),
                          yaxis=dict(scaleanchor="x"), **PLOTLY_DARK)
        plot.update_figure(fig)
        readout.text = (f"center = {state['cx']:+.6f} "
                        f"{state['cy']:+.6f}i   "
                        f"zoom = 2^{state['zoom']:.1f}   "
                        f"window = ±{half:.2e}   "
                        f"depth = {int(state['max_iter'])}")

    with ui.row().classes("items-end gap-8 flex-wrap"):
        with ui.column().classes("items-center"):
            zk = ui.knob(0.0, min=0.0, max=14.0, step=0.5,
                         show_value=True) \
                .props("size=64px color=primary track-color=grey-9")
            ui.label("zoom [powers of 2]").classes("text-xs text-gray-500")
            zk.on_value_change(
                lambda e: (state.update(zoom=float(e.value)), render()))
        with ui.column().classes("grow min-w-52"):
            cxs = ui.slider(min=-2.0, max=1.0, step=1e-6, value=-0.5) \
                .props("label-always color=primary")
            ui.label("center, real part").classes("text-xs text-gray-500")
            cxs.on_value_change(
                lambda e: (state.update(cx=float(e.value)), render()))
        with ui.column().classes("grow min-w-52"):
            cys = ui.slider(min=-1.5, max=1.5, step=1e-6, value=0.0) \
                .props("label-always color=primary")
            ui.label("center, imaginary part").classes(
                "text-xs text-gray-500")
            cys.on_value_change(
                lambda e: (state.update(cy=float(e.value)), render()))
        with ui.column().classes("grow min-w-40"):
            its = ui.slider(min=40, max=600, step=20, value=120) \
                .props("label-always color=secondary")
            ui.label("iteration depth (accuracy)").classes(
                "text-xs text-gray-500")
            its.on_value_change(
                lambda e: (state.update(max_iter=int(e.value)), render()))

    with ui.row().classes("items-center gap-3 mt-1"):
        for label_t, cx, cy, z in (
                ("full set", -0.5, 0.0, 0.0),
                ("seahorse valley", -0.745, 0.11, 6.0),
                ("elephant valley", 0.275, 0.005, 6.0),
                ("spiral", -0.7453, 0.1127, 9.5)):
            def jump(cx=cx, cy=cy, z=z):
                state.update(cx=cx, cy=cy, zoom=z)
                cxs.value, cys.value, zk.value = cx, cy, z
                render()
            ui.button(label_t, on_click=jump) \
                .props("push glossy ripple no-caps dense")

    render()

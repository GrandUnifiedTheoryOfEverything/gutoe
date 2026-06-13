#!/usr/bin/env python3
"""GUToE Control Room (NiceGUI delivery, v2).

The third delivery of the project UI, built on NiceGUI
(https://github.com/zauberzeug/nicegui), designed around one idea:

    every simple concept expands into its component parts, and each part
    keeps explaining itself with increasing complexity until the
    explanation terminates in an interactive moment -- a graphic you can
    drive with dials and levers.

The page is a recursive concept tree. Level 0 is one sentence; expanding
any node reveals its equation, its plain-language meaning, its component
concepts, and -- where a concept is best explained by doing -- a live
figure wired to knobs (dials), vertical sliders (levers), toggles, and
buttons. A global complexity selector (Basic / Advanced / Expert)
controls how much instrumentation each interactive moment exposes; in
Expert mode the PDG inputs themselves become levers so the sensitivity
of grand unification to experiment can be felt by hand.

All physics is computed live by the same modules used by the tests, the
paper, and the other two UIs (toe_math/rg_running.py,
toe_math/gut_embedding.py).

Run:  python3 nicegui_app.py     (serves on http://127.0.0.1:8051)
"""

import numpy as np
from nicegui import ui

from toe_math import gut_embedding as gut
from toe_math import master_equation as master_eq
from toe_math import rg_running as rg
from version import VERSION
from visualization import plotly_4d as p4d

# ---------------------------------------------------------------------------
# Page chrome: dark mode, MathJax, styling
# ---------------------------------------------------------------------------

ui.dark_mode().enable()

ui.add_head_html("""
<script>
window.MathJax = {tex: {inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                        displayMath: [['$$', '$$']]},
                  options: {enableMenu: false}};
</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js">
</script>
<style>
  .concept { border-left: 2px solid #30363d; }
  .concept .q-expansion-item__container .q-item { min-height: 44px; }
  .eq { font-size: 1.05rem; padding: 0.4rem 0; }
  .plain { color: #9aa4b2; font-style: italic; }
  .stop-note { color: #3fb950; font-size: 0.8rem; letter-spacing: 0.5px;
               text-transform: uppercase; }
  .hud-readout {
    font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', monospace;
    font-size: 0.85rem; color: #3fb950; letter-spacing: 0.08em;
    background: #0d1117; border: 1px solid #1f6f31; border-radius: 6px;
    padding: 0.3rem 0.7rem; margin-top: 0.4rem; display: inline-block;
    text-shadow: 0 0 8px #3fb95066;
  }
</style>
""")

LEVELS = {"Basic": 0, "Advanced": 1, "Expert": 2}

PLOTLY_DARK = dict(template="plotly_dark", paper_bgcolor="#121212",
                   plot_bgcolor="#121212")


def _dark(fig, height=None):
    fig.update_layout(**PLOTLY_DARK)
    if height:
        fig.update_layout(height=height)
    return fig


def _typeset():
    ui.run_javascript(
        "window.MathJax && MathJax.typesetPromise && MathJax.typesetPromise()")


# ---------------------------------------------------------------------------
# Header: title, version, the complexity menu
# ---------------------------------------------------------------------------

with ui.header().classes("items-center justify-between bg-[#161b22] px-6"):
    with ui.row().classes("items-center gap-4"):
        ui.icon("hub").classes("text-2xl text-blue-400")
        with ui.column().classes("gap-0"):
            ui.label("GUToE Control Room").classes("text-lg font-bold")
            ui.label("every concept expands until the explanation "
                     "becomes something you can touch") \
                .classes("text-xs text-gray-500")
    with ui.row().classes("items-center gap-3"):
        ui.badge(f"v{VERSION}", color="blue").props("rounded")
        complexity = ui.toggle(list(LEVELS), value="Basic") \
            .props("rounded unelevated toggle-color=primary")
        ui.tooltip("How much instrumentation each interactive moment "
                   "exposes. Expert turns the experimental inputs "
                   "themselves into levers.")


def at_level(element, min_level):
    """Show `element` only at or above the given complexity level."""
    element.bind_visibility_from(
        complexity, "value",
        lambda v, m=min_level: LEVELS.get(v, 0) >= m)
    return element


# ---------------------------------------------------------------------------
# Concept-tree helper
# ---------------------------------------------------------------------------

def concept(title, plain, *, icon="unfold_more", opened=False, anchor=None):
    """An expandable concept node: title + one-line plain meaning.

    Expanding it reveals whatever is built inside the returned context:
    equations, component concepts (nested calls), and interactive
    moments. Increasing depth = increasing complexity.
    """
    exp = ui.expansion(title, caption=plain, icon=icon, value=opened) \
        .classes("w-full concept rounded-lg bg-[#161b22] mb-2") \
        .props("dense-toggle expand-separator header-class=text-base")
    if anchor:
        exp.props(f'id={anchor}')
    return exp


def equation(latex):
    ui.html(f'<div class="eq">$${latex}$$</div>')


def stop_note(text="This is where this branch bottoms out — "
                   "the explanation above is the whole story."):
    ui.label(text).classes("stop-note mt-2")


# ---------------------------------------------------------------------------
# Navigation drawer: the concept hierarchy as a menu
# ---------------------------------------------------------------------------

NAV = [
    ("The composite action S", "c-root"),
    ("— Gravity sector", "c-gravity"),
    ("— Matter sector", "c-matter"),
    ("— Gauge sector & unification", "c-gauge"),
    ("— Quantum sector", "c-quantum"),
    ("Seeing the fourth dimension", "c-4d"),
    ("DIMENSION DRIVE (interactive)", "c-drive"),
    ("The honest conclusion", "c-conclusion"),
]

with ui.left_drawer(value=True).classes("bg-[#0d1117] p-3") as drawer:
    ui.label("Concept map").classes("text-xs uppercase text-gray-500 mb-2")
    for label_text, anchor in NAV:
        ui.button(label_text,
                  on_click=lambda a=anchor: ui.run_javascript(
                      f"document.getElementById('{a}')"
                      f"?.scrollIntoView({{behavior:'smooth'}})")) \
            .props("flat align=left ripple no-caps size=sm") \
            .classes("w-full justify-start text-gray-300")
    ui.separator().classes("my-3")
    ui.label("Other deliveries").classes("text-xs uppercase text-gray-500")
    ui.label("streamlit run streamlit_app.py").classes("text-xs font-mono")
    ui.label("python3 dash_app.py").classes("text-xs font-mono")

# ---------------------------------------------------------------------------
# THE CONCEPT TREE
# ---------------------------------------------------------------------------

with ui.column().classes("w-full max-w-5xl mx-auto p-4"):

    # ===== Level 0: the composite action ================================
    with concept("The composite action S",
                 "Add together everything physics has separately "
                 "established. That is all this equation does.",
                 icon="functions", opened=True, anchor="c-root"):
        equation(master_eq.MASTER_EQUATION_LINES[0])
        ui.markdown(master_eq.DEFINITION_TEXT).classes("text-sm")
        with at_level(ui.element("div").classes("w-full"), 1):
            ui.markdown(master_eq.WHAT_IT_IS_NOT).classes(
                "text-sm bg-[#1c2128] rounded p-3")

        # ----- Level 1: gravity ----------------------------------------
        with concept("S_gravity — spacetime curves in response to energy",
                     "One sentence: matter tells spacetime how to curve.",
                     icon="public", anchor="c-gravity"):
            equation(master_eq.MASTER_EQUATION_LINES[1])

            # Interactive moment: curvature you can drive
            with concept("Feel the curvature (interactive moment)",
                         "Turn the mass dial; the curvature well deepens.",
                         icon="play_circle"):
                curv_plot = ui.plotly(_dark(
                    p4d.spacetime_curvature_figure(mass=1.0, grid=40),
                    height=420)).classes("w-full")
                with ui.row().classes("items-center gap-8"):
                    with ui.column().classes("items-center"):
                        mass_knob = ui.knob(1.0, min=0.2, max=10.0,
                                            step=0.2, show_value=True) \
                            .props("size=64px color=primary "
                                   "track-color=grey-9")
                        ui.label("mass [M☉] — a dial").classes(
                            "text-xs text-gray-500")
                    with at_level(ui.column().classes("items-center"), 1):
                        grid_knob = ui.knob(40, min=20, max=90, step=5,
                                            show_value=True) \
                            .props("size=64px color=secondary "
                                   "track-color=grey-9")
                        ui.label("grid resolution").classes(
                            "text-xs text-gray-500")

                def _update_curv():
                    fig = _dark(p4d.spacetime_curvature_figure(
                        mass=float(mass_knob.value),
                        grid=int(grid_knob.value)), height=420)
                    curv_plot.update_figure(fig)
                mass_knob.on_value_change(lambda _: _update_curv())
                grid_knob.on_value_change(lambda _: _update_curv())
                stop_note("The graphic IS the explanation: curvature "
                          "scales with the Schwarzschild radius 2GM/c².")

            # Deeper components of the gravity concept
            with concept("Λ — the cosmological constant",
                         "A constant energy of empty space. It has UNITS.",
                         icon="straighten"):
                equation(r"\Lambda = 1.1056\times10^{-52}\ \mathrm{m^{-2}}"
                         r"\quad\text{(Planck 2018)}")
                ui.markdown(
                    "A dimensionless Λ is *meaningless* — exactly the "
                    "error the independent evaluation found in the "
                    "pre-2026 corpus, fixed everywhere since. The "
                    "*smallness* of this number versus quantum-field-"
                    "theory expectations is the cosmological-constant "
                    "problem (Weinberg 1989).").classes("text-sm")
                stop_note()

            with at_level(concept(
                    "Why can't we just quantize this?",
                    "Because perturbative quantum gravity destroys "
                    "itself at two loops.", icon="report"), 1):
                ui.markdown(
                    "'t Hooft–Veltman (1974) showed one-loop divergences "
                    "appear with matter; **Goroff–Sagnotti (1986)** found "
                    "a divergent two-loop counterterm cubic in the Weyl "
                    "tensor. Pure Einstein gravity, treated "
                    "perturbatively, needs infinitely many independent "
                    "counterterms — it loses predictivity. Every serious "
                    "unification program is, at heart, a proposed cure. "
                    "This project does **not** cure it (Open Problem 3)."
                ).classes("text-sm")
                stop_note("A stop by honesty: no one has taken this "
                          "branch further yet.")

            with at_level(concept(
                    "Competing programs: LQG and strings",
                    "Alternative gravities are rivals, not ingredients.",
                    icon="alt_route"), 1):
                ui.markdown(master_eq.REMARK_GRAVITY_PROGRAMS).classes(
                    "text-sm")
                stop_note()

        # ----- Level 1: matter -------------------------------------------
        with concept("S_matter — all matter: fermions plus the Higgs",
                     "Electrons, quarks, neutrinos — and the field that "
                     "gives them mass.",
                     icon="grain", anchor="c-matter"):
            equation(master_eq.MASTER_EQUATION_LINES[2])

            with concept("The Higgs potential (interactive moment)",
                         "A Mexican hat: the symmetric point is unstable; "
                         "the field must choose.",
                         icon="play_circle"):
                equation(master_eq.HIGGS_POTENTIAL)
                higgs_plot = ui.plotly(_dark(
                    p4d.higgs_potential_figure(grid=60), height=400)) \
                    .classes("w-full")
                ui.markdown(
                    "Rotate the hat: every direction around the brim is "
                    "an equally good vacuum. *Choosing one* is "
                    "spontaneous symmetry breaking; the ripples along "
                    "the brim are Goldstone modes eaten by the W and Z; "
                    "the radial ripple is the Higgs boson."
                ).classes("text-sm")
                stop_note()

            with at_level(concept(
                    "ψ — Dirac fermions in curved spacetime",
                    "Matter that spins, coupled to both gravity and the "
                    "forces.", icon="rotate_right"), 1):
                ui.markdown(
                    "$\\bar\\psi(i\\gamma^\\mu D_\\mu - m)\\psi$: the "
                    "covariant derivative $D_\\mu$ carries *both* the "
                    "spin connection (gravity) and the gauge potentials "
                    "(forces) — one derivative, every interaction. The "
                    "$\\sqrt{-g}$ ties matter to spacetime volume."
                ).classes("text-sm")
                stop_note()

        # ----- Level 1: gauge + the unification cascade ------------------
        with concept("S_gauge — forces are geometry in internal space",
                     "Electromagnetism, the weak and the strong force: "
                     "all curvature of internal symmetry spaces.",
                     icon="device_hub", anchor="c-gauge"):
            equation(master_eq.MASTER_EQUATION_LINES[3])
            equation(master_eq.FIELD_STRENGTH)

            # THE interactive moment: RG unification with full controls
            with concept("Do the three forces become one? "
                         "(the central interactive moment)",
                         "Run the couplings yourself. SM: a near miss. "
                         "MSSM: they meet.",
                         icon="play_circle", opened=True):

                rg_state = dict(models=("SM", "MSSM"), loops=2,
                                m_susy=1000.0, thr=3.0,
                                aem=rg.ALPHA_EM_INV_MZ,
                                s2w=rg.SIN2_THETA_W_MZ,
                                als=rg.ALPHA_S_MZ)

                with ui.row().classes("items-center gap-4 flex-wrap"):
                    model_toggle = ui.toggle(
                        ["SM", "MSSM", "Both"], value="Both") \
                        .props("rounded unelevated "
                               "toggle-color=primary ripple")
                    loops_toggle = ui.toggle({1: "1-loop", 2: "2-loop"},
                                             value=2) \
                        .props("rounded unelevated "
                               "toggle-color=secondary ripple")

                with at_level(ui.row().classes(
                        "items-end gap-10 flex-wrap mt-2"), 1):
                    with ui.column().classes("items-center"):
                        msusy_knob = ui.knob(1000, min=300, max=10000,
                                             step=100, show_value=True) \
                            .props("size=72px color=primary "
                                   "track-color=grey-9")
                        ui.label("m_SUSY [GeV] — dial").classes(
                            "text-xs text-gray-500")
                    with ui.column().classes("items-center"):
                        thr_knob = ui.knob(3.0, min=0.5, max=10.0,
                                           step=0.5, show_value=True) \
                            .props("size=72px color=secondary "
                                   "track-color=grey-9")
                        ui.label("unification criterion [%]").classes(
                            "text-xs text-gray-500")

                with at_level(ui.column().classes("w-full mt-2"), 2):
                    ui.label("EXPERT: the experimental inputs as levers — "
                             "feel how unification depends on what we "
                             "measured at M_Z").classes(
                        "text-xs uppercase text-amber-400")
                    with ui.row().classes("items-end gap-12 mt-1"):
                        lever_defs = [
                            ("α_em⁻¹(M_Z)", "aem", 126.5, 129.5, 0.01),
                            ("sin²θ_W(M_Z)", "s2w", 0.225, 0.238, 0.0001),
                            ("α_s(M_Z)", "als", 0.110, 0.126, 0.0002),
                        ]
                        levers = {}
                        for label_t, key, lo, hi, step in lever_defs:
                            with ui.column().classes("items-center"):
                                levers[key] = ui.slider(
                                    min=lo, max=hi, step=step,
                                    value=rg_state[key]) \
                                    .props("vertical reverse label-always "
                                           "color=amber") \
                                    .classes("h-40")
                                ui.label(label_t).classes(
                                    "text-xs text-gray-500")
                        with ui.column().classes("items-center gap-2"):
                            ui.button("Reset to PDG 2024",
                                      icon="restart_alt",
                                      on_click=lambda: _reset_pdg()) \
                                .props("push glossy color=amber-8 ripple")
                            ui.label("buttons push back").classes(
                                "text-xs text-gray-600")

                rg_plot = ui.plotly(_dark(rg.make_rg_figure_plotly(
                    models=("SM", "MSSM"), loops=2), height=460)) \
                    .classes("w-full mt-2")
                verdict_row = ui.row().classes("gap-2 flex-wrap mt-1")

                def _recompute_rg():
                    models = (("SM", "MSSM")
                              if model_toggle.value == "Both"
                              else (model_toggle.value,))
                    kw = dict(loops=int(loops_toggle.value),
                              m_susy=float(msusy_knob.value),
                              alpha_em_inv=float(levers["aem"].value),
                              sin2_theta_w=float(levers["s2w"].value),
                              alpha_s=float(levers["als"].value))
                    # build traces with the (possibly perturbed) inputs
                    import plotly.graph_objects as go
                    from plotly.subplots import make_subplots
                    fig = make_subplots(
                        rows=1, cols=len(models), shared_yaxes=True,
                        subplot_titles=list(models))
                    colors = ["#1f77b4", "#d62728", "#2ca02c"]
                    names = ["α₁⁻¹", "α₂⁻¹", "α₃⁻¹"]
                    verdict_row.clear()
                    for c, model in enumerate(models, start=1):
                        mu, a_inv = rg.run_couplings(model=model, **kw)
                        uni = rg.find_unification(mu, a_inv)
                        x = np.log10(mu)
                        for i in range(3):
                            fig.add_trace(
                                go.Scatter(x=x, y=a_inv[i], mode="lines",
                                           line=dict(color=colors[i],
                                                     width=2),
                                           name=names[i],
                                           showlegend=(c == 1)),
                                row=1, col=c)
                        if uni["M_GUT"] is None:
                            continue
                        unifies = uni["mismatch"] < thr_knob.value / 100
                        tau = rg.proton_lifetime_years(
                            uni["M_GUT"], 1.0 / uni["alpha_gut_inv"])
                        with verdict_row:
                            ui.badge(
                                f"{model}: mismatch "
                                f"{100 * uni['mismatch']:.1f}% — "
                                + ("UNIFIES" if unifies else "near miss"),
                                color="green" if unifies else "red") \
                                .props("rounded outline")
                            ui.badge(
                                f"{model}: M_GUT {uni['M_GUT']:.1e} GeV, "
                                f"τ_p {tau:.0e} yr "
                                + ("> Super-K ✓"
                                   if tau > rg.SUPERK_TAU_P_BOUND_YR
                                   else "< Super-K ✗ EXCLUDED"),
                                color="green"
                                if tau > rg.SUPERK_TAU_P_BOUND_YR
                                else "red").props("rounded outline")
                    fig.update_layout(height=460, **PLOTLY_DARK)
                    fig.update_xaxes(title_text="log₁₀(μ/GeV)")
                    fig.update_yaxes(title_text="αᵢ⁻¹", col=1)
                    rg_plot.update_figure(fig)

                def _reset_pdg():
                    levers["aem"].value = rg.ALPHA_EM_INV_MZ
                    levers["s2w"].value = rg.SIN2_THETA_W_MZ
                    levers["als"].value = rg.ALPHA_S_MZ
                    _recompute_rg()

                for ctrl in (model_toggle, loops_toggle, msusy_knob,
                             thr_knob, *levers.values()):
                    ctrl.on_value_change(lambda _: _recompute_rg())
                _recompute_rg()

                # Deeper: where the 5/3 comes from
                with at_level(concept(
                        "Where does the 5/3 in α₁ come from?",
                        "From the embedding itself — derived, not "
                        "assumed.", icon="calculate"), 1):
                    ui.markdown(gut.assignment_table_markdown()).classes(
                        "text-sm")
                    s = gut.summary()
                    a = s["anomalies"]
                    with ui.row().classes("gap-2 flex-wrap mt-2"):
                        for text in (
                                f"Tr(Y²) = {s['tr_Y2']}",
                                f"α₁/α_Y = {s['normalization_factor']}",
                                f"ΣY = {a['sum_Y']}",
                                f"ΣY³ = {a['sum_Y3']}",
                                "SO(10): 16 = 10 ⊕ 5̄ ⊕ 1"):
                            ui.badge(text, color="green").props(
                                "rounded outline")

                    # Deepest: the proton must decay
                    with at_level(concept(
                            "…and then the proton must decay",
                            "Unification predicts proton decay; "
                            "Super-Kamiokande keeps the receipts.",
                            icon="hourglass_bottom"), 1):
                        equation(r"\tau_p \sim "
                                 r"\frac{M_{\rm GUT}^4}"
                                 r"{\alpha_{\rm GUT}^2\, m_p^5}")
                        ui.markdown(
                            "Spin the **m_SUSY dial** above and watch "
                            "the τ_p badge: the MSSM point sits above "
                            "the Super-K bound (2.4×10³⁴ yr); the SM "
                            "near-miss scale is excluded by four orders "
                            "of magnitude — the classic demise of "
                            "minimal SU(5). Order-of-magnitude estimate "
                            "only.").classes("text-sm")
                        stop_note("Experiment gets the last word. "
                                  "That is the point.")

        # ----- Level 1: quantum -------------------------------------------
        with concept("S_quantum — corrections, loop by loop",
                     "Every process is the sum of all the ways it could "
                     "have happened.",
                     icon="all_inclusive", anchor="c-quantum"):
            equation(master_eq.MASTER_EQUATION_LINES[4])
            ui.markdown(
                "The organizing statement of perturbation theory: an "
                "expansion in powers of $\\hbar$. **The catch:** writing "
                "it down presupposes a perturbatively consistent theory "
                "— precisely what the gravity sector lacks (see *Why "
                "can't we just quantize this?* above)."
            ).classes("text-sm")
            stop_note()

    # ===== Level 0: the fourth dimension ==================================
    with concept("Seeing the fourth dimension",
                 "You cannot look at 4D — but you can project it, slice "
                 "it, or animate it. Three honest techniques.",
                 icon="view_in_ar", anchor="c-4d"):

        with concept("Projection (interactive moment)",
                     "Rotate in 4-space, then cast a 3D shadow — exactly "
                     "as your screen casts a 2D shadow of 3D.",
                     icon="play_circle"):
            ui.plotly(_dark(p4d.tesseract_figure(n_frames=36),
                            height=480)).classes("w-full")
            stop_note("Vertex color is the 4th coordinate w. The "
                      "'inner' and 'outer' cubes trade places — that "
                      "swap is the 4D rotation.")

        with concept("Slicing (interactive moment)",
                     "Drag the hyperplane through w and watch the "
                     "cross-section live and die.",
                     icon="play_circle"):
            slice_plot = ui.plotly(_dark(p4d.tesseract_slice_figure(0.0),
                                         height=420)).classes("w-full")
            with ui.row().classes("items-center gap-6"):
                with ui.column().classes("items-center"):
                    w_knob = ui.knob(0.0, min=-1.5, max=1.5, step=0.05,
                                     show_value=True) \
                        .props("size=72px color=primary "
                               "track-color=grey-9")
                    ui.label("hyperplane w — a dial through the 4th "
                             "dimension").classes("text-xs text-gray-500")
            w_knob.on_value_change(lambda e: slice_plot.update_figure(
                _dark(p4d.tesseract_slice_figure(float(e.value)),
                      height=420)))
            stop_note("Inside |w| ≤ 1 every slice is the same cube "
                      "(tesseract = cube × interval); at |w| = 1 it "
                      "vanishes at once.")

        with at_level(concept(
                "Time as the fourth coordinate",
                "A ripple in spacetime, with t as the animation axis.",
                icon="play_circle"), 1):
            ui.plotly(_dark(p4d.spacetime_evolution_figure(
                grid=50, n_frames=24), height=440)).classes("w-full")
            stop_note()

    # ===== Level 0: DIMENSION DRIVE =======================================
    with concept("DIMENSION DRIVE — the interactive geometry deck",
                 "Sci-fi skin, honest mathematics: spin a triangle into "
                 "a circle, master 3D in its three planes, engage 4D, "
                 "draw your own shape and spin it, and fall into the "
                 "Mandelbrot set.",
                 icon="rocket_launch", anchor="c-drive"):
        from visualization import dimension_drive as dd

        with concept("SPIN DECK — triangle → circle → square",
                     "One fixed point, one dial. The golden-angle "
                     "preset grows a sunflower.",
                     icon="play_circle", opened=True):
            dd.build_spin_deck()
            stop_note("Precision is the display: θ to a thousandth of "
                      "a degree on the readout.")

        with concept("SCENE DECK — a true three.js stage (ui.scene)",
                     "Orbit the camera with your mouse; drive the cube, "
                     "globe, or pyramid with plane↔axis dials.",
                     icon="view_in_ar"):
            dd.build_scene_deck()
            stop_note("In 3D every plane has a normal axis — that is "
                      "the luxury the next deck takes away.")

        with concept("XYZ DECK — mastery over 3D, then ENGAGE 4D",
                     "Cube, globe, or pyramid under three plane "
                     "controllers; one button adds the other three "
                     "planes of 4D.",
                     icon="threed_rotation"):
            dd.build_xyz_deck()
            stop_note("From mastery of 3D, 4D is expressed: three "
                      "planes become six. Nothing else changes.")

        with concept("DRAW DECK — your pointer, connected",
                     "Mouse and touch drawing for fun; then your sketch "
                     "gets the triangle treatment.",
                     icon="gesture"):
            dd.build_draw_deck()

        with at_level(concept("MANDELBROT MODE — z ← z² + c",
                              "Infinite structure from a one-line rule "
                              "(and honestly unrelated to unification).",
                              icon="all_out"), 1):
            dd.build_mandelbrot_deck()
            stop_note("Iteration depth is the accuracy dial; the "
                      "readout shows the exact complex window.")

    # ===== Level 0: the honest conclusion ==================================
    with concept("The honest conclusion",
                 "What all of the above is — and is not.",
                 icon="gavel", anchor="c-conclusion"):
        ui.markdown(
            "This Control Room is a **pedagogical and computational "
            "framework**. The composite action *organizes*; it does not "
            "unify. The quantitative content — the RG running you drove "
            "above, the embedding arithmetic, the proton-lifetime "
            "estimate — is a faithful reproduction of known results, "
            "kept honest by an independent academic evaluation whose "
            "findings are addressed point-by-point in "
            "`docs/CONCLUSION.md`. What remains open is stated as Open "
            "Problems 1–5 in `docs/THEORY.md`: a real unifying group "
            "with full dynamics, derived inter-sector couplings, a cure "
            "for non-renormalizability, selection among the gravity "
            "programs, and a novel falsifiable prediction. None is "
            "solved here. None is solved anywhere."
        ).classes("text-sm")
        with ui.row().classes("gap-2 mt-2"):
            ui.button("docs/CONCLUSION.md", icon="description",
                      on_click=lambda: ui.navigate.to(
                          "https://github.com/GrandUnifiedTheoryOf"
                          "Everything/gutoe/blob/main/docs/CONCLUSION.md",
                          new_tab=True)) \
                .props("push glossy ripple color=primary")
            ui.button("The independent evaluation", icon="rate_review",
                      on_click=lambda: ui.notify(
                          "PDF in the repository root: \"Professor "
                          "Codephreak's GUToE: An Independent Academic "
                          "Evaluation\"", type="info")) \
                .props("push glossy ripple color=secondary")

# Typeset MathJax after the client connects (content is in the DOM even
# inside collapsed expansions, so one pass covers everything).
ui.timer(1.5, _typeset, once=True)
ui.timer(4.0, _typeset, once=True)


if __name__ in {"__main__", "__mp_main__"}:
    print(f"GUToE Control Room v{VERSION} -> http://127.0.0.1:8051")
    ui.run(host="127.0.0.1", port=8051, title="GUToE Control Room",
           reload=False, show=False)

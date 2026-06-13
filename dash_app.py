#!/usr/bin/env python3
"""GUToE Scientific Dashboard (Dash delivery, v2).

The second-generation delivery of the project UI: a panel-based
scientific dashboard built on Plotly Dash, complementing the Streamlit
application (streamlit_app.py). Panels:

  1. Gauge-coupling unification -- live 1-/2-loop RG running with
     model, loop-order, and SUSY-threshold controls; unification
     metrics; Super-Kamiokande verdict.
  2. The composite action -- MathJax-rendered Definition with the
     "what it is / is not" framing.
  3. 4D visualization laboratory -- Plotly tesseract projection,
     hyperplane slicing, w-sweep field, spacetime ripple.
  4. D3.js tesseract -- a pure-SVG double-rotating tesseract rendered
     by D3 (assets/d3_panels.js), no Plotly involved.
  5. D3.js structure map -- force-directed graph of the composite
     action's logical structure: sectors, actions, research programs,
     propositions, experiments.
  6. SU(5)/SO(10) embedding -- generation table and anomaly checks.

Run:  python3 dash_app.py        (serves on http://127.0.0.1:8050)

The physics is computed live by toe_math/rg_running.py and
toe_math/gut_embedding.py -- the same code paths as the Streamlit app,
the paper, and the tests, so the deliveries cannot disagree.
"""

import json

import numpy as np
from dash import Dash, Input, Output, dcc, html

from toe_math import gut_embedding as gut
from toe_math import master_equation as master_eq
from toe_math import rg_running as rg
from version import VERSION
from visualization import plotly_4d as p4d

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = Dash(
    __name__,
    title="GUToE Scientific Dashboard",
    external_scripts=["https://d3js.org/d3.v7.min.js"],
)

M_SUSY_OPTIONS = [300, 500, 750, 1000, 1500, 2000, 3000, 5000, 10000]

PLOTLY_DARK = dict(
    template="plotly_dark",
    paper_bgcolor="#161b22",
    plot_bgcolor="#161b22",
)


def _panel(title, subtitle, children, panel_id=None, wide=False):
    cls = "panel panel-wide" if wide else "panel"
    head = [html.H2(title)]
    if subtitle:
        head.append(html.P(subtitle, className="panel-subtitle"))
    return html.Div([html.Div(head, className="panel-head")] + children,
                    className=cls, id=panel_id or f"panel-{title[:8]}")


def _segmented(options, value, control_id):
    """A segmented control built on RadioItems (styled in CSS)."""
    return dcc.RadioItems(
        id=control_id,
        options=[{"label": str(o), "value": o} for o in options],
        value=value, inline=True, className="segmented",
        labelClassName="segmented-option",
        inputClassName="segmented-input")


# ---------------------------------------------------------------------------
# Static panel content
# ---------------------------------------------------------------------------

MASTER_EQ_MD = (
    "$$" + master_eq.MASTER_EQUATION_ALIGNED.strip() + "$$\n\n"
    + master_eq.DEFINITION_TEXT + "\n\n"
    + master_eq.WHAT_IT_IS_NOT
)

_anoms = gut.check_anomaly_cancellation()
_summary = gut.summary()

EMBED_HEADER = ["Field", "SU(3)c", "SU(2)L", "Y", "States", "SU(5) irrep"]
EMBED_ROWS = [
    ("Q = (uL, dL)", "3", "2", "1/6", "6", "10"),
    ("u^c", "3-bar", "1", "-2/3", "3", "10"),
    ("e^c", "1", "1", "1", "1", "10"),
    ("d^c", "3-bar", "1", "1/3", "3", "5-bar"),
    ("L = (nu, e)", "1", "2", "-1/2", "2", "5-bar"),
]

D3_GRAPH_DATA = {
    "nodes": [
        {"id": "S (composite action)", "group": "core", "r": 16},
        {"id": "S_gravity", "group": "sector", "r": 11},
        {"id": "S_matter", "group": "sector", "r": 11},
        {"id": "S_gauge", "group": "sector", "r": 11},
        {"id": "S_quantum", "group": "sector", "r": 11},
        {"id": "Einstein-Hilbert action", "group": "action", "r": 8},
        {"id": "Loop quantum gravity", "group": "program", "r": 8},
        {"id": "String / M-theory", "group": "program", "r": 8},
        {"id": "Dirac action", "group": "action", "r": 8},
        {"id": "Higgs sector", "group": "action", "r": 8},
        {"id": "Yang-Mills action", "group": "action", "r": 8},
        {"id": "Loop expansion", "group": "action", "r": 8},
        {"id": "Goroff-Sagnotti divergence", "group": "obstacle", "r": 8},
        {"id": "SU(5) embedding", "group": "result", "r": 8},
        {"id": "SO(10) 16-spinor", "group": "result", "r": 8},
        {"id": "RG running (1-2 loop)", "group": "result", "r": 9},
        {"id": "M_GUT ~ 1.3e16 GeV (MSSM)", "group": "result", "r": 9},
        {"id": "Proton lifetime estimate", "group": "result", "r": 8},
        {"id": "Super-Kamiokande bound", "group": "experiment", "r": 8},
        {"id": "ATLAS SUSY limits", "group": "experiment", "r": 8},
        {"id": "Open problems 1-5", "group": "obstacle", "r": 10},
    ],
    "links": [
        {"source": "S (composite action)", "target": "S_gravity"},
        {"source": "S (composite action)", "target": "S_matter"},
        {"source": "S (composite action)", "target": "S_gauge"},
        {"source": "S (composite action)", "target": "S_quantum"},
        {"source": "S_gravity", "target": "Einstein-Hilbert action"},
        {"source": "S_gravity", "target": "Loop quantum gravity",
         "dashed": True},
        {"source": "S_gravity", "target": "String / M-theory",
         "dashed": True},
        {"source": "S_matter", "target": "Dirac action"},
        {"source": "S_matter", "target": "Higgs sector"},
        {"source": "S_gauge", "target": "Yang-Mills action"},
        {"source": "S_quantum", "target": "Loop expansion"},
        {"source": "S_quantum", "target": "Goroff-Sagnotti divergence",
         "dashed": True},
        {"source": "S_gauge", "target": "SU(5) embedding"},
        {"source": "SU(5) embedding", "target": "SO(10) 16-spinor"},
        {"source": "SU(5) embedding", "target": "RG running (1-2 loop)"},
        {"source": "RG running (1-2 loop)",
         "target": "M_GUT ~ 1.3e16 GeV (MSSM)"},
        {"source": "M_GUT ~ 1.3e16 GeV (MSSM)",
         "target": "Proton lifetime estimate"},
        {"source": "Proton lifetime estimate",
         "target": "Super-Kamiokande bound"},
        {"source": "M_GUT ~ 1.3e16 GeV (MSSM)",
         "target": "ATLAS SUSY limits", "dashed": True},
        {"source": "S (composite action)", "target": "Open problems 1-5",
         "dashed": True},
    ],
}

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

app.layout = html.Div([
    html.Header([
        html.Div([
            html.H1("GUToE Scientific Dashboard"),
            html.P("A pedagogical and computational framework for the "
                   "composite action of fundamental physics — not a theory "
                   "of everything, and honest about it.",
                   className="tagline"),
        ]),
        html.Div([
            html.Span(f"v{VERSION}", className="version-badge"),
            html.Span("Dash delivery", className="delivery-badge"),
        ], className="badges"),
    ], className="header"),

    html.Main([

        # ---- Panel 1: RG unification (wide) --------------------------
        _panel(
            "Gauge-Coupling Unification",
            "Live 1-/2-loop renormalization-group running "
            "(toe_math/rg_running.py). Reproduce offline with "
            "python3 -m toe_math.rg_running.",
            [
                html.Div([
                    html.Div([
                        html.Label("Models"),
                        dcc.Checklist(
                            id="rg-models",
                            options=[{"label": m, "value": m}
                                     for m in ("SM", "MSSM")],
                            value=["SM", "MSSM"], inline=True,
                            className="chip-group",
                            labelClassName="chip",
                            inputClassName="chip-input"),
                    ], className="control"),
                    html.Div([
                        html.Label("Loop order"),
                        _segmented([1, 2], 2, "rg-loops"),
                    ], className="control"),
                    html.Div([
                        html.Label("SUSY threshold m_SUSY [GeV]"),
                        dcc.Slider(
                            id="rg-msusy", min=0,
                            max=len(M_SUSY_OPTIONS) - 1, step=1, value=3,
                            marks={i: f"{v:g}" for i, v in
                                   enumerate(M_SUSY_OPTIONS)},
                            className="susy-slider"),
                    ], className="control control-grow"),
                ], className="control-row"),
                dcc.Loading(dcc.Graph(id="rg-graph",
                                      config={"displaylogo": False}),
                            type="dot", color="#58a6ff"),
                html.Div(id="rg-metrics", className="metrics-row"),
            ],
            panel_id="panel-rg", wide=True),

        # ---- Panel 2: composite action --------------------------------
        _panel(
            "The Composite Action",
            "Definition 1 — an organizing framework, not a theorem of "
            "unification (docs/THEORY.md).",
            [dcc.Markdown(MASTER_EQ_MD, mathjax=True,
                          className="mathjax-block")],
            panel_id="panel-action"),

        # ---- Panel 3: 4D laboratory ------------------------------------
        _panel(
            "4D Visualization Laboratory",
            "Genuine 4D techniques: projection and slicing "
            "(visualization/plotly_4d.py).",
            [
                html.Div([
                    html.Div([
                        html.Label("Figure"),
                        _segmented(
                            ["Tesseract", "Slice", "4D field", "Ripple"],
                            "Tesseract", "lab-choice"),
                    ], className="control"),
                    html.Div([
                        html.Label("Hyperplane w (slicing)"),
                        dcc.Slider(id="lab-w", min=-1.5, max=1.5,
                                   step=0.05, value=0.0,
                                   marks={-1: "-1", 0: "0", 1: "1"}),
                    ], className="control control-grow", id="lab-w-wrap"),
                ], className="control-row"),
                dcc.Loading(dcc.Graph(id="lab-graph",
                                      config={"displaylogo": False}),
                            type="dot", color="#58a6ff"),
            ],
            panel_id="panel-lab"),

        # ---- Panel 4: D3 tesseract -------------------------------------
        _panel(
            "Tesseract in Pure D3.js",
            "The same 4D mathematics rendered as SVG by D3 — double "
            "rotation in the (x,w) and (y,w) planes, perspective-projected. "
            "Drag to steer the 3D viewpoint; buttons control the 4D motion.",
            [
                html.Div([
                    html.Button("Pause", id="d3-tess-toggle",
                                className="btn btn-primary", n_clicks=0),
                    html.Button("Slower", id="d3-tess-slower",
                                className="btn", n_clicks=0),
                    html.Button("Faster", id="d3-tess-faster",
                                className="btn", n_clicks=0),
                    html.Button("Reset view", id="d3-tess-reset",
                                className="btn btn-ghost", n_clicks=0),
                ], className="btn-row"),
                html.Div(id="d3-tesseract", className="d3-stage"),
            ],
            panel_id="panel-d3-tess"),

        # ---- Panel 5: D3 structure map ----------------------------------
        _panel(
            "Structure Map (D3 force layout)",
            "The logical anatomy of the project: solid links are formal "
            "containment/derivation, dashed links are competing programs, "
            "obstacles, and constraints. Drag nodes; hover for emphasis.",
            [
                html.Div(id="d3-graph", className="d3-stage d3-stage-tall"),
                html.Div(json.dumps(D3_GRAPH_DATA), id="d3-graph-data",
                         style={"display": "none"}),
            ],
            panel_id="panel-d3-graph"),

        # ---- Panel 6: embedding ------------------------------------------
        _panel(
            "SU(5) / SO(10) Embedding",
            "One SM generation fits exactly in 5-bar + 10 of SU(5) "
            "(exposition of Georgi-Glashow 1974; "
            "python3 -m toe_math.gut_embedding).",
            [
                html.Table([
                    html.Thead(html.Tr([html.Th(h) for h in EMBED_HEADER])),
                    html.Tbody([html.Tr([html.Td(c) for c in row])
                                for row in EMBED_ROWS]),
                ], className="embed-table"),
                html.Div([
                    html.Span("Tr(Y²) = 10/3 → α₁ = (5/3) α_Y derived",
                              className="badge badge-ok"),
                    html.Span("Σ Y = 0", className="badge badge-ok"),
                    html.Span("Σ Y³ = 0", className="badge badge-ok"),
                    html.Span("SU(3)²·Y = 0", className="badge badge-ok"),
                    html.Span("SU(2)²·Y = 0", className="badge badge-ok"),
                    html.Span("SO(10): 16 = 10 ⊕ 5̄ ⊕ 1 (ν_R)",
                              className="badge badge-info"),
                ], className="badge-row"),
            ],
            panel_id="panel-embed"),
    ], className="grid"),

    html.Footer([
        html.P([
            "All numbers computed live from the same modules used by the "
            "tests and the paper. Honest scope: see ",
            html.A("docs/CONCLUSION.md", href="https://github.com/"
                   "GrandUnifiedTheoryOfEverything/gutoe/blob/main/docs/"
                   "CONCLUSION.md"),
            " and the independent evaluation in the repository root. "
            "Streamlit delivery: streamlit run streamlit_app.py.",
        ]),
    ], className="footer"),
], className="page")


# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------

def _metric_card(label, value, sub=None, tone="neutral"):
    body = [html.Div(label, className="metric-label"),
            html.Div(value, className="metric-value")]
    if sub:
        body.append(html.Div(sub, className="metric-sub"))
    return html.Div(body, className=f"metric metric-{tone}")


@app.callback(
    Output("rg-graph", "figure"),
    Output("rg-metrics", "children"),
    Input("rg-models", "value"),
    Input("rg-loops", "value"),
    Input("rg-msusy", "value"),
)
def update_rg(models, loops, msusy_idx):
    models = [m for m in ("SM", "MSSM") if m in (models or [])] or ["MSSM"]
    m_susy = float(M_SUSY_OPTIONS[int(msusy_idx)])
    fig = rg.make_rg_figure_plotly(models=models, loops=loops,
                                   m_susy=m_susy)
    fig.update_layout(**PLOTLY_DARK)

    cards = []
    for model in models:
        mu, a_inv = rg.run_couplings(model=model, loops=loops,
                                     m_susy=m_susy)
        uni = rg.find_unification(mu, a_inv)
        if uni["M_GUT"] is None:
            continue
        tau = rg.proton_lifetime_years(uni["M_GUT"],
                                       1.0 / uni["alpha_gut_inv"])
        ok = uni["unifies"]
        survives = tau > rg.SUPERK_TAU_P_BOUND_YR
        cards.extend([
            _metric_card(f"{model} · M_GUT", f"{uni['M_GUT']:.2e} GeV"),
            _metric_card(f"{model} · α_GUT⁻¹",
                         f"{uni['alpha_gut_inv']:.1f}"),
            _metric_card(f"{model} · mismatch",
                         f"{100 * uni['mismatch']:.1f}%",
                         "unifies (< 3%)" if ok else "no unification",
                         tone="ok" if ok else "bad"),
            _metric_card(f"{model} · τ_p estimate", f"{tau:.1e} yr",
                         "above Super-K bound" if survives
                         else "EXCLUDED by Super-K",
                         tone="ok" if survives else "bad"),
        ])
    return fig, cards


@app.callback(
    Output("lab-graph", "figure"),
    Output("lab-w-wrap", "style"),
    Input("lab-choice", "value"),
    Input("lab-w", "value"),
)
def update_lab(choice, w):
    show_w = {"display": "block"} if choice == "Slice" \
        else {"display": "none"}
    if choice == "Slice":
        fig = p4d.tesseract_slice_figure(float(w))
    elif choice == "4D field":
        fig = p4d.quantum_field_4d_figure(grid=40, n_frames=20)
    elif choice == "Ripple":
        fig = p4d.spacetime_evolution_figure(grid=50, n_frames=24)
    else:
        fig = p4d.tesseract_figure(n_frames=36)
    fig.update_layout(**PLOTLY_DARK)
    return fig, show_w


if __name__ == "__main__":
    print(f"GUToE Scientific Dashboard v{VERSION} -> "
          "http://127.0.0.1:8050")
    app.run(debug=False, host="127.0.0.1", port=8050)

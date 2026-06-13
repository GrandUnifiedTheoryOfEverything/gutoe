#!/usr/bin/env python3
"""Smoke tests for the v2 UI deliveries (Dash dashboard, NiceGUI
Control Room).

These run the callback/page-construction code paths directly, without a
browser. Run: python3 -m pytest tests/test_dashboards.py -q
"""

import os
import subprocess
import sys
import time
import urllib.request

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)


# ---------------------------------------------------------------------------
# Dash
# ---------------------------------------------------------------------------

def test_dash_app_builds_and_callbacks_run():
    os.chdir(REPO_ROOT)
    import dash_app

    fig, cards = dash_app.update_rg(["SM", "MSSM"], 2, 3)
    assert len(fig.data) == 6          # 3 couplings x 2 models
    assert len(cards) == 8             # 4 metric cards per model

    fig_t, style = dash_app.update_lab("Tesseract", 0.0)
    assert len(fig_t.frames) > 0
    assert style["display"] == "none"

    fig_s, style_s = dash_app.update_lab("Slice", 0.5)
    assert style_s["display"] == "block"

    assert dash_app.app.layout is not None
    assert dash_app.VERSION.startswith("2.")


def test_dash_assets_exist():
    for name in ("style.css", "d3_panels.js"):
        path = os.path.join(REPO_ROOT, "assets", name)
        assert os.path.exists(path), name
        assert os.path.getsize(path) > 1000, name


# ---------------------------------------------------------------------------
# NiceGUI (page construction happens at import; serving is checked by
# launching the real server briefly)
# ---------------------------------------------------------------------------

def test_nicegui_app_serves():
    proc = subprocess.Popen(
        [sys.executable, "nicegui_app.py"], cwd=REPO_ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        deadline = time.time() + 40
        status = None
        while time.time() < deadline:
            try:
                with urllib.request.urlopen(
                        "http://127.0.0.1:8051/", timeout=2) as resp:
                    status = resp.status
                    body = resp.read(20000).decode("utf-8", "replace")
                    break
            except Exception:
                time.sleep(1.0)
        assert status == 200, "NiceGUI server did not come up"
        assert "GUToE Control Room" in body
    finally:
        proc.terminate()
        proc.wait(timeout=10)


def test_rg_input_overrides():
    """The expert levers rely on run_couplings accepting input
    overrides; perturbing alpha_s must move the unification scale."""
    from toe_math import rg_running as rg
    base = rg.find_unification(*rg.run_couplings(model="MSSM", loops=1))
    pert = rg.find_unification(*rg.run_couplings(model="MSSM", loops=1,
                                                 alpha_s=0.112))
    assert base["M_GUT"] is not None and pert["M_GUT"] is not None
    assert abs(pert["M_GUT"] / base["M_GUT"] - 1) > 0.01


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))

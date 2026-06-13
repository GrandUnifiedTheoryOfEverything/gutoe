#!/usr/bin/env python3
"""Smoke test: every page of the Streamlit app renders without exception.

Run: python3 -m pytest tests/test_app_pages.py -q
(Needs to run from the repository root so relative paths resolve.)
"""

import os
import sys

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

PAGES = [
    "Home",
    "Master Equation",
    "Gauge Unification (RG)",
    "Formulas",
    "Visualizations",
    "Documentation",
    "Conclusion & Assessment",
    "References & About",
]


@pytest.fixture(scope="module")
def app():
    from streamlit.testing.v1 import AppTest
    os.chdir(REPO_ROOT)
    at = AppTest.from_file(os.path.join(REPO_ROOT, "streamlit_app.py"),
                           default_timeout=120)
    at.run()
    assert not at.exception, [str(e.value) for e in at.exception]
    return at


@pytest.mark.parametrize("page", PAGES)
def test_page_renders(app, page):
    app.sidebar.selectbox[0].set_value(page)
    app.run()
    assert not app.exception, \
        f"{page}: " + "; ".join(str(e.value)[:200] for e in app.exception)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))

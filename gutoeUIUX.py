#!/usr/bin/env python3
"""Compatibility shim: the canonical Streamlit application lives in streamlit_app.py.

`streamlit run gutoeUIUX.py` and `streamlit run streamlit_app.py` serve the
same application. This file exists only so historical references to
gutoeUIUX.py keep working without two diverging copies of the UI code.
"""

from streamlit_app import main

main()

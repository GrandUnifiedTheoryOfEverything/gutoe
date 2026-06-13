#!/usr/bin/env python3
"""
Theory of Everything (ToE) - A Unified Framework for Physics

This package provides a comprehensive framework for exploring and visualizing
the Theory of Everything, combining various physical theories into a unified model.
"""

# Import main components for easier access. Each layer is optional: the
# legacy agent modules reference a `theoryofeverything` package that does
# not exist in this repository layout, so tolerate their absence rather
# than make the whole repository unimportable (pytest imports this file
# when collecting tests).
try:
    from unified.toe_core import ToECore
    from unified.toe_formulas import FormulaTools
    from unified.toe_vis import VisualizationTools
    from unified.toe_unified import ToEUnified
except ImportError:
    ToECore = FormulaTools = VisualizationTools = ToEUnified = None

try:
    from core.agents.latexagent import LaTeXAgent
    from core.agents.pdfagent import PDFAgent
    from core.agents.toe_agent import AgentTools
except ImportError:
    LaTeXAgent = PDFAgent = AgentTools = None

# Version information
__version__ = '1.0.0'

#!/usr/bin/env python3
"""
Theory of Everything - Visualization Module

This module provides tools for visualizing the Theory of Everything.
"""

# Legacy import; the `theoryofeverything` package is not present in this
# repository layout, so tolerate its absence.
try:
    from theoryofeverything.visualization.toe_vis import VisualizationTools
except ImportError:
    VisualizationTools = None

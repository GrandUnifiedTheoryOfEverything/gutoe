#!/usr/bin/env python3
"""
Theory of Everything - Core Module

This module provides the core functionality for the Theory of Everything.
"""

# Legacy imports; the `theoryofeverything` package is not present in this
# repository layout, so tolerate its absence and fall back to the local
# module.
try:
    from theoryofeverything.core.toe_core import (
        ToECore, math_module_safe_context, load_json_safely,
        ensure_directory)
    from theoryofeverything.core import agents
except ImportError:
    try:
        from core.toe_core import (
            ToECore, math_module_safe_context, load_json_safely,
            ensure_directory)
    except ImportError:
        ToECore = None

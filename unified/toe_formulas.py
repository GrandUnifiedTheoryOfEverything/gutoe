#!/usr/bin/env python3
"""
Theory of Everything Formula Module

This module provides tools for working with formulas in the Theory of Everything,
including formula retrieval, exploration, and comparison.
"""

import json
from .toe_core import ToECore, load_json_safely


class FormulaTools:
    """
    Tools for working with formulas in the Theory of Everything
    """
    
    def __init__(self, core=None):
        """
        Initialize the formula tools
        
        Parameters:
        -----------
        core : ToECore or None
            Core API instance (will create a new one if None)
        """
        self.core = core if core is not None else ToECore()
        
        # Define the formula catalog
        self.formula_catalog = {
            'unified_action': 'The unified action (master equation)',
            'gravity_action': 'The gravity action components',
            'matter_action': 'The matter action components',
            'gauge_action': 'The gauge field action components',
            'quantum_corrections': 'The quantum corrections components',
            'full_master_equation': 'The full master equation'
        }
        
        # Define the formula relationships
        self.formula_relationships = {
            'unified_action': ['gravity_action', 'matter_action', 'gauge_action', 'quantum_corrections'],
            'gravity_action': ['full_master_equation'],
            'matter_action': ['full_master_equation'],
            'gauge_action': ['full_master_equation'],
            'quantum_corrections': ['full_master_equation'],
            'full_master_equation': []
        }
    
    def list_formulas(self):
        """
        List all available formulas
        
        Returns:
        --------
        dict
            Dictionary mapping formula names to descriptions
        """
        return self.formula_catalog
    
    def get_formula(self, formula_name):
        """
        Get a formula from the Theory of Everything
        
        Parameters:
        -----------
        formula_name : str
            Name of the formula to get
            
        Returns:
        --------
        dict
            Dictionary containing the formula information
        """
        if formula_name not in self.formula_catalog:
            raise ValueError(f"Unknown formula: {formula_name}. "
                           f"Available formulas: {list(self.formula_catalog.keys())}")
        
        # Define the script to get the formula
        script = """
import os
import sys
import json
from contextlib import contextmanager

@contextmanager
def math_module_safe_context():
    renamed = False
    if os.path.exists('math') and os.path.isdir('math'):
        os.rename('math', 'toe_math')
        renamed = True
    try:
        yield
    finally:
        if renamed and os.path.exists('toe_math') and os.path.isdir('toe_math'):
            os.rename('toe_math', 'math')

with math_module_safe_context():
    # Get the formula name
    formula_name = sys.argv[1] if len(sys.argv) > 1 else 'unified_action'
    
    # Define the formulas
    formulas = {
        'unified_action': {
            'name': 'Unified Action (Master Equation)',
            'latex': 'S = S_{\\\\text{gravity}} + S_{\\\\text{matter}} + S_{\\\\text{gauge}} + S_{\\\\text{quantum}}',
            'description': 'The total action is composed of four main parts: gravity, matter, gauge fields, and quantum corrections.',
            'components': ['gravity_action', 'matter_action', 'gauge_action', 'quantum_corrections']
        },
        'gravity_action': {
            'name': 'Gravity Action',
            'components': [
                {
                    'name': 'Einstein-Hilbert Action (Classical Gravity)',
                    'latex': 'S_{\\\\text{gravity}}^{\\\\text{EH}} = \\\\frac{1}{16\\\\pi G} \\\\int d^4x \\\\, \\\\sqrt{-g} \\\\, (R - 2\\\\Lambda)',
                    'description': 'The Einstein-Hilbert action describes classical gravity in terms of spacetime curvature.'
                },
                {
                    'name': 'Loop Quantum Gravity Extension',
                    'latex': 'S_{\\\\text{gravity}}^{\\\\text{LQG}} = \\\\frac{1}{8\\\\pi G} \\\\int d^4x \\\\, \\\\sqrt{-g} \\\\, \\\\epsilon^{abc} E_a^i E_b^j F_{ij}^c',
                    'description': 'Loop Quantum Gravity extends classical gravity to the quantum realm using Ashtekar variables.'
                },
                {
                    'name': 'String/M-Theory Gravity',
                    'latex': 'S_{\\\\text{gravity}}^{\\\\text{String}} = \\\\frac{1}{2\\\\kappa^2} \\\\int d^{10}x \\\\, \\\\sqrt{-g} \\\\, e^{-2\\\\phi} \\\\left(R + 4 (\\\\nabla \\\\phi)^2 - \\\\frac{1}{12} H_{\\\\mu\\\\nu\\\\rho} H^{\\\\mu\\\\nu\\\\rho}\\\\right)',
                    'description': 'String theory describes gravity in terms of vibrating strings in higher dimensions.'
                }
            ]
        },
        'matter_action': {
            'name': 'Matter Action',
            'components': [
                {
                    'name': 'Fermion Fields (Dirac Action)',
                    'latex': 'S_{\\\\text{fermion}} = \\\\int d^4x \\\\, \\\\sqrt{-g} \\\\, \\\\bar{\\\\psi} (i \\\\gamma^\\\\mu D_\\\\mu - m) \\\\psi',
                    'description': 'The Dirac action describes fermions (matter particles) in curved spacetime.'
                },
                {
                    'name': 'Higgs Field (Spontaneous Symmetry Breaking)',
                    'latex': 'S_{\\\\text{Higgs}} = \\\\int d^4x \\\\, \\\\sqrt{-g} \\\\, \\\\left[ (D_\\\\mu \\\\phi)^\\\\dagger (D^\\\\mu \\\\phi) - V(\\\\phi) \\\\right]',
                    'description': 'The Higgs action describes the Higgs field that gives mass to particles through spontaneous symmetry breaking.'
                }
            ]
        },
        'gauge_action': {
            'name': 'Gauge Field Action',
            'components': [
                {
                    'name': 'Yang-Mills Action (Non-Abelian Gauge Fields)',
                    'latex': 'S_{\\\\text{gauge}} = -\\\\frac{1}{4} \\\\int d^4x \\\\, \\\\sqrt{-g} \\\\, F_{\\\\mu\\\\nu}^a F^{\\\\mu\\\\nu}_a',
                    'description': 'The Yang-Mills action describes non-Abelian gauge fields that mediate the strong and weak forces.'
                },
                {
                    'name': 'Supersymmetric Gauge Fields',
                    'latex': 'S_{\\\\text{SUSY-gauge}} = \\\\int d^4x \\\\, \\\\left[ -\\\\frac{1}{4} F_{\\\\mu\\\\nu} F^{\\\\mu\\\\nu} + i \\\\bar{\\\\lambda} \\\\gamma^\\\\mu D_\\\\mu \\\\lambda \\\\right]',
                    'description': 'Supersymmetric gauge fields include both gauge bosons and their fermionic partners (gauginos).'
                }
            ]
        },
        'quantum_corrections': {
            'name': 'Quantum Corrections',
            'components': [
                {
                    'name': 'Path Integral Formulation',
                    'latex': 'Z = \\\\int \\\\mathcal{D}\\\\phi \\\\, e^{i S[\\\\phi]}',
                    'description': 'The path integral formulation describes quantum fields by integrating over all possible field configurations.'
                },
                {
                    'name': 'Loop Corrections and Renormalization',
                    'latex': 'S_{\\\\text{quantum}} = \\\\sum_{n=1}^{\\\\infty} \\\\hbar^n S_n',
                    'description': 'Loop corrections account for quantum fluctuations and virtual particles in quantum field theory.'
                }
            ]
        },
        'full_master_equation': {
            'name': 'Full Master Equation',
            'latex': 'S = \\\\frac{1}{16\\\\pi G} \\\\int d^4x \\\\, \\\\sqrt{-g} \\\\, (R - 2\\\\Lambda) + \\\\int d^4x \\\\, \\\\sqrt{-g} \\\\left[ \\\\bar{\\\\psi} (i \\\\gamma^\\\\mu D_\\\\mu - m) \\\\psi + (D_\\\\mu \\\\phi)^\\\\dagger (D^\\\\mu \\\\phi) - V(\\\\phi) - \\\\frac{1}{4} F_{\\\\mu\\\\nu}^a F^{\\\\mu\\\\nu}_a \\\\right] + \\\\sum_{n=1}^{\\\\infty} \\\\hbar^n S_n',
            'description': 'The full master equation combines all components of the Theory of Everything into a single mathematical framework.'
        }
    }
    
    # Get the requested formula
    if formula_name in formulas:
        result = formulas[formula_name]
    else:
        result = f"Unknown formula: {formula_name}"
    
    # Print the result
    print(json.dumps(result))
"""
        
        # Run the script
        result = self.core.run_with_math_safety(
            self.core.run_script_safely,
            script,
            args=[formula_name]
        )
        
        # Parse the result
        parsed_result = load_json_safely(result)
        if parsed_result is None:
            return {"error": result}
        
        return parsed_result
    
    def explore_formula(self, formula_name):
        """
        Explore a formula and its components
        
        Parameters:
        -----------
        formula_name : str
            Name of the formula to explore
            
        Returns:
        --------
        dict
            Dictionary containing the formula and its components
        """
        if formula_name not in self.formula_catalog:
            raise ValueError(f"Unknown formula: {formula_name}. "
                           f"Available formulas: {list(self.formula_catalog.keys())}")
        
        # Get the formula
        formula = self.get_formula(formula_name)
        
        # Get the components
        components = []
        if 'components' in formula:
            if isinstance(formula['components'], list):
                if all(isinstance(c, str) for c in formula['components']):
                    # Components are references to other formulas
                    for component_name in formula['components']:
                        component = self.get_formula(component_name)
                        components.append({
                            'name': component_name,
                            'formula': component
                        })
                else:
                    # Components are defined inline
                    components = formula['components']
        
        # Get the related formulas
        related_formulas = []
        for related_name, related_components in self.formula_relationships.items():
            if formula_name in related_components:
                related_formula = self.get_formula(related_name)
                related_formulas.append({
                    'name': related_name,
                    'formula': related_formula
                })
        
        return {
            'formula': formula,
            'components': components,
            'related_formulas': related_formulas
        }
    
    def compare_formulas(self, formula_names):
        """
        Compare multiple formulas
        
        Parameters:
        -----------
        formula_names : list
            List of formula names to compare
            
        Returns:
        --------
        dict
            Dictionary containing the comparison results
        """
        if not formula_names:
            raise ValueError("No formulas specified for comparison")
        
        for name in formula_names:
            if name not in self.formula_catalog:
                raise ValueError(f"Unknown formula: {name}. "
                               f"Available formulas: {list(self.formula_catalog.keys())}")
        
        # Get the formulas
        formulas = {}
        for name in formula_names:
            formulas[name] = self.get_formula(name)
        
        # Find common components
        common_components = set()
        for name, formula in formulas.items():
            if 'components' in formula and isinstance(formula['components'], list):
                if all(isinstance(c, str) for c in formula['components']):
                    # Components are references to other formulas
                    if not common_components:
                        common_components = set(formula['components'])
                    else:
                        common_components &= set(formula['components'])
        
        # Find unique components
        unique_components = {}
        for name, formula in formulas.items():
            if 'components' in formula and isinstance(formula['components'], list):
                if all(isinstance(c, str) for c in formula['components']):
                    # Components are references to other formulas
                    unique = set(formula['components']) - common_components
                    if unique:
                        unique_components[name] = list(unique)
        
        return {
            'formulas': formulas,
            'common_components': list(common_components),
            'unique_components': unique_components
        }
    
    def search_formulas(self, query):
        """
        Search for formulas matching a query
        
        Parameters:
        -----------
        query : str
            Search query
            
        Returns:
        --------
        dict
            Dictionary mapping formula names to match scores
        """
        import re
        
        query = query.lower()
        results = {}
        
        # Search in the formula catalog
        for name, description in self.formula_catalog.items():
            score = 0
            
            # Check if the query is in the name
            if query in name.lower():
                score += 3
            
            # Check if the query is in the description
            if query in description.lower():
                score += 2
            
            # Get the formula
            formula = self.get_formula(name)
            
            # Check if the query is in the formula name
            if 'name' in formula and query in formula['name'].lower():
                score += 2
            
            # Check if the query is in the formula description
            if 'description' in formula and query in formula['description'].lower():
                score += 1
            
            # Check if the query is in the formula latex
            if 'latex' in formula and query in formula['latex'].lower():
                score += 1
            
            # Add to results if there's a match
            if score > 0:
                results[name] = score
        
        # Sort by score (descending)
        return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))
    
    def get_formula_dependencies(self, formula_name):
        """
        Get the dependencies of a formula
        
        Parameters:
        -----------
        formula_name : str
            Name of the formula
            
        Returns:
        --------
        dict
            Dictionary containing the formula dependencies
        """
        if formula_name not in self.formula_catalog:
            raise ValueError(f"Unknown formula: {formula_name}. "
                           f"Available formulas: {list(self.formula_catalog.keys())}")
        
        # Get the formula
        formula = self.get_formula(formula_name)
        
        # Get the direct dependencies
        direct_dependencies = []
        if 'components' in formula and isinstance(formula['components'], list):
            if all(isinstance(c, str) for c in formula['components']):
                direct_dependencies = formula['components']
        
        # Get the indirect dependencies
        indirect_dependencies = []
        for dep in direct_dependencies:
            dep_formula = self.get_formula(dep)
            if 'components' in dep_formula and isinstance(dep_formula['components'], list):
                if all(isinstance(c, str) for c in dep_formula['components']):
                    indirect_dependencies.extend(dep_formula['components'])
        
        # Remove duplicates
        indirect_dependencies = list(set(indirect_dependencies) - set(direct_dependencies))
        
        return {
            'formula': formula,
            'direct_dependencies': direct_dependencies,
            'indirect_dependencies': indirect_dependencies
        }
    
    def export_formula_to_latex(self, formula_name):
        """
        Export a formula to LaTeX
        
        Parameters:
        -----------
        formula_name : str
            Name of the formula
            
        Returns:
        --------
        str
            LaTeX representation of the formula
        """
        if formula_name not in self.formula_catalog:
            raise ValueError(f"Unknown formula: {formula_name}. "
                           f"Available formulas: {list(self.formula_catalog.keys())}")
        
        # Get the formula
        formula = self.get_formula(formula_name)
        
        # Start with the document preamble
        latex = """\\documentclass{article}
\\usepackage{amsmath}
\\usepackage{amssymb}
\\usepackage{physics}
\\begin{document}

"""
        
        # Add the formula name and description
        latex += f"\\section{{{formula['name']}}}\n\n"
        if 'description' in formula:
            latex += f"{formula['description']}\n\n"
        
        # Add the formula itself
        if 'latex' in formula:
            latex += f"\\begin{{equation}}\n{formula['latex']}\n\\end{{equation}}\n\n"
        
        # Add the components if available
        if 'components' in formula:
            if isinstance(formula['components'], list):
                if all(isinstance(c, str) for c in formula['components']):
                    # Components are references to other formulas
                    latex += "\\section{Components}\n\n"
                    for component_name in formula['components']:
                        component = self.get_formula(component_name)
                        latex += f"\\subsection{{{component['name']}}}\n\n"
                        if 'description' in component:
                            latex += f"{component['description']}\n\n"
                        if 'latex' in component:
                            latex += f"\\begin{{equation}}\n{component['latex']}\n\\end{{equation}}\n\n"
                else:
                    # Components are defined inline
                    latex += "\\section{Components}\n\n"
                    for component in formula['components']:
                        latex += f"\\subsection{{{component['name']}}}\n\n"
                        if 'description' in component:
                            latex += f"{component['description']}\n\n"
                        if 'latex' in component:
                            latex += f"\\begin{{equation}}\n{component['latex']}\n\\end{{equation}}\n\n"
        
        # End the document
        latex += "\\end{document}"
        
        return latex

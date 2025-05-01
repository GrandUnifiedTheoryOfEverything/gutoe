#!/usr/bin/env python3
"""
Theory of Everything - Formula Tools

This module provides tools for working with mathematical formulas in the Theory of Everything.
"""

import os
import sys
import json
import re
from theoryofeverything.core.toe_core import ToECore, load_json_safely


class FormulaTools:
    """
    Tools for working with mathematical formulas
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
        
        # Load formulas from JSON files
        self.formulas = self._load_formulas()
    
    def _load_formulas(self):
        """
        Load formulas from JSON files
        
        Returns:
        --------
        dict
            Dictionary mapping formula names to formula data
        """
        formulas = {}
        
        # Define the formula files to load
        formula_files = {
            'gravity_action': 'component_formulas/gravity_action.json',
            'matter_action': 'component_formulas/matter_action.json',
            'gauge_action': 'component_formulas/gauge_action.json',
            'quantum_corrections': 'component_formulas/quantum_corrections.json',
            'unified_action': 'component_formulas/unified_action.json'
        }
        
        # Load each formula file
        for name, file_path in formula_files.items():
            formula_data = load_json_safely(file_path)
            if formula_data:
                formulas[name] = formula_data
        
        return formulas
    
    def list_formulas(self):
        """
        List all available formulas
        
        Returns:
        --------
        dict
            Dictionary mapping formula names to descriptions
        """
        return {name: data.get('description', 'No description available')
                for name, data in self.formulas.items()}
    
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
        if formula_name not in self.formulas:
            raise ValueError(f"Unknown formula: {formula_name}. "
                           f"Available formulas: {list(self.formulas.keys())}")
        
        return self.formulas[formula_name]
    
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
        formula = self.get_formula(formula_name)
        
        # Get the components of the formula
        components = formula.get('components', [])
        
        # Load the component formulas
        component_formulas = {}
        for component in components:
            if component in self.formulas:
                component_formulas[component] = self.formulas[component]
        
        return {
            'formula': formula,
            'components': component_formulas
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
        # Get the formulas
        formulas = {}
        for name in formula_names:
            try:
                formulas[name] = self.get_formula(name)
            except ValueError:
                formulas[name] = {'error': f"Unknown formula: {name}"}
        
        # Compare the formulas
        comparison = {
            'formulas': formulas,
            'common_components': [],
            'unique_components': {}
        }
        
        # Find common and unique components
        all_components = set()
        for name, formula in formulas.items():
            if 'error' not in formula:
                components = set(formula.get('components', []))
                all_components.update(components)
                comparison['unique_components'][name] = list(components)
        
        # Find common components
        for name, formula in formulas.items():
            if 'error' not in formula:
                components = set(formula.get('components', []))
                for other_name, other_formula in formulas.items():
                    if name != other_name and 'error' not in other_formula:
                        other_components = set(other_formula.get('components', []))
                        comparison['unique_components'][name] = list(
                            set(comparison['unique_components'][name]) - other_components
                        )
                        common = components.intersection(other_components)
                        for c in common:
                            if c not in comparison['common_components']:
                                comparison['common_components'].append(c)
        
        return comparison
    
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
        results = {}
        
        # Convert query to lowercase for case-insensitive matching
        query = query.lower()
        
        # Search in each formula
        for name, formula in self.formulas.items():
            score = 0
            
            # Check if query is in the name
            if query in name.lower():
                score += 3
            
            # Check if query is in the description
            description = formula.get('description', '').lower()
            if query in description:
                score += 2
            
            # Check if query is in the latex representation
            latex = formula.get('latex', '').lower()
            if query in latex:
                score += 1
            
            # Check if query is in the components
            components = formula.get('components', [])
            for component in components:
                if query in component.lower():
                    score += 1
            
            # Add to results if there's a match
            if score > 0:
                results[name] = score
        
        # Sort results by score (descending)
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
        formula = self.get_formula(formula_name)
        
        # Get the components of the formula
        components = formula.get('components', [])
        
        # Build the dependency tree
        dependencies = {
            'direct': components,
            'tree': {}
        }
        
        # Recursively get dependencies for each component
        for component in components:
            if component in self.formulas:
                component_deps = self.get_formula_dependencies(component)
                dependencies['tree'][component] = component_deps['direct']
        
        return dependencies
    
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
        formula = self.get_formula(formula_name)
        
        # Get the LaTeX representation
        latex = formula.get('latex', '')
        
        # If there's no LaTeX representation, generate one
        if not latex:
            latex = self._generate_latex_from_formula(formula)
        
        return latex
    
    def _generate_latex_from_formula(self, formula):
        """
        Generate LaTeX from a formula
        
        Parameters:
        -----------
        formula : dict
            Formula data
            
        Returns:
        --------
        str
            LaTeX representation of the formula
        """
        # Get the name and description
        name = formula.get('name', 'Unknown')
        description = formula.get('description', 'No description available')
        
        # Generate a simple LaTeX representation
        latex = f"\\section{{{name}}}\n\n{description}\n\n"
        
        # Add the equation if available
        equation = formula.get('equation', '')
        if equation:
            latex += f"\\begin{{equation}}\n{equation}\n\\end{{equation}}\n\n"
        
        # Add the components if available
        components = formula.get('components', [])
        if components:
            latex += "\\subsection{Components}\n\n"
            latex += "\\begin{itemize}\n"
            for component in components:
                latex += f"\\item {component}\n"
            latex += "\\end{itemize}\n\n"
        
        return latex

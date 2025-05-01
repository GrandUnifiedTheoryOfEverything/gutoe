#!/usr/bin/env python3
"""
Theory of Everything - Agent Tools

This module provides specialized tools for AI agents working with the Theory of Everything.
"""

import os
import sys
import json
import time
import random
from theoryofeverything.core.toe_core import ToECore, load_json_safely


class AgentTools:
    """
    Specialized tools for AI agents
    """
    
    def __init__(self, core=None):
        """
        Initialize the agent tools
        
        Parameters:
        -----------
        core : ToECore or None
            Core API instance (will create a new one if None)
        """
        self.core = core if core is not None else ToECore()
        self.session_id = self._generate_session_id()
        self.session_start_time = time.time()
        self.agent_mode_enabled = True
    
    def _generate_session_id(self):
        """
        Generate a unique session ID
        
        Returns:
        --------
        str
            Unique session ID
        """
        # Generate a random 8-character hexadecimal string
        return f"toe-{random.getrandbits(32):08x}"
    
    def is_agent_mode_enabled(self):
        """
        Check if agent mode is enabled
        
        Returns:
        --------
        bool
            True if agent mode is enabled, False otherwise
        """
        return self.agent_mode_enabled
    
    def get_session_info(self):
        """
        Get information about the current session
        
        Returns:
        --------
        dict
            Dictionary containing session information
        """
        return {
            'session_id': self.session_id,
            'session_start_time': self.session_start_time,
            'session_duration': time.time() - self.session_start_time,
            'agent_mode_enabled': self.agent_mode_enabled
        }
    
    def explore_theory(self, query=None):
        """
        Explore the Theory of Everything
        
        Parameters:
        -----------
        query : str or None
            Search query (if None, will explore the entire theory)
            
        Returns:
        --------
        dict
            Dictionary containing exploration results
        """
        if not self.agent_mode_enabled:
            raise ValueError("Agent mode is not enabled")
        
        # Define the components of the theory
        components = [
            'gravity_action',
            'matter_action',
            'gauge_action',
            'quantum_corrections',
            'unified_action'
        ]
        
        # If a query is provided, filter the components
        if query:
            query = query.lower()
            filtered_components = []
            for component in components:
                if query in component.lower():
                    filtered_components.append(component)
            components = filtered_components if filtered_components else components
        
        # Load the components
        component_data = {}
        for component in components:
            component_data[component] = load_json_safely(f"component_formulas/{component}.json")
        
        return {
            'query': query,
            'components': component_data
        }
    
    def generate_visualization_for_formula(self, formula_name):
        """
        Generate a visualization for a formula
        
        Parameters:
        -----------
        formula_name : str
            Name of the formula
            
        Returns:
        --------
        dict
            Dictionary containing the visualization results
        """
        if not self.agent_mode_enabled:
            raise ValueError("Agent mode is not enabled")
        
        # Define the mapping from formulas to visualizations
        formula_to_vis = {
            'gravity_action': '4d_spacetime_curvature',
            'matter_action': '4d_higgs_field',
            'gauge_action': 'gauge_field_4d',
            'quantum_corrections': 'quantum_foam_3d',
            'unified_action': 'extra_dimensions_3d'
        }
        
        # Check if the formula is supported
        if formula_name not in formula_to_vis:
            raise ValueError(f"Unsupported formula: {formula_name}. "
                           f"Supported formulas: {list(formula_to_vis.keys())}")
        
        # Get the visualization name
        vis_name = formula_to_vis[formula_name]
        
        # Generate the visualization
        from theoryofeverything.visualization.toe_vis import VisualizationTools
        vis_tools = VisualizationTools(self.core)
        path = vis_tools.generate_visualization(vis_name)
        
        return {
            'formula': formula_name,
            'visualization': vis_name,
            'path': path
        }
    
    def generate_visualization_sequence(self, visualization_name, param_ranges):
        """
        Generate a sequence of visualizations with varying parameters
        
        Parameters:
        -----------
        visualization_name : str
            Name of the visualization
        param_ranges : dict
            Dictionary mapping parameter names to lists of values
            
        Returns:
        --------
        dict
            Dictionary containing the visualization sequence results
        """
        if not self.agent_mode_enabled:
            raise ValueError("Agent mode is not enabled")
        
        # Check if the visualization is supported
        from theoryofeverything.visualization.toe_vis import VisualizationTools
        vis_tools = VisualizationTools(self.core)
        
        if visualization_name not in vis_tools.available_visualizations:
            raise ValueError(f"Unsupported visualization: {visualization_name}. "
                           f"Supported visualizations: {list(vis_tools.available_visualizations.keys())}")
        
        # Generate the visualizations
        results = []
        
        # Get the parameter names
        param_names = list(param_ranges.keys())
        
        # Generate all combinations of parameters
        import itertools
        param_values = [param_ranges[name] for name in param_names]
        combinations = list(itertools.product(*param_values))
        
        # Generate a visualization for each combination
        for combination in combinations:
            params = {name: value for name, value in zip(param_names, combination)}
            path = vis_tools.generate_visualization(visualization_name, params)
            results.append({
                'params': params,
                'path': path
            })
        
        return {
            'visualization': visualization_name,
            'param_ranges': param_ranges,
            'results': results
        }
    
    def extract_insights(self, formula_name=None, visualization_name=None):
        """
        Extract insights from a formula or visualization
        
        Parameters:
        -----------
        formula_name : str or None
            Name of the formula (if None, will use visualization_name)
        visualization_name : str or None
            Name of the visualization (if None, will use formula_name)
            
        Returns:
        --------
        dict
            Dictionary containing the extracted insights
        """
        if not self.agent_mode_enabled:
            raise ValueError("Agent mode is not enabled")
        
        # Check if at least one of formula_name or visualization_name is provided
        if formula_name is None and visualization_name is None:
            raise ValueError("At least one of formula_name or visualization_name must be provided")
        
        # If formula_name is provided but visualization_name is not, get the visualization for the formula
        if formula_name is not None and visualization_name is None:
            formula_to_vis = {
                'gravity_action': '4d_spacetime_curvature',
                'matter_action': '4d_higgs_field',
                'gauge_action': 'gauge_field_4d',
                'quantum_corrections': 'quantum_foam_3d',
                'unified_action': 'extra_dimensions_3d'
            }
            
            if formula_name not in formula_to_vis:
                raise ValueError(f"Unsupported formula: {formula_name}. "
                               f"Supported formulas: {list(formula_to_vis.keys())}")
            
            visualization_name = formula_to_vis[formula_name]
        
        # If visualization_name is provided but formula_name is not, get the formula for the visualization
        if visualization_name is not None and formula_name is None:
            vis_to_formula = {
                '4d_spacetime_curvature': 'gravity_action',
                '4d_higgs_field': 'matter_action',
                'gauge_field_4d': 'gauge_action',
                'quantum_foam_3d': 'quantum_corrections',
                'extra_dimensions_3d': 'unified_action'
            }
            
            if visualization_name not in vis_to_formula:
                raise ValueError(f"Unsupported visualization: {visualization_name}. "
                               f"Supported visualizations: {list(vis_to_formula.keys())}")
            
            formula_name = vis_to_formula[visualization_name]
        
        # Load the formula data
        formula_data = load_json_safely(f"component_formulas/{formula_name}.json")
        
        # Generate insights based on the formula and visualization
        insights = {
            'formula': formula_name,
            'visualization': visualization_name,
            'insights': []
        }
        
        # Add some insights based on the formula
        if formula_name == 'gravity_action':
            insights['insights'].append({
                'type': 'observation',
                'content': 'The spacetime curvature is directly proportional to the mass of the object.'
            })
            insights['insights'].append({
                'type': 'implication',
                'content': 'Massive objects create deep gravity wells, affecting the path of light and matter.'
            })
        elif formula_name == 'matter_action':
            insights['insights'].append({
                'type': 'observation',
                'content': 'The Higgs field has a Mexican hat potential, with a circle of minimum energy states.'
            })
            insights['insights'].append({
                'type': 'implication',
                'content': 'Spontaneous symmetry breaking occurs when the field settles into one of these minimum energy states.'
            })
        elif formula_name == 'gauge_action':
            insights['insights'].append({
                'type': 'observation',
                'content': 'Gauge fields mediate forces between particles through the exchange of gauge bosons.'
            })
            insights['insights'].append({
                'type': 'implication',
                'content': 'The structure of the gauge field determines the properties of the force it mediates.'
            })
        elif formula_name == 'quantum_corrections':
            insights['insights'].append({
                'type': 'observation',
                'content': 'Quantum fluctuations create a foam-like structure at the Planck scale.'
            })
            insights['insights'].append({
                'type': 'implication',
                'content': 'These fluctuations may lead to the emergence of spacetime itself from a more fundamental structure.'
            })
        elif formula_name == 'unified_action':
            insights['insights'].append({
                'type': 'observation',
                'content': 'The unified action combines all fundamental forces and matter fields into a single framework.'
            })
            insights['insights'].append({
                'type': 'implication',
                'content': 'Extra dimensions may be necessary to achieve a complete unification of all forces.'
            })
        
        return insights

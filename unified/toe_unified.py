#!/usr/bin/env python3
"""
Theory of Everything - Unified API

This module provides a unified API for the Theory of Everything,
combining all the individual modules into a single interface.
"""

import os
import sys

print(f"Current Working Directory in toe_unified.py: {os.getcwd()}")
print(f"Python Path in toe_unified.py: {sys.path}")

from .toe_core import ToECore

import json
import argparse
import os
import sys
import json
import argparse
from .toe_core import ToECore
from .toe_formulas import FormulaTools
# Assuming toe_vis.py and toe_agent.py are also in the unified directory
from .toe_vis import VisualizationTools
from .agents.toe_agent import AgentTools


class ToEUnified:
    """
    Unified API for the Theory of Everything
    """
    
    def __init__(self, output_dir="gfx", agent_mode=False):
        """
        Initialize the unified API
        
        Parameters:
        -----------
        output_dir : str
            Directory to save output files (will be created if it doesn't exist)
        agent_mode : bool
            Whether to enable agent-specific features
        """
        self.output_dir = output_dir
        self.agent_mode = agent_mode
        
        # Create the core API
        self.core = ToECore(output_dir=output_dir)
        
        # Create the formula tools
        self.formula_tools = FormulaTools(core=self.core)
        
        # Create the visualization tools
        self.vis_tools = VisualizationTools(core=self.core)
        
        # Create the agent tools if agent mode is enabled
        self.agent_tools = AgentTools(core=self.core) if agent_mode else None
    
    def is_agent_mode_enabled(self):
        """
        Check if agent mode is enabled
        
        Returns:
        --------
        bool
            True if agent mode is enabled, False otherwise
        """
        return self.agent_mode and self.agent_tools is not None
    
    # Formula methods
    
    def list_formulas(self):
        """
        List all available formulas
        
        Returns:
        --------
        dict
            Dictionary mapping formula names to descriptions
        """
        return self.formula_tools.list_formulas()
    
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
        return self.formula_tools.get_formula(formula_name)
    
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
        return self.formula_tools.explore_formula(formula_name)
    
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
        return self.formula_tools.compare_formulas(formula_names)
    
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
        return self.formula_tools.search_formulas(query)
    
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
        return self.formula_tools.get_formula_dependencies(formula_name)
    
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
        return self.formula_tools.export_formula_to_latex(formula_name)
    
    # Visualization methods
    
    def list_visualizations(self):
        """
        List all available visualizations
        
        Returns:
        --------
        dict
            Dictionary mapping visualization names to descriptions
        """
        return self.vis_tools.list_visualizations()
    
    def get_visualization_info(self, visualization_name):
        """
        Get information about a visualization
        
        Parameters:
        -----------
        visualization_name : str
            Name of the visualization
            
        Returns:
        --------
        dict
            Dictionary containing information about the visualization
        """
        return self.vis_tools.get_visualization_info(visualization_name)
    
    def get_visualization_parameters(self, visualization_name):
        """
        Get the parameters for a visualization
        
        Parameters:
        -----------
        visualization_name : str
            Name of the visualization
            
        Returns:
        --------
        dict
            Dictionary mapping parameter names to parameter information
        """
        return self.vis_tools.get_visualization_parameters(visualization_name)
    
    def validate_parameters(self, visualization_name, params):
        """
        Validate parameters for a visualization
        
        Parameters:
        -----------
        visualization_name : str
            Name of the visualization
        params : dict
            Parameters to validate
            
        Returns:
        --------
        dict
            Dictionary mapping parameter names to validation results
        """
        return self.vis_tools.validate_parameters(visualization_name, params)
    
    def generate_visualization(self, visualization_name, params=None, show=False):
        """
        Generate a visualization
        
        Parameters:
        -----------
        visualization_name : str
            Name of the visualization to generate
        params : dict or None
            Parameters for the visualization (if None, will use defaults)
        show : bool
            Whether to display the visualization (default: False)
            
        Returns:
        --------
        str
            Path to the saved visualization
        """
        return self.vis_tools.generate_visualization(visualization_name, params, show)
    
    def batch_generate_visualizations(self, visualization_configs):
        """
        Generate multiple visualizations in batch
        
        Parameters:
        -----------
        visualization_configs : list
            List of dictionaries, each containing 'name' and 'params' keys
            
        Returns:
        --------
        dict
            Dictionary mapping visualization names to file paths
        """
        return self.vis_tools.batch_generate_visualizations(visualization_configs)
    
    def suggest_parameters(self, visualization_name):
        """
        Suggest parameters for a visualization
        
        Parameters:
        -----------
        visualization_name : str
            Name of the visualization
            
        Returns:
        --------
        dict
            Dictionary mapping parameter names to suggested values
        """
        return self.vis_tools.suggest_parameters(visualization_name)
    
    # Agent methods
    
    def get_session_info(self):
        """
        Get information about the current session
        
        Returns:
        --------
        dict
            Dictionary containing session information
        """
        if not self.is_agent_mode_enabled():
            raise ValueError("Agent mode is not enabled")
        
        return self.agent_tools.get_session_info()
    
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
        if not self.is_agent_mode_enabled():
            raise ValueError("Agent mode is not enabled")
        
        return self.agent_tools.explore_theory(query)
    
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
        if not self.is_agent_mode_enabled():
            raise ValueError("Agent mode is not enabled")
        
        return self.agent_tools.generate_visualization_for_formula(formula_name)
    
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
        if not self.is_agent_mode_enabled():
            raise ValueError("Agent mode is not enabled")
        
        return self.agent_tools.generate_visualization_sequence(visualization_name, param_ranges)
    
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
        if not self.is_agent_mode_enabled():
            raise ValueError("Agent mode is not enabled")
        
        return self.agent_tools.extract_insights(formula_name, visualization_name)


def main():
    """Main function for the unified API"""
    parser = argparse.ArgumentParser(description='Theory of Everything Unified API')
    parser.add_argument('--output-dir', type=str, default='gfx',
                      help='Directory to save output files')
    parser.add_argument('--agent-mode', action='store_true',
                      help='Enable agent-specific features')
    
    args = parser.parse_args()
    
    # Create the API
    api = ToEUnified(output_dir=args.output_dir, agent_mode=args.agent_mode)
    
    # Print some information
    print("Theory of Everything Unified API")
    print("-------------------------------")
    print(f"Output directory: {args.output_dir}")
    print(f"Agent mode: {'Enabled' if args.agent_mode else 'Disabled'}")
    print()
    
    # List available formulas
    print("Available formulas:")
    formulas = api.list_formulas()
    for name, description in formulas.items():
        print(f"  {name}: {description}")
    print()
    
    # List available visualizations
    print("Available visualizations:")
    visualizations = api.list_visualizations()
    for name, description in visualizations.items():
        print(f"  {name}: {description}")
    print()
    
    # Print help message
    print("Use this API in your Python code or run with --help for more options.")


if __name__ == "__main__":
    main()

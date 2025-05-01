#!/usr/bin/env python3
"""
Theory of Everything UI Module

This module provides a simple command-line interface for human users to interact
with the Theory of Everything.
"""

import os
import sys
import json
import argparse
from toe_core import ToECore
from toe_formulas import FormulaTools
from toe_vis import VisualizationTools


class ConsoleUI:
    """
    Command-line interface for human users to interact with the Theory of Everything
    """
    
    def __init__(self):
        """Initialize the console UI"""
        self.core = ToECore()
        self.formula_tools = FormulaTools(core=self.core)
        self.vis_tools = VisualizationTools(core=self.core)
    
    def display_welcome(self):
        """Display a welcome message"""
        print("\n" + "=" * 80)
        print("Welcome to the Theory of Everything".center(80))
        print("=" * 80 + "\n")
        print("This program allows you to explore the Theory of Everything,")
        print("including formulas and visualizations.\n")
    
    def display_main_menu(self):
        """Display the main menu and get user choice"""
        print("\nMain Menu:")
        print("1. Explore Formulas")
        print("2. Generate Visualizations")
        print("3. Compare Formulas")
        print("4. Search")
        print("5. Exit")
        
        while True:
            try:
                choice = int(input("\nEnter your choice (1-5): "))
                if 1 <= choice <= 5:
                    return choice
                else:
                    print("Invalid choice. Please enter a number between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    def display_formula_menu(self):
        """Display the formula menu and get user choice"""
        print("\nFormula Menu:")
        formulas = self.formula_tools.list_formulas()
        
        # Display the formulas
        for i, (name, description) in enumerate(formulas.items(), 1):
            print(f"{i}. {name}: {description}")
        print(f"{len(formulas) + 1}. Back to Main Menu")
        
        while True:
            try:
                choice = int(input(f"\nEnter your choice (1-{len(formulas) + 1}): "))
                if 1 <= choice <= len(formulas):
                    return list(formulas.keys())[choice - 1]
                elif choice == len(formulas) + 1:
                    return None
                else:
                    print(f"Invalid choice. Please enter a number between 1 and {len(formulas) + 1}.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    def display_visualization_menu(self):
        """Display the visualization menu and get user choice"""
        print("\nVisualization Menu:")
        visualizations = self.vis_tools.list_visualizations()
        
        # Display the visualizations
        for i, (name, description) in enumerate(visualizations.items(), 1):
            print(f"{i}. {name}: {description}")
        print(f"{len(visualizations) + 1}. Back to Main Menu")
        
        while True:
            try:
                choice = int(input(f"\nEnter your choice (1-{len(visualizations) + 1}): "))
                if 1 <= choice <= len(visualizations):
                    return list(visualizations.keys())[choice - 1]
                elif choice == len(visualizations) + 1:
                    return None
                else:
                    print(f"Invalid choice. Please enter a number between 1 and {len(visualizations) + 1}.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    def display_formula(self, formula_name):
        """Display a formula"""
        try:
            formula = self.formula_tools.get_formula(formula_name)
            
            print("\n" + "=" * 80)
            print(f"Formula: {formula['name']}".center(80))
            print("=" * 80 + "\n")
            
            if 'description' in formula:
                print(f"Description: {formula['description']}\n")
            
            if 'latex' in formula:
                print(f"LaTeX: {formula['latex']}\n")
            
            if 'components' in formula:
                print("Components:")
                if isinstance(formula['components'], list):
                    if all(isinstance(c, str) for c in formula['components']):
                        # Components are references to other formulas
                        for component_name in formula['components']:
                            component = self.formula_tools.get_formula(component_name)
                            print(f"  - {component['name']}")
                    else:
                        # Components are defined inline
                        for component in formula['components']:
                            print(f"  - {component['name']}")
                            if 'description' in component:
                                print(f"    {component['description']}")
            
            print("\nOptions:")
            print("1. Explore Components")
            print("2. Generate Visualization")
            print("3. Export to LaTeX")
            print("4. Back to Formula Menu")
            
            while True:
                try:
                    choice = int(input("\nEnter your choice (1-4): "))
                    if choice == 1:
                        self.explore_formula_components(formula_name)
                        break
                    elif choice == 2:
                        self.generate_visualization_for_formula(formula_name)
                        break
                    elif choice == 3:
                        self.export_formula_to_latex(formula_name)
                        break
                    elif choice == 4:
                        break
                    else:
                        print("Invalid choice. Please enter a number between 1 and 4.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        
        except Exception as e:
            print(f"\nError: {str(e)}")
    
    def explore_formula_components(self, formula_name):
        """Explore the components of a formula"""
        try:
            exploration = self.formula_tools.explore_formula(formula_name)
            
            print("\n" + "=" * 80)
            print(f"Exploring: {exploration['formula']['name']}".center(80))
            print("=" * 80 + "\n")
            
            if exploration['components']:
                print("Components:")
                for component in exploration['components']:
                    if isinstance(component, dict) and 'name' in component and 'formula' in component:
                        print(f"  - {component['formula']['name']}")
                    elif isinstance(component, dict) and 'name' in component:
                        print(f"  - {component['name']}")
            else:
                print("No components found.")
            
            if exploration['related_formulas']:
                print("\nRelated Formulas:")
                for related in exploration['related_formulas']:
                    print(f"  - {related['formula']['name']}")
            else:
                print("\nNo related formulas found.")
            
            input("\nPress Enter to continue...")
        
        except Exception as e:
            print(f"\nError: {str(e)}")
            input("\nPress Enter to continue...")
    
    def generate_visualization_for_formula(self, formula_name):
        """Generate a visualization for a formula"""
        try:
            # Determine which visualization to use based on the formula
            visualization_mapping = {
                'unified_action': None,  # No specific visualization
                'gravity_action': '4d_spacetime_curvature',
                'matter_action': '4d_higgs_field',
                'gauge_action': 'gauge_field_4d',
                'quantum_corrections': 'quantum_foam_3d',
                'full_master_equation': 'extra_dimensions_3d'
            }
            
            visualization_name = visualization_mapping.get(formula_name)
            if visualization_name is None:
                print(f"\nNo visualization available for formula: {formula_name}")
                input("\nPress Enter to continue...")
                return
            
            # Get suggested parameters
            params = self.vis_tools.suggest_parameters(visualization_name)
            suggested_params = {name: info['default'] for name, info in params.items()}
            
            print(f"\nGenerating visualization: {visualization_name}")
            print("Using default parameters:")
            for name, value in suggested_params.items():
                print(f"  - {name}: {value}")
            
            # Generate the visualization
            vis_path = self.vis_tools.generate_visualization(visualization_name, suggested_params, show=True)
            
            print(f"\nVisualization saved to: {vis_path}")
            input("\nPress Enter to continue...")
        
        except Exception as e:
            print(f"\nError: {str(e)}")
            input("\nPress Enter to continue...")
    
    def export_formula_to_latex(self, formula_name):
        """Export a formula to LaTeX"""
        try:
            latex = self.formula_tools.export_formula_to_latex(formula_name)
            
            # Save the LaTeX to a file
            output_dir = "latex_output"
            self.core.ensure_directory(output_dir)
            output_file = os.path.join(output_dir, f"{formula_name}.tex")
            
            with open(output_file, 'w') as f:
                f.write(latex)
            
            print(f"\nFormula exported to LaTeX: {output_file}")
            input("\nPress Enter to continue...")
        
        except Exception as e:
            print(f"\nError: {str(e)}")
            input("\nPress Enter to continue...")
    
    def generate_visualization(self, visualization_name):
        """Generate a visualization"""
        try:
            # Get the visualization parameters
            param_info = self.vis_tools.get_visualization_parameters(visualization_name)
            
            print(f"\nGenerating visualization: {visualization_name}")
            print("\nParameters:")
            
            # Get user input for parameters
            params = {}
            for name, info in param_info.items():
                default = info['default']
                description = info['description']
                param_type = info['type']
                
                while True:
                    user_input = input(f"  {name} ({description}, default={default}): ")
                    if not user_input:
                        # Use default value
                        params[name] = default
                        break
                    
                    try:
                        if param_type == 'int':
                            value = int(user_input)
                        elif param_type == 'float':
                            value = float(user_input)
                        else:
                            value = user_input
                        
                        # Check range if applicable
                        if 'min' in info and value < info['min']:
                            print(f"Value must be at least {info['min']}. Using minimum value.")
                            value = info['min']
                        
                        if 'max' in info and value > info['max']:
                            print(f"Value must be at most {info['max']}. Using maximum value.")
                            value = info['max']
                        
                        params[name] = value
                        break
                    except ValueError:
                        print(f"Invalid input. Please enter a {param_type}.")
            
            # Generate the visualization
            print("\nGenerating visualization...")
            vis_path = self.vis_tools.generate_visualization(visualization_name, params, show=True)
            
            print(f"\nVisualization saved to: {vis_path}")
            input("\nPress Enter to continue...")
        
        except Exception as e:
            print(f"\nError: {str(e)}")
            input("\nPress Enter to continue...")
    
    def compare_formulas(self):
        """Compare multiple formulas"""
        try:
            print("\nCompare Formulas:")
            print("Select formulas to compare (enter 0 when done):")
            
            formulas = self.formula_tools.list_formulas()
            selected_formulas = []
            
            # Display the formulas
            for i, (name, description) in enumerate(formulas.items(), 1):
                print(f"{i}. {name}: {description}")
            
            while True:
                try:
                    choice = int(input("\nEnter formula number (0 to finish): "))
                    if choice == 0:
                        break
                    elif 1 <= choice <= len(formulas):
                        formula_name = list(formulas.keys())[choice - 1]
                        if formula_name not in selected_formulas:
                            selected_formulas.append(formula_name)
                            print(f"Added: {formula_name}")
                        else:
                            print(f"Formula already selected: {formula_name}")
                    else:
                        print(f"Invalid choice. Please enter a number between 0 and {len(formulas)}.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            
            if len(selected_formulas) < 2:
                print("\nAt least two formulas are required for comparison.")
                input("\nPress Enter to continue...")
                return
            
            # Compare the formulas
            comparison = self.formula_tools.compare_formulas(selected_formulas)
            
            print("\n" + "=" * 80)
            print("Formula Comparison".center(80))
            print("=" * 80 + "\n")
            
            print("Formulas compared:")
            for name in selected_formulas:
                print(f"  - {name}")
            
            if comparison['common_components']:
                print("\nCommon Components:")
                for component in comparison['common_components']:
                    print(f"  - {component}")
            else:
                print("\nNo common components found.")
            
            if comparison['unique_components']:
                print("\nUnique Components:")
                for formula_name, components in comparison['unique_components'].items():
                    print(f"  {formula_name}:")
                    for component in components:
                        print(f"    - {component}")
            else:
                print("\nNo unique components found.")
            
            input("\nPress Enter to continue...")
        
        except Exception as e:
            print(f"\nError: {str(e)}")
            input("\nPress Enter to continue...")
    
    def search(self):
        """Search for formulas or visualizations"""
        try:
            query = input("\nEnter search query: ")
            
            print("\nSearching...")
            
            # Search for formulas
            formula_results = self.formula_tools.search_formulas(query)
            
            print("\n" + "=" * 80)
            print("Search Results".center(80))
            print("=" * 80 + "\n")
            
            if formula_results:
                print("Formula Results:")
                for name, score in formula_results.items():
                    print(f"  - {name} (score: {score})")
                
                # Ask if the user wants to view a formula
                print("\nOptions:")
                print("1. View a formula")
                print("2. Back to Main Menu")
                
                while True:
                    try:
                        choice = int(input("\nEnter your choice (1-2): "))
                        if choice == 1:
                            formula_name = input("\nEnter formula name: ")
                            if formula_name in formula_results:
                                self.display_formula(formula_name)
                            else:
                                print(f"\nFormula not found: {formula_name}")
                            break
                        elif choice == 2:
                            break
                        else:
                            print("Invalid choice. Please enter 1 or 2.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
            else:
                print("No results found.")
                input("\nPress Enter to continue...")
        
        except Exception as e:
            print(f"\nError: {str(e)}")
            input("\nPress Enter to continue...")
    
    def run(self):
        """Run the console UI"""
        self.display_welcome()
        
        while True:
            choice = self.display_main_menu()
            
            if choice == 1:
                # Explore Formulas
                formula_name = self.display_formula_menu()
                if formula_name:
                    self.display_formula(formula_name)
            
            elif choice == 2:
                # Generate Visualizations
                visualization_name = self.display_visualization_menu()
                if visualization_name:
                    self.generate_visualization(visualization_name)
            
            elif choice == 3:
                # Compare Formulas
                self.compare_formulas()
            
            elif choice == 4:
                # Search
                self.search()
            
            elif choice == 5:
                # Exit
                print("\nThank you for using the Theory of Everything. Goodbye!")
                break


def main():
    """Main function to run the console UI"""
    parser = argparse.ArgumentParser(description='Theory of Everything UI')
    parser.add_argument('--formula', type=str, help='Display a specific formula')
    parser.add_argument('--visualization', type=str, help='Generate a specific visualization')
    parser.add_argument('--compare', type=str, nargs='+', help='Compare multiple formulas')
    parser.add_argument('--search', type=str, help='Search for formulas or visualizations')
    
    args = parser.parse_args()
    
    ui = ConsoleUI()
    
    if args.formula:
        ui.display_formula(args.formula)
    elif args.visualization:
        ui.generate_visualization(args.visualization)
    elif args.compare:
        ui.formula_tools.compare_formulas(args.compare)
    elif args.search:
        ui.search()
    else:
        ui.run()


if __name__ == "__main__":
    main()

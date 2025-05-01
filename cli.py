#!/usr/bin/env python3
"""
Command-line interface for the Theory of Everything
"""

import os
import sys
import json
import argparse
from theoryofeverything.toe_unified import ToEUnified


def main():
    """Main entry point for the CLI"""
    parser = argparse.ArgumentParser(description='Theory of Everything CLI')
    parser.add_argument('--output-dir', type=str, default='gfx',
                      help='Directory to save output files')
    parser.add_argument('--agent-mode', action='store_true',
                      help='Enable agent-specific features')

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Formula commands
    formula_parser = subparsers.add_parser('formula', help='Formula commands')
    formula_subparsers = formula_parser.add_subparsers(dest='formula_command', help='Formula command to run')

    list_formulas_parser = formula_subparsers.add_parser('list', help='List available formulas')

    get_formula_parser = formula_subparsers.add_parser('get', help='Get a formula')
    get_formula_parser.add_argument('name', type=str, help='Name of the formula to get')

    explore_formula_parser = formula_subparsers.add_parser('explore', help='Explore a formula')
    explore_formula_parser.add_argument('name', type=str, help='Name of the formula to explore')

    compare_formulas_parser = formula_subparsers.add_parser('compare', help='Compare formulas')
    compare_formulas_parser.add_argument('names', type=str, nargs='+', help='Names of the formulas to compare')

    search_formulas_parser = formula_subparsers.add_parser('search', help='Search for formulas')
    search_formulas_parser.add_argument('query', type=str, help='Search query')

    # Visualization commands
    vis_parser = subparsers.add_parser('visualization', help='Visualization commands')
    vis_subparsers = vis_parser.add_subparsers(dest='vis_command', help='Visualization command to run')

    list_vis_parser = vis_subparsers.add_parser('list', help='List available visualizations')

    get_vis_info_parser = vis_subparsers.add_parser('info', help='Get information about a visualization')
    get_vis_info_parser.add_argument('name', type=str, help='Name of the visualization')

    get_vis_params_parser = vis_subparsers.add_parser('params', help='Get parameters for a visualization')
    get_vis_params_parser.add_argument('name', type=str, help='Name of the visualization')

    generate_vis_parser = vis_subparsers.add_parser('generate', help='Generate a visualization')
    generate_vis_parser.add_argument('name', type=str, help='Name of the visualization to generate')
    generate_vis_parser.add_argument('--params', type=str, default='{}',
                                   help='JSON string of parameters for the visualization')
    generate_vis_parser.add_argument('--show', action='store_true',
                                   help='Show the visualization')

    suggest_params_parser = vis_subparsers.add_parser('suggest', help='Suggest parameters for a visualization')
    suggest_params_parser.add_argument('name', type=str, help='Name of the visualization')

    # Agent commands
    agent_parser = subparsers.add_parser('agent', help='Agent commands')
    agent_subparsers = agent_parser.add_subparsers(dest='agent_command', help='Agent command to run')

    session_info_parser = agent_subparsers.add_parser('session', help='Get session information')

    explore_theory_parser = agent_subparsers.add_parser('explore', help='Explore the Theory of Everything')
    explore_theory_parser.add_argument('--query', type=str, help='Search query')

    vis_for_formula_parser = agent_subparsers.add_parser('vis-for-formula', help='Generate a visualization for a formula')
    vis_for_formula_parser.add_argument('name', type=str, help='Name of the formula')

    vis_sequence_parser = agent_subparsers.add_parser('vis-sequence', help='Generate a visualization sequence')
    vis_sequence_parser.add_argument('name', type=str, help='Name of the visualization')
    vis_sequence_parser.add_argument('--param-ranges', type=str, required=True,
                                   help='JSON string of parameter ranges')

    insights_parser = agent_subparsers.add_parser('insights', help='Extract insights')
    insights_parser.add_argument('--formula', type=str, help='Name of the formula')
    insights_parser.add_argument('--visualization', type=str, help='Name of the visualization')

    args = parser.parse_args()

    # If no command is provided, show help
    if not args.command:
        parser.print_help()
        return 1

    # Create the API
    api = ToEUnified(output_dir=args.output_dir, agent_mode=args.agent_mode)

    # Run the requested command
    if args.command == 'formula':
        if args.formula_command == 'list':
            formulas = api.list_formulas()
            for name, description in formulas.items():
                print(f"{name}: {description}")

        elif args.formula_command == 'get':
            formula = api.get_formula(args.name)
            print(json.dumps(formula, indent=2))

        elif args.formula_command == 'explore':
            exploration = api.explore_formula(args.name)
            print(json.dumps(exploration, indent=2))

        elif args.formula_command == 'compare':
            comparison = api.compare_formulas(args.names)
            print(json.dumps(comparison, indent=2))

        elif args.formula_command == 'search':
            results = api.search_formulas(args.query)
            print(json.dumps(results, indent=2))

    elif args.command == 'visualization':
        if args.vis_command == 'list':
            visualizations = api.list_visualizations()
            for name, description in visualizations.items():
                print(f"{name}: {description}")

        elif args.vis_command == 'info':
            info = api.get_visualization_info(args.name)
            print(json.dumps(info, indent=2))

        elif args.vis_command == 'params':
            params = api.get_visualization_parameters(args.name)
            print(json.dumps(params, indent=2))

        elif args.vis_command == 'generate':
            params = json.loads(args.params)
            path = api.generate_visualization(args.name, params, args.show)
            print(f"Visualization saved to: {path}")

        elif args.vis_command == 'suggest':
            suggestions = api.suggest_parameters(args.name)
            print(json.dumps(suggestions, indent=2))

    elif args.command == 'agent':
        if not api.is_agent_mode_enabled():
            print("Error: Agent mode is not enabled. Use --agent-mode to enable it.")
            return 1

        if args.agent_command == 'session':
            info = api.get_session_info()
            print(json.dumps(info, indent=2))

        elif args.agent_command == 'explore':
            exploration = api.explore_theory(args.query)
            print(json.dumps(exploration, indent=2))

        elif args.agent_command == 'vis-for-formula':
            result = api.generate_visualization_for_formula(args.name)
            print(json.dumps(result, indent=2))

        elif args.agent_command == 'vis-sequence':
            param_ranges = json.loads(args.param_ranges)
            result = api.generate_visualization_sequence(args.name, param_ranges)
            print(json.dumps(result, indent=2))

        elif args.agent_command == 'insights':
            insights = api.extract_insights(args.formula, args.visualization)
            print(json.dumps(insights, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())

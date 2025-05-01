#!/usr/bin/env python3
"""
Test script for the Theory of Everything agent functionality
"""

import os
import sys
import json

# Add the parent directory to the path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the unified API
try:
    from toe_unified import ToEUnified
    print("Successfully imported ToEUnified")
except ImportError as e:
    print(f"Error importing ToEUnified: {e}")
    sys.exit(1)

# Test the agent functionality
try:
    # Create an instance of the API with agent mode enabled
    api = ToEUnified(output_dir="tests/agent_output", agent_mode=True)
    print("Successfully created ToEUnified instance with agent mode")
    
    # Test getting session information
    print("\nTesting session information...")
    session_info = api.get_session_info()
    print(f"Session ID: {session_info['session_id']}")
    print(f"Session directory: {session_info['session_dir']}")
    
    # Test exploring the theory
    print("\nTesting theory exploration...")
    exploration = api.explore_theory()
    print(f"Overview: {exploration['overview']['description']}")
    print("Key components:")
    for component in exploration['overview']['key_components']:
        print(f"  - {component}")
    
    # Test searching for formulas
    print("\nTesting formula search...")
    search_results = api.search_formulas("gravity")
    print(f"Found {len(search_results)} results")
    for name, score in search_results.items():
        print(f"  - {name} (score: {score})")
    
    # Test extracting insights
    print("\nTesting insight extraction...")
    insights = api.extract_insights(formula_name="gravity_action")
    print("Key insights:")
    for insight in insights['key_insights']:
        print(f"  - {insight}")
    
    # Test suggesting parameters
    print("\nTesting parameter suggestions...")
    suggestions = api.suggest_parameters("4d_spacetime_curvature")
    print("Suggested parameters:")
    for name, info in suggestions.items():
        print(f"  - {name}: {info['default']}")
    
    print("\nAll tests passed!")
except Exception as e:
    print(f"\nError: {str(e)}")
    sys.exit(1)

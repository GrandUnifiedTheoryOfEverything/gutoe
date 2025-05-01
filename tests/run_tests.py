#!/usr/bin/env python3
"""
Test runner for the Theory of Everything tests
"""

import os
import sys
import subprocess
import argparse

# Define the tests
TESTS = {
    "imports": "test_imports.py",
    "core": "test_core.py",
    "modules": "test_modules.py",
    "formula": "test_formula.py",
    "visualization": "test_visualization.py",
    "agent": "test_agent.py",
    "latex": "test_latex.py",
    "pdf": "test_pdf.py"
}

def run_test(test_name):
    """Run a specific test"""
    if test_name not in TESTS:
        print(f"Error: Unknown test '{test_name}'")
        return False

    test_script = TESTS[test_name]
    test_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), test_script)

    print(f"\n{'=' * 80}")
    print(f"Running {test_name} test: {test_script}")
    print(f"{'=' * 80}\n")

    try:
        result = subprocess.run([sys.executable, test_path], check=True)
        print(f"\n{test_name} test passed!")
        return True
    except subprocess.CalledProcessError:
        print(f"\n{test_name} test failed!")
        return False

def run_all_tests():
    """Run all tests"""
    results = {}

    for test_name in TESTS:
        results[test_name] = run_test(test_name)

    print("\n" + "=" * 80)
    print("Test Results Summary")
    print("=" * 80)

    all_passed = True
    for test_name, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False

    return all_passed

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Run Theory of Everything tests")
    parser.add_argument("test", nargs="?", choices=list(TESTS.keys()) + ["all"],
                      default="all", help="Test to run (default: all)")

    args = parser.parse_args()

    if args.test == "all":
        success = run_all_tests()
    else:
        success = run_test(args.test)

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Script to run the advanced visualizations
This script temporarily renames the math directory to avoid conflicts with Python's built-in math module
"""

import os
import sys
import shutil

def main():
    # Check if the math directory exists
    if os.path.exists('math') and os.path.isdir('math'):
        # Temporarily rename the math directory
        print("Temporarily renaming 'math' directory to 'toe_math'...")
        os.rename('math', 'toe_math')
        
        try:
            # Import and run the advanced visualizations
            print("Running advanced visualizations...")
            from advanced_vis import main as run_visualizations
            run_visualizations()
        finally:
            # Rename the directory back
            print("Renaming 'toe_math' directory back to 'math'...")
            if os.path.exists('toe_math') and os.path.isdir('toe_math'):
                os.rename('toe_math', 'math')
    else:
        print("The 'math' directory does not exist. Running visualizations directly...")
        from advanced_vis import main as run_visualizations
        run_visualizations()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Installation script for the Theory of Everything package
"""

import os
import sys
import subprocess
import argparse


def run_command(command):
    """Run a shell command and print the output"""
    print(f"Running: {command}")
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False


def install_package(dev_mode=False):
    """Install the package"""
    if dev_mode:
        return run_command("pip install -e .")
    else:
        return run_command("pip install .")


def create_directories():
    """Create necessary directories"""
    directories = [
        "gfx",
        "gfx/2d",
        "gfx/3d",
        "gfx/4d",
        "gfx/latex",
        "gfx/pdf"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            print(f"Creating directory: {directory}")
            os.makedirs(directory)
        else:
            print(f"Directory already exists: {directory}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Install the Theory of Everything package')
    parser.add_argument('--dev', action='store_true', help='Install in development mode')
    args = parser.parse_args()
    
    print("Installing the Theory of Everything package...")
    
    # Create necessary directories
    create_directories()
    
    # Install the package
    if install_package(args.dev):
        print("\nInstallation completed successfully!")
        print("\nYou can now use the package:")
        print("  - Import in Python: from theoryofeverything import ToEUnified")
        print("  - Command-line: toe --help")
        print("\nTo test the package, run: python test_package.py")
    else:
        print("\nInstallation failed.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

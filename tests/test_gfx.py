#!/usr/bin/env python3
"""
Test script to verify the gfx folder structure
"""

import os
import sys

def check_directory(directory):
    """Check if a directory exists and create it if it doesn't"""
    if not os.path.exists(directory):
        print(f"Creating directory: {directory}")
        os.makedirs(directory)
    else:
        print(f"Directory exists: {directory}")

def main():
    """Main function"""
    # Check the gfx directory
    gfx_dir = "gfx"
    check_directory(gfx_dir)
    
    # Check the subdirectories
    subdirs = ["2d", "3d", "4d", "latex", "pdf"]
    for subdir in subdirs:
        check_directory(os.path.join(gfx_dir, subdir))
    
    # Create a test file in each directory
    for subdir in subdirs:
        test_file = os.path.join(gfx_dir, subdir, "test_file.txt")
        print(f"Creating test file: {test_file}")
        with open(test_file, "w") as f:
            f.write(f"Test file for {subdir} directory\n")
    
    print("\nGfx folder structure verified and test files created.")

if __name__ == "__main__":
    main()

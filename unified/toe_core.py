#!/usr/bin/env python3
"""
Theory of Everything Core API

This module provides the core functionality for the Theory of Everything API,
including utilities for handling the math module conflict and basic file operations.
"""

import os
import sys
import json
import tempfile
import subprocess
from contextlib import contextmanager


@contextmanager
def math_module_safe_context():
    """
    Context manager that temporarily renames the math directory to avoid conflicts
    with Python's built-in math module.
    
    Usage:
        with math_module_safe_context():
            # Code that uses the math module
    """
    renamed = False
    original_name = 'math'
    temp_name = 'toe_math'
    
    try:
        # Check if the math directory exists and temporarily rename it
        if os.path.exists(original_name) and os.path.isdir(original_name):
            os.rename(original_name, temp_name)
            renamed = True
        yield
    finally:
        # Rename the directory back if it was renamed
        if renamed and os.path.exists(temp_name) and os.path.isdir(temp_name):
            os.rename(temp_name, original_name)


def ensure_directory(directory):
    """
    Ensure that a directory exists, creating it if necessary.
    
    Parameters:
    -----------
    directory : str
        Path to the directory
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def run_script_safely(script_content, args=None, env=None):
    """
    Run a Python script safely, handling the math module conflict.
    
    Parameters:
    -----------
    script_content : str or bytes
        Content of the script to run
    args : list or None
        Command line arguments to pass to the script
    env : dict or None
        Environment variables to set for the script
        
    Returns:
    --------
    str
        Output of the script
    """
    if args is None:
        args = []
    
    if isinstance(script_content, str):
        script_content = script_content.encode('utf-8')
    
    # Create a temporary script
    with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as f:
        script_path = f.name
        f.write(script_content)
    
    try:
        # Run the script
        try:
            result = subprocess.check_output(
                [sys.executable, script_path] + args,
                universal_newlines=True,
                stderr=subprocess.STDOUT,
                env=env
            )
            return result.strip()
        except subprocess.CalledProcessError as e:
            return f"Error: {e.output}"
    finally:
        # Clean up the temporary script
        os.unlink(script_path)


def load_json_safely(json_str):
    """
    Load JSON safely, returning None if the string is not valid JSON.
    
    Parameters:
    -----------
    json_str : str
        JSON string to parse
        
    Returns:
    --------
    dict or None
        Parsed JSON or None if the string is not valid JSON
    """
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return None


class ToECore:
    """
    Core functionality for the Theory of Everything API
    """
    
    def __init__(self, output_dir="visualizations"):
        """
        Initialize the core API
        
        Parameters:
        -----------
        output_dir : str
            Directory to save output files (will be created if it doesn't exist)
        """
        self.output_dir = output_dir
        ensure_directory(output_dir)
        
        # Check if the math directory exists
        self.has_math_dir = os.path.exists('math') and os.path.isdir('math')
    
    def run_with_math_safety(self, func, *args, **kwargs):
        """
        Run a function with math module safety
        
        Parameters:
        -----------
        func : callable
            Function to run
        *args, **kwargs
            Arguments to pass to the function
            
        Returns:
        --------
        any
            Result of the function
        """
        with math_module_safe_context():
            return func(*args, **kwargs)
    
    def save_output_file(self, content, filename, subdir=None):
        """
        Save content to a file in the output directory
        
        Parameters:
        -----------
        content : str or bytes
            Content to save
        filename : str
            Name of the file
        subdir : str or None
            Subdirectory within the output directory (will be created if necessary)
            
        Returns:
        --------
        str
            Path to the saved file
        """
        # Determine the output directory
        if subdir:
            output_dir = os.path.join(self.output_dir, subdir)
            ensure_directory(output_dir)
        else:
            output_dir = self.output_dir
        
        # Determine the file path
        file_path = os.path.join(output_dir, filename)
        
        # Save the content
        mode = 'wb' if isinstance(content, bytes) else 'w'
        with open(file_path, mode) as f:
            f.write(content)
        
        return file_path
    
    def load_output_file(self, filename, subdir=None, binary=False):
        """
        Load content from a file in the output directory
        
        Parameters:
        -----------
        filename : str
            Name of the file
        subdir : str or None
            Subdirectory within the output directory
        binary : bool
            Whether to load the file in binary mode
            
        Returns:
        --------
        str or bytes or None
            Content of the file, or None if the file does not exist
        """
        # Determine the file path
        if subdir:
            file_path = os.path.join(self.output_dir, subdir, filename)
        else:
            file_path = os.path.join(self.output_dir, filename)
        
        # Check if the file exists
        if not os.path.exists(file_path):
            return None
        
        # Load the content
        mode = 'rb' if binary else 'r'
        with open(file_path, mode) as f:
            return f.read()
    
    def list_output_files(self, subdir=None, pattern=None):
        """
        List files in the output directory
        
        Parameters:
        -----------
        subdir : str or None
            Subdirectory within the output directory
        pattern : str or None
            Pattern to match filenames against
            
        Returns:
        --------
        list
            List of filenames
        """
        import fnmatch
        
        # Determine the directory to list
        if subdir:
            dir_path = os.path.join(self.output_dir, subdir)
        else:
            dir_path = self.output_dir
        
        # Check if the directory exists
        if not os.path.exists(dir_path):
            return []
        
        # List the files
        files = os.listdir(dir_path)
        
        # Filter by pattern if specified
        if pattern:
            files = [f for f in files if fnmatch.fnmatch(f, pattern)]
        
        return files

    def run_script_safely(self, script_content, args=None, env=None):
        """
        Run a script safely
        
        Parameters:
        -----------
        script_content : str
            Content of the script to run
        args : list, optional
            Arguments to pass to the script
        env : dict, optional
            Environment variables to set
            
        Returns:
        --------
        str
            Output of the script
        """
        return run_script_safely(script_content, args, env)

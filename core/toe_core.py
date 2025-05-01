#!/usr/bin/env python3
"""
Theory of Everything - Core Module

This module provides the core functionality for the Theory of Everything.
"""

import os
import sys
import json
import importlib
import contextlib
import traceback
from io import StringIO


def ensure_directory(directory):
    """
    Ensure a directory exists
    
    Parameters:
    -----------
    directory : str
        Path to the directory
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def load_json_safely(file_path):
    """
    Load a JSON file safely
    
    Parameters:
    -----------
    file_path : str
        Path to the JSON file
        
    Returns:
    --------
    dict
        Loaded JSON data
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON file {file_path}: {e}")
        return {}


@contextlib.contextmanager
def math_module_safe_context():
    """
    Context manager for safely using the math module
    
    This context manager ensures that the math module is available
    and handles any errors that might occur when using it.
    """
    try:
        # Try to import the math module
        import math
        
        # Yield control back to the caller
        yield
    except Exception as e:
        print(f"Error in math module context: {e}")
        traceback.print_exc()


class ToECore:
    """
    Core functionality for the Theory of Everything
    """
    
    def __init__(self, output_dir="output"):
        """
        Initialize the core
        
        Parameters:
        -----------
        output_dir : str
            Directory to save output files (will be created if it doesn't exist)
        """
        self.output_dir = output_dir
        ensure_directory(output_dir)
    
    def save_output_file(self, content, filename):
        """
        Save content to a file in the output directory
        
        Parameters:
        -----------
        content : str
            Content to save
        filename : str
            Name of the file
            
        Returns:
        --------
        str
            Path to the saved file
        """
        # Ensure the output directory exists
        ensure_directory(self.output_dir)
        
        # Save the file
        file_path = os.path.join(self.output_dir, filename)
        with open(file_path, 'w') as f:
            f.write(content)
        
        return file_path
    
    def load_output_file(self, filename):
        """
        Load content from a file in the output directory
        
        Parameters:
        -----------
        filename : str
            Name of the file
            
        Returns:
        --------
        str
            Content of the file
        """
        file_path = os.path.join(self.output_dir, filename)
        
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading file {file_path}: {e}")
            return ""
    
    def run_script_safely(self, script, args=None):
        """
        Run a Python script safely
        
        Parameters:
        -----------
        script : str
            Python script to run
        args : list or None
            Arguments to pass to the script
            
        Returns:
        --------
        str
            Output of the script
        """
        if args is None:
            args = []
        
        # Create a StringIO object to capture stdout
        stdout = StringIO()
        
        # Save the original stdout
        original_stdout = sys.stdout
        
        try:
            # Redirect stdout to our StringIO object
            sys.stdout = stdout
            
            # Create a namespace for the script
            namespace = {
                'args': args,
                'params': {},
                'output_dir': self.output_dir
            }
            
            # If args is a dict, use it as params
            if isinstance(args, dict):
                namespace['params'] = args
            
            # Execute the script
            exec(script, namespace)
            
            # Get the output
            output = stdout.getvalue()
            
            return output
        except Exception as e:
            return f"Error executing script: {e}\n{traceback.format_exc()}"
        finally:
            # Restore the original stdout
            sys.stdout = original_stdout
    
    def run_with_math_safety(self, func, *args, **kwargs):
        """
        Run a function with math safety
        
        Parameters:
        -----------
        func : callable
            Function to run
        *args
            Arguments to pass to the function
        **kwargs
            Keyword arguments to pass to the function
            
        Returns:
        --------
        any
            Result of the function
        """
        with math_module_safe_context():
            return func(*args, **kwargs)

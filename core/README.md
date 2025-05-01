# Theory of Everything - Core

This directory contains core functionality for the Theory of Everything package.

## Core Components

- **ToECore**: Core functionality used by all other modules
- **math_module_safe_context**: Context manager for safely using the math module
- **load_json_safely**: Function for safely loading JSON files
- **ensure_directory**: Function for ensuring a directory exists

## Usage

```python
from theoryofeverything.core import ToECore, ensure_directory, load_json_safely

# Create a core instance
core = ToECore(output_dir="output")

# Ensure a directory exists
ensure_directory("output/data")

# Load a JSON file safely
data = load_json_safely("data.json")

# Save content to a file
path = core.save_output_file("Hello, world!", "hello.txt")
print(f"File saved to: {path}")

# Load content from a file
content = core.load_output_file("hello.txt")
print(content)

# Run a script safely
script = """
import math
print(f"Pi: {math.pi}")
"""
output = core.run_script_safely(script)
print(output)

# Run a function with math safety
def calculate_area(radius):
    import math
    return math.pi * radius ** 2

area = core.run_with_math_safety(calculate_area, 5)
print(f"Area: {area}")
```

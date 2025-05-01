#!/usr/bin/env python3
"""
Fix the gutoeUIUX.py file to handle components correctly
"""

import re

# Read the file
with open('gutoeUIUX.py', 'r') as f:
    content = f.read()

# Define the pattern to match
pattern = r'if st\.checkbox\("Explore formula components"\):\s+exploration = api\.explore_formula\(formula_name\)\s+components = exploration\.get\(\'components\', \{\}\)\s+\s+for component_name, component_data in components\.items\(\):\s+st\.markdown\("---"\)\s+display_formula\(component_name, component_data\)'

# Define the replacement
replacement = '''if st.checkbox("Explore formula components"):
            exploration = api.explore_formula(formula_name)
            components = exploration.get('components', [])
            
            for component in components:
                st.markdown("---")
                if isinstance(component, dict) and 'name' in component and 'formula' in component:
                    # Component is a reference to another formula
                    display_formula(component['name'], component['formula'])
                elif isinstance(component, dict):
                    # Component is defined inline with a name
                    for name, data in component.items():
                        display_formula(name, data)
                else:
                    # Component is something else
                    st.write(component)'''

# Replace the pattern
new_content = re.sub(pattern, replacement, content)

# Write the file
with open('gutoeUIUX.py', 'w') as f:
    f.write(new_content)

print("Fixed gutoeUIUX.py")

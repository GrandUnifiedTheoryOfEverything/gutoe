#!/usr/bin/env python3
"""
Fix the display_formula function in gutoeUIUX.py and streamlit_app.py
"""

import re

# Define the new display_formula function
new_display_formula = '''def display_formula(formula_name, formula_data):
    """Display a formula with its components"""
    st.subheader(f"{formula_data.get('name', formula_name)}")
    st.write(formula_data.get('description', 'No description available'))
    
    # Display the LaTeX formula
    latex = formula_data.get('latex', '')
    if latex:
        st.latex(latex)
    
    # Display components if available
    components = formula_data.get('components', [])
    if components:
        st.write("#### Components")
        for component in components:
            if isinstance(component, dict):
                # If component is a dictionary with name and latex
                if 'name' in component and 'latex' in component:
                    st.write(f"- **{component['name']}**")
                    st.latex(component['latex'])
                    if 'description' in component:
                        st.write(f"  {component['description']}")
                # If component is just a name reference
                elif isinstance(component, str):
                    st.write(f"- {component}")
            else:
                # Fallback for any other format
                st.write(f"- {component}")'''

# Fix gutoeUIUX.py
with open('gutoeUIUX.py', 'r') as f:
    content = f.read()

# Define the pattern to match the old display_formula function
pattern = r'def display_formula\(formula_name, formula_data\):.*?def generate_visualization'
# Use re.DOTALL to match across multiple lines
new_content = re.sub(pattern, new_display_formula + '\n\ndef generate_visualization', content, flags=re.DOTALL)

# Write the file
with open('gutoeUIUX.py', 'w') as f:
    f.write(new_content)

print("Fixed display_formula in gutoeUIUX.py")

# Fix streamlit_app.py
with open('streamlit_app.py', 'r') as f:
    content = f.read()

# Define the pattern to match the old display_formula function
pattern = r'def display_formula\(formula_name, formula_data\):.*?def generate_visualization'
# Use re.DOTALL to match across multiple lines
new_content = re.sub(pattern, new_display_formula + '\n\ndef generate_visualization', content, flags=re.DOTALL)

# Write the file
with open('streamlit_app.py', 'w') as f:
    f.write(new_content)

print("Fixed display_formula in streamlit_app.py")

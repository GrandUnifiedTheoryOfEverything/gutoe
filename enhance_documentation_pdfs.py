#!/usr/bin/env python3
"""
Enhance Documentation PDFs

This script uses the Augmentic PDF Agent to significantly improve the PDF documents
in the docs directory with professional styling, better formatting, and enhanced content.
"""

import os
import re
import sys
from augmentic_pdf_agent import PDFAgent

def read_markdown_file(file_path):
    """Read content from a markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        return None

def extract_sections_from_markdown(content):
    """Extract sections from markdown content"""
    if not content:
        return []
    
    # Split content by headings
    sections = []
    current_title = "Introduction"
    current_content = []
    
    lines = content.split('\n')
    for line in lines:
        if line.startswith('# '):
            # Main title, skip
            continue
        elif line.startswith('## '):
            # If we have content for the previous section, add it
            if current_content:
                sections.append({
                    "title": current_title,
                    "text": '\n'.join(current_content)
                })
                current_content = []
            
            # Start a new section
            current_title = line.replace('## ', '')
        else:
            current_content.append(line)
    
    # Add the last section
    if current_content:
        sections.append({
            "title": current_title,
            "text": '\n'.join(current_content)
        })
    
    return sections

def extract_title_from_markdown(content):
    """Extract title from markdown content"""
    if not content:
        return "Untitled Document"
    
    lines = content.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line.replace('# ', '')
    
    return "Untitled Document"

def enhance_documentation_pdf(markdown_path, output_pdf_path):
    """Enhance a documentation PDF using the Augmentic PDF Agent"""
    print(f"Enhancing {markdown_path} -> {output_pdf_path}")
    
    # Read markdown content
    content = read_markdown_file(markdown_path)
    if not content:
        return False
    
    # Extract title and sections
    title = extract_title_from_markdown(content)
    sections = extract_sections_from_markdown(content)
    
    # Create PDF agent
    agent = PDFAgent()
    agent.set_style_theme("professional")
    
    # Prepare content for PDF
    pdf_content = {
        "title": title,
        "subtitle": "Theory of Everything Documentation",
        "sections": sections
    }
    
    # Generate enhanced PDF
    pdf_path = agent.create_pdf(
        pdf_content,
        output_pdf_path,
        title=title,
        author="Theory of Everything Team",
        subject="Theory of Everything Documentation"
    )
    
    return pdf_path is not None

def enhance_scientific_pdf(markdown_path, output_pdf_path):
    """Enhance a scientific documentation PDF using the Augmentic PDF Agent"""
    print(f"Enhancing scientific document {markdown_path} -> {output_pdf_path}")
    
    # Read markdown content
    content = read_markdown_file(markdown_path)
    if not content:
        return False
    
    # Extract title and sections
    title = extract_title_from_markdown(content)
    
    # Extract abstract (first paragraph after title)
    abstract = ""
    introduction = ""
    methods = ""
    results = ""
    discussion = ""
    conclusion = ""
    references = []
    
    # Simple parsing of scientific content
    lines = content.split('\n')
    current_section = None
    section_content = []
    
    for line in lines:
        if line.startswith('# ') or line.startswith('## '):
            # Process previous section
            if current_section and section_content:
                section_text = '\n'.join(section_content)
                if current_section == "Abstract":
                    abstract = section_text
                elif current_section == "Introduction":
                    introduction = section_text
                elif current_section in ["Methods", "Methodology"]:
                    methods = section_text
                elif current_section == "Results":
                    results = section_text
                elif current_section == "Discussion":
                    discussion = section_text
                elif current_section in ["Conclusion", "Conclusions"]:
                    conclusion = section_text
                elif current_section in ["References", "Bibliography"]:
                    # Extract references
                    for ref_line in section_content:
                        if ref_line.strip():
                            references.append(ref_line.strip())
                
                section_content = []
            
            # Start new section
            if line.startswith('# '):
                current_section = line.replace('# ', '')
            else:
                current_section = line.replace('## ', '')
        else:
            section_content.append(line)
    
    # Process the last section
    if current_section and section_content:
        section_text = '\n'.join(section_content)
        if current_section == "Abstract":
            abstract = section_text
        elif current_section == "Introduction":
            introduction = section_text
        elif current_section in ["Methods", "Methodology"]:
            methods = section_text
        elif current_section == "Results":
            results = section_text
        elif current_section == "Discussion":
            discussion = section_text
        elif current_section in ["Conclusion", "Conclusions"]:
            conclusion = section_text
        elif current_section in ["References", "Bibliography"]:
            # Extract references
            for ref_line in section_content:
                if ref_line.strip():
                    references.append(ref_line.strip())
    
    # If no abstract found, use the first paragraph as abstract
    if not abstract and introduction:
        paragraphs = introduction.split('\n\n')
        if paragraphs:
            abstract = paragraphs[0]
    
    # Create PDF agent
    agent = PDFAgent()
    
    # Prepare content for scientific PDF
    scientific_content = {
        "title": title,
        "subtitle": "Theory of Everything Scientific Documentation",
        "abstract": abstract,
        "introduction": introduction,
        "methods": methods,
        "results": results,
        "discussion": discussion,
        "conclusion": conclusion,
        "references": references
    }
    
    # Generate enhanced scientific PDF
    pdf_path = agent.create_scientific_document(
        title,
        scientific_content,
        output_pdf_path
    )
    
    return pdf_path is not None

def enhance_all_documentation():
    """Enhance all documentation PDFs"""
    # Define base directories
    docs_dir = "/home/codephreak/theoryofeverything/theoryofeverything/docs"
    pdf_dir = os.path.join(docs_dir, "pdf")
    enhanced_dir = os.path.join(pdf_dir, "enhanced")
    
    # Create enhanced directory if it doesn't exist
    os.makedirs(enhanced_dir, exist_ok=True)
    
    # Enhance main documentation files
    markdown_files = [
        ("DOCUMENTATION.md", "Enhanced_Documentation.pdf"),
        ("USER_GUIDE.md", "Enhanced_User_Guide.pdf"),
        ("EXPLANATION.md", "Enhanced_Explanation.pdf"),
        ("AGENT_VISUALIZATIONS.md", "Enhanced_Agent_Visualizations.pdf"),
        ("ENHANCED_VISUALIZATIONS.md", "Enhanced_Visualization_Guide.pdf"),
        ("FORMULA_IMPROVEMENTS.md", "Enhanced_Formula_Guide.pdf"),
        ("README_MODULAR.md", "Enhanced_Modular_Architecture.pdf")
    ]
    
    # Process each markdown file
    for markdown_file, output_pdf in markdown_files:
        markdown_path = os.path.join(docs_dir, markdown_file)
        output_path = os.path.join(enhanced_dir, output_pdf)
        
        if os.path.exists(markdown_path):
            # Determine if it's a scientific document
            is_scientific = "EXPLANATION" in markdown_file or "DOCUMENTATION" in markdown_file
            
            if is_scientific:
                success = enhance_scientific_pdf(markdown_path, output_path)
            else:
                success = enhance_documentation_pdf(markdown_path, output_path)
            
            if success:
                print(f"Successfully enhanced {markdown_file} to {output_pdf}")
            else:
                print(f"Failed to enhance {markdown_file}")
        else:
            print(f"Markdown file not found: {markdown_path}")
    
    # Create a comprehensive Theory of Everything PDF
    create_comprehensive_pdf(docs_dir, enhanced_dir)
    
    print("\nEnhancement complete. Enhanced PDFs are available in:")
    print(enhanced_dir)

def create_comprehensive_pdf(docs_dir, output_dir):
    """Create a comprehensive Theory of Everything PDF"""
    print("Creating comprehensive Theory of Everything PDF...")
    
    # Define the markdown files to include, in order
    markdown_files = [
        "DOCUMENTATION.md",
        "EXPLANATION.md",
        "USER_GUIDE.md",
        "FORMULA_IMPROVEMENTS.md",
        "ENHANCED_VISUALIZATIONS.md",
        "AGENT_VISUALIZATIONS.md",
        "README_MODULAR.md"
    ]
    
    # Collect content from all files
    title = "Comprehensive Theory of Everything"
    sections = []
    
    for markdown_file in markdown_files:
        markdown_path = os.path.join(docs_dir, markdown_file)
        if os.path.exists(markdown_path):
            content = read_markdown_file(markdown_path)
            if content:
                # Extract file-specific sections
                file_sections = extract_sections_from_markdown(content)
                
                # Add a section header for the file
                file_title = extract_title_from_markdown(content)
                sections.append({
                    "title": file_title,
                    "text": f"The following sections are from {markdown_file}."
                })
                
                # Add the file's sections
                sections.extend(file_sections)
        else:
            print(f"Markdown file not found: {markdown_path}")
    
    # Create PDF agent
    agent = PDFAgent()
    agent.set_style_theme("professional")
    
    # Prepare content for comprehensive PDF
    pdf_content = {
        "title": title,
        "subtitle": "Complete Documentation",
        "sections": sections
    }
    
    # Generate comprehensive PDF
    output_path = os.path.join(output_dir, "Comprehensive_Theory_of_Everything.pdf")
    pdf_path = agent.create_pdf(
        pdf_content,
        output_path,
        title=title,
        author="Theory of Everything Team",
        subject="Comprehensive Theory of Everything Documentation"
    )
    
    if pdf_path:
        print(f"Successfully created comprehensive PDF: {output_path}")
    else:
        print("Failed to create comprehensive PDF")

if __name__ == "__main__":
    enhance_all_documentation()

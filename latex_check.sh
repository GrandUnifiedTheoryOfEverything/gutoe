#!/bin/bash

# Add LaTeX check to install.sh
awk '
/pip install -r requirements.txt/ {
    print
    print "print_green \"Required packages installed successfully!\""
    print ""
    print "# Check if LaTeX is installed"
    print "if ! command -v pdflatex &> /dev/null; then"
    print "    print_yellow \"WARNING: LaTeX (pdflatex) is not installed. PDF generation will not work.\""
    print "    print_yellow \"To install LaTeX:\""
    print "    print_yellow \"  - Linux: sudo apt-get install texlive-full\""
    print "    print_yellow \"  - macOS: brew install --cask mactex\""
    print "    print_yellow \"  - Windows: Download and install MiKTeX from https://miktex.org/\""
    print "else"
    print "    print_green \"LaTeX (pdflatex) is installed. PDF generation will work correctly.\""
    print "fi"
    next
}
/print_green "Required packages installed successfully!"/ {
    next
}
{print}
' install.sh > install.sh.new

mv install.sh.new install.sh
chmod +x install.sh

echo "Updated install.sh with LaTeX check"

#!/usr/bin/env python3
"""
Setup script for the Theory of Everything package
"""

from setuptools import setup, find_packages

setup(
    name="theoryofeverything",
    version="1.0.0",
    description="A Unified Framework for Physics",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Professor Codephreak",
    author_email="info@theoryofeverything.org",
    url="https://github.com/your-username/theoryofeverything",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy",
        "scipy",
        "sympy",
        "matplotlib",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "toe=theoryofeverything.cli:main",
        ],
    },
)

#!/usr/bin/env python3
"""Setup script for Customer Analytics MCP Server."""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements(filename):
    with open(filename, "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#") and not line.startswith("-r")]

setup(
    name="mcp-demo-server",
    version="0.1.0",
    description="A Model Context Protocol (MCP) server for fetching messages from an API endpoint",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/mcp-demo-server",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=read_requirements("requirements.txt"),
    extras_require={
        "dev": read_requirements("requirements-dev.txt")[1:]  # Skip the -r requirements.txt line
    },
    entry_points={
        "console_scripts": [
            "mcp-demo-server=mcp_demo_server.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="mcp model-context-protocol api messages http-client",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/mcp-demo-server/issues",
        "Source": "https://github.com/yourusername/mcp-demo-server",
        "Documentation": "https://github.com/yourusername/mcp-demo-server#readme",
    },
) 
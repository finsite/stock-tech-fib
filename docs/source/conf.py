import os
import sys

# Ensure Sphinx can find your project's source code
sys.path.insert(0, os.path.abspath("../../src"))  # Adjust if needed
sys.path.insert(0, os.path.abspath("../../src/app"))  # Adjust if needed

# Enable Sphinx extensions
extensions = [
    "sphinx.ext.autodoc",  # Auto-generate documentation from docstrings
    "sphinx.ext.napoleon",  # Support for Google-style and NumPy-style docstrings
    "sphinx.ext.viewcode",  # Include source code links
    "myst_parser",  # Support for Markdown files
]

# Use ReadTheDocs theme
html_theme = "sphinx_rtd_theme"

# Support both `.rst` and `.md` files
source_suffix = {".rst": "restructuredtext", ".md": "markdown"}

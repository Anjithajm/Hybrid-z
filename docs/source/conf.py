# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------

project = 'Hybrid-z'
author = 'Anjitha M'
copyright = '2026, Anjitha M'

# The full version, including alpha/beta/rc tags
release = '1.0'
version = '1.0.0'

# -- General configuration ---------------------------------------------------

# Sphinx extensions
extensions = [
    'sphinx.ext.duration',       # optional: build duration reporting
    'sphinx.ext.doctest',        # optional: test snippets in docs
    'sphinx.ext.autodoc',        # automatically document Python modules
    'sphinx.ext.autosummary',    # generate API summary pages
    'sphinx.ext.intersphinx',    # link to other projects docs
    'sphinx.ext.napoleon',       # support NumPy / Google style docstrings
    'sphinx_autodoc_typehints',  # optional: include type hints in docs
]

# Intersphinx mapping (link to external documentation)
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'tensorflow': ('https://www.tensorflow.org/api_docs/python', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
}
intersphinx_disabled_domains = ['std']

# Paths for templates
templates_path = ['_templates']

# List of patterns to ignore
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Generate autosummary pages automatically
autosummary_generate = True

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Options for EPUB output -------------------------------------------------
epub_show_urls = 'footnote'

# -- API module paths --------------------------------------------------------

import os
import sys
sys.path.insert(0, os.path.abspath('../'))  # Add repo root to Python path

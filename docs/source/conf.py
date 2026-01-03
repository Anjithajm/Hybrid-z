# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------

project = 'Hybrid-z'
author = 'Anjitha M'
copyright = '2026, Anjitha M'

release = '1.0'
version = '1.0.0'

# -- General configuration ---------------------------------------------------

# Sphinx extensions
extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
]

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'tensorflow': ('https://www.tensorflow.org/api_docs/python', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
autosummary_generate = True

# HTML output
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# EPUB output
epub_show_urls = 'footnote'

# -- Add repo root to sys.path for autodoc -----------------------------------

import os
import sys
sys.path.insert(0, os.path.abspath('../'))  # repo root

# -- Mock heavy dependencies for Read the Docs --------------------------------
# RTD cannot install TensorFlow, NumPy, Pandas, Matplotlib, etc.
# So we mock them during the doc build to avoid import errors

from unittest.mock import MagicMock

MOCK_MODULES = [
    'tensorflow',
    'numpy',
    'pandas',
    'matplotlib',
    'astropy',
    'sklearn'
]

for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = MagicMock()

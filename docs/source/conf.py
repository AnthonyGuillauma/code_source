import os
import sys

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'LogBuster'
copyright = '2025, Anthony GUILLAUMA'
author = 'Anthony GUILLAUMA'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode', 'sphinx.ext.napoleon']

templates_path = ['_templates']
exclude_patterns = []

language = 'fr'

# Ajout du chemin vers les modules
sys.path.insert(0, os.path.abspath('../../app'))

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ["documentation.css"]
html_theme_options = {
    "collapse_navigation": False,   # Pour éviter la fermeture automatique
    "sticky_navigation": True,  # Pour rendre le menu toujours visible
    "titles_only": False    # Pour éviter de masquer les sous-sections
}
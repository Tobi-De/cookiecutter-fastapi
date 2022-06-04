"""Sphinx configuration."""
project = "Fastapi Paginator"
author = "Tobi DEGNON"
copyright = "2022, Tobi DEGNON"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"

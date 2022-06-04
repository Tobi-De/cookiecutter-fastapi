"""Sphinx configuration."""
project = "Cookiecutter Fastapi"
author = "Tobi DEGNON"
copyright = "2022, Tobi DEGNON"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
myst_enable_extensions = ["tasklist"]
autodoc_typehints = "description"
html_theme = "furo"

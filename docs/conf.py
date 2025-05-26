"""Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
- https://www.sphinx-doc.org/en/master/usage/configuration.html
- https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
"""

import os
import sys
from typing import Any

sys.path.insert(0, os.path.abspath("../"))
project = "packio"
copyright = "2025, Zach Kurtz"
author = "Zach Kurtz"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.linkcode",
    "sphinx_rtd_theme",
    "sphinx_autodoc_typehints",
    "autoapi.extension",
]
autoapi_type = "python"
autoapi_dirs = ["../packio"]

# AutoAPI configuration
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "special-members",
    "imported-members",
]
autoapi_python_class_content = "both"
autoapi_member_order = "bysource"
autoapi_add_toctree_entry = False  # We'll handle this in our index.rst

templates_path = ["_templates"]
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    ".venv",
    "dev.py",
    "autoapi/processing/index.rst",
    "autoapi/run/index.rst",
]

autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "show-inheritance": True,
    "special-members": "__call__, __init__",
    "imported-members": False,
    "private-members": False,
}
autodoc_class_signature = "separated"
autodoc_member_order = "bysource"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_static_path = ["_static"]
html_css_files = ["css/custom.css"]
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "collapse_navigation": False,  # Don't collapse navigation entries
    "sticky_navigation": True,  # Make navigation scrollable with content
    "titles_only": False,  # Show full titles in navigation
}


def linkcode_resolve(domain: str, info: dict[str, Any]) -> str | None:
    """Utility function to generate GitHub source links."""
    if domain != "py":
        return None
    if not info["module"]:
        return None

    # Your GitHub username and repository name
    github_user = "zkurtz"
    github_repo = "packio"

    # Get the branch or tag (typically 'main' or 'master')
    github_branch = "main"  # Change to your default branch

    filename = info["module"].replace(".", "/")
    return f"https://github.com/{github_user}/{github_repo}/blob/{github_branch}/{filename}.py"

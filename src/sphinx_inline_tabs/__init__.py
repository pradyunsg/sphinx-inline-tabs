"""Add inline tabbed content to your Sphinx documentation."""

import os

__version__ = "2023.04.21.dev14"
__all__ = ["setup"]


def setup(app):
    """Entry point for sphinx theming."""
    app.require_sphinx("3.0")

    # We do imports from Sphinx, after validating the Sphinx version
    from ._impl import (
        CodeTabDirective,
        TabDirective,
        TabHtmlTransform,
        _TabInput,
        _TabLabel,
    )

    app.add_directive("tab", TabDirective)
    app.add_directive("code-tab", CodeTabDirective)
    app.add_post_transform(TabHtmlTransform)
    app.add_node(_TabInput, html=(_TabInput.visit, _TabInput.depart))
    app.add_node(_TabLabel, html=(_TabLabel.visit, _TabLabel.depart))

    # Include our static assets
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    app.connect(
        "builder-inited", (lambda app: app.config.html_static_path.append(static_dir))
    )

    app.add_js_file("tabs.js")
    app.add_css_file("tabs.css")

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
        "version": __version__,
    }

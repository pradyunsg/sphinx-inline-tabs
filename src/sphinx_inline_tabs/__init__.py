"""Add inline tabbed content to your Sphinx documentation."""

import os

from sphinx.config import ENUM

__version__ = "2023.04.21.dev14"
__all__ = ["setup"]


def setup(app):
    """Entry point for sphinx theming."""
    app.require_sphinx("3.0")

    # We do imports from Sphinx, after validating the Sphinx version
    from ._impl import TabContainer, TabDirective, TabHtmlTransform, TabInput, TabLabel

    app.add_config_value(
        "tabs_default_sync_behavior",
        "tab-title",
        "html",
        types=ENUM("tab-title", "none"),
    )
    app.add_config_value("tabs_no_sync_labels", set(), "html", types=[set])
    app.add_directive("tab", TabDirective)
    app.add_post_transform(TabHtmlTransform)
    app.add_node(TabInput, html=(TabInput.visit, TabInput.depart))
    app.add_node(TabLabel, html=(TabLabel.visit, TabLabel.depart))
    app.add_node(TabContainer, xml=(lambda _, __: None, lambda _, __: None))

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

"""Add inline tabbed content to your Sphinx documentation."""

__version__ = "2021.03.19.beta5"
__all__ = ["setup"]


def setup(app):
    """Entry point for sphinx theming."""
    import os
    from ._impl import TabDirective, TabHtmlTransform, _TabInput, _TabLabel

    app.require_sphinx("3.0")

    app.add_directive("tab", TabDirective)
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

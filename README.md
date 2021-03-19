# Sphinx Inline Tabs

![demo image](https://raw.githubusercontent.com/pradyunsg/sphinx-inline-tabs/main/docs/_static/demo.png)

<!-- start-include-here -->

Add inline tabbed content to your Sphinx documentation.

## Installation

This project is available on PyPI, and can be installed using pip:

```
pip install sphinx-inline-tabs
```

You'll also want to add the extension to `extensions` in `conf.py`:

```python
extensions = [
    ...,
    "sphinx_inline_tabs",
    ...,
]
```

## Features

- **Elegant design**: Small footprint in the markup and generated website, while looking good.
- **Configurable**: All the colors can be configured using CSS variables.
- **Synchronisation**: Tabs with the same label all switch with a single click.
- **Works without JavaScript**: JavaScript is not required for the basics, only for synchronisation.

<!-- end-include-here -->

## Contributing

sphinx-inline-tabs is a volunteer maintained open source project, and we welcome contributions of all forms. This is a fairly small package, and the development workflow is very similar to [Furo's development workflow](https://pradyunsg.me/furo/contributing/workflow/).

The [Code of Conduct](CODE_OF_CONDUCT.md) applies within all community spaces. If you are not familiar with our Code of Conduct policy, take a minute to read the policy before starting with your first contribution.

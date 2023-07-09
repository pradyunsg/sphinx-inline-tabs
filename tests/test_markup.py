"""Tests to ensure that the generated markup is correct.
"""

from pathlib import Path

import bs4
import pytest
from pytest_regressions.file_regression import FileRegressionFixture
from sphinx.testing.path import path as sphinx_path
from sphinx.testing.util import SphinxTestApp

DOCSET_ROOT = Path(__file__).parent / "docsets"
INPUT_FILES = {
    "markdown": "markdown.md",
    "restructuredtext": "restructuredtext.rst",
}


def only_role_main(html: str) -> str:
    """Return the content of the main role."""
    soup = bs4.BeautifulSoup(html, "html.parser")
    node = soup.find(attrs={"role": "main"})
    assert node
    return node.prettify(formatter=bs4.formatter.HTMLFormatter(indent=2))


@pytest.mark.parametrize("format", ["markdown", "restructuredtext"])
@pytest.mark.parametrize("builder", ["html"])
@pytest.mark.parametrize("docset", DOCSET_ROOT.glob("*"), ids=lambda path: path.name)
def test_markup(
    format: str,
    builder: str,
    docset: Path,
    file_regression: FileRegressionFixture,
    tmpdir: str,
) -> None:
    # GIVEN
    srcdir = sphinx_path(docset)
    builddir = sphinx_path(tmpdir)
    app = SphinxTestApp(srcdir=srcdir, builddir=builddir, buildername=builder)

    infile = Path(app.srcdir) / INPUT_FILES[format]
    outfile = Path(app.outdir) / f"{format}.{builder}"

    # WHEN
    app.build(filenames=[str(infile)])

    # THEN
    content = outfile.read_text()
    if builder == "html":
        content = only_role_main(content)
    file_regression.check(content, extension=f".{builder}")

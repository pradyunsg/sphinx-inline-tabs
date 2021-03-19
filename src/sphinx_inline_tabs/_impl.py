"""The actual implementation."""

from typing import List

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx.util.docutils import SphinxDirective
from sphinx.util.nodes import NodeMatcher


class TabContainer(nodes.container):
    """The initial tree-node for holding tab content."""


class _GeneralHTMLTagElement(nodes.Element, nodes.General):
    @staticmethod
    def visit(translator, node):
        attributes = node.attributes.copy()
        # Nobody needs this crap.
        attributes.pop("ids")
        attributes.pop("classes")
        attributes.pop("names")
        attributes.pop("dupnames")
        attributes.pop("backrefs")

        text = translator.starttag(node, node.tagname, **attributes)
        translator.body.append(text.strip())

    @staticmethod
    def depart(translator, node):
        if node.endtag:
            translator.body.append(f"</{node.tagname}>")


class _TabInput(_GeneralHTMLTagElement):
    tagname = "input"
    endtag = False


class _TabLabel(_GeneralHTMLTagElement):
    tagname = "label"
    endtag = True


class TabDirective(SphinxDirective):
    """Tabbed content in Sphinx documentation."""

    required_arguments = 1  # directive takes a single argument.
    final_argument_whitespace = True  # this allows that argument to contain spaces.
    has_content = True
    option_spec = {
        "new-set": directives.flag,
    }

    def run(self):
        """Parse a tabs directive."""
        self.assert_has_content()

        container = TabContainer("", type="tab", new_set="new-set" in self.options)
        self.set_source_info(container)

        # Handle the label (non-plain-text variants allowed)
        textnodes, messages = self.state.inline_text(self.arguments[0], self.lineno)
        label = nodes.rubric(self.arguments[0], *textnodes)

        # Handle the content
        content = nodes.container("", is_div=True, classes=["tab-content"])
        self.state.nested_parse(self.content, self.content_offset, content)

        container += label
        container += content

        return [container]


def _should_start_new_set(node, current_tab_set):
    # The current set is empty.
    if not current_tab_set:
        return False

    # Explicitly requested for a new tab set.
    if node["new_set"]:
        return True

    # From here, this code is trying to figure if the given node immediately
    # follows the previous tab, and hence should be in the same set.
    prev_node = current_tab_set[-1]
    if prev_node.parent != node.parent:  # Different parent
        return True

    parent = node.parent
    if parent.index(node) - 1 != parent.index(prev_node):
        return True

    # This node should be in the same set, so don't start a new one.
    return False


class TabHtmlTransform(SphinxPostTransform):
    """Transform output of TabDirective into usable chunks."""

    default_priority = 200
    formats = ["html"]

    def run(self):
        """Locate and replace `TabContainer`s."""
        matcher = NodeMatcher(TabContainer)

        set_counter = 0
        current_tab_set = []  # type: List[TabContainer]
        for node in self.document.traverse(matcher):  # type: TabContainer
            if _should_start_new_set(node, current_tab_set):
                self.finalize_set(current_tab_set, set_counter)
                set_counter += 1
                current_tab_set = []
            current_tab_set.append(node)

        if current_tab_set:
            self.finalize_set(current_tab_set, set_counter)

    def finalize_set(self, tab_set: List[TabContainer], set_counter: int):
        """Add these TabContainers as a single-set-of-tabs."""
        assert tab_set

        parent = tab_set[0].parent

        container = nodes.container("", is_div=True, classes=["tab-set"])
        container.parent = parent

        tab_set_name = f"tab-set--{set_counter}"
        node_counter = 0
        for node in tab_set:
            node_counter += 1
            tab_id = tab_set_name + f"-input--{node_counter}"
            title, content = node.children

            # <input>, for storing state in radio boxes.
            input_node = _TabInput(
                type="radio", ids=[tab_id], name=tab_set_name, classes=["tab-input"]
            )

            # <label>
            label_node = _TabLabel(
                "", *title.children, **{"for": tab_id}, classes=["tab-label"]
            )

            # For error messages
            input_node.source = node.source
            input_node.line = node.line
            label_node.source = node.source
            label_node.line = node.line

            # Populate with the content.
            container += input_node
            container += label_node
            container += content

        container.children[0]["checked"] = True

        # Replace all nodes in tab_set, with the container.
        start_at = parent.index(tab_set[0])
        end_at = parent.index(tab_set[-1])

        parent.children = (
            parent.children[:start_at] + [container] + parent[end_at + 1 :]
        )

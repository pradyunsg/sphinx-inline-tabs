"""The actual implementation."""

import itertools
from typing import List, Literal

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
        # The signature of this object is:
        #     __init__(self, rawsource='', text='', *children, **attributes)
        #
        # We want to directly populate the children here.
        label = nodes.label("", "", *textnodes)

        # Handle the content
        content = nodes.container("", is_div=True, classes=["tab-content"])
        self.state.nested_parse(self.content, self.content_offset, content)

        container += label
        container += content

        return [container]


class TabHtmlTransform(SphinxPostTransform):
    """Transform output of TabDirective into usable chunks."""

    default_priority = 200
    formats = ["html"]

    def run(self):
        """Locate and replace `TabContainer`s."""
        self.stack = []  # type: List[List[TabContainer]]
        self.counter = itertools.count(start=0, step=1)

        matcher = NodeMatcher(TabContainer)
        for node in self.document.traverse(matcher):  # type: TabContainer
            self._process_one_node(node)

        while self.stack:
            tab_set = self.stack.pop()
            self.finalize_set(tab_set, next(self.counter))

    def _process_one_node(self, node: TabContainer):
        # There is no existing tab set. Let's start a new one.
        if not self.stack:
            self.stack.append([node])
            return

        # There should never be an empty "current" tab set.
        assert self.stack[-1]

        close_till = None
        append = False
        for tab_set in reversed(self.stack[:]):
            last_node = tab_set[-1]

            # Is this node a direct child of the last node in this tab-set?
            is_child = node in last_node.children[1]
            if is_child:
                close_till = tab_set
                append = False
                break

            # Is this node a sibling of the last node in this tab-set?
            is_sibling = (
                node.parent == last_node.parent  # same parent
                # immediately after the previous node
                and node.parent.index(last_node) + 1 == node.parent.index(node)
            )
            if is_sibling:
                close_till = tab_set
                append = True
                break

        # Close all tab sets as required.
        if close_till is not None:
            while self.stack[-1] != close_till:
                self.finalize_set(self.stack.pop(), next(self.counter))
        else:
            while self.stack:
                self.finalize_set(self.stack.pop(), next(self.counter))

        # Start a new tab set, as required or if requested.
        if append and not node["new_set"]:
            assert self.stack
            self.stack[-1].append(node)
        else:
            self.stack.append([node])

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

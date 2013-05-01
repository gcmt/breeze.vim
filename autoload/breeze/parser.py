# -*- coding: utf-8 -*-
"""
breeze.parser
~~~~~~~~~~~~~

Parser class definition.

The Parser is responsible for parsing the current buffer and generating
a DOM tree.
"""

import vim
import itertools

import breeze.utils.misc
import breeze.utils.settings

try:
    # python 3
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser


class Node(object):
    """Node definition."""

    def __init__(self, tag="", attrs=None, parent=None, start=None, end=None):
        self.tag = tag          # tag name
        self.attrs = attrs      # a dictionary {attr: value, ..}
        self.start = start      # a tuple (row, col)
        self.end = end          # a tuple (row, col)
        self.parent = parent    # a Node or None (if root)
        self.children = []      # a list of Nodes

    def __str__(self):
        return "<{0} start={1} end={2}>".format(
            self.tag, self.start, self.end)

    def __repr__(self):
        return "<{0} start={1} end={2}>".format(
            self.tag, self.start, self.end)

    def id(self):
        """Returns the id attribute."""
        return self.attrs.get("id", [])

    def classes(self):
        """Returns the class attribute."""
        classes = self.attrs.get("class")
        if classes:
            return classes.split()
        else:
            return []

class Parser(HTMLParser):
    """Custom HTML parser."""

    def __init__(self):
        HTMLParser.__init__(self)  # TODO: check if this way is supported in python 3

        # module reference shortcuts
        self.misc = breeze.utils.misc

        self.tree = Node(tag="root")
        self.stack = [self.tree]
        self.empty_tags = dict((k, True) for k in
            ["br", "base", "hr", "meta", "link", "base", "link",
            "source", "meta", "img", "embed", "param", "area", "col", "input",
            "command", "keygen", "track", "wbr"])

    def feed(self, buffer):
        """Generates a brand new tree at each call."""
        self.tree = Node(tag="root")
        self.stack = [self.tree]
        HTMLParser.feed(self, "\n".join(buffer))
        self.close()
        self.reset()

    def handle_startendtag(self, tag, attrs):
        """Handles empty tags."""
        self.handle_starttag(tag, attrs, skip_emptytag_check=True)
        self.handle_endtag(tag)

    def handle_starttag(self, tag, attrs, skip_emptytag_check=False):
        """Handles the start of a tag.

        Note how this method handles empty tags. The HTMLParser does not
        recognize self-enclosing tags if they aren't closed with '../>',
        although this is totally acceptable in non-XHTML documents. So we call
        the handle_startendtag tags by ourselves and we make sure we don't run
        infinite recursive calls with the skip_emptytag_check parameter.
        """
        if not skip_emptytag_check and tag in self.empty_tags:
            self.handle_startendtag(tag, attrs)
            return

        if self.stack:
            node = Node(tag, dict(attrs), self.stack[-1], self.getpos())
            self.stack[-1].children.append(node)
            self.stack.append(node)

    def handle_endtag(self, tag):
        """Handles the end of a tag.

        If a script tag is opened, ignore all the junk in there until
        the tag is closed.
        """
        if self.stack:
            if self.stack[-1].tag == "script" and tag != "script":
                # ignore everything inside script tag
                return

            self.stack[-1].end = self.getpos()
            self.stack.pop(-1)

    def get_current_node(self):
        """Searches for the closest tag that encloses our current cursor
        position."""
        if self.tree.children:
            node, depth = self._closest_node(
                self.tree.children[0], 0, None, -1, self.misc.cursor())
            return node

    def _closest_node(self, tree, depth, closest_node, closest_depth, pos):
        """Finds the closest tag that encloses our current cursor
        position."""
        row, col = pos
        startrow, startcol = tree.start[0], tree.start[1]
        endrow = tree.end[0]
        attrslen = self.misc.attrs_len(tree)

        if tree.tag in self.empty_tags:
            endcol = tree.start[1] + len(tree.tag) + attrslen + 1
        else:
            endcol = tree.end[1] + len(tree.tag) + 2

        # check if the current position is inside the tag boundaries
        if startrow < row < endrow:
            cond = True
        elif startrow == row and endrow != row and startcol <= col:
            cond = True
        elif endrow == row and startrow != row and col <= endcol:
            cond = True
        elif startrow == row and endrow == row and startcol <= col <= endcol:
            cond = True
        else:
            cond = False

        # if cond is True the tag encloses our position and we temporarily
        # assume that this is the closest tag relative to our position
        if cond:
            closest_node = tree
            closest_depth = depth

        # check recursively for the closest tag
        for c in tree.children:
            n, d, = self._closest_node(
                        c, depth + 1, closest_node, closest_depth, pos)

            if d > closest_depth:
                closest_node = n
                closest_depth = d

            if depth < closest_depth:
                # we have already found the closest node and we are going up
                # the tree structure (depth < closest_depth). There is no
                # need to continue the search
                return closest_node, closest_depth

        return closest_node, closest_depth

    def print_dom_tree(self, indent=2):
        """Print the parsed DOM tree."""

        def _print_tree(tree, depth, indent):
            """Internal function for printing the HTML tree."""
            print(" " * depth + tree.tag + pos)
            for c in tree.children:
                _print_tree(c, depth + indent, indent)

        if self.tree.children:
            _print_tree(self.tree.children[0], 0, indent)

    def all_nodes(self):
        """Returns all DOM nodes as a generator."""

        def _flatten(tree):
            g = [tree]
            for c in tree.children:
                g = itertools.chain(g, _flatten(c))
            return g

        if self.tree.children:
            return _flatten(self.tree.children[0])
        else:
            return []

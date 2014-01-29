# -*- coding: utf-8 -*-
"""
breeze.parser
~~~~~~~~~~~~~

This module defines the Parser and Node classes. The Parser is responsible for
parsing the current buffer and generating a DOM tree, whereas the Node class is
needed to represent a single HTML node.
"""

import vim
import itertools

from breeze.utils import v
from breeze.utils import misc

try:
    # python 3
    import html.parser as HTMLParser
except ImportError:
    import HTMLParser as HTMLParser


class Node:

    def __init__(self, tag="", starttag_text="", parent=None, start=None, end=None):
        self.tag = tag  # tag name
        self.starttag_text = starttag_text  # raw starttag text
        self.start = start  # a tuple (row, col)
        self.end = end  # a tuple (row, col)
        self.parent = parent  # a Node or None (if root)
        self.children = []  # a list of Nodes

    def __str__(self):
        return "<{0} start={1} end={2}>".format(self.tag, self.start, self.end)

    def __repr__(self):
        return "<{0} start={1} end={2}>".format(self.tag, self.start, self.end)


class Parser(HTMLParser.HTMLParser):

    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.last_known_error = None
        self.success = False
        self.tree = Node(tag="root")
        self.stack = [self.tree]

    def feed(self, buffer):
        """To generate a brand new tree at each call."""
        self.tree = Node(tag="root")
        self.stack = [self.tree]
        try:
            HTMLParser.HTMLParser.feed(self, "\n".join(buffer))
            self.success = True
            self.last_known_error = None
        except HTMLParser.HTMLParseError as e:
            self.last_known_error = dict(msg=e.msg, pos=(e.lineno, e.offset))
            self.tree = Node(tag="root")
            self.success = False
        finally:
            self.reset()

    def handle_startendtag(self, tag, attrs):
        """To handle empty tags."""
        self.handle_starttag(tag, attrs, skip_emptytag_check=True)
        self.handle_endtag(tag)

    def handle_starttag(self, tag, attrs, skip_emptytag_check=False):
        """To handle the start of a tag.

        Note how this method handles empty tags. The HTMLParser does not
        recognize self-closing tags if they aren't closed with '../>',
        although this is totally acceptable in non-XHTML documents. So we call
        the handle_startendtag tags by ourselves and we make sure we don't run
        infinite recursive calls with the skip_emptytag_check parameter.
        """
        if not skip_emptytag_check and tag in misc.empty_tags:
            self.handle_startendtag(tag, attrs)
            return

        if self.stack:
            # Note: getpos() return 1-indexed line numbers and 0-indexed
            # column numbers
            node = Node(tag, self.get_starttag_text(), self.stack[-1], self.getpos())
            self.stack[-1].children.append(node)
            self.stack.append(node)

    def handle_endtag(self, tag):
        """To handle the end of a tag.

        If a script tag is opened, ignore all the junk in there until
        the tag is closed.
        """
        if self.stack:
            if self.stack[-1].tag == "script" and tag != "script":
                # ignore everything inside script tag
                return

            if tag != self.stack[-1].tag:
                # tag mismatch
                if any(n.tag == tag for n in self.stack):
                    msg = "no closing tag for '<{0}>'".format(
                        self.stack[-1].tag)
                    pos = self.stack[-1].start
                else:
                    msg = "no opening tag for '</{0}>'".format(tag)
                    pos = self.getpos()
                raise HTMLParser.HTMLParseError(msg, pos)

            self.stack[-1].end = self.getpos()
            self.stack.pop(-1)

    def get_current_node(self):
        """To return the current element (the one that enclose our cursor position)."""
        for c in self.tree.children:
            node, depth = self._closest_node(c, 0, None, -1, v.cursor())
            if node:
                return node

    def _closest_node(self, tree, depth, closest_node, closest_depth, pos):
        """To find the closest element that encloses our current cursor position."""
        if not tree.start or not tree.end:
            if not tree.start:
                self.last_known_error = dict(msg="malformed tag found", pos=tree.end)
            if not tree.end:
                self.last_known_error = dict(msg="malformed tag found", pos=tree.start)
            return (None, -1)

        row, col = pos
        startrow, startcol = tree.start[0], tree.start[1]
        endrow = tree.end[0]

        if tree.tag in misc.empty_tags:
            endcol = tree.start[1] + len(tree.starttag_text)
        else:
            endcol = tree.end[1] + len(tree.tag) + 2

        # check if the current position is inside the element boundaries
        if startrow < row < endrow:
            cond = True
        elif startrow == row and endrow != row and startcol <= col:
            cond = True
        elif endrow == row and startrow != row and col <= endcol:
            cond = True
        elif startrow == row and endrow == row and startcol <= col < endcol:
            cond = True
        else:
            cond = False

        # if cond is True the current element (tree) eclose our position. Now
        # we assume this is the closest node that enclose our position.
        if cond:

            closest_node = tree
            closest_depth = depth

            if not tree.children:
                return closest_node, closest_depth

            # if the current position is closest to the end of the current
            # enclosing tag, start iterating its children from the last element,
            # and vice-versa. This little piece of code just aims to improve
            # performances, nothing else.
            if row - tree.start[0] > tree.end[0] - row:
                rev = True
            else:
                rev = False

            for child in (reversed(tree.children) if rev else tree.children):
                n, d = self._closest_node(child, depth + 1, closest_node, closest_depth, pos)

                if d > closest_depth:
                    # a child of tree node is closest to the current position.
                    closest_node = n
                    closest_depth = d

                if depth < closest_depth:
                    # we have already found the closest node and we are going up
                    # the tree structure (depth < closest_depth). There is no
                    # need to continue the search
                    return closest_node, closest_depth

            return closest_node, closest_depth

        else:
            # untouched
            return closest_node, closest_depth

    def print_dom_tree(self, indent=2):
        """To print the parsed DOM tree."""

        def _print_tree(tree, depth, indent):
            """Internal function for printing the HTML tree."""
            print(" " * depth + tree.tag)
            for c in tree.children:
                _print_tree(c, depth + indent, indent)

        for c in self.tree.children:
            _print_tree(c, 0, indent)

    def all_nodes(self):
        """To return all DOM nodes as a generator."""

        def _flatten(tree):
            nodes = [tree]
            for c in tree.children:
                nodes += _flatten(c)
            return nodes

        nodes = []
        for c in self.tree.children:
            nodes += _flatten(c)
        return nodes

    def get_error(self):
        """To return the last known error."""
        if self.last_known_error is not None:
            return "Error found at {pos}, type: {msg}".format(**self.last_known_error)
        return "All should be fine!"

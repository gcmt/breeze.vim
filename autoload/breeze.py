# -*- coding: utf-8 -*-
"""
breeze.py
~~~~~~~~~

This module defines all classes of the Breeze plugin.
"""

import os
import vim
try:
    # python 3
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser


sys.path.insert(0, os.path.split(
    vim.eval('fnameescape(globpath(&runtimepath, "' +
             os.path.join("autoload", "breeze.py") + '"))'))[0])

import breeze.utils.misc
import breeze.utils.settings


class Node(object):
    """HTML node definition."""

    def __init__(self, tag="", attrs=None, parent=None, start=None, end=None):
        self.tag = tag
        self.attrs = attrs
        self.start = start
        self.end = end
        self.parent = parent
        self.children = []

    def __str__(self):
        return "<{0} start={1} end={2}>".format(
            self.tag, self.start, self.end)

    def __repr__(self):
        return "<{0} start={1} end={2}>".format(
            self.tag, self.start, self.end)


class MyHTMLParser(HTMLParser):
    """Custom HTML parser."""
    # TODO: error handling for bad formatted html

    def __init__(self):
        HTMLParser.__init__(self)  # TODO: check if this way is supported in python 3
        self.tree = Node(tag="root")
        self.stack = [self.tree]
        self.empty_tags = dict((k, True) for k in
            ["br", "base", "hr", "meta", "link", "base", "link",
            "source", "meta", "img", "embed", "param", "area", "col", "input",
            "command", "keygen", "track", "wbr"])

    def feed(self, buffer):
        """Overrides the 'feed' method with some initialization so every time
        we call 'feed' we get a brand new tree."""
        self.tree = Node(tag="root")
        self.stack = [self.tree]
        HTMLParser.feed(self, "\n".join(buffer))
        self.close()
        self.reset()

    def handle_startendtag(self, tag, attrs):
        """Handles empty tags.

        'skip_emptytag_check' is used to prevent infinite recursive calls
        when calling 'handle_starttag'.
        """
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

        node = Node(tag, attrs, self.stack[-1], self.getpos())
        self.stack[-1].children.append(node)
        self.stack.append(node)

    def handle_endtag(self, tag):
        """Handles the end of a tag."""
        node = self.stack[-1].end = self.getpos()
        self.stack.pop(-1)

    def current_node(self):
        """High level method that search for the closest tag that encloses
        our current cursor position."""
        if self.tree.children:
            node, depth = self._closest_node(
                self.tree.children[0], 0, None, -1, vim.current.window.cursor)
            return node

    def _closest_node(self, tree, depth, closest_node, closest_depth, pos):
        """Finds the closest tag that encloses our current cursor position."""
        # compute tag boundaries
        row, col = pos
        startrow, startcol = tree.start[0], tree.start[1]
        endrow = tree.end[0]
        attrs = " ".join("{0}='{1}'".format(a, v) for a, v in tree.attrs)
        if tree.tag in self.empty_tags:
            endcol = tree.start[1] + len(tree.tag) + len(attrs) + 3
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

        # ok, we the tag encloses our position. Now we assume this is
        # the closest (reltive to our position) tag.
        if cond:
            closest_node = tree
            closest_depth = depth

        # check recursively
        for c in tree.children:
            n, d, = self._closest_node(
                        c, depth + 1, closest_node, closest_depth, pos)

            if d > closest_depth:
                closest_node = n
                closest_depth = d

        return closest_node, closest_depth

    def print_dom_tree(self, indent=2, showpos=False):
        """Print the parsed HTML tree."""
        if self.tree.children:
            self._print_tree(self.tree.children[0], 0, indent, showpos)

    def _print_tree(self, tree, depth, indent, showpos):
        """Internal function for printing the HTML tree."""
        if showpos:
            pos = " :: start={0} end={1}".format(tree.start, tree.end)
        else:
            pos = ""
        print(" " * depth + tree.tag + pos)

        for c in tree.children:
            self._print_tree(c, depth + indent, indent, showpos)


class Breeze(object):
    """Main Breeze class."""

    def __init__(self):
        # modules reference shortcuts
        self.settings = breeze.utils.settings
        self.misc = breeze.utils.misc

        # caching stuff
        self.recalculate = True
        self.cached_tree = None

        self.parser = MyHTMLParser()

    def parse_current_buffer(f):
        """This method exists in order to provide some primitive form of
        caching, though not implemented yet."""
        def wrapper(self, *args, **kwargs):
            # TODO: caching is not implemented yet, that is, the document
            # is parsed every time the user calls a command
            if self.recalculate:
                self.parser.feed(vim.current.buffer)
                self.cached_tree = self.parser.tree
            else:
                self.parser.tree = self.cached_tree
            return f(self, *args, **kwargs)
        return wrapper

    @parse_current_buffer
    def print_dom(self):
        """Prints the DOM tree."""
        self.parser.print_dom_tree()

    @parse_current_buffer
    def match_tag(self):
        """Matches the current tag.

        If the cursor isn't on the start line of the tag, the cursor is
        positioned at the opening tag. If the cursor is on the first line of
        the tag instead, the cursor is positioned at the closing tag.
        """
        node = self.parser.current_node()
        if node:
            row, _ = vim.current.window.cursor
            if row != node.start[0]:
                target = node.start
            else:
                target = node.end
            vim.current.window.cursor = target
        else:
            self.misc.echom("cannot locate the current node")

    @parse_current_buffer
    def goto_next_sibling(self):
        """Moves the cursor to the next sibling node."""
        node = self.parser.current_node()
        if node:
            if node.parent.tag != "root":
                ch = node.parent.children
                for i, c in enumerate(ch):
                    if c.start == node.start and c.end == node.end:
                        if i + 1 < len(ch):
                            target = ch[i+1].start
                            vim.current.window.cursor = target
                        else:
                            self.misc.echom("no more siblings found")
            else:
                self.misc.echom("no siblings found")
        else:
            self.misc.echom("cannot locate the current node")

    @parse_current_buffer
    def goto_prev_sibling(self):
        """Moves the cursor to the previous sibling node."""
        node = self.parser.current_node()
        if node:
            if node.parent.tag != "root":
                ch = node.parent.children
                for i, c in enumerate(ch):
                    if c.start == node.start and c.end == node.end:
                        if i - 1 >= 0:
                            target = ch[i-1].start
                            vim.current.window.cursor = target
                        else:
                            self.misc.echom("no more siblings found")
            else:
                self.misc.echom("no siblings found")
        else:
            self.misc.echom("cannot locate the current node")

    @parse_current_buffer
    def goto_first_child(self):
        """Moves the cursor to the first child of the current node."""
        node = self.parser.current_node()
        if node:
            if node.children:
                target = node.children[0].start
                vim.current.window.cursor = target
            else:
                self.misc.echom("no children found")
        else:
            self.misc.echom("cannot locate the current node")

    @parse_current_buffer
    def goto_last_child(self):
        """Moves the cursor to the last child of the current node."""
        node = self.parser.current_node()
        if node:
            if node.children:
                target = node.children[-1].start
                vim.current.window.cursor = target
            else:
                self.misc.echom("no children found")
        else:
            self.misc.echom("cannot locate the current node")

    @parse_current_buffer
    def goto_parent(self):
        """Moves the cursor to the parent of the current node."""
        node = self.parser.current_node()
        if node:
            if node.parent.tag != "root":
                target = node.parent.start
                vim.current.window.cursor = target
            else:
                self.misc.echom("no parent found")
        else:
            self.misc.echom("cannot locate the current node")

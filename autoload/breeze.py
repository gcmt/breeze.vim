# -*- coding: utf-8 -*-
"""
breeze.py
~~~~~~~~~

This module defines all classes of the Breeze plugin.
"""

import os
import vim
import time

sys.path.insert(0, os.path.split(
    vim.eval('fnameescape(globpath(&runtimepath, "' +
             os.path.join("autoload", "breeze.py") + '"))'))[0])

import breeze.parser
import breeze.jumper
import breeze.utils.misc
import breeze.utils.settings


class Breeze(object):
    """Main Breeze class."""

    def __init__(self):
        # modules reference shortcuts
        self.settings = breeze.utils.settings
        self.misc = breeze.utils.misc

        self.parser = breeze.parser.Parser()
        self.jumper = breeze.jumper.Jumper(self)

        self.setup_colors()

        # caching stuff
        self.refresh_cache = True
        self.cache = None

        # empty tags
        self.empty_tags = dict((k, True) for k in
            ["br", "base", "hr", "meta", "link", "base", "source", "meta",
             "img", "embed", "param", "area", "col", "input", "command",
             "keygen", "track", "wbr"])

        # profiling dom parsing
        self.calls = 0
        self.sum = 0
        self.average = 0

    def profile(f):
        def wrapper(self, *args, **kwargs):
            start = time.clock()
            r = f(self, *args, **kwargs)
            self.sum += (time.clock() - start)
            self.calls += 1
            self.average = self.sum / float(self.calls)
            return r
        return wrapper

    def parse_current_buffer(f):
        """This method exists in order to provide some primitive form of
        caching.

        This decorator ensures that the wrapped method will have access to
        a non empty DOM tree structure.
        """
        def wrapper(self, *args, **kwargs):
            if self.refresh_cache or vim.eval("&modified") == '1':
                self.parser.feed(vim.current.buffer)
                self.cache = self.parser.tree
                self.refresh_cache = False
            else:
                self.parser.tree = self.cache
            return f(self, *args, **kwargs)
        return wrapper

    def add_pos_to_jumplist(f):
        """Adds the current cursor position to the jump list.

        The user can come back with Ctrl+O.
        """
        def wrapper(self, *args, **kwargs):
            vim.command("normal! m'")
            return f(self, *args, **kwargs)
        return wrapper

    def setup_colors(self):
        """Setups highlight groups according to the current settings."""
        if vim.eval("&background") == 'light':
            shade = self.settings.get("shade_color")
            marks = self.settings.get("jumpmark_color")
            match = self.settings.get("tag_color")
            block = self.settings.get("tagblock_color")
        else:
            shade = self.settings.get("shade_color_darkbg")
            marks = self.settings.get("jumpmark_color_darkbg")
            match = self.settings.get("tag_color_darkbg")
            block = self.settings.get("tagblock_color_darkbg")

        vim.command("hi link BreezeShade {0}".format(shade))
        vim.command("hi link BreezeJumpMark {0}".format(marks))
        vim.command("hi link BreezeTag {0}".format(match))
        vim.command("hi link BreezeTagBlock {0}".format(block))

    @add_pos_to_jumplist
    @parse_current_buffer
    def jump_forward(self):
        """Jump forward!"""
        self.jumper.jump(backward=False)

    @add_pos_to_jumplist
    @parse_current_buffer
    def jump_backward(self):
        """Jump backward!"""
        self.jumper.jump(backward=True)

    @parse_current_buffer
    def highlight_curr_tag(self):
        """Highlights opening and closing tags."""
        self.misc.clear_highlighting()
        node = self.parser.get_current_node()
        if node:
            line, startcol = node.start[0], node.start[1]+1
            endcol = startcol + len(node.tag) + 1
            opening = "\\%{0}l\\%>{1}c\%<{2}c".format(
                line, startcol, endcol)
            self.misc.highlight("BreezeTag", opening)

            if node.tag not in self.empty_tags:

                line, startcol = node.end[0], node.end[1]+1
                endcol = startcol + len(node.tag) + 2
                closing = "\\%{0}l\\%>{1}c\%<{2}c".format(
                    line, startcol, endcol)
                self.misc.highlight("BreezeTag", closing)
        else:
            self.misc.echom("cannot locate the current node")

    @parse_current_buffer
    def highlight_tag_block(self, node=None, group=None):
        """Highlights the whole current tag. Same as the 'vap' movement.

        Because 'vap' does not work with empty tags and this may be useful
        for other niceties.
        """
        if group is None:
            group = "BreezeTagBlock"
        if node is None:
            node = self.parser.get_current_node()

        if node:
            if (node.tag not in self.empty_tags
                and node.start[0] != node.end[0]):

                # highlight first line
                sline, startcol = node.start[0], node.start[1]
                endcol = startcol + len(node.tag) + 1
                patt = "\\%{0}l\\%>{1}c".format(
                    sline, startcol, endcol)
                self.misc.highlight(group, patt)

                # highlight end line
                eline, startcol = node.end[0], node.end[1]+1
                endcol = startcol + len(node.tag) + 3
                closing = "\\%{0}l\\%<{1}c".format(
                    eline, endcol)
                self.misc.highlight(group, closing)

                # highlight the intern
                patt = "\\%>{0}l\\%<{1}l".format(sline, eline)
                self.misc.highlight(group, patt)

            else:
                if node.tag in self.empty_tags:
                    # highlight empty tag
                    sline, startcol = node.start[0], node.start[1]
                    endcol = startcol + len(node.tag) + 1
                    patt = "\\%{0}l\\%>{1}c".format(
                        sline, startcol, endcol)
                    self.misc.highlight(group, patt)
                else:
                    line, startcol = node.start[0], node.start[1]
                    endcol = node.end[1] + len(node.tag) + 4
                    patt = "\\%{0}l\\%>{1}c\\%<{2}c".format(
                        line, startcol, endcol)
                    self.misc.highlight(group, patt)
        else:
            self.misc.echom("cannot locate the current node")

    @add_pos_to_jumplist
    @parse_current_buffer
    def current_tag(self):
        """Matches the current tag.

        If the cursor isn't on the start line of the tag, the cursor is
        positioned at the opening tag. If the cursor is on the first line of
        the tag instead, the cursor is positioned at the closing tag.
        """
        node = self.parser.get_current_node()
        if node:
            row, _ = self.misc.cursor()
            if row != node.start[0]:
                target = node.start
            else:
                target = node.end
            self.misc.cursor((target[0], target[1]+2))
        else:
            self.misc.echom("cannot locate the current node")

    @add_pos_to_jumplist
    @parse_current_buffer
    def goto_next_sibling(self):
        """Moves the cursor to the next sibling node."""
        node = self.parser.get_current_node()
        if node:
            if node.parent.tag != "root":
                ch = node.parent.children
                for i, c in enumerate(ch):
                    if c.start == node.start and c.end == node.end:
                        if i + 1 < len(ch):
                            target = ch[i+1].start
                            self.misc.cursor((target[0], target[1]+2))
                        else:
                            self.misc.echom("no more siblings found")
            else:
                self.misc.echom("no siblings found")
        else:
            self.misc.echom("cannot locate the current node")

    @add_pos_to_jumplist
    @parse_current_buffer
    def goto_prev_sibling(self):
        """Moves the cursor to the previous sibling node."""
        node = self.parser.get_current_node()
        if node:
            if node.parent.tag != "root":
                ch = node.parent.children
                for i, c in enumerate(ch):
                    if c.start == node.start and c.end == node.end:
                        if i - 1 >= 0:
                            target = ch[i-1].start
                            self.misc.cursor((target[0], target[1]+2))
                        else:
                            self.misc.echom("no more siblings found")
            else:
                self.misc.echom("no siblings found")
        else:
            self.misc.echom("cannot locate the current node")

    @add_pos_to_jumplist
    @parse_current_buffer
    def goto_first_child(self):
        """Moves the cursor to the first child of the current node."""
        node = self.parser.get_current_node()
        if node:
            if node.children:
                target = node.children[0].start
                self.misc.cursor((target[0], target[1]+2))
            else:
                self.misc.echom("no children found")
        else:
            self.misc.echom("cannot locate the current node")

    @add_pos_to_jumplist
    @parse_current_buffer
    def goto_last_child(self):
        """Moves the cursor to the last child of the current node."""
        node = self.parser.get_current_node()
        if node:
            if node.children:
                target = node.children[-1].start
                self.misc.cursor((target[0], target[1]+2))
            else:
                self.misc.echom("no children found")
        else:
            self.misc.echom("cannot locate the current node")

    @add_pos_to_jumplist
    @parse_current_buffer
    def goto_parent(self):
        """Moves the cursor to the parent of the current node."""
        node = self.parser.get_current_node()
        if node:
            if node.parent.tag != "root":
                target = node.parent.start
                self.misc.cursor((target[0], target[1]+2))
            else:
                self.misc.echom("no parent found")
        else:
            self.misc.echom("cannot locate the current node")

    @add_pos_to_jumplist
    @parse_current_buffer
    def print_dom(self):
        """Prints the DOM tree."""
        self.parser.print_dom_tree()

# -*- coding: utf-8 -*-
"""
breeze.core
~~~~~~~~~~~

This module defines Breeze class.
"""

import os
import vim

from breeze import parser
from breeze import jumper
from breeze.utils import v
from breeze.utils import misc
from breeze.utils import settings


class Breeze:

    def __init__(self):
        self.parser = parser.Parser()
        self.jumper = jumper.Jumper(self)
        self.setup_colors()
        # caching stuff
        self.refresh_cache = True
        self.cache = None

    def parse_current_buffer(f):
        """To provide some naive form of caching.

        This decorator ensures that the wrapped method will have access to
        a fully parsed DOM tree structure for the current buffer.
        """
        def wrapper(self, *args, **kwargs):
            if self.refresh_cache or vim.eval("&mod") == '1':
                self.parser.feed(vim.current.buffer)
                if self.parser.success:
                    self.cache = self.parser.tree
                    self.refresh_cache = False
                else:
                    v.clear_hl('BreezeJumpMark', 'BreezeShade')
                    self.refresh_cache = True
                    return
            else:
                self.parser.tree = self.cache
            return f(self, *args, **kwargs)
        return wrapper

    def remember_curr_pos(f):
        """To add the current cursor position to the jump list so that the user
        can come back with CTRL+O.
        """
        def wrapper(self, *args, **kwargs):
            vim.command("normal! m'")
            return f(self, *args, **kwargs)
        return wrapper

    def setup_colors(self):
        """To setup Breeze highlight groups."""
        postfix = "" if vim.eval("&bg") == "light" else "_darkbg"
        shade = settings.get("shade_color{}".format(postfix))
        mark = settings.get("jumpmark_color{}".format(postfix))
        hl = settings.get("hl_color{}".format(postfix))
        for g, color in (("Shade", shade), ("JumpMark", mark), ("Hl", hl)):
            if "=" in color:
                vim.command("hi Breeze{} {}".format(g, color))
            else:
                vim.command("hi link Breeze{} {}".format(g, color))

    @remember_curr_pos
    @parse_current_buffer
    def jump_forward(self):
        """Jump forward! Displays jump marks, asks for the destination and
        jumps to the selected tag."""
        self.jumper.jump(backward=False)

    @remember_curr_pos
    @parse_current_buffer
    def jump_backward(self):
        """Jump backward! Displays jump marks, asks for the destination and
        jumps to the selected tag."""
        self.jumper.jump(backward=True)

    @parse_current_buffer
    def highlight_curr_element(self):
        """Highlights opening and closing tags of the current element."""
        v.clear_hl('BreezeHl')

        node = self.parser.get_current_node()
        if not node:
            return

        line, scol = node.start[0], node.start[1]+1
        ecol = scol + len(node.tag) + 1
        patt = "\\%{}l\\%>{}c\%<{}c".format(line, scol, ecol)
        v.highlight("BreezeHl", patt)

        if node.tag not in misc.empty_tags:
            line, scol = node.end[0], node.end[1]+1
            ecol = scol + len(node.tag) + 2
            patt = "\\%{}l\\%>{}c\%<{}c".format(line, scol, ecol)
            v.highlight("BreezeHl", patt)

    @remember_curr_pos
    @parse_current_buffer
    def match_tag(self):
        """Matches the current tag.

        If the cursor is on the first line of the tag the cursor is positioned
        at the closing tag, and vice-versa.  If the cursor isn't on the start
        line of the tag, the cursor is positioned at the opening tag.
        """
        node = self.parser.get_current_node()
        if node:
            row, col = v.cursor()
            if row != node.start[0]:
                target = node.start
            else:
                endcol = node.start[1] + len(node.starttag_text)
                if col < endcol:
                    target = node.end
                else:
                    target = node.start

            row, col = target
            if not settings.get("jump_to_angle_bracket", bool):
                col += 1
            v.cursor((row, col))

    @remember_curr_pos
    @parse_current_buffer
    def goto_next_sibling(self):
        """To move the cursor to the next sibling node."""
        node = self.parser.get_current_node()
        if node and node.parent:
            ch = node.parent.children
            for i, c in enumerate(ch):
                if c.start == node.start and c.end == node.end and i + 1 < len(ch):
                    row, col = ch[i+1].start
                    if not settings.get("jump_to_angle_bracket", bool):
                        col += 1
                    v.cursor((row, col))

    @remember_curr_pos
    @parse_current_buffer
    def goto_prev_sibling(self):
        """To move the cursor to the previous sibling node."""
        node = self.parser.get_current_node()
        if node and node.parent:
            ch = node.parent.children
            for i, c in enumerate(ch):
                if c.start == node.start and c.end == node.end and i - 1 >= 0:
                    row, col = ch[i-1].start
                    if not settings.get("jump_to_angle_bracket", bool):
                        col += 1
                    v.cursor((row, col))

    @remember_curr_pos
    @parse_current_buffer
    def goto_first_sibling(self):
        """To move the cursor to the first sibling node."""
        node = self.parser.get_current_node()
        if node and node.parent:
            row, col = node.parent.children[0].start
            if not settings.get("jump_to_angle_bracket", bool):
                col += 1
            v.cursor((row, col))

    @remember_curr_pos
    @parse_current_buffer
    def goto_last_sibling(self):
        """To move the cursor to the last sibling node."""
        node = self.parser.get_current_node()
        if node and node.parent:
            row, col = node.parent.children[-1].start
            if not settings.get("jump_to_angle_bracket", bool):
                col += 1
            v.cursor((row, col))

    @remember_curr_pos
    @parse_current_buffer
    def goto_first_child(self):
        """To move the cursor to the first child of the current node."""
        node = self.parser.get_current_node()
        if node and node.children:
            row, col = node.children[0].start
            if not settings.get("jump_to_angle_bracket", bool):
                col += 1
            v.cursor((row, col))

    @remember_curr_pos
    @parse_current_buffer
    def goto_last_child(self):
        """To move the cursor to the last child of the current node."""
        node = self.parser.get_current_node()
        if node and node.children:
            row, col = node.children[-1].start
            if not settings.get("jump_to_angle_bracket", bool):
                col += 1
            v.cursor((row, col))

    @remember_curr_pos
    @parse_current_buffer
    def goto_parent(self):
        """To move the cursor to the parent of the current node."""
        node = self.parser.get_current_node()
        if node:
            if node.parent.tag != "root":
                row, col = node.parent.start
                if not settings.get("jump_to_angle_bracket", bool):
                    col += 1
                v.cursor((row, col))
            else:
                v.echom("no parent found")

    @parse_current_buffer
    def print_dom(self):
        """To print the DOM tree."""
        self.parser.print_dom_tree()

    def whats_wrong(self):
        """To tell the user about the last encountered problem."""
        v.echom(self.parser.get_error())

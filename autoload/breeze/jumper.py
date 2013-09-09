# -*- coding: utf-8 -*-
"""
breeze.jumper
~~~~~~~~~~~~~

This module defines the Jumper class. The Jumper is responsible for the jumping
functionality:

    1. display jump marks on the current buffer
    2. ask the user for the destination mark
    3. jump to the selected mark

The only method that should be called from the outside and that provide
the above functionality is the "jump" method.
"""

import vim
import string

from breeze.utils import v
from breeze.utils import input
from breeze.utils import settings


class Jumper(object):

    def __init__(self, plug):
        self.plug = plug
        self.jump_marks = list(string.letters)

    def jump(self, backward=False):
        """To display jump marks and move to the selected jump mark."""
        table = self._show_jump_marks(backward)
        choice = None
        while choice not in table:
            choice = self._ask_target_key()
            if choice is None:
                break

        v.clear_hl('BreezeJumpMark', 'BreezeShade')
        self._clear_jump_marks(table)

        if choice:
            row, col = table[choice][0]
            if not settings.get("jump_to_angle_bracket", bool):
                col += 1
            v.cursor((row, col))

    def _show_jump_marks(self, backward=False):
        """To display jump marks."""
        top, bot = v.window_bundaries()
        v.highlight("BreezeShade", "\\%>{}l\\%<{}l".format(top-1, bot+1))

        table = {}
        jump_marks = self.jump_marks[:]
        vim.command("setl modifiable noreadonly")

        top, bot = v.window_bundaries()
        nodes = [node for node in self.plug.parser.all_nodes()
                 if node.start[0] >= top and node.start[0] <= bot]
        if backward:
            nodes = reversed(nodes)

        vim.command("try|undojoin|catch|endtry")
        curr_pos = v.cursor()
        curr_row, curr_col = curr_pos[0]-1, curr_pos[1]

        for node in nodes:

            tag_row, tag_col = node.start[0]-1, node.start[1]+1

            mark = None
            if jump_marks:

                if backward:
                    if tag_row < curr_row or (tag_row == curr_row and tag_col < curr_col):
                        mark = jump_marks[0]
                        jump_marks.pop(0)
                else:
                    if tag_row > curr_row or (tag_row == curr_row and tag_col > curr_col):
                        mark = jump_marks[0]
                        jump_marks.pop(0)

            if mark:
                old = v.subst_char(v.buf(), mark, tag_row, tag_col)
                self._highlight_jump_mark((tag_row+1, tag_col+1))
                table[mark] = (node.start, old)

        vim.command("setl nomodified")
        v.redraw()

        return table

    def _highlight_jump_mark(self, pos, special=False):
        """To highligt the jump mark at the given position."""
        v.highlight("BreezeJumpMark", "\\%{}l\\%{}c".format(*pos))

    def _ask_target_key(self):
        """To ask the user where to jump."""
        key = input.Input()
        while True:
            v.redraw()
            vim.command('echohl Question|echo " target: "|echohl None')
            key.get()
            if key.ESC or key.INTERRUPT:
                return
            elif key.CHAR:
                return key.CHAR

    def _clear_jump_marks(self, table):
        """To clear jump marks."""
        vim.command("try|undojoin|catch|endtry")
        # restore characters
        for mark, tpl in table.items():
            pos, old = tpl
            row, col = pos[0]-1, pos[1]+1
            v.subst_char(v.buf(), old, row, col)

        vim.command("setl nomodified")
        v.redraw()

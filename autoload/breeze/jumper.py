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

    def jump(self, backward=False):
        """To display jump marks and move to the selected jump mark."""
        table = self._show_jump_marks(v.cursor(), backward)
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

    def _show_jump_marks(self, curr_pos, backward=False):
        """To display jump marks."""
        top, bot = v.window_bundaries()
        v.highlight("BreezeShade", "\\%>{0}l\\%<{1}l".format(top-1, bot+1))

        table = {}
        jump_marks = list(string.letters)
        vim.command("setl modifiable noreadonly")
        vim.command("try|undojoin|catch|endtry")

        nodes = filter(lambda n: top <= n.start[0] <= bot, self.plug.parser.all_nodes())
        nodes = reversed(nodes) if backward else nodes

        for node in nodes:

            if not jump_marks:
                break

            # both trow and tcol are 1-indexed
            trow, tcol = node.start[0], node.start[1]
            crow, ccol = curr_pos[0], curr_pos[1]-1

            if backward:
                if not (trow < crow or (trow == crow and tcol < ccol)):
                    continue
            else:
                if not (trow > crow or (trow == crow and tcol > ccol)):
                    continue

            old = v.subst_char(v.buf(), jump_marks[0], trow-1, tcol+1)
            self._highlight_jump_mark((trow, tcol+2))
            table[jump_marks.pop(0)] = (node.start, old)

        vim.command("setl nomodified")
        v.redraw()

        return table

    def _highlight_jump_mark(self, pos, special=False):
        """To highligt the jump mark at the given position."""
        v.highlight("BreezeJumpMark", "\\%{0}l\\%{1}c".format(*pos))

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

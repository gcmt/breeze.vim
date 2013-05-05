# -*- coding: utf-8 -*-
"""
breeze.jumper
~~~~~~~~~~~~~

Jumper class definition.

The Jumper is responsible for the jumping functionality:

    1. display jump marks on the current buffer
    2. ask the user for the destination mark
    3. jump to the selected mark

The only method that should be called from the outside and that provide
the above functionality is the "jump" method.
"""

import vim

import breeze.input
import breeze.utils.misc
import breeze.utils.settings


class Jumper(object):

    def __init__(self, plug):
        # modules reference shortcuts
        self.settings = breeze.utils.settings
        self.misc = breeze.utils.misc

        self.plug = plug

        # jump marks
        self.jump_marks = list("qwertyuiopasdfghjklzxcvbnm"
                               "QWERTYUIOPASDFGHJKLZXCVBNM")

    def show_jump_marks(self, backward=False):
        """Displays jump marks."""
        top, bot = self.misc.window_bundaries()
        self.misc.highlight("BreezeShade",
            "\\%>{0}l\\%<{1}l".format(top-1, bot+1))

        table = {}
        buf = vim.current.buffer
        jump_marks = self.jump_marks[:]

        vim.command("setlocal modifiable")
        vim.command("setlocal noreadonly")
        #vim.command("syntax off")

        top, bot = self.misc.window_bundaries()
        ps = [node.start for node in self.plug.parser.all_nodes()
              if node.start[0] >= top and node.start[0] <= bot]

        vim.command("try|undojoin|catch|endtry")

        curr_pos = self.misc.cursor()
        for pos in ps:

            if jump_marks:
                row, col = pos[0]-1, pos[1]+1

                if backward:
                    if row < curr_pos[0]:
                        mark = jump_marks[0]
                        jump_marks.pop(0)
                    else:
                        mark = None
                else:
                    if row >= curr_pos[0]:
                        mark = jump_marks[0]
                        jump_marks.pop(0)
                    else:
                        mark = None
            else:
                mark = None

            if mark:
                old = self.misc.subst_char(buf, mark, row, col)
                self.highlight_jump_mark((row+1, col+1))
                table[mark] = (pos, old)

        vim.command("setlocal nomodified")
        vim.command("redraw")
        return table

    def highlight_jump_mark(self, pos, special=False):
        """Highligts the jump mark at the given position."""
        self.misc.highlight("BreezeJumpMark", "\\%{0}l\\%{1}c".format(*pos))

    def ask_target_key(self):
        """Ask the user where to jump."""
        input = breeze.input.Input()
        while True:
            vim.command('echohl Question|echo " target: "|echohl None')
            input.get()

            if input.ESC or input.INTERRUPT:
                return
            elif input.CHAR:
                return input.CHAR

            vim.command("redraw")

    def clear_jump_marks(self, table):
        """Clear jump marks."""
        vim.command("try|undojoin|catch|endtry")
        # restore characters
        buf = vim.current.buffer
        for mark, v in table.items():
            pos, old = v
            row, col = pos[0]-1, pos[1]+1
            self.misc.subst_char(buf, old, row, col)

        #vim.command("syntax on")
        vim.command("setlocal nomodified")
        vim.command("redraw")

    def jump(self, backward=False):
        """Displays jump marks, asks for the target key and moves
        to the desired position.

        The whole process can be aborted with <ESC> or Ctrl-C.
        """
        table = self.show_jump_marks(backward)
        choice = None
        while choice not in table:
            choice = self.ask_target_key()
            if choice is None:
                break

        self.misc.clear_hl()
        self.clear_jump_marks(table)

        if choice:
            row, col = table[choice][0]
            if not self.settings.get("jump_to_angle_bracket", bool):
                col += 1
            self.misc.cursor((row, col))


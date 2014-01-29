# -*- coding: utf-8 -*-
"""
breeze.utils.input
~~~~~~~~~~~~~~~~~~

This module defines the Input class that is responsible for handling
the input coming from the user via the command line.
"""

import vim


class Input:

    def __init__(self):
        self._reset()

    def _reset(self):
        """To reset the input state."""
        self.LEFT = self.RIGHT = self.UP = self.DOWN = None
        self.RETURN = self.ESC = self.TAB = self.CTRL = self.BS = None
        self.INTERRUPT = self.MOUSE = self.MAC_CMD = None
        self.CHAR = ""
        self.F1 = self.F2 = self.F3 = self.F4 = self.F5 = self.F6 = None
        self.F7 = self.F8 = self.F9 = self.F10 = self.F11 = self.F12 = None
        vim.command("let g:_breeze_char = ''")
        vim.command("let g:_breeze_interrupt = 0")

    def get(self):
        """To read a key pressed by the user."""
        self._reset()

        vim.command("""
            try |
             let g:_breeze_char = strtrans(getchar()) |
            catch |
             let g:_breeze_interrupt = 1 |
            endtry
        """)

        if vim.eval('g:_breeze_interrupt') == '1':  # Ctrl + c
            self.CTRL = True
            self.CHAR = unicode("c", "utf-8")
            self.INTERRUPT = True
            return

        raw_char = vim.eval('g:_breeze_char')

        # only with mac os
        # 'cmd' key has been pressed
        if raw_char.startswith("<80><fc><80>"):
            self.MAC_CMD = True
            char = raw_char.replace("<80><fc><80>", "")
            nr = vim.eval("char2nr('{0}')".format(char))
        else:
            # we use str2nr in order to get a negative number as a result if
            # the user press a special key such as backspace
            nr = int(vim.eval("str2nr('{0}')".format(raw_char)))

        if nr != 0:

            if nr == 13:
                self.RETURN = True
            elif nr == 27:
                self.ESC = True
            elif nr == 9:  # same as Ctrl+i.. miss something?
                self.TAB = True
            elif 1 <= nr <= 26:
                self.CTRL = True
                self.CHAR = vim.eval("nr2char({0})".format(nr + 96)).decode('utf-8')
            else:
                self.CHAR = vim.eval("nr2char({0})".format(nr)).decode('utf-8')

        else:

            c = raw_char.replace("<80>", "")
            if c == 'kl':
                self.LEFT = True
            elif c == 'kr':
                self.RIGHT = True
            elif c == 'ku':
                self.UP = True
            elif c == 'kd':
                self.DOWN = True
            elif c == 'kb':  # backspace
                self.BS = True
            elif c == 'k1':
                self.F1 = True
            elif c == 'k2':
                self.F2 = True
            elif c == 'k3':
                self.F3 = True
            elif c == 'k4':
                self.F4 = True
            elif c == 'k5':
                self.F5 = True
            elif c == 'k6':
                self.F6 = True
            elif c == 'k7':
                self.F7 = True
            elif c == 'k8':
                self.F8 = True
            elif c == 'k9':
                self.F9 = True
            elif c == 'k10':
                self.F10 = True
            elif c == 'k11':
                self.F11 = True
            elif c == 'k12':
                self.F12 = True
            else:
                # mouse clicks or scrolls
                self.MOUSE = True

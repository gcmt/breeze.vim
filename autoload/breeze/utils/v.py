# -*- coding: utf-8 -*-
"""
breeze.utils.v
~~~~~~~~~~~~~~

This module defines thin wrappers around vim commands and functions.
"""

import vim

from breeze.utils import settings


def echom(msg):
    """To display a message to the user via the command line."""
    vim.command('echom "[breeze] {}"'.format(msg.replace('"', '\"')))


def echohl(msg, hlgroup):
    """To display a colored message to the user via the command line."""
    vim.command("echohl {}".format(hlgroup))
    echom(msg)
    vim.command("echohl None")


def redraw():
    """Little wrapper around the redraw command."""
    vim.command('redraw')


def cursor(target=None):
    """To move the cursor or return the current cursor position."""
    if not target:
        return vim.current.window.cursor
    else:
        vim.current.window.cursor = target


def window_bundaries():
    """To return the top and bottom lines number for the current window."""
    curr_pos = cursor()

    scrolloff = vim.eval("&scrolloff")
    vim.command("setlocal scrolloff=0")

    # :help keepjumps -> Moving around in {command} does not change the '',
    # '. and '^ marks, the jumplist or the changelist.
    vim.command("keepjumps normal! H")
    top = cursor()[0]
    vim.command("keepjumps normal! L")
    bot = cursor()[0]

    # restore position and changed options
    cursor(curr_pos)
    vim.command("setlocal scrolloff={}".format(scrolloff))

    return top, bot


def highlight(group, patt, priority=10):
    """Wrapper of the matchadd() vim function."""
    return vim.eval("matchadd('{}', '{}', {})".format(group, patt, priority))


def clear_hl(*groups):
    """To clear Breeze highlightings."""
    for match in vim.eval("getmatches()"):
        if match['group'] in groups:
            vim.command("call matchdelete({})".format(match['id']))


def subst_char(buffer, v, row, col):
    """To substitute a character in the buffer with the given character at the
    given position. Return the substituted character."""
    if row >= len(buffer):
        raise ValueError("row index out of bound")

    new_line = list(buffer[row])
    if col >= len(new_line):
        raise ValueError("column index out of bound")

    old = buffer[row][col]
    new_line[col] = v
    buffer[row] = "".join(new_line)

    return old

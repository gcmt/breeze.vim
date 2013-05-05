# -*- coding: utf-8 -*-
"""
breeze.utils.misc
~~~~~~~~~~~~~~~~~

This module defines various utility functions and some tiny wrappers
around vim functions.
"""

import vim
import breeze.utils.settings


def echom(msg):
    """Gives a simple feedback to the user via the command line."""
    vim.command('echom "[breeze] {0}"'.format(msg.replace('"', '\"')))


def echov(msg):
    """Gives a feedback only if g:breeze_verbosity = 1."""
    if breeze.utils.settings.get("verbosity", bool):
        echom(msg)


def cursor(target=None):
    """Moves the cursor or returs the current cursor position."""
    if not target:
        return vim.current.window.cursor
    else:
        vim.current.window.cursor = target


def window_bundaries():
    """Returns the top and bottom lines number for the current window."""
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
    vim.command("setlocal scrolloff={0}".format(scrolloff))

    return top, bot


def highlight(group, patt, priority=10):
    """Wraps the matchadd() vim function."""
    return vim.eval("matchadd('{0}', '{1}', {2})".format(
                    group, patt, priority))


def clear_hl_by_ids(ids):
    """Clears Breeze highlightings with id in 'ids'."""
    for id in ids:
        vim.command("call matchdelete({0})".format(id))


def clear_hl():
    """Clears Breeze highlightings.

    For performance reasons the group BreezeHl handled separately
    with the clear_hl_by_ids function.
    """
    for match in vim.eval("getmatches()"):
        if match['group'] in ('BreezeJumpMark', 'BreezeShade'):
            vim.command("call matchdelete({0})".format(match['id']))


def subst_char(buffer, v, row, col):
    """Substitutes a character in the buffer with the given character at the
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





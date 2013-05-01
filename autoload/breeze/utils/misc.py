# -*- coding: utf-8 -*-
"""
breeze.utils.misc
~~~~~~~~~~~~~~~~~

This module defines various utility functions and some tiny wrappers
around vim functions.
"""

import vim


def echom(msg):
    """Gives a simple feedback to the user via the command line."""
    vim.command('echom "[breeze] {0}"'.format(msg.replace('"', '\"')))


def cursor(target=None, kj=False):
    """Moves the cursor.

    If the kj parameter is set to True, then the command behaves as following:
    :help keepjumps -> Moving around in {command} does not change the '', '.
                       and '^ marks, the jumplist or the changelist...
    """
    if not target:
        return vim.current.window.cursor
    vim.command("{0}call cursor({1}, {2})".format(
        "keepjumps " if kj else "", target[0], target[1]))


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
    vim.eval("matchadd('{0}', '{1}', {2})".format(
        group, patt, priority))


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


def clear_highlighting():
    """Clears Breeze highlightings."""
    matches = vim.eval("getmatches()")
    g = ('BreezeJumpMark', 'BreezeShade', 'BreezeTag', 'BreezeTagBlock')
    for match in matches:
        if match['group'] in g:
            vim.command("call matchdelete({0})".format(match['id']))


def attrs_len(node):
    """Returns the length of rendered attributes."""
    return sum(len(a) + len(v) for a, v in node.attrs) + 3 * len(node.attrs)

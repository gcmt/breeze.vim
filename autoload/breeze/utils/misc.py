# -*- coding: utf-8 -*-
"""
breeze.utils.misc
~~~~~~~~~~~~~~~~~

This module defines various utility functions and some tiny wrappers
around vim functions.
"""

import vim


def echom(msg):
    """Display a simple feedback to the user via the command line."""
    vim.command('echom "[breeze] {0}"'.format(msg.replace('"', '\"')))

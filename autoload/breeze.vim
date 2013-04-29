" ============================================================================
" File: autoload/breeze.vim
" Description: Fast XHTML navigation
" Mantainer: Giacomo Comitti (https://github.com/gcmt)
" Url: https://github.com/gcmt/breeze.vim
" License: MIT
" Version: 1.0
" Last Changed: 29/04/2013
" ============================================================================

" init

fu! breeze#init()
    let py_module = fnameescape(globpath(&runtimepath, 'autoload/breeze.py'))
    exe 'pyfile ' . py_module
    python breeze_plugin = Breeze()
endfu

call breeze#init()


" wrappers

fu! breeze#PrintDom()
    py breeze_plugin.print_dom()
endfu

fu! breeze#MatchTag()
    py breeze_plugin.match_tag()
endfu

fu! breeze#NextSibling()
    py breeze_plugin.goto_next_sibling()
endfu

fu! breeze#PrevSibling()
    py breeze_plugin.goto_prev_sibling()
endfu

fu! breeze#FirstChild()
    py breeze_plugin.goto_first_child()
endfu

fu! breeze#LastChild()
    py breeze_plugin.goto_last_child()
endfu

fu! breeze#Parent()
    py breeze_plugin.goto_parent()
endfu

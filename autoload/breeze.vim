" ============================================================================
" File: autoload/breeze.vim
" Description: DOM navigation
" Mantainer: Giacomo Comitti (https://github.com/gcmt)
" Url: https://github.com/gcmt/breeze.vim
" License: MIT
" Version: 1.0.1
" Last Changed: 6/24/2013
" ============================================================================

" Init {{{

fu! breeze#init()
    let py_module = fnameescape(globpath(&runtimepath, 'autoload/breeze.py'))
    exe 'pyfile ' . py_module
    python breeze_plugin = Breeze()
endfu

call breeze#init()
let g:breeze_initialized = 1

" }}}

" Wrappers {{{

" tag jumping {{{

fu! breeze#JumpForward()
    py breeze_plugin.jump_forward()
endfu

fu! breeze#JumpBackward()
    py breeze_plugin.jump_backward()
endfu

" }}}

" tag matching / highlighting {{{

fu! breeze#MatchTag()
    py breeze_plugin.match_tag()
endfu

fu! breeze#HighlightElement()
    py breeze_plugin.highlight_curr_element()
endfu

fu! breeze#HighlightElementBlock()
    py breeze_plugin.highlight_element_block()
endfu

" }}}

" dom navigation {{{

fu! breeze#NextSibling()
    py breeze_plugin.goto_next_sibling()
endfu

fu! breeze#PrevSibling()
    py breeze_plugin.goto_prev_sibling()
endfu

fu! breeze#FirstSibling()
    py breeze_plugin.goto_first_sibling()
endfu

fu! breeze#LastSibling()
    py breeze_plugin.goto_last_sibling()
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

" }}}

" misc {{{

fu! breeze#PrintDom()
    py breeze_plugin.print_dom()
endfu

fu! breeze#WhatsWrong()
    py breeze_plugin.whats_wrong()
endfu

" }}}

" }}}

" Autocommands {{{

augroup breeze_plugin

    au!
    exe 'au Colorscheme '.g:breeze_highlight_filename_patterns.' py breeze_plugin.setup_colors()'
    exe 'au CursorMoved,CursorMovedI,BufLeave,BufWinLeave,WinLeave *.* py breeze_plugin.clear_element_hl()'

    " FIX: at this events the plugin should rebuild the cache,
    " not just tell that the cache need to be updated
    exe 'au BufReadPost,BufWritePost,BufEnter '.g:breeze_highlight_filename_patterns.' py breeze_plugin.refresh_cache=True'
    exe 'au CursorHold,CursorHoldI '.g:breeze_highlight_filename_patterns.' py breeze_plugin.refresh_cache=True'
    exe 'au InsertEnter,InsertLeave '.g:breeze_highlight_filename_patterns.' py breeze_plugin.refresh_cache=True'
    exe 'au BufWritePost '.g:breeze_highlight_filename_patterns.' py breeze_plugin.refresh_cache=True'

    if g:breeze_hl_element
        exe 'au CursorMoved '.g:breeze_highlight_filename_patterns.' py breeze_plugin.highlight_curr_element()'
        au InsertEnter *.* py breeze_plugin.clear_element_hl()
    endif

augroup END

" }}}

" ============================================================================
" File: autoload/breeze.vim
" Description: DOM navigation
" Mantainer: Giacomo Comitti (https://github.com/gcmt)
" Url: https://github.com/gcmt/breeze.vim
" License: MIT
" Version: 1.0
" Last Changed: 5/1/2013
" ============================================================================

" Init  {{{

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
    au Colorscheme *.html,*.htm,*.xhtml,*.xml py breeze_plugin.setup_colors()
    au BufEnter,BufLeave,CursorMoved *.html,*.htm,*.xhtml,*.xml py breeze.utils.misc.clear_highlighting()

    " update the cache
    au BufReadPost,BufWritePost,BufEnter *.html,*.htm,*.xhtml,*.xml py breeze_plugin.refresh_cache=True
    au CursorHold,CursorHoldI *.html,*.htm,*.xhtml,*.xml py breeze_plugin.refresh_cache=True
    au InsertEnter,InsertLeave *.html,*.htm,*.xhtml,*.xml py breeze_plugin.refresh_cache=True
    au BufWritePost *.html,*.htm,*.xhtml,*.xml py breeze_plugin.refresh_cache=True

    if g:breeze_hl_element
        " the user want current element always highlighted. The CursorMoved'
        " event is somewhat costly but here the cache comes into play
        au CursorMoved *.html,*.htm,*.xhtml,*.xml py breeze_plugin.highlight_curr_element()
    endif

augroup END

" }}}

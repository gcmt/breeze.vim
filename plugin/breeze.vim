" ============================================================================
" File: plugin/breeze.vim
" Description: DOM navigation
" Mantainer: Giacomo Comitti (https://github.com/gcmt)
" Url: https://github.com/gcmt/breeze.vim
" License: MIT
" Version: 1.0
" Last Changed: 5/1/2013
" ============================================================================

" Init {{{

if exists("g:breeze_loaded") || &cp || exists("g:breeze_disable") ||
    \ !has('python')
    finish
endif
let g:breeze_loaded = 1

" }}}

" Settings {{{

let g:breeze_hl_element =
    \ get(g:, 'breeze_hl_element', 1)


let g:breeze_tag_color =
    \ get(g:, 'breeze_tag_color', 'MatchParen')
let g:breeze_tag_color_darkbg =
    \ get(g:, 'breeze_tag_color_darkbg', 'MatchParen')

let g:breeze_tagblock_color =
    \ get(g:, 'breeze_tagblock_color', 'MatchParen')
let g:breeze_tagblock_color_darkbg =
    \ get(g:, 'breeze_tagblock_color_darkbg', 'MatchParen')


let g:breeze_shade_color =
    \ get(g:, 'breeze_shade_color', 'gui=NONE guifg=#777777 cterm=NONE ctermfg=242')
let g:breeze_shade_color_darkbg =
    \ get(g:, 'breeze_shade_color_darkbg', 'gui=NONE guifg=#777777 cterm=NONE ctermfg=242')

let g:breeze_jumpmark_color =
    \get(g:, 'breeze_jumpmark_color', 'gui=bold guifg=#ff6155 cterm=bold ctermfg=203')
let g:breeze_jumpmark_color_darkbg =
    \ get(g:, 'breeze_jumpmark_color_darkbg', 'gui=bold guifg=#ff6155 cterm=bold ctermfg=203')

" }}}

" Commands {{{

" tag jumping
command! BreezeJumpF call breeze#JumpForward()
command! BreezeJumpB call breeze#JumpBackward()

" tag matching / highlighting
command! BreezeMatchTag call breeze#MatchTag()
command! BreezeHlElement call breeze#HighlightElement()
command! BreezeHlElementBlock call breeze#HighlightElementBlock()

" dom navigation
command! BreezeNextSibling call breeze#NextSibling()
command! BreezePrevSibling call breeze#PrevSibling()
command! BreezeFirstChild call breeze#FirstChild()
command! BreezeLastChild call breeze#LastChild()
command! BreezeParent call breeze#Parent()

" misc
command! BreezePrintDom call breeze#PrintDom()

" }}}

" autocommands {{{

augroup breeze_init
    au!
    au BufWinEnter *.html,*.htm,*.xhtml,*.xml
        \ if !exists("g:breeze_initialized") | call breeze#init() | endif
augroup END

" }}}

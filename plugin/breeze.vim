" ============================================================================
" File: plugin/breeze.vim
" Description: DOM navigation
" Mantainer: Giacomo Comitti (https://github.com/gcmt)
" Url: https://github.com/gcmt/breeze.vim
" License: MIT
" Version: 1.0.1
" Last Changed: 6/24/2013
" ============================================================================

" Init {{{

if exists("g:breeze_loaded") || &cp || exists("g:breeze_disable") || !has('python')
    finish
endif
let g:breeze_loaded = 1

" }}}

" Settings {{{

let g:breeze_hl_element =
    \ get(g:, 'breeze_hl_element', 1)

let g:breeze_jump_to_angle_bracket =
    \ get(g:, 'breeze_jump_to_angle_bracket', 0)


let g:breeze_hl_color =
    \ get(g:, 'breeze_hl_color', 'MatchParen')
let g:breeze_hl_color_darkbg =
    \ get(g:, 'breeze_hl_color_darkbg', '')


let g:breeze_shade_color =
    \ get(g:, 'breeze_shade_color', 'gui=NONE guifg=#777777 cterm=NONE ctermfg=242')
let g:breeze_shade_color_darkbg =
    \ get(g:, 'breeze_shade_color_darkbg', '')

let g:breeze_jumpmark_color =
    \get(g:, 'breeze_jumpmark_color', 'gui=bold guifg=#ff6155 cterm=bold ctermfg=203')
let g:breeze_jumpmark_color_darkbg =
    \ get(g:, 'breeze_jumpmark_color_darkbg', '')

let g:breeze_verbosity = get(g:, "breeze_verbosity", 0)

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
command! BreezeFirstSibling call breeze#FirstSibling()
command! BreezeLastSibling call breeze#LastSibling()
command! BreezeFirstChild call breeze#FirstChild()
command! BreezeLastChild call breeze#LastChild()
command! BreezeParent call breeze#Parent()

" misc
command! BreezePrintDom call breeze#PrintDom()
command! BreezeWhatsWrong call breeze#WhatsWrong()

" }}}

" autocommands {{{

if exists("g:breeze_highlight_filename_patterns")
    let g:breeze_highlight_filename_patterns = "*.html,*.htm,*.xhtml,*.xml,".g:breeze_highlight_filename_patterns
else
    let g:breeze_highlight_filename_patterns = "*.html,*.htm,*.xhtml,*.xml"
endif

augroup breeze_init
    au!
    exe 'au BufWinEnter '.g:breeze_highlight_filename_patterns.' if !exists("g:breeze_initialized") | call breeze#init() | endif'
augroup END

" }}}

" ============================================================================
" File: plugin/breeze.vim
" Description: HTML utils
" Mantainer: Giacomo Comitti - https://github.com/gcmt
" Url: https://github.com/gcmt/breeze.vim
" License: MIT
" Last Changed: 8 Sep 2013
" ============================================================================


" Init
" ----------------------------------------------------------------------------

if exists("g:breeze_loaded") || &cp || !has('python') || exists("g:breeze_disable")
    finish
endif
let g:breeze_loaded = 1


" Settings
" ----------------------------------------------------------------------------

" basic

let g:breeze_active_filetypes =
    \ "*.html,*.htm,*.xhtml,*.xml," . get(g:, 'breeze_active_filetypes', '')
    " deprecated
    \ . get(g:, 'breeze_highlight_filename_patterns', '')

let g:breeze_highlight_curr_element =
    \ get(g:, 'breeze_highlight_curr_element', 1)
" deprecated
let g:breeze_highlight_curr_element =
    \ get(g:, 'breeze_hl_element', g:breeze_highlight_curr_element)

let g:breeze_jump_to_angle_bracket =
    \ get(g:, 'breeze_jump_to_angle_bracket', 0)

" appearance

let g:breeze_hl_color =
    \ get(g:, 'breeze_hl_color', 'MatchParen')

let g:breeze_hl_color_darkbg =
    \ get(g:, 'breeze_hl_color_darkbg', g:breeze_hl_color)

let g:breeze_shade_color =
    \ get(g:, 'breeze_shade_color', 'Comment')

let g:breeze_shade_color_darkbg =
    \ get(g:, 'breeze_shade_color_darkbg', g:breeze_shade_color)

let g:breeze_jumpmark_color =
    \ get(g:, 'breeze_jumpmark_color', 'WarningMsg')

let g:breeze_jumpmark_color_darkbg =
    \ get(g:, 'breeze_jumpmark_color_darkbg', g:breeze_jumpmark_color)


" Commands
" ----------------------------------------------------------------------------

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


" Autocommands
" ----------------------------------------------------------------------------

augroup breeze_init
    au!
    exe 'au BufWinEnter '.g:breeze_active_filetypes.' if !exists("g:breeze_initialized") | call breeze#init() | endif'
augroup END

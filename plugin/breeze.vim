" ============================================================================
" File: plugin/breeze.vim
" Description: HTML motions
" Mantainer: Giacomo Comitti - https://github.com/gcmt
" Url: https://github.com/gcmt/breeze.vim
" License: MIT
" ============================================================================

" Init
" =============================================================================

if exists("g:loaded_breeze")
    finish
endif
let g:loaded_breeze = 1

let s:save_cpo = &cpo
set cpo&vim

" Colors
" =============================================================================

fu! s:setup_colors()
    hi default link BreezeJumpMark WarningMsg
    hi default link BreezeShade Comment
    hi default link BreezePrompt String
endfu

cal s:setup_colors()

" Settings
" =============================================================================

let g:breeze_prompt =
    \ get(g:, "breeze_prompt", " Target: ")

let g:breeze_marks =
    \ get(g:, "breeze_marks", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

" Mappings
" =============================================================================

nnoremap <silent> <Plug>(breeze-jump-tag-forward) :cal breeze#JumpTag(0)<CR>
nnoremap <silent> <Plug>(breeze-jump-tag-backward) :cal breeze#JumpTag(1)<CR>

nnoremap <silent> <Plug>(breeze-jump-attribute-forward) :cal breeze#JumpAttribute(0)<CR>
nnoremap <silent> <Plug>(breeze-jump-attribute-backward) :cal breeze#JumpAttribute(1)<CR>

" Autocommands
" =============================================================================

augroup breeze
    au!
    au BufWritePost .vimrc cal s:setup_colors()
    au Colorscheme * cal s:setup_colors()
augroup END

" =============================================================================

let &cpo = s:save_cpo
unlet s:save_cpo

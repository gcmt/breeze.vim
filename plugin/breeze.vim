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

let g:breeze_version = "v3.0"

let s:save_cpo = &cpo
set cpo&vim

" Colors
" =============================================================================

fu! s:setup_colors()
    hi default link BreezeJumpMark WarningMsg
    hi default link BreezeShade Comment
    hi default link BreezePrompt String
    hi default link BreezeHighlightedLine CursorLine
endfu

cal s:setup_colors()

" Settings
" =============================================================================

let g:breeze_prompt =
    \ get(g:, "breeze_prompt", " Target: ")

let g:breeze_marks =
    \ get(g:, "breeze_marks", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

" Highlight the current line
" =============================================================================

" To highlight the current line
fu s:highlight_line()
    let s:hl = matchadd("BreezeHighlightedLine", '\%'.line(".")."l")
    redraw
endfu

fu s:clear_highlighting()
    sil! call matchdelete(s:hl)
    unlet! s:hl
endfu

" Mappings
" =============================================================================

nnoremap <silent> <Plug>(breeze-next-tag) :cal breeze#Jump("tag", 0)<CR>
nnoremap <silent> <Plug>(breeze-prev-tag) :cal breeze#Jump("tag", 1)<CR>
nnoremap <silent> <Plug>(breeze-next-tag-hl) :cal breeze#Jump("tag", 0)<CR>:cal <SID>highlight_line()<CR>
nnoremap <silent> <Plug>(breeze-prev-tag-hl) :cal breeze#Jump("tag", 1)<CR>:cal <SID>highlight_line()<CR>

nnoremap <silent> <Plug>(breeze-next-attribute) :cal breeze#Jump("attribute", 0)<CR>
nnoremap <silent> <Plug>(breeze-prev-attribute) :cal breeze#Jump("attribute", 1)<CR>
nnoremap <silent> <Plug>(breeze-next-attribute-hl) :cal breeze#Jump("attribute", 0)<CR>:cal <SID>highlight_line()<CR>
nnoremap <silent> <Plug>(breeze-prev-attribute-hl) :cal breeze#Jump("attribute", 1)<CR>:cal <SID>highlight_line()<CR>

nnoremap <silent> <Plug>(breeze-jump-tag-forward) :cal breeze#JumpAsk("tag", 0)<CR>
nnoremap <silent> <Plug>(breeze-jump-tag-backward) :cal breeze#JumpAsk("tag", 1)<CR>

nnoremap <silent> <Plug>(breeze-jump-attribute-forward) :cal breeze#JumpAsk("attribute", 0)<CR>
nnoremap <silent> <Plug>(breeze-jump-attribute-backward) :cal breeze#JumpAsk("attribute", 1)<CR>

" Autocommands
" =============================================================================

augroup breeze
    au!
    au BufWritePost .vimrc cal s:setup_colors()
    au Colorscheme * cal s:setup_colors()
    au CursorMoved,CursorMovedI,WinLeave * cal s:clear_highlighting()
augroup END

" =============================================================================

let &cpo = s:save_cpo
unlet s:save_cpo

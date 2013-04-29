" ============================================================================
" File: plugin/breeze.vim
" Description: Fast XHTML navigation
" Mantainer: Giacomo Comitti (https://github.com/gcmt)
" Url: https://github.com/gcmt/breeze.vim
" License: MIT
" Version: 1.0
" Last Changed: 29/04/2013
" ============================================================================

" TODO:
"
"   - option to let the NextSibling command continues with the parent siblings
"     (the same thing for the PrevSibling)
"   - commands LastSibling e FirstSibling
"   - command to iterate the children without using FistChild and NexSibling
"   - command to iterate parent's siblings
"   - ability to specify the number of motions
"   - html outlining in a side window (like tagbar or nerdtree)
"   - highlight the current tag
"

" Init

if  v:version < 703 || !has('python') || exists("g:breeze_loaded") || &cp
    finish
endif
let g:breeze_loaded = 1


" Commands

command! BreezePrintDom call breeze#PrintDom()
command! BreezeMatchTag call breeze#MatchTag()
command! BreezeNextSibling call breeze#NextSibling()
command! BreezePrevSibling call breeze#PrevSibling()
command! BreezeFirstChild call breeze#FirstChild()
command! BreezeLastChild call breeze#LastChild()
command! BreezeParent call breeze#Parent()


" Mappngs

if get(g:, 'breeze_default_mappings', 1)

endif



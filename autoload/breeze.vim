" ============================================================================
" File: autoload/breeze.vim
" Description: HTML motions
" Mantainer: Giacomo Comitti - https://github.com/gcmt
" Url: https://github.com/gcmt/breeze.vim
" License: MIT
" ============================================================================

let s:save_cpo = &cpo
set cpo&vim

" Internal variables
" ============================================================================

let s:attr_pattern = "\\v(\\<!--\\_.{-}(--\\>)@!)@<!((\\<[^>]{-})@<=(\\=)@<=(\"|'))"
let s:tag_pattern = "\\v(\\<!--\\_.{-}(--\\>)@!)@<!\\<[^/!](\"[^\"]*\"|'[^']*'|[^\"'>])*\\>"

" Core functions
" ============================================================================

fu breeze#MoveToTag(backward)
    normal! m'
    if search(s:tag_pattern, a:backward ? "b" : "W")
        norm! l
    endif
endfu

fu breeze#MoveToAttribute(backward)
    normal! m'
    if search(s:attr_pattern, a:backward ? "b" : "W")
        norm! l
    endif
endfu

fu breeze#JumpTag(backward)
    let marks = s:show_marks(a:backward, s:tag_pattern)
    cal s:jump(marks)
    cal s:clear_marks(marks)
endfu

fu breeze#JumpAttribute(backward)
    let marks = s:show_marks(a:backward, s:attr_pattern)
    cal s:jump(marks)
    cal s:clear_marks(marks)
endfu

" To display marks for HTML attributes or tags
fu s:show_marks(backward, pattern)
    let stopline = a:backward ? line('w0') : line('w$')
    let marks = s:get_marks(a:pattern, a:backward ? "b" : "W", stopline)
    let marks = s:display_marks(marks)
    return marks
endfu

" To search for all marks
fu s:get_marks(patt, flags, stopline)
    let view = winsaveview()
    let marks = split(g:breeze_marks, "\\zs")
    let candidates = {}
    while 1
        let [line, col] = searchpos(a:patt, a:flags, a:stopline)
        if line == 0 && col == 0 || empty(marks)
            break
        end
        let candidates[remove(marks, 0)] = [line, col]
    endw
    cal winrestview(view)
    return candidates
endfu

" To display all marks
fu s:display_marks(marks)
    cal matchadd("BreezeShade", '\%>'.(line('w0')-1).'l\%<'.line('w$').'l')
    try | undojoin | catch | endtry
    let marks = {}
    for mark in keys(a:marks)
        let [linenr, colnr] = a:marks[mark]
        let line = getline(linenr)
        let marks[mark] = [linenr, colnr, line[colnr]]
        cal setline(linenr, s:str_subst(line, colnr, mark))
        cal matchadd("BreezeJumpMark", '\%'.linenr.'l\%'.(colnr+1).'c')
    endfor
    setl nomodified
    return marks
endfu

" To ask the user where to jump and move there
fu s:jump(marks)
    if empty(a:marks) | return | end
    normal! m'
    while 1
        redraw
        cal s:show_prompt()
        let choice = s:get_char()
        if choice =~ '<C-C>\|<ESC>'
            break
        end
        if has_key(a:marks, choice)
            let [line, col, oldchar] = get(a:marks, choice)
            cal setpos(".", [0, line, col+1, 0])
            break
        end
    endw
endfu

" To display the prompt
fu s:show_prompt()
    echohl BreezePrompt | echon g:breeze_prompt | echohl None
endfu

" To clear all marks
fu s:clear_marks(marks)
    cal s:clear_matches('BreezeJumpMark', 'BreezeShade')
    try | undojoin | catch | endtry
    for [linenr, colnr, oldchar] in values(a:marks)
        cal setline(linenr, s:str_subst(getline(linenr), colnr, oldchar))
    endfor
    setl nomodified
endfu

" Utilities
" =============================================================================

" To clear matches for all given groups
fu s:clear_matches(...)
    for m in getmatches()
        if index(a:000, m.group) != -1
            cal matchdelete(m.id)
        end
    endfor
endfu

" To substitute a character in a string
fu s:str_subst(str, col, char)
    return strpart(a:str, 0, a:col) . a:char . strpart(a:str, a:col+1)
endfu

" To get a key pressed by the user
fu s:get_char()
    let char = strtrans(getchar())
        if char == 13 | return "<CR>"
    elseif char == 27 | return "<ESC>"
    elseif char == 9 | return "<TAB>"
    elseif char >= 1 && char <= 26 | return "<C-" . nr2char(char+64) . ">"
    elseif char != 0 | return nr2char(char)
    elseif match(char, '<fc>^D') > 0 | return "<C-SPACE>"
    elseif match(char, 'kb') > 0 | return "<BS>"
    elseif match(char, 'ku') > 0 | return "<UP>"
    elseif match(char, 'kd') > 0 | return "<DOWN>"
    elseif match(char, 'kl') > 0 | return "<LEFT>"
    elseif match(char, 'kr') > 0 | return "<RIGHT>"
    elseif match(char, 'k\\d\\+') > 0 | return "<F" . match(char, '\\d\\+', 4)] . ">"
    end
endfu

" =============================================================================

let &cpo = s:save_cpo
unlet s:save_cpo

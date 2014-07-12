" ============================================================================
" File: autoload/breeze.vim
" Description: HTML motions
" Mantainer: Giacomo Comitti - https://github.com/gcmt
" Url: https://github.com/gcmt/breeze.vim
" License: MIT
" ============================================================================

fu breeze#JumpTag(backward)
    let marks = breeze#show_marks_for_tags(a:backward)
    cal breeze#jump(marks)
    cal breeze#clear_marks(marks)
endfu

fu breeze#JumpAttribute(backward)
    let marks = breeze#show_marks_for_attributes(a:backward)
    cal breeze#jump(marks)
    cal breeze#clear_marks(marks)
endfu

" To ask the user where to jump and move there
fu breeze#jump(marks)
    if empty(a:marks) | return | end
    normal! m'
    while 1
        redraw
        cal breeze#show_prompt()
        let choice = breeze#get_input()
        if choice =~ "<C-C>\\|<ESC>" | break | end
        if has_key(a:marks, choice)
            let [line, col, oldchar] = get(a:marks, choice)
            cal setpos(".", [0, line, col+1, 0])
            break
        end
    endw
endfu

" To display the prompt
fu breeze#show_prompt()
    echohl BreezePrompt | echon g:breeze_prompt | echohl None
endfu

" To display marks for HTML attributes
fu breeze#show_marks_for_attributes(backward)
    let stopline = a:backward ? line('w0') : line('w$')
    let patt = "\\v(\\<!--\\_.{-}(--\\>)@!)@<!((\\<[^>]{-})@<=(\\=)@<=(\"|'))"
    let marks = breeze#get_marks(patt, a:backward ? "b" : "W", stopline)
    let marks = breeze#display_marks(marks)
    return marks
endfu

" To display marks for HTML opening tags
fu breeze#show_marks_for_tags(backward)
    let stopline = a:backward ? line('w0') : line('w$')
    let patt = "\\v(\\<!--\\_.{-}(--\\>)@!)@<!\\<[^/!](\"[^\"]*\"|'[^']*'|[^\"'>])*\\>"
    let marks = breeze#get_marks(patt, a:backward ? "b" : "W", stopline)
    let marks = breeze#display_marks(marks)
    return marks
endfu

" To search for all marks
fu breeze#get_marks(patt, flags, stopline)
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
fu breeze#display_marks(marks)
    cal matchadd("BreezeShade", '\%>'.(line('w0')-1).'l\%<'.line('w$').'l')
    try | undojoin | catch | endtry
    let marks = {}
    for mark in keys(a:marks)
        let [linenr, colnr] = a:marks[mark]
        let line = getline(linenr)
        let marks[mark] = [linenr, colnr, line[colnr]]
        cal setline(linenr, breeze#subst_char(line, colnr, mark))
        cal matchadd("BreezeJumpMark", '\%'.linenr.'l\%'.(colnr+1).'c')
    endfor
    setl nomodified
    return marks
endfu

" To clear all marks
fu breeze#clear_marks(marks)
    cal breeze#clear_highlighting()
    try | undojoin | catch | endtry
    for [linenr, colnr, oldchar] in values(a:marks)
        cal setline(linenr, breeze#subst_char(getline(linenr), colnr, oldchar))
    endfor
    setl nomodified
endfu

" To clear Breeze highlightings
fu breeze#clear_highlighting()
    for m in getmatches()
        if m.group =~ 'BreezeJumpMark\|BreezeShade'
            cal matchdelete(m.id)
        end
    endfor
endfu

" Utilities
" =============================================================================

" To substitute a character in a string
fu breeze#subst_char(str, col, char)
    let lst = split(a:str, "\\zs")
    let lst[a:col] = a:char
    return join(lst, '')
endfu

" To get a key pressed by the user
fu breeze#get_input()
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

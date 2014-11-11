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

let s:regex_for = {
\ "attribute": "\\v(\\<!--\\_.{-}(--\\>)@!)@<!((\\<[^>]{-})@<=(\\=)@<=(\"[^\"]*\"|'[^']*'))",
\ "tag": "\\v(\\<!--\\_.{-}(--\\>)@!)@<!\\<[^/!](\"[^\"]*\"|'[^']*'|[^\"'>])*\\>",
\ }

" Core functions
" ============================================================================

fu breeze#Jump(target, backward)
	let repeat = !a:backward ? 0 : s:inside(a:target)
    if search(s:regex_for[a:target], a:backward ? "sbW" : "sW")
		if repeat
			cal search(s:regex_for[a:target], a:backward ? "sbW" : "sW")
		end
		norm! l
    endif
endfu

fu breeze#JumpAsk(target, backward)
    let stopline = a:backward ? line('w0') : line('w$')
    let marks = s:get_marks(s:regex_for[a:target], a:backward ? "b" : "W", stopline)
    let changed_chars = s:display_marks(marks)
    cal s:jump(marks)
    cal s:clear_marks(changed_chars)
endfu

" To check if the cursor is inside a tag or attribute
fu! s:inside(target)
	let pattern = s:regex_for[a:target]
	let [lnum, col] = searchpos(s:regex_for[a:target], "nb")
    if lnum != 0 && col != 0 && lnum == line(".")
		let start_match = col
		let end_match = start_match + strlen(matchstr(getline("."), pattern, col-1, 1))
		if col(".") >= start_match && col(".") <= end_match
			return 1
		end
	end
	return 0
endfu

" To search for all candidate marks
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
    let changed_chars = []
    for mark in keys(a:marks)
        let [linenr, colnr] = a:marks[mark]
        let changed_chars = add(changed_chars, [getline(linenr)[colnr], linenr, colnr])
        cal setline(linenr, s:str_subst(getline(linenr), colnr, mark))
        cal matchadd("BreezeJumpMark", '\%'.linenr.'l\%'.(colnr+1).'c')
    endfor
    setl nomodified
    return changed_chars
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
            cal setpos(".", [0] + get(a:marks, choice) + [0])
            norm! l
            break
        end
    endw
endfu

" To display the prompt
fu s:show_prompt()
    echohl BreezePrompt | echon g:breeze_prompt | echohl None
endfu

" To clear all marks
fu s:clear_marks(changed_chars)
    cal s:clear_matches('BreezeJumpMark', 'BreezeShade')
    try | undojoin | catch | endtry
    for [oldchar, linenr, colnr] in a:changed_chars
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

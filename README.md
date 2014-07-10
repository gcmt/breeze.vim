## breeze.vim

Breeze is little plugin that provides a handful of EasyMotion-like HTML motions.

![Preview](_assets/preview.gif "Preview.")

> **Breeze has changed!**
Since version 2.0 Breeze has undergone significant changes. While some features like tag matching and dom navigation have been removed, the jumping functionality have been strengthened. If you liked real time tag matching I suggest you to try [MatchTagAlways](https://github.com/Valloric/MatchTagAlways), it seems to work much better.

### Installation
Install either with [Vundle](https://github.com/gmarik/vundle), [Pathogen](https://github.com/tpope/vim-pathogen) or [Neobundle](https://github.com/Shougo/neobundle.vim).

### Usage

Breeze does not define any mappings for you, you have to map Breeze motions by yourself. Below an example of how you can set you own mappings:
```vim
" jump to all visible opening tags after the cursor position
map <leader>j <Plug>(breeze-jump-tag-forward)
" jump to all visible opening tags before the cursor position
map <leader>J <Plug>(breeze-jump-tag-backward)

" jump to all visible HTML attributes after the cursor position
map <leader>a <Plug>(breeze-jump-attribute-forward)
" jump to all visible HTML attributes before the cursor position
map <leader>A <Plug>(breeze-jump-attribute-backward)
```
After triggering one of the mappings above, Breeze will ask you for where you want to jump to. To abort the whole process press either `<ESC>` or `CTRL+C`.

This is all you have to know to start jumping around your HTML files. Just remember that once you have jumped somewhere you can easily move back to the previous position with `CTRL+O` (`:h CTRL+O`).

### Settings

**g:breeze\_prompt**

With this option  you can set your own custom prompt.

Default: `" Target: "`

**g:breeze\_marks**

With this option you can set the marks used by Breeze to point out all the locations you can jump to.

Default: `"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"`



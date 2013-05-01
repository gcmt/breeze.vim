# breeze.vim

**v1.0**

HTML navigation inspired by vim-easymotion.

Features:
* HTML navigation like vim-easymotion
* Tag matching
* Low level commands for DOM navigation

### Requirements
* Vim compiled with python 2.6+


### Installation
You can either extract the content of the folder into the `$HOME/.vim`
directory or use plugin managers such as Vundle or Pathogen. 


## Tag jumping
![Screenshot](/extra/jump.gif "Tag jumping inspired by vim-easymotion")   

As you can see this form is heavily inspired by vim-easimotion.
To jump to following tags use the command `BreezeJumpForward`. 
Use `BreezeJumpBackward` to move to preceding tags.

When you fire one of the aforementioned commands, Breeze display
colored marks on the tags you can jump to and wait for your choice.
Once you have moved to a tag you can easily jump back using the `CTRL+O` 
vim mapping (:help CTRL+O).

### commands

**BreezeJumpForward**

**BreezeJumpBackward**


### settings

**g:breeze_shade_color**  
default: `gui=NONE guifg=#777777 cterm=NONE ctermfg=242`

**g:breeze_shade_color_darkbg**  
default: `gui=NONE guifg=#777777 cterm=NONE ctermfg=242`

**g:breeze_jumpmark_color**  
default: `gui=bold guifg=#ff6155 cterm=bold ctermfg=203`

**g:breeze_jumpmark_color_darkbg**  
default: `gui=bold guifg=#ff6155 cterm=bold ctermfg=203`



## Tag matching
![Screenshot](/extra/high.gif "Tag matching")   

### commands

**BreezeCurrentTag**   
If the cursor is on the opening tag, this command moves the cursor to the closing
tag, and vice-versa. If the command is called in other locations this command moves
the cursor to the opening tag of the node that presumably enclose our position.

**BreezeHighlightTag**

**BreezeHighlightTagBlock**


### settings

**g:breeze_highlight_tag**
default: `1`

**g:breeze_tag_color**
default: `MatchParen`

**g:breeze_tag_color_darkbg**
default: `MatchParen`

**g:breeze_tagblock_color**
default: `MatchParen`

**g:breeze_tagblock_color_darkbg**
default: `MatchParen`


## DOM navigation
![Screenshot](/extra/dom.gif "DOM navigation")   

## commands

**BreezeHighlightTagBlock**

**BreezeNextSibling**
Moves the cursor to the next sibling node.**

**BreezePrevSibling**
Moves the cursor to the previous sibling node.**

**BreezeFirstChild**
Moves the cursor to the first child node.**

**BreezeLastChild**
Moves the cursor to the last child node.**

**BreezeParent**
Moves the cursor to the parent node.**

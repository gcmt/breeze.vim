# breeze.vim

**v1.0**

Basic DOM navigation.


## Requirements

* Vim compiled with python 2.6+


## Installation

You can either extract the content of the folder into the `$HOME/.vim`
directory or use your favorite plugin manager, such as Vundle or Pathogen.                         


## Commands

### BreezeMatchTag
If the cursor is on the opening tag, this command moves the cursor to the closing
tag, and vice-versa. If the command is called in other locations this command moves
the cursor to the opening tag of the node that presumably enclose our position.

### BreezeNextSibling
Moves the cursor to the next sibling node.

### BreezePrevSibling
Moves the cursor to the previous sibling node.

### BreezeFirstChild
Moves the cursor to the first child node.

### BreezeLastChild
Moves the cursor to the last child node.

### BreezeParent
Moves the cursor to the parent node.

### BreezePrintDom
Prints the DOM.

### ... more coming


## Settings

None.

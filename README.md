# deoplete-notmuch

Deoplete-notmuch offers asynchronous completion of email addresses using `notmuch address`.
Inspired by @fszymanski and @frbor's abook sources.

## Installation

To install `deoplete-notmuch`, use your favourite plugin manager.

#### Using [vim-plug](https://github.com/junegunn/vim-plug) on neovim

```vim
Plug 'Shougo/deoplete.nvim', {'do': ':UpdateRemotePlugins'}
Plug 'paretje/deoplete-notmuch', {'for': 'mail'}
```

## Configuration
```vim
" notmuch address command to fetch completions
" NOTE: --format=sexp is required
let g:deoplete#sources#notmuch#command = ['notmuch', 'address', '--format=sexp', '--output=recipients', '--deduplicate=address', 'tag:sent']
```

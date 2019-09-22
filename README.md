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
" NOTE: --format=json is required
let g:deoplete#sources#notmuch#command = ['notmuch', 'address', '--format=json', '--deduplicate=address', '*']
```

The command must output JSON in the following schema to be parseable by this plugin (so as long as the output is in spec, one may try to use a different source than `notmuch`):
```json
[
    {
        "name":"Jane Doe",
        "address":"jane@mail.doe",
        "name-addr":"Jane Doe <jane@mail.doe>"
    },
]
```

You can modify the `notmuch search` to great extents, for example replace `'*'` by `tag:sent` and add `--output=recipients` to narrow the completions down to people who already received an email from you. For further information, see `man 1 notmuch-address` and `man 7 notmuch-search-terms`.

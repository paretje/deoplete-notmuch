import re
import subprocess
from subprocess import CalledProcessError
from .base import Base


class Source(Base):
    COLON_PATTERN = re.compile(r':\s?')
    COMMA_PATTERN = re.compile(r'.+,\s?')
    HEADER_PATTERN = re.compile(r'^(Bcc|Cc|From|Reply-To|To):(\s?|.+,\s?)')
    SEXP_PATTERN = re.compile(r'\(:name "(?P<name>.*)" :address "(?P<address>.+)" :name-addr "(?P<name_addr>.+)"\)')

    def __init__(self, vim):
        super().__init__(vim)

        # TODO: sensible rank?
        self.rank = 600
        self.name = 'notmuch'
        self.mark = '[nm]'
        self.min_pattern_length = 0
        self.filetypes = ['mail']
        # TODO: fszymanski/deoplete-abook doesn't define input_pattern at all
        self.input_pattern = '[^:,]+'
        # TODO: other options: ['matcher_length', 'matcher_full_fuzzy']
        # self.matchers = ['matcher_fuzzy']

        # TODO: should this be done in on_init?
        self.command = vim.vars.get('deoplete#sources#notmuch#command',
                                    ['notmuch', 'address',
                                     '--format=sexp',
                                     '--output=recipients',
                                     '--deduplicate=address',
                                     'tag:sent'])

    def get_complete_position(self, context):
        colon = self.COLON_PATTERN.search(context['input'])
        comma = self.COMMA_PATTERN.search(context['input'])
        return max(colon.end() if colon is not None else -1,
                   comma.end() if comma is not None else -1)

    # TODO: caching
    def gather_candidates(self, context):
        if self.HEADER_PATTERN.search(context['input']) is None:
            return []

        try:
            command_results = subprocess.check_output(self.command, universal_newlines=True).split('\n')
        except CalledProcessError:
            return []

        results = []
        for row in command_results:
            regexp = self.SEXP_PATTERN.search(row.strip())
            if regexp:
                results.append({'word': regexp.group("name_addr")})
        return results

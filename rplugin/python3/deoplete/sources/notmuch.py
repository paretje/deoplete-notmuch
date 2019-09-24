import json
import re
import subprocess
import time
from .base import Base


class Source(Base):
    COLON_PATTERN = re.compile(r':\s*')
    COMMA_PATTERN = re.compile(r',\s*')
    HEADER_PATTERN = re.compile(r'^(Bcc|Cc|From|Reply-To|To):')
    MAX_CACHE_AGE = 10  # in seconds

    def __init__(self, vim):
        super().__init__(vim)

        self.rank = 75  # default is 100, give deoplete-abook priority
        self.name = 'notmuch'
        self.mark = '[nm]'
        self.min_pattern_length = 0
        self.filetypes = ['mail']
        self.matchers = ['matcher_full_fuzzy', 'matcher_length']
        self.last_update = None
        self.results = None

    def on_init(self, context):
        self.command = context['vars'].get('deoplete#sources#notmuch#command',
                                           ['notmuch', 'address',
                                            '--format=json',
                                            '--deduplicate=address',
                                            '*'])

    def get_complete_position(self, context):
        colon = self.COLON_PATTERN.search(context['input'])
        comma = self.COMMA_PATTERN.search(context['input'])
        return max(colon.end() if colon is not None else -1,
                   comma.end() if comma is not None else -1)

    def gather_candidates(self, context):
        if self.HEADER_PATTERN.search(context['input']) is None:
            return

        if not self.results or time.time() - self.last_update > self.MAX_CACHE_AGE:
            command_results = subprocess.check_output(self.command)
            self.results = [{'word': e['name-addr'] + ', ', 'abbr':e['name-addr']}
                            for e in json.loads(command_results)]
            self.last_update = time.time()
        return self.results

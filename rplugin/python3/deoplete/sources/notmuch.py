import json
import re
import subprocess
from subprocess import CalledProcessError
from .base import Base


class Source(Base):
    COLON_PATTERN = re.compile(r':\s?')
    COMMA_PATTERN = re.compile(r'.+,\s?')
    HEADER_PATTERN = re.compile(r'^(Bcc|Cc|From|Reply-To|To):(\s?|.+,\s?)')

    def __init__(self, vim):
        super().__init__(vim)

        self.rank = 75  # default is 100, give deoplete-abook priority
        self.name = 'notmuch'
        self.mark = '[nm]'
        self.min_pattern_length = 0
        self.filetypes = ['mail']
        self.matchers = ['matcher_full_fuzzy', 'matcher_length']

    def on_init(self, context):
        self.command = context['vars'].get('deoplete#sources#notmuch#command',
                                           ['notmuch', 'address',
                                            '--format=json',
                                            '--output=recipients',
                                            'tag:sent'])

    def get_complete_position(self, context):
        colon = self.COLON_PATTERN.search(context['input'])
        comma = self.COMMA_PATTERN.search(context['input'])
        return max(colon.end() if colon is not None else -1,
                   comma.end() if comma is not None else -1)

    # TODO: caching?
    def gather_candidates(self, context):
        if self.HEADER_PATTERN.search(context['input']) is None:
            return
    
        command_results = subprocess.check_output(self.command)
        results = json.loads(command_results)
        return [ e['name-addr'] for e in results]

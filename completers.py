from prompt_toolkit.completion import Completer, Completion
import os, re

class StaticCompleter(Completer):
    def __init__(self, words: list[str]):
        self.words = words

    def get_completions(self, document, complete_event):
        text_before_cursor = document.text_before_cursor
        for word in self.words:
            if word.startswith(text_before_cursor):
                yield Completion(word, start_position=-len(text_before_cursor))

def dir_sort(path, files: list[str]) -> list[str]:
    # sort files alphabetically
    files.sort()
    # now, sort files so that directories come before files
    files.sort(key=lambda f: os.path.isdir(os.path.join(path, f)))
    # add a '/' to directories
    files = [f + ('/' if os.path.isdir(os.path.join(path, f)) else '') for f in files]
    return files

class FileCompleter(Completer):
    def get_completions(self, document, complete_event):
        text_before_cursor = document.text_before_cursor
        path = os.getcwd()

        if text_before_cursor:
            parts = text_before_cursor.split('/')
            path = os.path.join(path, *parts[:-1])

        try:
            files = os.listdir(path)
            # ignore .git directory
            files = [f for f in files if not f == '.git']
            # check for a .gitignore file and ignore any files that match the globs in the .gitignore file
            # we can't use regular expressions directly on the globs, so we need to
            # escape periods and convert asterisks to regex wildcards
            # for example: *.pyc -> .*\.pyc
            if os.path.exists(os.path.join(path, '.gitignore')):
                with open(os.path.join(path, '.gitignore'), 'r') as f:
                    # escape periods
                    ignore_globs = [glob.replace('.', '\\.') for glob in f.read().splitlines()]
                    # replace asterisks with regex wildcards
                    ignore_globs = [glob.replace('*', '.*') for glob in ignore_globs]
                    files = [f for f in files if not re.match('|'.join(ignore_globs), f)]

            files = dir_sort(path, files)

        except OSError:
            files = []

        for f in files:
            if not text_before_cursor or f.startswith(os.path.basename(text_before_cursor)):
                completion = os.path.join(os.path.dirname(text_before_cursor), f)
                yield Completion(completion, start_position=-len(text_before_cursor))

from prompt_toolkit.document import Document

class MainCompleter(Completer):
    def __init__(self):
        # Define static commands
        commands = ['load', 'drop', 'help']

        # Create completers
        self.command_completer = StaticCompleter(commands)
        self.file_completer = FileCompleter()

    def get_completions(self, document, complete_event):
        text_before_cursor = document.text_before_cursor
        words = text_before_cursor.split()

        if not complete_event.completion_requested and text_before_cursor.endswith(' '):
            return
        if not words or (len(words) == 1 and not text_before_cursor.endswith(' ')):
            yield from self.command_completer.get_completions(document, complete_event)
        elif words[0] == 'load':
            # Adjust document for file completer
            file_document = Document(text=' '.join(words[1:]), cursor_position=document.cursor_position - len(words[0]) - 1)
            yield from self.file_completer.get_completions(file_document, complete_event)

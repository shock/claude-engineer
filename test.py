from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
import os
import asyncio
import re

class StaticCompleter(Completer):
    def __init__(self, words):
        self.words = words

    def get_completions(self, document, complete_event):
        text_before_cursor = document.text_before_cursor
        for word in self.words:
            if word.startswith(text_before_cursor):
                yield Completion(word, start_position=-len(text_before_cursor))

ROOT_DIR = os.getcwd()

class FileCompleter(Completer):
    def get_completions(self, document, complete_event):
        text_before_cursor = document.text_before_cursor
        path = ROOT_DIR

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
            # if os.path.exists(os.path.join(path, '.gitignore')):
            #     with open(os.path.join(path, '.gitignore'), 'r') as f:
            #         ignore_globs = [re.escape(glob) for glob in f.read().splitlines()]
                    files = [f for f in files if not re.match('|'.join(ignore_globs), f)]
            # # ignore hidden files
            # files = [f for f in files if not f.startswith('.')]

            # sort files alphabetically
            files.sort()

            # now, sort files so that directories come before files
            files.sort(key=lambda f: os.path.isdir(os.path.join(path, f)))

            # add a '/' to directories
            files = [f + ('/' if os.path.isdir(os.path.join(path, f)) else '') for f in files]


        except OSError:
            files = []

        for f in files:
            if not text_before_cursor or f.startswith(os.path.basename(text_before_cursor)):
                completion = os.path.join(os.path.dirname(text_before_cursor), f)
                yield Completion(completion, start_position=-len(text_before_cursor))

from prompt_toolkit.document import Document

class MainCompleter(Completer):
    def __init__(self, command_completer, file_completer):
        self.command_completer = command_completer
        self.file_completer = file_completer

    def get_completions(self, document, complete_event):
        text_before_cursor = document.text_before_cursor
        words = text_before_cursor.split()

        if not words or (len(words) == 1 and not text_before_cursor.endswith(' ')):
            yield from self.command_completer.get_completions(document, complete_event)
        elif words[0] == 'load':
            # Adjust document for file completer
            file_document = Document(text=' '.join(words[1:]), cursor_position=document.cursor_position - len(words[0]) - 1)
            yield from self.file_completer.get_completions(file_document, complete_event)

# Define static commands
commands = ['load', 'drop', 'help']

# Create completers
command_completer = StaticCompleter(commands)
file_completer = FileCompleter()
main_completer = MainCompleter(command_completer, file_completer)

# Create a PromptSession
session = PromptSession()

async def get_prompt():
    prompt = await asyncio.to_thread(session.prompt, '> ', completer=main_completer)
    return prompt

async def main():
    while True:
        try:
            user_input = await get_prompt()
            print(f'You entered: {user_input}')
        except KeyboardInterrupt:
            break
        except EOFError:
            break

if __name__ == "__main__":
    asyncio.run(main())

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
import os


class StaticCompleter(Completer):
    def __init__(self, words):
        self.words = words

    def get_completions(self, document, complete_event):
        text_before_cursor = document.text_before_cursor
        for word in self.words:
            if word.startswith(text_before_cursor):
                yield Completion(word, start_position=-len(text_before_cursor))

class FileCompleter(Completer):
    def get_completions(self, document, complete_event):
        # Get the text before the cursor
        text_before_cursor = document.text_before_cursor
        # List files in the current working directory
        files = os.listdir('.')
        # Filter files that start with the text before the cursor
        completions = [f for f in files if f.startswith(text_before_cursor)]

        # Yield Completion objects for each matching file
        for completion in completions:
            yield Completion(completion, start_position=-len(text_before_cursor))

class MainCompleter(Completer):
    def __init__(self, command_completer, file_completer):
        self.command_completer = command_completer
        self.file_completer = file_completer

    def get_completions(self, document, complete_event):
        text_before_cursor = document.text_before_cursor
        words = text_before_cursor.split()

        if len(words) == 1:
            yield from self.command_completer.get_completions(document, complete_event)
        elif len(words) > 1 and words[0] == 'load':
            # Adjust document for file completer
            new_document = document._replace(text_before_cursor=text_before_cursor[len(words[0])+1:])
            yield from self.file_completer.get_completions(new_document, complete_event)
        # Add more commands and their respective completers here as needed.

from prompt_toolkit import PromptSession

# Define static commands
commands = ['load', 'drop', 'help']

# Create completers
command_completer = StaticCompleter(commands)
file_completer = FileCompleter()
main_completer = MainCompleter(command_completer, file_completer)

# Create a PromptSession
session = PromptSession()

while True:
    try:
        # Use the main completer with the prompt session
        user_input = session.prompt('> ', completer=main_completer)
        print(f'You entered: {user_input}')
    except KeyboardInterrupt:
        # Handle Ctrl+C to exit gracefully
        break
    except EOFError:
        # Handle Ctrl+D to exit gracefully
        break

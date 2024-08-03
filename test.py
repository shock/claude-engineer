from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
import os
import asyncio

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
        # Get the text before the cursor
        text_before_cursor = document.text_before_cursor
        # List files in the current working directory
        path = ROOT_DIR
        parts = text_before_cursor.split('/')
        path = os.path.join(path, *parts[:-1])
        if len(parts) > 1:
            os.chdir(path)
        files = os.listdir('.')
        # Filter files that start with the text before the cursor
        completions = []
        for f in files:
            if f.startswith(parts[-1]):
                path_parts = parts[:-1] + [f]
                completion = "/".join(path_parts)
                completions.append(completion)
        # completions = ["/".join(parts[:-1].append(f))  for f in files if f.startswith(parts[-1])]

        # Yield Completion objects for each matching file
        for completion in completions:
            # yield Completion(os.path.join(text_before_cursor.rsplit('/', 1)[0], completion), start_position=-len(text_before_cursor))
            yield Completion(completion, start_position=-len(text_before_cursor))

from prompt_toolkit.document import Document

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
            new_document = Document(text=' '.join(words[1:]), cursor_position=document.cursor_position - len(words[0]) - 1)
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

async def get_prompt():
    # prompt = session.prompt('> ', completer=main_completer)
    prompt = await asyncio.to_thread(session.prompt, '> ', completer=main_completer)
    return prompt

async def main():
    while True:
        try:
            # Use the main completer with the prompt session
            user_input = await get_prompt()
            print(f'You entered: {user_input}')
        except KeyboardInterrupt:
            # Handle Ctrl+C to exit gracefully
            break
        except EOFError:
            # Handle Ctrl+D to exit gracefully
            break

if __name__ == "__main__":
    asyncio.run(main())

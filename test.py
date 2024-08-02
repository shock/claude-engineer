from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
import os

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

# Create a PromptSession
session = PromptSession()

while True:
    try:
        # Use the custom FileCompleter with the prompt session
        user_input = session.prompt('> ', completer=FileCompleter())
        print(f'You entered: {user_input}')
    except KeyboardInterrupt:
        # Handle Ctrl+C to exit gracefully
        break
    except EOFError:
        # Handle Ctrl+D to exit gracefully
        break

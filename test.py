from prompt_toolkit import PromptSession
import os
import asyncio
import re
from completers import *

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

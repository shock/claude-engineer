from prompt_toolkit import PromptSession
import os
import asyncio
import re
from completers import *

main_completer = MainCompleter()

# Create a PromptSession
session = PromptSession()

async def get_prompt():
    prompt = await asyncio.to_thread(session.prompt, '> ', completer=main_completer)
    return prompt

async def main():
    print("Starting main loop...")
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

#!/usr/bin/env python3

import os
from dotenv import load_dotenv
import json
from tavily import TavilyClient
import base64
from PIL import Image
import io
import re
from anthropic import Anthropic, APIStatusError, APIError
import difflib
import time
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.markdown import Markdown
import asyncio
import aiohttp
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style

from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
import datetime
import venv
import subprocess
import sys
import signal
import logging
from typing import Tuple, Optional

console = Console()
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion

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

# Create a PromptSession
session = PromptSession()

async def get_user_input(prompt="You: ", completer=None):
    style = Style.from_dict({
        'prompt': 'cyan bold',
    })
    session = PromptSession(style=style)
    return await session.prompt_async(prompt, multiline=False)


async def main():
    global automode, conversation_history
    console.print(Panel("Welcome to the Claude-3-Sonnet Engineer Chat with Multi-Agent and Image Support!", title="Welcome", style="bold green"))

    file_completer = FileCompleter()

    prompt_ready = False
    while True:
        try:
            prompt_ready = True
            user_input = await get_user_input(prompt="You: ", completer=file_completer)
            prompt_ready = False
            print(user_input)
        except Exception as e:
            console.print(Panel(f"Error: {e}", title="Error", style="bold red"))
            continue

if __name__ == "__main__":
    asyncio.run(main())

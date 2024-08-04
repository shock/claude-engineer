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
from completers import MainCompleter

# Create a PromptSession
session = PromptSession()
main_completer = MainCompleter()

async def get_user_input(prompt="You: ", completer=None):
    style = Style.from_dict({
        'prompt': 'cyan bold',
    })
    session = PromptSession(style=style)
    # return await session.prompt_async(prompt, multiline=False)
    prompt = await asyncio.to_thread(session.prompt, prompt, multiline=False, completer=completer)
    return prompt


async def main():
    global automode, conversation_history
    console.print(Panel("Welcome to the Claude-3-Sonnet Engineer Chat with Multi-Agent and Image Support!", title="Welcome", style="bold green"))

    prompt_ready = False
    while True:
        try:
            prompt_ready = True
            user_input = await get_user_input(prompt="You: ", completer=main_completer)
            prompt_ready = False
            print(user_input)
        except Exception as e:
            console.print(Panel(f"Error: {e}", title="Error", style="bold red"))
            continue

if __name__ == "__main__":
    asyncio.run(main())

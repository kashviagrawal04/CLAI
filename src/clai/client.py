"""Thin wrapper around the Anthropic SDK used by the clai CLI."""

from __future__ import annotations

import os
import sys

DEFAULT_MODEL = "claude-sonnet-4-6"


def get_api_key() -> str:
    """Read the API key from the environment or exit with a helpful message."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print(
            "Error: ANTHROPIC_API_KEY is not set.\n"
            "Get a key at https://console.anthropic.com/ and then run:\n"
            "  export ANTHROPIC_API_KEY=sk-ant-...",
            file=sys.stderr,
        )
        sys.exit(1)
    return api_key


def get_client():
    """Create and return an Anthropic client instance."""
    try:
        import anthropic
    except ImportError:
        print(
            "Error: the 'anthropic' package is not installed.\n"
            "Run: pip install -r requirements.txt",
            file=sys.stderr,
        )
        sys.exit(1)

    return anthropic.Anthropic(api_key=get_api_key())


def complete(prompt: str, system: str | None = None, model: str = DEFAULT_MODEL,
             max_tokens: int = 1024) -> str:
    """Send a single prompt to Claude and return the text response."""
    client = get_client()
    kwargs = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system:
        kwargs["system"] = system

    response = client.messages.create(**kwargs)
    return "".join(block.text for block in response.content if block.type == "text")


def stream_chat(messages: list[dict], model: str = DEFAULT_MODEL, max_tokens: int = 1024):
    """Stream a multi-turn chat response from Claude, yielding text chunks."""
    client = get_client()
    with client.messages.stream(
        model=model,
        max_tokens=max_tokens,
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            yield text

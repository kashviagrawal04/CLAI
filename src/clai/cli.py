"""Command-line interface for clai."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .client import complete, stream_chat, DEFAULT_MODEL

MAX_FILE_CHARS = 60_000  # keep summarize/ask input to a sane size


def cmd_ask(args: argparse.Namespace) -> int:
    answer = complete(args.question, model=args.model)
    print(answer)
    return 0


def cmd_summarize(args: argparse.Namespace) -> int:
    path = Path(args.file)
    if not path.exists():
        print(f"Error: file not found: {path}", file=sys.stderr)
        return 1

    text = path.read_text(errors="ignore")[:MAX_FILE_CHARS]
    prompt = f"Summarize the following file in {args.length} bullet points:\n\n{text}"
    summary = complete(prompt, model=args.model)
    print(summary)
    return 0


def cmd_chat(args: argparse.Namespace) -> int:
    print("clai chat — type 'exit' or Ctrl-D to quit.\n")
    history: list[dict] = []

    while True:
        try:
            user_input = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye!")
            return 0

        if user_input.lower() in {"exit", "quit"}:
            print("bye!")
            return 0
        if not user_input:
            continue

        history.append({"role": "user", "content": user_input})
        print("clai> ", end="", flush=True)

        reply_chunks = []
        for chunk in stream_chat(history, model=args.model):
            print(chunk, end="", flush=True)
            reply_chunks.append(chunk)
        print()

        history.append({"role": "assistant", "content": "".join(reply_chunks)})

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="clai",
        description="A small command-line AI assistant powered by the Claude API.",
    )
    parser.add_argument("--version", action="version", version=f"clai {__version__}")

    subparsers = parser.add_subparsers(dest="command", required=True)

    ask_parser = subparsers.add_parser("ask", help="Ask a one-off question")
    ask_parser.add_argument("question", help="The question to ask")
    ask_parser.add_argument("--model", default=DEFAULT_MODEL, help="Model to use")
    ask_parser.set_defaults(func=cmd_ask)

    summarize_parser = subparsers.add_parser("summarize", help="Summarize a text file")
    summarize_parser.add_argument("file", help="Path to the file to summarize")
    summarize_parser.add_argument("--length", type=int, default=5, help="Number of bullet points")
    summarize_parser.add_argument("--model", default=DEFAULT_MODEL, help="Model to use")
    summarize_parser.set_defaults(func=cmd_summarize)

    chat_parser = subparsers.add_parser("chat", help="Start an interactive chat session")
    chat_parser.add_argument("--model", default=DEFAULT_MODEL, help="Model to use")
    chat_parser.set_defaults(func=cmd_chat)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

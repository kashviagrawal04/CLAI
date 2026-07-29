"""Tests for clai.cli — focused on parsing and logic that doesn't need a live API key."""

import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from clai.cli import build_parser, cmd_summarize  # noqa: E402


def test_parser_ask():
    parser = build_parser()
    args = parser.parse_args(["ask", "what is the capital of France?"])
    assert args.command == "ask"
    assert args.question == "what is the capital of France?"


def test_parser_summarize_defaults():
    parser = build_parser()
    args = parser.parse_args(["summarize", "notes.txt"])
    assert args.file == "notes.txt"
    assert args.length == 5


def test_parser_summarize_custom_length():
    parser = build_parser()
    args = parser.parse_args(["summarize", "notes.txt", "--length", "3"])
    assert args.length == 3


def test_parser_chat():
    parser = build_parser()
    args = parser.parse_args(["chat"])
    assert args.command == "chat"


def test_summarize_missing_file(capsys):
    parser = build_parser()
    args = parser.parse_args(["summarize", "/no/such/file.txt"])
    exit_code = cmd_summarize(args)
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "not found" in captured.err


def test_summarize_calls_complete(tmp_path):
    test_file = tmp_path / "notes.txt"
    test_file.write_text("Some notes about clai.")

    parser = build_parser()
    args = parser.parse_args(["summarize", str(test_file)])

    with patch("clai.cli.complete", return_value="- A summary point") as mock_complete:
        exit_code = cmd_summarize(args)

    assert exit_code == 0
    assert mock_complete.called
    prompt_arg = mock_complete.call_args[0][0]
    assert "Some notes about clai." in prompt_arg

# clai

A small command-line AI assistant powered by the [Claude API](https://www.anthropic.com).

```
$ clai ask "why is the sky blue?"
The sky appears blue because of Rayleigh scattering...

$ clai summarize report.txt --length 3
- Point one...
- Point two...
- Point three...

$ clai chat
clai chat — type 'exit' or Ctrl-D to quit.
you> hey, what can you help with?
clai> ...
```

## Features

- **`clai ask <question>`** — get a quick one-off answer
- **`clai summarize <file>`** — summarize any text file into bullet points
- **`clai chat`** — interactive, streaming multi-turn chat session in your terminal

## Installation

```bash
git clone https://github.com/<your-username>/clai.git
cd clai
pip install -e .
```

## Setup

Get an API key from the [Anthropic Console](https://console.anthropic.com/) and export it:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

## Usage

```bash
clai ask "explain quicksort in one paragraph"
clai summarize notes.txt --length 5
clai chat --model claude-sonnet-4-6
```

Run `clai --help` or `clai <command> --help` for all options.

## Development

```bash
pip install -e ".[dev]"
pytest
```

## Project structure

```
clai/
├── src/clai/
│   ├── __init__.py
│   ├── cli.py       # argparse-based CLI and subcommands
│   └── client.py     # thin wrapper around the Anthropic SDK
├── tests/
│   └── test_cli.py
├── .github/workflows/tests.yml   # CI: runs pytest on push/PR
├── pyproject.toml
├── requirements.txt
└── LICENSE
```

## License

MIT — see [LICENSE](LICENSE).

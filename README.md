# simple-agent

A minimal tool-calling agent, built as a base for a **prompt injection**
exercise. One person builds the agent; the other writes injection attacks
against it.

## How it works

The agent (`agent.py`) runs a simple loop on top of the Anthropic Messages API:

1. Send the conversation (and the available tools) to the model.
2. If the model asks to use a tool, run it (`tools.py`) and send the result back.
3. Repeat until the model returns a plain text answer.

Two tools are available:

- `read_note` — read a note file from the `notes/` folder.
- `calculator` — evaluate a basic arithmetic expression.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...   # or copy .env.example to .env
```

## Run

```bash
python agent.py
```

Then try, for example:

```
you> What's on my todo list?
you> What is 18 * (7 + 4)?
```

## Project layout

```
agent.py        the agent loop
tools.py        the tools (read_note, calculator)
notes/          note files the agent can read
requirements.txt
```

## Prompt injection (second part)

The `read_note` tool returns the raw text of a file, and the agent passes that
text to the model. This is the attack surface: a note can contain instructions
aimed at the model ("ignore your previous instructions and ...") to make the
agent misbehave.

The injection work lives in `notes/` — add attack notes there (e.g.
`injected.txt`) and document, for each one, what it tries to do and whether the
agent falls for it.

## Notes

- Model used: `claude-sonnet-5-5` (change `MODEL` in `agent.py`).
- To use a different provider, swap the `client.messages.create(...)` call in
  `agent.py` for that provider's SDK; the loop structure stays the same.

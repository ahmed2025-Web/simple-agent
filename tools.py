"""Tools the agent can call.

Two simple tools:
  - read_note: read a note file from the notes/ folder (untrusted content!)
  - calculator: evaluate a basic arithmetic expression

`read_note` is the interesting one for prompt injection: the text it returns
comes from a file, and a note can contain instructions aimed at the model.
"""

import os

NOTES_DIR = os.path.join(os.path.dirname(__file__), "notes")

# Tool schemas sent to the model.
TOOLS = [
    {
        "name": "read_note",
        "description": "Read the contents of one of the user's notes by file name.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The note file name, e.g. 'todo.txt'.",
                }
            },
            "required": ["name"],
        },
    },
    {
        "name": "calculator",
        "description": "Evaluate a basic arithmetic expression, e.g. '3 * (4 + 5)'.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The arithmetic expression to evaluate.",
                }
            },
            "required": ["expression"],
        },
    },
]


def run_tool(name: str, tool_input: dict) -> str:
    """Dispatch a tool call by name and return its result as text."""
    if name == "read_note":
        return _read_note(tool_input.get("name", ""))
    if name == "calculator":
        return _calculator(tool_input.get("expression", ""))
    return f"Error: unknown tool '{name}'."


def _read_note(name: str) -> str:
    # Keep the read inside notes/ so a note name cannot escape the folder.
    safe_name = os.path.basename(name)
    path = os.path.join(NOTES_DIR, safe_name)
    if not os.path.isfile(path):
        available = ", ".join(sorted(os.listdir(NOTES_DIR))) if os.path.isdir(NOTES_DIR) else ""
        return f"Error: note '{safe_name}' not found. Available notes: {available}"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _calculator(expression: str) -> str:
    # Evaluate arithmetic only, with no access to names or builtins.
    allowed = set("0123456789+-*/(). %")
    if not expression or set(expression) - allowed:
        return "Error: only numbers and + - * / % ( ) are allowed."
    try:
        result = eval(expression, {"__builtins__": {}}, {})  # noqa: S307 - input is filtered above
    except Exception as exc:  # noqa: BLE001
        return f"Error: could not evaluate expression ({exc})."
    return str(result)

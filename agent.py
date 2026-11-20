"""Simple agent with tool-calling, built on the Groq API (free tier).

The agent runs a loop: it sends the conversation to the model, and if the
model asks to use a tool, we run that tool and send the result back. This
continues until the model produces a plain text answer.

This is intentionally minimal so it is easy to read and easy to attack:
the prompt-injection experiments live in the documents the agent reads
(see the `notes/` folder and README).
"""

import os
import json

from groq import Groq

from tools import TOOLS, run_tool

MODEL = "llama-3.3-70b-versatile"
MAX_STEPS = 10

SYSTEM_PROMPT = (
    "You are a helpful personal assistant. "
    "You can read the user's notes and do arithmetic using the provided tools. "
    "Answer the user's questions using the information you find."
)


def run_agent(user_message: str) -> str:
    """Run the agent on a single user message and return its final answer."""
    client = Groq()  # reads GROQ_API_KEY from the environment

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    for _ in range(MAX_STEPS):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            max_tokens=1024,
        )
        message = response.choices[0].message

        # Record the assistant turn (text + any tool-call requests).
        messages.append(message)

        if not message.tool_calls:
            # No tool requested: the model gave a final answer.
            return message.content or ""

        # Run every tool the model asked for and feed the results back.
        for call in message.tool_calls:
            args = json.loads(call.function.arguments or "{}")
            print(f"[tool] {call.function.name}({json.dumps(args)})")
            result = run_tool(call.function.name, args)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result,
                }
            )

    return "Stopped: reached the maximum number of steps."


def main() -> None:
    if not os.environ.get("GROQ_API_KEY"):
        raise SystemExit("Please set the GROQ_API_KEY environment variable.")

    print("Simple agent. Type a question, or 'quit' to exit.\n")
    while True:
        try:
            user_message = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if user_message.lower() in {"quit", "exit"}:
            break
        if not user_message:
            continue
        answer = run_agent(user_message)
        print(f"\nagent> {answer}\n")


if __name__ == "__main__":
    main()

# notes/

Plain-text notes the agent can read with the `read_note` tool.

This folder is the main entry point for the **prompt injection** part of the
project: because the agent reads these files and passes their content to the
model, a note can contain text that tries to hijack the agent's behaviour.

Add your injection test cases here as new `.txt` files (for example
`injected.txt`) and document what each one tries to do.

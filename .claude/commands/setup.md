# First-Time Setup

Run all setup steps so the user can start using the Boiler Historian project. The user may have no coding experience — do not ask them to run commands or edit files. Handle everything yourself and explain what you're doing in plain language as you go.

## Steps

### 1. Check Python

Verify Python 3.11+ is installed:

```
python --version
```

If Python is not found or is below 3.11, stop and tell the user:
- They need to install Python 3.11 or newer
- Direct them to https://www.python.org/downloads/
- On Windows, remind them to check "Add Python to PATH" during installation
- Ask them to run `/setup` again after installing Python

### 2. Create a project-local virtual environment and install dependencies

Install all dependencies into a **virtual environment (`venv`) inside the project folder** rather
than into the user's global Python. This keeps everything self-contained: the packages live in a
`.venv/` folder in the project (already git-ignored), nothing is added to the global Python
installation, and there are no version clashes with other software on the user's machine.

First, create the virtual environment in the project root:

```
python -m venv .venv
```

Then install the dependencies **into the venv**, using the venv's own Python. The path to the
venv's Python depends on the operating system:

- **Windows:**
  ```
  .venv/Scripts/python -m pip install -r requirements.txt
  ```
- **macOS / Linux:**
  ```
  .venv/bin/python -m pip install -r requirements.txt
  ```

**Important — for every remaining step in this setup, use the venv's Python, not the bare
`python`.** In the commands below this is written as `<venv-python>`; substitute the correct path
for the operating system (`.venv/Scripts/python` on Windows, `.venv/bin/python` on macOS/Linux).
Using the venv's Python is what ensures the newly installed packages are found.

Tell the user this may take a minute or two on first run, especially for the machine learning
packages. If `python -m venv` fails because `venv` is unavailable (rare, on some minimal Linux
installs), tell the user to install it (e.g. `sudo apt install python3-venv`) and run `/setup`
again.

### 3. Build the document search index

Check if the vector database already exists (run with the venv's Python):

```
<venv-python> -c "import os; print('exists' if os.path.isdir('rag_vector_db') and len(os.listdir('rag_vector_db')) > 0 else 'missing')"
```

If it prints "missing", build it:

```
<venv-python> build_docs_db.py
```

Tell the user this downloads a small AI model (~130 MB) on first run for document search. It only needs to happen once.

If it prints "exists", skip this step and tell the user the document index is already built.

### 4. Configure the MCP server

The MCP server is registered in a file named `.mcp.json` at the project root — this is the
file Claude Code reads to discover project-scoped MCP servers. **Important:**
`.claude/settings.local.json` does NOT register MCP servers; it must be `.mcp.json`.

Check whether `.mcp.json` already exists at the project root with a `boiler-historian`
entry. If it does, skip this step.

If not, determine the absolute path to this project directory (run with the venv's Python):

```
<venv-python> -c "import os; print(os.path.abspath('.'))"
```

And the absolute path to the venv's Python interpreter — **run this with the venv's Python**, so
the path returned points at the venv (this is what makes the MCP server use the project-local
packages rather than the global Python):

```
<venv-python> -c "import sys; print(sys.executable)"
```

Then create `.mcp.json` at the project root with this content:

```json
{
  "mcpServers": {
    "boiler-historian": {
      "type": "stdio",
      "command": "<absolute path to venv python>",
      "args": ["<absolute path to project directory>/historian_mcp_server.py"]
    }
  }
}
```

Use the actual absolute paths from the commands above — the venv interpreter path for `command`,
and the project directory joined with `historian_mcp_server.py` for the `args` entry. Use
forward slashes even on Windows.

### 5. Tell the user what to do next

Tell the user:

1. Setup is complete!
2. They need to **restart Claude Code** for the boiler data tools to become available. This is required because the MCP server configuration was just added and Claude Code needs to reload it. On restart, Claude Code may show a one-time prompt asking whether to trust/use the `boiler-historian` MCP server configured in `.mcp.json` — they should **approve/allow it**, or the tools will not connect.
3. After restarting, they can start asking questions about the boiler. Some examples:
   - "List all the sensor tags available."
   - "What has steam temperature been doing over the last day?"
   - "What alarms were firing on March 29 around 2pm?"
   - "What's upstream of the steam temperature sensor?"
   - "Show me the troubleshooting guide for high IDF vibration."
4. For a full guide to everything the system can do, see `CLAUDE.md`.
5. To run a statistical process monitoring analysis, type `/mspc-analysis`.

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

### 2. Install dependencies

```
pip install -r requirements.txt
```

If this fails with a permissions error, try:

```
pip install --user -r requirements.txt
```

Tell the user this may take a minute or two on first run, especially for the machine learning packages.

### 3. Build the document search index

Check if the vector database already exists:

```
python -c "import os; print('exists' if os.path.isdir('rag_vector_db') and len(os.listdir('rag_vector_db')) > 0 else 'missing')"
```

If it prints "missing", build it:

```
python build_docs_db.py
```

Tell the user this downloads a small AI model (~130 MB) on first run for document search. It only needs to happen once.

If it prints "exists", skip this step and tell the user the document index is already built.

### 4. Configure the MCP server

Read the file `.claude/settings.local.json`. Check if it already has a `mcpServers` entry with `boiler-historian` configured.

If NOT already configured, determine the absolute path to this project directory:

```
python -c "import os; print(os.path.abspath('.'))"
```

And determine the absolute path to the Python interpreter:

```
python -c "import sys; print(sys.executable)"
```

Then update `.claude/settings.local.json` to add the MCP server configuration. The file should look like this (merge with any existing content):

```json
{
  "mcpServers": {
    "boiler-historian": {
      "command": "<absolute path to python>",
      "args": ["historian_mcp_server.py"],
      "cwd": "<absolute path to project directory>"
    }
  }
}
```

Use the actual absolute paths from the commands above. Use forward slashes even on Windows.

### 5. Tell the user what to do next

Tell the user:

1. Setup is complete!
2. They need to **restart Claude Code** for the boiler data tools to become available. This is required because the MCP server configuration was just added and Claude Code needs to reload it.
3. After restarting, they can start asking questions about the boiler. Some examples:
   - "List all the sensor tags available."
   - "What has steam temperature been doing over the last day?"
   - "What alarms were firing on March 29 around 2pm?"
   - "What's upstream of the steam temperature sensor?"
   - "Show me the troubleshooting guide for high IDF vibration."
4. For a full guide to everything the system can do, see `CLAUDE.md`.
5. To run a statistical process monitoring analysis, type `/mspc-analysis`.

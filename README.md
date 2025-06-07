# AGENT MCP CARS

This is a simple implementation of a CLI interface for interacting with an agent that communicates with an MCP server and a car database.

The goal is to build an AI agent that can decide when to call tools — including one that sends a request to an MCP server, which then queries a local car database and returns results.

---

## Running the Project

This guide explains how to run the complete system — including the MCP server, CLI interface, and database.

---

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/REPO_NAME.git
cd REPO_NAME
```

2. Set Up Environment Variables

Create a .env file in the root of the project:

```python
DATABASE_URL=sqlite:///./carros.db
TOGETHER_API_KEY=sk-<your-together-api-key>
MCP_HOST=127.0.0.1
MCP_PORT=3333
```

💡 If you're not using Together.ai, you can omit the TOGETHER_API_KEY line.

3. Install Dependencies
Option A: Using uv (recommended)

```bash
uv sync
```
This will:

    Create the virtual environment

    Install all dependencies from uv.lock

    Set up the environment for running CLI commands via uv run

Option B: Using pip

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

Commands Reference

All commands are run via:

    uv run main.py <command> (if using uv)
    or
    PYTHONPATH=src python main.py <command>

seed-db – Seed the database
Populate the database with fake car entries.

    uv run main.py seed

Optional flags:

    --reseed: Drop and recreate all tables before seeding.

Example:
    uv run main.py seed --reseed

    mcp – Start the MCP server

Runs the local MCP server.

    uv run main.py mcp

Expected output:

MCP server running at 127.0.0.1:3333 ...

prompt – Run the interactive agent
Starts an interactive CLI where you can ask questions. The agent will decide when to query the database via the MCP server.

    uv run main.py prompt

check-db – Verify database connection
Check that the database connection is functional and print a summary.

    uv run main.py check-db

Notes

    Replace uv run ... with PYTHONPATH=src python main.py ... if not using uv

    All commands are run from the project root

    The database file will be created automatically as carros.db in the root directory

Example Workflow

# Seed the database
uv run main.py seed --reseed

# Start MCP server (in a new terminal)
uv run main.py mcp

# Open the interactive agent (in another terminal)
uv run main.py prompt

---

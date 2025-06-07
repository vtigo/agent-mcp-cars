# AGENT MCP CARS

This is a simple implementation of a CLI interface for interacting with an agent that communicates with an MCP server, which queries a car database.

The goal is to build an AI agent that can decide when to send requests to the MCP server — the MCP server contains all the logic for querying the database.

> AGENT -> MCP SERVER -> DATABASE -> MCP SERVER -> AGENT

---
## Running the Project

This guide explains how to run the complete system — including the MCP server, CLI interface, and database.
### 1. Clone the Repository

```bash
git clone https://github.com/vtigo/agent-mcp-cars.git
cd agent-mcp-cars
```
### 2. Set Up Environment Variables

Create a **.env** file in the root of the project:

```bash
DATABASE_URL=sqlite:///./carros.db
TOGETHER_API_KEY=sk-<your-together-api-key>
MCP_HOST=127.0.0.1
MCP_PORT=3333
```

### 3. Install Dependencies
#### Option A: Using uv (recommended)

```bash
uv sync
```
This will:

- Create the virtual environment
- Install all dependencies from uv.lock
- Set up the environment for running CLI commands via uv run

#### Option B: Using pip

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

--- 
## Commands Reference

All commands are run via:
```bash
uv run main.py <command> #(if using uv)
```

or
```bash
PYTHONPATH=src python main.py <command>
```

> all commands should be run from the root

### seed-db 
```bash
uv run main.py seed-db
```
Populate the database with fake car entries.
It also creates the database if it doesn't exist.

> optional flag:
> --reseed: Drop and recreate all tables before seeding.

### mcp
Runs the local MCP server.
```bash
uv run main.py mcp
```

### prompt
Starts an interactive CLI where you can ask questions. The agent will decide when to query the database via the MCP server.
```bash
uv run main.py prompt
```

### check-db
Check that the database connection is functional.
```bash
uv run main.py check-db
```
####
> Replace uv run ... with **PYTHONPATH=src python main.py** ... if not using uv
> 
> All commands are run from the project **root**
> 
> The database file will be created automatically as carros.db in the root directory

--- 
## Example Workflow

### 1. Seed the database

```bash
uv run main.py seed-db
```

### 2. Start MCP server
```bash
uv run main.py mcp
```


### 3. Open the interactive agent (in a new terminal)
```bash
uv run main.py prompt
```


---

# AGENT MCP CARS

This is a simple implementation of a CLI interface for chatting with an agent, a MCP server and a simple database modelling for cars.
The goal of this project is to have an agent that can reason about calling a tool that sends a request to a MCP server, who can query the database and return some cars.

## Running the project
This guide explains how to run the complete system (MCP server + interactive CLI) from a fresh clone.

---

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/REPO_NAME.git
cd REPO_NAME
```

### 2. Set up environment variables
Create a `.env` file in the root of the project with the following content:

```env
DATABASE_URL=sqlite:///./carros.db
TOGETHER_API_KEY=sk-<your-together-api-key>
MCP_HOST=127.0.0.1
MCP_PORT=3333
```

> **Note:** If you're not using Together.ai, you can omit the `TOGETHER_API_KEY` line.

### 3. Install dependencies

#### Using `uv` (recommended)

```bash
# This will create the virtual enviroment and install all the dependencies for you
uv sync
```

#### Or using standard `pip`

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

## The CLI 
To run the cli u can ...

or

```bash
# Run script that creates tables and populates with fake data
PYTHONPATH=src python main.py {command}
```

### Seed the database (this will create a cars.db file in the root if you dont already have it)

```bash
PYTHONPATH=src python main.py seed
```

### Start the MCP server
open a dedicated terminal instance (at the project root) and run:

```bash
PYTHONPATH=src python main.py mcp
```
you should see:

```
MCP server running at 127.0.0.1:3333 ...
```

### 6. Run the interactive prompt

In another terminal (at the project root):

```bash
PYTHONPATH=src uv run main.py prompt
```

Type your questions and wait for the agent to reply (it will query the database when needed).

---

### Useful commands

* **Check database connection**:

  ```bash
  PYTHONPATH=src uv run main.py check-db
  ```
```
```


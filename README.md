# AGENT MCP CARS

[![Python](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org)

An interactive CLI agent that communicates with an MCP server to query a car database.
The goal is to build an AI agent that decides when to send requests to the MCP server — which then queries the database and returns the results.

```
Agent ──▶ MCP Server ──▶ Database  
       ◀────────────────
```

---

## Running the Project

This guide explains how to run the complete system — including the MCP server, CLI interface, and database.

### 1. Clone the Repository

```bash
git clone https://github.com/vtigo/agent-mcp-cars.git
cd agent-mcp-cars
```

### 2. Set Up Environment Variables

Create a `.env` file in the root of the project:

```env
DATABASE_URL=sqlite:///./carros.db
TOGETHER_API_KEY=sk-<your-together-api-key>
MCP_HOST=127.0.0.1
MCP_PORT=3333
```

> 💡 If you're not using Together.ai, you can omit the `TOGETHER_API_KEY` line.

---

### 3. Install Dependencies

#### ✅ Option A: Using `uv` (recommended)

```bash
uv sync
```

This will:

* Create a `.venv/` if one doesn’t exist
* Install dependencies from `uv.lock`
* Prepare the environment for use with `uv run`

#### ✅ Option B: Using `pip`

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

---

## 🔧 Command Reference

All commands are run from the **project root** using either:

```bash
uv run main.py <command>
# OR (if not using uv)
PYTHONPATH=src python main.py <command>
```

### 📅 `seed-db`

Populate the database with fake car entries.
It also creates the database if it doesn't exist.

```bash
uv run main.py seed-db
```

> 💡 **Optional flag:**
> `--reseed` — Drops and recreates all tables before seeding.

Example:

```bash
uv run main.py seed-db --reseed
```

---

### 📧 `mcp`

Start the local MCP server.

```bash
uv run main.py mcp
```

Expected output:

```
MCP server running at 127.0.0.1:3333 ...
```

---

### 💬 `prompt`

Starts an interactive CLI where you can ask the agent questions.
The agent will decide when to query the MCP server to fetch data.

```bash
uv run main.py prompt
```
---

### ✅ `check-db`

Check that the database connection is functional and print a status report.

```bash
uv run main.py check-db
```
---

## 🧪 Example Workflow

Follow this step-by-step to run everything:

### 1. Seed the Database

```bash
uv run main.py seed-db --reseed
```

### 2. Start the MCP Server

```bash
uv run main.py mcp
```

### 3. Start the Interactive CLI Agent (in another terminal)

```bash
uv run main.py prompt
```

---

## 📌 Notes

* All commands assume you're in the **project root**
* Replace `uv run` with `PYTHONPATH=src python` if not using `uv`
* The database file (`carros.db`) is created automatically when seeding

---

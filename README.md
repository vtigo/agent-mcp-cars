# 🚗 AGENT MCP CARS

[![Python](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

An interactive CLI agent that communicates with an MCP server to query a car database.
The goal is to build an AI agent that decides when to send requests to the MCP server — which then queries the database and returns the results.

```
Agent ──▶ MCP Server ──▶ Database  
       ◀───────────────────────
```
---
## Project structure

```bash
├── cars.db # SQLite database, create with the seed script
├── main.py # Main entry point
├── pyproject.toml
├── README.md
├── requirements.txt
├── scripts
│   ├── read_db.py # Look at every entry in the database
│   └── start_mcp_server.py # Run the MCP server
├── src
│   └── app
│       ├── agent
│       │   ├── agent_llm.py
│       │   └── tools.py
│       ├── cli
│       │   ├── interface.py
│       ├── database
│       │   ├── config.py
│       │   ├── seed.py
│       │   └── session.py
│       ├── mcp
│       │   ├── client.py
│       │   └── server.py
│       ├── models
│       │   └── car.py
│       └── runner.py # Run the CLI with commands
├── tests
│   └── test.py
└── uv.lock
```

---

## 📦 Running the Project

This guide explains how to run the complete system — including the MCP server, CLI interface, and database.

### 1. Clone the Repository

```bash
git clone https://github.com/vtigo/agent-mcp-cars.git
cd agent-mcp-cars
```

### 2. Set Up Environment Variables

Create a `.env` file in the root of the project:

```env
DATABASE_URL=sqlite:///./cars.db
TOGETHER_API_KEY=sk-<your-together-api-key>
MCP_HOST=127.0.0.1
MCP_PORT=3333
```

> 💡 If do not have a together api key, check out the next section.

---

### 2.1 📡 Using the Together API (skip if you already have a together api key)

This project requires access to a language model via Together.ai. If you do not already have an API key, follow these steps:

1. Go to [https://api.together.xyz](https://api.together.xyz)
2. Sign up for an account
3. Navigate to the API section and generate your API key
4. Add the key to your `.env` file as:

```env
TOGETHER_API_KEY=sk-<your-together-api-key>
```
---

### 3. Install Dependencies

#### ✅ Option A: Using `uv` (recommended)

```bash
v sync
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows
```

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
python main.py <command>
```

### 📅 `seed-db`

Populate the database with fake car entries.
It also creates the database if it doesn't exist.

```bash
python main.py seed-db
```

> 💡 **Optional flag:**
> `--reseed` — Drops and recreates all tables before seeding.

Example:

```bash
python main.py seed-db --reseed
```

---

### 📧 `mcp`

Start the local MCP server.

```bash
python main.py mcp
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
python main.py prompt
```

---

### ✅ `check-db`

Check that the database connection is functional and print a status report.

```bash
python main.py check-db
```

---

## 🧪 Example Workflow

Follow this step-by-step to run everything:

### 1. Seed the Database

```bash
python main.py seed-db --reseed
```

### 2. Start the MCP Server

```bash
python main.py mcp
```

### 3. Start the Interactive CLI Agent (in another terminal)

```bash
python main.py prompt
```

---

## 📌 Notes

* All commands assume you're in the **project root**
* The database file (`cars.db`) is created automatically when seeding

---

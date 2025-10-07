# Expense Tracker MCP Server

A Model Context Protocol (MCP) server for tracking and managing personal expenses. This server provides tools for adding, listing, and summarizing expenses with SQLite database storage.

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Available Tools](#available-tools)
- [Available Resources](#available-resources)
- [Usage Examples](#usage-examples)
- [Testing the Server](#testing-the-server)
- [Converting FastAPI to FastMCP](#converting-fastapi-to-fastmcp)
- [Database Schema](#database-schema)
- [Categories](#categories)

## ✨ Features

- **Add Expenses**: Record expenses with date, amount, category, subcategory, and notes
- **List Expenses**: Retrieve expenses within a date range
- **Summarize Expenses**: Get category-wise expense summaries
- **Persistent Storage**: SQLite database for reliable data storage
- **Category Management**: Pre-defined expense categories with subcategories
- **MCP Resource**: Expose categories as a resource for AI models

## 📁 Project Structure

```
expense-tracker-mcp/
├── main.py              # Main MCP server implementation
├── pyproject.toml       # Project dependencies and metadata
├── categories.json      # Expense categories and subcategories
├── expenses.db          # SQLite database (auto-created)
├── uv.lock             # Lock file for dependencies
└── README.md           # This file
```

## 🔧 Prerequisites

- Python 3.13 or higher
- UV package manager (recommended) or pip
- Claude Desktop (for MCP integration)

## 🚀 Installation & Setup

### Step 1: Install UV

```bash
# On Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 2: Create Project Folder

```bash
mkdir expense-tracker-mcp
cd expense-tracker-mcp
```

### Step 3: Open in VS Code

```bash
code .
```

### Step 4: Open Terminal in VS Code

Use `` Ctrl + ` `` (backtick) or go to **Terminal** → **New Terminal**

### Step 5: Initialize UV Project

```bash
uv init
```

### Step 6: Add FastMCP Dependency

```bash
uv add fastmcp
```

### Step 7: Verify FastMCP Installation

```bash
fastmcp version
```

### Step 8: Create the Server

Create `main.py` with the expense tracker code (see project structure).

### Step 9: Test the Server (Development Mode)

```bash
uv run fastmcp dev main.py
```

This starts the server in development mode for testing.

### Step 10: Run the Server (Production Mode)

```bash
uv run fastmcp run main.py
```

### Step 11: Install to Claude Desktop

```bash
uv run fastmcp install claude-desktop main.py
```

This registers the MCP server with Claude Desktop, making it available as a tool.

## 🛠️ Available Tools

### 1. `add_expense`

Add a new expense entry to the database.

**Parameters:**

- `date` (string, required): Date in YYYY-MM-DD format
- `amount` (float, required): Expense amount
- `category` (string, required): Expense category
- `subcategory` (string, optional): Expense subcategory
- `note` (string, optional): Additional notes

**Returns:**

```json
{
  "status": "ok",
  "id": 1
}
```

### 2. `list_expenses`

List expense entries within an inclusive date range.

**Parameters:**

- `start_date` (string, required): Start date in YYYY-MM-DD format
- `end_date` (string, required): End date in YYYY-MM-DD format

**Returns:**

```json
[
  {
    "id": 1,
    "date": "2025-10-07",
    "amount": 50.0,
    "category": "food",
    "subcategory": "groceries",
    "note": "Weekly shopping"
  }
]
```

### 3. `summarize`

Summarize expenses by category within an inclusive date range.

**Parameters:**

- `start_date` (string, required): Start date in YYYY-MM-DD format
- `end_date` (string, required): End date in YYYY-MM-DD format
- `category` (string, optional): Filter by specific category

**Returns:**

```json
[
  {
    "category": "food",
    "total_amount": 150.0
  },
  {
    "category": "transport",
    "total_amount": 75.0
  }
]
```

## 📦 Available Resources

### `expense://categories`

Returns the list of available expense categories and their subcategories.

**MIME Type:** `application/json`

**Returns:** Content of `categories.json` file

## 💡 Usage Examples

Once installed in Claude Desktop, you can interact with the server using natural language:

**Example 1: Adding an expense**

```
Add an expense of $45.50 for groceries on 2025-10-07
```

**Example 2: Listing expenses**

```
Show me all expenses from 2025-10-01 to 2025-10-07
```

**Example 3: Summarizing expenses**

```
Summarize my expenses for October 2025
```

**Example 4: Category-specific summary**

```
How much did I spend on food in October?
```

## 🧪 Testing the Server

### Development Mode (with hot reload)

```bash
uv run fastmcp dev main.py
```

### Production Mode

```bash
uv run fastmcp run main.py
```

### Verify Server Status

After installing to Claude Desktop:

1. Open Claude Desktop
2. Check for the ExpenseTracker tools in the available tools list
3. Try asking Claude to add or list expenses

## 🔄 Converting FastAPI to FastMCP

If you have an existing FastAPI application and want to convert it to a FastMCP server, follow these steps:

### Step 1: Understand the Differences

| FastAPI                     | FastMCP                          |
| --------------------------- | -------------------------------- |
| Web API server              | MCP protocol server              |
| HTTP endpoints              | MCP tools & resources            |
| `@app.get()`, `@app.post()` | `@mcp.tool()`, `@mcp.resource()` |
| Request/Response model      | Function parameters/returns      |
| ASGI server (Uvicorn)       | MCP server (stdio/SSE)           |

### Step 2: Install FastMCP

```bash
uv add fastmcp
# or
pip install fastmcp
```

### Step 3: Replace FastAPI Imports

**Before (FastAPI):**

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
```

**After (FastMCP):**

```python
from fastmcp import FastMCP

mcp = FastMCP("YourServerName")
```

### Step 4: Convert Endpoints to Tools

**Before (FastAPI):**

```python
@app.post("/add-expense")
def add_expense(date: str, amount: float, category: str):
    # Your logic here
    return {"status": "ok", "id": 1}
```

**After (FastMCP):**

```python
@mcp.tool()
def add_expense(date: str, amount: float, category: str):
    '''Add a new expense entry to the database.'''
    # Your logic here
    return {"status": "ok", "id": 1}
```

### Step 5: Convert GET Endpoints to Resources (Optional)

If you have endpoints that serve static/dynamic data:

**Before (FastAPI):**

```python
@app.get("/categories")
def get_categories():
    with open("categories.json", "r") as f:
        return json.load(f)
```

**After (FastMCP):**

```python
@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    with open("categories.json", "r", encoding="utf-8") as f:
        return f.read()
```

### Step 6: Update the Main Entry Point

**Before (FastAPI):**

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**After (FastMCP):**

```python
if __name__ == "__main__":
    mcp.run()
```

### Step 7: Remove HTTP-Specific Code

Remove:

- Pydantic models (unless needed for validation)
- HTTP status codes
- Request/Response objects
- Middleware
- CORS configurations
- Authentication middleware (MCP handles this differently)

### Step 8: Test Your Conversion

```bash
# Test in development mode
uv run fastmcp dev main.py

# Install to Claude Desktop
uv run fastmcp install claude-desktop main.py
```

### Key Conversion Tips

1. **Simplify Returns**: MCP tools should return simple Python dictionaries, lists, or primitives
2. **Add Docstrings**: Always add clear docstrings to tools - AI models use these
3. **Use Type Hints**: Type hints help MCP understand tool parameters
4. **Remove HTTP Logic**: No need for status codes, headers, or HTTP-specific handling
5. **Direct Function Calls**: MCP tools are called directly, not via HTTP requests
6. **Database/Business Logic**: Keep all your existing business logic intact

### Example: Complete Conversion

**FastAPI Version:**

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Expense(BaseModel):
    date: str
    amount: float
    category: str

@app.post("/expenses")
def create_expense(expense: Expense):
    # Add to database
    return {"status": "success", "id": 1}

@app.get("/expenses")
def list_expenses(start_date: str, end_date: str):
    # Query database
    return [{"id": 1, "date": "2025-10-07", "amount": 50.0}]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**FastMCP Version:**

```python
from fastmcp import FastMCP
import sqlite3

mcp = FastMCP("ExpenseTracker")

@mcp.tool()
def add_expense(date: str, amount: float, category: str):
    '''Add a new expense entry to the database.'''
    # Add to database
    return {"status": "ok", "id": 1}

@mcp.tool()
def list_expenses(start_date: str, end_date: str):
    '''List expense entries within a date range.'''
    # Query database
    return [{"id": 1, "date": "2025-10-07", "amount": 50.0}]

if __name__ == "__main__":
    mcp.run()
```

## 🗄️ Database Schema

The SQLite database (`expenses.db`) has the following schema:

```sql
CREATE TABLE IF NOT EXISTS expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    subcategory TEXT DEFAULT '',
    note TEXT DEFAULT ''
);
```

**Fields:**

- `id`: Auto-incrementing unique identifier
- `date`: Expense date (TEXT format: YYYY-MM-DD)
- `amount`: Expense amount (REAL/Float)
- `category`: Main expense category (TEXT)
- `subcategory`: Optional subcategory (TEXT)
- `note`: Optional note/description (TEXT)

## 📂 Categories

The server supports the following expense categories (see `categories.json` for full details):

- **food**: groceries, dining_out, coffee_tea, etc.
- **transport**: fuel, public_transport, parking, etc.
- **housing**: rent, maintenance, repairs, etc.
- **utilities**: electricity, water, internet, etc.
- **health**: medicines, doctor_consultation, fitness_gym, etc.
- **education**: books, courses, online_subscriptions, etc.
- **family_kids**: school_fees, daycare, toys_games, etc.
- **entertainment**: movies_events, streaming_subscriptions, etc.
- **shopping**: clothing, electronics, accessories, etc.
- **subscriptions**: saas_tools, cloud_ai, newsletters, etc.
- **personal_care**: salon_spa, grooming, cosmetics, etc.
- **gifts_donations**: gifts_personal, charity, festivals, etc.
- **finance_fees**: bank_charges, late_fees, interest, etc.
- **business**: software_tools, hosting, marketing, etc.
- **travel**: flights, hotels, visa_passport, etc.
- **home**: household_supplies, cleaning, kitchenware, etc.
- **pet**: food, vet, grooming, supplies, etc.
- **taxes**: income_tax, gst, professional_tax, etc.
- **investments**: mutual_funds, stocks, crypto, etc.
- **misc**: uncategorized, other, etc.

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## 📧 Support

For questions or issues, please open an issue on the GitHub repository.

---

**Built with ❤️ using FastMCP**

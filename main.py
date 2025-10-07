from fastmcp import FastMCP
import os
import sqlite3
from typing import List, Dict, Any

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

mcp = FastMCP("ExpenseTracker")

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        # Expenses table
        c.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Income table
        c.execute("""
            CREATE TABLE IF NOT EXISTS income(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                source TEXT NOT NULL,
                note TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Budget table
        c.execute("""
            CREATE TABLE IF NOT EXISTS budgets(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                monthly_limit REAL NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(category, start_date)
            )
        """)

init_db()

@mcp.tool()
def add_expense(date: str, amount: float, category: str, subcategory: str = "", note: str = ""):
    '''Add a single expense entry to the database.
    
    Args:
        date: Date in YYYY-MM-DD format
        amount: Amount spent
        category: Expense category
        subcategory: Optional subcategory
        note: Optional note or description
    '''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
            (date, amount, category, subcategory, note)
        )
        return {"status": "success", "id": cur.lastrowid, "message": f"Expense added with ID {cur.lastrowid}"}

@mcp.tool()
def add_multiple_expenses(expenses: List[Dict[str, Any]]):
    '''Add multiple expense entries at once.
    
    Args:
        expenses: List of expense dictionaries, each containing:
                  - date (required): Date in YYYY-MM-DD format
                  - amount (required): Amount spent
                  - category (required): Expense category
                  - subcategory (optional): Subcategory
                  - note (optional): Description
    
    Example:
        expenses = [
            {"date": "2025-01-15", "amount": 50.0, "category": "food", "note": "Groceries"},
            {"date": "2025-01-16", "amount": 30.0, "category": "transport", "subcategory": "fuel"}
        ]
    '''
    added_ids = []
    with sqlite3.connect(DB_PATH) as c:
        for exp in expenses:
            cur = c.execute(
                "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
                (
                    exp.get("date"),
                    exp.get("amount"),
                    exp.get("category"),
                    exp.get("subcategory", ""),
                    exp.get("note", "")
                )
            )
            added_ids.append(cur.lastrowid)
    
    return {
        "status": "success",
        "count": len(added_ids),
        "ids": added_ids,
        "message": f"Successfully added {len(added_ids)} expenses"
    }

@mcp.tool()
def add_income(date: str, amount: float, source: str, note: str = ""):
    '''Add an income entry to track earnings.
    
    Args:
        date: Date in YYYY-MM-DD format
        amount: Amount earned
        source: Source of income (e.g., salary, freelance, investment)
        note: Optional note or description
    '''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "INSERT INTO income(date, amount, source, note) VALUES (?,?,?,?)",
            (date, amount, source, note)
        )
        return {"status": "success", "id": cur.lastrowid, "message": f"Income added with ID {cur.lastrowid}"}

@mcp.tool()
def add_multiple_income(income_entries: List[Dict[str, Any]]):
    '''Add multiple income entries at once.
    
    Args:
        income_entries: List of income dictionaries, each containing:
                       - date (required): Date in YYYY-MM-DD format
                       - amount (required): Amount earned
                       - source (required): Income source
                       - note (optional): Description
    '''
    added_ids = []
    with sqlite3.connect(DB_PATH) as c:
        for inc in income_entries:
            cur = c.execute(
                "INSERT INTO income(date, amount, source, note) VALUES (?,?,?,?)",
                (
                    inc.get("date"),
                    inc.get("amount"),
                    inc.get("source"),
                    inc.get("note", "")
                )
            )
            added_ids.append(cur.lastrowid)
    
    return {
        "status": "success",
        "count": len(added_ids),
        "ids": added_ids,
        "message": f"Successfully added {len(added_ids)} income entries"
    }
    
    
@mcp.tool()
def list_expenses(start_date: str, end_date: str):
    '''List expense entries within an inclusive date range.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    '''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE date BETWEEN ? AND ? 
            ORDER BY date DESC, id DESC
            """,
            (start_date, end_date)
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

@mcp.tool()
def list_income(start_date: str, end_date: str):
    '''List income entries within an inclusive date range.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    '''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            """
            SELECT id, date, amount, source, note
            FROM income
            WHERE date BETWEEN ? AND ? 
            ORDER BY date DESC, id DESC
            """,
            (start_date, end_date)
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

@mcp.tool()
def summarize(start_date: str, end_date: str, category: str = None):
    '''Summarize expenses by category within an inclusive date range.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        category: Optional category filter
    '''
    with sqlite3.connect(DB_PATH) as c:
        query = (
            """
            SELECT category, SUM(amount) AS total_amount, COUNT(*) as count
            FROM expenses
            WHERE date BETWEEN ? AND ? 
            """
        )
        params = [start_date, end_date]

        if category:
            query += " AND category = ?"
            params.append(category)

        query += " GROUP BY category ORDER BY total_amount DESC"

        cur = c.execute(query, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

@mcp.tool()
def financial_summary(start_date: str, end_date: str):
    '''Get a comprehensive financial summary showing income, expenses, and balance.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    
    Returns:
        Dictionary containing:
        - total_income: Total income earned
        - total_expenses: Total expenses spent
        - balance: Net balance (income - expenses)
        - income_by_source: Breakdown of income by source
        - expenses_by_category: Breakdown of expenses by category
    '''
    with sqlite3.connect(DB_PATH) as c:
        # Get total income
        cur = c.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM income WHERE date BETWEEN ? AND ?",
            (start_date, end_date)
        )
        total_income = cur.fetchone()[0]
        
        # Get total expenses
        cur = c.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE date BETWEEN ? AND ?",
            (start_date, end_date)
        )
        total_expenses = cur.fetchone()[0]
        
        # Get income by source
        cur = c.execute(
            """
            SELECT source, SUM(amount) as total, COUNT(*) as count
            FROM income
            WHERE date BETWEEN ? AND ?
            GROUP BY source
            ORDER BY total DESC
            """,
            (start_date, end_date)
        )
        income_by_source = [{"source": r[0], "total": r[1], "count": r[2]} for r in cur.fetchall()]
        
        # Get expenses by category
        cur = c.execute(
            """
            SELECT category, SUM(amount) as total, COUNT(*) as count
            FROM expenses
            WHERE date BETWEEN ? AND ?
            GROUP BY category
            ORDER BY total DESC
            """,
            (start_date, end_date)
        )
        expenses_by_category = [{"category": r[0], "total": r[1], "count": r[2]} for r in cur.fetchall()]
        
        return {
            "period": {"start_date": start_date, "end_date": end_date},
            "total_income": round(total_income, 2),
            "total_expenses": round(total_expenses, 2),
            "balance": round(total_income - total_expenses, 2),
            "income_by_source": income_by_source,
            "expenses_by_category": expenses_by_category
        }

@mcp.tool()
def set_budget(category: str, monthly_limit: float, start_date: str, end_date: str = None):
    '''Set or update a budget limit for a category.
    
    Args:
        category: Expense category to budget
        monthly_limit: Maximum amount to spend per month
        start_date: Budget start date in YYYY-MM-DD format
        end_date: Optional budget end date (null for ongoing)
    '''
    with sqlite3.connect(DB_PATH) as c:
        try:
            c.execute(
                """
                INSERT INTO budgets(category, monthly_limit, start_date, end_date)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(category, start_date) 
                DO UPDATE SET monthly_limit = ?, end_date = ?
                """,
                (category, monthly_limit, start_date, end_date, monthly_limit, end_date)
            )
            return {
                "status": "success",
                "message": f"Budget set for {category}: ${monthly_limit}/month starting {start_date}"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

@mcp.tool()
def check_budget(category: str, start_date: str, end_date: str):
    '''Check budget status for a category in a date range.
    
    Args:
        category: Expense category to check
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    
    Returns:
        Budget information including limit, spent amount, remaining, and status
    '''
    with sqlite3.connect(DB_PATH) as c:
        # Get budget limit
        cur = c.execute(
            """
            SELECT monthly_limit, start_date, end_date
            FROM budgets
            WHERE category = ?
            AND start_date <= ?
            AND (end_date IS NULL OR end_date >= ?)
            ORDER BY start_date DESC
            LIMIT 1
            """,
            (category, start_date, start_date)
        )
        budget_row = cur.fetchone()
        
        if not budget_row:
            return {
                "status": "no_budget",
                "category": category,
                "message": f"No budget set for {category}"
            }
        
        budget_limit = budget_row[0]
        
        # Get actual spending
        cur = c.execute(
            """
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
            WHERE category = ?
            AND date BETWEEN ? AND ?
            """,
            (category, start_date, end_date)
        )
        spent = cur.fetchone()[0]
        
        remaining = budget_limit - spent
        percentage = (spent / budget_limit * 100) if budget_limit > 0 else 0
        
        status = "under_budget"
        if spent > budget_limit:
            status = "over_budget"
        elif percentage >= 90:
            status = "warning"
        
        return {
            "status": status,
            "category": category,
            "period": {"start_date": start_date, "end_date": end_date},
            "budget_limit": round(budget_limit, 2),
            "spent": round(spent, 2),
            "remaining": round(remaining, 2),
            "percentage_used": round(percentage, 2)
        }

@mcp.tool()
def list_budgets():
    '''List all active budgets.'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            """
            SELECT category, monthly_limit, start_date, end_date
            FROM budgets
            WHERE end_date IS NULL OR end_date >= date('now')
            ORDER BY category ASC
            """
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

@mcp.tool()
def delete_expense(expense_id: int):
    '''Delete an expense entry by ID.
    
    Args:
        expense_id: ID of the expense to delete
    '''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        if cur.rowcount > 0:
            return {"status": "success", "message": f"Expense {expense_id} deleted"}
        else:
            return {"status": "error", "message": f"Expense {expense_id} not found"}

@mcp.tool()
def delete_income(income_id: int):
    '''Delete an income entry by ID.
    
    Args:
        income_id: ID of the income to delete
    '''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("DELETE FROM income WHERE id = ?", (income_id,))
        if cur.rowcount > 0:
            return {"status": "success", "message": f"Income {income_id} deleted"}
        else:
            return {"status": "error", "message": f"Income {income_id} not found"}

@mcp.tool()
def update_expense(expense_id: int, date: str = None, amount: float = None, 
                   category: str = None, subcategory: str = None, note: str = None):
    '''Update an existing expense entry.
    
    Args:
        expense_id: ID of the expense to update
        date: New date (optional)
        amount: New amount (optional)
        category: New category (optional)
        subcategory: New subcategory (optional)
        note: New note (optional)
    '''
    updates = []
    params = []
    
    if date is not None:
        updates.append("date = ?")
        params.append(date)
    if amount is not None:
        updates.append("amount = ?")
        params.append(amount)
    if category is not None:
        updates.append("category = ?")
        params.append(category)
    if subcategory is not None:
        updates.append("subcategory = ?")
        params.append(subcategory)
    if note is not None:
        updates.append("note = ?")
        params.append(note)
    
    if not updates:
        return {"status": "error", "message": "No fields to update"}
    
    params.append(expense_id)
    query = f"UPDATE expenses SET {', '.join(updates)} WHERE id = ?"
    
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(query, params)
        if cur.rowcount > 0:
            return {"status": "success", "message": f"Expense {expense_id} updated"}
        else:
            return {"status": "error", "message": f"Expense {expense_id} not found"}

@mcp.tool()
def get_spending_trends(start_date: str, end_date: str, group_by: str = "month"):
    '''Analyze spending trends over time.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        group_by: Group by 'day', 'week', or 'month' (default: month)
    
    Returns:
        Spending trends grouped by the specified time period
    '''
    date_format = {
        "day": "%Y-%m-%d",
        "week": "%Y-W%W",
        "month": "%Y-%m"
    }.get(group_by, "%Y-%m")
    
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            f"""
            SELECT 
                strftime('{date_format}', date) as period,
                SUM(amount) as total_spent,
                COUNT(*) as transaction_count,
                AVG(amount) as avg_transaction
            FROM expenses
            WHERE date BETWEEN ? AND ?
            GROUP BY period
            ORDER BY period ASC
            """,
            (start_date, end_date)
        )
        
        results = []
        for row in cur.fetchall():
            results.append({
                "period": row[0],
                "total_spent": round(row[1], 2),
                "transaction_count": row[2],
                "avg_transaction": round(row[3], 2)
            })
        
        return {
            "group_by": group_by,
            "date_range": {"start": start_date, "end": end_date},
            "trends": results
        }

@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    # Read fresh each time so you can edit the file without restarting
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    mcp.run()
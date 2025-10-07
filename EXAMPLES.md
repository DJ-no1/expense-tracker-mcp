# Usage Examples for Expense Tracker MCP Server

## Basic Operations

### Adding Single Expense

```
User: "Add an expense of $45.50 for groceries from the food category on 2025-10-05"

Result: Expense added with ID, categorized under 'food' with subcategory 'groceries'
```

### Adding Multiple Expenses

```
User: "Add these expenses:
- $120 for electricity on October 1st
- $35 for coffee on October 3rd
- $80 for gas on October 5th"

Result: All three expenses added in a single batch operation
```

### Adding Income

```
User: "I received $5000 as salary on October 1st, 2025"

Result: Income entry created with source 'salary'
```

### Adding Multiple Income Entries

```
User: "Record these income entries:
- $5000 salary on October 1st
- $750 freelance payment on October 10th
- $100 interest from savings on October 15th"

Result: All income entries recorded at once
```

## Budget Management

### Setting a Budget

```
User: "Set a monthly budget of $600 for food starting October 2025"

Result: Budget created for 'food' category with $600/month limit
```

### Checking Budget Status

```
User: "How much of my food budget have I used in October?"

Result: Shows:
- Budget limit: $600
- Amount spent: $287.50
- Remaining: $312.50
- Percentage used: 47.92%
- Status: under_budget
```

### Budget Warning (90%+ used)

```
User: "Check my transport budget for October"

Result: Shows:
- Status: warning
- Budget limit: $200
- Amount spent: $185
- Remaining: $15
- Percentage used: 92.5%
```

### Over Budget Alert

```
User: "Check my entertainment budget"

Result: Shows:
- Status: over_budget
- Budget limit: $100
- Amount spent: $125
- Remaining: -$25
- Percentage used: 125%
```

## Financial Analysis

### Monthly Financial Summary

```
User: "Show me my financial summary for October 2025"

Result:
{
  "period": {"start_date": "2025-10-01", "end_date": "2025-10-31"},
  "total_income": 5850.00,
  "total_expenses": 2340.50,
  "balance": 3509.50,
  "income_by_source": [
    {"source": "salary", "total": 5000, "count": 1},
    {"source": "freelance", "total": 750, "count": 1},
    {"source": "interest", "total": 100, "count": 1}
  ],
  "expenses_by_category": [
    {"category": "food", "total": 845.30, "count": 25},
    {"category": "housing", "total": 600, "count": 1},
    {"category": "transport", "total": 320, "count": 12},
    {"category": "utilities", "total": 245, "count": 4},
    {"category": "entertainment", "total": 180, "count": 8}
  ]
}
```

### Spending Trends Analysis

```
User: "Show my spending trends for the last 3 months, grouped by month"

Result: Month-by-month breakdown showing:
- Total spent each month
- Number of transactions
- Average transaction amount
- Trends over time
```

```
User: "Analyze my daily spending in October"

Result: Day-by-day breakdown for detailed analysis
```

### Category Summary

```
User: "Summarize my expenses by category for October 2025"

Result: Lists all categories with:
- Total amount spent
- Number of transactions
- Sorted by highest spending
```

## List and Review

### List Expenses

```
User: "Show me all my expenses in October 2025"

Result: Detailed list of all expenses with dates, amounts, categories, and notes
```

### List Income

```
User: "Show all my income for October 2025"

Result: List of all income entries with sources and amounts
```

### List All Budgets

```
User: "What budgets do I have set up?"

Result: Shows all active budgets with their limits and time periods
```

## Update and Delete

### Update Expense

```
User: "Update expense ID 42 to $55 instead of $50"

Result: Expense updated with new amount
```

### Delete Expense

```
User: "Delete expense with ID 38, I entered it by mistake"

Result: Expense removed from database
```

## Complex Queries

### How Much Did I Earn vs Spend?

```
User: "For January through March 2025, how much did I earn and how much did I spend?"

Result:
- Total Income: $16,500
- Total Expenses: $8,950
- Net Balance: +$7,550
- Savings Rate: 45.8%
```

### Category-Specific Analysis

```
User: "How much have I spent on food this year?"

Result: Shows total food expenses with count and breakdown by subcategories
```

### Budget Performance Review

```
User: "Check all my budgets for October and show which ones I'm over or under"

Result: Comprehensive budget report showing status of each category
```

## Tips for Using with Claude

1. **Be conversational**: Claude understands natural language

   - ✅ "I spent $50 on groceries yesterday"
   - ✅ "Add groceries expense of $50 from yesterday"

2. **Batch operations**: Add multiple entries at once

   - "Add my weekly expenses: coffee $35, gas $80, groceries $150, gym $60"

3. **Date flexibility**: Multiple date formats work

   - "today", "yesterday", "October 5", "2025-10-05", "Oct 5th"

4. **Ask for insights**: Let Claude analyze your data

   - "What's my biggest expense category this month?"
   - "Am I spending more this month than last month?"
   - "Which budgets am I close to exceeding?"

5. **Track goals**: Set and monitor financial goals
   - "I want to save $1000 this month, how am I doing?"
   - "What's my savings rate for the last quarter?"

## Integration in Claude Desktop

After installation, the ExpenseTracker server will be available in Claude Desktop. Simply start asking Claude to track your expenses, income, and budgets naturally in conversation!

Example conversation:

```
You: "I just bought coffee for $5.50"
Claude: *Uses add_expense tool* "I've recorded your coffee expense of $5.50. Would you like me to categorize it under 'food' or 'entertainment'?"

You: "Food category, and can you check my food budget?"
Claude: *Uses check_budget tool* "Your food budget is $500/month. You've spent $287.50 so far (57.5%). You have $212.50 remaining."

You: "Great! How much have I spent total this month?"
Claude: *Uses financial_summary tool* "This month you've spent $1,245 total. Your top categories are Food ($287.50), Transport ($320), and Housing ($600)."
```

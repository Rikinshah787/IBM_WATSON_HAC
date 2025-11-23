import sqlite3
import json
import os

DB_NAME = "orchestrate.db"

def get_db_connection():
    """Helper to get DB connection"""
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row # Allow accessing columns by name
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

class BaseAgent:
    def __init__(self):
        self.name = "Base Agent"

    def execute_query(self, query, params=()):
        """Execute a read-only query and return list of dicts"""
        conn = get_db_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()
            # Convert sqlite3.Row objects to dicts
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"Query Error in {self.name}: {e}")
            return []

class HRAgent(BaseAgent):
    def __init__(self):
        self.name = "HR Agent"
        self.description = "Handles employee data, performance ratings, and satisfaction scores."

    def get_employee_details(self, name=None):
        query = "SELECT * FROM employees"
        params = ()
        if name:
            query += " WHERE name LIKE ?"
            params = (f"%{name}%",)
        return self.execute_query(query, params)

    def get_performance_report(self):
        return self.execute_query("SELECT name, performance_rating, satisfaction_score FROM employees")

class SalesAgent(BaseAgent):
    def __init__(self):
        self.name = "Sales Agent"
        self.description = "Handles sales revenue, deals closed, and regional sales data."

    def get_sales_by_region(self):
        return self.execute_query("""
            SELECT region, SUM(revenue) as total_revenue, SUM(deals_closed) as total_deals 
            FROM sales GROUP BY region
        """)

    def get_sales_by_employee(self, employee_name):
        # Join with employees table to get name
        return self.execute_query("""
            SELECT e.name, SUM(s.revenue) as total_revenue, SUM(s.deals_closed) as total_deals
            FROM sales s
            JOIN employees e ON s.employee_id = e.id
            WHERE e.name LIKE ?
            GROUP BY e.name
        """, (f"%{employee_name}%",))

class CustomerServiceAgent(BaseAgent):
    def __init__(self):
        self.name = "Customer Service Agent"
        self.description = "Handles support tickets, issue categories, and resolution times."

    def get_ticket_stats(self):
        return self.execute_query("""
            SELECT status, COUNT(*) as count, AVG(resolution_time_hours) as avg_resolution_time
            FROM tickets GROUP BY status
        """)
    
    def get_open_tickets(self):
        return self.execute_query("SELECT * FROM tickets WHERE status = 'Open'")

class FinanceAgent(BaseAgent):
    def __init__(self):
        self.name = "Finance Agent"
        self.description = "Handles department expenses, budgets, and financial reporting."

    def get_department_expenses(self):
        return self.execute_query("""
            SELECT department, SUM(expense_amount) as total_expense, SUM(budget_limit) as total_budget
            FROM finance GROUP BY department
        """)

# --- Registry of available agents ---
AGENTS = {
    "hr": HRAgent(),
    "sales": SalesAgent(),
    "service": CustomerServiceAgent(),
    "finance": FinanceAgent()
}

def run_agent_test():
    """Simple test to verify agents work"""
    print("Testing Agents...")
    
    hr = HRAgent()
    print(f"HR Agent found {len(hr.get_employee_details())} employees.")
    
    sales = SalesAgent()
    print(f"Sales Agent found stats for regions: {sales.get_sales_by_region()}")

if __name__ == "__main__":
    run_agent_test()

import sqlite3
import os
from datetime import datetime, timedelta
import random

# Database file path
DB_NAME = "orchestrate.db"

def create_connection():
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        print(f"✅ Connected to SQLite database: {DB_NAME}")
    except sqlite3.Error as e:
        print(f"❌ Error connecting to database: {e}")
    return conn

def create_tables(conn):
    """Create the 4 tables for the agents."""
    cursor = conn.cursor()
    
    # 1. HR Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        role TEXT,
        department TEXT,
        performance_rating TEXT, -- 'Excellent', 'Good', 'Average', 'Poor'
        attendance_score INTEGER, -- 0-100
        satisfaction_score INTEGER -- 0-10
    );
    """)
    
    # 2. Sales Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id TEXT PRIMARY KEY,
        employee_id TEXT,
        region TEXT,
        revenue REAL,
        deals_closed INTEGER,
        date TEXT,
        FOREIGN KEY (employee_id) REFERENCES employees (id)
    );
    """)
    
    # 3. Customer Service Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id TEXT PRIMARY KEY,
        customer_id TEXT,
        assigned_agent_id TEXT,
        issue_category TEXT,
        status TEXT, -- 'Open', 'In Progress', 'Resolved', 'Closed'
        resolution_time_hours REAL,
        created_at TEXT,
        FOREIGN KEY (assigned_agent_id) REFERENCES employees (id)
    );
    """)
    
    # 4. Finance Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS finance (
        id TEXT PRIMARY KEY,
        department TEXT,
        category TEXT, -- 'Salaries', 'Software', 'Travel', 'Marketing'
        expense_amount REAL,
        budget_limit REAL,
        date TEXT
    );
    """)
    
    conn.commit()
    print("✅ Tables created successfully.")

def seed_data(conn):
    """Insert sample data into the tables."""
    cursor = conn.cursor()
    
    # Clear existing data to avoid duplicates on re-run
    cursor.execute("DELETE FROM employees")
    cursor.execute("DELETE FROM sales")
    cursor.execute("DELETE FROM tickets")
    cursor.execute("DELETE FROM finance")
    
    print("🧹 Cleared existing data.")

    # --- 1. Seed Employees (HR) ---
    employees = [
        ("EMP001", "Alice Johnson", "Sales Manager", "Sales", "Excellent", 98, 9),
        ("EMP002", "Bob Smith", "Sales Executive", "Sales", "Average", 92, 7),
        ("EMP003", "Charlie Brown", "Support Agent", "Customer Service", "Good", 95, 8),
        ("EMP004", "Diana Prince", "Support Lead", "Customer Service", "Excellent", 99, 10),
        ("EMP005", "Evan Wright", "Financial Analyst", "Finance", "Good", 96, 8),
    ]
    cursor.executemany("INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?)", employees)
    
    # --- 2. Seed Sales (Sales) ---
    sales_data = []
    regions = ["North", "South", "East", "West"]
    for i in range(1, 21):
        sales_data.append((
            f"SALE{i:03d}",
            random.choice(["EMP001", "EMP002"]), # Only sales employees
            random.choice(regions),
            random.uniform(5000, 50000), # Revenue
            random.randint(1, 5), # Deals closed
            (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
        ))
    cursor.executemany("INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?)", sales_data)

    # --- 3. Seed Tickets (Customer Service) ---
    tickets_data = []
    issues = ["Login Issue", "Billing Error", "Feature Request", "Bug Report"]
    statuses = ["Open", "Resolved", "Closed"]
    for i in range(1, 31):
        tickets_data.append((
            f"TKT{i:03d}",
            f"CUST{random.randint(100, 999)}",
            random.choice(["EMP003", "EMP004"]), # Support agents
            random.choice(issues),
            random.choice(statuses),
            random.uniform(0.5, 48.0), # Resolution time hours
            (datetime.now() - timedelta(days=random.randint(0, 10))).strftime("%Y-%m-%d %H:%M:%S")
        ))
    cursor.executemany("INSERT INTO tickets VALUES (?, ?, ?, ?, ?, ?, ?)", tickets_data)

    # --- 4. Seed Finance (Finance) ---
    finance_data = [
        ("FIN001", "Sales", "Travel", 12000.50, 15000.00, "2023-10-01"),
        ("FIN002", "Sales", "Software", 5000.00, 5000.00, "2023-10-05"),
        ("FIN003", "Customer Service", "Salaries", 45000.00, 45000.00, "2023-10-01"),
        ("FIN004", "Finance", "Audit Tools", 8000.00, 10000.00, "2023-10-10"),
        ("FIN005", "HR", "Recruitment", 3500.00, 5000.00, "2023-10-15"),
    ]
    cursor.executemany("INSERT INTO finance VALUES (?, ?, ?, ?, ?, ?)", finance_data)

    conn.commit()
    print("✅ Sample data seeded successfully.")

def main():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME) # Reset DB for clean state
        
    conn = create_connection()
    if conn:
        create_tables(conn)
        seed_data(conn)
        conn.close()
        print("\n🚀 Database setup complete! 'orchestrate.db' is ready.")

if __name__ == "__main__":
    main()

"""
Script to generate mock CSV data for all sectors
"""

import pandas as pd
import os
from pathlib import Path
from datetime import datetime, timedelta
import random

# Create data directories
data_dir = Path("data")
for sector in ["hr", "sales", "service", "finance"]:
    (data_dir / sector).mkdir(parents=True, exist_ok=True)

print("📁 Creating mock data files...")

# HR Data
print("👥 Creating HR data...")

# Employee data
employees = []
departments = ["Sales", "Engineering", "Support", "Marketing", "Finance", "HR"]
for i in range(100):
    employees.append({
        "employee_id": f"EMP{i+1:04d}",
        "name": f"Employee {i+1}",
        "department": random.choice(departments),
        "position": f"Position {i % 5 + 1}",
        "hire_date": (datetime.now() - timedelta(days=random.randint(30, 1000))).strftime("%Y-%m-%d"),
        "status": random.choice(["Active", "Active", "Active", "Left"]),
        "salary": random.randint(50000, 150000)
    })
pd.DataFrame(employees).to_csv(data_dir / "hr" / "employee_data.csv", index=False)

# Attrition data
attrition = []
for dept in departments:
    for month in range(1, 4):  # Q1-Q3
        attrition.append({
            "department": dept,
            "quarter": f"Q{month}",
            "employees_left": random.randint(2, 8),
            "total_employees": random.randint(80, 120),
            "attrition_rate": round(random.uniform(5.0, 12.0), 1)
        })
pd.DataFrame(attrition).to_csv(data_dir / "hr" / "attrition_data.csv", index=False)

# Satisfaction scores
satisfaction = []
for dept in departments:
    for month in range(1, 4):
        satisfaction.append({
            "department": dept,
            "quarter": f"Q{month}",
            "satisfaction_score": round(random.uniform(6.5, 9.0), 1),
            "response_count": random.randint(20, 50)
        })
pd.DataFrame(satisfaction).to_csv(data_dir / "hr" / "satisfaction_scores.csv", index=False)

# Sales Data
print("💰 Creating Sales data...")

# Pipeline data
pipeline = []
stages = ["Prospecting", "Qualification", "Proposal", "Negotiation", "Closed Won", "Closed Lost"]
for i in range(50):
    pipeline.append({
        "deal_id": f"DEAL-{i+1:04d}",
        "customer_name": f"Customer {i+1}",
        "value": random.randint(10000, 200000),
        "stage": random.choice(stages),
        "probability": random.randint(10, 90),
        "close_date": (datetime.now() + timedelta(days=random.randint(-30, 90))).strftime("%Y-%m-%d"),
        "status": random.choice(["active", "stale", "won", "lost"])
    })
pd.DataFrame(pipeline).to_csv(data_dir / "sales" / "pipeline_data.csv", index=False)

# Deals data
deals = []
for i in range(30):
    deals.append({
        "deal_id": f"DEAL-{i+1:04d}",
        "customer_id": f"CUST{i+1:04d}",
        "customer_name": f"Customer {i+1}",
        "amount": random.randint(20000, 150000),
        "status": random.choice(["won", "lost", "pending"]),
        "close_date": (datetime.now() - timedelta(days=random.randint(1, 180))).strftime("%Y-%m-%d")
    })
pd.DataFrame(deals).to_csv(data_dir / "sales" / "deals_data.csv", index=False)

# Customer data
customers = []
for i in range(40):
    customers.append({
        "customer_id": f"CUST{i+1:04d}",
        "customer_name": f"Customer {i+1}",
        "industry": random.choice(["Tech", "Finance", "Retail", "Healthcare", "Manufacturing"]),
        "revenue": random.randint(1000000, 10000000),
        "performance": random.randint(70, 95)
    })
pd.DataFrame(customers).to_csv(data_dir / "sales" / "customer_data.csv", index=False)

# Customer Service Data
print("🎧 Creating Customer Service data...")

# Tickets data
tickets = []
priorities = ["Low", "Medium", "High", "Critical"]
statuses = ["Open", "In Progress", "Resolved", "Pending"]
for i in range(80):
    customer_id = f"CUST{random.randint(1, 40):04d}"
    tickets.append({
        "ticket_id": f"TICKET-{i+1:04d}",
        "customer_id": customer_id,
        "customer_name": f"Customer {customer_id[-2:]}",
        "subject": f"Issue {i+1}",
        "priority": random.choice(priorities),
        "status": random.choice(statuses),
        "age_days": random.randint(1, 15),
        "created_date": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
    })
pd.DataFrame(tickets).to_csv(data_dir / "service" / "tickets_data.csv", index=False)

# Response times
response_times = []
for month in range(1, 4):
    response_times.append({
        "month": f"Month {month}",
        "avg_response_time_hours": round(random.uniform(1.5, 4.0), 1),
        "tickets_processed": random.randint(200, 300)
    })
pd.DataFrame(response_times).to_csv(data_dir / "service" / "response_times.csv", index=False)

# Escalations
escalations = []
complaint_types = ["Billing", "Technical", "Product", "Support", "Account"]
for i in range(25):
    escalations.append({
        "escalation_id": f"ESC-{i+1:04d}",
        "ticket_id": f"TICKET-{random.randint(1, 80):04d}",
        "type": random.choice(complaint_types),
        "category": random.choice(["urgent", "high", "medium"]),
        "financial_impact": random.randint(500, 5000),
        "cost": random.randint(500, 5000),
        "status": random.choice(["resolved", "pending", "investigating"])
    })
pd.DataFrame(escalations).to_csv(data_dir / "service" / "escalations.csv", index=False)

# Finance Data
print("💵 Creating Finance data...")

# Invoices data
invoices = []
for i in range(60):
    invoices.append({
        "invoice_id": f"INV-{i+1:04d}",
        "vendor": f"Vendor {random.randint(1, 20)}",
        "amount": random.randint(500, 15000),
        "status": random.choice(["pending", "approved", "paid", "rejected"]),
        "due_date": (datetime.now() + timedelta(days=random.randint(-10, 30))).strftime("%Y-%m-%d"),
        "category": random.choice(["Services", "Equipment", "Software", "Consulting"])
    })
pd.DataFrame(invoices).to_csv(data_dir / "finance" / "invoices_data.csv", index=False)

# Budget data
budget = []
departments = ["Sales", "Engineering", "Support", "Marketing", "Finance", "HR"]
for dept in departments:
    for quarter in ["Q1", "Q2", "Q3"]:
        budget.append({
            "department": dept,
            "quarter": quarter,
            "allocated": random.randint(200000, 500000),
            "spent": random.randint(150000, 450000),
            "utilization": round(random.uniform(70, 95), 1)
        })
pd.DataFrame(budget).to_csv(data_dir / "finance" / "budget_data.csv", index=False)

# Cashflow data
cashflow = []
for month in range(1, 10):  # 9 months
    cashflow.append({
        "month": f"Month {month}",
        "cash_flow": random.randint(800000, 1500000),
        "revenue": random.randint(1200000, 2000000),
        "expenses": random.randint(800000, 1200000),
        "amount": random.randint(800000, 1500000)
    })
pd.DataFrame(cashflow).to_csv(data_dir / "finance" / "cashflow_data.csv", index=False)

print("✅ All mock data files created successfully!")
print(f"📁 Data directory: {data_dir.absolute()}")


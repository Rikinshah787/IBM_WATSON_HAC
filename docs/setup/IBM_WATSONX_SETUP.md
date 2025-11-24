# 🏗️ OrchestrateIQ Architecture & Setup

## ✅ Overview
OrchestrateIQ is an intelligent business automation platform that uses **IBM watsonx.ai (Granite Model)** as a "Virtual Orchestrator" to route user queries to specific domain agents (HR, Sales, Service, Finance).

## 🧩 Architecture

### 1. **User Layer**
- **User asks a question** (e.g., "Show me employee performance vs sales results").
- Request goes to **FastAPI Backend**.

### 2. **Virtual Orchestrator (The Brain)**
- **Technology:** IBM watsonx.ai (Granite-3-8b-instruct)
- **Function:**
  - Analyzes user intent.
  - Routes the request to the correct **Agent**.
  - Summarizes the final data into a natural language response.

### 3. **Agent Layer (4 Agents)**
Each agent is a Python class in `backend/agents.py`:
- **HR Agent** → Employee data, attendance, satisfaction.
- **Sales Agent** → Leads, sales data, forecasts.
- **Customer Service Agent** → Tickets, resolutions.
- **Finance Agent** → Reports, expenses, budgets.

### 4. **Data Source Layer**
- **Database:** SQLite (`orchestrate.db`)
- **Tables:** `employees`, `sales`, `tickets`, `finance`
- **Data:** Seeded with realistic mock data via `backend/setup_database.py`.

---

## 🛠️ Setup Instructions

### 1. Environment Variables (`backend/.env`)
Ensure your `.env` file has the correct watsonx.ai credentials:
```env
WATSONX_AI_API_KEY=your_api_key
WATSONX_AI_PROJECT_ID=your_project_id
WATSONX_AI_URL=https://us-south.ml.cloud.ibm.com
WATSONX_AI_MODEL_ID=ibm/granite-3-8b-instruct
```

### 2. Initialize Database
Run this script to create the SQLite database and seed it with data:
```bash
python backend/setup_database.py
```

### 3. Run the Backend
Start the FastAPI server:
```bash
uvicorn backend.app.main:app --reload
```
The API will be available at `http://localhost:8000`.

### 4. Run the Frontend
Start the React frontend:
```bash
cd frontend
npm start
```
The UI will be available at `http://localhost:3000`.

---

## 🧪 Testing the API
You can test the chat endpoint directly:

```bash
curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "How are sales doing in the North region?"}'
```

## 🔄 Flow Example
1. **User:** "How are sales doing?"
2. **Orchestrator:** Calls Granite → Identifies intent "SALES".
3. **Sales Agent:** Queries SQLite `sales` table.
4. **Orchestrator:** Calls Granite with data → Generates summary.
5. **Response:** "Sales in the North region are strong with $45,000 revenue..."

# IBM watsonx Orchestrate Setup Guide

## 🎯 Complete Setup for IBM watsonx Orchestrate Integration

This guide will walk you through setting up IBM watsonx Orchestrate for OrchestrateIQ, including creating skills, building workflows, and configuring the integration.

---

## 📋 Prerequisites

- IBM Cloud account (sign up at https://cloud.ibm.com)
- watsonx Orchestrate instance provisioned
- API keys ready

---

## Step 1: Get Your IBM Cloud Credentials

### 1.1 Get IBM Cloud API Key

1. Go to https://cloud.ibm.com/iam/apikeys
2. Click **"Create an IBM Cloud API key"**
3. Give it a name: `OrchestrateIQ-API-Key`
4. Click **"Create"**
5. **IMPORTANT:** Copy and save the API key immediately (you won't see it again!)
6. This is your `WATSONX_ORCHESTRATE_API_KEY`

### 1.2 Get Project ID

1. Go to https://cloud.ibm.com/watsonx/orchestrate
2. Open your watsonx Orchestrate instance
3. Click on **"Projects"** in the left sidebar
4. Select or create a project (e.g., "OrchestrateIQ")
5. Click on the project name
6. Look for **"Project ID"** in the project settings/details
7. Copy this - it's your `WATSONX_ORCHESTRATE_PROJECT_ID`

### 1.3 Get Instance ID (CRN)

1. Go to https://cloud.ibm.com/resources
2. Find your **watsonx Orchestrate** service instance
3. Click on it
4. In the details page, find **"CRN"** (Cloud Resource Name)
5. Copy the full CRN - it's your `WATSONX_ORCHESTRATE_INSTANCE_ID`
6. Format: `crn:v1:bluemix:public:pm-20:us-south:a/xxxxx:xxxxx::`

### 1.4 Get Service URL

Your URL depends on your region:
- **US South:** `https://us-south.ml.cloud.ibm.com`
- **EU Germany:** `https://eu-de.ml.cloud.ibm.com`
- **UK:** `https://eu-gb.ml.cloud.ibm.com`
- **Japan:** `https://jp-tok.ml.cloud.ibm.com`

---

## Step 2: Configure Your .env File

1. **Copy the example file:**
   ```bash
   cd backend
   copy .env.example .env
   ```

2. **Edit the .env file** with your credentials:
   ```env
   # IBM watsonx Orchestrate Configuration
   WATSONX_ORCHESTRATE_API_KEY=your_actual_api_key_here
   WATSONX_ORCHESTRATE_URL=https://us-south.ml.cloud.ibm.com
   WATSONX_ORCHESTRATE_PROJECT_ID=your_actual_project_id_here
   WATSONX_ORCHESTRATE_INSTANCE_ID=crn:v1:bluemix:public:pm-20:us-south:a/xxxxx
   
   # IBM watsonx.ai Configuration (Optional but recommended)
   WATSONX_AI_API_KEY=your_actual_api_key_here
   WATSONX_AI_URL=https://us-south.ml.cloud.ibm.com
   WATSONX_AI_PROJECT_ID=your_actual_project_id_here
   WATSONX_AI_MODEL_ID=ibm/granite-13b-chat-v2
   
   # Application Configuration
   DEBUG=True
   LOG_LEVEL=INFO
   BACKEND_PORT=8000
   CORS_ORIGINS=http://localhost:3000
   USE_MOCK_MODE=False
   ```

3. **Save the file**

---

## Step 3: Set Up watsonx Orchestrate Skills

### 3.1 Access watsonx Orchestrate

1. Go to https://cloud.ibm.com/watsonx/orchestrate
2. Click on your watsonx Orchestrate instance
3. Click **"Launch watsonx Orchestrate"**

### 3.2 Create Skills for Each Sector

We need to create skills for 4 sectors: **HR, Sales, Customer Service, Finance**

#### HR Skills to Create:

1. **Get Employee Data**
   - Name: `get_employee_data`
   - Description: "Retrieve employee information including performance, attendance, and satisfaction"
   - Input: employee_id (optional)
   - Output: Employee data (JSON)

2. **Approve Leave Request**
   - Name: `approve_leave_request`
   - Description: "Approve or reject employee leave requests"
   - Input: request_id, status (approved/rejected)
   - Output: Approval confirmation

3. **Get Performance Metrics**
   - Name: `get_performance_metrics`
   - Description: "Get employee performance metrics and ratings"
   - Input: employee_id, time_period
   - Output: Performance data

#### Sales Skills to Create:

1. **Get Sales Data**
   - Name: `get_sales_data`
   - Description: "Retrieve sales pipeline, deals, and revenue data"
   - Input: time_period, region (optional)
   - Output: Sales data (JSON)

2. **Update Deal Status**
   - Name: `update_deal_status`
   - Description: "Update the status of a sales deal"
   - Input: deal_id, new_status
   - Output: Update confirmation

3. **Get Revenue Forecast**
   - Name: `get_revenue_forecast`
   - Description: "Get revenue forecasts and predictions"
   - Input: time_period
   - Output: Forecast data

#### Customer Service Skills to Create:

1. **Get Ticket Data**
   - Name: `get_ticket_data`
   - Description: "Retrieve customer support tickets and their status"
   - Input: status (optional), priority (optional)
   - Output: Ticket data (JSON)

2. **Escalate Ticket**
   - Name: `escalate_ticket`
   - Description: "Escalate a support ticket to higher priority"
   - Input: ticket_id, reason
   - Output: Escalation confirmation

3. **Get Customer Satisfaction**
   - Name: `get_customer_satisfaction`
   - Description: "Get customer satisfaction scores and feedback"
   - Input: time_period
   - Output: CSAT data

#### Finance Skills to Create:

1. **Get Financial Data**
   - Name: `get_financial_data`
   - Description: "Retrieve financial metrics, expenses, and budget data"
   - Input: time_period, category (optional)
   - Output: Financial data (JSON)

2. **Approve Expense**
   - Name: `approve_expense`
   - Description: "Approve or reject expense requests"
   - Input: expense_id, status
   - Output: Approval confirmation

3. **Get Budget Status**
   - Name: `get_budget_status`
   - Description: "Get current budget status and utilization"
   - Input: department
   - Output: Budget data

### 3.3 How to Create a Skill in watsonx Orchestrate

1. In watsonx Orchestrate, click **"Skills"** in the left sidebar
2. Click **"Add skill"** or **"Create skill"**
3. Choose **"Custom skill"** or **"API skill"**
4. Fill in the details:
   - **Name:** (e.g., `get_employee_data`)
   - **Description:** (clear description of what it does)
   - **API Endpoint:** `http://localhost:8000/api/v1/orchestrate/execute`
   - **Method:** POST
   - **Headers:** 
     ```json
     {
       "Content-Type": "application/json"
     }
     ```
   - **Request Body:**
     ```json
     {
       "skill_name": "get_employee_data",
       "parameters": {}
     }
     ```
5. Click **"Save"**
6. Repeat for all skills listed above

---

## Step 4: Create Workflows in watsonx Orchestrate

### 4.1 Example Workflow: "Employee Performance Review"

1. Click **"Workflows"** in the left sidebar
2. Click **"Create workflow"**
3. Name it: `Employee Performance Review`
4. Add these steps:
   - **Step 1:** Call `get_employee_data` skill
   - **Step 2:** Call `get_performance_metrics` skill
   - **Step 3:** Analyze data (use AI reasoning)
   - **Step 4:** Generate insights
5. Connect the steps
6. Save the workflow

### 4.2 Example Workflow: "Sales Pipeline Analysis"

1. Create new workflow: `Sales Pipeline Analysis`
2. Add steps:
   - **Step 1:** Call `get_sales_data` skill
   - **Step 2:** Call `get_revenue_forecast` skill
   - **Step 3:** Identify at-risk deals
   - **Step 4:** Generate recommendations
3. Save the workflow

### 4.3 Example Workflow: "Cross-Sector Analysis"

This is the **key differentiator** - analyzing across multiple sectors!

1. Create workflow: `Cross-Sector Business Intelligence`
2. Add steps:
   - **Step 1:** Call `get_employee_data` (HR)
   - **Step 2:** Call `get_sales_data` (Sales)
   - **Step 3:** Call `get_ticket_data` (Customer Service)
   - **Step 4:** Call `get_financial_data` (Finance)
   - **Step 5:** AI Analysis - Find correlations
   - **Step 6:** Generate cross-sector insights
3. Example insights:
   - "Low employee satisfaction in Region X correlates with decreased sales"
   - "High support tickets from customers of Sales Rep Y"
   - "Budget overruns in departments with high turnover"

---

## Step 5: Test the Integration

### 5.1 Start the Backend

```bash
cd backend
uvicorn app.main:app --reload
```

### 5.2 Test Health Endpoint

Open browser: http://localhost:8000/health

You should see:
```json
{
  "status": "healthy",
  "version": "1.1.0",
  "watsonx_orchestrate": "connected"
}
```

### 5.3 Test a Query

```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Show me employee performance metrics",
    "sector": "HR"
  }'
```

### 5.4 Check Logs

Look at `backend/logs/orchestrateiq.log` for detailed debug information.

---

## Step 6: Advanced Configuration

### 6.1 Enable AI Reasoning with watsonx.ai

1. Go to https://cloud.ibm.com/watsonx/ai
2. Create a watsonx.ai project (or use existing)
3. Get the Project ID
4. Add to your `.env`:
   ```env
   WATSONX_AI_API_KEY=your_api_key
   WATSONX_AI_PROJECT_ID=your_project_id
   WATSONX_AI_MODEL_ID=ibm/granite-13b-chat-v2
   ```

### 6.2 Configure Granite Model

The recommended model is **IBM Granite 13B Chat v2**:
- Good balance of performance and speed
- Optimized for business use cases
- Supports complex reasoning

Alternative models:
- `ibm/granite-13b-instruct-v2` - For instruction-following
- `ibm/granite-20b-multilingual` - For multilingual support

---

## Step 7: Create Your Graph/Workflow Diagram

### 7.1 Workflow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Query (Natural Language)            │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              Intent Recognition (AI)                         │
│  - Identify sector (HR/Sales/Service/Finance)               │
│  - Identify action (query/analyze/approve/alert)            │
│  - Extract parameters                                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│           watsonx Orchestrate Skill Selection                │
│  - Select appropriate skills based on intent                 │
│  - Prepare skill parameters                                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┬─────────────┐
        ▼             ▼             ▼             ▼
    ┌───────┐    ┌────────┐    ┌─────────┐   ┌─────────┐
    │  HR   │    │ Sales  │    │ Service │   │ Finance │
    │ Skills│    │ Skills │    │ Skills  │   │ Skills  │
    └───┬───┘    └────┬───┘    └────┬────┘   └────┬────┘
        │             │              │             │
        └─────────────┼──────────────┼─────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              Data Aggregation & Processing                   │
│  - Combine data from multiple skills                         │
│  - Normalize and structure data                              │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│         AI Analysis (watsonx.ai Granite Model)               │
│  - Cross-sector correlation analysis                         │
│  - Pattern recognition                                       │
│  - Insight generation                                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              Action Orchestration                            │
│  - Auto-approvals                                            │
│  - Alert generation                                          │
│  - Task assignments                                          │
│  - Workflow triggers                                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│           Response Generation & Visualization                │
│  - Format insights                                           │
│  - Create visualizations                                     │
│  - Return to user                                            │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 Example Flow: "Show me employees with low performance"

1. **User Query:** "Show me employees with low performance"
2. **Intent Recognition:** 
   - Sector: HR
   - Action: Query
   - Entity: Employees
   - Filter: Low performance
3. **Skill Selection:** `get_employee_data`, `get_performance_metrics`
4. **Execution:** Call both skills via watsonx Orchestrate
5. **Data Processing:** Filter employees with performance < 3.0
6. **AI Analysis:** Identify patterns (e.g., correlation with tenure, department)
7. **Action:** Generate alert for HR manager
8. **Response:** Return list of employees + insights + recommended actions

---

## Step 8: Verify Everything Works

### Checklist:

- [ ] IBM Cloud API key obtained
- [ ] watsonx Orchestrate project created
- [ ] Project ID and Instance ID copied
- [ ] `.env` file configured with all credentials
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Skills created in watsonx Orchestrate (at least 3-4 for testing)
- [ ] Workflows created (at least 1 cross-sector workflow)
- [ ] Backend server starts without errors
- [ ] Health endpoint returns "connected" status
- [ ] Test query returns valid response
- [ ] Logs show successful API calls to watsonx

---

## 🎯 Quick Start Commands

```bash
# 1. Install backend dependencies
cd backend
pip install -r requirements.txt

# 2. Configure environment
copy .env.example .env
# Edit .env with your credentials

# 3. Generate mock data (optional, for testing)
python create_mock_data.py

# 4. Start backend
uvicorn app.main:app --reload

# 5. In a new terminal, start frontend
cd frontend
npm install
npm start

# 6. Open browser
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/docs
```

---

## 🔧 Troubleshooting

### Issue: "Authentication failed"
- **Solution:** Verify your API key is correct and has proper permissions

### Issue: "Project not found"
- **Solution:** Double-check your Project ID in the watsonx Orchestrate UI

### Issue: "Skills not found"
- **Solution:** Ensure skills are created and published in watsonx Orchestrate

### Issue: "Connection timeout"
- **Solution:** Check your network, firewall, and ensure the URL is correct for your region

### Issue: "Mock mode is active"
- **Solution:** Set `USE_MOCK_MODE=False` in `.env` and verify credentials are correct

---

## 📚 Additional Resources

- [IBM watsonx Orchestrate Documentation](https://www.ibm.com/docs/en/watsonx/orchestrate)
- [IBM watsonx.ai Documentation](https://www.ibm.com/docs/en/watsonx-as-a-service)
- [IBM Cloud API Keys](https://cloud.ibm.com/docs/account?topic=account-userapikey)
- [Granite Models Guide](https://www.ibm.com/products/watsonx-ai/foundation-models)

---

## 🎉 You're All Set!

Once everything is configured, you'll have:
- ✅ Full watsonx Orchestrate integration
- ✅ AI-powered cross-sector analysis
- ✅ Automated workflow orchestration
- ✅ Real-time insights and actions
- ✅ Beautiful UI with dual themes

**Need help?** Check the logs in `backend/logs/` or refer to [DEBUG.md](DEBUG.md)

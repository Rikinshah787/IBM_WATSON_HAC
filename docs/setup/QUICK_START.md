# 🚀 Quick Setup Reference Card

## ⚡ Super Quick Start (5 Minutes)

### 1️⃣ Get Your IBM Credentials (2 min)

**API Key:**
- Go to: https://cloud.ibm.com/iam/apikeys
- Click "Create an IBM Cloud API key"
- Copy and save it!

**Project ID:**
- Go to: https://cloud.ibm.com/watsonx/orchestrate
- Open your project → Copy the Project ID

**Instance ID (CRN):**
- Go to: https://cloud.ibm.com/resources
- Find watsonx Orchestrate → Copy the CRN

### 2️⃣ Configure .env File (1 min)

```bash
cd backend
copy .env.example .env
```

Edit `.env` and paste your credentials:
```env
WATSONX_ORCHESTRATE_API_KEY=paste_your_api_key_here
WATSONX_ORCHESTRATE_URL=https://us-south.ml.cloud.ibm.com
WATSONX_ORCHESTRATE_PROJECT_ID=paste_your_project_id_here
WATSONX_ORCHESTRATE_INSTANCE_ID=paste_your_crn_here

WATSONX_AI_API_KEY=paste_your_api_key_here
WATSONX_AI_URL=https://us-south.ml.cloud.ibm.com
WATSONX_AI_PROJECT_ID=paste_your_project_id_here
WATSONX_AI_MODEL_ID=ibm/granite-13b-chat-v2

DEBUG=True
USE_MOCK_MODE=False
```

### 3️⃣ Run the Application (2 min)

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

**Open Browser:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs

---

## 🎯 Essential Skills to Create in watsonx Orchestrate

Go to: https://cloud.ibm.com/watsonx/orchestrate → Skills → Create

### HR Skills (3 minimum)
1. **get_employee_data** - Get employee info
2. **get_performance_metrics** - Get performance data
3. **approve_leave_request** - Approve/reject leave

### Sales Skills (3 minimum)
1. **get_sales_data** - Get sales pipeline
2. **update_deal_status** - Update deal status
3. **get_revenue_forecast** - Get forecasts

### Customer Service Skills (3 minimum)
1. **get_ticket_data** - Get support tickets
2. **escalate_ticket** - Escalate tickets
3. **get_customer_satisfaction** - Get CSAT scores

### Finance Skills (3 minimum)
1. **get_financial_data** - Get financial metrics
2. **approve_expense** - Approve expenses
3. **get_budget_status** - Get budget status

---

## 📊 Create Your First Workflow

### Example: "Employee Performance Review"

1. Go to watsonx Orchestrate → Workflows → Create
2. Name: `Employee Performance Review`
3. Add steps:
   - Step 1: Call `get_employee_data`
   - Step 2: Call `get_performance_metrics`
   - Step 3: AI Analysis (use Granite model)
   - Step 4: Generate insights
4. Save and publish

### Example: "Cross-Sector Analysis" (The Key Feature!)

1. Create workflow: `Cross-Sector Intelligence`
2. Add steps:
   - Step 1: `get_employee_data` (HR)
   - Step 2: `get_sales_data` (Sales)
   - Step 3: `get_ticket_data` (Service)
   - Step 4: `get_financial_data` (Finance)
   - Step 5: AI finds correlations
   - Step 6: Generate cross-sector insights
3. Save and publish

---

## 🔍 Test Your Setup

### Test 1: Health Check
```bash
curl http://localhost:8000/health
```
Should return: `{"status": "healthy", "watsonx_orchestrate": "connected"}`

### Test 2: Simple Query
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me employee performance", "sector": "HR"}'
```

### Test 3: Frontend
- Open: http://localhost:3000
- Type: "Show me sales pipeline"
- Should see results!

---

## 🎨 Your Workflow Graph

```
User Query
    ↓
AI Intent Recognition
    ↓
Skill Selection
    ↓
┌───────┬────────┬─────────┬─────────┐
│  HR   │ Sales  │ Service │ Finance │
└───┬───┴────┬───┴────┬────┴────┬────┘
    └────────┴────────┴─────────┘
              ↓
    Data Aggregation
              ↓
    AI Analysis (Granite)
              ↓
    Cross-Sector Insights
              ↓
    Actions & Alerts
              ↓
    Beautiful UI Response
```

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "Authentication failed" | Check API key in `.env` |
| "Project not found" | Verify Project ID is correct |
| "Skills not found" | Create skills in watsonx Orchestrate |
| Backend won't start | Check if port 8000 is free |
| Frontend won't start | Check if port 3000 is free |
| "Mock mode active" | Set `USE_MOCK_MODE=False` in `.env` |

---

## 📁 Important Files

- `backend/.env` - Your credentials (NEVER commit this!)
- `backend/.env.example` - Template for credentials
- `IBM_WATSONX_SETUP.md` - Full detailed setup guide
- `backend/logs/orchestrateiq.log` - Debug logs

---

## 🎯 Your Checklist

- [ ] ✅ Dependencies installed (`pip install -r requirements.txt`)
- [ ] ✅ IBM Cloud API key obtained
- [ ] ✅ Project ID and Instance ID copied
- [ ] ✅ `.env` file configured
- [ ] ✅ At least 3 skills created per sector in watsonx Orchestrate
- [ ] ✅ At least 1 cross-sector workflow created
- [ ] ✅ Backend starts successfully
- [ ] ✅ Frontend starts successfully
- [ ] ✅ Health check returns "connected"
- [ ] ✅ Test query works

---

## 🚀 Next Steps

1. **Create more skills** in watsonx Orchestrate
2. **Build complex workflows** with multiple steps
3. **Test cross-sector queries** like:
   - "Which sales reps have customers with high support tickets?"
   - "Show correlation between employee satisfaction and sales performance"
   - "Find departments with budget overruns and high turnover"
4. **Customize the UI** themes (Galaxy Dark / Antigravity Light)
5. **Deploy to production** (see DEPLOYMENT.md)

---

## 📚 Full Documentation

- **IBM_WATSONX_SETUP.md** - Complete setup guide (READ THIS!)
- **SETUP.md** - General setup instructions
- **API.md** - API documentation
- **DEBUG.md** - Debugging guide
- **DEPLOYMENT.md** - Deployment instructions

---

## 💡 Pro Tips

1. **Start with mock mode** to test the UI, then switch to real API
2. **Check logs** in `backend/logs/` for debugging
3. **Use Granite models** for best performance
4. **Create cross-sector workflows** - that's the unique value!
5. **Test incrementally** - one skill at a time

---

**Need Help?** 
- Check logs: `backend/logs/orchestrateiq.log`
- Read: `IBM_WATSONX_SETUP.md`
- IBM Docs: https://www.ibm.com/docs/en/watsonx/orchestrate

**You're ready to orchestrate! 🎉**

# Testing Guide

Guide for testing OrchestrateIQ end-to-end.

## Quick Test

### 1. Start Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python create_mock_data.py
uvicorn app.main:app --reload
```

### 2. Start Frontend

```bash
cd frontend
npm install
npm start
```

### 3. Test End-to-End Flow

1. **Open Browser**: Navigate to `http://localhost:3000`

2. **Test Dashboard**: Verify all 4 sector cards load with data

3. **Test Chat Interface**: Try these queries:

   **HR Query:**
   ```
   Show me attrition trends this quarter and which departments are at risk
   ```

   **Sales Query:**
   ```
   Analyze our Q3 pipeline and flag deals that need immediate attention
   ```

   **Cross-Sector Query:**
   ```
   What's the correlation between employee satisfaction scores and sales performance?
   ```

   **Finance Query:**
   ```
   Review pending invoices and approve those under $5K automatically
   ```

4. **Verify Actions**: Check that actions are triggered (approvals, alerts, etc.)

5. **Check Logs**: Review `backend/logs/orchestrateiq.log` for debug information

## API Testing

### Using curl

```bash
# Health check
curl http://localhost:8000/health

# Process query
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me attrition trends", "sector": "hr"}'

# Get dashboard data
curl http://localhost:8000/api/v1/dashboard/hr
```

### Using Swagger UI

Visit `http://localhost:8000/docs` for interactive API documentation.

## Expected Results

### Query Response Should Include:
- ✅ Detected intent
- ✅ Involved sectors
- ✅ Insights (at least 1)
- ✅ Actions (when applicable)
- ✅ Response text
- ✅ Execution time

### Dashboard Data Should Include:
- ✅ Metrics (2+ metrics per sector)
- ✅ Trends (3+ data points)
- ✅ Alerts (when applicable)

### UI Should Show:
- ✅ All 4 sector cards
- ✅ Theme toggle works
- ✅ Chat interface functional
- ✅ Visualizations render
- ✅ Responsive design

## Troubleshooting

If tests fail:

1. **Backend not responding**: Check if server is running on port 8000
2. **Frontend errors**: Check browser console for errors
3. **No data**: Verify mock data files exist in `backend/data/`
4. **API errors**: Check `backend/logs/` for error details

## Performance Testing

Expected performance:
- Query processing: < 2 seconds
- Dashboard load: < 1 second
- API response time: < 500ms

## Success Criteria

✅ All 8+ use cases work
✅ Cross-sector queries work
✅ Actions are triggered
✅ Dashboard updates in real-time
✅ UI is responsive and beautiful
✅ Logs are comprehensive
✅ No critical errors


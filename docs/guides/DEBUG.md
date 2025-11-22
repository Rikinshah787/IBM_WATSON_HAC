# Debug Guide

Comprehensive guide for debugging OrchestrateIQ.

## Logging System

OrchestrateIQ uses a comprehensive logging system with multiple log levels and outputs.

### Log Locations

- **Console**: Real-time logs in terminal
- **orchestrateiq.log**: Main application log (JSON format)
- **debug.log**: Detailed debug log (JSON format)

Log files are located in `backend/logs/` directory.

### Log Levels

- **DEBUG**: Detailed information for debugging
- **INFO**: General informational messages
- **WARNING**: Warning messages
- **ERROR**: Error messages
- **CRITICAL**: Critical errors

### Configuring Log Level

Set in `.env` file:

```env
LOG_LEVEL=DEBUG  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## Debug Logging Points

### Backend Debug Points

1. **Agent Initialization**
   - Location: `backend/app/orchestrate/agent.py`
   - Logs: Agent initialization, API connection status

2. **Workflow Execution**
   - Location: `backend/app/orchestrate/workflows.py`
   - Logs: Intent recognition, workflow steps, data processing

3. **Digital Skills**
   - Location: `backend/app/orchestrate/skills.py`
   - Logs: Skill execution, data retrieval, API calls

4. **Data Processing**
   - Location: `backend/app/data/*.py`
   - Logs: Data analysis, metric calculation, insight generation

5. **API Requests**
   - Location: `backend/app/api/routes.py`
   - Logs: Request/response logging, error handling

### Frontend Debug Points

1. **API Calls**
   - Location: `frontend/src/services/api.js`
   - Logs: Request/response in browser console

2. **Component State**
   - Location: All React components
   - Logs: Component lifecycle, state changes

## Common Debug Scenarios

### 1. Agent Not Initializing

**Symptoms:**
- Health check returns "not_initialized"
- Logs show initialization errors

**Debug Steps:**
1. Check `.env` file for correct credentials
2. Verify API key format
3. Check network connectivity
4. Review `logs/orchestrateiq.log` for detailed errors

**Example Log:**
```
❌ Failed to initialize agent: Invalid API key
```

### 2. Query Processing Fails

**Symptoms:**
- API returns 500 error
- No response from agent

**Debug Steps:**
1. Check query format in request
2. Verify data files exist in `backend/data/`
3. Review workflow execution logs
4. Check for missing dependencies

**Example Log:**
```
❌ Query processing failed: Data file not found: data/hr/attrition_data.csv
```

### 3. Frontend Not Connecting

**Symptoms:**
- Frontend shows connection errors
- API calls fail

**Debug Steps:**
1. Verify backend is running on correct port
2. Check CORS configuration
3. Verify `REACT_APP_API_URL` in frontend `.env`
4. Check browser console for errors

### 4. Mock Data Issues

**Symptoms:**
- Empty or missing data
- Incorrect data format

**Debug Steps:**
1. Regenerate mock data: `python backend/create_mock_data.py`
2. Verify CSV files exist and are readable
3. Check data format matches expected schema

## Enabling Verbose Debugging

### Backend

Set in `.env`:
```env
DEBUG=True
LOG_LEVEL=DEBUG
```

### Frontend

Enable in browser console:
```javascript
localStorage.setItem('debug', 'true');
```

## Debug Dashboard

Access debug information via:

- **Health Endpoint**: `http://localhost:8000/health`
- **API Docs**: `http://localhost:8000/docs` (Swagger UI)

## Performance Debugging

### Backend Performance

Check execution times in logs:
```
✅ Query processed successfully in 1.23s
```

### Frontend Performance

Use browser DevTools:
- Network tab: API call timing
- Performance tab: Component render times

## Troubleshooting Checklist

- [ ] Backend server is running
- [ ] Frontend server is running
- [ ] Environment variables are set correctly
- [ ] Mock data files exist
- [ ] Logs directory is writable
- [ ] No port conflicts
- [ ] Dependencies are installed
- [ ] API credentials are valid (if using real watsonx)

## Getting Help

If issues persist:

1. Check logs in `backend/logs/`
2. Review error messages in console
3. Verify all setup steps in [SETUP.md](SETUP.md)
4. Check [API.md](API.md) for endpoint documentation


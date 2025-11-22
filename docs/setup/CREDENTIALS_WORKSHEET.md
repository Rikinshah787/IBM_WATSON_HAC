# 🔑 IBM watsonx Credentials Worksheet

Fill this out as you gather your credentials, then copy to `.env` file.

---

## Step 1: IBM Cloud API Key

**Where to get it:** https://cloud.ibm.com/iam/apikeys

1. Click "Create an IBM Cloud API key"
2. Name: `OrchestrateIQ-API-Key`
3. Copy the key immediately (you won't see it again!)

**Your API Key:**
```
WATSONX_ORCHESTRATE_API_KEY=_______________________________________________
```

---

## Step 2: watsonx Orchestrate Project ID

**Where to get it:** https://cloud.ibm.com/watsonx/orchestrate

1. Open your watsonx Orchestrate instance
2. Click "Projects" → Select/Create project
3. Copy the Project ID from project settings

**Your Project ID:**
```
WATSONX_ORCHESTRATE_PROJECT_ID=_______________________________________________
```

---

## Step 3: watsonx Orchestrate Instance ID (CRN)

**Where to get it:** https://cloud.ibm.com/resources

1. Find your watsonx Orchestrate service
2. Click on it
3. Copy the CRN (Cloud Resource Name)

**Your Instance ID:**
```
WATSONX_ORCHESTRATE_INSTANCE_ID=crn:v1:bluemix:public:pm-20:____________
```

---

## Step 4: Service URL (Region)

**Select your region:**

- [ ] US South: `https://us-south.ml.cloud.ibm.com`
- [ ] EU Germany: `https://eu-de.ml.cloud.ibm.com`
- [ ] UK: `https://eu-gb.ml.cloud.ibm.com`
- [ ] Japan: `https://jp-tok.ml.cloud.ibm.com`

**Your URL:**
```
WATSONX_ORCHESTRATE_URL=_______________________________________________
```

---

## Step 5: watsonx.ai Configuration (Optional but Recommended)

**Same as above, or separate project:**

**Your watsonx.ai API Key:**
```
WATSONX_AI_API_KEY=_______________________________________________
```

**Your watsonx.ai Project ID:**
```
WATSONX_AI_PROJECT_ID=_______________________________________________
```

**Your watsonx.ai URL:**
```
WATSONX_AI_URL=_______________________________________________
```

**Model to use:** (recommended)
```
WATSONX_AI_MODEL_ID=ibm/granite-13b-chat-v2
```

---

## Complete .env File Template

Once you've filled in all the above, copy this to `backend/.env`:

```env
# ============================================
# IBM watsonx Orchestrate Configuration
# ============================================
WATSONX_ORCHESTRATE_API_KEY=paste_your_api_key_here
WATSONX_ORCHESTRATE_URL=https://us-south.ml.cloud.ibm.com
WATSONX_ORCHESTRATE_PROJECT_ID=paste_your_project_id_here
WATSONX_ORCHESTRATE_INSTANCE_ID=paste_your_crn_here

# ============================================
# IBM watsonx.ai Configuration
# ============================================
WATSONX_AI_API_KEY=paste_your_api_key_here
WATSONX_AI_URL=https://us-south.ml.cloud.ibm.com
WATSONX_AI_PROJECT_ID=paste_your_project_id_here
WATSONX_AI_MODEL_ID=ibm/granite-13b-chat-v2

# ============================================
# Application Configuration
# ============================================
DEBUG=True
LOG_LEVEL=INFO
BACKEND_PORT=8000
CORS_ORIGINS=http://localhost:3000
USE_MOCK_MODE=False
REQUEST_TIMEOUT=30
MAX_RETRIES=3
ENABLE_API_LOGGING=True
```

---

## Verification Checklist

- [ ] API Key copied and pasted
- [ ] Project ID copied and pasted
- [ ] Instance ID (CRN) copied and pasted
- [ ] Correct region URL selected
- [ ] watsonx.ai credentials added (optional)
- [ ] `.env` file created in `backend/` directory
- [ ] All credentials pasted into `.env`
- [ ] No extra spaces or quotes around values
- [ ] File saved

---

## Quick Test

After filling in your `.env` file:

```bash
cd backend
uvicorn app.main:app --reload
```

Then open: http://localhost:8000/health

You should see:
```json
{
  "status": "healthy",
  "watsonx_orchestrate": "connected"
}
```

If you see "connected" - you're all set! 🎉

If you see "disconnected" or errors:
1. Check your API key is correct
2. Check your Project ID is correct
3. Check your Instance ID (CRN) is correct
4. Check the logs in `backend/logs/orchestrateiq.log`

---

## Security Notes

⚠️ **IMPORTANT:**
- **NEVER** commit `.env` file to git
- **NEVER** share your API keys publicly
- `.env` is already in `.gitignore`
- Keep your credentials secure

---

## Need Help?

- **Full Setup Guide:** See `IBM_WATSONX_SETUP.md`
- **Quick Start:** See `QUICK_START.md`
- **Troubleshooting:** See `DEBUG.md`
- **IBM Docs:** https://www.ibm.com/docs/en/watsonx/orchestrate

---

**Once complete, you're ready to orchestrate! 🚀**

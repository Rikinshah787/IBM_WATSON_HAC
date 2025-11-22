# Setup Guide

This guide will help you set up OrchestrateIQ on your local machine.

## Prerequisites

- Python 3.9 or higher
- Node.js 16+ and npm
- IBM watsonx Orchestrate API credentials
- IBM watsonx.ai API credentials (optional but recommended)

## Backend Setup

### 1. Navigate to backend directory

```bash
cd backend
```

### 2. Create virtual environment (recommended)

```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

**Installation Notes:**
- **Expected time:** 2-3 minutes (optimized to exclude unused packages)
- **pandas is optional:** The code automatically falls back to Python's built-in `csv` module if pandas is not installed
- **If you have pandas globally:** You can use it without installing via requirements.txt
- **Optimized packages:** Removed unused heavy dependencies (`ibm-watson-machine-learning`, `ibm-cloud-sdk-core`, `openpyxl`) for faster installation

### 4. Configure environment variables

Copy the example environment file:

```bash
copy .env.example .env
```

**Linux/Mac:**
```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
# IBM watsonx Orchestrate Configuration
WATSONX_ORCHESTRATE_API_KEY=your_api_key_here
WATSONX_ORCHESTRATE_URL=https://api.watsonx.orchestrate.cloud.ibm.com
WATSONX_ORCHESTRATE_PROJECT_ID=your_project_id_here

# IBM watsonx.ai Configuration (Optional)
WATSONX_AI_API_KEY=your_watsonx_ai_api_key_here
WATSONX_AI_URL=https://us-south.ml.cloud.ibm.com
WATSONX_AI_PROJECT_ID=your_watsonx_ai_project_id_here

# Application Configuration
DEBUG=True
LOG_LEVEL=INFO
BACKEND_PORT=8000
CORS_ORIGINS=http://localhost:3000
```

### 5. Generate mock data (if not already created)

```bash
python create_mock_data.py
```

### 6. Run the backend server

```bash
uvicorn app.main:app --reload
```

The backend will be available at `http://localhost:8000`

## Frontend Setup

### 1. Navigate to frontend directory

```bash
cd frontend
```

### 2. Install dependencies

```bash
npm install
```

### 3. Configure API URL (if needed)

Create a `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:8000/api/v1
```

### 4. Run the frontend

```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## Verification

1. Backend health check: Visit `http://localhost:8000/health`
2. Frontend: Visit `http://localhost:3000`
3. Check logs in `backend/logs/` directory for debug information

## Troubleshooting

### Backend Issues

- **Port already in use**: Change `BACKEND_PORT` in `.env`
- **Import errors**: Ensure virtual environment is activated
- **Missing data files**: Run `python create_mock_data.py`
- **Slow installation (>10 minutes)**: Cancel (Ctrl+C) and check internet connection. The optimized requirements should install in 2-3 minutes.
- **pandas import warnings**: This is normal - the code will use built-in `csv` module if pandas is not available

### Frontend Issues

- **API connection errors**: Verify backend is running and `REACT_APP_API_URL` is correct
- **Build errors**: Delete `node_modules` and run `npm install` again

### watsonx Orchestrate Issues

- **API key errors**: Verify credentials in `.env` file
- **Connection errors**: Check network connectivity and API URL
- **Mock mode**: If credentials are missing, the system will run in mock mode

## Next Steps

- Read [API.md](API.md) for API documentation
- Read [DEBUG.md](DEBUG.md) for debugging guide
- Read [DEPLOYMENT.md](DEPLOYMENT.md) for deployment instructions


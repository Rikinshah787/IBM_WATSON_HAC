# OrchestrateIQ - AI-Powered Business Command Center

An intelligent AI agent solution using IBM watsonx Orchestrate to orchestrate workflows across HR, Sales, Customer Service, and Finance sectors. This solution demonstrates cross-sector intelligence, proactive orchestration, and actionable automation.

## 🎯 Unique Value Proposition

**OrchestrateIQ** is not just a dashboard—it's an intelligent orchestrator that:
- Identifies cross-sector relationships and patterns
- Proactively triggers workflows and automates actions
- Handles complex, multi-sector queries in natural language
- Automates approvals, routing, and coordination across systems

## 🏗️ Architecture

- **Backend**: Python FastAPI with watsonx Orchestrate integration
- **Frontend**: React.js with beautiful dual themes (Galaxy Dark / Antigravity Light)
- **AI**: IBM watsonx Orchestrate + watsonx.ai (Granite models)
- **Data**: Mock CSV/Excel datasets for demonstration

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- IBM watsonx Orchestrate API credentials
- IBM watsonx.ai API credentials (optional)

### Installation

1. **Backend Setup**:
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Add your watsonx credentials to .env
```

2. **Frontend Setup**:
```bash
cd frontend
npm install
```

3. **Run Backend**:
```bash
cd backend
uvicorn app.main:app --reload
```

4. **Run Frontend**:
```bash
cd frontend
npm start
```

## 📊 Features

- **8+ Use Cases** across 4 sectors
- **Cross-Sector Analysis** - Identify relationships between sectors
- **Action Automation** - Auto-approvals, alerts, task assignments
- **Beautiful UI** - Galaxy dark theme and Antigravity light theme
- **Real-time Updates** - Live dashboard updates
- **Comprehensive Logging** - Debug logs at every stage

## 📚 Documentation

- [SETUP.md](SETUP.md) - Detailed setup instructions
- [API.md](API.md) - API documentation
- [DEBUG.md](DEBUG.md) - Debug logging guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment instructions
- [VERSIONING.md](VERSIONING.md) - Version management guide
- [CHANGELOG.md](CHANGELOG.md) - Version history and changes

## ⚠️ Important Notes

**Prohibited Models** (Do NOT use):
- llama-3-405b-instruct
- mistral-medium-2505
- mistral-small-3-1-24b-instruct-2503

**Approved Models**:
- IBM Granite models (via watsonx.ai)
- Models available through watsonx Orchestrate

## 📁 Project Structure

```
IBMWATSON/
├── backend/          # FastAPI backend
├── frontend/         # React frontend
├── docs/            # Documentation
└── README.md        # This file
```

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## 📝 License

This project is created for IBM watsonx Orchestrate Hackathon.


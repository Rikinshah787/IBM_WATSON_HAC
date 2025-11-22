# API Documentation

OrchestrateIQ REST API documentation.

## Base URL

```
http://localhost:8000/api/v1
```

## Endpoints

### Health Check

**GET** `/health`

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "agent": "initialized",
  "timestamp": "2024-01-01 12:00:00"
}
```

### Process Query

**POST** `/query`

Process a natural language query through the AI agent.

**Request Body:**
```json
{
  "query": "Show me attrition trends this quarter and which departments are at risk",
  "sector": "hr",
  "context": {}
}
```

**Response:**
```json
{
  "query": "Show me attrition trends...",
  "intent": "analyze_attrition",
  "sectors": ["hr"],
  "insights": [
    {
      "title": "Attrition Trend Analysis",
      "description": "Attrition rate is 8.5% this quarter",
      "sector": "hr",
      "confidence": 0.9,
      "data": {...}
    }
  ],
  "actions": [
    {
      "action_type": "generate_retention_plan",
      "target": "departments: Sales, Support",
      "parameters": {...},
      "status": "completed"
    }
  ],
  "data": {...},
  "response_text": "I found 1 key insight(s): ...",
  "execution_time": 1.23,
  "timestamp": "2024-01-01T12:00:00"
}
```

### Get Dashboard Data

**GET** `/dashboard/{sector}`

Get dashboard data for a specific sector.

**Path Parameters:**
- `sector`: One of `hr`, `sales`, `service`, `finance`

**Response:**
```json
{
  "sector": "hr",
  "metrics": {
    "total_employees": 1250,
    "attrition_rate": 8.5,
    "satisfaction_score": 7.8
  },
  "trends": [
    {
      "period": "Q1",
      "attrition": 6.2,
      "satisfaction": 7.5
    }
  ],
  "alerts": [
    {
      "type": "high_attrition",
      "department": "Sales",
      "severity": "high"
    }
  ],
  "last_updated": "2024-01-01T12:00:00"
}
```

### Get Sectors

**GET** `/sectors`

Get list of available sectors.

**Response:**
```json
["hr", "sales", "service", "finance"]
```

## Example Queries

### HR Queries

1. **Attrition Analysis**
```json
{
  "query": "Show me attrition trends this quarter and which departments are at risk",
  "sector": "hr"
}
```

2. **Satisfaction-Sales Correlation**
```json
{
  "query": "What's the correlation between employee satisfaction scores and sales performance?"
}
```

### Sales Queries

1. **Pipeline Analysis**
```json
{
  "query": "Analyze our Q3 pipeline and flag deals that need immediate attention",
  "sector": "sales"
}
```

2. **Blocking Tickets**
```json
{
  "query": "Which customer service tickets are blocking our biggest deals?"
}
```

### Customer Service Queries

1. **Escalation Prediction**
```json
{
  "query": "Show me ticket trends and predict which issues will escalate this week",
  "sector": "service"
}
```

2. **Financial Impact**
```json
{
  "query": "What's the financial impact of our top 5 customer complaints?"
}
```

### Finance Queries

1. **Auto-Approval**
```json
{
  "query": "Review pending invoices and approve those under $5K automatically",
  "sector": "finance"
}
```

2. **Budget Analysis**
```json
{
  "query": "How does our current cash flow affect our hiring budget for next quarter?"
}
```

## Error Responses

All errors follow this format:

```json
{
  "error": "Error message",
  "message": "Detailed error description"
}
```

**Status Codes:**
- `200`: Success
- `400`: Bad Request
- `500`: Internal Server Error
- `503`: Service Unavailable

## Rate Limiting

Currently no rate limiting is implemented. For production, implement appropriate rate limiting.

## Authentication

Currently no authentication is required. For production, implement API key or OAuth authentication.


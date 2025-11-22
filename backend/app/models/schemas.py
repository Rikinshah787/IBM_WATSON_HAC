"""
Pydantic models for API request/response schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class Sector(str, Enum):
    """Business sectors"""
    HR = "hr"
    SALES = "sales"
    SERVICE = "service"
    FINANCE = "finance"
    CROSS_SECTOR = "cross_sector"


class QueryRequest(BaseModel):
    """Request model for agent queries"""
    query: str = Field(..., description="Natural language query")
    sector: Optional[Sector] = Field(None, description="Target sector (optional)")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "Show me attrition trends this quarter and which departments are at risk",
                "sector": "hr",
                "context": {}
            }
        }


class Insight(BaseModel):
    """Insight model"""
    title: str
    description: str
    sector: Sector
    confidence: float = Field(..., ge=0.0, le=1.0)
    data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.now)


class Action(BaseModel):
    """Action model"""
    action_type: str = Field(..., description="Type of action (approve, alert, assign, etc.)")
    target: str = Field(..., description="Target of the action")
    parameters: Dict[str, Any] = Field(default_factory=dict)
    status: str = Field(default="pending", description="Action status")
    timestamp: datetime = Field(default_factory=datetime.now)


class QueryResponse(BaseModel):
    """Response model for agent queries"""
    query: str
    intent: str = Field(..., description="Detected intent")
    sectors: List[Sector] = Field(..., description="Involved sectors")
    insights: List[Insight] = Field(default_factory=list)
    actions: List[Action] = Field(default_factory=list)
    data: Dict[str, Any] = Field(default_factory=dict)
    response_text: str = Field(..., description="Natural language response")
    execution_time: float = Field(..., description="Execution time in seconds")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "Show me attrition trends",
                "intent": "analyze_attrition",
                "sectors": ["hr"],
                "insights": [],
                "actions": [],
                "data": {},
                "response_text": "Attrition trends analysis...",
                "execution_time": 1.23
            }
        }


class DashboardData(BaseModel):
    """Dashboard data model"""
    sector: Sector
    metrics: Dict[str, Any]
    trends: List[Dict[str, Any]]
    alerts: List[Dict[str, Any]]
    last_updated: datetime = Field(default_factory=datetime.now)


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    agent: str
    timestamp: str


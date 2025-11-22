"""
API routes for OrchestrateIQ
"""

import logging
import time
from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List

from app.models.schemas import (
    QueryRequest,
    QueryResponse,
    DashboardData,
    Sector,
    HealthResponse
)
from app.orchestrate.agent import OrchestrateAgent

logger = logging.getLogger(__name__)

router = APIRouter(tags=["orchestrateiq"])


def get_agent(request: Request) -> OrchestrateAgent:
    """Dependency to get agent instance"""
    agent = getattr(request.app.state, "agent", None)
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    return agent


@router.post("/query", response_model=QueryResponse)
async def process_query(
    request: QueryRequest,
    agent: OrchestrateAgent = Depends(get_agent)
):
    """
    Process a natural language query through watsonx Orchestrate
    
    Args:
        request: Query request with natural language query
        agent: Orchestrate agent instance
    
    Returns:
        QueryResponse with insights, actions, and data
    """
    start_time = time.time()
    logger.info(f"📥 Received query: {request.query}")
    logger.debug(f"Query details: sector={request.sector}, context={request.context}")
    
    try:
        # Process query through orchestrate agent
        response = await agent.process_query(
            query=request.query,
            sector=request.sector,
            context=request.context or {}
        )
        
        execution_time = time.time() - start_time
        logger.info(f"✅ Query processed successfully in {execution_time:.2f}s")
        logger.debug(f"Response: {response.dict()}")
        
        return response
        
    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"❌ Query processing failed after {execution_time:.2f}s: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")


@router.get("/dashboard/{sector}", response_model=DashboardData)
async def get_dashboard_data(
    sector: Sector,
    agent: OrchestrateAgent = Depends(get_agent)
):
    """
    Get dashboard data for a specific sector
    
    Args:
        sector: Business sector
        agent: Orchestrate agent instance
    
    Returns:
        DashboardData with metrics, trends, and alerts
    """
    logger.info(f"📊 Fetching dashboard data for sector: {sector.value}")
    
    try:
        data = await agent.get_dashboard_data(sector)
        logger.info(f"✅ Dashboard data retrieved for {sector.value}")
        return data
        
    except Exception as e:
        logger.error(f"❌ Failed to get dashboard data: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get dashboard data: {str(e)}")


@router.get("/sectors", response_model=List[str])
async def get_sectors():
    """
    Get list of available sectors
    
    Returns:
        List of sector names
    """
    logger.debug("Fetching available sectors")
    return [sector.value for sector in Sector]


@router.get("/health", response_model=HealthResponse)
async def health_check(agent: OrchestrateAgent = Depends(get_agent)):
    """
    Health check endpoint
    
    Returns:
        Health status
    """
    logger.debug("Health check requested")
    return HealthResponse(
        status="healthy" if agent.is_initialized else "degraded",
        agent="initialized" if agent.is_initialized else "not_initialized",
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
    )


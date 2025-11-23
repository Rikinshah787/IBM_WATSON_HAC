"""
watsonx Orchestrate Agent Integration
Handles agent initialization, query processing, and orchestration
"""

import logging
import os
from typing import Optional, Dict, Any, List
from datetime import datetime
import time

from pydantic_settings import BaseSettings
from app.models.schemas import QueryResponse, DashboardData, Sector, Insight, Action
from app.orchestrate.workflows import WorkflowOrchestrator
from app.orchestrate.watsonx_ai import WatsonXClient, WatsonXSettings
from app.data import get_data_handler

logger = logging.getLogger(__name__)


class OrchestrateSettings(BaseSettings):
    """watsonx Orchestrate configuration"""
    api_key: str = ""
    url: str = "https://api.watsonx.orchestrate.cloud.ibm.com"
    project_id: str = ""
    
    class Config:
        env_prefix = "WATSONX_ORCHESTRATE_"
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


class OrchestrateAgent:
    """
    Main agent class for watsonx Orchestrate integration
    Handles query processing, workflow orchestration, and data retrieval
    """
    
    def __init__(self):
        """Initialize agent with configuration"""
        self.settings = OrchestrateSettings()
        self.is_initialized = False
        self.workflow_orchestrator = None
        self.watsonx_client = None
        logger.info("🔧 OrchestrateAgent instance created")
    
    async def initialize(self):
        """
        Initialize watsonx Orchestrate agent
        Sets up API connection and workflow orchestrator
        """
        logger.info("🚀 Initializing watsonx Orchestrate agent...")
        
        try:
            # Validate configuration
            if not self.settings.api_key:
                logger.warning("⚠️ watsonx Orchestrate API key not found. Using mock mode.")
                # Continue with mock mode for development
            else:
                logger.info("✅ watsonx Orchestrate API key found")
                logger.debug(f"API URL: {self.settings.url}")
                logger.debug(f"Project ID: {self.settings.project_id}")
            
            # Initialize WatsonX Client
            logger.info("🧠 Initializing WatsonX AI Client...")
            try:
                self.watsonx_client = WatsonXClient()
                if self.watsonx_client.available:
                    logger.info("✅ WatsonX AI Client available")
                else:
                    logger.warning("⚠️ WatsonX AI Client not configured (missing credentials)")
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize WatsonX Client: {e}")
                self.watsonx_client = None

            # Initialize workflow orchestrator
            logger.info("🔗 Initializing workflow orchestrator...")
            self.workflow_orchestrator = WorkflowOrchestrator(watsonx_client=self.watsonx_client)
            await self.workflow_orchestrator.initialize()
            
            self.is_initialized = True
            logger.info("✅ watsonx Orchestrate agent initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize agent: {str(e)}", exc_info=True)
            # Allow initialization to continue in mock mode
            self.is_initialized = True
            logger.warning("⚠️ Continuing in mock mode for development")
    
    async def process_query(
        self,
        query: str,
        sector: Optional[Sector] = None,
        context: Dict[str, Any] = None
    ) -> QueryResponse:
        """
        Process a natural language query through orchestration
        
        Args:
            query: Natural language query
            sector: Target sector (optional)
            context: Additional context
        
        Returns:
            QueryResponse with insights, actions, and data
        """
        start_time = time.time()
        context = context or {}
        
        logger.info(f"📝 Processing query: {query}")
        logger.debug(f"Query parameters: sector={sector}, context={context}")
        
        try:
            # Step 1: Intent recognition (using workflow orchestrator)
            logger.debug("🔍 Step 1: Recognizing intent...")
            intent_result = await self.workflow_orchestrator.recognize_intent(query, sector)
            intent = intent_result.get("intent", "general_query")
            detected_sectors = intent_result.get("sectors", [sector] if sector else [])
            
            logger.info(f"✅ Intent recognized: {intent}")
            logger.info(f"📊 Detected sectors: {detected_sectors}")
            
            # Step 2: Orchestrate workflow
            logger.debug("🔄 Step 2: Orchestrating workflow...")
            workflow_result = await self.workflow_orchestrator.execute_workflow(
                intent=intent,
                query=query,
                sectors=detected_sectors,
                context=context
            )
            
            # Step 3: Extract insights and actions
            insights = workflow_result.get("insights", [])
            actions = workflow_result.get("actions", [])
            data = workflow_result.get("data", {})
            
            logger.info(f"✅ Workflow executed: {len(insights)} insights, {len(actions)} actions")
            
            # Step 4: Generate response text
            logger.debug("💬 Step 4: Generating response text...")
            response_text = await self._generate_response_text(
                query=query,
                intent=intent,
                insights=insights,
                actions=actions,
                data=data
            )
            
            execution_time = time.time() - start_time
            
            # Create response
            response = QueryResponse(
                query=query,
                intent=intent,
                sectors=detected_sectors,
                insights=insights,
                actions=actions,
                data=data,
                response_text=response_text,
                execution_time=execution_time,
                timestamp=datetime.now()
            )
            
            logger.info(f"✅ Query processed successfully in {execution_time:.2f}s")
            return response
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"❌ Query processing failed after {execution_time:.2f}s: {str(e)}", exc_info=True)
            raise
    
    async def get_dashboard_data(self, sector: Sector) -> DashboardData:
        """
        Get dashboard data for a specific sector
        
        Args:
            sector: Business sector
        
        Returns:
            DashboardData with metrics, trends, and alerts
        """
        logger.info(f"📊 Fetching dashboard data for sector: {sector.value}")
        
        try:
            # Get data handler for sector
            data_handler = get_data_handler(sector)
            
            # Get metrics and trends
            metrics = await data_handler.get_metrics()
            trends = await data_handler.get_trends()
            alerts = await data_handler.get_alerts()
            
            logger.info(f"✅ Dashboard data retrieved: {len(metrics)} metrics, {len(trends)} trends, {len(alerts)} alerts")
            
            return DashboardData(
                sector=sector,
                metrics=metrics,
                trends=trends,
                alerts=alerts,
                last_updated=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"❌ Failed to get dashboard data: {str(e)}", exc_info=True)
            raise
    
    async def _generate_response_text(
        self,
        query: str,
        intent: str,
        insights: List[Insight],
        actions: List[Action],
        data: Dict[str, Any]
    ) -> str:
        """
        Generate natural language response text
        
        Args:
            query: Original query
            intent: Detected intent
            insights: List of insights
            actions: List of actions
            data: Retrieved data
        
        Returns:
            Natural language response
        """
        logger.debug("Generating response text...")
        
        # Build response based on insights and actions
        response_parts = []
        
        if insights:
            response_parts.append(f"I found {len(insights)} key insight(s):")
            for insight in insights[:3]:  # Limit to top 3
                response_parts.append(f"• {insight.description}")
        
        if actions:
            response_parts.append(f"\nI've triggered {len(actions)} action(s):")
            for action in actions:
                response_parts.append(f"• {action.action_type}: {action.target}")
        
        if data:
            response_parts.append("\nHere's the data you requested:")
            # Add summary of data
        
        if not response_parts:
            response_parts.append("I've processed your query and retrieved the relevant information.")
        
        return "\n".join(response_parts)


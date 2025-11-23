"""
Workflow Orchestration Logic
Defines and executes workflows for different intents and sectors
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.models.schemas import Sector, Insight, Action
from app.orchestrate.skills import DigitalSkillsManager
from app.data import get_data_handler

logger = logging.getLogger(__name__)


class WorkflowOrchestrator:
    """
    Orchestrates workflows across sectors
    Maps intents to workflows and executes them
    """
    
    def __init__(self, watsonx_client=None):
        """Initialize workflow orchestrator"""
        self.skills_manager = None
        self.watsonx_client = watsonx_client
        self.intent_mappings = self._initialize_intent_mappings()
        logger.info("🔧 WorkflowOrchestrator created")
    
    async def initialize(self):
        """Initialize workflow orchestrator"""
        logger.info("🚀 Initializing workflow orchestrator...")
        
        # Initialize digital skills manager
        self.skills_manager = DigitalSkillsManager()
        await self.skills_manager.initialize()
        
        logger.info("✅ Workflow orchestrator initialized")
    
    def _initialize_intent_mappings(self) -> Dict[str, Dict[str, Any]]:
        """
        Initialize intent to workflow mappings
        
        Returns:
            Dictionary mapping intents to workflow configurations
        """
        return {
            # HR Intents
            "analyze_attrition": {
                "sectors": [Sector.HR],
                "workflow": "hr_attrition_analysis",
                "skills": ["workday_hr"]
            },
            "correlate_satisfaction_sales": {
                "sectors": [Sector.HR, Sector.SALES],
                "workflow": "cross_sector_correlation",
                "skills": ["workday_hr", "salesforce"]
            },
            
            # Sales Intents
            "analyze_pipeline": {
                "sectors": [Sector.SALES],
                "workflow": "sales_pipeline_analysis",
                "skills": ["salesforce"]
            },
            "identify_blocking_tickets": {
                "sectors": [Sector.SALES, Sector.SERVICE],
                "workflow": "cross_sector_blocking_analysis",
                "skills": ["salesforce", "servicenow"]
            },
            
            # Customer Service Intents
            "predict_escalations": {
                "sectors": [Sector.SERVICE],
                "workflow": "service_escalation_prediction",
                "skills": ["servicenow"]
            },
            "analyze_complaint_impact": {
                "sectors": [Sector.SERVICE, Sector.FINANCE],
                "workflow": "cross_sector_impact_analysis",
                "skills": ["servicenow", "sap"]
            },
            
            # Finance Intents
            "auto_approve_invoices": {
                "sectors": [Sector.FINANCE],
                "workflow": "finance_auto_approval",
                "skills": ["sap"]
            },
            "analyze_budget_hiring": {
                "sectors": [Sector.FINANCE, Sector.HR],
                "workflow": "cross_sector_budget_analysis",
                "skills": ["sap", "workday_hr"]
            },
            
            # General
            "general_query": {
                "sectors": [],
                "workflow": "general_workflow",
                "skills": []
            }
        }
    
    async def recognize_intent(
        self,
        query: str,
        sector: Optional[Sector] = None
    ) -> Dict[str, Any]:
        """
        Recognize intent from natural language query
        
        Args:
            query: Natural language query
            sector: Optional target sector
        
        Returns:
            Dictionary with intent and detected sectors
        """
        logger.debug(f"🔍 Recognizing intent from query: {query}")
        
        query_lower = query.lower()
        
        # Try Watson AI for intent recognition first
        if self.watsonx_client and self.watsonx_client.available:
            logger.debug("🧠 Using Watson AI for intent recognition")
            ai_result = await self.watsonx_client.recognize_intent(query, [s.value for s in Sector])
            if ai_result and ai_result.get("intent"):
                intent = ai_result["intent"]
                # Map string sectors back to Enum
                detected_sectors = []
                for s_str in ai_result.get("sectors", []):
                    try:
                        detected_sectors.append(Sector(s_str.lower()))
                    except ValueError:
                        pass
                
                logger.info(f"✅ Watson recognized intent: {intent}, Sectors: {detected_sectors}")
                return {
                    "intent": intent,
                    "sectors": detected_sectors,
                    "confidence": 0.95
                }

        # Fallback to keyword-based intent recognition
        logger.debug("⚠️ Watson AI unavailable or failed, falling back to keywords")
        
        intent = "general_query"
        detected_sectors = []
        
        # Check for sector keywords
        if any(word in query_lower for word in ["attrition", "employee", "hiring", "satisfaction", "hr", "human resources"]):
            detected_sectors.append(Sector.HR)
            if "attrition" in query_lower and "trend" in query_lower:
                intent = "analyze_attrition"
            elif "satisfaction" in query_lower and ("sales" in query_lower or "performance" in query_lower):
                intent = "correlate_satisfaction_sales"
        
        if any(word in query_lower for word in ["pipeline", "deal", "sales", "customer", "revenue"]):
            detected_sectors.append(Sector.SALES)
            if "pipeline" in query_lower:
                intent = "analyze_pipeline"
            elif "ticket" in query_lower and ("block" in query_lower or "blocking" in query_lower):
                intent = "identify_blocking_tickets"
        
        if any(word in query_lower for word in ["ticket", "service", "support", "escalat", "complaint"]):
            detected_sectors.append(Sector.SERVICE)
            if "escalat" in query_lower or "predict" in query_lower:
                intent = "predict_escalations"
            elif "complaint" in query_lower and ("impact" in query_lower or "financial" in query_lower):
                intent = "analyze_complaint_impact"
        
        if any(word in query_lower for word in ["invoice", "finance", "budget", "cash flow", "approve"]):
            detected_sectors.append(Sector.FINANCE)
            if "approve" in query_lower and "invoice" in query_lower:
                intent = "auto_approve_invoices"
            elif "budget" in query_lower and ("hiring" in query_lower or "hr" in query_lower):
                intent = "analyze_budget_hiring"
        
        # Use provided sector if no sectors detected
        if not detected_sectors and sector:
            detected_sectors = [sector]
        
        logger.info(f"✅ Intent recognized (Keyword): {intent}, Sectors: {detected_sectors}")
        
        return {
            "intent": intent,
            "sectors": detected_sectors,
            "confidence": 0.85  # Mock confidence score
        }
    
    async def execute_workflow(
        self,
        intent: str,
        query: str,
        sectors: List[Sector],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute workflow for a given intent
        
        Args:
            intent: Detected intent
            query: Original query
            sectors: Involved sectors
            context: Additional context
        
        Returns:
            Dictionary with insights, actions, and data
        """
        logger.info(f"🔄 Executing workflow for intent: {intent}")
        logger.debug(f"Workflow parameters: sectors={sectors}, context={context}")
        
        # Get workflow configuration
        workflow_config = self.intent_mappings.get(intent, self.intent_mappings["general_query"])
        workflow_name = workflow_config["workflow"]
        required_skills = workflow_config["skills"]
        
        logger.debug(f"Workflow: {workflow_name}, Required skills: {required_skills}")
        
        # Execute workflow based on intent
        if workflow_name == "hr_attrition_analysis":
            return await self._execute_hr_attrition_workflow(query, sectors, context)
        
        elif workflow_name == "cross_sector_correlation":
            return await self._execute_correlation_workflow(query, sectors, context)
        
        elif workflow_name == "sales_pipeline_analysis":
            return await self._execute_sales_pipeline_workflow(query, sectors, context)
        
        elif workflow_name == "cross_sector_blocking_analysis":
            return await self._execute_blocking_analysis_workflow(query, sectors, context)
        
        elif workflow_name == "service_escalation_prediction":
            return await self._execute_escalation_prediction_workflow(query, sectors, context)
        
        elif workflow_name == "cross_sector_impact_analysis":
            return await self._execute_impact_analysis_workflow(query, sectors, context)
        
        elif workflow_name == "finance_auto_approval":
            return await self._execute_auto_approval_workflow(query, sectors, context)
        
        elif workflow_name == "cross_sector_budget_analysis":
            return await self._execute_budget_analysis_workflow(query, sectors, context)
        
        else:
            return await self._execute_general_workflow(query, sectors, context)
    
    # Workflow execution methods
    async def _execute_hr_attrition_workflow(
        self,
        query: str,
        sectors: List[Sector],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute HR attrition analysis workflow"""
        logger.info("🔄 Executing HR attrition analysis workflow")
        
        # Get data using digital skills
        hr_data = await self.skills_manager.execute_skill("workday_hr", "get_attrition_data", {})
        
        # Process data
        data_handler = get_data_handler(Sector.HR)
        analysis = await data_handler.analyze_attrition(hr_data)
        
        # Generate insights
        description = f"Attrition rate is {analysis.get('attrition_rate', 0):.1f}% this quarter"
        
        # Use Watson to generate insight if available
        if self.watsonx_client and self.watsonx_client.available:
            ai_insight = await self.watsonx_client.generate_insight(query, analysis, context)
            if ai_insight:
                description = ai_insight

        insights = [
            Insight(
                title="Attrition Trend Analysis",
                description=description,
                sector=Sector.HR,
                confidence=0.9,
                data=analysis
            )
        ]
        
        # Generate actions
        high_risk_depts = analysis.get("high_risk_departments", [])
        actions = []
        if high_risk_depts:
            actions.append(
                Action(
                    action_type="generate_retention_plan",
                    target=f"departments: {', '.join(high_risk_depts)}",
                    parameters={"departments": high_risk_depts},
                    status="completed"
                )
            )
        
        return {
            "insights": insights,
            "actions": actions,
            "data": analysis
        }
    
    async def _execute_correlation_workflow(
        self,
        query: str,
        sectors: List[Sector],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute cross-sector correlation workflow"""
        logger.info("🔄 Executing cross-sector correlation workflow")
        
        # Get data from multiple sectors
        hr_data = await self.skills_manager.execute_skill("workday_hr", "get_satisfaction_data", {})
        sales_data = await self.skills_manager.execute_skill("salesforce", "get_performance_data", {})
        
        # Cross-sector analysis
        hr_handler = get_data_handler(Sector.HR)
        sales_handler = get_data_handler(Sector.SALES)
        
        correlation = await hr_handler.correlate_with_sales(hr_data, sales_data)
        
        insights = [
            Insight(
                title="Satisfaction-Sales Correlation",
                description=correlation.get("description", "Correlation analysis completed"),
                sector=Sector.CROSS_SECTOR,
                confidence=0.85,
                data=correlation
            )
        ]
        
        return {
            "insights": insights,
            "actions": [],
            "data": correlation
        }
    
    async def _execute_sales_pipeline_workflow(
        self,
        query: str,
        sectors: List[Sector],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute sales pipeline analysis workflow"""
        logger.info("🔄 Executing sales pipeline analysis workflow")
        
        sales_data = await self.skills_manager.execute_skill("salesforce", "get_pipeline_data", {})
        data_handler = get_data_handler(Sector.SALES)
        analysis = await data_handler.analyze_pipeline(sales_data)
        
        insights = [
            Insight(
                title="Pipeline Analysis",
                description=f"Pipeline health: {analysis.get('health_score', 0):.1f}/100",
                sector=Sector.SALES,
                confidence=0.9,
                data=analysis
            )
        ]
        
        # Auto-assign tasks for urgent deals
        urgent_deals = analysis.get("urgent_deals", [])
        actions = []
        for deal in urgent_deals[:3]:  # Limit to 3
            actions.append(
                Action(
                    action_type="assign_task",
                    target=f"deal: {deal.get('id', 'unknown')}",
                    parameters={"deal_id": deal.get("id"), "priority": "high"},
                    status="completed"
                )
            )
        
        return {
            "insights": insights,
            "actions": actions,
            "data": analysis
        }
    
    async def _execute_blocking_analysis_workflow(
        self,
        query: str,
        sectors: List[Sector],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute blocking ticket analysis workflow"""
        logger.info("🔄 Executing blocking ticket analysis workflow")
        
        sales_data = await self.skills_manager.execute_skill("salesforce", "get_deals_data", {})
        service_data = await self.skills_manager.execute_skill("servicenow", "get_tickets_data", {})
        
        sales_handler = get_data_handler(Sector.SALES)
        blocking_analysis = await sales_handler.identify_blocking_tickets(sales_data, service_data)
        
        insights = [
            Insight(
                title="Blocking Tickets Analysis",
                description=f"Found {len(blocking_analysis.get('blocking_tickets', []))} tickets blocking deals",
                sector=Sector.CROSS_SECTOR,
                confidence=0.88,
                data=blocking_analysis
            )
        ]
        
        # Escalate blocking tickets
        actions = []
        for ticket in blocking_analysis.get("blocking_tickets", [])[:3]:
            actions.append(
                Action(
                    action_type="escalate_ticket",
                    target=f"ticket: {ticket.get('id', 'unknown')}",
                    parameters={"ticket_id": ticket.get("id"), "priority": "critical"},
                    status="completed"
                )
            )
        
        return {
            "insights": insights,
            "actions": actions,
            "data": blocking_analysis
        }
    
    async def _execute_escalation_prediction_workflow(
        self,
        query: str,
        sectors: List[Sector],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute escalation prediction workflow"""
        logger.info("🔄 Executing escalation prediction workflow")
        
        service_data = await self.skills_manager.execute_skill("servicenow", "get_tickets_data", {})
        data_handler = get_data_handler(Sector.SERVICE)
        prediction = await data_handler.predict_escalations(service_data)
        
        insights = [
            Insight(
                title="Escalation Prediction",
                description=f"Predicted {len(prediction.get('high_risk_tickets', []))} tickets likely to escalate",
                sector=Sector.SERVICE,
                confidence=0.87,
                data=prediction
            )
        ]
        
        # Pre-assign senior agents
        actions = []
        for ticket in prediction.get("high_risk_tickets", [])[:3]:
            actions.append(
                Action(
                    action_type="assign_senior_agent",
                    target=f"ticket: {ticket.get('id', 'unknown')}",
                    parameters={"ticket_id": ticket.get("id"), "agent_level": "senior"},
                    status="completed"
                )
            )
        
        return {
            "insights": insights,
            "actions": actions,
            "data": prediction
        }
    
    async def _execute_impact_analysis_workflow(
        self,
        query: str,
        sectors: List[Sector],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute complaint impact analysis workflow"""
        logger.info("🔄 Executing complaint impact analysis workflow")
        
        service_data = await self.skills_manager.execute_skill("servicenow", "get_complaints_data", {})
        finance_data = await self.skills_manager.execute_skill("sap", "get_financial_data", {})
        
        service_handler = get_data_handler(Sector.SERVICE)
        impact_analysis = await service_handler.analyze_financial_impact(service_data, finance_data)
        
        insights = [
            Insight(
                title="Financial Impact Analysis",
                description=f"Top 5 complaints have ${impact_analysis.get('total_impact', 0):,.0f} financial impact",
                sector=Sector.CROSS_SECTOR,
                confidence=0.9,
                data=impact_analysis
            )
        ]
        
        return {
            "insights": insights,
            "actions": [],
            "data": impact_analysis
        }
    
    async def _execute_auto_approval_workflow(
        self,
        query: str,
        sectors: List[Sector],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute auto-approval workflow"""
        logger.info("🔄 Executing auto-approval workflow")
        
        finance_data = await self.skills_manager.execute_skill("sap", "get_invoices_data", {})
        data_handler = get_data_handler(Sector.FINANCE)
        approval_result = await data_handler.auto_approve_invoices(finance_data, threshold=5000)
        
        insights = [
            Insight(
                title="Auto-Approval Summary",
                description=f"Approved {approval_result.get('approved_count', 0)} invoices automatically",
                sector=Sector.FINANCE,
                confidence=1.0,
                data=approval_result
            )
        ]
        
        # Generate approval actions
        actions = []
        for invoice in approval_result.get("approved_invoices", []):
            actions.append(
                Action(
                    action_type="approve_invoice",
                    target=f"invoice: {invoice.get('id', 'unknown')}",
                    parameters={"invoice_id": invoice.get("id"), "amount": invoice.get("amount")},
                    status="completed"
                )
            )
        
        return {
            "insights": insights,
            "actions": actions,
            "data": approval_result
        }
    
    async def _execute_budget_analysis_workflow(
        self,
        query: str,
        sectors: List[Sector],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute budget-hiring analysis workflow"""
        logger.info("🔄 Executing budget-hiring analysis workflow")
        
        finance_data = await self.skills_manager.execute_skill("sap", "get_cashflow_data", {})
        hr_data = await self.skills_manager.execute_skill("workday_hr", "get_hiring_plan_data", {})
        
        finance_handler = get_data_handler(Sector.FINANCE)
        analysis = await finance_handler.analyze_hiring_budget(finance_data, hr_data)
        
        insights = [
            Insight(
                title="Budget-Hiring Analysis",
                description=analysis.get("recommendation", "Budget analysis completed"),
                sector=Sector.CROSS_SECTOR,
                confidence=0.88,
                data=analysis
            )
        ]
        
        return {
            "insights": insights,
            "actions": [],
            "data": analysis
        }
    
    async def _execute_general_workflow(
        self,
        query: str,
        sectors: List[Sector],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute general workflow for unrecognized intents"""
        logger.info("🔄 Executing general workflow")
        
        return {
            "insights": [],
            "actions": [],
            "data": {"message": "General query processed", "query": query}
        }


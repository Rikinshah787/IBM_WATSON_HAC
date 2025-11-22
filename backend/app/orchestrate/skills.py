"""
Digital Skills Manager
Mocks enterprise integrations (Workday, Salesforce, ServiceNow, SAP)
"""

import logging
from typing import Dict, Any, Optional
from pathlib import Path
import csv

# Try to import pandas, fallback to csv module if not available
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

logger = logging.getLogger(__name__)

if not HAS_PANDAS:
    logger.info("⚠️ pandas not available, using built-in csv module")


class DigitalSkillsManager:
    """
    Manages digital skills (mocked enterprise integrations)
    Simulates Workday, Salesforce, ServiceNow, and SAP APIs
    """
    
    def __init__(self):
        """Initialize digital skills manager"""
        self.skills = {}
        self.data_path = Path(__file__).parent.parent.parent / "data"
        logger.info("🔧 DigitalSkillsManager created")
    
    async def initialize(self):
        """Initialize all digital skills"""
        logger.info("🚀 Initializing digital skills...")
        
        # Register all skills
        self.skills = {
            "workday_hr": self._workday_hr_skill,
            "salesforce": self._salesforce_skill,
            "servicenow": self._servicenow_skill,
            "sap": self._sap_skill
        }
        
        logger.info(f"✅ Initialized {len(self.skills)} digital skills")
        logger.debug(f"Available skills: {list(self.skills.keys())}")
    
    async def execute_skill(
        self,
        skill_name: str,
        operation: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a digital skill operation
        
        Args:
            skill_name: Name of the skill (workday_hr, salesforce, etc.)
            operation: Operation to perform
            parameters: Operation parameters
        
        Returns:
            Result data from the skill
        """
        logger.info(f"🔧 Executing skill: {skill_name}.{operation}")
        logger.debug(f"Parameters: {parameters}")
        
        if skill_name not in self.skills:
            logger.error(f"❌ Unknown skill: {skill_name}")
            raise ValueError(f"Unknown skill: {skill_name}")
        
        try:
            skill_func = self.skills[skill_name]
            result = await skill_func(operation, parameters)
            logger.info(f"✅ Skill executed successfully: {skill_name}.{operation}")
            return result
        except Exception as e:
            logger.error(f"❌ Skill execution failed: {skill_name}.{operation} - {str(e)}", exc_info=True)
            raise
    
    # Workday HR Skill
    async def _workday_hr_skill(self, operation: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Workday HR digital skill"""
        logger.debug(f"Workday HR skill: {operation}")
        
        if operation == "get_attrition_data":
            return await self._load_csv_data("hr", "attrition_data.csv")
        elif operation == "get_satisfaction_data":
            return await self._load_csv_data("hr", "satisfaction_scores.csv")
        elif operation == "get_hiring_plan_data":
            return await self._load_csv_data("hr", "employee_data.csv")
        else:
            logger.warning(f"Unknown Workday operation: {operation}")
            return {}
    
    # Salesforce Skill
    async def _salesforce_skill(self, operation: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Salesforce digital skill"""
        logger.debug(f"Salesforce skill: {operation}")
        
        if operation == "get_pipeline_data":
            return await self._load_csv_data("sales", "pipeline_data.csv")
        elif operation == "get_deals_data":
            return await self._load_csv_data("sales", "deals_data.csv")
        elif operation == "get_performance_data":
            return await self._load_csv_data("sales", "customer_data.csv")
        else:
            logger.warning(f"Unknown Salesforce operation: {operation}")
            return {}
    
    # ServiceNow Skill
    async def _servicenow_skill(self, operation: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """ServiceNow digital skill"""
        logger.debug(f"ServiceNow skill: {operation}")
        
        if operation == "get_tickets_data":
            return await self._load_csv_data("service", "tickets_data.csv")
        elif operation == "get_complaints_data":
            return await self._load_csv_data("service", "escalations.csv")
        elif operation == "get_response_times":
            return await self._load_csv_data("service", "response_times.csv")
        else:
            logger.warning(f"Unknown ServiceNow operation: {operation}")
            return {}
    
    # SAP Skill
    async def _sap_skill(self, operation: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """SAP digital skill"""
        logger.debug(f"SAP skill: {operation}")
        
        if operation == "get_invoices_data":
            return await self._load_csv_data("finance", "invoices_data.csv")
        elif operation == "get_financial_data":
            return await self._load_csv_data("finance", "cashflow_data.csv")
        elif operation == "get_cashflow_data":
            return await self._load_csv_data("finance", "cashflow_data.csv")
        elif operation == "get_budget_data":
            return await self._load_csv_data("finance", "budget_data.csv")
        else:
            logger.warning(f"Unknown SAP operation: {operation}")
            return {}
    
    async def _load_csv_data(self, sector: str, filename: str) -> Dict[str, Any]:
        """
        Load CSV data file
        
        Args:
            sector: Sector name (hr, sales, service, finance)
            filename: CSV filename
        
        Returns:
            Dictionary with data
        """
        file_path = self.data_path / sector / filename
        
        if not file_path.exists():
            logger.warning(f"⚠️ Data file not found: {file_path}")
            return {"error": "Data file not found", "file": str(file_path)}
        
        try:
            if HAS_PANDAS:
                # Use pandas if available (faster)
                df = pd.read_csv(file_path)
                logger.debug(f"✅ Loaded {len(df)} rows from {filename} (using pandas)")
                return {
                    "data": df.to_dict(orient="records"),
                    "count": len(df),
                    "columns": df.columns.tolist()
                }
            else:
                # Fallback to built-in csv module
                records = []
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    records = list(reader)
                
                columns = list(reader.fieldnames) if records else []
                logger.debug(f"✅ Loaded {len(records)} rows from {filename} (using csv module)")
                return {
                    "data": records,
                    "count": len(records),
                    "columns": columns
                }
        except Exception as e:
            logger.error(f"❌ Failed to load CSV: {str(e)}", exc_info=True)
            return {"error": str(e), "file": str(file_path)}


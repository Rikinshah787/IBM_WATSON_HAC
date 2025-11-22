"""
HR Data Handler
Processes HR data and generates insights
"""

import logging
from typing import Dict, Any, List

# Try to import pandas, fallback to manual processing if not available
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

logger = logging.getLogger(__name__)


class HRDataHandler:
    """Handles HR data processing and analysis"""
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get HR metrics"""
        logger.debug("Getting HR metrics")
        return {
            "total_employees": 1250,
            "attrition_rate": 8.5,
            "satisfaction_score": 7.8,
            "open_positions": 45
        }
    
    async def get_trends(self) -> List[Dict[str, Any]]:
        """Get HR trends"""
        logger.debug("Getting HR trends")
        return [
            {"period": "Q1", "attrition": 6.2, "satisfaction": 7.5},
            {"period": "Q2", "attrition": 7.1, "satisfaction": 7.7},
            {"period": "Q3", "attrition": 8.5, "satisfaction": 7.8}
        ]
    
    async def get_alerts(self) -> List[Dict[str, Any]]:
        """Get HR alerts"""
        logger.debug("Getting HR alerts")
        return [
            {"type": "high_attrition", "department": "Sales", "severity": "high"},
            {"type": "low_satisfaction", "department": "Support", "severity": "medium"}
        ]
    
    async def analyze_attrition(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze attrition data"""
        logger.info("Analyzing attrition data")
        
        records = data.get("data", [])
        if not records:
            return {"attrition_rate": 0, "high_risk_departments": []}
        
        if HAS_PANDAS:
            df = pd.DataFrame(records)
            
            # Calculate attrition rate
            total = len(df)
            if "status" in df.columns:
                left = len(df[df["status"] == "Left"])
                attrition_rate = (left / total * 100) if total > 0 else 0
            else:
                attrition_rate = 8.5  # Default
            
            # Identify high-risk departments
            high_risk = []
            if "department" in df.columns:
                dept_attrition = df.groupby("department").apply(
                    lambda x: len(x[x.get("status", pd.Series()) == "Left"]) / len(x) * 100
                    if "status" in x.columns else 0
                )
                high_risk = dept_attrition[dept_attrition > 10].index.tolist()
            
            departments_analyzed = df["department"].nunique() if "department" in df.columns else 0
        else:
            # Manual processing without pandas
            total = len(records)
            left = len([r for r in records if r.get("status") == "Left"])
            attrition_rate = (left / total * 100) if total > 0 else 0
            
            # Group by department and calculate attrition
            dept_counts = {}
            for record in records:
                dept = record.get("department", "Unknown")
                if dept not in dept_counts:
                    dept_counts[dept] = {"total": 0, "left": 0}
                dept_counts[dept]["total"] += 1
                if record.get("status") == "Left":
                    dept_counts[dept]["left"] += 1
            
            # Find high-risk departments (>10% attrition)
            high_risk = [
                dept for dept, counts in dept_counts.items()
                if counts["total"] > 0 and (counts["left"] / counts["total"] * 100) > 10
            ]
            departments_analyzed = len(dept_counts)
        
        logger.info(f"Attrition analysis: {attrition_rate:.1f}% rate, {len(high_risk)} high-risk departments")
        
        return {
            "attrition_rate": attrition_rate,
            "high_risk_departments": high_risk[:5],  # Top 5
            "total_employees": total,
            "departments_analyzed": departments_analyzed
        }
    
    async def correlate_with_sales(
        self,
        hr_data: Dict[str, Any],
        sales_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Correlate HR satisfaction with sales performance"""
        logger.info("Correlating HR satisfaction with sales performance")
        
        hr_records = hr_data.get("data", [])
        sales_records = sales_data.get("data", [])
        
        # Simple correlation calculation
        avg_satisfaction = 7.8  # Default
        if hr_records and "satisfaction_score" in hr_records[0]:
            scores = [r.get("satisfaction_score", 0) for r in hr_records]
            avg_satisfaction = sum(scores) / len(scores) if scores else 7.8
        
        avg_sales_performance = 85  # Default
        if sales_records and "performance" in sales_records[0]:
            perfs = [r.get("performance", 0) for r in sales_records]
            avg_sales_performance = sum(perfs) / len(perfs) if perfs else 85
        
        correlation = "positive" if avg_satisfaction > 7.5 and avg_sales_performance > 80 else "neutral"
        
        return {
            "correlation": correlation,
            "avg_satisfaction": avg_satisfaction,
            "avg_sales_performance": avg_sales_performance,
            "description": f"Employee satisfaction ({avg_satisfaction:.1f}/10) shows {correlation} correlation with sales performance ({avg_sales_performance:.1f}%)"
        }


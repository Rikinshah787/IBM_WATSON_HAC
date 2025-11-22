"""
Customer Service Data Handler
Processes service data and generates insights
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


class ServiceDataHandler:
    """Handles customer service data processing and analysis"""
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get service metrics"""
        logger.debug("Getting service metrics")
        return {
            "open_tickets": 234,
            "avg_response_time": 2.5,
            "resolution_rate": 87.5,
            "escalation_rate": 12.3
        }
    
    async def get_trends(self) -> List[Dict[str, Any]]:
        """Get service trends"""
        logger.debug("Getting service trends")
        return [
            {"period": "Q1", "tickets": 210, "response_time": 3.2},
            {"period": "Q2", "tickets": 225, "response_time": 2.8},
            {"period": "Q3", "tickets": 234, "response_time": 2.5}
        ]
    
    async def get_alerts(self) -> List[Dict[str, Any]]:
        """Get service alerts"""
        logger.debug("Getting service alerts")
        return [
            {"type": "high_escalation", "count": 15, "severity": "high"},
            {"type": "slow_response", "avg_time": 4.5, "severity": "medium"}
        ]
    
    async def predict_escalations(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict which tickets will escalate"""
        logger.info("Predicting ticket escalations")
        
        records = data.get("data", [])
        if not records:
            return {"high_risk_tickets": [], "prediction_confidence": 0.85}
        
        # Identify high-risk tickets (works with or without pandas)
        high_risk = []
        for ticket in records:
            risk_score = 0
            
            # Age factor
            age_days = ticket.get("age_days", 0)
            if isinstance(age_days, str):
                try:
                    age_days = float(age_days)
                except (ValueError, TypeError):
                    age_days = 0
            
            if age_days > 5:
                risk_score += 3
            elif age_days > 3:
                risk_score += 2
            
            # Priority factor
            priority = str(ticket.get("priority", "")).lower()
            if "high" in priority or "critical" in priority:
                risk_score += 3
            elif "medium" in priority:
                risk_score += 1
            
            # Status factor
            status = str(ticket.get("status", "")).lower()
            if "open" in status or "pending" in status:
                risk_score += 2
            
            if risk_score >= 5:
                high_risk.append({
                    "id": ticket.get("id", "unknown"),
                    "risk_score": risk_score,
                    "reason": "High age, priority, or unresolved status"
                })
        
        logger.info(f"Predicted {len(high_risk)} high-risk tickets")
        
        return {
            "high_risk_tickets": high_risk[:10],  # Top 10
            "total_high_risk": len(high_risk),
            "prediction_confidence": 0.87
        }
    
    async def analyze_financial_impact(
        self,
        service_data: Dict[str, Any],
        finance_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze financial impact of customer complaints"""
        logger.info("Analyzing financial impact of complaints")
        
        service_records = service_data.get("data", [])
        
        # Get top 5 complaints by frequency or severity
        top_complaints = []
        if service_records:
            # Group by complaint type
            complaint_types = {}
            for record in service_records:
                complaint_type = record.get("type") or record.get("category", "unknown")
                if complaint_type not in complaint_types:
                    complaint_types[complaint_type] = {
                        "count": 0,
                        "total_impact": 0,
                        "avg_impact": 0
                    }
                complaint_types[complaint_type]["count"] += 1
                impact = record.get("financial_impact", 0) or record.get("cost", 0) or 0
                complaint_types[complaint_type]["total_impact"] += impact
            
            # Calculate averages and sort
            for ctype, data in complaint_types.items():
                data["avg_impact"] = data["total_impact"] / data["count"] if data["count"] > 0 else 0
            
            top_complaints = sorted(
                [
                    {"type": k, **v}
                    for k, v in complaint_types.items()
                ],
                key=lambda x: x["total_impact"],
                reverse=True
            )[:5]
        
        total_impact = sum(c.get("total_impact", 0) for c in top_complaints)
        
        return {
            "top_complaints": top_complaints,
            "total_impact": total_impact,
            "avg_impact_per_complaint": total_impact / len(top_complaints) if top_complaints else 0
        }


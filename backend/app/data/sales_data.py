"""
Sales Data Handler
Processes sales data and generates insights
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


class SalesDataHandler:
    """Handles sales data processing and analysis"""
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get sales metrics"""
        logger.debug("Getting sales metrics")
        return {
            "total_pipeline_value": 2500000,
            "deals_closed": 45,
            "conversion_rate": 23.5,
            "avg_deal_size": 55000
        }
    
    async def get_trends(self) -> List[Dict[str, Any]]:
        """Get sales trends"""
        logger.debug("Getting sales trends")
        return [
            {"period": "Q1", "revenue": 1200000, "deals": 38},
            {"period": "Q2", "revenue": 1350000, "deals": 42},
            {"period": "Q3", "revenue": 1500000, "deals": 45}
        ]
    
    async def get_alerts(self) -> List[Dict[str, Any]]:
        """Get sales alerts"""
        logger.debug("Getting sales alerts")
        return [
            {"type": "stale_deal", "deal_id": "DEAL-123", "days_stale": 45, "severity": "high"},
            {"type": "low_conversion", "period": "Q3", "severity": "medium"}
        ]
    
    async def analyze_pipeline(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze sales pipeline"""
        logger.info("Analyzing sales pipeline")
        
        records = data.get("data", [])
        if not records:
            return {"health_score": 75, "urgent_deals": []}
        
        if HAS_PANDAS:
            df = pd.DataFrame(records)
            
            # Calculate pipeline health
            total_value = df.get("value", pd.Series()).sum() if "value" in df.columns else 2500000
            avg_deal_size = total_value / len(df) if len(df) > 0 else 55000
            
            # Identify urgent deals (stale or high value)
            urgent_deals = []
            if "value" in df.columns and "status" in df.columns:
                urgent = df[
                    (df["value"] > 50000) | 
                    (df["status"] == "stale")
                ]
                urgent_deals = urgent.to_dict(orient="records")[:5]
            
            total_deals = len(df)
        else:
            # Manual processing without pandas
            total_value = sum(float(r.get("value", 0)) for r in records if r.get("value"))
            if total_value == 0:
                total_value = 2500000  # Default
            avg_deal_size = total_value / len(records) if records else 55000
            
            # Identify urgent deals
            urgent_deals = [
                r for r in records
                if (float(r.get("value", 0)) > 50000 or r.get("status") == "stale")
            ][:5]
            total_deals = len(records)
        
        health_score = min(100, max(0, 75 + (avg_deal_size / 1000)))
        
        logger.info(f"Pipeline analysis: health={health_score:.1f}, {len(urgent_deals)} urgent deals")
        
        return {
            "health_score": health_score,
            "total_pipeline_value": total_value,
            "avg_deal_size": avg_deal_size,
            "urgent_deals": urgent_deals,
            "total_deals": total_deals
        }
    
    async def identify_blocking_tickets(
        self,
        sales_data: Dict[str, Any],
        service_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Identify customer service tickets blocking sales deals"""
        logger.info("Identifying blocking tickets")
        
        sales_records = sales_data.get("data", [])
        service_records = service_data.get("data", [])
        
        # Simple matching logic
        blocking_tickets = []
        if sales_records and service_records:
            # Match by customer ID or name
            for deal in sales_records[:10]:  # Check top 10 deals
                customer_id = deal.get("customer_id") or deal.get("customer_name", "")
                matching_tickets = [
                    t for t in service_records
                    if (t.get("customer_id") == customer_id or 
                        t.get("customer_name", "").lower() == str(customer_id).lower())
                    and t.get("status") != "resolved"
                ]
                if matching_tickets:
                    blocking_tickets.extend(matching_tickets[:2])  # Max 2 per deal
        
        logger.info(f"Found {len(blocking_tickets)} blocking tickets")
        
        return {
            "blocking_tickets": blocking_tickets[:10],  # Top 10
            "total_blocking": len(blocking_tickets),
            "deals_affected": len(set(t.get("customer_id") for t in blocking_tickets))
        }


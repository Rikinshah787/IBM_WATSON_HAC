"""
Finance Data Handler
Processes finance data and generates insights
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


class FinanceDataHandler:
    """Handles finance data processing and analysis"""
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get finance metrics"""
        logger.debug("Getting finance metrics")
        return {
            "total_revenue": 4500000,
            "pending_invoices": 67,
            "cash_flow": 1250000,
            "budget_utilization": 78.5
        }
    
    async def get_trends(self) -> List[Dict[str, Any]]:
        """Get finance trends"""
        logger.debug("Getting finance trends")
        return [
            {"period": "Q1", "revenue": 4000000, "expenses": 3200000},
            {"period": "Q2", "revenue": 4250000, "expenses": 3400000},
            {"period": "Q3", "revenue": 4500000, "expenses": 3500000}
        ]
    
    async def get_alerts(self) -> List[Dict[str, Any]]:
        """Get finance alerts"""
        logger.debug("Getting finance alerts")
        return [
            {"type": "overdue_invoice", "count": 12, "total_amount": 125000, "severity": "high"},
            {"type": "budget_alert", "department": "IT", "utilization": 95, "severity": "medium"}
        ]
    
    async def auto_approve_invoices(
        self,
        data: Dict[str, Any],
        threshold: float = 5000
    ) -> Dict[str, Any]:
        """Auto-approve invoices under threshold"""
        logger.info(f"Auto-approving invoices under ${threshold:,.0f}")
        
        records = data.get("data", [])
        if not records:
            return {"approved_count": 0, "approved_invoices": []}
        
        # Filter invoices eligible for auto-approval (works with or without pandas)
        approved = []
        for invoice in records:
            amount = invoice.get("amount", 0)
            if isinstance(amount, str):
                try:
                    amount = float(amount)
                except (ValueError, TypeError):
                    amount = 0
            
            status = str(invoice.get("status", "")).lower()
            
            if amount <= threshold and status == "pending":
                approved.append(invoice)
        
        logger.info(f"Auto-approved {len(approved)} invoices")
        
        return {
            "approved_count": len(approved),
            "approved_invoices": approved[:20],  # Limit to 20
            "threshold": threshold,
            "total_amount": sum(float(i.get("amount", 0)) for i in approved)
        }
    
    async def analyze_hiring_budget(
        self,
        finance_data: Dict[str, Any],
        hr_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze how cash flow affects hiring budget"""
        logger.info("Analyzing hiring budget impact")
        
        finance_records = finance_data.get("data", [])
        hr_records = hr_data.get("data", [])
        
        # Calculate available cash flow
        available_cash = 0
        if finance_records:
            cash_flows = [r.get("cash_flow", 0) or r.get("amount", 0) for r in finance_records]
            available_cash = sum(cash_flows) if cash_flows else 1250000
        else:
            available_cash = 1250000  # Default
        
        # Calculate hiring needs
        open_positions = 0
        if hr_records:
            open_positions = len([r for r in hr_records if r.get("status") == "open"])
        else:
            open_positions = 45  # Default
        
        # Estimate hiring cost (average $80k per position)
        avg_hiring_cost = 80000
        total_hiring_cost = open_positions * avg_hiring_cost
        
        # Generate recommendation
        if available_cash >= total_hiring_cost * 1.2:  # 20% buffer
            recommendation = f"Strong cash flow (${available_cash:,.0f}) supports hiring {open_positions} positions. Recommended budget: ${total_hiring_cost:,.0f}"
            can_afford = True
        elif available_cash >= total_hiring_cost:
            recommendation = f"Cash flow (${available_cash:,.0f}) can support hiring but with limited buffer. Consider reducing to {int(open_positions * 0.8)} positions."
            can_afford = True
        else:
            recommendation = f"Limited cash flow (${available_cash:,.0f}) may not support all {open_positions} positions. Recommended: {int(available_cash / avg_hiring_cost)} positions."
            can_afford = False
        
        return {
            "available_cash": available_cash,
            "open_positions": open_positions,
            "estimated_hiring_cost": total_hiring_cost,
            "can_afford": can_afford,
            "recommendation": recommendation
        }


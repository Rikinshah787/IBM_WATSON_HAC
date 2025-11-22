"""
Action trigger logic
Handles automated actions like approvals, alerts, task assignments
"""

import logging
from typing import Dict, Any, List
from app.models.schemas import Action

logger = logging.getLogger(__name__)


class ActionTrigger:
    """Triggers automated actions based on insights"""
    
    def __init__(self):
        """Initialize action trigger"""
        logger.info("🔧 ActionTrigger created")
    
    async def trigger_actions(
        self,
        intent: str,
        data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> List[Action]:
        """
        Trigger actions based on intent and data
        
        Args:
            intent: Detected intent
            data: Processed data
            context: Additional context
        
        Returns:
            List of triggered actions
        """
        logger.info(f"⚡ Triggering actions for intent: {intent}")
        
        actions = []
        
        # Auto-approval actions
        if "approve" in intent.lower():
            actions.extend(await self._trigger_approval_actions(data))
        
        # Alert actions
        if "alert" in intent.lower() or "risk" in intent.lower():
            actions.extend(await self._trigger_alert_actions(data))
        
        # Task assignment actions
        if "assign" in intent.lower() or "task" in intent.lower():
            actions.extend(await self._trigger_task_actions(data))
        
        logger.info(f"✅ Triggered {len(actions)} actions")
        return actions
    
    async def _trigger_approval_actions(self, data: Dict[str, Any]) -> List[Action]:
        """Trigger approval actions"""
        actions = []
        
        approved_items = data.get("approved_invoices", []) or data.get("approved_items", [])
        for item in approved_items[:10]:  # Limit to 10
            actions.append(
                Action(
                    action_type="approve_invoice",
                    target=f"invoice: {item.get('id', 'unknown')}",
                    parameters={"invoice_id": item.get("id"), "amount": item.get("amount")},
                    status="completed"
                )
            )
        
        return actions
    
    async def _trigger_alert_actions(self, data: Dict[str, Any]) -> List[Action]:
        """Trigger alert actions"""
        actions = []
        
        high_risk_items = data.get("high_risk_departments", []) or data.get("high_risk_tickets", [])
        for item in high_risk_items[:5]:  # Limit to 5
            if isinstance(item, str):
                actions.append(
                    Action(
                        action_type="send_alert",
                        target=f"department: {item}",
                        parameters={"department": item, "severity": "high"},
                        status="completed"
                    )
                )
        
        return actions
    
    async def _trigger_task_actions(self, data: Dict[str, Any]) -> List[Action]:
        """Trigger task assignment actions"""
        actions = []
        
        urgent_items = data.get("urgent_deals", []) or data.get("high_risk_tickets", [])
        for item in urgent_items[:5]:  # Limit to 5
            item_id = item.get("id") if isinstance(item, dict) else str(item)
            actions.append(
                Action(
                    action_type="assign_task",
                    target=f"item: {item_id}",
                    parameters={"item_id": item_id, "priority": "high"},
                    status="completed"
                )
            )
        
        return actions


"""
core/orch_b.py
OrchB: Human-Facing orchestrator for permissions, escalation & user interaction.
"""

from typing import Dict, List, Any, Tuple
from datetime import datetime
from .agent_utils import PermissionLevel, ThreatLevel, AuditLogger


class OrchB:
    """
    Human-Facing Agent
    - Manages user permissions (Observe/Alert/Analyze/Isolate/Auto-Respond)
    - Handles escalation prompts for sensitive actions
    - Integrates user feedback for OrchA learning
    - Translates alerts to user-friendly output
    """
    
    def __init__(self, audit_logger: AuditLogger, user_config: Dict[str, Any] = None):
        self.audit_logger = audit_logger
        self.user_config = user_config or {}
        
        # Current user permission level (default: OBSERVE)
        self.permission_level = PermissionLevel.OBSERVE
        
        # Track user decisions
        self.user_decisions = []
        
        self.logger_name = "OrchB"
    
    def set_permission_level(self, level: PermissionLevel):
        """Set user's overall permission level."""
        self.permission_level = level
        self.audit_logger.log_decision(
            agent=self.logger_name,
            decision="set_permission_level",
            details={"new_level": level.value}
        )
    
    def check_permission(self, action: str, widget: str = None) -> Tuple[bool, str]:
        """
        Check if user has permission to perform action.
        Returns (allowed, reason).
        """
        
        action_requirements = {
            "observe": PermissionLevel.OBSERVE,
            "alert": PermissionLevel.ALERT,
            "analyze": PermissionLevel.ANALYZE,
            "isolate": PermissionLevel.ISOLATE,
            "auto_respond": PermissionLevel.AUTO_RESPOND,
        }
        
        required_level = action_requirements.get(action, PermissionLevel.OBSERVE)
        
        # Check if user has sufficient permissions
        perm_order = [
            PermissionLevel.OBSERVE,
            PermissionLevel.ALERT,
            PermissionLevel.ANALYZE,
            PermissionLevel.ISOLATE,
            PermissionLevel.AUTO_RESPOND
        ]
        
        user_index = perm_order.index(self.permission_level)
        required_index = perm_order.index(required_level)
        
        allowed = user_index >= required_index
        reason = f"User permission: {self.permission_level.value}, required: {required_level.value}"
        
        self.audit_logger.log_decision(
            agent=self.logger_name,
            decision="check_permission",
            details={
                "action": action,
                "widget": widget,
                "allowed": allowed,
                "reason": reason
            }
        )
        
        return allowed, reason
    
    def request_user_approval(self, action: str, details: str) -> bool:
        """
        Prompt user for approval on sensitive actions.
        Returns True if approved, False if denied.
        """
        
        prompt = f"⚠️  {action}: {details}\nAllow? [Y/n]: "
        user_input = input(prompt).lower().strip()
        
        approved = user_input in ['y', 'yes', '']
        
        decision_record = {
            "action": action,
            "details": details,
            "approved": approved,
            "timestamp": datetime.now().isoformat()
        }
        
        self.user_decisions.append(decision_record)
        
        self.audit_logger.log_decision(
            agent=self.logger_name,
            decision="user_approval",
            details=decision_record
        )
        
        return approved
    
    def handle_alert(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle analyzed alert based on threat level.
        Applies permission checks and generates user output.
        """
        
        threat_level = ThreatLevel[analysis["threat_level"].upper()]
        action_map = {
            ThreatLevel.LOW: "log_only",
            ThreatLevel.MEDIUM: "prompt_user",
            ThreatLevel.HIGH: "isolate_alert"
        }
        
        action = action_map[threat_level]
        
        result = {
            "event_id": analysis["event_id"],
            "action": action,
            "message": f"[{threat_level.value.upper()}] {analysis['reasoning']}"
        }
        
        # Check permission for action
        allowed, reason = self.check_permission(action)
        
        if not allowed and action != "log_only":
            result["status"] = "denied"
            result["reason"] = reason
        else:
            result["status"] = "approved"
        
        self.audit_logger.log_alert(
            alert_id=analysis["event_id"],
            level=threat_level,
            message=result["message"],
            context=analysis
        )
        
        return result
    
    def get_user_feedback(self, event_id: str) -> str:
        """
        Prompt user to mark alert as false positive or confirmed threat.
        """
        
        feedback_prompt = f"\n📝 Mark event {event_id} as:\n[1] False positive\n[2] Confirmed threat\n[3] Skip\nChoice [1-3]: "
        choice = input(feedback_prompt).strip()
        
        feedback_map = {
            "1": "false_positive",
            "2": "confirmed_threat",
            "3": "skip"
        }
        
        feedback = feedback_map.get(choice, "skip")
        
        if feedback != "skip":
            self.audit_logger.log_decision(
                agent=self.logger_name,
                decision="user_feedback",
                details={"event_id": event_id, "feedback": feedback}
            )
        
        return feedback
    
    def get_stats(self) -> Dict[str, Any]:
        """Return OrchB statistics."""
        return {
            "current_permission_level": self.permission_level.value,
            "user_decisions_count": len(self.user_decisions),
            "recent_decisions": self.user_decisions[-5:] if self.user_decisions else []
        }
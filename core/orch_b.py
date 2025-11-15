"""
core/orch_b.py
OrchB: Human-Facing orchestrator for permissions, escalation & user interaction.
Bridges OrchA decisions with human approval & feedback loops.
"""

from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
from .agent_utils import (
    PermissionLevel, ThreatLevel, AuditLogger, Decision, ThreatScore
)


class OrchB:
    """
    Human-Facing Agent (Human-AI Bridge)
    - Manages user permissions (Observe/Alert/Analyze/Isolate/Auto-Respond)
    - Handles escalation prompts for sensitive actions
    - Integrates user feedback for OrchA learning
    - Translates alerts to user-friendly output
    - Bridges dispatcher execution with human approval
    """
    
    def __init__(self, audit_logger: AuditLogger, user_config: Dict[str, Any] = None):
        self.audit_logger = audit_logger
        self.user_config = user_config or {}
        
        # Current user permission level (default: OBSERVE)
        self.permission_level = PermissionLevel.OBSERVE
        
        # Track user decisions for learning
        self.user_decisions = []
        self.approved_actions = []
        self.denied_actions = []
        
        # Escalation history
        self.escalations = []
        
        # User preferences
        self.auto_approve_thresholds = self.user_config.get("auto_approve", {
            "low": True,
            "medium": False,
            "high": False
        })
        
        self.logger_name = "OrchB"
        self.active = False
    
    def start(self):
        """Activate OrchB."""
        self.active = True
        print(f"   ✓ {self.logger_name} activated")
        return True
    
    def stop(self):
        """Deactivate OrchB."""
        self.active = False
        print(f"   ✓ {self.logger_name} deactivated")
        return True
    
    def set_permission_level(self, level: PermissionLevel):
        """Set user's overall permission level."""
        old_level = self.permission_level
        self.permission_level = level
        
        # Simple audit logging (with UTF-8 encoding)
        with open("logs/audit.log", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().isoformat()}] PERMISSION_CHANGE: {old_level.value} -> {level.value}\n")
        
        print(f"   ✓ Permission level changed: {old_level.value} -> {level.value}")
    
    def check_permission(self, action: str, threat_level: ThreatLevel = None, widget: str = None) -> Tuple[bool, str]:
        """Check if user has permission to perform action."""
        action_requirements = {
            "observe": PermissionLevel.OBSERVE,
            "alert": PermissionLevel.ALERT,
            "analyze": PermissionLevel.ANALYZE,
            "isolate": PermissionLevel.ISOLATE,
            "quarantine": PermissionLevel.ISOLATE,
            "process_kill": PermissionLevel.ISOLATE,
            "network_block": PermissionLevel.ISOLATE,
            "auto_respond": PermissionLevel.AUTO_RESPOND,
        }
        
        required_level = action_requirements.get(action, PermissionLevel.OBSERVE)
        
        perm_order = [
            PermissionLevel.OBSERVE,
            PermissionLevel.ALERT,
            PermissionLevel.ANALYZE,
            PermissionLevel.ISOLATE,
            PermissionLevel.AUTO_RESPOND
        ]
        
        try:
            user_index = perm_order.index(self.permission_level)
            required_index = perm_order.index(required_level)
            allowed = user_index >= required_index
        except ValueError:
            allowed = False
        
        reason = f"User: {self.permission_level.value} | Required: {required_level.value}"
        return allowed, reason
    
    def evaluate_escalation(self, decision: Decision, threat_level: ThreatLevel) -> bool:
        """Determine if decision needs human escalation."""
        if self.permission_level == PermissionLevel.AUTO_RESPOND:
            return False
        
        if threat_level == ThreatLevel.HIGH:
            return True
        
        if threat_level == ThreatLevel.MEDIUM:
            return not self.auto_approve_thresholds.get("medium", False)
        
        if threat_level == ThreatLevel.LOW:
            return not self.auto_approve_thresholds.get("low", True)
        
        return True
    
    def escalate_to_user(self, decision: Decision, threat_level: ThreatLevel, context: Dict) -> bool:
        """Escalate decision to user for approval."""
        escalation_entry = {
            "timestamp": datetime.now().isoformat(),
            "threat_level": threat_level.value,
            "recommended_action": decision.action,
            "confidence": decision.confidence,
            "reasoning": decision.reasoning
        }
        self.escalations.append(escalation_entry)
        
        prompt_text = f"""
╔════════════════════════════════════════════════════╗
║           ⚠️  ESCALATION REQUIRED                 ║
╚════════════════════════════════════════════════════╝

🔴 Threat Level: {threat_level.value.upper()}
📊 Confidence: {decision.confidence*100:.1f}%
💡 Recommended Action: {decision.action}
📝 Reason: {decision.reasoning}

Context:
{self._format_context(context)}

════════════════════════════════════════════════════

Allow action? [Y/n]: """
        
        user_input = input(prompt_text).lower().strip()
        approved = user_input in ['y', 'yes', '']
        
        decision_record = {
            "decision_id": decision.decision_id,
            "action": decision.action,
            "approved": approved,
            "timestamp": datetime.now().isoformat()
        }
        
        if approved:
            self.approved_actions.append(decision_record)
            print("   ✅ Action approved")
        else:
            self.denied_actions.append(decision_record)
            print("   ❌ Action denied")
        
        self.user_decisions.append(decision_record)
        
        # Simple audit logging (with UTF-8 encoding)
        with open("logs/audit.log", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().isoformat()}] USER_APPROVAL: {decision.action} - {approved}\n")
        
        return approved
    
    def get_user_feedback(self, event_id: str, orcha_score: int = None) -> Optional[str]:
        """Prompt user to provide feedback for learning."""
        feedback_prompt = f"""
📝 Feedback for event {event_id}
{'   (OrchA score: '+str(orcha_score)+'%)' if orcha_score else ''}

[1] False positive (should NOT have alerted)
[2] Confirmed threat (good catch!)
[3] Missed details (needs refinement)
[4] Skip

Choice [1-4]: """
        
        choice = input(feedback_prompt).strip()
        
        feedback_map = {
            "1": "false_positive",
            "2": "confirmed_threat",
            "3": "missed_details",
            "4": None
        }
        
        feedback = feedback_map.get(choice)
        
        if feedback:
            # Simple audit logging (with UTF-8 encoding)
            with open("logs/audit.log", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now().isoformat()}] USER_FEEDBACK: {event_id} - {feedback}\n")
            print(f"   ✓ Feedback recorded: {feedback}")
        
        return feedback
    
    def format_alert(self, analysis: Dict[str, Any]) -> str:
        """Convert threat analysis to user-friendly alert."""
        threat_level = analysis.get("threat_level", "unknown").upper()
        source = analysis.get("source", "unknown")
        reasoning = analysis.get("reasoning", "Unknown reason")
        
        alert = f"""
🚨 [{threat_level}] Security Alert
   Source: {source}
   Event: {analysis.get('event_type', 'unknown')}
   Reason: {reasoning}
   Confidence: {analysis.get('confidence_score', 0)}%
"""
        return alert
    
    def _format_context(self, context: Dict) -> str:
        """Format context dict for readable display."""
        lines = []
        for key, value in context.items():
            if isinstance(value, dict):
                lines.append(f"  {key}:")
                for k, v in value.items():
                    lines.append(f"    - {k}: {v}")
            else:
                lines.append(f"  {key}: {value}")
        return "\n".join(lines)
    
    def get_stats(self) -> Dict[str, Any]:
        """Return OrchB statistics."""
        return {
            "agent_name": self.logger_name,
            "active": self.active,
            "current_permission_level": self.permission_level.value,
            "approved_actions": len(self.approved_actions),
            "denied_actions": len(self.denied_actions),
            "escalations_handled": len(self.escalations),
            "total_user_decisions": len(self.user_decisions),
            "recent_decisions": [d for d in self.user_decisions[-5:]] if self.user_decisions else []
        }
    
    def get_approval_stats(self) -> Dict[str, Any]:
        """Get approval/denial statistics."""
        total = len(self.user_decisions)
        if total == 0:
            return {"total": 0, "approval_rate": "N/A"}
        
        approval_rate = (len(self.approved_actions) / total) * 100
        
        return {
            "total_decisions": total,
            "approved": len(self.approved_actions),
            "denied": len(self.denied_actions),
            "approval_rate": f"{approval_rate:.1f}%"
        }

"""
core/orch_a.py
OrchA: AI Task Master orchestrator for threat analysis & scoring.
"""

from typing import Dict, List, Any
from datetime import datetime
from .agent_utils import Event, ThreatLevel, AuditLogger, PermissionLevel
import json


class OrchA:
    """
    AI Task Master Agent
    - Consumes sensor signals from widgets
    - Routes to AI inference (local LLM)
    - Assigns threat levels based on confidence thresholds
    - Maintains audit log and learning feedback
    """
    
    def __init__(self, audit_logger: AuditLogger, config: Dict[str, Any] = None):
        self.audit_logger = audit_logger
        self.config = config or {}
        
        # Confidence thresholds
        self.threat_thresholds = {
            ThreatLevel.LOW: (0, 60),      # < 60% = LOW
            ThreatLevel.MEDIUM: (60, 85),  # 60-85% = MEDIUM
            ThreatLevel.HIGH: (85, 100)    # > 85% = HIGH
        }
        
        # False positive tracking (for learning)
        self.false_positives = []
        self.learning_history = []
        
        self.logger_name = "OrchA"
    
    def analyze_event(self, event: Event) -> Dict[str, Any]:
        """
        Analyze incoming event and assign threat score.
        In MVP: simple heuristics. Later: LLM inference.
        """
        
        # Simple scoring logic for MVP
        confidence_score = self._score_event(event)
        threat_level = self._assign_threat_level(confidence_score)
        
        # Create analysis result
        analysis = {
            "event_id": event.event_id,
            "source": event.source,
            "confidence_score": confidence_score,
            "threat_level": threat_level.value,
            "timestamp": datetime.now().isoformat(),
            "reasoning": f"Event type '{event.event_type}' scored {confidence_score}%"
        }
        
        # Log decision
        self.audit_logger.log_decision(
            agent=self.logger_name,
            decision="analyze_event",
            details=analysis
        )
        
        return analysis
    
    def _score_event(self, event: Event) -> int:
        """
        Score event threat level (0-100).
        MVP: simple heuristics based on event type.
        Future: LLM-based scoring via Ollama.
        """
        
        payload = event.payload
        
        # File Integrity Widget scoring
        if event.source == "file_integrity":
            # High-risk paths get higher scores
            path = payload.get("path", "")
            if "system" in path.lower() or "windows" in path.lower():
                return 75  # MEDIUM/HIGH
            elif "project" in path.lower() or "user" in path.lower():
                return 30  # LOW
            return 40
        
        # Process Monitor Widget scoring
        elif event.source == "process_monitor":
            process_name = payload.get("process_name", "")
            # Suspicious processes
            if any(x in process_name.lower() for x in ["powershell", "cmd", "wscript"]):
                return 65  # MEDIUM
            return 35
        
        # Network Sniffer Widget scoring
        elif event.source == "network_sniffer":
            ip = payload.get("destination_ip", "")
            # Known public clouds = lower risk
            if any(x in ip for x in ["8.8.8.8", "1.1.1.1"]):
                return 20
            return 50  # Unknown = medium caution
        
        # Default
        return 45
    
    def _assign_threat_level(self, score: int) -> ThreatLevel:
        """Assign threat level based on confidence score."""
        if score < 60:
            return ThreatLevel.LOW
        elif score < 85:
            return ThreatLevel.MEDIUM
        else:
            return ThreatLevel.HIGH
    
    def learn_from_feedback(self, event_id: str, feedback: str):
        """
        Learn from user feedback (e.g., false positive marking).
        Adjusts future scoring logic.
        """
        
        feedback_entry = {
            "event_id": event_id,
            "feedback": feedback,  # "false_positive", "confirmed_threat", etc.
            "timestamp": datetime.now().isoformat()
        }
        
        self.learning_history.append(feedback_entry)
        
        if feedback == "false_positive":
            self.false_positives.append(event_id)
        
        self.audit_logger.log_decision(
            agent=self.logger_name,
            decision="learn_from_feedback",
            details=feedback_entry
        )
    
    def get_stats(self) -> Dict[str, Any]:
        """Return OrchA statistics."""
        return {
            "false_positives_tracked": len(self.false_positives),
            "learning_entries": len(self.learning_history),
            "threat_thresholds": {k.value: v for k, v in self.threat_thresholds.items()}
        }
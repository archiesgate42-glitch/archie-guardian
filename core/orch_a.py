"""
core/orch_a.py
OrchA: AI Task Master orchestrator for threat analysis & scoring.
Bridges widgets → threat intelligence → action dispatcher
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from .agent_utils import (
    Event, ThreatLevel, AuditLogger, PermissionLevel, 
    ThreatScore, Decision, EventQueue
)
import json


class OrchA:
    """
    AI Task Master Agent
    - Consumes sensor signals from widgets
    - Routes to AI inference (local LLM)
    - Assigns threat levels based on confidence thresholds
    - Maintains audit log and learning feedback
    - Integrates with dispatcher for action execution
    """
    
    def __init__(self, audit_logger: AuditLogger, config: Dict[str, Any] = None):
        self.audit_logger = audit_logger
        self.config = config or {}
        self.event_queue = EventQueue()
        
        # Threat thresholds (in percentages)
        self.threat_thresholds = {
            ThreatLevel.LOW: (0, 60),      # < 60% = LOW
            ThreatLevel.MEDIUM: (60, 85),  # 60-85% = MEDIUM
            ThreatLevel.HIGH: (85, 100)    # > 85% = HIGH
        }
        
        # Learning & feedback tracking
        self.false_positives = []
        self.learning_history = []
        self.threat_patterns = {}  # Pattern recognition
        
        # Decision history (for audit trail)
        self.decisions = []
        
        self.logger_name = "OrchA"
        self.active = False
    
    def start(self):
        """Activate OrchA."""
        self.active = True
        print(f"   ✓ {self.logger_name} activated")
        return True
    
    def stop(self):
        """Deactivate OrchA."""
        self.active = False
        print(f"   ✓ {self.logger_name} deactivated")
        return True
    
    def ingest_event(self, event: Event):
        """Push event into processing queue."""
        if not self.active:
            return
        self.event_queue.push(event)
    
    def process_events(self) -> List[Decision]:
        """Process all unprocessed events, return decisions."""
        decisions = []
        unprocessed = self.event_queue.get_all_unprocessed()
        
        for event in unprocessed:
            try:
                analysis = self.analyze_event(event)
                
                # Mark as processed
                event.processed = True
                
                # Generate decision if threat detected
                if analysis["threat_level"] in ["medium", "high"]:
                    decision = self._generate_decision(event, analysis)
                    decisions.append(decision)
                    self.decisions.append(decision)
            except Exception as e:
                self.audit_logger.log_alert(
                    alert_id=f"orcha_error_{event.event_id}",
                    level=ThreatLevel.LOW,
                    message=f"Error processing event: {e}",
                    context={"event": event.to_dict()}
                )
        
        return decisions
    
    def analyze_event(self, event: Event) -> Dict[str, Any]:
        """
        Analyze incoming event and assign threat score.
        MVP: heuristic-based. Future: LLM via Ollama/local models.
        """
        
        # Score the event (0-100)
        confidence_score = self._score_event(event)
        threat_level = self._assign_threat_level(confidence_score)
        
        # Breakdown of scoring factors
        factors = self._get_score_factors(event)
        
        analysis = {
            "event_id": event.event_id,
            "source": event.source,
            "event_type": event.event_type,
            "confidence_score": confidence_score,
            "threat_level": threat_level.value,
            "factors": factors,
            "timestamp": datetime.now().isoformat(),
            "reasoning": f"Event '{event.event_type}' from {event.source} scored {confidence_score}% threat"
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
        MVP: heuristics. Future: LLM-based scoring.
        """
        
        payload = event.payload
        base_score = 0
        
        # File Integrity Widget scoring
        if event.source == "file_integrity":
            event_type = payload.get("event_type", "")
            path = payload.get("path", "").lower()
            
            # High-risk operations
            if event_type == "modified":
                base_score = 40
            elif event_type in ["created", "deleted"]:
                base_score = 30
            
            # High-risk paths
            if any(x in path for x in ["system32", "windows", "program files"]):
                base_score += 30
            elif any(x in path for x in [".exe", ".dll", ".sys"]):
                base_score += 20
            
            return min(base_score, 100)
        
        # Process Monitor Widget scoring
        elif event.source == "process_monitor":
            process_name = payload.get("name", "").lower()
            
            # Suspicious process names
            suspicious = ["powershell", "cmd.exe", "wscript", "cscript", "regsrv32"]
            if any(x in process_name for x in suspicious):
                base_score = 70
            else:
                base_score = 25
            
            # Parent process context (if available)
            if "parent" in payload:
                if payload["parent"] in suspicious:
                    base_score += 20
            
            return min(base_score, 100)
        
        # Network Sniffer Widget scoring
        elif event.source == "network_sniffer":
            remote_addr = payload.get("remote_address", "")
            process = payload.get("process", "").lower()
            
            # Suspicious processes making network calls
            if any(x in process for x in ["powershell", "cmd", "wscript"]):
                base_score = 75
            
            # Known safe destinations
            if any(x in remote_addr for x in ["8.8.8.8", "1.1.1.1", "127.0.0.1"]):
                base_score = max(base_score - 30, 0)
            
            return min(base_score, 100)
        
        # Windows Defender widget scoring
        elif event.source == "windows_defender":
            threats_found = payload.get("threats_found", 0)
            scan_type = payload.get("scan_type", "")
            
            if threats_found > 0:
                base_score = 80 + min(threats_found * 5, 20)
            else:
                base_score = 10
            
            return min(base_score, 100)
        
        # RRNC widget scoring
        elif event.source == "rrnc":
            action = payload.get("action", "")
            
            if action in ["process_kill", "quarantine"]:
                base_score = 85  # RRNC already made a decision
            elif action == "capture_forensics":
                base_score = 75
            
            return min(base_score, 100)
        
        # Default
        return 45
    
    def _get_score_factors(self, event: Event) -> Dict[str, float]:
        """Return breakdown of threat factors."""
        factors = {}
        
        if event.source == "file_integrity":
            payload = event.payload
            path = payload.get("path", "").lower()
            
            if "system" in path:
                factors["system_path"] = 0.8
            if ".exe" in path or ".dll" in path:
                factors["executable"] = 0.7
            factors["modification"] = 0.6
        
        elif event.source == "process_monitor":
            process = payload.get("name", "").lower()
            if "powershell" in process or "cmd" in process:
                factors["suspicious_process"] = 0.9
        
        elif event.source == "network_sniffer":
            factors["network_activity"] = 0.6
        
        return factors
    
    def _assign_threat_level(self, score: int) -> ThreatLevel:
        """Assign threat level based on confidence score."""
        if score < 60:
            return ThreatLevel.LOW
        elif score < 85:
            return ThreatLevel.MEDIUM
        else:
            return ThreatLevel.HIGH
    
    def _generate_decision(self, event: Event, analysis: Dict) -> Decision:
        """Generate actionable decision from analysis."""
        threat_level = ThreatLevel[analysis["threat_level"].upper()]
        
        # Recommend action based on threat
        action = "escalate"  # Default: escalate to OrchB/human
        
        if threat_level == ThreatLevel.HIGH:
            action = "quarantine"  # Auto-isolate high threats
        elif threat_level == ThreatLevel.MEDIUM:
            action = "alert"  # Alert human
        
        decision = Decision(
            agent=self.logger_name,
            action=action,
            confidence=analysis["confidence_score"] / 100.0,
            reasoning=analysis["reasoning"]
        )
        
        return decision
    
    def learn_from_feedback(self, event_id: str, feedback: str, correct_classification: str = None):
        """
        Learn from user feedback to improve future scoring.
        Feedback: "false_positive", "confirmed_threat", "missed_threat"
        """
        
        feedback_entry = {
            "event_id": event_id,
            "feedback": feedback,
            "correct_classification": correct_classification,
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
            "agent_name": self.logger_name,
            "active": self.active,
            "events_queued": len(self.event_queue.queue),
            "decisions_made": len(self.decisions),
            "false_positives_tracked": len(self.false_positives),
            "learning_entries": len(self.learning_history),
            "threat_thresholds": {k.value: v for k, v in self.threat_thresholds.items()}
        }
    
    def get_recent_decisions(self, limit: int = 10) -> List[Dict]:
        """Get recent decisions for audit trail."""
        return [d.to_dict() for d in self.decisions[-limit:]]
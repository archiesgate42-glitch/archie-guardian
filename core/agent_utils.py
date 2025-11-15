"""
core/agent_utils.py
Utility functions and base classes for Archie Guardian agents.
"""

import logging
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from enum import Enum


# ============================================================================
# Permission Levels
# ============================================================================

class PermissionLevel(Enum):
    """Tiered permission model."""
    OBSERVE = "observe"           # Read-only
    ALERT = "alert"               # Can notify
    ANALYZE = "analyze"           # Can analyze context
    ISOLATE = "isolate"           # Can quarantine
    AUTO_RESPOND = "auto_respond"  # Automatic actions


# ============================================================================
# Threat Levels
# ============================================================================

class ThreatLevel(Enum):
    """Alert severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# ============================================================================
# Decision Models
# ============================================================================

class Decision:
    """AI agent decision with reasoning & confidence."""
    
    def __init__(self, agent: str, action: str, confidence: float = 0.5, reasoning: str = ""):
        self.agent = agent
        self.action = action
        self.confidence = confidence  # 0-1.0
        self.reasoning = reasoning
        self.timestamp = datetime.now()
        self.decision_id = f"dec_{int(self.timestamp.timestamp() * 1000)}"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "agent": self.agent,
            "action": self.action,
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "timestamp": self.timestamp.isoformat()
        }


class ThreatScore:
    """Threat assessment with breakdown."""
    
    def __init__(self, threat_level: ThreatLevel, score: float, factors: Dict[str, float] = None):
        self.threat_level = threat_level
        self.score = score  # 0-100
        self.factors = factors or {}  # e.g., {"process_anomaly": 0.8, "network_suspicious": 0.6}
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "threat_level": self.threat_level.value,
            "score": self.score,
            "factors": self.factors,
            "timestamp": self.timestamp.isoformat()
        }


# ============================================================================
# Audit Logger (Enhanced)
# ============================================================================

class AuditLogger:
    """Centralized audit trail for all Guardian decisions."""
    
    def __init__(self, log_file: str = "logs/audit.log"):
        self.log_file = log_file
        self.logger = logging.getLogger("ArchieGuardian.Audit")
        
        # Create file handler
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            '[%(asctime)s] %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def log_decision(self, decision: Decision):
        """Log an agent decision with context."""
        self.logger.info(f"DECISION: {json.dumps(decision.to_dict())}")
    
    def log_alert(self, alert_id: str, level: ThreatLevel, message: str, context: Dict):
        """Log a security alert."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "alert_id": alert_id,
            "level": level.value,
            "message": message,
            "context": context
        }
        self.logger.warning(f"ALERT: {json.dumps(entry)}")
    
    def log_action_executed(self, widget: str, action: str, result: Dict):
        """Log an action execution."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "widget": widget,
            "action": action,
            "result": result
        }
        self.logger.info(f"ACTION: {json.dumps(entry)}")


# ============================================================================
# Event Model (Enhanced)
# ============================================================================

class Event:
    """Base class for system events detected by widgets."""
    
    def __init__(self, event_type: str, source: str, payload: Dict[str, Any], severity: str = "info"):
        self.event_type = event_type
        self.source = source  # e.g., "file_integrity", "process_monitor"
        self.payload = payload
        self.severity = severity  # info, warning, critical
        self.timestamp = datetime.now()
        self.event_id = f"{source}_{int(self.timestamp.timestamp() * 1000)}"
        self.processed = False  # Track if OrchA has analyzed
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "source": self.source,
            "severity": self.severity,
            "timestamp": self.timestamp.isoformat(),
            "payload": self.payload,
            "processed": self.processed
        }


class EventQueue:
    """Thread-safe event queue for widget->orchestrator flow."""
    
    def __init__(self, max_size: int = 1000):
        self.queue: List[Event] = []
        self.max_size = max_size
    
    def push(self, event: Event):
        """Add event to queue."""
        self.queue.append(event)
        if len(self.queue) > self.max_size:
            self.queue = self.queue[-self.max_size:]
    
    def pop(self) -> Optional[Event]:
        """Get next unprocessed event."""
        for event in self.queue:
            if not event.processed:
                return event
        return None
    
    def get_all_unprocessed(self) -> List[Event]:
        """Get all unprocessed events."""
        return [e for e in self.queue if not e.processed]


# ============================================================================
# Config Loader (Enhanced)
# ============================================================================

import yaml

class ConfigLoader:
    """Load manifest & user config from YAML."""
    
    @staticmethod
    def load_manifest(path: str = "config/manifest.yaml") -> Dict[str, Any]:
        """Load widget manifest."""
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            logging.warning(f"Manifest not found at {path}. Using defaults.")
            return {}
    
    @staticmethod
    def load_user_config(path: str = "config/user_config.yaml") -> Dict[str, Any]:
        """Load user settings."""
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            logging.warning(f"User config not found at {path}. Using defaults.")
            return {
                "permission_level": "observe",
                "auto_respond": False,
                "alert_threshold": 0.75
            }
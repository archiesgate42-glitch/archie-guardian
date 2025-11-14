"""
core/agent_utils.py
Utility functions and base classes for Archie Guardian agents.
"""

import logging
import json
from datetime import datetime
from typing import Dict, List, Any
from enum import Enum

# ============================================================================
# Permission Levels
# ============================================================================

class PermissionLevel(Enum):
    """Tiered permission model."""
    OBSERVE = "observe"  # Read-only
    ALERT = "alert"      # Can notify
    ANALYZE = "analyze"  # Can analyze context
    ISOLATE = "isolate"  # Can quarantine
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
# Audit Logger
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
    
    def log_decision(self, agent: str, decision: str, details: Dict[str, Any]):
        """Log an agent decision with context."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "decision": decision,
            "details": details
        }
        self.logger.info(json.dumps(entry))
    
    def log_alert(self, alert_id: str, level: ThreatLevel, message: str, context: Dict):
        """Log a security alert."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "alert_id": alert_id,
            "level": level.value,
            "message": message,
            "context": context
        }
        self.logger.warning(json.dumps(entry))


# ============================================================================
# Event Model
# ============================================================================

class Event:
    """Base class for system events detected by widgets."""
    
    def __init__(self, event_type: str, source: str, payload: Dict[str, Any]):
        self.event_type = event_type
        self.source = source  # e.g., "file_integrity", "process_monitor"
        self.payload = payload
        self.timestamp = datetime.now()
        self.event_id = f"{source}_{int(self.timestamp.timestamp() * 1000)}"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "source": self.source,
            "timestamp": self.timestamp.isoformat(),
            "payload": self.payload
        }


# ============================================================================
# Config Loader
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
            print(f"Manifest not found at {path}. Using defaults.")
            return {}
    
    @staticmethod
    def load_user_config(path: str = "config/user_config.yaml") -> Dict[str, Any]:
        """Load user settings."""
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            print(f"User config not found at {path}. Using defaults.")
            return {}
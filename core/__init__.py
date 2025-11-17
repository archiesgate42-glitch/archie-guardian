"""
core package for Archie Guardian
Contains orchestrator, utilities, and AI components
"""

__version__ = "1.0"

try:
    from .agent_utils import AuditLogger, PermissionLevel, ThreatLevel
    from .orch_a import OrchA
    from .orch_b import OrchB
    from .orchestrator import MasterOrchestrator
    from .ollama_connector import OllamaConnector
except ImportError as e:
    print(f"Warning: Could not import all core modules: {e}")

__all__ = [
    "AuditLogger",
    "PermissionLevel",
    "ThreatLevel",
    "OrchA",
    "OrchB",
    "MasterOrchestrator",
    "OllamaConnector",
]
__docformat__ = "restructuredtext"
__author__ = "Archie Guardian Team"
__credits__ = ["Archie Guardian Contributors"]
__license__ = "MIT"
__maintainer__ = "Archie Guardian Team"

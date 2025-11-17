"""
Archie Guardian: Local AI-driven host-based security monitoring system with real-time threat detection, multi-agent orchestration, and interactive Ollama chat for behavioral analysis.

Package: core
Contains orchestrator, utilities, and AI components (OrchA, OrchB, Ollama connector)
"""

__version__ = "1.0"
__author__ = "Archie Gate (Louis J.)"
__email__ = "archiesgate42@gmail.com"
__license__ = "MIT"
__docformat__ = "restructuredtext"

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

# Project Description
PROJECT_DESCRIPTION = """
Archie Guardian v1.0

A local, transparent, AI-driven host-based security monitoring system featuring:
- Real-time monitoring: File Integrity, Process Monitor, Network Sniffer
- Multi-agent AI orchestration: OrchA (threat analysis) + OrchB (human-AI bridge)
- Local LLM inference: Ollama (Llama3) for security event analysis
- Interactive CLI: Commands, events, audit logs, and direct AI chat
- Privacy-first: 100% local processing, no cloud dependencies
- Granular permissions: Observe → Alert → Analyze → Isolate → Auto-Respond

Philosophy: Transparent. Autonomous. Community-driven.
"""
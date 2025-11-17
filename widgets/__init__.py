"""
Archie Guardian: Local AI-driven host-based security monitoring system with real-time threat detection, multi-agent orchestration, and interactive Ollama chat for behavioral analysis.

Package: widgets
Contains all security monitoring sensors and AI chat interface (File, Process, Network, Defender, RRNC, Ollama)
"""

__version__ = "1.0"
__author__ = "Archie Gate (Louis J.)"
__license__ = "MIT"

try:
    from .file_integrity import FileIntegrityWidget
    from .process_monitor import ProcessMonitorWidget
    from .network_sniffer import NetworkSnifferWidget
    from .windows_defender import WindowsDefenderWidget
    from .rrnc import RapidResponseNeutralizeCapture
    from .ollama_chat import OllamaChatWidget
except ImportError as e:
    print(f"Warning: Could not import all widgets: {e}")

__all__ = [
    "FileIntegrityWidget",
    "ProcessMonitorWidget",
    "NetworkSnifferWidget",
    "WindowsDefenderWidget",
    "RapidResponseNeutralizeCapture",
    "OllamaChatWidget",
]

# Widgets Overview
WIDGETS_INFO = {
    "file_integrity": "Monitor real-time file changes in system directories",
    "process_monitor": "Detect and track new process spawning events",
    "network_sniffer": "Log network connections and process-to-IP mappings",
    "windows_defender": "Integration with Windows security scans and threats",
    "rrnc": "Rapid Response Neutralize & Capture for threat mitigation",
    "ollama_chat": "Local AI (Llama3) for interactive security analysis via chat",
}
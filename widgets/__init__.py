"""
widgets package for Archie Guardian
Contains all security monitoring widgets
"""

__version__ = "1.0"
__author__ = "Archie Gate"

# Import key widgets for easy access
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

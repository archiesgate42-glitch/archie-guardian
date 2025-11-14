"""
widgets/file_integrity.py
File Integrity Widget: Monitor file changes in specified directories.
Uses Watchdog for efficient filesystem monitoring.
"""

import os
import time
from typing import Dict, List, Any
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileIntegrityHandler(FileSystemEventHandler):
    """Watchdog event handler for file changes."""
    
    def __init__(self, widget_instance):
        self.widget = widget_instance
    
    def on_modified(self, event):
        if not event.is_directory:
            self.widget.record_event("modified", event.src_path)
    
    def on_created(self, event):
        if not event.is_directory:
            self.widget.record_event("created", event.src_path)
    
    def on_deleted(self, event):
        if not event.is_directory:
            self.widget.record_event("deleted", event.src_path)


class FileIntegrityWidget:
    """
    File Integrity Widget - LIVE
    - Monitors file changes in specified directories using Watchdog
    - Generates real-time events for analysis
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        
        # Directories to monitor (customize here)
        self.watch_paths = self.config.get("watch_paths", [
            os.path.expanduser("~/Projects"),
            os.path.expanduser("~/Downloads"),
            os.path.expanduser("~/Documents"),
        ])
        
        # Event buffer (keep last 50 events)
        self.events = []
        self.max_events = 50
        
        # Watchdog observer
        self.observer = Observer()
        self.event_handler = FileIntegrityHandler(self)
        
        self.widget_name = "file_integrity"
        self.enabled = False
    
    def start(self):
        """Start monitoring file changes."""
        try:
            # Only schedule paths that exist
            scheduled_paths = []
            for path in self.watch_paths:
                expanded_path = os.path.expanduser(path)
                if os.path.exists(expanded_path):
                    self.observer.schedule(self.event_handler, expanded_path, recursive=True)
                    scheduled_paths.append(expanded_path)
            
            self.observer.start()
            self.enabled = True
            
            print(f"   🟢 File Integrity Widget: Monitoring {len(scheduled_paths)} paths")
            return True
        except Exception as e:
            print(f"   ❌ Error starting File Integrity Widget: {e}")
            return False
    
    def stop(self):
        """Stop monitoring."""
        try:
            if self.observer.is_alive():
                self.observer.stop()
                self.observer.join(timeout=5)
            self.enabled = False
            return True
        except Exception as e:
            print(f"   ❌ Error stopping widget: {e}")
            return False
    
    def record_event(self, event_type: str, path: str):
        """Record file change event."""
        try:
            event_data = {
                "timestamp": time.time(),
                "event_type": event_type,
                "path": path,
                "file_size": self._get_file_size(path),
                "is_file": os.path.isfile(path)
            }
            
            self.events.append(event_data)
            
            # Keep only last N events
            if len(self.events) > self.max_events:
                self.events = self.events[-self.max_events:]
        except Exception as e:
            pass  # Silently skip errors on individual events
    
    def get_events(self) -> List[Dict[str, Any]]:
        """Return buffered events."""
        return self.events
    
    def get_recent_events(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get most recent N events."""
        return self.events[-count:] if self.events else []
    
    def clear_events(self):
        """Clear event buffer."""
        self.events = []
    
    def _get_file_size(self, path: str) -> int:
        """Get file size if it exists."""
        try:
            if os.path.exists(path):
                return os.path.getsize(path)
        except:
            pass
        return 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Return widget statistics."""
        return {
            "widget_name": self.widget_name,
            "enabled": self.enabled,
            "watched_paths": self.watch_paths,
            "events_buffered": len(self.events),
            "status": "🟢 LIVE" if self.enabled else "⭕ Idle"
        }
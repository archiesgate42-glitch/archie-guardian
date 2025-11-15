# Widget Development Guide

> Learn how to build custom monitoring widgets for Archie Guardian.

---

## 📚 Table of Contents

- [Widget Basics](#widget-basics)
- [Required Interface](#required-interface)
- [Event Structure](#event-structure)
- [Best Practices](#best-practices)
- [Examples](#examples)
- [Testing Your Widget](#testing-your-widget)
- [Integration](#integration)

---

## 🎯 Widget Basics

### What is a Widget?

A **widget** is a modular monitoring sensor that:
- Detects system events (files, processes, network, etc.)
- Buffers events for analysis
- Provides actions (scan, quarantine, etc.)
- Reports statistics

### Widget Lifecycle

```
1. __init__()      Initialize state
   ↓
2. start()         Begin monitoring
   ↓
3. [Event generation loop]
   - Detect events
   - Buffer in memory
   ↓
4. get_recent_events()  Query buffered events
   ↓
5. stop()          Cleanup & shutdown
```

---

## 📋 Required Interface

Every widget MUST implement these methods:

### **`start() -> bool`**

Activate monitoring.

```python
def start(self) -> bool:
    """
    Start widget monitoring.
    
    Returns:
        True if successful, False otherwise
    """
    if self.active:
        return True
    
    self.active = True
    print(f"   🟢 {self.name} Widget started")
    
    # Initialize monitoring threads, connections, etc.
    self._init_monitoring()
    
    return True
```

### **`stop() -> bool`**

Deactivate monitoring.

```python
def stop(self) -> bool:
    """
    Stop widget monitoring.
    
    Returns:
        True if successful, False otherwise
    """
    if not self.active:
        return True
    
    self.active = False
    print(f"   ⭕ {self.name} Widget stopped")
    
    # Cleanup threads, close connections, etc.
    self._cleanup()
    
    return True
```

### **`get_recent_events(limit: int = 20) -> List[Dict]`**

Return buffered events.

```python
def get_recent_events(self, limit: int = 20) -> List[Dict]:
    """
    Get most recent events.
    
    Args:
        limit: Maximum number of events to return
    
    Returns:
        List of event dictionaries (most recent last)
    """
    return self.events[-limit:] if self.events else []
```

### **`get_stats() -> Dict[str, Any]`**

Return widget metrics.

```python
def get_stats(self) -> Dict[str, Any]:
    """
    Get widget statistics.
    
    Returns:
        Dict with name, active status, event count, timestamp
    """
    return {
        "name": self.name,
        "active": self.active,
        "events_buffered": len(self.events),
        "timestamp": datetime.now().isoformat()
    }
```

### **`get_actions() -> Dict[str, List[str]]`**

List available actions.

```python
def get_actions(self) -> Dict[str, List[str]]:
    """
    Get list of available actions.
    
    Returns:
        Dict with "actions" key containing list of action names
    """
    return {
        "actions": ["action_1", "action_2", "action_3"]
    }
```

### **Action Methods**

Define custom action handlers:

```python
def action_name(self, **kwargs) -> Dict:
    """
    Execute an action.
    
    Args:
        **kwargs: Action parameters (extracted from CLI)
    
    Returns:
        Dict with result details
    """
    # Execute action
    result = do_something(**kwargs)
    
    return {
        "status": "success",
        "message": f"Action completed: {result}",
        "details": result
    }
```

---

## 📦 Event Structure

Events should follow this structure:

```python
event = {
    "timestamp": datetime.now().isoformat(),
    "event_type": "created",  # or "modified", "deleted", "spawned", etc.
    "source": "file_integrity",  # Your widget name
    "path": "/path/to/file",  # Optional: path-related events
    "pid": 1234,  # Optional: process-related events
    "name": "process.exe",  # Optional: process name
    "remote_address": "1.2.3.4:443",  # Optional: network-related
    # ... other contextual fields
}
```

### Event Types

- **File Integrity:** `created`, `modified`, `deleted`
- **Process Monitor:** `spawned`, `terminated`
- **Network Sniffer:** `connection_established`, `connection_closed`
- **Scanner:** `scan_started`, `scan_complete`, `threat_detected`
- **Response:** `action_executed`, `quarantine_success`, `quarantine_failed`

---

## ✅ Best Practices

### 1. Thread Safety

Use locks when accessing shared state:

```python
import threading

class MyWidget:
    def __init__(self):
        self.events = []
        self.lock = threading.Lock()
    
    def _add_event(self, event):
        with self.lock:
            self.events.append(event)
    
    def get_recent_events(self, limit=20):
        with self.lock:
            return self.events[-limit:].copy()
```

### 2. Error Handling

Gracefully handle failures:

```python
def start(self) -> bool:
    try:
        # Initialization code
        self._init_monitoring()
        self.active = True
        return True
    except Exception as e:
        print(f"   ❌ {self.name} failed to start: {e}")
        self.active = False
        return False
```

### 3. Resource Management

Clean up resources on shutdown:

```python
def stop(self) -> bool:
    try:
        # Stop monitoring thread
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        
        # Close connections
        if self.connection:
            self.connection.close()
        
        self.active = False
        return True
    except Exception as e:
        print(f"   ❌ Failed to stop: {e}")
        return False
```

### 4. Logging

Log important events:

```python
import logging

logger = logging.getLogger(__name__)

def _on_event(self, event):
    logger.debug(f"Event detected: {event['event_type']}")
    self._add_event(event)
```

### 5. Performance

- Buffer events in memory (don't disk I/O for every event)
- Use efficient data structures (deque for fixed-size buffers)
- Avoid blocking operations in main thread

```python
from collections import deque

class MyWidget:
    def __init__(self):
        self.events = deque(maxlen=1000)  # Auto-purge oldest
        self.monitoring_thread = None
    
    def _monitor_loop(self):
        """Run in background thread."""
        while self.active:
            event = self._detect_event()
            if event:
                self.events.append(event)
            time.sleep(0.1)  # Avoid busy-waiting
```

---

## 💡 Examples

### Example 1: Simple Timer Widget

```python
import time
from datetime import datetime
from typing import List, Dict, Any


class TimerWidget:
    """A simple widget that generates events at intervals."""
    
    def __init__(self):
        self.name = "timer"
        self.active = False
        self.events = []
    
    def start(self) -> bool:
        self.active = True
        print(f"   🟢 {self.name} Widget started")
        return True
    
    def stop(self) -> bool:
        self.active = False
        print(f"   ⭕ {self.name} Widget stopped")
        return True
    
    def get_recent_events(self, limit: int = 20) -> List[Dict]:
        return self.events[-limit:]
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "active": self.active,
            "events_buffered": len(self.events),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_actions(self) -> Dict[str, List[str]]:
        return {"actions": ["trigger_event"]}
    
    def trigger_event(self, **kwargs) -> Dict:
        """Generate a test event."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "timer_tick",
            "source": "timer"
        }
        self.events.append(event)
        return {"status": "success", "message": "Event generated"}
```

### Example 2: Disk Space Monitor

```python
import shutil
from datetime import datetime
from typing import List, Dict, Any


class DiskSpaceWidget:
    """Monitor disk space on key partitions."""
    
    def __init__(self):
        self.name = "disk_space"
        self.active = False
        self.events = []
        self.warning_threshold = 80  # Percent
    
    def start(self) -> bool:
        self.active = True
        print(f"   🟢 {self.name} Widget started")
        self._check_disks()  # Initial check
        return True
    
    def stop(self) -> bool:
        self.active = False
        print(f"   ⭕ {self.name} Widget stopped")
        return True
    
    def get_recent_events(self, limit: int = 20) -> List[Dict]:
        return self.events[-limit:]
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "active": self.active,
            "events_buffered": len(self.events),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_actions(self) -> Dict[str, List[str]]:
        return {"actions": ["check_now", "set_threshold"]}
    
    def _check_disks(self):
        """Check disk usage and generate events."""
        for partition in ['C:\\', 'D:\\']:
            try:
                usage = shutil.disk_usage(partition)
                percent = (usage.used / usage.total) * 100
                
                if percent > self.warning_threshold:
                    event = {
                        "timestamp": datetime.now().isoformat(),
                        "event_type": "disk_warning",
                        "source": "disk_space",
                        "partition": partition,
                        "usage_percent": percent,
                        "free_gb": usage.free / 1e9
                    }
                    self.events.append(event)
            except OSError:
                pass
    
    def check_now(self, **kwargs) -> Dict:
        """Manually trigger a disk check."""
        self._check_disks()
        return {"status": "success", "events_generated": len(self.events)}
    
    def set_threshold(self, threshold: int = 80, **kwargs) -> Dict:
        """Update warning threshold."""
        self.warning_threshold = threshold
        return {"status": "success", "new_threshold": threshold}
```

---

## 🧪 Testing Your Widget

### Unit Test

Create `tests/test_my_widget.py`:

```python
import unittest
from widgets.my_widget import MyWidget


class TestMyWidget(unittest.TestCase):
    
    def setUp(self):
        self.widget = MyWidget()
    
    def test_start_stop(self):
        """Test widget lifecycle."""
        self.assertTrue(self.widget.start())
        self.assertTrue(self.widget.active)
        self.assertTrue(self.widget.stop())
        self.assertFalse(self.widget.active)
    
    def test_events(self):
        """Test event buffering."""
        self.widget.start()
        self.widget.trigger_event()  # Or however events are generated
        events = self.widget.get_recent_events()
        self.assertGreater(len(events), 0)
    
    def test_stats(self):
        """Test stats reporting."""
        stats = self.widget.get_stats()
        self.assertIn("name", stats)
        self.assertIn("active", stats)
        self.assertIn("events_buffered", stats)


if __name__ == "__main__":
    unittest.main()
```

### Manual Testing

```bash
# Run Guardian
python guardian.py

# Select: 2 (enable)
# Select your widget number
# Select: 5 (events) to see live events
# Select: 4 (action) to test your action handlers
```

---

## 🔌 Integration

### Register Your Widget

Add to `guardian.py`:

```python
widget_imports = {
    "my_widget": ("widgets.my_widget", "MyWidget"),  # ADD THIS
    "file_integrity": ("widgets.file_integrity", "FileIntegrityWidget"),
    # ...
}
```

### Directory Structure

```
widgets/
├── __init__.py
├── my_widget.py          # Your new widget
└── ...
```

### File Template

```python
"""
widgets/my_widget.py
MyWidget: Brief description.

Example:
    >>> widget = MyWidget()
    >>> widget.start()
    >>> events = widget.get_recent_events()
"""

from datetime import datetime
from typing import List, Dict, Any


class MyWidget:
    """Your widget description."""
    
    def __init__(self):
        self.name = "my_widget"
        self.active = False
        self.events = []
    
    # Implement all required methods...
```

---

## 🚀 Advanced Features

### Asynchronous Event Generation

```python
import threading

class AsyncWidget:
    def start(self) -> bool:
        self.active = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        return True
    
    def _monitor_loop(self):
        """Run in background."""
        while self.active:
            event = self._detect_event()
            if event:
                self.events.append(event)
            time.sleep(1)
```

### Configuration

```python
def __init__(self, config: Dict = None):
    self.config = config or {}
    self.threshold = self.config.get("threshold", 100)
    self.paths = self.config.get("paths", [])
```

---

## 📖 See Also

- [CONTRIBUTING.md](../CONTRIBUTING.md) — Widget submission guidelines
- [ARCHITECTURE.md](../ARCHITECTURE.md) — System design overview
- [CLI.md](./CLI.md) — User interface reference

---

**Happy widget building!** 🎉
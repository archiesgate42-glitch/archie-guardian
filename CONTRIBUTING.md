# Contributing to Archie Guardian

> We welcome contributions! This guide will help you get started.

---

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Creating a Widget](#creating-a-widget)
- [Coding Conventions](#coding-conventions)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Code of Conduct](#code-of-conduct)

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+**
- **Git**
- **Familiarity with:** Python, async programming (optional), Windows APIs (optional)

### Fork & Clone

```bash
# Fork on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/archie-guardian.git
cd archie-guardian

# Add upstream remote
git remote add upstream https://github.com/archiesgate42-glitch/archie-guardian.git
```

---

## 🛠️ Development Setup

### Create a Virtual Environment

```bash
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt

# Optional: Development tools
pip install pytest pytest-cov black flake8
```

### Verify Your Setup

```bash
python guardian.py
# Should show: ✨ ARCHIE GUARDIAN v1.0 - All systems operational
```

---

## 🧩 Creating a Widget

### Widget Interface

All widgets must implement this interface:

```python
class MyWidget:
    """My custom monitoring widget."""
    
    def __init__(self):
        """Initialize widget state."""
        self.name = "my_widget"
        self.events = []
    
    def start(self) -> bool:
        """Activate monitoring."""
        print(f"   🟢 {self.name} Widget started")
        return True
    
    def stop(self) -> bool:
        """Deactivate monitoring."""
        print(f"   ⭕ {self.name} Widget stopped")
        return True
    
    def get_recent_events(self, limit: int = 20) -> List[Dict]:
        """Return buffered events."""
        return self.events[-limit:]
    
    def get_stats(self) -> Dict[str, Any]:
        """Return widget metrics."""
        return {
            "name": self.name,
            "active": True,
            "events_buffered": len(self.events),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_actions(self) -> Dict[str, List[str]]:
        """List available actions."""
        return {
            "actions": ["custom_action_1", "custom_action_2"]
        }
    
    def custom_action_1(self, **kwargs) -> Dict:
        """Example action."""
        return {"status": "success", "message": "Action executed"}
```

### Widget Template (Copy-Paste)

```python
"""
widgets/my_widget.py
MyWidget: Brief description of what it monitors.
"""

from datetime import datetime
from typing import List, Dict, Any


class MyWidget:
    """
    MyWidget: Describe what this widget does.
    
    Example:
        >>> widget = MyWidget()
        >>> widget.start()
        >>> events = widget.get_recent_events()
    """
    
    def __init__(self):
        """Initialize widget."""
        self.name = "my_widget"
        self.events = []
        self.active = False
    
    def start(self) -> bool:
        """Start monitoring."""
        if self.active:
            return True
        
        self.active = True
        print(f"   🟢 {self.name} Widget started")
        
        # TODO: Initialize monitoring logic
        
        return True
    
    def stop(self) -> bool:
        """Stop monitoring."""
        if not self.active:
            return True
        
        self.active = False
        print(f"   ⭕ {self.name} Widget stopped")
        
        # TODO: Cleanup logic
        
        return True
    
    def get_recent_events(self, limit: int = 20) -> List[Dict]:
        """Get buffered events."""
        return self.events[-limit:] if self.events else []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get widget statistics."""
        return {
            "name": self.name,
            "active": self.active,
            "events_buffered": len(self.events),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_actions(self) -> Dict[str, List[str]]:
        """List available actions."""
        return {
            "actions": ["action_1", "action_2"]
        }
    
    def action_1(self, **kwargs) -> Dict:
        """Example action."""
        # TODO: Implement action
        return {"status": "success"}
```

### Registering Your Widget

1. **Save** your widget to `widgets/my_widget.py`
2. **Update** `guardian.py` widget_imports dict:

```python
widget_imports = {
    "my_widget": ("widgets.my_widget", "MyWidget"),  # Add this
    "file_integrity": ("widgets.file_integrity", "FileIntegrityWidget"),
    # ...
}
```

3. **Test** it runs:

```bash
python guardian.py
# Should show: ✅ my_widget loaded
```

---

## 💻 Coding Conventions

### Style Guide

Follow **PEP 8** with these conventions:

```python
# 1. Use type hints
def analyze_event(event: Event) -> Dict[str, Any]:
    """Analyze security event."""
    pass

# 2. Docstrings for all public functions
def process_data(data: List[int]) -> int:
    """
    Process input data.
    
    Args:
        data: List of integers to process.
    
    Returns:
        Processed result.
    """
    pass

# 3. Meaningful variable names
threats_detected = 0          # ✓ Good
threats = 0                   # ✗ Ambiguous

# 4. Comments for WHY, not WHAT
# Increase score for system paths (more critical)   # ✓ Why
score += 30                                          # Why?

# ✗ Bad
score += 30  # Add 30 to score (obvious from code)

# 5. Logging for important events
import logging
logger = logging.getLogger(__name__)

logger.info("Widget started successfully")
logger.error("Failed to initialize: %s", error)
```

### File Organization

```python
"""
widgets/my_widget.py
Brief description + usage notes.
"""

# 1. Imports (stdlib, third-party, local)
from datetime import datetime
from typing import List, Dict, Any

import psutil

from core.agent_utils import Event, AuditLogger

# 2. Constants
DEFAULT_BUFFER_SIZE = 100
CRITICAL_PATHS = ["/System", "/root"]

# 3. Main class
class MyWidget:
    pass

# 4. Helper functions (if needed)
def _helper_function():
    pass
```

---

## 🧪 Testing

### Unit Tests

Create `tests/test_my_widget.py`:

```python
import unittest
from widgets.my_widget import MyWidget


class TestMyWidget(unittest.TestCase):
    
    def setUp(self):
        """Initialize test widget."""
        self.widget = MyWidget()
    
    def test_start(self):
        """Test widget starts correctly."""
        result = self.widget.start()
        self.assertTrue(result)
    
    def test_stop(self):
        """Test widget stops correctly."""
        self.widget.start()
        result = self.widget.stop()
        self.assertTrue(result)
    
    def test_get_stats(self):
        """Test stats are returned."""
        stats = self.widget.get_stats()
        self.assertIn("name", stats)
        self.assertIn("active", stats)


if __name__ == "__main__":
    unittest.main()
```

### Run Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=widgets tests/

# Verbose output
pytest -v tests/
```

### Manual Testing

```bash
python guardian.py
# 1. enable my_widget
# 2. action (select widget, execute action)
# 3. events (verify events show up)
# 4. Ctrl+C to exit
```

---

## 📤 Submitting Changes

### Workflow

1. **Create a branch:**
   ```bash
   git checkout -b feature/my-new-widget
   ```

2. **Make changes** & commit frequently:
   ```bash
   git add .
   git commit -m "Add MyWidget for monitoring X"
   ```

3. **Push to your fork:**
   ```bash
   git push origin feature/my-new-widget
   ```

4. **Create a Pull Request** on GitHub with:
   - **Title:** Clear, descriptive
   - **Description:** What & why
   - **Testing:** How you tested
   - **Screenshots:** If UI changes

### PR Checklist

Before submitting, verify:

- [ ] Code follows PEP 8 (`black` + `flake8`)
- [ ] All tests pass (`pytest`)
- [ ] Widget implements required interface
- [ ] Docstrings are complete
- [ ] No breaking changes
- [ ] Audit logging added (where relevant)
- [ ] README updated (if feature-level change)

### Code Review

- Be respectful & constructive
- Ask questions if unclear
- Suggest improvements, don't demand
- Respond to feedback within 48 hours

---

## 🤝 Reporting Issues

### Bug Reports

Use the issue template:

```markdown
**Describe the bug:**
[Clear description]

**To Reproduce:**
1. Step 1
2. Step 2

**Expected behavior:**
[What should happen]

**Actual behavior:**
[What actually happened]

**Environment:**
- OS: [Windows/Linux/Mac]
- Python: [3.9/3.10/etc]
- Version: [v0.3/v1.0]

**Logs:**
[Copy from logs/audit.log]
```

### Feature Requests

```markdown
**Feature:**
[Clear title]

**Motivation:**
Why is this needed?

**Proposed Solution:**
How should it work?

**Alternatives:**
Other approaches?
```

---

## 📝 Commit Messages

Write clear, atomic commits:

```
# Good ✓
git commit -m "Add network sniffer widget with IPv4/IPv6 support"
git commit -m "Fix permission check race condition in OrchB"
git commit -m "Update docs: add CONTRIBUTING.md"

# Bad ✗
git commit -m "changes"
git commit -m "bug fix"
git commit -m "wip"
```

### Commit Format

```
[type] [scope]: [subject]

[body - explain WHAT & WHY]

[footer - references/breaking changes]
```

**Types:** `feat`, `fix`, `docs`, `test`, `refactor`, `chore`

**Example:**
```
feat(widgets): add gpu monitor widget

Add new widget to monitor GPU temperature and utilization.
Implements real-time NVIDIA CUDA monitoring.
Handles cases where GPU drivers not installed.

Closes #42
```

---

## 🏆 Recognition

Contributors are recognized in:
- `CONTRIBUTORS.md`
- GitHub contributors graph
- Release notes

---

## ❓ Questions?

- **Discussions:** https://github.com/archiesgate42-glitch/archie-guardian/discussions
- **Issues:** https://github.com/archiesgate42-glitch/archie-guardian/issues
- **Email:** [maintainer contact info]

---

## 📖 Code of Conduct

We are committed to providing a welcoming community. All contributors must:

- Be respectful & inclusive
- Welcome diverse perspectives
- Report harassment to maintainers
- Follow open-source best practices

By contributing, you agree to these terms.

---

**Happy Contributing!** 🎉
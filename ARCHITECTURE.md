# Archie Guardian - Technical Architecture

> Deep dive into the system design, orchestration patterns, and component interactions.

---

## 🏗️ System Overview

Archie Guardian is a **4-layer multi-agent security system** that combines real-time monitoring widgets with AI-driven threat analysis and human-in-the-loop decision making.

```
┌─────────────────────────────────────────────────────┐
│          CLI Interface + Real-time UI               │
│     (guardian.py + interactive menu system)         │
├─────────────────────────────────────────────────────┤
│      Orchestration Layer (OrchA + OrchB)            │
│  • AI Threat Analysis (OrchA)                       │
│  • Human-Facing Bridge (OrchB)                      │
│  • Master Orchestrator (event routing)              │
├─────────────────────────────────────────────────────┤
│         Inference Layer (Future: Ollama)            │
│  • Local LLM for threat classification              │
│  • Pattern recognition & anomaly detection          │
├─────────────────────────────────────────────────────┤
│    Sensor Layer (5 Active Widgets on Windows)       │
│  • File Integrity Monitor                           │
│  • Process Monitor                                  │
│  • Network Sniffer                                  │
│  • Windows Defender Integration                     │
│  • Rapid Response Neutralize & Capture (RRNC)      │
└─────────────────────────────────────────────────────┘
```

---

## 🧩 Component Architecture

### Layer 1: Sensor Widgets (`/widgets`)

Each widget implements a consistent interface:

```python
class Widget:
    def start(self) -> bool
        """Activate monitoring"""
    
    def stop(self) -> bool
        """Deactivate monitoring"""
    
    def get_recent_events(limit: int) -> List[Event]
        """Fetch buffered events"""
    
    def get_stats(self) -> Dict
        """Return monitoring metrics"""
    
    def get_actions(self) -> Dict
        """List available actions"""
```

**Widgets included:**

| Widget | File | Purpose | Events |
|--------|------|---------|--------|
| **File Integrity** | `file_integrity.py` | Monitor file system changes (CRUD) | `created`, `modified`, `deleted` |
| **Process Monitor** | `process_monitor.py` | Detect new process spawning | `spawned`, `terminated` |
| **Network Sniffer** | `network_sniffer.py` | Track network connections | `connection_established` |
| **Windows Defender** | `windows_defender.py` | Scan integration + threat feedback | `scan_complete`, `threat_detected` |
| **RRNC** | `rrnc.py` | Auto-response & forensics capture | `action_executed`, `quarantine_success` |

### Layer 2: Agent Utilities (`/core/agent_utils.py`)

Shared data structures & base classes:

```python
# Core Data Models
Event              # {event_id, source, event_type, payload, timestamp}
ThreatLevel        # Enum: LOW, MEDIUM, HIGH
PermissionLevel    # Enum: OBSERVE, ALERT, ANALYZE, ISOLATE, AUTO_RESPOND
Decision           # {agent, action, confidence, reasoning}

# Management Classes
AuditLogger        # Log all decisions & actions to audit.log
EventQueue         # Thread-safe event buffer
ConfigLoader       # YAML config management
```

### Layer 3: Orchestrators (`/core`)

#### **OrchA (AI Task Master)** — `orch_a.py`

Analyzes events and assigns threat scores.

**Flow:**
1. Receives Event from widget
2. Scores threat (0-100) using heuristics + (future) LLM
3. Assigns ThreatLevel (LOW/MEDIUM/HIGH)
4. Generates Decision with reasoning
5. Logs to audit trail

**Key methods:**
- `analyze_event(event)` → threat score & reasoning
- `learn_from_feedback(event_id, feedback)` → improves future scoring
- `get_stats()` → false positive tracking, learning history

**Threat Scoring Logic (MVP):**
```
File Integrity:
  - System path (.exe/.dll/.sys) → +30-50 points
  - User path (~/Downloads) → +0-20 points

Process Monitor:
  - Suspicious process (powershell, cmd) → +65 points
  - Normal process (explorer.exe) → +10 points

Network Sniffer:
  - Process making connection → +50 points
  - Known safe IP (8.8.8.8) → -30 points
```

#### **OrchB (Human-Facing Bridge)** — `orch_b.py`

Manages user permissions, escalation, and feedback loops.

**Flow:**
1. Receives Decision from OrchA
2. Checks user permission level
3. Evaluates if escalation needed
4. Prompts user (if MEDIUM/HIGH + not auto-approve)
5. Stores approval decision
6. Returns approved/denied

**Permission Hierarchy:**
```
OBSERVE         → Read-only monitoring
  ↓
ALERT           → Send notifications
  ↓
ANALYZE         → Request context/reasoning
  ↓
ISOLATE         → Kill processes, block IPs (requires approval)
  ↓
AUTO_RESPOND    → Execute all actions automatically
```

**Key methods:**
- `check_permission(action)` → bool
- `evaluate_escalation(decision, threat_level)` → bool
- `escalate_to_user(decision, context)` → approved
- `get_user_feedback(event_id)` → feedback type
- `get_approval_stats()` → approval rate tracking

#### **Master Orchestrator** — `orchestrator.py`

Central coordinator that ties everything together.

**Event Pipeline:**
```
Widget Event
    ↓
EventQueue (buffer)
    ↓
OrchA.analyze_event()
    ↓
OrchA.process_events() → Decision
    ↓
OrchB.evaluate_escalation()
    ↓
[If escalation needed]
  → OrchB.escalate_to_user() → approved/denied
    ↓
[If approved]
  → Dispatcher.execute_action()
    ↓
OrchB.get_user_feedback() → learn_from_feedback()
    ↓
Event marked PROCESSED
```

**Key methods:**
- `start()` / `stop()` → lifecycle management
- `ingest_widget_event(event)` → push to queue
- `process_events()` → drain queue, run pipeline
- `get_orchestrator_stats()` → metrics & health

---

## 📊 Data Flow Diagrams

### Event Lifecycle

```
┌─────────────┐
│ File Widget │ → NEW_EVENT (file modified)
└──────┬──────┘
       │
       ↓
┌──────────────┐
│ Event Queue  │ (buffered, timestamped)
└──────┬───────┘
       │
       ↓
┌──────────────────┐
│ OrchA.analyze()  │ → threat_score: 75%
└──────┬───────────┘
       │
       ↓
┌────────────────────┐
│ OrchB.escalate?    │ → YES (MEDIUM threat)
└──────┬─────────────┘
       │
       ↓
┌──────────────────────────┐
│ User Prompt              │ → "Allow quarantine? [Y/n]"
└──────┬───────────────────┘
       │
       ├─→ [Y] → APPROVED
       │   ├→ Dispatcher.kill_process()
       │   └→ get_user_feedback()
       │
       └─→ [n] → DENIED
           └→ Log decision, continue
```

### Permission Check Flow

```
┌────────────────┐
│ Decision       │ action: "isolate"
│ Threat: HIGH   │
└────────┬───────┘
         │
         ↓
┌──────────────────────────┐
│ OrchB.check_permission() │
└────────┬─────────────────┘
         │
         ├─ User: OBSERVE     → DENIED ✗
         ├─ User: ALERT       → DENIED ✗
         ├─ User: ANALYZE     → DENIED ✗
         ├─ User: ISOLATE     → ALLOWED ✓
         └─ User: AUTO_RESPOND→ ALLOWED ✓
```

---

## 🔄 Multi-Agent Orchestration Pattern

### Why Multi-Agent?

Guardian uses a **master-subordinate orchestration** pattern:

- **OrchA (Specialist)** — Focuses on threat analysis; optimized for accuracy
- **OrchB (Gatekeeper)** — Handles human policies; ensures user intent
- **Master Orch (Coordinator)** — Routes events, manages lifecycle

This separation provides:
- **Modularity** — Easy to swap threat models or permission rules
- **Auditability** — Clear decision trail (who decided what)
- **Testability** — Each agent can be tested independently
- **Future extensibility** — Can add OrchC (auto-remediation), OrchD (threat intelligence), etc.

### Decision Authority

```
OrchA says: "This is 85% likely a threat"
OrchB says: "User has permission ISOLATE, but needs to approve first"
Master says: "Escalate to user → Wait for approval → Execute if approved"
```

---

## 🔐 Security Design

### Threat Model

**Assumption:** Guardian runs on a **trusted** machine (user is admin).

**What Guardian protects against:**
- File tampering (ransomware, accidental overwrites)
- Suspicious process spawning
- Anomalous network activity

**What Guardian does NOT protect against:**
- Kernel-level rootkits (e.g., DKOM - Direct Kernel Object Manipulation)
- Pre-execution infiltration
- Cryptographic backdoors in system libraries

### Audit Trail

Every decision is logged to `logs/audit.log` with:
```
[timestamp] ACTION: details
```

Example:
```
[2025-11-15T15:21:18.488132] WIDGET_ENABLED: windows_defender
[2025-11-15T15:21:18.488132] ACTION_EXECUTED: windows_defender.quick_scan({'path': 'C:\\'})
[2025-11-15T15:21:20.000000] PERMISSION_CHANGE: observe -> auto_respond
[2025-11-15T15:21:25.000000] USER_APPROVAL: isolate - true
```

### Permission Model

User permission levels are **hierarchical**:

```
OBSERVE (Level 0)
  ├─ Read monitoring data
  └─ View audit logs

ALERT (Level 1)
  ├─ Everything above
  ├─ Receive notifications
  └─ View threat analysis

ANALYZE (Level 2)
  ├─ Everything above
  ├─ Request detailed context
  └─ Export reports

ISOLATE (Level 3)
  ├─ Everything above
  ├─ Approve quarantine actions
  ├─ Kill processes (with user approval)
  └─ Block network connections

AUTO_RESPOND (Level 4)
  ├─ Everything above
  └─ Execute all actions automatically
```

---

## 🎯 Future Extensions

### v1.0 Roadmap

**Dispatcher Integration:**
- Define action handlers per widget
- Execute OS-level commands (kill process, block IP, quarantine file)
- Atomic transactions (rollback on failure)

**Ollama Integration:**
- Replace heuristic scoring with LLM-based analysis
- Fine-tuned models for specific threat domains
- Confidence calibration via feedback loops

**Hot-Reload Widgets:**
- Load/unload widgets without restart
- Dynamic configuration via CLI

**Advanced TUI Dashboard:**
- Real-time threat heatmap
- Time-series graphs (CPU, network activity)
- Interactive widget status

### v2.0+ Vision

- **Widget Marketplace** — Community-contributed sensors
- **Multi-Machine Telemetry** — Optional central dashboard
- **Threat Intelligence Feed** — Integrate MISP, CVE databases
- **Custom LLM Models** — Fine-tune on user's threat landscape

---

## 📚 Code Organization

```
archie-guardian/
├── guardian.py             # Main entry point + CLI
├── core/
│   ├── __init__.py
│   ├── agent_utils.py      # Shared data structures
│   ├── orch_a.py           # AI threat analyzer
│   ├── orch_b.py           # Human-facing bridge
│   └── orchestrator.py     # Master coordinator
├── widgets/
│   ├── __init__.py
│   ├── file_integrity.py
│   ├── process_monitor.py
│   ├── network_sniffer.py
│   ├── windows_defender.py
│   └── rrnc.py
├── config/
│   ├── manifest.yaml       # Widget definitions
│   └── user_config.yaml    # User settings
├── logs/
│   └── audit.log
├── docs/
│   ├── CLI.md
│   ├── WIDGETS.md
│   └── PERMISSIONS.md
├── README.md
├── ARCHITECTURE.md         # This file
├── CONTRIBUTING.md
├── LICENSE
└── requirements.txt
```

---

## 🧪 Testing & Debugging

### Unit Tests (Future)

```bash
pytest tests/test_orch_a.py        # Test threat scoring
pytest tests/test_orch_b.py        # Test permissions
pytest tests/test_widgets.py       # Test sensors
```

### Debug Logging

Enable verbose logging:
```bash
export DEBUG=1
python guardian.py
```

### Profiling

Check resource usage:
```bash
# Monitor CPU/RAM
python -m cProfile -s cumulative guardian.py
```

---

## 📖 References

- **Event-Driven Architecture:** https://en.wikipedia.org/wiki/Event-driven_architecture
- **Multi-Agent Systems:** https://en.wikipedia.org/wiki/Multi-agent_system
- **Audit Logging Best Practices:** https://owasp.org/www-community/attacks/Audit_Log_Poisoning
- **Windows Security APIs:** https://docs.microsoft.com/en-us/windows/win32/security

---

**Last Updated:** November 2025  
**Version:** 1.0
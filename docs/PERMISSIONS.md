# Permission Model & Audit Trail

> Security, access control, and audit logging in Archie Guardian.

---

## 🔐 Permission Levels

Archie Guardian uses a **hierarchical permission system**. Each level unlocks new capabilities while maintaining security and auditability.

### Permission Hierarchy

```
┌─────────────────────────────────────────┐
│ Level 0: OBSERVE                        │
│ (Read-only monitoring)                  │
└────────────────────┬────────────────────┘
                     ↓
┌─────────────────────────────────────────┐
│ Level 1: ALERT                          │
│ (Observe + Notifications)               │
└────────────────────┬────────────────────┘
                     ↓
┌─────────────────────────────────────────┐
│ Level 2: ANALYZE                        │
│ (Alert + Threat Analysis)               │
└────────────────────┬────────────────────┘
                     ↓
┌─────────────────────────────────────────┐
│ Level 3: ISOLATE                        │
│ (Analyze + User-Approved Actions)       │
└────────────────────┬────────────────────┘
                     ↓
┌─────────────────────────────────────────┐
│ Level 4: AUTO_RESPOND                   │
│ (Isolate + Auto Execution)              │
└─────────────────────────────────────────┘
```

---

## 📊 Permission Levels Detailed

### **Level 0: OBSERVE**

**Capabilities:**
- View real-time monitoring data
- View audit logs
- Access widget statistics
- NO alerts or notifications

**When to use:**
- First-time testing
- Sandbox environment
- Learning the system

**Example:**
```
guardian> status
📊 GUARDIAN STATUS
Status: ✅ OPERATIONAL
Permission Level: OBSERVE
Widgets: [showing live data]
```

**Restrictions:**
- Cannot receive notifications ❌
- Cannot execute actions ❌
- Cannot access threat analysis ❌

---

### **Level 1: ALERT**

**Capabilities:**
- Everything from OBSERVE
- Receive threat notifications
- View threat level classifications

**When to use:**
- Want to be notified of issues
- Development/testing environment
- Non-critical systems

**Example:**
```
🚨 [MEDIUM] Security Alert
   Source: process_monitor
   Event: Suspicious process spawned
   Reason: powershell.exe from temp directory
   Confidence: 65%
```

**Restrictions:**
- Cannot see threat analysis details ❌
- Cannot execute actions ❌

---

### **Level 2: ANALYZE**

**Capabilities:**
- Everything from ALERT
- View detailed threat analysis from OrchA
- See confidence scores & reasoning
- Export threat context

**When to use:**
- Want to understand threats
- Review before taking action
- Compliance/audit requirements

**Example:**
```
📊 Threat Analysis
Confidence: 78%
Reasoning: File modified in system directory (.exe)
           Process spawned from Network location
           Child of explorer.exe

Classification: MEDIUM THREAT
Recommended: Quarantine and investigate
```

**Restrictions:**
- Cannot execute remediation ❌
- Still need approval for actions ❌

---

### **Level 3: ISOLATE**

**Capabilities:**
- Everything from ANALYZE
- Execute isolating actions with user approval
- Kill suspicious processes
- Quarantine files
- Block network connections

**When to use:**
- Production systems with oversight
- Want to mitigate threats with approval
- Compliance requirements met

**Example Session:**
```
guardian> action
[Select windows_defender]
[Select quarantine_threat]

╔════════════════════════════════════════════════════╗
║           ⚠️  ESCALATION REQUIRED                 ║
╚════════════════════════════════════════════════════╝

🔴 Threat Level: HIGH
📊 Confidence: 92%
💡 Recommended Action: quarantine
📝 Reason: Detected ransomware pattern

Allow action? [Y/n]: y
   ✅ Action approved
   [File quarantined successfully]
```

**Restrictions:**
- All actions require user approval ⚠️

---

### **Level 4: AUTO_RESPOND**

**Capabilities:**
- Everything from ISOLATE
- Auto-execute remediation without user approval
- Full autonomous threat response

**⚠️ WARNING:**
- **Use with extreme caution!**
- Recommended only for mature deployments
- Should run alongside traditional antivirus

**When to use:**
- Trusted environment with no user oversight needed
- 24/7 unattended monitoring
- Critical infrastructure with tuned threat detection

**Example:**
```
guardian> set_perms
[Select 5: AUTO_RESPOND]
✅ Permission level: AUTO_RESPOND

[Later, when threat detected...]
🚨 [HIGH] Threat Detected
OrchB.evaluate_escalation() → No escalation needed
Dispatcher.execute_action() → Kill process 4521
[Quarantine successful]
[DONE - no user interaction needed]
```

---

## 🎯 Permission Matrix

| Action | OBSERVE | ALERT | ANALYZE | ISOLATE | AUTO_RESPOND |
|--------|---------|-------|---------|---------|--------------|
| View monitoring | ✓ | ✓ | ✓ | ✓ | ✓ |
| View logs | ✓ | ✓ | ✓ | ✓ | ✓ |
| Get alerts | ✗ | ✓ | ✓ | ✓ | ✓ |
| View threat analysis | ✗ | ✗ | ✓ | ✓ | ✓ |
| Execute actions (approve) | ✗ | ✗ | ✗ | ✓ | ✓ |
| Execute actions (auto) | ✗ | ✗ | ✗ | ✗ | ✓ |

---

## 🔄 Permission Change Flow

```
User runs: guardian> set_perms
           [Select new level]
                ↓
OrchB.set_permission_level(level)
                ↓
Update self.permission_level
                ↓
Log to audit.log:
[timestamp] PERMISSION_CHANGE: old_level -> new_level
                ↓
Print confirmation
                ↓
Return to menu
```

**Example log:**
```
[2025-11-15T15:21:20.000000] PERMISSION_CHANGE: observe -> auto_respond
```

---

## 📝 Audit Trail

### What Gets Logged

Archie Guardian logs **every significant action** to `logs/audit.log`.

### Log Format

```
[ISO_8601_TIMESTAMP] EVENT_TYPE: details
```

### Event Types

| Event | Logged When | Example |
|-------|----------|---------|
| `STARTUP` | Guardian initializes | `[2025-11-15T15:06:42.195] STARTUP: Guardian v1.0 initialized` |
| `WIDGET_ENABLED` | Widget activated | `[2025-11-15T15:10:34] WIDGET_ENABLED: file_integrity` |
| `WIDGET_DISABLED` | Widget deactivated | `[2025-11-15T15:11:50] WIDGET_DISABLED: process_monitor` |
| `ACTION_EXECUTED` | Action runs successfully | `[2025-11-15T15:21:18] ACTION_EXECUTED: windows_defender.quick_scan({'path': 'C:\\'})` |
| `PERMISSION_CHANGE` | Permission level updated | `[2025-11-15T15:21:20] PERMISSION_CHANGE: observe -> auto_respond` |
| `USER_APPROVAL` | User approves/denies action | `[2025-11-15T15:21:25] USER_APPROVAL: isolate - true` |
| `USER_FEEDBACK` | User rates threat detection | `[2025-11-15T15:21:30] USER_FEEDBACK: ev_abc123 - confirmed_threat` |
| `SHUTDOWN` | Guardian exits gracefully | `[2025-11-15T15:22:00] SHUTDOWN: Guardian graceful exit` |
| `INTERRUPT` | User force-quit (Ctrl+C) | `[2025-11-15T15:22:15] INTERRUPT: User Ctrl+C` |

### Example Audit Log

```
[2025-11-15T15:06:42.195] STARTUP: Guardian v1.0 initialized
[2025-11-15T15:10:34.694] WIDGET_ENABLED: file_integrity
[2025-11-15T15:10:34.758] WIDGET_ENABLED: windows_defender
[2025-11-15T15:21:18.488] ACTION_EXECUTED: windows_defender.quick_scan({'path': 'C:\\'})
[2025-11-15T15:21:20.000] PERMISSION_CHANGE: observe -> auto_respond
[2025-11-15T15:21:25.000] USER_APPROVAL: isolate - true
[2025-11-15T15:22:00.000] SHUTDOWN: Guardian graceful exit
```

---

## 🔍 Audit Log Analysis

### View Recent Logs

```bash
# Show last 20 entries
guardian> logs

# Or from shell
tail -20 logs/audit.log
```

### Search for Specific Events

```bash
# Find all permission changes
grep "PERMISSION_CHANGE" logs/audit.log

# Find all user approvals
grep "USER_APPROVAL" logs/audit.log

# Find all actions executed
grep "ACTION_EXECUTED" logs/audit.log
```

### Parse Logs Programmatically

```python
import json
from datetime import datetime

def parse_audit_log():
    entries = []
    with open("logs/audit.log", "r", encoding="utf-8") as f:
        for line in f:
            # Format: [timestamp] EVENT_TYPE: details
            timestamp_end = line.index("]")
            timestamp = line[1:timestamp_end]
            
            rest = line[timestamp_end+2:].strip()
            event_type, details = rest.split(":", 1)
            
            entries.append({
                "timestamp": datetime.fromisoformat(timestamp),
                "event_type": event_type.strip(),
                "details": details.strip()
            })
    
    return entries

# Usage
logs = parse_audit_log()
for entry in logs:
    print(f"{entry['timestamp']} | {entry['event_type']}")
```

---

## 🛡️ Security Best Practices

### 1. Principle of Least Privilege

Start with **OBSERVE** and only increase permissions as needed.

```
❌ Bad:   Start with AUTO_RESPOND
✅ Good:  Start with OBSERVE → ALERT → ANALYZE → ISOLATE
```

### 2. Regular Permission Audits

Review `logs/audit.log` for unexpected permission changes:

```bash
# Check who changed permissions
grep "PERMISSION_CHANGE" logs/audit.log | tail -10

# Alert on AUTO_RESPOND enables
grep "auto_respond" logs/audit.log
```

### 3. Backup Audit Logs

Protect audit trail from tampering:

```bash
# Copy audit log regularly
cp logs/audit.log backups/audit.log.$(date +%Y%m%d)

# Verify log integrity (future version)
sha256sum logs/audit.log > logs/audit.log.sha256
```

### 4. Monitor Permission Changes

Set up alerts for:
- Permission level increases
- Suspicious action sequences
- Approval denial patterns

---

## 🧠 Decision Flow with Permissions

### Low Threat (15% confidence)

```
OrchA scores threat = 15%
           ↓
OrchB.evaluate_escalation()
           ↓
       Permission: OBSERVE?
           ↓
       YES → No notification (observing only)
       NO  → Send alert
```

### Medium Threat (65% confidence)

```
OrchA scores threat = 65%
           ↓
OrchB.evaluate_escalation()
           ↓
User has ISOLATE permission?
           ↓
       YES → Escalate to user for approval
             [User says yes/no]
       NO  → Just alert (cannot execute)
```

### High Threat (92% confidence)

```
OrchA scores threat = 92%
           ↓
OrchB.evaluate_escalation()
           ↓
User has AUTO_RESPOND permission?
           ↓
       YES → Execute immediately
               Log: USER_APPROVAL - auto_respond
       NO  → Always escalate to user
             [User must approve]
```

---

## 🔄 Permission Change Workflow

1. User runs: `guardian> set_perms`
2. Menu shows permission levels (1-5)
3. User selects new level (e.g., 5 = AUTO_RESPOND)
4. OrchB verifies permission hierarchy
5. Updates internal state
6. Logs change to audit.log
7. Confirms to user

**Security check:** Cannot skip levels (e.g., can't go OBSERVE → ISOLATE)

---

## 📊 Compliance Considerations

### SOC 2 Type II Compliance

Guardian supports:
- ✅ Complete audit trail
- ✅ User decision tracking
- ✅ Permission-based access control
- ✅ Non-repudiation (timestamped logs)

### HIPAA/PCI-DSS

- Logs should be encrypted at rest
- Implement log rotation (future v1.1)
- Archive for compliance period (future)

### Example: SIEM Integration

```bash
# Stream logs to SIEM (future)
tail -f logs/audit.log | \
  jq '.[1:-1] | split(" ") | {timestamp: .[0], event: .[1], details: .[2]}' | \
  curl -X POST -d @- https://siem.example.com/api/events
```

---

## 🚨 Common Scenarios

### Scenario 1: Investigate Suspicious Process

```
User sees process_monitor event
           ↓
User runs: action → process_monitor → get_details
           ↓
Permission: ANALYZE? YES
           ↓
Shows threat analysis (confidence: 45%)
           ↓
User says: NOT a threat (false positive feedback)
           ↓
OrchA learns: confidence should be lower for this pattern
```

**Logs:**
```
[T1] ACTION_EXECUTED: process_monitor.get_details({'pid': 1234})
[T2] USER_FEEDBACK: ev_xyz - false_positive
```

### Scenario 2: Auto-Respond to Ransomware

```
File widget detects suspicious modifications
           ↓
OrchA scores: 95% threat (HIGH)
           ↓
User has AUTO_RESPOND? YES
           ↓
OrchB.evaluate_escalation() → False (95% = always execute)
           ↓
Dispatcher quarantines file
           ↓
Logs: ACTION_EXECUTED + USER_APPROVAL (auto)
```

**Logs:**
```
[T1] ACTION_EXECUTED: windows_defender.quarantine({'file': 'C:\Temp\evil.exe'})
[T2] USER_APPROVAL: quarantine - auto_respond
```

---

## 📚 See Also

- [ARCHITECTURE.md](../ARCHITECTURE.md) — OrchB implementation details
- [CLI.md](./CLI.md) — How to set permissions
- [CONTRIBUTING.md](../CONTRIBUTING.md) — Security practices for contributors

---

**Remember: With great permission comes great responsibility!** ⚖️
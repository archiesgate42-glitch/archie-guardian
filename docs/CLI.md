# CLI Reference

> Complete command guide for Archie Guardian.

---

## 🎮 Interactive Menu

Guardian uses a numbered menu system. Run and follow the prompts:

```bash
python guardian.py

╔════════════════════════════════════════════════════╗
║     ARCHIE GUARDIAN v1.0 - MAIN MENU              ║
║  Widget Manager + Multi-Agent Orchestration       ║
╚════════════════════════════════════════════════════╝

Commands:
  1. status      - Show Guardian status
  2. enable      - Enable widget(s) [numbered]
  3. disable     - Disable widget(s) [numbered]
  4. action      - Execute widget action [numbered]
  5. events      - Show live widget events
  6. logs        - View audit logs
  7. orch_stats  - Show orchestrator statistics
  8. set_perms   - Set user permission level
  9. help        - Show help
  0. quit        - Exit Guardian

Enter command (0-9):
```

---

## 📊 Command Reference

### **1. status** — System Overview

Display current system state, widget status, and orchestrator metrics.

**Usage:**
```
Enter command (0-9): 1
```

**Output:**
```
📊 GUARDIAN STATUS
==================================================
Status: ✅ OPERATIONAL
Version: 1.0 (Multi-Agent Orchestration)
Permission Level: OBSERVE

Widgets:
  🟢 file_integrity       - LIVE (0 events)
  🟢 network_sniffer      - LIVE (18 events)
  🟢 process_monitor      - LIVE (0 events)
  🟢 rrnc                 - LIVE (0 events)
  🟢 windows_defender     - LIVE (0 events)

Orchestrator: ⭕ Standby (CLI-only mode)

Audit Log: logs/audit.log
==================================================
```

**What it shows:**
- System operational status
- Current permission level
- List of all widgets with live event counts
- Orchestrator status

---

### **2. enable** — Activate Widgets

Start monitoring with specified widgets.

**Usage:**
```
Enter command (0-9): 2

🔋 ENABLE WIDGETS
==================================================
Available widgets:
  1. file_integrity       [⭕ Disabled]
  2. process_monitor      [⭕ Disabled]
  3. network_sniffer      [⭕ Disabled]
  4. windows_defender     [⭕ Disabled]
  5. rrnc                 [⭕ Disabled]

Select widget(s) (e.g. 1,2,3 or 1-3 or just 1): 1-5
```

**Selection formats:**
- `1` — Enable widget 1 only
- `1,2,3` — Enable widgets 1, 2, and 3
- `1-5` — Enable widgets 1 through 5
- `1-3,5` — Enable widgets 1-3 and 5

**Output:**
```
   🟢 File Integrity Widget: Monitoring 2 paths
✅ file_integrity enabled
   🟢 Process Monitor Widget started
✅ process_monitor enabled
...
✅ Enabled 5 widget(s)
```

---

### **3. disable** — Deactivate Widgets

Stop monitoring with specified widgets.

**Usage:**
```
Enter command (0-9): 3

🔴 DISABLE WIDGETS
==================================================
Active widgets:
  1. file_integrity
  2. process_monitor
  3. network_sniffer
  4. windows_defender
  5. rrnc

Select widget(s) to disable (e.g. 1,2 or 1-2): 1-2
```

**Selection format:** Same as enable (1, 1-3, 1,2,3, etc.)

**Output:**
```
✅ file_integrity disabled
✅ process_monitor disabled
```

---

### **4. action** — Execute Widget Actions

Perform specific operations on active widgets.

**Usage:**
```
Enter command (0-9): 4

⚡ ACTION EXECUTION
============================================================
Active widgets:
  1. file_integrity
  2. process_monitor
  3. network_sniffer
  4. windows_defender
  5. rrnc

Select widget (number): 4

Available actions for 'windows_defender':
  1. quick_scan
  2. full_scan
  3. custom_scan
  4. get_threat_details
  5. quarantine_threat

Select action (number): 1

Enter parameters for 'quick_scan':
Format: key=value (e.g. pid=1234 path=C:\\temp)
(Press Enter to skip)
> path=C:\
```

**Parameters:**
- Provide as `key=value` pairs separated by spaces
- Types auto-detected (int, float, string)
- Press Enter to skip

**Example actions:**

| Widget | Action | Parameters | Effect |
|--------|--------|-----------|--------|
| windows_defender | quick_scan | `path=C:\` | Scan directory |
| process_monitor | get_info | `pid=1234` | Show process details |
| network_sniffer | get_connections | (none) | List active connections |
| file_integrity | watch_path | `path=/home/user/docs` | Monitor path |

**Output:**
```
▶️  Executing windows_defender.quick_scan({'path': 'C:\\'})...
   [Defender] 🔍 Quick scan running on C:\...
   [Defender] ✅ Quick scan complete | Threats: 0 | Files: 12,483

============================================================
Status: ✅ SUCCESS
Result: {'scan_type': 'quick', 'path': 'C:\\', 'threats_found': 0, 'files_scanned': 12483, 'scan_time': '2m 15s', 'timestamp': '2025-11-15T15:21:18.488132'}
============================================================
```

---

### **5. events** — Live Events View

Display real-time events from active widgets.

**Usage:**
```
Enter command (0-9): 5
```

**Output:**
```
📡 LIVE WIDGET EVENTS
============================================================

🔍 NETWORK_SNIFFER:
------------------------------------------------------------
  [15:20:53] OneDrive.exe    -> 52.104.58.55:443
  [15:20:53] Code.exe        -> 127.0.0.1:56406
  [15:20:53] comet.exe       -> 104.18.26.48:443
------------------------------------------------------------

🔍 PROCESS_MONITOR:
------------------------------------------------------------
  [15:02:06] PID  8596 | RuntimeBroker.exe
------------------------------------------------------------

🔍 WINDOWS_DEFENDER:
------------------------------------------------------------
  [15:21:18] quick_scan   | Threats: 0
------------------------------------------------------------
============================================================
```

**Shows last 10 events per widget:**
- **File Integrity:** file changes (created/modified/deleted)
- **Process Monitor:** new process spawns (PID + name)
- **Network Sniffer:** network connections (process + destination)
- **Windows Defender:** scan results
- **RRNC:** auto-response actions

---

### **6. logs** — Audit Trail

View recent audit log entries.

**Usage:**
```
Enter command (0-9): 6
```

**Output:**
```
📝 RECENT AUDIT LOGS
============================================================
[2025-11-15T15:10:34.694443] WIDGET_ENABLED: file_integrity
[2025-11-15T15:10:34.758565] WIDGET_ENABLED: windows_defender
[2025-11-15T15:11:48.000422] ACTION_EXECUTED: windows_defender.quick_scan({'path': 'C:\\'})
[2025-11-15T15:21:20.000000] PERMISSION_CHANGE: observe -> auto_respond
[2025-11-15T15:21:25.000000] USER_APPROVAL: isolate - true
============================================================
```

**Log types:**
- `STARTUP` — Guardian initialization
- `WIDGET_ENABLED` / `WIDGET_DISABLED` — Widget lifecycle
- `ACTION_EXECUTED` — Action completion
- `PERMISSION_CHANGE` — Permission level updates
- `USER_APPROVAL` — User decisions on escalations
- `USER_FEEDBACK` — User threat assessment feedback

---

### **7. orch_stats** — Orchestrator Statistics

Show AI orchestration metrics and decision statistics.

**Usage:**
```
Enter command (0-9): 7
```

**Output:**
```
🤖 ORCHESTRATOR STATISTICS (v1.0)
============================================================
Status: ⭕ Standby
Events Ingested: 0
Events Processed: 0
Decisions Made: 0

OrchA (AI Task Master):
  False positives tracked: 0
  Learning entries: 0

OrchB (Human-AI Bridge):
  Current permission: observe
  User decisions: 0

============================================================
```

**Metrics explained:**
- **Events Ingested** — Total events received from widgets
- **Events Processed** — Events analyzed & decided upon
- **Decisions Made** — Number of OrchA threat decisions
- **False Positives** — Events marked as false alarms by user
- **Learning Entries** — Training data for model improvement
- **User Decisions** — Count of user escalation approvals

---

### **8. set_perms** — Set Permission Level

Configure what actions Guardian is authorized to perform.

**Usage:**
```
Enter command (0-9): 8

🔐 SET PERMISSION LEVEL
==================================================
  1. observe         - Observe only (read-only)
  2. alert           - Can receive alerts
  3. analyze         - Can analyze & review
  4. isolate         - Can isolate threats
  5. auto_respond    - Auto-respond mode

Select permission level [1-5]: 5
   ✓ Permission level changed: observe -> auto_respond
   ✓ User permission updated: auto_respond
✅ Permission level set
```

**Permission levels (hierarchical):**

| Level | Capabilities | When to use |
|-------|-------------|------------|
| **Observe** | Read monitoring data + logs | First time testing |
| **Alert** | Above + notifications | Want to be notified |
| **Analyze** | Above + AI threat analysis | Need context on alerts |
| **Isolate** | Above + user-approved remediation | Want to approve before action |
| **Auto-Respond** | Above + auto execution | Trust Guardian completely |

---

### **9. help** — Show Help

Display command reference and quick-start guide.

**Usage:**
```
Enter command (0-9): 9
```

**Output:** Full help text with command descriptions and roadmap.

---

### **0. quit** — Exit Guardian

Gracefully shutdown Guardian.

**Usage:**
```
Enter command (0-9): 0

🛑 Shutting down Archie Guardian...
   ⭕ Process Monitor Widget stopped
   ⭕ Network Sniffer Widget stopped
   ⭕ Windows Defender Widget deactivated
   ⭕ RRNC deactivated
✅ Goodbye!
```

---

## 🚨 Escalation Prompts

When Guardian detects a MEDIUM/HIGH threat and user permission level requires approval:

```
╔════════════════════════════════════════════════════╗
║           ⚠️  ESCALATION REQUIRED                 ║
╚════════════════════════════════════════════════════╝

🔴 Threat Level: MEDIUM
📊 Confidence: 78.5%
💡 Recommended Action: isolate
📝 Reason: Suspicious process spawning from temp directory

Context:
  process: evil.exe
  pid: 1234
  parent: explorer.exe
  command_line: C:\Temp\evil.exe --steal-tokens

════════════════════════════════════════════════════

Allow action? [Y/n]: y

   ✅ Action approved
```

**Respond:**
- `y` or `yes` or just press Enter → Approve action
- `n` or `no` → Deny action

---

## 📝 Feedback Prompts

After action execution, you may be asked for feedback:

```
📝 Feedback for event ev_abc123
   (OrchA score: 78%)

[1] False positive (should NOT have alerted)
[2] Confirmed threat (good catch!)
[3] Missed details (needs refinement)
[4] Skip

Choice [1-4]: 2
   ✓ Feedback recorded: confirmed_threat
```

**Your feedback trains the AI** → improves future threat scoring.

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+C` | Interrupt current operation (graceful shutdown) |
| Enter | Confirm selection |
| `1-9` | Select menu option |

---

## 🐛 Troubleshooting

### Widget won't enable
```
❌ Failed to init windows_defender: ...
```
**Solution:** Check Windows Defender is installed (`Get-MpComputerStatus` in PowerShell)

### No events showing
```
📡 LIVE WIDGET EVENTS
No active widget events yet. Enable a widget first!
```
**Solution:** Run `2` (enable), then wait a few seconds for events to be generated

### Permission denied on action
```
User: observe | Required: isolate
Reason: User permission: observe, required: isolate
```
**Solution:** Run `8` (set_perms) to increase permission level

---

## 📚 Advanced Usage

### Batch Operations

```
Select widget(s): 1-5        # Enable all 5 widgets
Select widget(s) to disable: 2,4  # Disable widgets 2 and 4
```

### Monitoring Specific Paths

```
Select action: watch_path
Enter parameters: path=C:\Users\archi\Documents
```

---

**Need help?** Open an issue: https://github.com/archiesgate42-glitch/archie-guardian/issues
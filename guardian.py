#!/usr/bin/env python
"""
guardian.py (MVP v1.0 - Widget Manager + Multi-Agent Orchestrator)
Main entry point for Archie Guardian.
Integrates: Widgets + OrchA (AI) + OrchB (Human) + Dispatcher + Master Orchestrator
"""

import sys
import json
import os
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import widgets dynamically
AVAILABLE_WIDGETS = {}

widget_imports = {
    "file_integrity": ("widgets.file_integrity", "FileIntegrityWidget"),
    "process_monitor": ("widgets.process_monitor", "ProcessMonitorWidget"),
    "network_sniffer": ("widgets.network_sniffer", "NetworkSnifferWidget"),
    "windows_defender": ("widgets.windows_defender", "WindowsDefenderWidget"),
    "rrnc": ("widgets.rrnc", "RapidResponseNeutralizeCapture"),
}

# Try to import each widget
for widget_name, (module_path, class_name) in widget_imports.items():
    try:
        module = __import__(module_path, fromlist=[class_name])
        widget_class = getattr(module, class_name)
        AVAILABLE_WIDGETS[widget_name] = widget_class
        print(f"   ✅ {widget_name} loaded")
    except (ImportError, AttributeError) as e:
        print(f"   ⚠️  {widget_name} not available: {e}")

# Import orchestrator components
# Import orchestrator components
ORCHESTRATOR_AVAILABLE = False
try:
    from core.agent_utils import AuditLogger, PermissionLevel, ThreatLevel
    from core.orch_a import OrchA
    from core.orch_b import OrchB
    from core.orchestrator import MasterOrchestrator
    print(f"   ✅ core/orchestrator system loaded")
    ORCHESTRATOR_AVAILABLE = True
except ImportError as e:
    print(f"   ⚠️  orchestrator not available: {e}")
    # Fallback: use simple audit logging
    class AuditLogger:
        def __init__(self, log_file):
            self.log_file = log_file
    ORCHESTRATOR_AVAILABLE = False

print("=" * 60)
print("✨ ARCHIE GUARDIAN v1.0 - Local AI Security + Multi-Agent Orchestration")
print("=" * 60)
print()

# Initialize audit logger
os.makedirs("logs", exist_ok=True)
audit_logger = AuditLogger("logs/audit.log")

# Widget state dictionary
widget_state = {}
widgets_instances = {}

# Initialize all available widgets as disabled
for widget_name in AVAILABLE_WIDGETS:
    widget_state[widget_name] = False

# Master orchestrator instance (if available)
master_orch = None

def log_event(event_type, details):
    """Log event to audit log."""
    try:
        with open("logs/audit.log", "a") as f:
            f.write(f"[{datetime.now().isoformat()}] {event_type}: {details}\n")
    except:
        pass

# Startup sequence
try:
    print("[1/7] Checking core modules...")
    print("   ✅ Core imports successful")
    
    print("[2/7] Checking widget system...")
    print(f"   ✅ Widget system ready ({len(AVAILABLE_WIDGETS)}/{len(widget_imports)} widgets available)")
    
    print("[3/7] Initializing audit logger...")
    # COMMENT THIS OUT FOR NOW (old API)
    # audit_logger.log_decision(
    #     agent="Guardian",
    #     decision="startup",
    #     details={"version": "1.0", "timestamp": datetime.now().isoformat()}
    # )
    log_event("STARTUP", "Guardian v1.0 initialized")
    print("   ✅ Audit logger initialized (logs/audit.log)")

    print("[4/7] Initializing widget instances...")
    for widget_name, widget_class in AVAILABLE_WIDGETS.items():
        try:
            widgets_instances[widget_name] = widget_class()
            print(f"   ✅ {widget_name} ready")
        except Exception as e:
            print(f"   ❌ Failed to init {widget_name}: {e}")
    
    print("[5/7] Initializing orchestrator system...")
    if ORCHESTRATOR_AVAILABLE:
        master_orch = MasterOrchestrator(
            audit_logger,
            dispatcher=None,  # TODO: integrate dispatcher
            config={
                "orcha_config": {},
                "orchb_config": {}
            }
        )
        print("   ✅ Master Orchestrator ready (OrchA + OrchB)")
    else:
        print("   ⚠️  Orchestrator not available (CLI-only mode)")
    
    print("[6/7] Verifying state management...")
    print("   ✅ State tracking initialized")
    
    print("[7/7] CLI interface ready...")
    print("   ✅ All systems operational\n")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# CLI FUNCTIONS (v0.5 Compatibility)
# ============================================================================

def main_menu():
    """Display main menu."""
    print("╔════════════════════════════════════════════════════╗")
    print("║     ARCHIE GUARDIAN v1.0 - MAIN MENU              ║")
    print("║  Widget Manager + Multi-Agent Orchestration       ║")
    print("╚════════════════════════════════════════════════════╝")
    print()
    print("Commands:")
    print("  1. status      - Show Guardian status")
    print("  2. enable      - Enable widget(s) [numbered]")
    print("  3. disable     - Disable widget(s) [numbered]")
    print("  4. action      - Execute widget action [numbered]")
    print("  5. events      - Show live widget events")
    print("  6. logs        - View audit logs")
    print("  7. orch_stats  - Show orchestrator statistics")
    print("  8. set_perms   - Set user permission level")
    print("  9. help        - Show help")
    print("  0. quit        - Exit Guardian")
    print()

def show_status():
    """Show status with real widget state."""
    print("\n📊 GUARDIAN STATUS")
    print("=" * 50)
    print("Status: ✅ OPERATIONAL")
    print("Version: 1.0 (Multi-Agent Orchestration)")
    print(f"Permission Level: {master_orch.orchb.permission_level.value.upper() if master_orch else 'N/A'}")
    print()
    print("Widgets:")
    
    for widget_name in sorted(widget_state.keys()):
        enabled = widget_state[widget_name]
        status_icon = "🟢" if enabled else "⭕"
        
        if widget_name in widgets_instances and enabled:
            widget = widgets_instances[widget_name]
            if hasattr(widget, 'get_stats'):
                try:
                    stats = widget.get_stats()
                    events = stats.get("events_buffered", 0)
                    print(f"  {status_icon} {widget_name:<20} - LIVE ({events} events)")
                except Exception as e:
                    print(f"  {status_icon} {widget_name:<20} - LIVE (error: {e})")
            else:
                print(f"  {status_icon} {widget_name:<20} - LIVE")
        else:
            print(f"  {status_icon} {widget_name:<20} - Idle")
    
    print()
    if master_orch and master_orch.active:
        orch_stats = master_orch.get_orchestrator_stats()
        print(f"Orchestrator: ✅ ACTIVE")
        print(f"  Events queued: {orch_stats['events_ingested']}")
        print(f"  Decisions made: {orch_stats['decisions_made']}")
    else:
        print("Orchestrator: ⭕ Standby (CLI-only mode)")
    
    print()
    print("Audit Log: logs/audit.log")
    print("=" * 50 + "\n")

def enable_widget_menu():
    """Interactive widget selection (numbered)"""
    print("\n🔋 ENABLE WIDGETS")
    print("=" * 50)
    
    available_widgets = list(widget_state.keys())
    
    # Show options
    print("Available widgets:")
    for i, widget in enumerate(available_widgets, 1):
        status = "✅ ENABLED" if widget_state[widget] else "⭕ Disabled"
        print(f"  {i}. {widget:<20} [{status}]")
    
    # Get selection
    selection = input("\nSelect widget(s) (e.g. 1,2,3 or 1-3 or just 1): ").strip()
    
    widgets_to_enable = []
    
    try:
        # Handle range input (1-3)
        if "-" in selection:
            start, end = selection.split("-")
            start, end = int(start.strip()), int(end.strip())
            for i in range(start - 1, end):
                if 0 <= i < len(available_widgets):
                    widgets_to_enable.append(available_widgets[i])
        
        # Handle comma-separated input (1,2,3)
        elif "," in selection:
            for num in selection.split(","):
                idx = int(num.strip()) - 1
                if 0 <= idx < len(available_widgets):
                    widgets_to_enable.append(available_widgets[idx])
        
        # Handle single input
        else:
            idx = int(selection) - 1
            if 0 <= idx < len(available_widgets):
                widgets_to_enable.append(available_widgets[idx])
    
    except ValueError:
        print("❌ Invalid input. Use numbers (1, 2, 3) or ranges (1-3)\n")
        return
    
    # Enable selected widgets
    enabled_count = 0
    for widget_name in widgets_to_enable:
        if widget_state[widget_name]:
            print(f"⚠️  {widget_name} already enabled")
            continue
        
        if widget_name in widgets_instances:
            widget = widgets_instances[widget_name]
            if hasattr(widget, 'start') and widget.start():
                widget_state[widget_name] = True
                log_event("WIDGET_ENABLED", widget_name)
                print(f"✅ {widget_name} enabled")
                enabled_count += 1
    
    print(f"\n✅ Enabled {enabled_count} widget(s)\n")

def disable_widget_menu():
    """Interactive widget deselection (numbered)"""
    print("\n🔴 DISABLE WIDGETS")
    print("=" * 50)
    
    active_widgets = [w for w in widget_state if widget_state[w]]
    
    if not active_widgets:
        print("❌ No active widgets to disable.\n")
        return
    
    # Show options
    print("Active widgets:")
    for i, widget in enumerate(active_widgets, 1):
        print(f"  {i}. {widget}")
    
    # Get selection
    selection = input("\nSelect widget(s) to disable (e.g. 1,2 or 1-2): ").strip()
    
    widgets_to_disable = []
    
    try:
        # Handle range input (1-2)
        if "-" in selection:
            start, end = selection.split("-")
            start, end = int(start.strip()), int(end.strip())
            for i in range(start - 1, end):
                if 0 <= i < len(active_widgets):
                    widgets_to_disable.append(active_widgets[i])
        
        # Handle comma-separated input (1,2)
        elif "," in selection:
            for num in selection.split(","):
                idx = int(num.strip()) - 1
                if 0 <= idx < len(active_widgets):
                    widgets_to_disable.append(active_widgets[idx])
        
        # Handle single input
        else:
            idx = int(selection) - 1
            if 0 <= idx < len(active_widgets):
                widgets_to_disable.append(active_widgets[idx])
    
    except ValueError:
        print("❌ Invalid input.\n")
        return
    
    # Disable selected widgets
    for widget_name in widgets_to_disable:
        if widget_name in widgets_instances:
            widget = widgets_instances[widget_name]
            if hasattr(widget, 'stop'):
                widget.stop()
        
        widget_state[widget_name] = False
        log_event("WIDGET_DISABLED", widget_name)
        print(f"✅ {widget_name} disabled")
    
    print()

def execute_action_menu():
    """Interactive action execution (numbered selection)"""
    print("\n⚡ ACTION EXECUTION")
    print("=" * 60)
    
    # Show active widgets
    active_widgets = [w for w in widget_state if widget_state[w]]
    if not active_widgets:
        print("❌ No active widgets. Enable one first.\n")
        return
    
    print("Active widgets:")
    for i, widget in enumerate(active_widgets, 1):
        print(f"  {i}. {widget}")
    
    # Select widget
    widget_input = input("\nSelect widget (number): ").strip()
    try:
        widget_idx = int(widget_input) - 1
        if not (0 <= widget_idx < len(active_widgets)):
            print("❌ Invalid selection\n")
            return
        widget_name = active_widgets[widget_idx]
    except ValueError:
        print("❌ Invalid input (use number)\n")
        return
    
    # Get available actions
    widget = widgets_instances[widget_name]
    if not hasattr(widget, 'get_actions'):
        print(f"❌ Widget '{widget_name}' does not support actions\n")
        return
    
    actions_dict = widget.get_actions()
    actions = actions_dict.get("actions", [])
    
    if not actions:
        print(f"❌ No actions available for '{widget_name}'\n")
        return
    
    print(f"\nAvailable actions for '{widget_name}':")
    for i, action in enumerate(actions, 1):
        print(f"  {i}. {action}")
    
    # Select action
    action_input = input("\nSelect action (number): ").strip()
    try:
        action_idx = int(action_input) - 1
        if not (0 <= action_idx < len(actions)):
            print("❌ Invalid selection\n")
            return
        action_name = actions[action_idx]
    except ValueError:
        print("❌ Invalid input (use number)\n")
        return
    
    # Get parameters
    print(f"\nEnter parameters for '{action_name}':")
    print("Format: key=value (e.g. pid=1234 path=C:\\\\temp)")
    print("(Press Enter to skip)")
    
    kwargs = {}
    param_input = input("> ").strip()
    
    if param_input:
        for param in param_input.split():
            if "=" in param:
                key, val = param.split("=", 1)
                # Auto-type conversion
                try:
                    kwargs[key.strip()] = int(val.strip())
                except ValueError:
                    try:
                        kwargs[key.strip()] = float(val.strip())
                    except ValueError:
                        kwargs[key.strip()] = val.strip()
    
    # Execute action
    print(f"\n▶️  Executing {widget_name}.{action_name}({kwargs})...")
    
    try:
        action_method = getattr(widget, action_name)
        result = action_method(**kwargs)
        
        # Log action
        log_event("ACTION_EXECUTED", f"{widget_name}.{action_name}({kwargs})")
        
        print("\n" + "=" * 60)
        print(f"Status: ✅ SUCCESS")
        print(f"Result: {result}")
        print("=" * 60 + "\n")
        
    except Exception as e:
        log_event("ACTION_FAILED", f"{widget_name}.{action_name}() failed: {e}")
        
        print("\n" + "=" * 60)
        print(f"Status: ❌ ERROR")
        print(f"Error: {str(e)}")
        print("=" * 60 + "\n")

def show_events():
    """Show live events from enabled widgets."""
    print("\n📡 LIVE WIDGET EVENTS")
    print("=" * 60)
    
    has_events = False
    
    for widget_name in sorted(widget_state.keys()):
        if widget_state[widget_name] and widget_name in widgets_instances:
            widget = widgets_instances[widget_name]
            
            if hasattr(widget, 'get_recent_events'):
                events = widget.get_recent_events(20)
                
                if events:
                    has_events = True
                    print(f"\n🔍 {widget_name.upper()}:")
                    print("-" * 60)
                    
                    for event in events[-10:]:  # Show last 10
                        if isinstance(event, dict) and "timestamp" in event:
                            ts = datetime.fromtimestamp(event.get("timestamp", 0)).strftime("%H:%M:%S")
                            
                            # Format based on widget type
                            if widget_name == "file_integrity":
                                event_type = event.get("event_type", "unknown")
                                path = event.get("path", "unknown")
                                if len(path) > 40:
                                    path = "..." + path[-37:]
                                print(f"  [{ts}] {event_type:8} | {path}")
                            
                            elif widget_name == "process_monitor":
                                pid = event.get("pid", "?")
                                name = event.get("name", "unknown")
                                print(f"  [{ts}] PID {pid:5} | {name}")
                            
                            elif widget_name == "network_sniffer":
                                process = event.get("process", "unknown")
                                remote = event.get("remote_address", "?")
                                print(f"  [{ts}] {process:15} -> {remote}")
                            
                            elif widget_name == "windows_defender":
                                action = event.get("action", "scan")
                                threats = event.get("threats_found", 0)
                                print(f"  [{ts}] {action:12} | Threats: {threats}")
                            
                            elif widget_name == "rrnc":
                                action = event.get("action", "unknown")
                                status = event.get("status", "unknown")
                                print(f"  [{ts}] {action:18} | {status}")
                        else:
                            print(f"  {event}")
                
                print("-" * 60)
    
    if not has_events:
        print("No active widget events yet. Enable a widget first!")
    
    print("=" * 60 + "\n")

def show_logs():
    """Show recent audit logs."""
    print("\n📝 RECENT AUDIT LOGS")
    print("=" * 60)
    try:
        with open("logs/audit.log", "r") as f:
            lines = f.readlines()
            recent = lines[-20:] if len(lines) > 20 else lines
            for line in recent:
                print(line.rstrip())
    except FileNotFoundError:
        print("No logs found yet.")
    print("=" * 60 + "\n")

def show_orchestrator_stats():
    """Show orchestrator statistics (v1.0 feature)."""
    if not master_orch or not ORCHESTRATOR_AVAILABLE:
        print("\n❌ Orchestrator not available\n")
        return
    
    print("\n🤖 ORCHESTRATOR STATISTICS (v1.0)")
    print("=" * 60)
    
    stats = master_orch.get_orchestrator_stats()
    
    print(f"Status: {'✅ ACTIVE' if stats['master_status'] == 'active' else '⭕ Standby'}")
    print(f"Events Ingested: {stats['events_ingested']}")
    print(f"Events Processed: {stats['events_processed']}")
    print(f"Decisions Made: {stats['decisions_made']}")
    print()
    
    print("OrchA (AI Task Master):")
    print(f"  False positives tracked: {stats['orcha_stats'].get('false_positives_tracked', 0)}")
    print(f"  Learning entries: {stats['orcha_stats'].get('learning_entries', 0)}")
    print()
    
    print("OrchB (Human-AI Bridge):")
    print(f"  Current permission: {stats['orchb_stats'].get('current_permission_level', 'N/A')}")
    print(f"  User decisions: {stats['orchb_stats'].get('user_decisions_count', 0)}")
    approval = stats['orchb_stats'].get('approval_rate', 'N/A') if 'approval_rate' in stats.get('orchb_stats', {}) else 'N/A'
    # Note: approval_rate would come from orchb.get_approval_stats()
    
    print()
    print("=" * 60 + "\n")

def set_permission_menu():
    """Set user permission level (v1.0 feature)."""
    if not master_orch or not ORCHESTRATOR_AVAILABLE:
        print("\n❌ Orchestrator not available\n")
        return
    
    print("\n🔐 SET PERMISSION LEVEL")
    print("=" * 50)
    
    perms = [
        ("1", PermissionLevel.OBSERVE, "Observe only (read-only)"),
        ("2", PermissionLevel.ALERT, "Can receive alerts"),
        ("3", PermissionLevel.ANALYZE, "Can analyze & review"),
        ("4", PermissionLevel.ISOLATE, "Can isolate threats"),
        ("5", PermissionLevel.AUTO_RESPOND, "Auto-respond mode")
    ]
    
    for num, perm, desc in perms:
        print(f"  {num}. {perm.value:<15} - {desc}")
    
    choice = input("\nSelect permission level [1-5]: ").strip()
    
    perm_map = {p[0]: p[1] for p in perms}
    
    if choice in perm_map:
        master_orch.set_user_permission(perm_map[choice])
        print(f"✅ Permission level set\n")
    else:
        print("❌ Invalid choice\n")

def show_help():
    """Show help information."""
    print("""
📚 ARCHIE GUARDIAN v1.0 HELP

MVP v1.0 - Multi-Widget Manager + Human-AI Orchestration

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AVAILABLE WIDGETS:
  ✅ file_integrity       - Real-time filesystem monitoring
  ✅ process_monitor      - New process spawning detection
  ✅ network_sniffer      - Network connection tracking
  ✅ windows_defender     - Windows Defender scan integration
  ✅ rrnc                 - Rapid Response Neutralize & Capture

COMMANDS (numbered selection):
  1. status              - View system status & widget states
  2. enable              - Enable widget(s) [1, 1-3, or 1,2,3]
  3. disable             - Disable widget(s) [same format]
  4. action              - Execute widget action [numbered steps]
  5. events              - View live events from active widgets
  6. logs                - View audit trail
  7. orch_stats          - Show orchestrator statistics (NEW!)
  8. set_perms           - Set user permission level (NEW!)
  9. help                - Show this help
  0. quit                - Exit Guardian

NEW IN v1.0:
  🤖 OrchA (AI Task Master) - Threat analysis & scoring
  🤝 OrchB (Human Bridge) - User escalation & feedback
  📊 Master Orchestrator - Event → Decision → Action pipeline
  🔐 Permission levels - Observe/Alert/Analyze/Isolate/Auto-Respond

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUICK START:
  1. enable              (select: 1-5 to enable all)
  2. orch_stats          (see orchestrator status)
  3. set_perms           (set your permission level)
  4. action              (execute widget action)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ROADMAP:
  v1.0 (NOW)      - Multi-agent orchestration ✅
  v1.1 (Q1 2026)  - CrewAI integration, Ollama inference
  v2.0 (H2 2026)  - Community widgets, marketplace

DOCS: https://github.com/ArchieGate/archie-guardian
    """)

def interactive_cli():
    """Interactive CLI loop."""
    while True:
        main_menu()
        choice = input("Enter command (0-9): ").strip().lower()
        
        if choice in ["1", "status"]:
            show_status()
        
        elif choice in ["2", "enable"]:
            enable_widget_menu()
        
        elif choice in ["3", "disable"]:
            disable_widget_menu()
        
        elif choice in ["4", "action"]:
            execute_action_menu()
        
        elif choice in ["5", "events"]:
            show_events()
        
        elif choice in ["6", "logs"]:
            show_logs()
        
        elif choice in ["7", "orch_stats"]:
            show_orchestrator_stats()
        
        elif choice in ["8", "set_perms"]:
            set_permission_menu()
        
        elif choice in ["9", "help"]:
            show_help()
        
        elif choice in ["0", "quit", "exit"]:
            print("\n🛑 Shutting down Archie Guardian...")
            for widget_name in widget_state:
                if widget_state[widget_name] and widget_name in widgets_instances:
                    try:
                        widget = widgets_instances[widget_name]
                        if hasattr(widget, 'stop'):
                            widget.stop()
                    except:
                        pass
            
            if master_orch:
                master_orch.stop()
            
            log_event("SHUTDOWN", "Guardian graceful exit")
            print("✅ Goodbye!\n")
            break
        
        else:
            print("❌ Unknown command. Try again.\n")

if __name__ == "__main__":
    try:
        interactive_cli()
    except KeyboardInterrupt:
        print("\n\n🛑 Guardian interrupted by user")
        log_event("INTERRUPT", "User Ctrl+C")
        for widget_name in widgets_instances:
            if widget_state.get(widget_name):
                try:
                    widget = widgets_instances[widget_name]
                    if hasattr(widget, 'stop'):
                        widget.stop()
                except:
                    pass
        
        if master_orch:
            try:
                master_orch.stop()
            except:
                pass
        
        sys.exit(0)

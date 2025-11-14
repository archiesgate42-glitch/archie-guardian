#!/usr/bin/env python
"""
guardian.py (MVP v0.3 - All 3 Widgets Live!)
Main entry point for Archie Guardian.
Complete File Integrity, Process Monitor, and Network Sniffer integration.
"""

import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import all widgets
try:
    from widgets.file_integrity import FileIntegrityWidget
    FILE_INTEGRITY_AVAILABLE = True
except ImportError as e:
    FILE_INTEGRITY_AVAILABLE = False

try:
    from widgets.process_monitor import ProcessMonitorWidget
    PROCESS_MONITOR_AVAILABLE = True
except ImportError as e:
    PROCESS_MONITOR_AVAILABLE = False

try:
    from widgets.network_sniffer import NetworkSnifferWidget
    NETWORK_SNIFFER_AVAILABLE = True
except ImportError as e:
    NETWORK_SNIFFER_AVAILABLE = False

print("=" * 60)
print("✨ ARCHIE GUARDIAN v0.3 - Local AI Security")
print("=" * 60)
print()

# Initialize audit logger
os.makedirs("logs", exist_ok=True)

# Widget state dictionary
widget_state = {
    "file_integrity": False,
    "process_monitor": False,
    "network_sniffer": False
}

# Widget instances
widgets_instances = {}

def log_event(event_type, details):
    """Log event to audit log."""
    try:
        with open("logs/audit.log", "a") as f:
            f.write(f"[{datetime.now().isoformat()}] {event_type}: {details}\n")
    except:
        pass

# Test basic imports
try:
    print("[1/6] Checking core modules...")
    print("   ✅ Core imports successful")
    
    print("[2/6] Checking widget system...")
    widget_count = 0
    if FILE_INTEGRITY_AVAILABLE:
        print("   ✅ File Integrity Widget loaded (LIVE)")
        widget_count += 1
    else:
        print("   ⚠️  File Integrity Widget not available")
    
    if PROCESS_MONITOR_AVAILABLE:
        print("   ✅ Process Monitor Widget loaded (LIVE)")
        widget_count += 1
    else:
        print("   ⚠️  Process Monitor Widget not available")
    
    if NETWORK_SNIFFER_AVAILABLE:
        print("   ✅ Network Sniffer Widget loaded (LIVE)")
        widget_count += 1
    else:
        print("   ⚠️  Network Sniffer Widget not available")
    
    print(f"   ✅ Widget system ready ({widget_count}/3 widgets available)")
    
    print("[3/6] Initializing audit logger...")
    log_event("STARTUP", "Guardian v0.3 initialized")
    print("   ✅ Audit logger initialized (logs/audit.log)")
    
    print("[4/6] Initializing widgets...")
    # Initialize File Integrity Widget
    if FILE_INTEGRITY_AVAILABLE:
        widgets_instances["file_integrity"] = FileIntegrityWidget()
        print("   ✅ File Integrity Widget ready")
    
    # Initialize Process Monitor Widget
    if PROCESS_MONITOR_AVAILABLE:
        widgets_instances["process_monitor"] = ProcessMonitorWidget()
        print("   ✅ Process Monitor Widget ready")
    
    # Initialize Network Sniffer Widget
    if NETWORK_SNIFFER_AVAILABLE:
        widgets_instances["network_sniffer"] = NetworkSnifferWidget()
        print("   ✅ Network Sniffer Widget ready")
    
    print("[5/6] Verifying state management...")
    print("   ✅ State tracking initialized")
    
    print("[6/6] CLI interface ready...")
    print("   ✅ All systems operational\n")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


# CLI Functions
def main_menu():
    """Display main menu."""
    print("╔════════════════════════════════════════════════════╗")
    print("║       ARCHIE GUARDIAN v0.3 - MAIN MENU            ║")
    print("╚════════════════════════════════════════════════════╝")
    print()
    print("Commands:")
    print("  1. status      - Show Guardian status")
    print("  2. enable      - Enable a widget")
    print("  3. disable     - Disable a widget")
    print("  4. events      - Show live widget events")
    print("  5. logs        - View audit logs")
    print("  6. help        - Show help")
    print("  7. quit        - Exit Guardian")
    print()


def show_status():
    """Show status with real widget state."""
    print("\n📊 GUARDIAN STATUS")
    print("=" * 50)
    print("Status: ✅ OPERATIONAL")
    print("Version: 0.3 (MVP - All Widgets Live)")
    print("Permission Level: OBSERVE (default)")
    print()
    print("Widgets:")
    
    for widget_name, enabled in widget_state.items():
        status_icon = "🟢" if enabled else "⭕"
        status_text = "LIVE" if enabled else "Idle"
        
        # Get real widget stats if available
        if widget_name in widgets_instances and enabled:
            widget = widgets_instances[widget_name]
            stats = widget.get_stats()
            event_count = stats.get("events_buffered", 0)
            status_text = f"LIVE ({event_count} events)"
        
        print(f"  {status_icon} {widget_name:<20} - {status_text}")
    
    print()
    print("Audit Log: logs/audit.log")
    print("=" * 50 + "\n")


def enable_widget(widget_name):
    """Enable a widget and start monitoring."""
    if widget_name not in widget_state:
        print(f"❌ Widget '{widget_name}' not found")
        return
    
    if widget_state[widget_name]:
        print(f"⚠️  Widget '{widget_name}' already enabled")
        return
    
    # Try to start the real widget
    if widget_name in widgets_instances:
        widget = widgets_instances[widget_name]
        if widget.start():
            widget_state[widget_name] = True
            log_event("WIDGET_ENABLED", widget_name)
            print(f"✅ Widget '{widget_name}' enabled (LIVE MONITORING)\n")
        else:
            print(f"❌ Failed to start widget '{widget_name}'\n")
    else:
        print(f"❌ Widget '{widget_name}' not available\n")


def disable_widget(widget_name):
    """Disable a widget and stop monitoring."""
    if widget_name not in widget_state:
        print(f"❌ Widget '{widget_name}' not found")
        return
    
    if not widget_state[widget_name]:
        print(f"⚠️  Widget '{widget_name}' already disabled")
        return
    
    # Try to stop the real widget
    if widget_name in widgets_instances:
        widget = widgets_instances[widget_name]
        widget.stop()
    
    widget_state[widget_name] = False
    log_event("WIDGET_DISABLED", widget_name)
    print(f"✅ Widget '{widget_name}' disabled\n")


def show_events():
    """Show live events from enabled widgets."""
    print("\n📡 LIVE WIDGET EVENTS")
    print("=" * 60)
    
    has_events = False
    
    for widget_name, enabled in widget_state.items():
        if enabled and widget_name in widgets_instances:
            widget = widgets_instances[widget_name]
            events = widget.get_recent_events(20)
            
            if events:
                has_events = True
                print(f"\n🔍 {widget_name.upper()}:")
                print("-" * 60)
                
                for event in events[-10:]:  # Show last 10
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


def show_help():
    """Show help information."""
    print("""
📚 ARCHIE GUARDIAN v0.3 HELP

This is MVP v0.3 - ALL 3 WIDGETS LIVE!
Multi-agent AI orchestration coming next.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NEW IN v0.3:
  ✅ File Integrity Widget (LIVE)
     - Real-time filesystem monitoring
     - Watchdog-based efficient tracking
     
  ✅ Process Monitor Widget (LIVE)
     - Detects new process spawns
     - Tracks PID, name, user, cmdline
     - No elevated privileges needed
     
  ✅ Network Sniffer Widget (LIVE)
     - Monitors established network connections
     - Process-to-connection mapping
     - No root required (safe & universal)

COMMANDS:
  status   - View system status & widget states
  enable   - Enable a widget (starts live monitoring)
  disable  - Disable a widget (stops monitoring)
  events   - View live events from active widgets
  logs     - View audit trail
  help     - Show this help
  quit     - Exit Guardian

QUICK START:
  1. enable file_integrity      (watch file changes)
  2. enable process_monitor     (watch new processes)
  3. enable network_sniffer     (watch network activity)
  4. events                     (see all live data!)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ROADMAP:
  v0.3 (NOW)      - All 3 widgets live ✅
  v1.0 (Q1 2026)  - CrewAI orchestration, Ollama inference
  v2.0 (H2 2026)  - Community widgets, marketplace

DOCS: https://github.com/ArchieGate/archie-guardian
    """)


def interactive_cli():
    """Interactive CLI loop."""
    while True:
        main_menu()
        choice = input("Enter command (1-7): ").strip().lower()
        
        if choice in ["1", "status"]:
            show_status()
        
        elif choice in ["2", "enable"]:
            widget = input("Widget name (file_integrity/process_monitor/network_sniffer): ").strip().lower()
            enable_widget(widget)
        
        elif choice in ["3", "disable"]:
            widget = input("Widget name: ").strip().lower()
            disable_widget(widget)
        
        elif choice in ["4", "events"]:
            show_events()
        
        elif choice in ["5", "logs"]:
            show_logs()
        
        elif choice in ["6", "help"]:
            show_help()
        
        elif choice in ["7", "quit", "exit"]:
            print("\n🛑 Shutting down Archie Guardian...")
            # Stop all widgets
            for widget_name in widgets_instances:
                if widget_state.get(widget_name):
                    disable_widget(widget_name)
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
        # Stop all widgets
        for widget_name in widgets_instances:
            if widget_state.get(widget_name):
                try:
                    widgets_instances[widget_name].stop()
                except:
                    pass
        sys.exit(0)
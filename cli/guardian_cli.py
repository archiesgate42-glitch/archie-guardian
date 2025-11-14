"""
cli/guardian_cli.py
Command-line interface for Archie Guardian.
"""

import cmd
import sys


class GuardianCLI(cmd.Cmd):
    """Interactive CLI for Archie Guardian."""
    
    intro = """
╔════════════════════════════════════════════════════╗
║     ARCHIE GUARDIAN v0.1 - Local AI Security       ║
║        Type 'help' for available commands          ║
╚════════════════════════════════════════════════════╝
"""
    
    prompt = "guardian> "
    
    def __init__(self, guardian_instance):
        super().__init__()
        self.guardian = guardian_instance
    
    def do_status(self, arg):
        """Show current Guardian status."""
        self.guardian.status()
    
    def do_enable(self, arg):
        """Enable a widget. Usage: enable <widget_name>"""
        if not arg:
            print("❌ Usage: enable <widget_name>")
            print("   Available widgets: file_integrity, process_monitor, network_sniffer")
            return
        
        widget_name = arg.strip().lower()
        self.guardian.enable_widget(widget_name)
    
    def do_disable(self, arg):
        """Disable a widget. Usage: disable <widget_name>"""
        if not arg:
            print("❌ Usage: disable <widget_name>")
            return
        
        widget_name = arg.strip().lower()
        self.guardian.disable_widget(widget_name)
    
    def do_logs(self, arg):
        """Show recent audit logs."""
        try:
            with open("logs/audit.log", "r") as f:
                lines = f.readlines()
                # Show last 20 lines
                recent = lines[-20:] if len(lines) > 20 else lines
                print("\n" + "="*60)
                print("RECENT AUDIT LOG")
                print("="*60)
                for line in recent:
                    print(line.rstrip())
                print("="*60 + "\n")
        except FileNotFoundError:
            print("❌ No audit log found yet")
    
    def do_permission(self, arg):
        """Set user permission level. Usage: permission <level>"""
        if not arg:
            from core.agent_utils import PermissionLevel
            levels = [p.value for p in PermissionLevel]
            print(f"❌ Usage: permission <level>")
            print(f"   Available levels: {', '.join(levels)}")
            return
        
        level_str = arg.strip().lower()
        
        try:
            from core.agent_utils import PermissionLevel
            level = PermissionLevel[level_str.upper()]
            self.guardian.orch_b.set_permission_level(level)
            print(f"✅ Permission level set to: {level.value}")
        except KeyError:
            print(f"❌ Invalid permission level: {level_str}")
    
    def do_analyze(self, arg):
        """Manually trigger analysis on buffered events."""
        print("🔍 Analyzing buffered events...")
        
        total_analyzed = 0
        for widget_name, widget in self.guardian.widgets.items():
            if widget.enabled:
                events = widget.get_events()
                for event in events:
                    analysis = self.guardian.orch_a.analyze_event(event)
                    alert = self.guardian.orch_b.handle_alert(analysis)
                    
                    print(f"   [{widget_name}] {alert['message']}")
                    total_analyzed += 1
                
                widget.clear_events()
        
        print(f"✅ Analyzed {total_analyzed} events\n")
    
    def do_feedback(self, arg):
        """Mark an event as false positive. Usage: feedback <event_id>"""
        if not arg:
            print("❌ Usage: feedback <event_id>")
            return
        
        event_id = arg.strip()
        
        # Get user feedback
        feedback = self.guardian.orch_b.get_user_feedback(event_id)
        
        # Pass to OrchA for learning
        if feedback != "skip":
            self.guardian.orch_a.learn_from_feedback(event_id, feedback)
            print(f"✅ Feedback recorded: {feedback}\n")
    
    def do_config(self, arg):
        """Show current configuration."""
        print("\n" + "="*60)
        print("CONFIGURATION")
        print("="*60)
        print(f"Manifest: {self.guardian.manifest}")
        print(f"User Config: {self.guardian.user_config}")
        print("="*60 + "\n")
    
    def do_quit(self, arg):
        """Exit Guardian."""
        self.guardian.shutdown()
        return True
    
    def do_help(self, arg):
        """Show help."""
        super().do_help(arg)
    
    def emptyline(self):
        """Do nothing on empty input."""
        pass
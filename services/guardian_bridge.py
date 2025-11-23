"""
GuardianBridge Service
Interface tussen Flask UI en guardian.py backend
"""

import sys
import os
import json
import threading
from typing import Dict, List, Any, Optional, Generator
from datetime import datetime

# Add parent directory to path to import guardian modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # Try to import guardian module directly
    # Note: guardian.py must be imported before GuardianBridge is used
    # The start_ui.py script handles this initialization
    import guardian
    from core.agent_utils import PermissionLevel
except ImportError as e:
    # If guardian is not yet loaded, we'll handle it gracefully
    guardian = None
    try:
        from core.agent_utils import PermissionLevel
    except ImportError:
        PermissionLevel = None
except Exception as e:
    print(f"Warning: Error loading guardian: {e}")
    guardian = None
    PermissionLevel = None


class GuardianBridge:
    """
    Bridge service tussen Flask UI en guardian.py backend.
    Singleton pattern voor thread-safe access.
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Singleton pattern."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(GuardianBridge, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize bridge (only called once due to singleton)."""
        if hasattr(self, '_initialized'):
            return
        
        self._initialized = True
        self._guardian_loaded = False
        
        # Try to load guardian.py globals
        self._load_guardian()
    
    def _load_guardian(self):
        """Load guardian.py globals if available."""
        try:
            if guardian and hasattr(guardian, 'widget_state'):
                self.widget_state = guardian.widget_state
                self.widgets_instances = guardian.widgets_instances
                self.master_orch = guardian.master_orch
                self.audit_logger = guardian.audit_logger
                self._guardian_loaded = True
                print("✅ GuardianBridge: Connected to guardian.py backend")
            else:
                print("⚠️  GuardianBridge: guardian.py not loaded, using fallback mode")
                self._guardian_loaded = False
        except Exception as e:
            print(f"⚠️  GuardianBridge: Error loading guardian: {e}")
            self._guardian_loaded = False
    
    def is_connected(self) -> bool:
        """Check if bridge is connected to guardian backend."""
        return self._guardian_loaded
    
    def get_widget_status(self, widget_name: str) -> Dict[str, Any]:
        """
        Haal widget status op.
        
        Args:
            widget_name: Naam van de widget
            
        Returns:
            dict: Widget status informatie
        """
        if not self._guardian_loaded:
            return {
                "name": widget_name,
                "active": False,
                "error": "Guardian backend not loaded"
            }
        
        try:
            is_active = self.widget_state.get(widget_name, False)
            widget_instance = self.widgets_instances.get(widget_name)
            
            status = {
                "name": widget_name,
                "active": is_active,
                "status": "active" if is_active else "idle"
            }
            
            # Get additional stats if widget is active
            if is_active and widget_instance:
                if hasattr(widget_instance, 'get_stats'):
                    try:
                        stats = widget_instance.get_stats()
                        status.update(stats)
                    except:
                        pass
                
                if hasattr(widget_instance, 'get_status'):
                    try:
                        widget_status = widget_instance.get_status()
                        status.update(widget_status)
                        # Include model info for ollama_chat widget
                        if widget_name == 'ollama_chat' and 'model' in widget_status:
                            status['model'] = widget_status['model']
                    except:
                        pass
            
            return status
            
        except Exception as e:
            return {
                "name": widget_name,
                "active": False,
                "status": "error",
                "error": str(e)
            }
    
    def get_all_widgets_status(self) -> List[Dict[str, Any]]:
        """Haal status van alle widgets op."""
        if not self._guardian_loaded:
            return []
        
        widgets = []
        for widget_name in self.widget_state.keys():
            widgets.append(self.get_widget_status(widget_name))
        
        return widgets
    
    def start_widget(self, widget_name: str) -> Dict[str, Any]:
        """
        Start een widget.
        
        Args:
            widget_name: Naam van de widget
            
        Returns:
            dict: Result met success status
        """
        if not self._guardian_loaded:
            return {
                "success": False,
                "error": "Guardian backend not loaded"
            }
        
        try:
            # Check if widget exists
            if widget_name not in self.widgets_instances:
                return {
                    "success": False,
                    "error": f"Widget '{widget_name}' not found"
                }
            
            # Check if already active
            if self.widget_state.get(widget_name, False):
                return {
                    "success": True,
                    "message": f"Widget '{widget_name}' already active",
                    "status": "active"
                }
            
            # Start widget
            widget_instance = self.widgets_instances[widget_name]
            if hasattr(widget_instance, 'start'):
                success = widget_instance.start()
                if success:
                    self.widget_state[widget_name] = True
                    
                    # Log event
                    if hasattr(self, 'audit_logger'):
                        try:
                            with open("logs/audit.log", "a", encoding="utf-8") as f:
                                f.write(f"[{datetime.now().isoformat()}] WIDGET_ENABLED: {widget_name}\n")
                        except:
                            pass
                    
                    return {
                        "success": True,
                        "message": f"Widget '{widget_name}' started",
                        "status": "active"
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to start widget '{widget_name}'"
                    }
            else:
                return {
                    "success": False,
                    "error": f"Widget '{widget_name}' has no start() method"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def stop_widget(self, widget_name: str) -> Dict[str, Any]:
        """
        Stop een widget.
        
        Args:
            widget_name: Naam van de widget
            
        Returns:
            dict: Result met success status
        """
        if not self._guardian_loaded:
            return {
                "success": False,
                "error": "Guardian backend not loaded"
            }
        
        try:
            # Check if widget exists
            if widget_name not in self.widgets_instances:
                return {
                    "success": False,
                    "error": f"Widget '{widget_name}' not found"
                }
            
            # Check if already inactive
            if not self.widget_state.get(widget_name, False):
                return {
                    "success": True,
                    "message": f"Widget '{widget_name}' already inactive",
                    "status": "idle"
                }
            
            # Stop widget
            widget_instance = self.widgets_instances[widget_name]
            if hasattr(widget_instance, 'stop'):
                widget_instance.stop()
                self.widget_state[widget_name] = False
                
                # Log event
                try:
                    with open("logs/audit.log", "a", encoding="utf-8") as f:
                        f.write(f"[{datetime.now().isoformat()}] WIDGET_DISABLED: {widget_name}\n")
                except:
                    pass
                
                return {
                    "success": True,
                    "message": f"Widget '{widget_name}' stopped",
                    "status": "idle"
                }
            else:
                return {
                    "success": False,
                    "error": f"Widget '{widget_name}' has no stop() method"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def stream_logs(self, last_position: int = 0) -> Generator[str, None, None]:
        """
        Stream logs vanaf een bepaalde positie.
        
        Args:
            last_position: Laatste byte positie (voor resume)
            
        Yields:
            str: Nieuwe log entries
        """
        log_file = "logs/audit.log"
        
        if not os.path.exists(log_file):
            yield json.dumps({
                "log": "No log file found",
                "timestamp": datetime.now().isoformat()
            }) + "\n"
            return
        
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                # Seek to last position
                if last_position > 0:
                    f.seek(last_position)
                
                while True:
                    line = f.readline()
                    if line:
                        yield json.dumps({
                            "log": line.rstrip(),
                            "timestamp": datetime.now().isoformat()
                        }) + "\n"
                    else:
                        # Check file size for new content
                        current_pos = f.tell()
                        file_size = os.path.getsize(log_file)
                        
                        if file_size > current_pos:
                            # File was truncated or rotated, start from beginning
                            f.seek(0)
                        else:
                            # No new content, wait a bit
                            import time
                            time.sleep(0.5)
        except Exception as e:
            yield json.dumps({
                "log": f"Error reading log: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }) + "\n"
    
    def send_chat_message(self, message: str) -> Dict[str, Any]:
        """
        Stuur een chat bericht naar Ollama.
        
        Args:
            message: User message
            
        Returns:
            dict: Response met AI reply
        """
        if not self._guardian_loaded:
            return {
                "success": False,
                "error": "Guardian backend not loaded"
            }
        
        try:
            ollama_widget = self.widgets_instances.get("ollama_chat")
            
            if not ollama_widget:
                return {
                    "success": False,
                    "error": "Ollama chat widget not available"
                }
            
            if not self.widget_state.get("ollama_chat", False):
                return {
                    "success": False,
                    "error": "Ollama chat widget not active. Enable it first."
                }
            
            # Send message
            response = ollama_widget.send_message(message)
            
            return {
                "success": True,
                "response": response,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_chat_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Haal chat geschiedenis op.
        
        Args:
            limit: Maximum aantal berichten
            
        Returns:
            list: Chat history entries
        """
        history_file = "logs/chat_history.json"
        
        if not os.path.exists(history_file):
            return []
        
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                history = json.load(f)
                return history[-limit:] if len(history) > limit else history
        except Exception as e:
            print(f"Error loading chat history: {e}")
            return []
    
    def get_system_status(self) -> Dict[str, Any]:
        """Haal overall system status op."""
        if not self._guardian_loaded:
            return {
                "status": "disconnected",
                "message": "Guardian backend not loaded"
            }
        
        try:
            active_widgets = sum(1 for active in self.widget_state.values() if active)
            total_widgets = len(self.widget_state)
            
            status = {
                "status": "operational",
                "version": "1.0",
                "widgets": {
                    "active": active_widgets,
                    "total": total_widgets
                },
                "orchestrator": {
                    "active": False
                }
            }
            
            # Get orchestrator status
            if self.master_orch:
                if hasattr(self.master_orch, 'active'):
                    status["orchestrator"]["active"] = self.master_orch.active
                
                if hasattr(self.master_orch, 'orchb'):
                    if hasattr(self.master_orch.orchb, 'permission_level'):
                        status["permission_level"] = self.master_orch.orchb.permission_level.value
            
            return status
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def get_permission_level(self) -> Dict[str, Any]:
        """Haal huidige permission level op."""
        if not self._guardian_loaded or not self.master_orch:
            return {
                "permission_level": "observe",
                "available_levels": [p.value for p in PermissionLevel]
            }
        
        try:
            if hasattr(self.master_orch, 'orchb'):
                level = self.master_orch.orchb.permission_level.value
            else:
                level = "observe"
            
            return {
                "permission_level": level,
                "available_levels": [p.value for p in PermissionLevel]
            }
        except Exception as e:
            return {
                "permission_level": "observe",
                "error": str(e)
            }
    
    def set_permission_level(self, level: str) -> Dict[str, Any]:
        """
        Update permission level.
        
        Args:
            level: Permission level string (observe, alert, analyze, isolate, auto_respond)
            
        Returns:
            dict: Result
        """
        if not self._guardian_loaded or not self.master_orch:
            return {
                "success": False,
                "error": "Guardian backend not loaded"
            }
        
        try:
            # Convert string to PermissionLevel enum
            try:
                perm_level = PermissionLevel(level.lower())
            except ValueError:
                return {
                    "success": False,
                    "error": f"Invalid permission level: {level}"
                }
            
            # Set permission
            if hasattr(self.master_orch, 'set_user_permission'):
                self.master_orch.set_user_permission(perm_level)
            elif hasattr(self.master_orch, 'orchb'):
                self.master_orch.orchb.set_permission_level(perm_level)
            else:
                return {
                    "success": False,
                    "error": "Permission system not available"
                }
            
            return {
                "success": True,
                "permission_level": level.lower()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


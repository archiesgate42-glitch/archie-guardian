"""
ollama_chat.py
Ollama Chat Widget for Archie Guardian
Interactive AI chat interface for security analysis with persistent history
"""

import json
import os
from datetime import datetime
from core.ollama_connector import OllamaConnector


class OllamaChatWidget:
    """Interactive Ollama chat widget with persistent history."""
    
    HISTORY_FILE = "logs/chat_history.json"
    MAX_HISTORY = 50
    
    def __init__(self):
        """Initialize Ollama chat widget with persistent history."""
        self.name = "ollama_chat"
        self.active = False
        self.connector = None
        self.chat_history = []
        self.system_context = self._build_system_context()
        
        # Ensure logs directory exists
        os.makedirs("logs", exist_ok=True)
        
        # Load previous chat history
        self.load_history()
    
    def _build_system_context(self) -> str:
        """Build system context for Ollama."""
        return """You are Ollama, the AI assistant for Archie Guardian.

Archie Guardian is a local AI-driven host-based security monitoring system featuring:
- 6 widgets: File Integrity, Process Monitor, Network Sniffer, Windows Defender, RRNC, Chat
- Multi-agent AI orchestration: OrchA (threat analysis) + OrchB (human-AI bridge)
- Local Llama3 LLM inference via Ollama (100% local, no cloud)
- Interactive CLI with real-time security event analysis
- Granular permission system: Observe → Alert → Analyze → Isolate → Auto-Respond

Your role:
- Explain security events and threats in clear language
- Analyze logs and suggest responses
- Help users understand their system behavior
- Provide security best practices

Stay focused on security context. Be concise and actionable."""
    
    def load_history(self):
        """Load previous chat history from persistent storage."""
        try:
            if os.path.exists(self.HISTORY_FILE):
                with open(self.HISTORY_FILE, "r") as f:
                    self.chat_history = json.load(f)
                    print(f"   📂 Loaded {len(self.chat_history)} previous chat messages")
            else:
                self.chat_history = []
        except Exception as e:
            print(f"   ⚠️  Could not load chat history: {e}")
            self.chat_history = []
    
    def save_history(self):
        """Persist chat history to disk."""
        try:
            # Trim to MAX_HISTORY before saving
            history_to_save = self.chat_history[-self.MAX_HISTORY:]
            
            with open(self.HISTORY_FILE, "w") as f:
                json.dump(history_to_save, f, indent=2)
        except Exception as e:
            print(f"   ⚠️  Could not save chat history: {e}")
    
    def start(self) -> bool:
        """Start the Ollama chat widget."""
        try:
            self.connector = OllamaConnector(
                model="Llama3:latest",
                timeout=180
            )
            
            if self.connector.is_connected:
                self.active = True
                print(f"   🟢 Ollama Chat Widget: {self.connector.model} ready")
                print(f"   💬 Chat history: {len(self.chat_history)} messages loaded")
                return True
            else:
                print("   ❌ Ollama Chat Widget: Failed to connect")
                return False
                
        except Exception as e:
            print(f"   ❌ Ollama Chat Widget: {e}")
            return False
    
    def stop(self):
        """Stop the Ollama chat widget and save history."""
        self.active = False
        self.save_history()
    
    def send_message(self, user_input: str) -> str:
        """
        Send a message to Ollama and get response.
        
        Args:
            user_input: User's prompt/question
        
        Returns:
            str: Model response
        """
        if not self.active or not self.connector:
            return "❌ Ollama chat not active. Enable it first."
        
        try:
            response = self.connector.chat(user_input)
            
            # Store in history
            message_entry = {
                "timestamp": datetime.now().isoformat(),
                "user": user_input,
                "assistant": response
            }
            self.chat_history.append(message_entry)
            
            # Keep history under limit
            if len(self.chat_history) > self.MAX_HISTORY:
                self.chat_history.pop(0)
            
            # Save to persistent storage
            self.save_history()
            
            return response
            
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def analyze_event(self, event_dict: dict) -> str:
        """Analyze a security event using Ollama."""
        if not self.active or not self.connector:
            return "❌ Ollama not active"
        
        try:
            result = self.connector.analyze_security_event(event_dict)
            return result.get("analysis", "No analysis available")
        except Exception as e:
            return f"❌ Analysis error: {str(e)}"
    
    def get_status(self) -> dict:
        """Get widget status."""
        return {
            "active": self.active,
            "model": self.connector.model if self.connector else "N/A",
            "chat_history_size": len(self.chat_history),
            "connected": self.connector.is_connected if self.connector else False,
            "history_file": self.HISTORY_FILE
        }
    
    def get_chat_history(self, limit: int = 10) -> list:
        """
        Get recent chat history.
        
        Args:
            limit: Number of recent messages to return
        
        Returns:
            list: Recent chat messages
        """
        return self.chat_history[-limit:] if self.chat_history else []
    
    def clear_history(self) -> str:
        """Clear all chat history from memory and disk."""
        try:
            self.chat_history = []
            
            # Also delete the history file
            if os.path.exists(self.HISTORY_FILE):
                os.remove(self.HISTORY_FILE)
            
            return "✅ Chat history cleared"
        except Exception as e:
            return f"❌ Error clearing history: {str(e)}"
    
    def export_history(self, filename: str = None) -> str:
        """
        Export chat history to a file.
        
        Args:
            filename: Optional custom filename (default: chat_export_[timestamp].json)
        
        Returns:
            str: Export status message
        """
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"logs/chat_export_{timestamp}.json"
            
            os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
            
            with open(filename, "w") as f:
                json.dump(self.chat_history, f, indent=2)
            
            return f"✅ Chat history exported to {filename}"
        except Exception as e:
            return f"❌ Export error: {str(e)}"
    
    def get_actions(self) -> dict:
        """Get available widget actions."""
        return {
            "actions": [
                "send_message",
                "analyze_event",
                "clear_history",
                "export_history",
                "get_chat_history"
            ]
        }
    
    def get_recent_events(self, limit: int = 20) -> list:
        """Get recent chat messages as events."""
        recent = self.get_chat_history(limit)
        
        # Format as events for display
        events = []
        for msg in recent:
            events.append({
                "timestamp": datetime.fromisoformat(msg["timestamp"]).timestamp(),
                "user": msg["user"][:50] + "..." if len(msg["user"]) > 50 else msg["user"],
                "type": "chat_message"
            })
        
        return events
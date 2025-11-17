"""
ollama_chat.py
Ollama Chat Widget for Archie Guardian
Interactive AI chat interface for security analysis
"""

import threading
import json
from datetime import datetime
from core.ollama_connector import OllamaConnector


class OllamaChatWidget:
    """Interactive Ollama chat widget for Archie Guardian."""
    
    def __init__(self):
        """Initialize Ollama chat widget."""
        self.name = "ollama_chat"
        self.active = False
        self.connector = None
        self.chat_history = []
        self.max_history = 50
    
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
                return True
            else:
                print("   ❌ Ollama Chat Widget: Failed to connect")
                return False
                
        except Exception as e:
            print(f"   ❌ Ollama Chat Widget: {e}")
            return False
    
    def stop(self):
        """Stop the Ollama chat widget."""
        self.active = False
    
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
            self.chat_history.append({
                "timestamp": datetime.now().isoformat(),
                "user": user_input,
                "assistant": response
            })
            
            # Keep history under limit
            if len(self.chat_history) > self.max_history:
                self.chat_history.pop(0)
            
            return response
            
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def analyze_event(self, event_dict: dict) -> str:
        """Analyze a security event using Ollama."""
        if not self.active or not self.connector:
            return "❌ Ollama not active"
        
        result = self.connector.analyze_security_event(event_dict)
        return result.get("analysis", "No analysis available")
    
    def get_status(self) -> dict:
        """Get widget status."""
        return {
            "active": self.active,
            "model": self.connector.model if self.connector else "N/A",
            "chat_history_size": len(self.chat_history),
            "connected": self.connector.is_connected if self.connector else False
        }
    
    def get_chat_history(self, limit: int = 10) -> list:
        """Get recent chat history."""
        return self.chat_history[-limit:] if self.chat_history else []
    
    def clear_history(self):
        """Clear chat history."""
        self.chat_history = []
        return "✅ Chat history cleared"
    
    def get_actions(self) -> dict:
        """Get available widget actions."""
        return {
            "actions": [
                "send_message",
                "analyze_event",
                "clear_history",
                "get_chat_history"
            ]
        }
    
    def get_recent_events(self, limit: int = 20) -> list:
        """Get recent chat messages."""
        return self.get_chat_history(limit)

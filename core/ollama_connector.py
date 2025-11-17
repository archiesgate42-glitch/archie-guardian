"""
ollama_connector.py
Ollama API connector for Archie Guardian
Handles communication with local Ollama instance (Llama 3)
"""

import requests
import json
from typing import Optional, Dict, Any
from requests.exceptions import RequestException, Timeout


class OllamaConnector:
    """Connector for Ollama local LLM API."""
    
    DEFAULT_BASE_URL = "http://localhost:11434"
    DEFAULT_TIMEOUT = 120
    DEFAULT_MODEL = "llama3"
    
    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        model: str = DEFAULT_MODEL,
        timeout: int = DEFAULT_TIMEOUT
    ):
        """Initialize Ollama connector."""
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        self.is_connected = False
        self.check_connection()
    
    def check_connection(self) -> bool:
        """
        Check if Ollama server is reachable and model is available.
        
        Returns:
            bool: True if connected and model exists
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            
            if response.status_code != 200:
                self.is_connected = False
                return False
            
            models = response.json().get("models", [])
            model_exists = any(
                self.model.lower() in m.get("name", "").lower()
                for m in models
            )
            
            self.is_connected = model_exists
            return model_exists
            
        except RequestException:
            self.is_connected = False
            return False
    
    def chat(self, prompt: str, stream: bool = False) -> str:
        """
        Send a prompt to Ollama and get response.
        
        Args:
            prompt: The prompt/question to send
            stream: Whether to stream response (default: False)
        
        Returns:
            str: Model response or error message
        """
        if not self.is_connected:
            return "❌ Ollama not connected. Run 'ollama serve' first."
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": stream,
                    "options": {
                        "num_thread": 16,
                        "num_gpu": 0,
                        "temperature": 0.3,
                    }
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json().get("response", "No response returned")
            
            return f"❌ Error {response.status_code}: {response.text}"
            
        except Timeout:
            return "⏱️ Request timed out. Model might be slow or overloaded."
        except RequestException as e:
            return f"❌ Connection error: {str(e)}"
    
    def analyze_security_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a security event using Ollama.
        
        Args:
            event: Security event dict (e.g. from widgets)
        
        Returns:
            dict: Analysis result
        """
        prompt = self._build_security_prompt(event)
        analysis = self.chat(prompt)
        
        return {
            "analysis": analysis,
            "event": event,
            "model": self.model
        }
    
    def _build_security_prompt(self, event: Dict[str, Any]) -> str:
        """Build security analysis prompt from event data."""
        event_type = event.get("type", "unknown")
        details = json.dumps(event, indent=2)
        
        return f"""You are a cybersecurity analyst for Archie Guardian, a host-based security monitoring system.

Analyze this security event:

Event Type: {event_type}
Details:
{details}

Provide:
1. Threat assessment (Low/Medium/High/Critical)
2. Brief explanation
3. Recommended action

Be concise and actionable."""
    
    def get_status(self) -> Dict[str, Any]:
        """Get connector status information."""
        return {
            "connected": self.is_connected,
            "model": self.model,
            "base_url": self.base_url,
            "timeout": self.timeout
        }
    
    def list_models(self) -> list[str]:
        """List available Ollama models."""
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            if response.status_code == 200:
                return [m.get("name") for m in response.json().get("models", [])]
        except RequestException:
            pass
        return []
    
    def switch_model(self, model_name: str) -> bool:
        """
        Switch to a different model.
        
        Args:
            model_name: Name of model to switch to
        
        Returns:
            bool: True if successful
        """
        old_model = self.model
        self.model = model_name
        
        if self.check_connection():
            print(f"✅ Switched to model: {model_name}")
            return True
        
        self.model = old_model
        print(f"❌ Model '{model_name}' not available")
        return False

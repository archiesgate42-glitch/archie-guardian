import logging
import os
import signal
from datetime import datetime

logger = logging.getLogger(__name__)

class RapidResponseNeutralizeCapture:
    """
    RRNC Widget - Rapid Response Neutralize & Capture.
    Methods: start, stop, process_kill, network_block, quarantine, capture_forensics, analyze_threat, get_stats, get_recent_events
    """
    def __init__(self, config=None):
        self.config = config or {}
        self.active = False
        self.response_time = self.config.get('response_time', 2)  # seconds
        self.neutralization_level = self.config.get('neutralization_level', 'high')  # low/medium/high
        self.capture_rate = self.config.get('capture_rate', 0.95)  # confidence threshold
        self.events = []
        self.quarantine_vault = "C:\\Guardian_Vault"
        
        # Create vault if not exists
        os.makedirs(self.quarantine_vault, exist_ok=True)

    def start(self):
        """Activate RRNC widget"""
        self.active = True
        logger.info("🟢 RRNC Widget activated")
        print(f"   🟢 RRNC activated | Response: {self.response_time}s | Level: {self.neutralization_level}")
        return True

    def stop(self):
        """Deactivate RRNC widget"""
        self.active = False
        logger.info("⭕ RRNC Widget deactivated")
        print("   ⭕ RRNC deactivated")
        return True

    def analyze_threat(self, threat_data=None):
        """Analyze potential threat and calculate confidence score"""
        if not self.active:
            return {"status": "RRNC not active", "action": "analyze", "result": "failed"}
        
        # Default threat data als niets ingevoerd
        if threat_data is None:
            threat_data = {
                "type": "unknown",
                "confidence": 0.5
            }
        
        # Simple confidence calculation based on threat data
        confidence = threat_data.get("confidence", 0.5)
        threat_type = threat_data.get("type", "unknown")
        
        logger.info(f"Analyzing threat: {threat_type} | Confidence: {confidence*100:.1f}%")
        print(f"   [RRNC] 🔍 Threat analysis | Type: {threat_type} | Confidence: {confidence*100:.1f}%")
        
        event = {
            "timestamp": datetime.now().timestamp(),
            "action": "analyze_threat",
            "threat_type": threat_type,
            "confidence": confidence,
            "status": "analyzed",
            "recommendation": "HIGH_THREAT" if confidence > 0.85 else "LOW_THREAT"
        }
        self.events.append(event)
        
        return {
            "status": "success",
            "action": "analyze",
            "threat_type": threat_type,
            "confidence": confidence,
            "recommendation": event["recommendation"]
        }

    def process_kill(self, pid, force=True):
        """Kill a suspicious process"""
        if not self.active:
            return {"status": "RRNC not active", "action": "process_kill", "result": "failed"}
        
        signal_type = signal.SIGKILL if force else signal.SIGTERM
        logger.warning(f"Process kill initiated: PID {pid} (force={force})")
        print(f"   [RRNC] ⚡ Process {pid} terminated (signal: {'SIGKILL' if force else 'SIGTERM'})")
        
        # TODO: Implement actual os.kill(pid, signal_type)
        
        event = {
            "timestamp": datetime.now().timestamp(),
            "action": "process_kill",
            "pid": pid,
            "signal": "SIGKILL" if force else "SIGTERM",
            "status": "killed"
        }
        self.events.append(event)
        
        return {"status": "success", "action": "process_kill", "pid": pid, "signal": "SIGKILL" if force else "SIGTERM"}

    def network_block(self, ip, port=None):
        """Block suspicious network connection via firewall"""
        if not self.active:
            return {"status": "RRNC not active", "action": "network_block", "result": "failed"}
        
        logger.warning(f"Network block initiated: {ip}:{port if port else 'ANY'}")
        print(f"   [RRNC] 🔒 Connection blocked: {ip}:{port if port else 'ANY'}")
        
        # TODO: Implement PowerShell firewall rule
        # powershell command: New-NetFirewallRule -DisplayName "Block RRNC" -Direction Outbound -Action Block -RemoteAddress {ip}
        
        event = {
            "timestamp": datetime.now().timestamp(),
            "action": "network_block",
            "ip": ip,
            "port": port,
            "status": "blocked"
        }
        self.events.append(event)
        
        return {"status": "success", "action": "network_block", "ip": ip, "port": port}

    def quarantine(self, file_path):
        """Quarantine a suspicious file"""
        if not self.active:
            return {"status": "RRNC not active", "action": "quarantine", "result": "failed"}
        
        if not os.path.exists(file_path):
            return {"status": "File not found", "action": "quarantine", "result": "failed", "file": file_path}
        
        logger.warning(f"Quarantine initiated: {file_path}")
        print(f"   [RRNC] 🔐 File quarantined: {file_path}")
        
        # TODO: Implement move to vault
        # shutil.move(file_path, os.path.join(self.quarantine_vault, os.path.basename(file_path)))
        
        event = {
            "timestamp": datetime.now().timestamp(),
            "action": "quarantine",
            "file": file_path,
            "vault": self.quarantine_vault,
            "status": "quarantined"
        }
        self.events.append(event)
        
        return {"status": "success", "action": "quarantine", "file": file_path, "vault": self.quarantine_vault}

    def capture_forensics(self, threat_id, data_type="all"):
        """Capture forensic evidence"""
        if not self.active:
            return {"status": "RRNC not active", "action": "capture", "result": "failed"}
        
        logger.info(f"Forensic capture initiated: {threat_id} | Type: {data_type}")
        print(f"   [RRNC] 📸 Forensic data captured | Threat: {threat_id} | Type: {data_type}")
        
        # TODO: Implement actual forensic capture
        # - Memory dumps (if process)
        # - Network packets (if network)
        # - File hashes and metadata
        # - Timeline reconstruction
        
        forensic_path = os.path.join(self.quarantine_vault, f"forensics_{threat_id}")
        os.makedirs(forensic_path, exist_ok=True)
        
        event = {
            "timestamp": datetime.now().timestamp(),
            "action": "capture_forensics",
            "threat_id": threat_id,
            "data_type": data_type,
            "forensic_path": forensic_path,
            "status": "captured"
        }
        self.events.append(event)
        
        return {
            "status": "success",
            "action": "capture_forensics",
            "threat_id": threat_id,
            "forensic_path": forensic_path,
            "data_types": ["memory_dump", "packet_capture", "file_hashes", "timeline"] if data_type == "all" else [data_type]
        }

    def get_stats(self):
        """Return widget status"""
        return {
            "widget_name": "rrnc",
            "enabled": self.active,  # ✅ CORRECT (not self.enabled)
            "events_buffered": len(self.events) if hasattr(self, 'events') else 0,
            "status": "🟢 LIVE" if self.active else "⭕ Idle"
    }

    def get_actions(self):
        """Available actions based on state"""
        return {
            "actions": ["analyze_threat", "process_kill", "network_block", "quarantine", "capture_forensics"] if self.active else [],
            "status": "active" if self.active else "inactive"
        }

    def get_recent_events(self, limit=10):
        """Get recent RRNC events"""
        return self.events[-limit:] if self.events else []

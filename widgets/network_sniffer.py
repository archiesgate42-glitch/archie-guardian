import psutil
import time
from threading import Thread

class NetworkSnifferWidget:
    """
    Safe network sniffer: monitort actieve netwerk sockets/processen (geen root nodig).
    """
    def __init__(self, config=None):
        self.config = config or {}
        self.active = False
        self.events = []
        self.max_events = 50
        self.thread = None
        self._previous = set()

    def start(self):
        self.active = True
        self.thread = Thread(target=self._watch, daemon=True)
        self.thread.start()
        print("   🟢 Network Sniffer Widget started (no root needed)")
        return True

    def stop(self):
        self.active = False
        if self.thread:
            self.thread.join(timeout=2)
        print("   ⭕ Network Sniffer Widget stopped")
        return True

    def _watch(self):
        while self.active:
            active_conns = set()
            for proc in psutil.process_iter(['pid','name']):
                try:
                    for conn in proc.connections(kind='inet'):
                        if conn.status == psutil.CONN_ESTABLISHED:
                            key = (proc.info['pid'], conn.raddr, conn.laddr)
                            if key not in self._previous:
                                event = {
                                    "timestamp": time.time(),
                                    "pid": proc.info['pid'],
                                    "process": proc.info['name'],
                                    "local_address": f"{conn.laddr.ip}:{conn.laddr.port}",
                                    "remote_address": f"{conn.raddr.ip}:{conn.raddr.port}",
                                }
                                self.events.append(event)
                                if len(self.events) > self.max_events:
                                    self.events = self.events[-self.max_events:]
                            active_conns.add(key)
                except Exception:
                    continue
            self._previous = active_conns
            time.sleep(1.5)

    def get_recent_events(self, count=10):
        return self.events[-count:] if self.events else []

    def get_stats(self):
     """Return widget status"""
     return {
        "widget_name": "network_sniffer",
        "enabled": self.active,  # ✅ CORRECT (not self.enabled)
        "events_buffered": len(self.events) if hasattr(self, 'events') else 0,
        "status": "🟢 LIVE" if self.active else "⭕ Idle"
    }

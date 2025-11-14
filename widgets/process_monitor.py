import psutil
import time
from threading import Thread

class ProcessMonitorWidget:
    """
    Live process monitor widget. Detects new process spawns.
    """
    def __init__(self, config=None):
        self.config = config or {}
        self.active = False
        self.events = []
        self.max_events = 50
        self._prev_pids = set()
        self.thread = None

    def start(self):
        self.active = True
        self._prev_pids = set(psutil.pids())
        self.thread = Thread(target=self._watch, daemon=True)
        self.thread.start()
        print("   🟢 Process Monitor Widget started")
        return True

    def stop(self):
        self.active = False
        if self.thread:
            self.thread.join(timeout=2)
        print("   ⭕ Process Monitor Widget stopped")
        return True

    def _watch(self):
        while self.active:
            current_pids = set(psutil.pids())
            new_pids = current_pids - self._prev_pids
            for pid in new_pids:
                try:
                    p = psutil.Process(pid)
                    event = {
                        "timestamp": time.time(),
                        "pid": pid,
                        "name": p.name(),
                        "cmdline": " ".join(p.cmdline() or []),
                        "user": p.username()
                    }
                    self.events.append(event)
                    if len(self.events) > self.max_events:
                        self.events = self.events[-self.max_events:]
                except Exception:
                    continue
            self._prev_pids = current_pids
            time.sleep(1)

    def get_recent_events(self, count=10):
        return self.events[-count:] if self.events else []

    def get_stats(self):
        return {
            "widget_name": "process_monitor",
            "enabled": self.active,
            "events_buffered": len(self.events),
            "status": "🟢 LIVE" if self.active else "⭕ Idle"
        }

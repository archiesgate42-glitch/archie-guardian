"""
core/orchestrator.py
Master Orchestrator: Coordinates Widgets, OrchA, OrchB, and Dispatcher.
The central nervous system of Archie Guardian v1.0+
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import threading
import time

from .agent_utils import AuditLogger, Event, PermissionLevel, ThreatLevel, EventQueue
from .orch_a import OrchA
from .orch_b import OrchB


class MasterOrchestrator:
    """
    Central orchestrator that:
    1. Consumes events from widgets
    2. Analyzes threats (OrchA)
    3. Escalates to human (OrchB)
    4. Executes dispatcher actions
    5. Tracks feedback for learning
    """
    
    def __init__(self, audit_logger: AuditLogger, dispatcher=None, config: Dict[str, Any] = None):
        self.audit_logger = audit_logger
        self.dispatcher = dispatcher  # Widget action executor
        self.config = config or {}
        
        # Initialize sub-orchestrators
        self.orcha = OrchA(audit_logger, config.get("orcha_config", {}))
        self.orchb = OrchB(audit_logger, config.get("orchb_config", {}))
        
        # Event management
        self.event_queue = EventQueue()
        self.processed_events = []
        self.decisions_made = []
        
        # Thread management (for event processing)
        self.active = False
        self.processing_thread = None
        self.lock = threading.Lock()
        
        self.logger_name = "MasterOrch"
    
    def start(self):
        """Start the master orchestrator."""
        if self.active:
            return
        
        self.active = True
        self.orcha.start()
        self.orchb.start()
        
        # Start event processing thread
        self.processing_thread = threading.Thread(target=self._process_events_loop, daemon=True)
        self.processing_thread.start()
        
        print(f"   ✓ {self.logger_name} activated")
        self.audit_logger.log_decision(
            agent=self.logger_name,
            decision="orchestrator_start",
            details={"timestamp": datetime.now().isoformat()}
        )
    
    def stop(self):
        """Stop the master orchestrator."""
        if not self.active:
            return
        
        self.active = False
        self.orcha.stop()
        self.orchb.stop()
        
        # Wait for processing thread
        if self.processing_thread:
            self.processing_thread.join(timeout=5)
        
        print(f"   ✓ {self.logger_name} deactivated")
        self.audit_logger.log_decision(
            agent=self.logger_name,
            decision="orchestrator_stop",
            details={"timestamp": datetime.now().isoformat()}
        )
    
    def ingest_widget_event(self, event: Event):
        """
        Accept event from widget (file_integrity, process_monitor, etc).
        """
        with self.lock:
            self.event_queue.push(event)
            
            self.audit_logger.log_decision(
                agent=self.logger_name,
                decision="ingest_event",
                details={
                    "event_id": event.event_id,
                    "source": event.source,
                    "event_type": event.event_type,
                    "timestamp": datetime.now().isoformat()
                }
            )
    
    def _process_events_loop(self):
        """
        Main event processing loop (runs in background thread).
        Continuously processes unprocessed events.
        """
        while self.active:
            try:
                # Get next unprocessed event
                event = self.event_queue.pop()
                if event:
                    self._handle_event(event)
                else:
                    time.sleep(0.1)  # Avoid busy-waiting
            except Exception as e:
                self.audit_logger.log_alert(
                    alert_id=f"orch_error_{int(time.time())}",
                    level=ThreatLevel.LOW,
                    message=f"Error in event processing: {e}",
                    context={}
                )
                time.sleep(1)
    
    def _handle_event(self, event: Event):
        """
        Handle single event through full pipeline:
        Widget Event → OrchA Analysis → OrchB Escalation → Dispatcher Execution
        """
        
        print(f"\n🔄 Processing event: {event.event_id} from {event.source}")
        
        # Step 1: OrchA analyzes threat
        analysis = self.orcha.analyze_event(event)
        threat_level = ThreatLevel[analysis["threat_level"].upper()]
        
        print(f"   📊 OrchA analysis: {threat_level.value} threat ({analysis['confidence_score']}%)")
        
        # Step 2: OrchA generates decision
        orcha_decisions = self.orcha.process_events()
        if not orcha_decisions:
            # No threat detected, log and continue
            event.processed = True
            self.processed_events.append({
                "event_id": event.event_id,
                "status": "no_threat",
                "analysis": analysis
            })
            return
        
        decision = orcha_decisions[0]  # Get first decision
        print(f"   💡 Recommendation: {decision.action}")
        
        # Step 3: Check if needs human escalation
        needs_escalation = self.orchb.evaluate_escalation(decision, threat_level)
        
        if needs_escalation:
            # Step 4: Escalate to user for approval
            print(f"   ⚠️  Escalating to user...")
            approved = self.orchb.escalate_to_user(decision, threat_level, analysis)
            
            if not approved:
                # User denied action
                event.processed = True
                self.processed_events.append({
                    "event_id": event.event_id,
                    "status": "user_denied",
                    "decision": decision.to_dict()
                })
                return
        else:
            print(f"   ✅ Auto-approved (permission level: {self.orchb.permission_level.value})")
        
        # Step 5: Execute action via dispatcher
        if self.dispatcher:
            action_result = self._execute_action(decision, event, analysis)
            
            if action_result["status"] == "success":
                print(f"   ✅ Action executed: {decision.action}")
        else:
            print(f"   ⚠️  No dispatcher available (action would be: {decision.action})")
        
        # Step 6: Request user feedback (for learning)
        feedback = self.orchb.get_user_feedback(event.event_id, analysis["confidence_score"])
        if feedback:
            self.orcha.learn_from_feedback(event.event_id, feedback)
        
        # Mark event as processed
        event.processed = True
        self.processed_events.append({
            "event_id": event.event_id,
            "status": "completed",
            "decision": decision.to_dict(),
            "feedback": feedback
        })
        
        self.decisions_made.append(decision)
    
    def _execute_action(self, decision, event: Event, analysis: Dict) -> Dict[str, Any]:
        """
        Execute action via dispatcher.
        Maps OrchA decisions to widget actions.
        """
        
        action_map = {
            "quarantine": {
                "file_integrity": "quarantine",
                "process_monitor": "kill_process",
                "network_sniffer": "block_ip"
            },
            "alert": {
                "all": "log_alert"
            },
            "escalate": {
                "all": "escalate_to_security"
            }
        }
        
        widget_action = action_map.get(decision.action, {}).get(event.source, "log_only")
        
        try:
            # Call dispatcher action
            result = self.dispatcher.execute_action(
                widget=event.source,
                action=widget_action,
                **event.payload
            ) if self.dispatcher else {"status": "no_dispatcher"}
            
            self.audit_logger.log_action_executed(
                widget=event.source,
                action=widget_action,
                result=result
            )
            
            return result
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def get_orchestrator_stats(self) -> Dict[str, Any]:
        """Get comprehensive orchestrator statistics."""
        return {
            "master_status": "active" if self.active else "inactive",
            "events_ingested": len(self.event_queue.queue),
            "events_processed": len(self.processed_events),
            "decisions_made": len(self.decisions_made),
            "orcha_stats": self.orcha.get_stats(),
            "orchb_stats": self.orchb.get_stats(),
            "orchb_approvals": self.orchb.get_approval_stats(),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_recent_decisions(self, limit: int = 10) -> List[Dict]:
        """Get recent orchestrator decisions."""
        return [
            {
                "event_id": d["event_id"],
                "status": d["status"],
                "decision": d.get("decision"),
                "feedback": d.get("feedback")
            }
            for d in self.processed_events[-limit:]
        ]
    
    def set_user_permission(self, level: PermissionLevel):
        """Update user permission level globally."""
        self.orchb.set_permission_level(level)
        print(f"   ✓ User permission updated: {level.value}")

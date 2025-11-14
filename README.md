Archie Guardian
Local. Transparent. AI-Driven Security.

Real-time system monitoring with File Integrity, Process Monitor, and Network Sniffer widgets. Powered by multi-agent AI orchestration (CrewAI) + local LLM inference (Ollama).

status
python
license
stars

🚀 Quick Start
bash
# Clone & setup
git clone https://github.com/archiesgate42-glitch/archie-guardian.git
cd archie-guardian
pip install -r requirements.txt

# Start Guardian
python guardian.py

# Output
============================================================
✨ ARCHIE GUARDIAN v0.3 - Local AI Security
============================================================

[1/6] Checking core modules...
   ✅ Core imports successful
[2/6] Checking widget system...
   ✅ File Integrity Widget loaded (LIVE)
   ✅ Process Monitor Widget loaded (LIVE)
   ✅ Network Sniffer Widget loaded (LIVE)
...
✨ Features
🎯 MVP (v0.3) - All 3 Widgets Live
Widget	Status	What It Does
File Integrity	✅ LIVE	Monitor file changes in real-time (~/Projects, ~/Downloads, ~/Documents)
Process Monitor	✅ LIVE	Detect new process spawns, track PIDs, user context
Network Sniffer	✅ LIVE	Log established connections, process-to-IP mapping (no root needed!)
🧠 AI-Driven Analysis
OrchA (AI Task Master): Analyzes events, assigns threat levels, learns from feedback

OrchB (Human-Facing): Permission management, user interaction, audit logging

Tech-Human Translator: Converts technical findings → plain English alerts

🔒 Privacy & Control
✅ Local-first: Runs entirely on your machine (no cloud)

✅ Transparent: Every decision logged & explainable

✅ Granular Permissions: Observe → Alert → Analyze → Isolate → Auto-Respond

✅ Audit Trail: Complete history of all actions

📋 CLI Commands
text
guardian status              # Show system status & widget states
guardian enable <widget>     # Start monitoring (with permission check)
guardian disable <widget>    # Stop monitoring
guardian events              # View live widget events
guardian logs                # See audit trail
guardian help                # Full help
guardian quit                # Exit
Example Session
text
guardian> enable file_integrity
   🟢 File Integrity Widget: Monitoring 2 paths
✅ Widget 'file_integrity' enabled (LIVE MONITORING)

guardian> enable process_monitor
   🟢 Process Monitor Widget started
✅ Widget 'process_monitor' enabled (LIVE MONITORING)

guardian> enable network_sniffer
   🟢 Network Sniffer Widget started (no root needed)
✅ Widget 'network_sniffer' enabled (LIVE MONITORING)

guardian> events
📡 LIVE WIDGET EVENTS
============================================================

🔍 PROCESS_MONITOR:
  [23:04:14] PID 16548 | comet.exe

🔍 NETWORK_SNIFFER:
  [23:04:18] comet.exe       -> 151.101.1.91:443
  [23:04:18] OneDrive.exe    -> 172.211.123.249:443
🏗️ Architecture
Four-Layer Design:

Sensor Layer — Widgets (File, Process, Network)

Orchestration Layer — OrchA + OrchB agents

Inference Layer — Ollama (local LLM)

CLI/Audit Layer — User interface + logging

text
┌─────────────────────────────────────────┐
│  User Interface (CLI + Real-time Events)│
├─────────────────────────────────────────┤
│ OrchA (AI Master) + OrchB (Human-Facing)│
├─────────────────────────────────────────┤
│       Ollama (Local LLM Inference)      │
├─────────────────────────────────────────┤
│ File Widget | Process Widget | Net Widget│
└─────────────────────────────────────────┘
Full technical paper: See ARCHITECTURE.md

📦 Requirements
Python 3.9+

psutil — Process monitoring

watchdog — File system events

Ollama (optional) — Local LLM inference

Install Dependencies
bash
pip install -r requirements.txt
Setup Ollama (optional but recommended)
bash
# Download Ollama from https://ollama.ai
ollama pull mistral
🔐 Permission Model
Define what Guardian is allowed to do:

Level	Capabilities	Use Case
Observe	Read-only monitoring	"Just watch my system"
Alert	Send notifications	"Alert me to suspicious activity"
Analyze	AI context analysis	"I want explanations"
Isolate	Quarantine processes (requires approval)	"Handle threats, ask me first"
Auto-Respond	Automatic mitigation	"I trust you to defend"
📊 Performance
Resource Profile (all widgets active):

Component	CPU	RAM	Notes
Core (OrchA+B)	2-5%	50-100 MB	Idle baseline
Ollama (inference)	20-30%	500MB-4GB	During analysis spikes
Widgets (all 3)	2-3%	60 MB	Extremely lightweight
Total	5-15%	600MB-4.2GB	Runs smoothly on any modern machine
🚦 Roadmap
v0.3 (NOW) ✅
✅ File Integrity Widget

✅ Process Monitor Widget

✅ Network Sniffer Widget

✅ OrchA + OrchB orchestration

✅ CLI interface

✅ Audit logging

v1 (Q1 2026) 🎯
Network Sniffer advanced features

Hot-reload widgets

Plugin system (beta)

Advanced CLI + TUI dashboard

Community feedback integration

v2+ (H2 2026) 🌟
Additional widgets (Resource Drain, Registry Watch, Crypto Detector)

Widget marketplace

Multi-machine telemetry (optional)

Fine-tuned LLM models for specific threat domains

Governance & community roadmap

🛡️ Threat Model
Guardian protects against:

File tampering (ransomware, accidental overwrites)

Suspicious process spawning

Unexpected network activity

Anomalous user behavior

Guardian does NOT protect against:

Kernel-level rootkits

Offline attacks

Cryptographic backdoors in system libraries

Philosophy: Guardian is complementary to traditional antivirus, not a replacement.

🤝 Contributing
We welcome contributions! Here's how:

Fork the repo

Create a branch (git checkout -b feature/my-widget)

Build your widget (see Widget Development Guide)

Test locally (python guardian.py)

Submit a PR with description + test results

Widget Template
python
class MyWidget:
    def sense(self) -> List[Event]:
        """Detect events."""
        pass
    
    def classify(self, event: Event) -> Classification:
        """Classify severity."""
        pass
    
    def report(self) -> Dict:
        """Return telemetry."""
        pass
Drop your widget in /widgets/ and Guardian auto-loads it!

📖 Documentation
Full Technical Paper — Deep dive into design, multi-agent orchestration, CrewAI patterns

CLI Reference — Complete command reference

Widget Development — Build your own sensors

Permission Model — Security & audit trails

⚖️ License
MIT License — See LICENSE for details.

TL;DR: You can use, modify, and distribute Archie Guardian freely, even commercially. Just give credit.

🙋 FAQ
Q: Why local instead of cloud?
A: Privacy, speed, control. Your data stays on your machine. Plus, no subscription fees!

Q: Can I use other LLMs?
A: v0.3 uses Ollama, but v1 will support LM Studio, Hugging Face, and custom models.

Q: Is this a replacement for antivirus?
A: No. Guardian does behavioral monitoring & anomaly detection. Use it alongside traditional antivirus.

Q: What's the learning curve?
A: Minimal. Run guardian status and you're done. Advanced tuning is optional.

Q: How do I report bugs?
A: Open an Issue on GitHub.

🎯 What's Next?
Star the repo ⭐ (helps us grow!)

Try v0.3 — Run python guardian.py and test the widgets

Share feedback — What would YOU monitor?

Contribute — Build a custom widget!

Spread the word — Tweet, blog, discuss!

📞 Community
GitHub: archiesgate42-glitch/archie-guardian

Issues: Report bugs or request features

Discussions: Share ideas & feedback

💡 Philosophy
Archie Guardian embodies three principles:

Transparency — You understand every decision the system makes

Autonomy — You control what Guardian can do

Community — Together we build the security tools we deserve

Made with ❤️ by Archie Gate
November 2025
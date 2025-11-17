# Archie Guardian

![Archie Guardian Logo](assets/logo.png)

> **Local. Transparent. AI-Driven Security.**

Real-time system monitoring with **File Integrity**, **Process Monitor**, **Network Sniffer** widgets + **Local AI Chat** powered by Ollama (Llama3).

---

## 🏗️ System Architecture

![Architecture Diagram](assets/architecture-diagram.png)

The system follows a **4-layer design**:

```
┌─────────────────────────────────────────────┐
│   User Interface (CLI + Interactive Chat)   │
├─────────────────────────────────────────────┤
│  OrchA (AI Master) + OrchB (Human-Facing)  │
├─────────────────────────────────────────────┤
│  Ollama (Local Llama3 LLM Inference) [NEW!] │
├─────────────────────────────────────────────┤
│  File | Process | Network | Ollama Widgets  │
└─────────────────────────────────────────────┘
```
![status](https://img.shields.io/badge/status-MVP%20v0.3-blue)
![python](https://img.shields.io/badge/python-3.9%2B-brightgreen)
![license](https://img.shields.io/badge/license-MIT-green)
![stars](https://img.shields.io/github/stars/archiesgate42-glitch/archie-guardian?style=flat)
---

## 🚀 Quick Start

```bash
# Clone & setup
git clone https://github.com/archiesgate42-glitch/archie-guardian.git
cd archie-guardian
python -m venv venv
.\venv\Scripts\Activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Install Ollama (optional but highly recommended for AI features)
# Download from: https://ollama.ai

# Start Guardian
python guardian.py

# Output
============================================================
✨ ARCHIE GUARDIAN v1.0 - Local AI Security + Multi-Agent
============================================================

[1/7] Checking core modules...
   ✅ Core imports successful
[2/7] Checking widget system...
   ✅ Widget system ready (6/6 widgets available)
   ✅ file_integrity loaded
   ✅ process_monitor loaded
   ✅ network_sniffer loaded
   ✅ windows_defender loaded
   ✅ rrnc loaded
   ✅ ollama_chat loaded
[3/7] Initializing audit logger...
   ✅ Audit logger initialized (logs/audit.log)
[4/7] Initializing widget instances...
   ✅ All widgets ready
[5/7] Initializing orchestrator system...
   ✅ Master Orchestrator ready (OrchA + OrchB)
[6/7] Verifying state management...
   ✅ State tracking initialized
[7/7] CLI interface ready...
   ✅ All systems operational
```

---

## ✨ Features

### 🎯 v1.0 - All 6 Widgets Live

| Widget | Status | What It Does |
|--------|--------|-------------|
| **File Integrity** | ✅ LIVE | Monitor file changes in real-time |
| **Process Monitor** | ✅ LIVE | Detect new process spawns, track PIDs, user context |
| **Network Sniffer** | ✅ LIVE | Log established connections, process-to-IP mapping (no root needed!) |
| **Windows Defender** | ✅ LIVE | Integration with Windows security scans |
| **RRNC** | ✅ LIVE | Rapid Response Neutralize & Capture for threat mitigation |
| **Ollama Chat** | ✅ NEW | Local AI (Llama3) for security analysis & interactive chat |

### 🧠 AI-Driven Analysis

- **OrchA (AI Task Master):** Analyzes events, assigns threat levels, learns from feedback
- **OrchB (Human-Facing):** Permission management, user interaction, audit logging
- **Ollama Integration:** Local LLM inference for security event analysis (no cloud!)
- **Tech-Human Translator:** Converts technical findings → plain English alerts

### 💬 New: Interactive Ollama Chat [v1.0]

Ask Guardian's AI questions directly:
- "Analyze this suspicious network activity"
- "What does this security event mean?"
- "Help me understand file integrity alerts"
- Real-time responses without leaving the CLI
- Full chat history maintained per session

### 🔒 Privacy & Control

- ✅ **Local-first:** Runs entirely on your machine (no cloud)
- ✅ **Transparent:** Every decision logged & explainable
- ✅ **Granular Permissions:** Observe → Alert → Analyze → Isolate → Auto-Respond
- ✅ **Audit Trail:** Complete history of all actions
- ✅ **Optional AI:** Enable/disable Ollama as a widget

---

## 📋 CLI Commands

```
 1. status      - Show system status & widget states
 2. enable      - Enable widget(s) [numbered]
 3. disable     - Disable widget(s) [numbered]
 4. action      - Execute widget action [numbered]
 5. events      - View live widget events
 6. logs        - View audit trail
 7. orch_stats  - Show orchestrator statistics
 8. set_perms   - Set user permission level
 9. help        - Show help
10. chat        - Interactive Ollama chat [NEW!]
 0. quit        - Exit Guardian
```

### Example Session

```
Enter command (0-9, 10): 2

🔋 ENABLE WIDGETS
==================================================
Available widgets:
  1. file_integrity       [⭕ Disabled]
  2. process_monitor      [⭕ Disabled]
  3. network_sniffer      [⭕ Disabled]
  4. windows_defender     [⭕ Disabled]
  5. rrnc                 [⭕ Disabled]
  6. ollama_chat          [⭕ Disabled]

Select widget(s) (e.g. 1,2,3 or 1-3 or just 1): 1-5
   🟢 File Integrity Widget: Monitoring 2 paths
✅ file_integrity enabled
   🟢 Process Monitor Widget started
✅ process_monitor enabled
   🟢 Network Sniffer Widget started
✅ network_sniffer enabled
   🟢 Windows Defender Widget activated
✅ windows_defender enabled
   🟢 RRNC activated
✅ rrnc enabled

✅ Enabled 5 widget(s)

Enter command (0-9, 10): 6
🟢 ollama_chat          [⭕ Disabled]

Select widget(s) (e.g. 1,2,3 or 1-3 or just 1): 6
   🟢 Ollama Chat Widget: Llama3:latest ready
✅ ollama_chat enabled

Enter command (0-9, 10): 10

💬 OLLAMA CHAT (type 'exit' or 'quit' to exit)
============================================================

🧑 You: What security threats should I be monitoring?

⏳ Thinking...

🤖 Ollama:
Based on your system monitoring setup with Guardian, here are the key security threats you should focus on:

1. **File Integrity Threats**
   - Ransomware attacks (encrypts your files)
   - Trojan backdoors (modify system files)
   - Configuration tampering

2. **Process-Level Threats**
   - Malware spawning hidden processes
   - Privilege escalation attempts
   - Memory injection attacks

3. **Network Security**
   - Unauthorized data exfiltration
   - C2 (Command & Control) communication
   - Suspicious external connections

Monitor these patterns and Guardian will help you respond quickly.

🧑 You: exit
✅ Chat ended
```

---

## 📦 Requirements

- **Python 3.9+**
- **psutil** — Process monitoring
- **watchdog** — File system events
- **requests** — HTTP for Ollama API
- **Ollama** (optional) — Local LLM inference (recommended for v1.0+)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Setup Ollama (Optional but Highly Recommended)

```bash
# 1. Download Ollama from https://ollama.ai
# 2. Install and start Ollama service
# 3. Pull Llama3 model
ollama pull llama3

# 4. Start Ollama server (runs in background)
ollama serve

# 5. Guardian will auto-connect when you enable ollama_chat widget
```

**Why Ollama?**
- Zero subscription fees
- All processing happens locally (your data stays private)
- Fast inference on CPU (optimized settings included)
- Easy model switching (Llama3, Mistral, Phi, etc.)

---

## 🔐 Permission Model

Define what Guardian is allowed to do:

| Level | Capabilities | Use Case |
|-------|-------------|----------|
| **Observe** | Read-only monitoring | "Just watch my system" |
| **Alert** | Send notifications | "Alert me to suspicious activity" |
| **Analyze** | AI context analysis | "I want explanations" |
| **Isolate** | Quarantine processes (requires approval) | "Handle threats, ask me first" |
| **Auto-Respond** | Automatic mitigation | "I trust you to defend" |

---

## 📊 Performance

**Resource Profile (all widgets active):**

| Component | CPU | RAM | Notes |
|-----------|-----|-----|-------|
| Core (OrchA+B) | 2-5% | 50-100 MB | Idle baseline |
| Ollama (inference) | 20-40% | 500MB-4GB | During chat/analysis |
| Widgets (all 5) | 2-3% | 80 MB | Lightweight monitoring |
| **Total** | **8-20%** | **700MB-4.2GB** | Smooth on modern machines |

**Tested on:** AMD Ryzen 7 7730U + 32GB RAM (smooth performance)

---

## 🚦 Roadmap

### v1.0 (NOW) ✅
- ✅ File Integrity Widget
- ✅ Process Monitor Widget
- ✅ Network Sniffer Widget
- ✅ Windows Defender Widget
- ✅ RRNC (Rapid Response) Widget
- ✅ Ollama Chat Widget [NEW!]
- ✅ OrchA + OrchB orchestration
- ✅ Interactive CLI
- ✅ Audit logging
- ✅ Multi-agent system

### v1.1 (Q1 2026) 🎯
- Chat history persistence
- CrewAI integration (enhanced orchestration)
- Hot-reload widgets
- Advanced threat patterns
- Community widget contributions

### v2.0 (H2 2026) 🌟
- TUI dashboard (terminal UI)
- Additional widgets (Resource Drain, Registry Watch, Crypto Detector)
- Widget marketplace
- Multi-machine telemetry (optional)
- Fine-tuned LLM models for security domains
- Governance & community roadmap

---

## 🛡️ Threat Model

**Guardian protects against:**
- File tampering (ransomware, accidental overwrites)
- Suspicious process spawning
- Unexpected network activity
- Anomalous user behavior

**Guardian does NOT protect against:**
- Kernel-level rootkits
- Offline attacks
- Cryptographic backdoors in system libraries

**Philosophy:** Guardian is *complementary* to traditional antivirus, not a replacement.

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork** the repo
2. **Create a branch** (`git checkout -b feature/my-widget`)
3. **Build your widget** (see [Widget Development Guide](./docs/WIDGETS.md))
4. **Test locally** (`python guardian.py`)
5. **Submit a PR** with description + test results

### Widget Template

```python
class MyWidget:
    def __init__(self):
        self.name = "my_widget"
        self.active = False
    
    def start(self) -> bool:
        """Initialize and start widget."""
        self.active = True
        return True
    
    def stop(self):
        """Cleanup and stop widget."""
        self.active = False
    
    def get_recent_events(self, limit: int = 20) -> list:
        """Return recent events."""
        return []
    
    def get_actions(self) -> dict:
        """Available actions."""
        return {"actions": []}
    
    def get_stats(self) -> dict:
        """Return widget statistics."""
        return {"status": "active"}
```

Drop your widget in `/widgets/` and Guardian auto-loads it!

---

## 📖 Documentation

- **[Architecture Deep Dive](./ARCHITECTURE.md)** — Design patterns, multi-agent orchestration, CrewAI
- **[CLI Reference](./docs/CLI.md)** — Complete command reference
- **[Widget Development](./docs/WIDGETS.md)** — Build custom sensors
- **[Permission Model](./docs/PERMISSIONS.md)** — Security & audit trails
- **[Ollama Integration](./docs/OLLAMA.md)** — Setup & customization

---

## ⚖️ License

MIT License — See [LICENSE](./LICENSE) for details.

**TL;DR:** You can use, modify, and distribute Archie Guardian freely, even commercially. Just give credit.

---

## 🙋 FAQ

**Q: Why local instead of cloud?**  
A: Privacy, speed, control. Your data stays on your machine. Plus, no subscription fees!

**Q: Can I use other LLMs?**  
A: v1.0 uses Ollama (Llama3), v1.1+ will support LM Studio, HuggingFace models, and custom endpoints.

**Q: Is this a replacement for antivirus?**  
A: No. Guardian does *behavioral monitoring & anomaly detection*. Use it alongside traditional antivirus.

**Q: What's the learning curve?**  
A: Minimal. Run `python guardian.py` → `2` → select widgets → `1` for status. Advanced tuning is optional.

**Q: Does Ollama run automatically?**  
A: Ollama runs as a service (Windows/Mac/Linux). Guardian auto-connects when you enable the ollama_chat widget.

**Q: How do I report bugs?**  
A: Open an [Issue](https://github.com/archiesgate42-glitch/archie-guardian/issues) on GitHub.

**Q: Can I contribute widgets?**  
A: Yes! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

---

## 🎯 What's Next?

1. **Star the repo** ⭐ (helps us grow!)
2. **Try v1.0** — Run `python guardian.py` and test the widgets
3. **Enable Ollama** — Ask the AI questions directly in CLI
4. **Share feedback** — What would YOU monitor?
5. **Contribute** — Build a custom widget!
6. **Spread the word** — Tweet, blog, discuss!

---

## 📞 Community

- **GitHub:** [archiesgate42-glitch/archie-guardian](https://github.com/archiesgate42-glitch/archie-guardian)
- **Issues:** [Report bugs or request features](https://github.com/archiesgate42-glitch/archie-guardian/issues)
- **Discussions:** [Share ideas & feedback](https://github.com/archiesgate42-glitch/archie-guardian/discussions)
- **LinkedIn:** [@ArchieGate](https://linkedin.com)

---

## 💡 Philosophy

Archie Guardian embodies three principles:

1. **Transparency** — You understand every decision the system makes
2. **Autonomy** — You control what Guardian can do
3. **Community** — Together we build the security tools we deserve

---

## 🎓 Tech Stack

- **Python 3.9+** — Core language
- **psutil** — System monitoring
- **watchdog** — File system events
- **requests** — Ollama API communication
- **Ollama + Llama3** — Local LLM inference
- **CrewAI** — Multi-agent orchestration (v1.1+)

---

## 📈 Stats

- ⭐ **GitHub Stars:** Growing community
- 🚀 **v1.0 Release:** Production-ready
- 🤖 **AI Integration:** Ollama + Llama3
- 📊 **6 Widgets:** File, Process, Network, Defender, RRNC, Chat
- 🔒 **100% Local:** Zero cloud dependencies

---

**Made with ❤️ by Archie Gate (Louis J.)**  
*Local AI Security for Everyone*  
*November 2025*

---

## 🔗 Quick Links

- Repository: https://github.com/archiesgate42-glitch/archie-guardian
- Download Ollama: https://ollama.ai
- Report Issues: https://github.com/archiesgate42-glitch/archie-guardian/issues
- Discussions: https://github.com/archiesgate42-glitch/archie-guardian/discussions

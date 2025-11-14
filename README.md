# Archie Guardian: Local, Ethical, Co-Orchestrated Security

## A Technical Paper on Multi-Agent AI-Driven System Protection

  

**Author:** Archie Gate  

**Date:** November 2025  

**Status:** Technical Specification & Architecture Design  

**Version:** 0.1 (MVP Specification)

  

---

  

## Executive Summary

  

Archie Guardian is a **local-first, modular security system** that leverages multi-agent AI orchestration (via CrewAI) to deliver transparent, user-controlled threat detection and response. Unlike cloud-dependent solutions, Archie Guardian runs entirely on user hardware with optional local LLM inference (Ollama), ensuring complete data privacy and eliminates proprietary black-box security analysis.

  

The system embodies **co-orchestration philosophy**: human and AI agents collaborate transparently, with users maintaining granular permission models and full audit trails. This paper details the architectural patterns, security model, performance considerations, and extensibility framework that make Archie Guardian a paradigm shift in personal security tools.

  

---

  

## 1. Introduction & Philosophy

  

### 1.1 Problem Statement

  

Current security tools suffer from three critical limitations:

  

1. **Opacity:** Users cannot understand *why* an alert fired or what the system decided.

2. **Cloud Dependency:** Telemetry, analysis, and threat intelligence leak to third parties.

3. **Inflexibility:** Pre-defined rules and scoring; no user context or learning from feedback.

  

### 1.2 Our Approach: Co-Orchestration

  

Archie Guardian reframes security as a **human-AI partnership**:

  

- **OrchA (AI Task Master):** Autonomous threat analysis, pattern matching, confidence scoring.

- **OrchB (Human-Facing Agent):** Permission management, user feedback integration, alert translation.

- **Tech-Human Translator:** Converts technical findings into actionable, understandable language.

- **Modular Widgets:** Independent sensor modules (File Integrity, Process Monitor, Network Sniffer) that plug into the orchestration framework.

  

This design ensures:

- **Transparency:** Every decision logged and explainable.

- **Control:** Users grant permissions at granular levels.

- **Learning:** System improves from user feedback (false positive flagging, context tuning).

  

### 1.3 Target Use Cases

  

1. **Developer machines** running sensitive code/projects.

2. **Security-conscious users** wanting local, auditable monitoring.

3. **Compliance scenarios** (e.g., forensic recovery audits, internal security reviews).

4. **Educational/research** exploration of AI-driven security patterns.

  

---

  

## 2. Architecture Overview

  

### 2.1 Layered Architecture

  

Archie Guardian operates across four integrated layers:

  .\Archie Guardian\assets\Schermafbeelding 2025-11-14 210112.png

  

### 2.2 Core Components

  

#### **2.2.1 Orchestrators**

  

**OrchA (AI Task Master):**

- Consumes sensor signals from active widgets.

- Routes to AI inference layer (Ollama).

- Assigns threat levels (Low/Med/High) based on confidence thresholds.

- Maintains audit log of all decisions.

- Implements learning loop from user feedback.

  

**OrchB (Human-Facing Agent):**

- Intercepts user commands via CLI.

- Checks permission model (Observe/Alert/Analyze/Isolate/Auto-Respond).

- Issues prompts for escalation when needed.

- Translates findings via Tech-Human Translator.

- Logs all user interactions for audit trail.

  

#### **2.2.2 Tech-Human Translator**

  

A specialized component that:

- Converts raw threat signals → plain English explanations.

- Contextualizes alerts ("File changed in your project folder" vs. "Suspicious write to system directory").

- Suggests remediation based on threat type and user history.

- Enables bi-directional feedback: user marks alerts as false positives → OrchA adjusts future scoring.

  

#### **2.2.3 Widget Module System**

  

**Architecture:**
.\Archie Guardian\assets\Schermafbeelding 2025-11-14 210044.png

  

**Key Features:**

- **On-Demand Loading:** Only enabled widgets consume resources.

- **Hot-Reload Capable:** Enable/disable widgets without restart.

- **Standardized Interface:** Each widget implements `sense()`, `classify()`, `report()` methods.

- **Thread-Safe Queue:** All signals serialized safely to prevent race conditions.

  

**MVP Widgets (v0.1):**

1. **File Integrity Widget:** Monitors file changes in specified directories (project folders, system paths). Uses watchdog for efficiency.

2. **Process Monitor Widget:** Tracks process spawning, unexpected children, resource spikes. Via psutil.

3. **Network Sniffer Widget:** Logs outbound connections, flags suspicious IPs/domains. Via socket hooks + optional Scapy.

  

**Future Widgets (v2+):**

- Resource Drain (CPU/RAM anomalies).

- Registry/Config Watch (Windows-specific system changes).

- Cryptography Detector (SSL/TLS mismatches).

- User Behavior (keylogger patterns, remote access signs).

- Log Analyzer (correlate Windows/system logs).

- Community-contributed modules (plugin marketplace).

  

### 2.3 Data Flow: Sensing → Analysis → Action

  .\Archie Guardian\assets\Schermafbeelding 2025-11-14 210052.png


---

  

## 3. Multi-Agent Orchestration (CrewAI Integration)

  

### 3.1 Agent Topology

  

Archie Guardian instantiates **10 agents** (MVP: 2 orchestrators + 3 functional + 1 translator; v2: +6 optional):

  

| Agent | Role | Task | Inputs | Outputs |

|-------|------|------|--------|---------|

| **OrchA** | AI Task Master | Coordinate analysis, threat scoring | Sensor signals | Threat level, confidence |

| **OrchB** | Human-Facing | Permission checks, user feedback | User commands | Escalation prompts, audit logs |

| **File Integrity Sensor** | Functional | Monitor file changes | Watchdog events | File delta events |

| **Process Monitor Sensor** | Functional | Track process spawning | psutil data | Process events |

| **Network Sniffer Sensor** | Functional | Log connections | Socket hooks | Network events |

| **Tech-Human Translator** | Context Creator | Explain threats in plain English | Raw events + AI scores | Human-readable alerts |

| *(+4 more in v2)* | — | — | — | — |

.\Archie Guardian\assets\Schermafbeelding 2025-11-14 210024.png
  

### 3.2 CrewAI Implementation

  

Each agent uses CrewAI's task-based model:

  

```python

# Pseudo-code illustration

from crewai import Agent, Task, Crew

  

orcha = Agent(

    role="AI Task Master",

    goal="Analyze sensor data, assign threat levels",

    tools=[analyzer_tool, scorer_tool, audit_logger],

    llm=ollama_llm  # Local inference

)

  

task_analyze = Task(

    description="Score incoming signals for threat likelihood",

    agent=orcha,

    expected_output="Threat level (Low/Med/High) + confidence score"

)

  

crew = Crew(agents=[orcha, orthb, ...], tasks=[task_analyze, ...])

```

  

**Key Patterns:**

- **Sequential Task Flow:** Sensing → Aggregation → Analysis → Decision → Translation.

- **Feedback Loop:** User feedback tasks fed back to OrchA for re-tuning.

- **Tool Integration:** Each agent has access to OS-level tools (file system, process list, network stack).

- **Local LLM:** Ollama instance handles inference; no cloud calls.

  

---

  

## 4. Permission Model & Security

  

### 4.1 Tiered Permission System

  

Users define what Archie Guardian **is allowed to do** via granular levels:

  

| Level | Bevoegdheden | Transparantie |

|-------|-----------|---------------|

| **Observe** | Read-only file/network monitoring | All events logged |

| **Alert** | Can send notifications, generate logs | User sees all alerts |

| **Analyze** | AI can analyze context, suggest actions | Reasoning logged |

| **Isolate** | Can quarantine suspicious processes | Requires user approval |

| **Auto-Respond** | Automatic mitigation (blocks, kills) | Full audit trail, opt-in only |

  

### 4.2 User Interaction Flow (Permission Escalation)

  

```

User CMD: "guardian> enable-network-sniffer"

  ↓

OrchB checks permission model (user set to "Observe")

  ↓

Network Sniffer needs "Analyze" permission

  ↓

Escalation prompt: "Network monitoring enabled?"

  ↓

User approves [YES] → Widget activates, logs approval

       OR declines [NO] → Logged as denied, no action

```

  ![[Schermafbeelding 2025-11-14 210024.png]]

### 4.3 Audit Trail & Accountability

  

Every decision logged:

- **What:** Permission check, widget activation, alert fired, user feedback.

- **When:** Precise timestamp.

- **Why:** Reasoning (confidence score, matching pattern).

- **Who:** User approval, auto-action trigger, AI scoring.

  

Example audit entry:

```

[2025-11-14 20:15:33] FILE_INTEGRITY: /home/archie/Projects/secret.txt modified

[2025-11-14 20:15:34] OrchA: Threat score 42% (LOW) - known project directory, time: night

[2025-11-14 20:15:35] OrchB: Alert threshold met, user permission: "Alert"

[2025-11-14 20:15:36] USER_FEEDBACK: "False positive - I edited the file" → learning triggered

```

  

---

  

## 5. Local LLM Integration (Ollama)

  

### 5.1 Why Ollama?

  

- **Privacy:** Inference runs locally; no data leaves the machine.

- **Speed:** Sub-second latency for threat scoring.

- **Customization:** Fine-tune model on user's threat taxonomy.

- **Simplicity:** Single command to spin up (`ollama run mistral` or similar).

  

### 5.2 Inference Pipeline

  

```

Raw event (e.g., "Process powershell.exe spawned by chrome.exe")

  ↓

Context embedding (system info, recent events, user history)

  ↓

Ollama LLM prompt:

  "Assess threat: {event}. Context: {history}. Score 0-100."

  ↓

LLM output: "Score: 35 (LOW - process chain plausible, no suspicious args)"

  ↓

OrchA assigns confidence: 35% < 60% → LOG ONLY

```

  

### 5.3 Model Selection

  

**MVP (v0.1):** Mistral 7B (balance of speed + accuracy, ~4GB VRAM)  

**v2+:** Option to swap for Llama 2, Falcon, etc. based on user preference.

  

---

  

## 6. CLI & User Interface

  

### 6.1 CLI Command Structure

  

```

guardian [command] [options]

  

Commands:

  status                    Show Guardian status, active widgets, alerts

  enable <widget>           Enable widget (with permission check)

  disable <widget>          Disable widget

  config <param> <value>    Set permission level or thresholds

  logs [--filter=<type>]    View audit trail

  feedback [--mark-fp]      Mark alert as false positive (learning)

  co-tune                   Interactive co-creation with OrchB (ask questions)

  help                      Show help

  

Examples:

  $ guardian status

  Status: ACTIVE

  Widgets: [File Integrity: ON] [Process Monitor: ON] [Network: OFF]

  Alerts (24h): 3 (1 high, 2 low)

  $ guardian enable network-sniffer

  Permission check: Current level = "Observe" (insufficient)

  Escalate to "Analyze"? [Y/n]: Y

  Approved. Network monitoring activated.

  $ guardian feedback --mark-fp 42

  Alert #42 marked as false positive → OrchA adjusts scoring

```

  

### 6.2 Dashboard (Optional TUI)

  

Real-time minimal dashboard (using `rich` or `blessed` library):

  

```

╔═════════════════════════════════════════╗

║   ARCHIE GUARDIAN v0.1 - STATUS        ║

╠═════════════════════════════════════════╣

║ System: ACTIVE | Threats: 0 | FP: 2    ║

║ ┌──────────────────────────────────┐   ║

║ │ [✓] File Integrity   [>>>>>>  ] │   ║

║ │ [✓] Process Monitor  [>>>>>>>]  │   ║

║ │ [ ] Network Sniffer  [disabled] │   ║

║ └──────────────────────────────────┘   ║

║ Recent: 20:15 - File changed /proj     ║

║         20:12 - Process spawn OK       ║

╚═════════════════════════════════════════╝

```

  

---

  

## 7. Performance & Scalability

  

### 7.1 Resource Profile (MVP)

  

| Component | CPU | RAM | Disk | Network |

|-----------|-----|-----|------|---------|

| OrchA + OrchB (Python base) | ~2-5% idle | 50-100 MB | — | — |

| Ollama (local LLM inference) | 20-30% (during score) | 500MB - 4GB | 4-8 GB | — |

| File Integrity Widget | 0-2% (idle) | 20 MB | — | — |

| Process Monitor Widget | 1-2% (idle) | 10 MB | — | — |

| Network Sniffer Widget | 1-3% (idle) | 30 MB | — | — |

| **Total (all active)** | **5-15%** | **600MB - 4.2GB** | **4-8GB** | **Minimal** |

  

**Notes:**

- Ollama inference spikes briefly when analyzing each event.

- Watchdog (file monitoring) is extremely efficient; OS-native.

- On-demand widget loading keeps baseline low.

  

### 7.2 Scalability Path

  

- **v0.1 (MVP):** Single machine, 3 widgets, local LLM.

- **v1:** Hot-reload widgets, plugin system, extended dashboard.

- **v2+:** Multi-machine telemetry (optional), distributed widget network, advanced tuning UI.

  

---

  

## 8. Threat Model & Security Considerations

  

### 8.1 Assumed Threat Model

  

Archie Guardian protects against:

- **File tampering** in project/sensitive directories (ransomware, accidental overwrites).

- **Suspicious processes** (crypto-miners, malware spawned by compromised apps).

- **Unexpected network activity** (C2 callbacks, exfiltration attempts).

- **User context deviation** (anomalous behavior flags).

  

Archie Guardian does **not** protect against:

- **Kernel-level rootkits** (assumption: local LLM & watchdog can't bypass kernel-mode threats).

- **Offline attacks** (Guardian only monitors active system).

- **Cryptographic backdoors** (relies on system crypto libs being trustworthy).

  

### 8.2 Local-First Security

  

By running locally:

- ✅ No cloud telemetry leaks.

- ✅ No third-party keys/credentials exposed.

- ✅ User retains all data & control.

- ⚠️ Single-machine attack surface (if machine compromised, Guardian can be bypassed).

  

Mitigation: Encourage users to:

- Run OS security updates regularly.

- Use signed, trusted LLM models (e.g., official Ollama registry).

- Enable audit logging and review periodically.

  

---

  

## 9. Extensibility & Community

  

### 9.1 Widget Plugin System

  

Custom widgets follow this interface:

  

```python

class CustomWidget:

    def sense(self) -> List[Event]:

        """Return list of detected events."""

        pass

    def classify(self, event: Event) -> Classification:

        """Classify event severity/type."""

        pass

    def report(self) -> Dict:

        """Return telemetry for audit log."""

        pass

```

  

Users/community can drop custom widgets into `/archie/widgets/` folder; system auto-loads.

  

### 9.2 Community Contributions

  

Future roadmap includes:

- **Widget Marketplace:** GitHub-based registry of community-built sensors.

- **LLM Fine-Tuning:** Shared models tuned for specific threat domains (e.g., crypto-theft, ransomware).

- **Co-Creation Events:** Hackathons & workshops on extending Archie Guardian.

  

---

  

## 10. Deployment & Adoption Path

  

### 10.1 Installation (v0.1)

  

```bash

# Clone repo

git clone https://github.com/ArchieGate/archie-guardian.git

cd archie-guardian

  

# Install dependencies

pip install -r requirements.txt

  

# Set up Ollama (one-time)

ollama pull mistral

  

# Run

python guardian.py

```

  

### 10.2 Adoption Strategy

  

1. **v0.1 (November 2025):** MVP release (File Integrity + Process Monitor + basic CLI).

2. **Early adopters:** Developers, security researchers, DevOps teams.

3. **Feedback collection:** Community testing, fine-tuning threat scoring.

4. **v1 (Q1 2026):** Network Sniffer, advanced CLI, plugin system.

5. **v2+ (H2 2026):** Multi-machine support, marketplace, governance model.

  

---

  

## 11. Comparison with Existing Tools

  

| Feature | Guardian | osquery | Wazuh | Splunk |

|---------|----------|---------|-------|--------|

| **Local-first** | ✅ Yes | ✅ Yes | ⚠️ Hybrid | ❌ Cloud-centric |

| **Transparent AI** | ✅ Yes | ❌ No | ❌ Opaque rules | ❌ Black-box ML |

| **Modular widgets** | ✅ Yes | ✅ Yes | ⚠️ Limited | ❌ Monolithic |

| **User learning** | ✅ Yes | ❌ No | ❌ No | ❌ No |

| **Permission model** | ✅ Granular | ❌ No | ⚠️ Basic | ❌ No |

| **Cost** | 💰 Free | 💰 Free | 💰 Freemium | 💰 Enterprise |

| **Ease of setup** | ✅ ~5 min | ⚠️ ~30 min | ❌ Complex | ❌ Very complex |

  

---

  

## 12. Roadmap & Future Work

  

### 12.1 MVP (v0.1) - November 2025

- ✅ File Integrity Widget

- ✅ Process Monitor Widget

- ✅ OrchA + OrchB (basic)

- ✅ Local Ollama integration

- ✅ CLI interface

- ✅ Permission model

- ✅ Audit logging

  

### 12.2 v1 (Q1 2026)

- Network Sniffer Widget (full)

- Hot-reload capability

- Plugin system (basic)

- Advanced CLI + TUI dashboard

- Community feedback integration

  

### 12.3 v2+ (H2 2026)

- Additional widgets (Resource Drain, Registry Watch, Crypto Detector, etc.)

- Widget marketplace

- Multi-machine telemetry (optional)

- Advanced tuning UI

- Commercial support (optional)

  

---

  

## 13. Conclusion

  

Archie Guardian represents a paradigm shift in personal/developer security: **transparent, local, AI-driven, user-controlled**. By leveraging multi-agent orchestration (CrewAI), modular widget architecture, and local LLM inference, it delivers security without compromise.

  

The system is designed for:

- **Developers** who want to understand their system's threats.

- **Security practitioners** exploring AI-driven defense.

- **Privacy advocates** rejecting cloud-dependent tools.

- **Communities** building together on open-source security.

  

We invite contributions, feedback, and co-creation to evolve Archie Guardian into the security standard for the next generation of tools.

  

---

  

## Appendices

  

### A. FAQ

  

**Q: Why local inference over cloud APIs?**  

A: Privacy, latency, cost, and user control. Plus, it's the philosophical core of Guardian—transparency over convenience.

  

**Q: Can I use other LLMs besides Ollama?**  

A: v0.1 is Ollama-centric, but v1 will support pluggable LLM backends (LM Studio, Hugging Face, etc.).

  

**Q: Is this a replacement for traditional antivirus?**  

A: No; Guardian is *complementary*. It's for behavioral monitoring and anomaly detection, not signature-based malware blocking.

  

**Q: What's the learning curve?**  

A: Minimal. CLI is intuitive; advanced tuning is optional. Most users run `guardian status` and let it work.

  

### B. Glossary

  

- **OrchA:** AI Task Master orchestrator (analysis & scoring).

- **OrchB:** Human-Facing orchestrator (permissions & interaction).

- **Widget:** Modular sensor (File Integrity, Process Monitor, etc.).

- **Tech-Human Translator:** Agent that converts technical findings to plain language.

- **Co-Orchestration:** Collaborative decision-making between humans and AI agents.

- **Audit Trail:** Complete log of all system decisions and user actions.

  

### C. References

  

- CrewAI Framework: https://github.com/joaomdmoura/crewai

- Ollama Local LLM: https://ollama.ai

- watchdog (file system events): https://github.com/gorakhargosh/watchdog

- psutil (process & system monitoring): https://github.com/giampaolo/psutil

  

---

  

**End of Technical Paper**

  

**For updates, issues, contributions:** https://github.com/ArchieGate/archie-guardian  

**Community & Co-Creation:** Discord/Twitter @ArchieGate
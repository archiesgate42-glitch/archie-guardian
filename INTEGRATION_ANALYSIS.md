# Archie Guardian UI Integration - Analyse Document

## 📋 Project Analyse

### Bestaande Architectuur

#### 1. Guardian.py (Hoofdbestand)
- **Widget Management**: `widget_state` dict, `widgets_instances` dict
- **Orchestrator**: `master_orch` (MasterOrchestrator instance)
- **Chat**: `ollama_chat` widget met `send_message()` en `get_chat_history()`
- **Logging**: `log_event()` functie naar `logs/audit.log`
- **Startup**: Initialiseert alle widgets en orchestrator

#### 2. Widget Interface (Consistent)
Alle widgets implementeren:
- `start() -> bool`: Activeer widget
- `stop()`: Deactiveer widget
- `get_recent_events(limit: int) -> list`: Recente events
- `get_stats() -> dict`: Widget statistieken
- `get_actions() -> dict`: Beschikbare acties

**Beschikbare Widgets:**
1. `file_integrity` (F-I)
2. `process_monitor` (P-M)
3. `network_sniffer` (N-S)
4. `windows_defender` (W-D)
5. `rrnc` (RRNC)
6. `ollama_chat` (AI-M)

#### 3. Orchestrator Systeem
- **MasterOrchestrator**: Centrale coordinator
- **OrchA**: AI threat analyzer
- **OrchB**: Human-facing bridge met permission levels
- **PermissionLevels**: OBSERVE, ALERT, ANALYZE, ISOLATE, AUTO_RESPOND

#### 4. Chat Systeem
- **OllamaChatWidget**: `send_message()`, `get_chat_history()`
- **History**: Opgeslagen in `logs/chat_history.json`
- **Connector**: `OllamaConnector` via `core/ollama_connector.py`

#### 5. Logging
- **Audit Log**: `logs/audit.log` (append-only)
- **Chat History**: `logs/chat_history.json` (JSON array)

---

## 🔌 Integratiepunten

### API Endpoints Nodig

#### Widget Management
- `GET /api/widgets` → Lijst alle widgets + status
- `POST /api/widgets/<name>/start` → Start widget
- `POST /api/widgets/<name>/stop` → Stop widget
- `GET /api/widgets/<name>/status` → Widget status

#### Live Data Streaming
- `GET /api/stream/logs` → SSE voor audit.log
- `GET /api/stream/widgets` → SSE voor widget status updates

#### Chat Interface
- `POST /api/chat` → Send message naar Ollama
- `GET /api/chat/history` → Haal chat geschiedenis op

#### System Status
- `GET /api/status` → Overall system health
- `GET /api/config` → Current configuration
- `POST /api/config` → Update configuration

#### Permissions
- `GET /api/permissions` → Huidige permission level
- `POST /api/permissions` → Update permission level

---

## 🏗️ Implementatie Plan

### Fase 1: GuardianBridge Service
**Bestand**: `services/guardian_bridge.py`

**Functionaliteit:**
- Interface tussen Flask UI en guardian.py
- Singleton pattern (één instance)
- Widget start/stop via `widget_state` en `widgets_instances`
- Chat forwarding naar `ollama_chat` widget
- Log streaming via file tailing
- Status polling

### Fase 2: Flask API
**Bestand**: `guardian_api.py`

**Features:**
- Flask app met CORS enabled
- Alle endpoints zoals hierboven
- Error handling decorator
- SSE streaming voor logs en status

### Fase 3: Frontend
**Bestanden**: 
- `templates/index.html` (HTML)
- `static/css/style.css` (CSS)
- `static/js/main.js` (JavaScript)

**Layout (volgens image):**
1. **Top Section**: Model selectie + kleur indicators (widget status)
2. **Left Section**: Overzicht en live gegevens (terminal output)
3. **Right Section**: Output chatvenster (chat history)
4. **Bottom Section**: Input chatvenster (chat input)

**Features:**
- Widget control cards met enable/disable
- Real-time log streaming
- Chat interface met history
- Error display component
- SSE reconnection logic
- Mobile responsive

---

## 🔄 Data Flow

```
UI (Browser)
    ↓ HTTP/SSE
Flask API (guardian_api.py)
    ↓ Python calls
GuardianBridge (services/guardian_bridge.py)
    ↓ Direct access
guardian.py globals (widget_state, widgets_instances, master_orch)
    ↓ Widget methods
Widget Instances (file_integrity, process_monitor, etc.)
```

---

## ✅ Dependencies Check

**Al aanwezig in requirements.txt:**
- ✅ Flask (via venv)
- ✅ flask-cors (via venv)
- ✅ requests (voor Ollama)
- ✅ watchdog (voor file monitoring)
- ✅ psutil (voor process monitoring)

**Nieuwe dependencies nodig:**
- Geen! Alles is al beschikbaar.

---

## 🎯 Integratie Strategie

### Singleton Pattern voor GuardianBridge
- Één instance die guardian.py globals beheert
- Thread-safe voor concurrent requests
- Lazy initialization

### SSE Streaming
- Log streaming: Tail `logs/audit.log` file
- Status streaming: Poll widget status elke 2 seconden
- Reconnection logic met exponential backoff

### Error Handling
- Decorator pattern voor alle endpoints
- Consistent error response format
- Logging naar console + audit.log

---

## 📝 Volgende Stappen

1. ✅ Analyse compleet
2. ⏳ Maak GuardianBridge service
3. ⏳ Implementeer Flask API
4. ⏳ Maak HTML/CSS/JS frontend
5. ⏳ Test end-to-end integratie
6. ⏳ Mobile responsive verificatie


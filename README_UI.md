# Archie Guardian UI - Gebruikershandleiding

## 🚀 Quick Start

### Stap 1: Start Guardian Backend

**Optie A: Start via start_ui.py (Aanbevolen)**
```bash
python start_ui.py
```

Dit script:
- Initialiseert de guardian.py backend
- Laadt alle widgets en orchestrator
- Start de Flask UI server automatisch

**Optie B: Handmatig starten**
```bash
# Terminal 1: Start guardian.py (laat dit draaien)
python guardian.py
# (Laat dit draaien, druk Ctrl+C om te stoppen)

# Terminal 2: Start UI server
python guardian_api.py
```

### Stap 2: Open de UI

Open je webbrowser en ga naar:
```
http://localhost:5000
```

---

## 📋 UI Functionaliteit

### Top Sectie: Widget Status

- **Widget Cards**: Elke widget heeft een kaart met status indicator
- **Kleuren**:
  - 🟢 Groen = Actief
  - ⚪ Grijs = Idle
  - 🔴 Rood = Error
- **Controls**: Klik op ▶ om te starten, ⏸ om te stoppen

**Beschikbare Widgets:**
- **F-I**: File Integrity Monitor
- **N-S**: Network Sniffer
- **RRNC**: Rapid Response Neutralize & Capture
- **ORC**: Orchestrator
- **P-M**: Process Monitor
- **W-D**: Windows Defender
- **AI-M**: Ollama Chat

### Linker Sectie: Live Logs

- Real-time streaming van `logs/audit.log`
- Toont alle Guardian activiteit
- Auto-scroll naar nieuwste logs
- Kleurcodering:
  - Groen = Success
  - Rood = Error
  - Geel = Warning
  - Blauw = Info

### Rechter Sectie: Chat Output

- Chat geschiedenis met ArchieGuardian AI
- Berichten worden automatisch geladen bij start
- Real-time updates tijdens chat sessies

### Onderste Sectie: Chat Input

- Type je bericht in het input veld
- Druk Enter of klik "Verstuur"
- Typing indicator tijdens AI response
- Auto-focus voor snelle input

---

## 🔧 API Endpoints

De UI gebruikt de volgende API endpoints:

### Widget Management
- `GET /api/widgets` - Lijst alle widgets + status
- `POST /api/widgets/<name>/start` - Start widget
- `POST /api/widgets/<name>/stop` - Stop widget
- `GET /api/widgets/<name>/status` - Widget status

### Chat
- `POST /api/chat` - Stuur bericht naar Ollama
- `GET /api/chat/history` - Haal chat geschiedenis op

### Streaming (SSE)
- `GET /api/stream/logs` - Real-time log streaming
- `GET /api/stream/widgets` - Real-time widget status updates

### System
- `GET /api/status` - System health
- `GET /api/config` - Configuration
- `GET /api/permissions` - Permission level
- `GET /api/health` - Health check

---

## 🐛 Troubleshooting

### UI laadt niet
1. Check of Flask server draait: `python guardian_api.py`
2. Check browser console voor errors (F12)
3. Check of poort 5000 beschikbaar is

### Widgets starten niet
1. Check of guardian.py backend draait
2. Check `logs/audit.log` voor errors
3. Zorg dat widgets correct geïnstalleerd zijn

### Chat werkt niet
1. Zorg dat Ollama service draait: `ollama serve`
2. Enable de `ollama_chat` widget eerst
3. Check Ollama connectie in terminal output

### Logs streamen niet
1. Check of `logs/audit.log` bestaat
2. Check browser console voor SSE errors
3. Refresh de pagina

### Mobile Layout Issues
- UI is responsive maar werkt het beste op desktop
- Op mobile: gebruik landscape mode voor betere ervaring
- Widget cards worden kleiner op kleine schermen

---

## 📱 Mobile Support

De UI is responsive en werkt op:
- Desktop (1920x1080+): Volledige layout
- Tablet (768px+): Aangepaste layout
- Mobile (480px+): Compacte layout

**Mobile Features:**
- Touch-friendly buttons
- Responsive widget grid
- Scrollable chat en logs
- Auto-adjusting layout

---

## 🔒 Security Notes

- UI draait lokaal op `localhost:5000`
- Geen externe toegang standaard
- CORS is enabled voor development
- Voor productie: disable debug mode in `guardian_api.py`

---

## 📝 Development

### Project Structuur
```
.
├── guardian.py              # Backend (moet draaien)
├── guardian_api.py          # Flask API server
├── start_ui.py              # Start script (aanbevolen)
├── services/
│   └── guardian_bridge.py   # Bridge tussen UI en backend
├── templates/
│   └── index.html           # HTML template
└── static/
    ├── css/
    │   └── style.css        # Stylesheet
    └── js/
        └── main.js          # JavaScript logic
```

### Debug Mode
In `guardian_api.py`:
```python
app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
```

### Logging
- Backend logs: `logs/audit.log`
- Flask logs: Console output
- Browser logs: F12 Developer Tools

---

## ✅ Test Checklist

- [ ] Guardian backend start zonder errors
- [ ] UI laadt op http://localhost:5000
- [ ] Widgets kunnen worden gestart/gestopt
- [ ] Logs streamen real-time
- [ ] Chat functionaliteit werkt
- [ ] Error messages tonen correct
- [ ] Reconnection werkt na connection loss
- [ ] Mobile layout werkt correct
- [ ] Layout matcht de provided image

---

## 🎯 Volgende Stappen

1. **Test alle functionaliteit** volgens checklist
2. **Verifieer layout** matcht de provided image
3. **Test op mobile** devices
4. **Check error handling** in verschillende scenarios
5. **Documenteer** eventuele issues

---

**Gemaakt voor Archie Guardian v1.0**  
*Local AI Security for Everyone*


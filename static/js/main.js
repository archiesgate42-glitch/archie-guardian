/**
 * Archie Guardian UI - Main JavaScript
 * Widget Management, Chat, SSE Streaming, Error Handling
 */

// ============================================================================
// Widget Manager Class
// ============================================================================

class WidgetManager {
    constructor() {
        this.widgets = {};
        this.pollInterval = 2000; // Poll every 2 seconds
        this.widgetMapping = {
            'file_integrity': { name: 'F-I', color: '#4a90e2' },
            'network_sniffer': { name: 'N-S', color: '#ffd700' },
            'rrnc': { name: 'RRNC', color: '#ff0000' },
            'orchestrator': { name: 'ORC', color: '#00ff00' },
            'process_monitor': { name: 'P-M', color: '#ff8800' },
            'windows_defender': { name: 'W-D', color: '#4a2a7a' },
            'ollama_chat': { name: 'AI-M', color: '#9b59b6' }
        };
        this.modelLogos = {
            'llama': '/assets/logo-llama.jpg',
            'llama3': '/assets/logo-llama.jpg',
            'llama3.1': '/assets/logo-llama.jpg',
            'gpt': '/assets/logo-gpt.jpg',
            'gpt-4': '/assets/logo-gpt.jpg',
            'mistral': '/assets/logo-Minstral.jpg',
            'minstral': '/assets/logo-Minstral.jpg'
        };
        this.currentModel = 'llama3.1';
        this.init();
    }

    async init() {
        await this.loadWidgets();
        this.startPolling();
        this.attachEventListeners();
        this.updateModelLogo();
    }

    async loadWidgets() {
        try {
            const response = await fetch('/api/widgets');
            if (!response.ok) throw new Error('Failed to load widgets');

            const widgets = await response.json();
            this.renderWidgets(widgets);

            widgets.forEach(widget => {
                this.updateWidgetUI(widget);
                // Store widget data for model logo detection
                this.widgets[widget.name] = widget;
            });
            
            // Update model logo if ollama_chat widget is available
            if (this.widgets['ollama_chat']) {
                this.updateModelLogo();
            }
        } catch (error) {
            console.error('Widget load error:', error);
            ErrorManager.showError('Failed to load widget status');
        }
    }

    startPolling() {
        setInterval(async () => {
            try {
                await this.loadWidgets();
            } catch (error) {
                console.error('Polling error:', error);
            }
        }, this.pollInterval);
    }

    renderWidgets(widgets) {
        const grid = document.getElementById('widget-grid');
        if (!grid) return;

        grid.innerHTML = '';

        widgets.forEach(widget => {
            const mapping = this.widgetMapping[widget.name] || { name: widget.name, color: '#666' };
            const card = document.createElement('div');
            card.className = 'widget-card';
            card.dataset.widget = widget.name;

            const status = widget.active ? 'active' : 'idle';
            const action = widget.active ? 'stop' : 'start';
            const buttonText = widget.active ? '⏸' : '▶';

            card.innerHTML = `
                <div class="widget-info">
                    <span class="widget-name">${mapping.name}</span>
                    <span class="widget-status" data-status="${status}">●</span>
                </div>
                <button class="widget-toggle" data-action="${action}">${buttonText}</button>
            `;

            grid.appendChild(card);
        });

        // Setup event listeners for new buttons
        this.setupEventListeners();
    }

    attachEventListeners() {
        // Use event delegation for dynamic widgets
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('widget-toggle')) {
                const widgetCard = e.target.closest('.widget-card');
                const widgetName = widgetCard?.dataset.widget;
                const action = e.target.dataset.action;
                
                if (widgetName && action) {
                    this.toggleWidget(widgetName, action);
                }
            }
        });
    }

    async toggleWidget(widgetName, action) {
        const button = document.querySelector(
            `.widget-card[data-widget="${widgetName}"] .widget-toggle`
        );

        if (!button) return;

        // Loading state
        button.disabled = true;
        button.textContent = '⏳';

        try {
            const endpoint = action === 'start' ? 'start' : 'stop';
            const response = await fetch(`/api/widgets/${widgetName}/${endpoint}`, {
                method: 'POST'
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || error.message || 'Unknown error');
            }

            const result = await response.json();
            
            // Update UI with new status
            this.updateWidgetUI({
                name: widgetName,
                status: result.status || (action === 'start' ? 'active' : 'idle'),
                enabled: result.status === 'active' || action === 'start'
            });

        } catch (error) {
            console.error(`Widget ${action} failed:`, error);
            ErrorManager.showError(`Failed to ${action} widget: ${error.message}`);
        } finally {
            button.disabled = false;
        }
    }

    updateWidgetUI(widget) {
        const card = document.querySelector(`.widget-card[data-widget="${widget.name}"]`);
        if (!card) return;

        const statusDot = card.querySelector('.widget-status');
        const button = card.querySelector('.widget-toggle');

        const isActive = widget.enabled || widget.status === 'active';

        if (statusDot) {
            statusDot.dataset.status = isActive ? 'active' : 'idle';
        }

        if (button) {
            if (isActive) {
                button.dataset.action = 'stop';
                button.textContent = '⏸';
                button.style.background = '#e74c3c';
            } else {
                button.dataset.action = 'start';
                button.textContent = '▶';
                button.style.background = '#4a90e2';
            }
        }
    }


    updateModelLogo() {
        // Get model from ollama_chat widget if available
        const ollamaWidget = this.widgets['ollama_chat'];
        if (ollamaWidget && ollamaWidget.model) {
            const modelName = ollamaWidget.model.toLowerCase();
            this.setModelLogo(modelName);
        } else {
            // Default to llama
            this.setModelLogo('llama3.1');
        }
    }

    setModelLogo(modelName) {
        const modelLogoEl = document.getElementById('model-logo');
        const modelNameEl = document.getElementById('model-name');
        
        if (!modelLogoEl || !modelNameEl) return;

        // Find matching logo
        let logoPath = this.modelLogos['llama']; // Default
        let displayName = 'Llama3.1';

        // Check for exact match first
        if (this.modelLogos[modelName]) {
            logoPath = this.modelLogos[modelName];
            displayName = this.formatModelName(modelName);
        } else {
            // Check for partial matches
            for (const [key, path] of Object.entries(this.modelLogos)) {
                if (modelName.includes(key) || key.includes(modelName)) {
                    logoPath = path;
                    displayName = this.formatModelName(modelName);
                    break;
                }
            }
        }

        // Update logo and name
        if (modelLogoEl.src !== logoPath) {
            modelLogoEl.src = logoPath;
            modelLogoEl.alt = displayName;
        }
        modelNameEl.textContent = displayName;
        this.currentModel = modelName;
    }

    formatModelName(modelName) {
        // Format model name for display
        const name = modelName.toLowerCase();
        if (name.includes('llama')) {
            if (name.includes('3.1')) return 'Llama3.1';
            if (name.includes('3')) return 'Llama3';
            return 'Llama';
        }
        if (name.includes('gpt')) {
            if (name.includes('4')) return 'GPT-4';
            return 'GPT';
        }
        if (name.includes('mistral') || name.includes('minstral')) {
            return 'Mistral';
        }
        // Default: capitalize first letter
        return modelName.charAt(0).toUpperCase() + modelName.slice(1);
    }
}

// ============================================================================
// SSE Manager Class
// ============================================================================

class SSEManager {
    constructor(url, onMessage, onError) {
        this.url = url;
        this.onMessage = onMessage;
        this.onError = onError;
        this.eventSource = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 3000;
        this.connect();
    }

    connect() {
        try {
            this.eventSource = new EventSource(this.url);

            this.eventSource.onmessage = (event) => {
                this.reconnectAttempts = 0; // Reset on success
                if (this.onMessage) {
                    this.onMessage(event);
                }
            };

            this.eventSource.onerror = (error) => {
                console.error('SSE Error:', error);
                this.handleError();
            };

            this.eventSource.onopen = () => {
                console.log('SSE Connected:', this.url);
                this.reconnectAttempts = 0;
            };

        } catch (error) {
            console.error('Failed to create EventSource:', error);
            this.handleError();
        }
    }

    handleError() {
        if (this.eventSource) {
            this.eventSource.close();
        }

        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`Reconnecting (attempt ${this.reconnectAttempts})...`);

            setTimeout(() => {
                this.connect();
            }, this.reconnectDelay);

            if (this.onError) {
                this.onError(`Connection lost. Reconnecting... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
            }
        } else {
            if (this.onError) {
                this.onError('Connection failed after multiple attempts. Please refresh the page.');
            }
        }
    }

    close() {
        if (this.eventSource) {
            this.eventSource.close();
        }
    }
}

// ============================================================================
// Log Manager Class
// ============================================================================

class LogManager {
    constructor() {
        this.terminalContent = document.getElementById('terminal-content');
        this.sseManager = null;
        this.init();
    }

    init() {
        if (!this.terminalContent) return;

        // Initial startup message
        this.appendLog('ARCHIE GUARDIAN v1.0 - Local AI Security + Multi-Agent Orchestration + Ollama', 'info');
        this.appendLog('Initializing UI...', 'info');

        // Start SSE stream
        this.sseManager = new SSEManager(
            '/api/stream/logs',
            (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.appendLog(data.log, 'info');
                } catch (error) {
                    console.error('Error parsing log data:', error);
                }
            },
            (error) => {
                ErrorManager.showError(error);
            }
        );
    }

    appendLog(message, type = 'info') {
        if (!this.terminalContent) return;

        const logEntry = document.createElement('div');
        logEntry.className = `log-entry ${type}`;
        logEntry.textContent = message;

        this.terminalContent.appendChild(logEntry);
        this.terminalContent.scrollTop = this.terminalContent.scrollHeight;

        // Limit log entries to prevent memory issues
        const maxEntries = 1000;
        while (this.terminalContent.children.length > maxEntries) {
            this.terminalContent.removeChild(this.terminalContent.firstChild);
        }
    }
}

// ============================================================================
// Chat Manager Class
// ============================================================================

class ChatManager {
    constructor() {
        this.chatOutput = document.getElementById('chat-output');
        this.userInput = document.getElementById('user-input');
        this.sendBtn = document.getElementById('send-btn');
        this.isProcessing = false;
        this.init();
    }

    init() {
        if (!this.chatOutput || !this.userInput || !this.sendBtn) return;

        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Load chat history on init
        this.loadHistory();
    }

    async loadHistory() {
        try {
            const response = await fetch('/api/chat/history?limit=20');
            if (!response.ok) throw new Error('Failed to load history');

            const history = await response.json();
            history.forEach(msg => {
                this.displayMessage(msg.user, 'user', msg.timestamp);
                this.displayMessage(msg.assistant, 'ai', msg.timestamp);
            });
        } catch (error) {
            console.error('Could not load chat history:', error);
        }
    }

    async sendMessage() {
        if (this.isProcessing) return;

        const message = this.userInput.value.trim();
        if (!message) return;

        // Display user message
        this.displayMessage(message, 'user');
        this.userInput.value = '';

        // Show typing indicator
        const typingId = this.showTypingIndicator();

        this.isProcessing = true;
        this.sendBtn.disabled = true;

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.message || 'Chat request failed');
            }

            const data = await response.json();

            // Remove typing indicator
            this.removeTypingIndicator(typingId);

            // Display AI response
            this.displayMessage(data.response, 'ai');

        } catch (error) {
            console.error('Chat error:', error);
            this.removeTypingIndicator(typingId);
            this.displayMessage(
                `Error: ${error.message}. Please try again.`,
                'system'
            );
        } finally {
            this.isProcessing = false;
            this.sendBtn.disabled = false;
            this.userInput.focus();
        }
    }

    displayMessage(message, sender, timestamp = null) {
        if (!this.chatOutput) return;

        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chat-message', `chat-message--${sender}`);

        const time = timestamp ? new Date(timestamp).toLocaleTimeString() : new Date().toLocaleTimeString();

        messageDiv.innerHTML = `
            <div class="message-header">
                <span class="message-sender">${sender === 'user' ? 'You' : sender === 'ai' ? 'ArchieGuardian' : 'System'}</span>
                <span class="message-time">${time}</span>
            </div>
            <div class="message-content">${this.formatMessage(message)}</div>
        `;

        this.chatOutput.appendChild(messageDiv);
        this.chatOutput.scrollTop = this.chatOutput.scrollHeight;
    }

    formatMessage(message) {
        // Escape HTML + basic markdown-like formatting
        return message
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/\n/g, '<br>')
            .replace(/`([^`]+)`/g, '<code>$1</code>');
    }

    showTypingIndicator() {
        if (!this.chatOutput) return null;

        const id = 'typing-' + Date.now();
        const typingDiv = document.createElement('div');
        typingDiv.id = id;
        typingDiv.classList.add('chat-message', 'chat-message--ai', 'typing-indicator');
        typingDiv.innerHTML = `
            <div class="message-content">
                <span class="dot"></span>
                <span class="dot"></span>
                <span class="dot"></span>
            </div>
        `;
        this.chatOutput.appendChild(typingDiv);
        this.chatOutput.scrollTop = this.chatOutput.scrollHeight;
        return id;
    }

    removeTypingIndicator(id) {
        if (!id) return;
        const element = document.getElementById(id);
        if (element) element.remove();
    }
}

// ============================================================================
// Error Manager Class
// ============================================================================

class ErrorManager {
    static showError(message) {
        const errorDiv = document.getElementById('error-message');
        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
            setTimeout(() => {
                errorDiv.style.display = 'none';
            }, 5000);
        }
    }
}

// ============================================================================
// Initialize on page load
// ============================================================================

let widgetManager, logManager, chatManager;

document.addEventListener('DOMContentLoaded', () => {
    console.log('Initializing Archie Guardian UI...');

    // Initialize managers
    widgetManager = new WidgetManager();
    logManager = new LogManager();
    chatManager = new ChatManager();

    // Check API health
    fetch('/api/health')
        .then(response => response.json())
        .then(data => {
            if (data.bridge_connected) {
                logManager.appendLog('✅ Connected to Guardian backend', 'success');
            } else {
                logManager.appendLog('⚠️  Guardian backend not connected', 'warning');
                ErrorManager.showError('Guardian backend not connected. Please start guardian.py first.');
            }
        })
        .catch(error => {
            console.error('Health check failed:', error);
            ErrorManager.showError('Could not connect to API. Is the server running?');
        });
});


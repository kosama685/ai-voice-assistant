/**
 * Voice Assistant Web Widget
 * Production-Ready Voice Chat Widget
 */

class VoiceAssistantWidget {
    constructor(config = {}) {
        this.config = {
            apiUrl: config.apiUrl || 'http://127.0.0.1:5000',
            widgetId: config.widgetId || 'voice-widget-' + Date.now(),
            theme: config.theme || 'light',
            position: config.position || 'bottom-right',
            size: config.size || 'medium',
            cornerRadius: config.cornerRadius || '12px',
            primaryColor: config.primaryColor || '#667eea',
            secondaryColor: config.secondaryColor || '#764ba2',
            companyLogo: config.companyLogo || null,
            companyName: config.companyName || 'Voice Assistant',
            ...config
        };

        this.state = {
            isOpen: false,
            isListening: false,
            isSpeaking: false,
            currentTab: 'chat',
            messages: [],
            sessionId: this.generateSessionId(),
            turnCount: 0,
            analytics: {
                voicePlays: 0,
                clicks: 0,
                turns: 0,
                startTime: Date.now()
            }
        };

        this.init();
    }

    generateSessionId() {
        return 'session_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
    }

    init() {
        this.createWidgetHTML();
        this.attachEventListeners();
        this.loadStyles();
        console.log('✅ Voice Assistant Widget Initialized', this.state.sessionId);
    }

    createWidgetHTML() {
        const container = document.createElement('div');
        container.id = this.config.widgetId;
        container.className = `voice-widget ${this.config.theme} ${this.config.position}`;
        container.innerHTML = `
            <div class="widget-button" id="widget-toggle">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M12 1C6.48 1 2 5.48 2 11v8c0 1.1.9 2 2 2h4v-8H4v-3c0-4.42 3.58-8 8-8s8 3.58 8 8v3h-4v8h4c1.1 0 2-.9 2-2v-8c0-5.52-4.48-10-10-10z"/>
                </svg>
            </div>

            <div class="widget-window" id="widget-window" style="display: none;">
                <div class="widget-header">
                    <div class="header-content">
                        ${this.config.companyLogo ? `<img src="${this.config.companyLogo}" class="company-logo">` : ''}
                        <div class="header-text">
                            <h3>${this.config.companyName}</h3>
                            <span class="status-indicator">● Online</span>
                        </div>
                    </div>
                    <button class="close-btn" id="widget-close">✕</button>
                </div>

                <div class="widget-tabs">
                    <button class="tab-btn active" data-tab="chat">💬 Chat</button>
                    <button class="tab-btn" data-tab="voice">🎤 Voice</button>
                    <button class="tab-btn" data-tab="info">ℹ️ Info</button>
                    <button class="tab-btn" data-tab="settings">⚙️ Settings</button>
                </div>

                <div class="widget-content">
                    <!-- Chat Tab -->
                    <div class="tab-content active" id="tab-chat">
                        <div class="chat-messages" id="chat-messages"></div>
                        <div class="chat-input-area">
                            <input type="text" id="chat-input" placeholder="Type your message..." class="chat-input">
                            <button id="send-btn" class="send-btn">Send</button>
                        </div>
                    </div>

                    <!-- Voice Tab -->
                    <div class="tab-content" id="tab-voice">
                        <div class="voice-controls">
                            <button id="mic-btn" class="mic-btn">
                                <svg width="48" height="48" viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
                                    <path d="M17 16.91c-1.48 1.46-3.51 2.36-5.7 2.36-2.2 0-4.23-.9-5.7-2.36M19 12h2c0 .64-.27 1.26-.74 1.73"/>
                                </svg>
                            </button>
                            <div class="voice-status" id="voice-status">Click to start listening</div>
                        </div>
                        <div class="voice-transcript" id="voice-transcript"></div>
                    </div>

                    <!-- Info Tab -->
                    <div class="tab-content" id="tab-info">
                        <div class="info-content">
                            <h4>About This Widget</h4>
                            <p>Voice Assistant powered by AI</p>
                            <div class="info-stats">
                                <div class="stat">
                                    <span class="stat-label">Session ID:</span>
                                    <span class="stat-value">${this.state.sessionId}</span>
                                </div>
                                <div class="stat">
                                    <span class="stat-label">Turns:</span>
                                    <span class="stat-value" id="stat-turns">0</span>
                                </div>
                                <div class="stat">
                                    <span class="stat-label">Voice Plays:</span>
                                    <span class="stat-value" id="stat-voice-plays">0</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Settings Tab -->
                    <div class="tab-content" id="tab-settings">
                        <div class="settings-content">
                            <div class="setting-item">
                                <label>Theme</label>
                                <select id="theme-select">
                                    <option value="light">Light</option>
                                    <option value="dark">Dark</option>
                                </select>
                            </div>
                            <div class="setting-item">
                                <label>
                                    <input type="checkbox" id="sound-toggle" checked>
                                    Enable Sound
                                </label>
                            </div>
                            <div class="setting-item">
                                <label>
                                    <input type="checkbox" id="notifications-toggle" checked>
                                    Enable Notifications
                                </label>
                            </div>
                            <button id="clear-chat-btn" class="btn-secondary">Clear Chat</button>
                        </div>
                    </div>
                </div>

                <div class="widget-footer">
                    <small>Powered by Voice Assistant</small>
                </div>
            </div>
        `;

        document.body.appendChild(container);
    }

    attachEventListeners() {
        // Toggle widget
        document.getElementById('widget-toggle').addEventListener('click', () => this.toggleWidget());
        document.getElementById('widget-close').addEventListener('click', () => this.toggleWidget());

        // Chat
        document.getElementById('send-btn').addEventListener('click', () => this.sendMessage());
        document.getElementById('chat-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });

        // Voice
        document.getElementById('mic-btn').addEventListener('click', () => this.toggleMicrophone());

        // Tabs
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.switchTab(e.target.dataset.tab));
        });

        // Settings
        document.getElementById('theme-select').addEventListener('change', (e) => this.changeTheme(e.target.value));
        document.getElementById('clear-chat-btn').addEventListener('click', () => this.clearChat());

        this.trackAnalytics('widget_initialized');
    }

    loadStyles() {
        const style = document.createElement('style');
        style.textContent = this.getStyles();
        document.head.appendChild(style);
    }

    getStyles() {
        return `
            .voice-widget {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                position: fixed;
                z-index: 9999;
            }

            .voice-widget.bottom-right {
                bottom: 20px;
                right: 20px;
            }

            .voice-widget.bottom-left {
                bottom: 20px;
                left: 20px;
            }

            .widget-button {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background: linear-gradient(135deg, ${this.config.primaryColor} 0%, ${this.config.secondaryColor} 100%);
                color: white;
                border: none;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                transition: all 0.3s ease;
            }

            .widget-button:hover {
                transform: scale(1.1);
                box-shadow: 0 6px 20px rgba(0,0,0,0.2);
            }

            .widget-window {
                position: absolute;
                bottom: 80px;
                right: 0;
                width: 400px;
                height: 600px;
                background: white;
                border-radius: ${this.config.cornerRadius};
                box-shadow: 0 5px 40px rgba(0,0,0,0.16);
                display: flex;
                flex-direction: column;
                overflow: hidden;
                animation: slideUp 0.3s ease;
            }

            @keyframes slideUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .widget-header {
                background: linear-gradient(135deg, ${this.config.primaryColor} 0%, ${this.config.secondaryColor} 100%);
                color: white;
                padding: 16px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .header-content {
                display: flex;
                align-items: center;
                gap: 12px;
            }

            .company-logo {
                width: 40px;
                height: 40px;
                border-radius: 50%;
            }

            .header-text h3 {
                margin: 0;
                font-size: 16px;
            }

            .status-indicator {
                font-size: 12px;
                opacity: 0.9;
            }

            .close-btn {
                background: none;
                border: none;
                color: white;
                font-size: 24px;
                cursor: pointer;
            }

            .widget-tabs {
                display: flex;
                border-bottom: 1px solid #e0e0e0;
                background: #f5f5f5;
            }

            .tab-btn {
                flex: 1;
                padding: 12px;
                border: none;
                background: none;
                cursor: pointer;
                font-size: 12px;
                border-bottom: 3px solid transparent;
                transition: all 0.3s;
            }

            .tab-btn.active {
                border-bottom-color: ${this.config.primaryColor};
                color: ${this.config.primaryColor};
                font-weight: 600;
            }

            .widget-content {
                flex: 1;
                overflow-y: auto;
                padding: 16px;
            }

            .tab-content {
                display: none;
            }

            .tab-content.active {
                display: block;
            }

            .chat-messages {
                display: flex;
                flex-direction: column;
                gap: 12px;
                margin-bottom: 16px;
                height: 400px;
                overflow-y: auto;
            }

            .message {
                display: flex;
                gap: 8px;
                animation: fadeIn 0.3s ease;
            }

            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }

            .message.user {
                justify-content: flex-end;
            }

            .message-bubble {
                max-width: 80%;
                padding: 12px 16px;
                border-radius: 12px;
                word-wrap: break-word;
            }

            .message.user .message-bubble {
                background: ${this.config.primaryColor};
                color: white;
            }

            .message.assistant .message-bubble {
                background: #f0f0f0;
                color: #333;
            }

            .chat-input-area {
                display: flex;
                gap: 8px;
            }

            .chat-input {
                flex: 1;
                padding: 10px 12px;
                border: 1px solid #ddd;
                border-radius: 20px;
                font-size: 14px;
            }

            .send-btn {
                padding: 10px 16px;
                background: ${this.config.primaryColor};
                color: white;
                border: none;
                border-radius: 20px;
                cursor: pointer;
                font-weight: 600;
            }

            .voice-controls {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 20px;
                padding: 40px 20px;
            }

            .mic-btn {
                width: 80px;
                height: 80px;
                border-radius: 50%;
                background: ${this.config.primaryColor};
                color: white;
                border: none;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.3s;
            }

            .mic-btn:hover {
                transform: scale(1.05);
            }

            .mic-btn.listening {
                background: #ff6b6b;
                animation: pulse 1s infinite;
            }

            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.1); }
            }

            .voice-status {
                text-align: center;
                color: #666;
                font-size: 14px;
            }

            .info-stats {
                display: flex;
                flex-direction: column;
                gap: 12px;
                margin-top: 16px;
            }

            .stat {
                display: flex;
                justify-content: space-between;
                padding: 8px;
                background: #f5f5f5;
                border-radius: 8px;
            }

            .settings-content {
                display: flex;
                flex-direction: column;
                gap: 16px;
            }

            .setting-item {
                display: flex;
                flex-direction: column;
                gap: 8px;
            }

            .setting-item select,
            .setting-item input[type="checkbox"] {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }

            .btn-secondary {
                padding: 10px 16px;
                background: #f0f0f0;
                border: 1px solid #ddd;
                border-radius: 4px;
                cursor: pointer;
            }

            .widget-footer {
                padding: 12px;
                text-align: center;
                border-top: 1px solid #e0e0e0;
                font-size: 12px;
                color: #999;
            }

            .voice-widget.dark {
                --bg: #1e1e1e;
                --text: #fff;
            }
        `;
    }

    toggleWidget() {
        this.state.isOpen = !this.state.isOpen;
        const window = document.getElementById('widget-window');
        window.style.display = this.state.isOpen ? 'flex' : 'none';
        this.trackAnalytics('widget_toggled');
    }

    switchTab(tabName) {
        document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        
        document.getElementById(`tab-${tabName}`).classList.add('active');
        event.target.classList.add('active');
        
        this.state.currentTab = tabName;
        this.trackAnalytics(`tab_switched_${tabName}`);
    }

    async sendMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        
        if (!message) return;

        this.addMessage('user', message);
        input.value = '';
        this.state.turnCount++;

        try {
            const response = await fetch(`${this.config.apiUrl}/widget/api/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message,
                    sessionId: this.state.sessionId,
                    synthesize: true
                })
            });

            const data = await response.json();

            if (!data.success) {
                console.error('API Error:', data.error);
                this.addMessage('assistant', `Error: ${data.error || 'Failed to get response'}`);
                return;
            }

            this.addMessage('assistant', data.response);
            this.trackAnalytics('message_sent');
        } catch (error) {
            console.error('Error:', error);
            this.addMessage('assistant', 'Sorry, I encountered an error. Please try again.');
        }
    }

    addMessage(sender, text) {
        const messagesDiv = document.getElementById('chat-messages');
        const messageEl = document.createElement('div');
        messageEl.className = `message ${sender}`;
        messageEl.innerHTML = `<div class="message-bubble">${text}</div>`;
        messagesDiv.appendChild(messageEl);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    toggleMicrophone() {
        this.state.isListening = !this.state.isListening;
        const btn = document.getElementById('mic-btn');
        
        if (this.state.isListening) {
            btn.classList.add('listening');
            document.getElementById('voice-status').textContent = 'Listening...';
            this.startListening();
        } else {
            btn.classList.remove('listening');
            document.getElementById('voice-status').textContent = 'Click to start listening';
            this.stopListening();
        }
    }

    startListening() {
        console.log('🎤 Microphone started');
        this.trackAnalytics('microphone_started');
    }

    stopListening() {
        console.log('🎤 Microphone stopped');
        this.trackAnalytics('microphone_stopped');
    }

    changeTheme(theme) {
        this.config.theme = theme;
        document.querySelector('.voice-widget').className = `voice-widget ${theme} ${this.config.position}`;
    }

    clearChat() {
        document.getElementById('chat-messages').innerHTML = '';
        this.state.messages = [];
        this.trackAnalytics('chat_cleared');
    }

    trackAnalytics(event) {
        this.state.analytics.clicks++;
        console.log(`📊 Analytics: ${event}`);
    }
}

// Initialize widget when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.VoiceAssistantWidget = VoiceAssistantWidget;
    });
} else {
    window.VoiceAssistantWidget = VoiceAssistantWidget;
}


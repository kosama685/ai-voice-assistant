# 🎤 Voice Assistant - Complete Setup Guide v2.3

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- Git
- Microphone (for voice input)

### Step 1: Clone & Setup Environment

```bash
cd c:\laragon\www\voice_assistant_app

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Copy environment file
copy .env.example .env
```

### Step 2: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# Optional: Install Whisper for local speech-to-text
pip install openai-whisper

# Optional: Install Coqui TTS for local text-to-speech
pip install TTS
```

### Step 3: Configure APIs

#### Google Gemini API (LLM)
1. Go to https://aistudio.google.com/api-keys
2. Create a new API key
3. Add to `.env`:
   ```
   GEMINI_API_KEY=your_key_here
   ```

#### Google Cloud APIs (Optional)
1. Create a Google Cloud project
2. Enable Speech-to-Text and Text-to-Speech APIs
3. Create a service account and download credentials
4. Add to `.env`:
   ```
   GOOGLE_CLOUD_PROJECT=your_project_id
   GOOGLE_CLOUD_CREDENTIALS=/path/to/credentials.json
   ```

#### ElevenLabs TTS (Optional)
1. Sign up at https://elevenlabs.io
2. Get your API key
3. Add to `.env`:
   ```
   ELEVENLABS_API_KEY=your_key_here
   ```

### Step 4: Database Setup

```bash
# Create database
mysql -u root -p
CREATE DATABASE voiceast;
EXIT;

# Run migrations
flask db upgrade

# Create admin user
python create_admin.py
```

### Step 5: Start the Application

```bash
python run.py
```

Access at: http://127.0.0.1:5000

---

## 📋 Features Overview

### 🎤 Voice Chat
- **Real-time voice input** via microphone
- **Automatic transcription** using Whisper
- **AI-powered responses** using Google Gemini
- **Text-to-speech output** (Coqui/Google/ElevenLabs)
- **Conversation history** with analytics

### 🤖 AI Capabilities
- **Natural language understanding** with Gemini
- **Sentiment analysis** of conversations
- **Named entity extraction** from text
- **Marketing copy generation** for products
- **Context-aware responses** with conversation memory

### 🔊 Speech Processing
- **ASR (Speech-to-Text)**:
  - Local Whisper (free, offline)
  - OpenAI Whisper API (cloud)
  - Google Speech-to-Text (cloud)

- **TTS (Text-to-Speech)**:
  - Coqui TTS (free, local, fast)
  - Google Cloud TTS (high quality)
  - ElevenLabs (premium voices)

### 📊 Analytics & Insights
- Conversation sentiment analysis
- Entity extraction and tracking
- Message statistics
- Usage analytics
- Performance monitoring

---

## 🔌 API Endpoints

### Voice Chat API
```
POST   /api/voice/conversations              # Create conversation
GET    /api/voice/conversations              # List conversations
GET    /api/voice/conversations/:id          # Get conversation
POST   /api/voice/chat/voice                 # Send voice message
POST   /api/voice/chat/text                  # Send text message
GET    /api/voice/conversations/:id/analyze  # Analyze conversation
```

### AI Operations
```
POST   /api/voice/ai/generate                # Generate response
POST   /api/voice/ai/sentiment               # Analyze sentiment
POST   /api/voice/ai/entities                # Extract entities
POST   /api/voice/ai/marketing               # Generate marketing copy
```

### Text-to-Speech
```
POST   /api/voice/tts/synthesize             # Synthesize speech
```

---

## 🎯 Usage Examples

### Python Client Example
```python
import requests

BASE_URL = "http://localhost:5000"
HEADERS = {"Authorization": "Bearer YOUR_TOKEN"}

# Create conversation
response = requests.post(
    f"{BASE_URL}/api/voice/conversations",
    json={"title": "My Chat"},
    headers=HEADERS
)
conversation_id = response.json()['conversation_id']

# Send text message
response = requests.post(
    f"{BASE_URL}/api/voice/chat/text",
    json={
        "conversation_id": conversation_id,
        "text": "Hello, how are you?",
        "synthesize": True
    },
    headers=HEADERS
)

# Get response
data = response.json()
print(data['response_text'])
if data['audio']:
    # Play audio
    import base64
    audio_data = base64.b64decode(data['audio'])
    # Save and play...
```

### JavaScript/Frontend Example
```javascript
// Create conversation
const response = await fetch('/api/voice/conversations', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title: 'My Chat' })
});
const data = await response.json();
const conversationId = data.conversation_id;

// Send text message
const msgResponse = await fetch('/api/voice/chat/text', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        conversation_id: conversationId,
        text: 'Hello!',
        synthesize: true
    })
});

const msgData = await msgResponse.json();
console.log(msgData.response_text);
```

---

## ⚙️ Configuration Options

### AI Settings
- `GEMINI_MODEL`: Model to use (default: gemini-1.5-flash)
- `WHISPER_MODEL`: Whisper model size (base, small, medium, large)
- `WHISPER_USE_LOCAL`: Use local Whisper (true/false)

### TTS Providers (Priority Order)
1. Coqui TTS (local, fastest)
2. Google Cloud TTS (high quality)
3. ElevenLabs (premium voices)

### Feature Flags
- `ENABLE_VOICE_CHAT`: Enable voice input/output
- `ENABLE_AI_RESPONSES`: Enable AI responses
- `ENABLE_ANALYTICS`: Enable analytics tracking
- `ENABLE_PAYMENT`: Enable payment processing

---

## 🐛 Troubleshooting

### Microphone Not Working
```bash
# Check if browser has microphone permission
# Allow microphone access in browser settings
# Test microphone: https://www.onlinemictest.com/
```

### Whisper Not Transcribing
```bash
# Install Whisper
pip install openai-whisper

# Download model
whisper --model base --help

# Test locally
whisper audio.wav --model base
```

### TTS Not Working
```bash
# Try Coqui first (local)
pip install TTS

# Or use Google Cloud TTS
pip install google-cloud-texttospeech

# Or use ElevenLabs
# Set ELEVENLABS_API_KEY in .env
```

### Database Connection Error
```bash
# Check MySQL is running
# Verify credentials in .env
# Create database: CREATE DATABASE voiceast;
```

---

## 📚 Documentation

- **API Documentation**: `/api-sandbox`
- **Widget Demo**: `/widget-demo`
- **Voice Chat**: `/voice-chat`
- **Dashboard**: `/`

---

## 🔐 Security Notes

1. **Never commit `.env` file** - Use `.env.example` as template
2. **Rotate API keys** regularly
3. **Use HTTPS** in production
4. **Validate all inputs** on backend
5. **Rate limit** API endpoints
6. **Encrypt** sensitive data

---

## 📊 Performance Tips

1. Use local Whisper for faster transcription
2. Use Coqui TTS for faster synthesis
3. Cache AI responses when possible
4. Limit conversation history to recent messages
5. Use connection pooling for database

---

## 🚀 Deployment

### Docker
```bash
docker build -t voice-assistant .
docker run -p 5000:5000 voice-assistant
```

### Production Checklist
- [ ] Set `FLASK_ENV=production`
- [ ] Use strong `SECRET_KEY`
- [ ] Enable HTTPS
- [ ] Set up database backups
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Rate limiting
- [ ] CORS configuration

---

## 📞 Support

For issues or questions:
1. Check troubleshooting section
2. Review API documentation
3. Check logs in `/logs` directory
4. Open an issue on GitHub

---

**Version**: 2.3  
**Last Updated**: 2025-10-23  
**Status**: ✅ Production Ready


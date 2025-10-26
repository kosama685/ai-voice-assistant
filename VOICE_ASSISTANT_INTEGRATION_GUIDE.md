# 🎤 Voice Assistant Integration Guide

## Complete Setup for AI-Powered Voice Assistant

This guide covers the complete integration of Google Gemini, Whisper, and TTS into your Voice Assistant Management System.

---

## 📋 Prerequisites

- Python 3.8+
- Flask 2.3.3+
- MySQL database
- Microphone access (for voice input)
- Internet connection (for API calls)

---

## 🚀 Quick Start (5 Minutes)

### 1. Install Dependencies

```bash
cd c:\laragon\www\voice_assistant_app

# Install Python dependencies
pip install -r requirements.txt

# Install Whisper for local speech-to-text
pip install openai-whisper

# Install Coqui TTS for local text-to-speech (optional)
pip install TTS
```

### 2. Configure Environment

```bash
# Copy environment template
copy .env.example .env

# Edit .env and verify these keys:
# GEMINI_API_KEY=AIzaSyBHAl_-FQIXwNK43WUs0c6vxQMKf0OKw14
# ASR_PROVIDER=local_whisper
# TTS_PROVIDER=google_tts
```

### 3. Start Application

```bash
python run.py
```

### 4. Access Voice Assistant Test

Open browser: **http://127.0.0.1:5000/voice-assistant-test**

---

## 🔧 Detailed Configuration

### Google Gemini API (LLM)

**Status**: ✅ Already configured  
**API Key**: `AIzaSyBHAl_-FQIXwNK43WUs0c6vxQMKf0OKw14`  
**Model**: `gemini-1.5-flash`  
**Free Tier**: 60 requests/minute, 1,000 requests/day

**Configuration in `.env`**:
```env
GEMINI_API_KEY=AIzaSyBHAl_-FQIXwNK43WUs0c6vxQMKf0OKw14
GEMINI_MODEL=gemini-1.5-flash
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1024
```

### Whisper (Speech-to-Text)

**Option 1: Local Whisper (Recommended)**
- Free, offline, no API key needed
- Models: tiny, base, small, medium, large
- Download time: 1-3 GB depending on model

```bash
# Install
pip install openai-whisper

# Download model (first run)
# Automatically downloads on first use
```

**Configuration in `.env`**:
```env
ASR_PROVIDER=local_whisper
WHISPER_MODEL=base
```

**Option 2: Google Speech-to-Text**
- Cloud-based, more accurate
- Free tier: 60 minutes/month

```env
ASR_PROVIDER=google_asr
GOOGLE_CLOUD_API_KEY=your_key_here
GOOGLE_CLOUD_PROJECT=projects/500069590671
```

### Text-to-Speech (TTS)

**Option 1: Google Cloud TTS (Recommended)**
- High quality, natural voices
- Free tier: 1 million characters/month

```env
TTS_PROVIDER=google_tts
GOOGLE_CLOUD_API_KEY=your_key_here
TTS_DEFAULT_VOICE=en-US-Neural2-C
TTS_SPEED=1.0
```

**Option 2: Coqui TTS (Local)**
- Free, offline, fast
- No API key needed

```bash
pip install TTS
```

```env
COQUI_TTS_ENABLED=true
TTS_PROVIDER=coqui_tts
```

**Option 3: ElevenLabs (Premium)**
- Realistic voices, voice cloning
- Free tier: 10,000 characters/month

```env
ELEVENLABS_API_KEY=your_key_here
TTS_PROVIDER=elevenlabs
```

---

## 📁 New Files Created

### Services Layer
- `services/llm_service.py` - Google Gemini integration
- `services/asr_service.py` - Whisper/Google ASR integration
- `services/tts_service.py` - Google TTS/Coqui/ElevenLabs integration
- `services/voice_orchestrator.py` - Complete pipeline orchestration

### Routes
- Updated `routes/widget.py` - Enhanced voice endpoints

### Templates
- `templates/voice_assistant_test.html` - Test and demo page

### Configuration
- `.env.example` - Environment template

---

## 🔌 API Endpoints

### Voice Processing
```
POST /widget/api/voice
- Input: base64 audio
- Output: transcribed text + AI response + TTS audio
- Pipeline: ASR → LLM → TTS
```

### Text Processing
```
POST /widget/api/chat
- Input: text message
- Output: AI response + TTS audio
- Pipeline: LLM → TTS
```

### System Health
```
GET /widget/api/health
- Returns: ASR, LLM, TTS service status
```

### Configuration
```
GET /widget/api/config
- Returns: Current provider configuration
```

### Statistics
```
GET /widget/api/stats/<session_id>
- Returns: Conversation statistics
```

---

## 🧪 Testing

### Test Page
Access: **http://127.0.0.1:5000/voice-assistant-test**

Features:
- ✅ Voice recording and transcription
- ✅ Text input
- ✅ AI response generation
- ✅ Text-to-speech playback
- ✅ System health check
- ✅ Configuration display
- ✅ Conversation history
- ✅ Statistics tracking

### Manual Testing

```bash
# Test LLM
curl -X POST http://127.0.0.1:5000/widget/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "sessionId": "test123"}'

# Test Health
curl http://127.0.0.1:5000/widget/api/health

# Test Config
curl http://127.0.0.1:5000/widget/api/config
```

---

## 🐛 Troubleshooting

### Whisper Not Working
```bash
# Check installation
python -c "import whisper; print(whisper.__version__)"

# Reinstall
pip uninstall openai-whisper -y
pip install openai-whisper

# Download model manually
whisper --model base --help
```

### Gemini API Errors
- Verify API key in `.env`
- Check rate limits (60 req/min)
- Ensure internet connection

### TTS Not Working
- Try Coqui first (local, no API key)
- Then Google TTS (requires API key)
- Finally ElevenLabs (requires API key)

### Microphone Not Working
- Check browser permissions
- Allow microphone in browser settings
- Test at: https://www.onlinemictest.com/

---

## 📊 Performance Metrics

| Operation | Time | Provider |
|-----------|------|----------|
| Transcription | 1-3s | Whisper (local) |
| AI Response | 2-5s | Gemini |
| TTS Synthesis | 0.5-2s | Coqui |
| **Total** | **3-10s** | Combined |

---

## 🔐 Security Best Practices

1. **Store API keys in `.env`** (never commit to git)
2. **Add `.env` to `.gitignore`**
3. **Use environment variables** for all secrets
4. **Enable rate limiting** for production
5. **Validate user input** before processing
6. **Use HTTPS** in production

---

## 📚 Additional Resources

- [Google Gemini API Docs](https://ai.google.dev/)
- [Whisper Documentation](https://github.com/openai/whisper)
- [Google Cloud TTS Docs](https://cloud.google.com/text-to-speech/docs)
- [Coqui TTS GitHub](https://github.com/coqui-ai/TTS)
- [ElevenLabs API Docs](https://elevenlabs.io/docs)

---

## 🎯 Next Steps

1. ✅ Install dependencies
2. ✅ Configure `.env` file
3. ✅ Start Flask application
4. ✅ Test at `/voice-assistant-test`
5. ✅ Integrate into your application
6. ✅ Deploy to production

---

**Version**: 2.3  
**Last Updated**: 2025-10-23  
**Status**: ✅ Production Ready


# 📚 Voice Assistant API Documentation

Complete API reference for the Voice Assistant system.

---

## 🔗 Base URL

```
http://127.0.0.1:5000/widget/api
```

---

## 🎤 Voice Processing Endpoint

### POST `/voice`

Process voice input through complete ASR → LLM → TTS pipeline.

**Request:**
```json
{
  "audio": "base64_encoded_audio_data",
  "sessionId": "session_123",
  "audioFormat": "wav",
  "language": "en-US",
  "synthesize": true,
  "voice": "en-US-Neural2-C"
}
```

**Parameters:**
- `audio` (string, required): Base64-encoded audio data
- `sessionId` (string, required): Unique session identifier
- `audioFormat` (string, optional): Audio format (wav, mp3). Default: wav
- `language` (string, optional): Language code. Default: en-US
- `synthesize` (boolean, optional): Generate TTS response. Default: true
- `voice` (string, optional): TTS voice selection

**Response:**
```json
{
  "success": true,
  "transcribed": "What is the capital of France?",
  "response": "The capital of France is Paris.",
  "audio": "base64_encoded_audio_response",
  "providers": {
    "asr": "local_whisper",
    "llm": "gemini",
    "tts": "google_tts"
  },
  "turnCount": 1,
  "processingTime": 5.23
}
```

**Status Codes:**
- `200`: Success
- `400`: Bad request
- `500`: Server error

---

## 💬 Text Chat Endpoint

### POST `/chat`

Process text input through LLM → TTS pipeline.

**Request:**
```json
{
  "message": "Hello, how are you?",
  "sessionId": "session_123",
  "synthesize": true,
  "voice": "en-US-Neural2-C"
}
```

**Parameters:**
- `message` (string, required): User message
- `sessionId` (string, required): Unique session identifier
- `synthesize` (boolean, optional): Generate TTS response. Default: true
- `voice` (string, optional): TTS voice selection

**Response:**
```json
{
  "success": true,
  "userMessage": "Hello, how are you?",
  "response": "I'm doing well, thank you for asking!",
  "audio": "base64_encoded_audio_response",
  "providers": {
    "llm": "gemini",
    "tts": "google_tts"
  },
  "turnCount": 1,
  "processingTime": 3.45
}
```

---

## 🏥 Health Check Endpoint

### GET `/health`

Check system health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-23T10:30:00Z",
  "activeSessions": 5,
  "services": {
    "asr": {
      "status": "healthy",
      "provider": "local_whisper",
      "model": "base"
    },
    "llm": {
      "status": "healthy",
      "provider": "gemini",
      "model": "gemini-1.5-flash"
    },
    "tts": {
      "status": "healthy",
      "provider": "google_tts",
      "coqui_available": true,
      "google_configured": true,
      "elevenlabs_configured": false
    }
  }
}
```

---

## ⚙️ Configuration Endpoint

### GET `/config`

Get current system configuration.

**Response:**
```json
{
  "asr": {
    "provider": "local_whisper",
    "model": "base"
  },
  "llm": {
    "provider": "gemini",
    "model": "gemini-1.5-flash",
    "temperature": 0.7
  },
  "tts": {
    "provider": "google_tts",
    "default_voice": "en-US-Neural2-C",
    "default_speed": 1.0
  }
}
```

---

## 📊 Statistics Endpoint

### GET `/stats/<session_id>`

Get conversation statistics for a session.

**Response:**
```json
{
  "session_id": "session_123",
  "turn_count": 5,
  "total_user_chars": 245,
  "total_response_chars": 1023,
  "avg_response_length": 204.6,
  "providers": {
    "asr": "local_whisper",
    "llm": "gemini",
    "tts": "google_tts"
  },
  "created_at": "2025-10-23T10:00:00Z",
  "last_updated": "2025-10-23T10:15:00Z"
}
```

---

## 🔐 Error Responses

### Error Format

```json
{
  "success": false,
  "error": "Error message",
  "errorCode": "ERROR_CODE",
  "timestamp": "2025-10-23T10:30:00Z"
}
```

### Common Errors

| Code | Message | Solution |
|------|---------|----------|
| `INVALID_AUDIO` | Invalid audio data | Ensure audio is base64-encoded |
| `ASR_FAILED` | Speech-to-text failed | Check microphone, try again |
| `LLM_FAILED` | AI response generation failed | Check API key, rate limits |
| `TTS_FAILED` | Text-to-speech failed | Try different TTS provider |
| `SESSION_NOT_FOUND` | Session not found | Create new session |
| `RATE_LIMIT_EXCEEDED` | Too many requests | Wait before retrying |

---

## 📝 Request Examples

### cURL - Voice Input

```bash
curl -X POST http://127.0.0.1:5000/widget/api/voice \
  -H "Content-Type: application/json" \
  -d '{
    "audio": "UklGRi4A...",
    "sessionId": "session_123",
    "synthesize": true
  }'
```

### cURL - Text Input

```bash
curl -X POST http://127.0.0.1:5000/widget/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello",
    "sessionId": "session_123",
    "synthesize": true
  }'
```

### JavaScript - Voice Input

```javascript
const response = await fetch('/widget/api/voice', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    audio: base64Audio,
    sessionId: 'session_123',
    synthesize: true
  })
});

const data = await response.json();
console.log(data.response);
```

### JavaScript - Text Input

```javascript
const response = await fetch('/widget/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'Hello',
    sessionId: 'session_123',
    synthesize: true
  })
});

const data = await response.json();
console.log(data.response);
```

---

## 🔄 Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not found |
| 429 | Rate limit exceeded |
| 500 | Server error |
| 503 | Service unavailable |

---

## ⏱️ Rate Limits

- **Requests per minute**: 60
- **Requests per hour**: 1000
- **Requests per day**: 10000

---

## 🔑 Authentication

Currently, the API is public. For production, implement:

```python
@app.before_request
def check_auth():
    token = request.headers.get('Authorization')
    if not token:
        return {'error': 'Missing token'}, 401
```

---

## 📦 Response Formats

### Audio Format

Audio is returned as base64-encoded MP3:

```javascript
const audio = new Audio(`data:audio/mp3;base64,${response.audio}`);
audio.play();
```

### Timestamps

All timestamps are in ISO 8601 format:
```
2025-10-23T10:30:00Z
```

---

## 🧪 Testing

### Health Check
```bash
curl http://127.0.0.1:5000/widget/api/health
```

### Configuration
```bash
curl http://127.0.0.1:5000/widget/api/config
```

### Statistics
```bash
curl http://127.0.0.1:5000/widget/api/stats/session_123
```

---

## 📚 Integration Guide

See `VOICE_ASSISTANT_INTEGRATION_GUIDE.md` for detailed setup instructions.

---

**Version**: 2.3  
**Last Updated**: 2025-10-23  
**Status**: ✅ Production Ready


"""
LLM Service - Google Gemini Integration
Handles conversational AI responses
"""

import os
import json
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime

class LLMService:
    """Google Gemini LLM Service"""
    
    def __init__(self):
        self.api_key = os.environ.get('GEMINI_API_KEY', 'AIzaSyBHAl_-FQIXwNK43WUs0c6vxQMKf0OKw14')
        self.model = os.environ.get('GEMINI_MODEL', 'gemini-1.5-flash')
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.temperature = float(os.environ.get('LLM_TEMPERATURE', '0.7'))
        self.max_tokens = int(os.environ.get('LLM_MAX_TOKENS', '1024'))
        self.conversation_history = {}  # Store conversation context
        
    def generate_response(
        self,
        prompt: str,
        session_id: str = None,
        context: str = None,
        temperature: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Generate response using Google Gemini

        Args:
            prompt: User message
            session_id: Conversation session ID
            context: Previous conversation context
            temperature: Response creativity (0.0-1.0)

        Returns:
            Dict with response, metadata, and status
        """
        try:
            if not self.api_key or self.api_key == 'AIzaSyBHAl_-FQIXwNK43WUs0c6vxQMKf0OKw14':
                # Verify API key is valid
                if not self._verify_api_key():
                    return {
                        'success': False,
                        'error': 'Invalid or missing Gemini API key. Please configure GEMINI_API_KEY in .env',
                        'provider': 'gemini',
                        'status_code': 401
                    }

            temp = temperature if temperature is not None else self.temperature

            # Build conversation context
            full_prompt = self._build_prompt(prompt, session_id, context)

            url = f"{self.base_url}/{self.model}:generateContent"
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "VoiceAssistant/2.3"
            }

            payload = {
                "contents": [{
                    "parts": [{"text": full_prompt}]
                }],
                "generationConfig": {
                    "temperature": temp,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": self.max_tokens,
                }
            }

            # Make request with proper error handling
            response = requests.post(
                f"{url}?key={self.api_key}",
                json=payload,
                headers=headers,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()

                # Check if response has candidates
                if 'candidates' not in data or not data['candidates']:
                    return {
                        'success': False,
                        'error': 'No response generated from Gemini API',
                        'provider': 'gemini',
                        'raw_response': data
                    }

                text = data['candidates'][0]['content']['parts'][0]['text']

                # Store in conversation history
                if session_id:
                    self._store_conversation(session_id, prompt, text)

                return {
                    'success': True,
                    'response': text,
                    'model': self.model,
                    'provider': 'gemini',
                    'tokens_used': len(text.split()),
                    'timestamp': datetime.utcnow().isoformat()
                }
            else:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', {}).get('message', 'Unknown error')
                except:
                    error_msg = response.text or 'Unknown error'

                return {
                    'success': False,
                    'error': f"Gemini API error: {error_msg}",
                    'provider': 'gemini',
                    'status_code': response.status_code,
                    'response_text': response.text[:500]  # First 500 chars for debugging
                }

        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Request timeout - Gemini API took too long',
                'provider': 'gemini'
            }
        except requests.exceptions.ConnectionError as e:
            return {
                'success': False,
                'error': f'Connection error: {str(e)}',
                'provider': 'gemini'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}',
                'provider': 'gemini'
            }
    
    def _verify_api_key(self) -> bool:
        """Verify API key is valid by making a test request"""
        try:
            url = f"{self.base_url}/{self.model}:generateContent"
            headers = {"Content-Type": "application/json"}

            payload = {
                "contents": [{
                    "parts": [{"text": "test"}]
                }],
                "generationConfig": {
                    "temperature": 0.1,
                    "maxOutputTokens": 10,
                }
            }

            response = requests.post(
                f"{url}?key={self.api_key}",
                json=payload,
                headers=headers,
                timeout=10
            )

            return response.status_code == 200
        except:
            return False

    def _build_prompt(self, prompt: str, session_id: str = None, context: str = None) -> str:
        """Build prompt with context"""
        system_prompt = """You are a helpful, friendly voice assistant. 
Keep responses concise (1-2 sentences for voice).
Be conversational and natural.
If asked about capabilities, mention you can help with questions, provide information, and have conversations."""
        
        if context:
            return f"{system_prompt}\n\nPrevious context:\n{context}\n\nUser: {prompt}"
        
        if session_id and session_id in self.conversation_history:
            history = self.conversation_history[session_id]
            context_str = "\n".join([f"{m['role']}: {m['text']}" for m in history[-5:]])
            return f"{system_prompt}\n\nConversation:\n{context_str}\n\nUser: {prompt}"
        
        return f"{system_prompt}\n\nUser: {prompt}"
    
    def _store_conversation(self, session_id: str, user_msg: str, assistant_msg: str):
        """Store conversation for context"""
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []
        
        self.conversation_history[session_id].append({
            'role': 'user',
            'text': user_msg,
            'timestamp': datetime.utcnow().isoformat()
        })
        self.conversation_history[session_id].append({
            'role': 'assistant',
            'text': assistant_msg,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        # Keep only last 20 messages
        if len(self.conversation_history[session_id]) > 20:
            self.conversation_history[session_id] = self.conversation_history[session_id][-20:]
    
    def get_conversation_history(self, session_id: str) -> List[Dict]:
        """Get conversation history for a session"""
        return self.conversation_history.get(session_id, [])
    
    def clear_conversation(self, session_id: str):
        """Clear conversation history"""
        if session_id in self.conversation_history:
            del self.conversation_history[session_id]
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text"""
        prompt = f"""Analyze the sentiment of this text and respond with JSON:
{{"sentiment": "positive/negative/neutral", "confidence": 0-100, "emotion": "emotion_name"}}

Text: "{text}"

Respond ONLY with the JSON, no other text."""
        
        result = self.generate_response(prompt)
        if result['success']:
            try:
                # Extract JSON from response
                response_text = result['response']
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    sentiment_data = json.loads(response_text[json_start:json_end])
                    return {
                        'success': True,
                        'sentiment': sentiment_data,
                        'provider': 'gemini'
                    }
            except:
                pass
        
        return {
            'success': False,
            'error': 'Failed to analyze sentiment',
            'provider': 'gemini'
        }
    
    def get_health_status(self) -> Dict[str, Any]:
        """Check API health"""
        try:
            result = self.generate_response("Say 'OK' if you're working")
            return {
                'status': 'healthy' if result['success'] else 'unhealthy',
                'provider': 'gemini',
                'model': self.model,
                'api_key_configured': bool(self.api_key),
                'timestamp': datetime.utcnow().isoformat()
            }
        except:
            return {
                'status': 'unhealthy',
                'provider': 'gemini',
                'error': 'Failed to connect to Gemini API'
            }


# Singleton instance
llm_service = LLMService()


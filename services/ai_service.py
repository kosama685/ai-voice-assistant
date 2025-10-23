"""
AI Service Module - Handles all AI/LLM operations
Integrates: Google Gemini, OpenAI Whisper, Google TTS, ElevenLabs, Coqui TTS
"""

import os
import json
import base64
import requests
from typing import Optional, Dict, Any
from config import Config

class AIService:
    """Main AI Service for LLM, ASR, and TTS operations"""
    
    def __init__(self):
        self.gemini_api_key = Config.GEMINI_API_KEY
        self.gemini_model = Config.GEMINI_MODEL
        self.gemini_base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        
    # ============ LLM / CHAT OPERATIONS ============
    
    def generate_response(self, prompt: str, context: str = "", temperature: float = 0.7) -> Dict[str, Any]:
        """
        Generate AI response using Google Gemini
        
        Args:
            prompt: User message/prompt
            context: Optional conversation context
            temperature: Response creativity (0.0-1.0)
            
        Returns:
            Dict with response, tokens, and metadata
        """
        try:
            full_prompt = f"{context}\n\nUser: {prompt}" if context else prompt
            
            url = f"{self.gemini_base_url}/{self.gemini_model}:generateContent"
            headers = {"Content-Type": "application/json"}
            
            payload = {
                "contents": [{
                    "parts": [{"text": full_prompt}]
                }],
                "generationConfig": {
                    "temperature": temperature,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 1024,
                }
            }
            
            response = requests.post(
                f"{url}?key={self.gemini_api_key}",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                text = data['candidates'][0]['content']['parts'][0]['text']
                return {
                    'success': True,
                    'response': text,
                    'model': self.gemini_model,
                    'tokens_used': len(text.split()),
                    'provider': 'gemini'
                }
            else:
                return {
                    'success': False,
                    'error': f"Gemini API error: {response.status_code}",
                    'provider': 'gemini'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'provider': 'gemini'
            }
    
    def generate_marketing_copy(self, product_name: str, features: list) -> Dict[str, Any]:
        """Generate marketing copy for a product"""
        features_text = ", ".join(features)
        prompt = f"""Create compelling marketing copy for:
Product: {product_name}
Features: {features_text}

Generate:
1. Catchy headline
2. 2-3 sentence description
3. 3 key benefits
4. Call-to-action

Format as JSON."""
        
        return self.generate_response(prompt, temperature=0.8)
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text"""
        prompt = f"""Analyze the sentiment of this text and provide:
1. Sentiment (positive/negative/neutral)
2. Confidence (0-100)
3. Key emotions detected
4. Brief explanation

Text: "{text}"

Respond in JSON format."""
        
        return self.generate_response(prompt, temperature=0.3)
    
    def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract named entities from text"""
        prompt = f"""Extract named entities from this text:
- People
- Organizations
- Locations
- Products
- Dates

Text: "{text}"

Respond in JSON format with entity type as key and list of entities as value."""
        
        return self.generate_response(prompt, temperature=0.2)
    
    # ============ VOICE PROCESSING ============
    
    def transcribe_audio(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Transcribe audio using Whisper (local or API)
        
        Args:
            audio_file_path: Path to audio file
            
        Returns:
            Dict with transcription and metadata
        """
        try:
            if Config.WHISPER_USE_LOCAL:
                return self._transcribe_local_whisper(audio_file_path)
            else:
                return self._transcribe_openai_whisper(audio_file_path)
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'provider': 'whisper'
            }
    
    def _transcribe_local_whisper(self, audio_file_path: str) -> Dict[str, Any]:
        """Transcribe using local Whisper (requires whisper.cpp or similar)"""
        try:
            import subprocess
            result = subprocess.run(
                ['whisper', audio_file_path, '--model', Config.WHISPER_MODEL, '--output_format', 'json'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                output = json.loads(result.stdout)
                return {
                    'success': True,
                    'text': output.get('text', ''),
                    'language': output.get('language', 'en'),
                    'provider': 'whisper_local'
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr,
                    'provider': 'whisper_local'
                }
        except Exception as e:
            return {
                'success': False,
                'error': f"Local Whisper error: {str(e)}",
                'provider': 'whisper_local'
            }
    
    def _transcribe_openai_whisper(self, audio_file_path: str) -> Dict[str, Any]:
        """Transcribe using OpenAI Whisper API"""
        try:
            with open(audio_file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(
                    'https://api.openai.com/v1/audio/transcriptions',
                    files=files,
                    data={'model': 'whisper-1'},
                    headers={'Authorization': f'Bearer {os.environ.get("OPENAI_API_KEY", "")}'},
                    timeout=60
                )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'text': data.get('text', ''),
                    'provider': 'whisper_api'
                }
            else:
                return {
                    'success': False,
                    'error': f"Whisper API error: {response.status_code}",
                    'provider': 'whisper_api'
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'provider': 'whisper_api'
            }
    
    # ============ TEXT-TO-SPEECH ============
    
    def synthesize_speech(self, text: str, voice: str = "default") -> Dict[str, Any]:
        """
        Synthesize speech from text
        Tries: Coqui (local) -> Google TTS -> ElevenLabs
        
        Args:
            text: Text to synthesize
            voice: Voice identifier
            
        Returns:
            Dict with audio data (base64) and metadata
        """
        # Try Coqui first (local, fastest)
        if Config.COQUI_TTS_ENABLED:
            result = self._synthesize_coqui(text)
            if result['success']:
                return result
        
        # Try Google TTS
        if Config.GOOGLE_TTS_ENABLED:
            result = self._synthesize_google_tts(text, voice)
            if result['success']:
                return result
        
        # Try ElevenLabs
        if Config.ELEVENLABS_API_KEY:
            result = self._synthesize_elevenlabs(text, voice)
            if result['success']:
                return result
        
        return {
            'success': False,
            'error': 'No TTS provider available',
            'provider': 'none'
        }
    
    def _synthesize_coqui(self, text: str) -> Dict[str, Any]:
        """Synthesize using Coqui TTS (local)"""
        try:
            from TTS.api import TTS
            tts = TTS(Config.COQUI_TTS_MODEL, gpu=False)
            output_path = "/tmp/coqui_output.wav"
            tts.tts_to_file(text=text, file_path=output_path)
            
            with open(output_path, 'rb') as f:
                audio_data = base64.b64encode(f.read()).decode('utf-8')
            
            return {
                'success': True,
                'audio': audio_data,
                'provider': 'coqui_tts',
                'format': 'wav'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'provider': 'coqui_tts'
            }
    
    def _synthesize_google_tts(self, text: str, voice: str = "en-US-Neural2-C") -> Dict[str, Any]:
        """Synthesize using Google Cloud TTS"""
        try:
            from google.cloud import texttospeech
            client = texttospeech.TextToSpeechClient()
            
            synthesis_input = texttospeech.SynthesisInput(text=text)
            voice_obj = texttospeech.VoiceSelectionParams(
                language_code="en-US",
                name=voice
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            
            response = client.synthesize_speech(
                input=synthesis_input,
                voice=voice_obj,
                audio_config=audio_config
            )
            
            audio_data = base64.b64encode(response.audio_content).decode('utf-8')
            return {
                'success': True,
                'audio': audio_data,
                'provider': 'google_tts',
                'format': 'mp3'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'provider': 'google_tts'
            }
    
    def _synthesize_elevenlabs(self, text: str, voice_id: str = None) -> Dict[str, Any]:
        """Synthesize using ElevenLabs TTS"""
        try:
            voice_id = voice_id or Config.ELEVENLABS_VOICE_ID
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            
            headers = {
                "xi-api-key": Config.ELEVENLABS_API_KEY,
                "Content-Type": "application/json"
            }
            
            payload = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                audio_data = base64.b64encode(response.content).decode('utf-8')
                return {
                    'success': True,
                    'audio': audio_data,
                    'provider': 'elevenlabs',
                    'format': 'mp3'
                }
            else:
                return {
                    'success': False,
                    'error': f"ElevenLabs error: {response.status_code}",
                    'provider': 'elevenlabs'
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'provider': 'elevenlabs'
            }


# Singleton instance
ai_service = AIService()


"""
TTS Service - Text-to-Speech Integration
Supports Google Cloud TTS, Coqui TTS, and ElevenLabs
"""

import os
import io
import base64
import requests
from typing import Dict, Any, Optional
from datetime import datetime

class TTSService:
    """Text-to-Speech Service"""
    
    def __init__(self):
        self.provider = os.environ.get('TTS_PROVIDER', 'google_tts')
        self.google_api_key = os.environ.get('GOOGLE_CLOUD_API_KEY', '')
        self.elevenlabs_api_key = os.environ.get('ELEVENLABS_API_KEY', '')
        self.coqui_enabled = os.environ.get('COQUI_TTS_ENABLED', 'true').lower() == 'true'
        self.default_voice = os.environ.get('TTS_DEFAULT_VOICE', 'en-US-Neural2-C')
        self.default_speed = float(os.environ.get('TTS_SPEED', '1.0'))
        
        # Try to import Coqui TTS if enabled
        self.tts_model = None
        if self.coqui_enabled:
            try:
                from TTS.api import TTS
                self.tts_model = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", gpu=False)
                print("✅ Coqui TTS model loaded successfully")
            except ImportError:
                print("⚠️ Coqui TTS not installed. Install with: pip install TTS")
            except Exception as e:
                print(f"⚠️ Failed to load Coqui TTS: {e}")
    
    def synthesize(
        self,
        text: str,
        voice: Optional[str] = None,
        speed: Optional[float] = None,
        language: str = 'en-US'
    ) -> Dict[str, Any]:
        """
        Synthesize text to speech
        
        Args:
            text: Text to synthesize
            voice: Voice name/ID
            speed: Speech speed (0.5-2.0)
            language: Language code
            
        Returns:
            Dict with audio data (base64) and metadata
        """
        voice = voice or self.default_voice
        speed = speed or self.default_speed
        
        # Try providers in order
        if self.coqui_enabled:
            result = self._synthesize_coqui(text, speed)
            if result['success']:
                return result
        
        if self.provider == 'google_tts' or self.google_api_key:
            result = self._synthesize_google_tts(text, voice, speed, language)
            if result['success']:
                return result
        
        if self.elevenlabs_api_key:
            result = self._synthesize_elevenlabs(text, voice)
            if result['success']:
                return result
        
        return {
            'success': False,
            'error': 'No TTS provider available',
            'provider': self.provider
        }
    
    def _synthesize_coqui(self, text: str, speed: float = 1.0) -> Dict[str, Any]:
        """Synthesize using Coqui TTS (local)"""
        try:
            if not self.tts_model:
                return {
                    'success': False,
                    'error': 'Coqui TTS model not loaded',
                    'provider': 'coqui_tts'
                }
            
            # Synthesize
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
                tmp_path = tmp.name
            
            try:
                self.tts_model.tts_to_file(text=text, file_path=tmp_path)
                
                # Read audio file
                with open(tmp_path, 'rb') as f:
                    audio_data = f.read()
                
                # Encode to base64
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                
                return {
                    'success': True,
                    'audio': audio_base64,
                    'audio_format': 'wav',
                    'provider': 'coqui_tts',
                    'model': 'tacotron2-DDC',
                    'timestamp': datetime.utcnow().isoformat()
                }
            finally:
                import os as os_module
                if os_module.path.exists(tmp_path):
                    os_module.remove(tmp_path)
                    
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'provider': 'coqui_tts'
            }
    
    def _synthesize_google_tts(
        self,
        text: str,
        voice: str,
        speed: float,
        language: str
    ) -> Dict[str, Any]:
        """Synthesize using Google Cloud TTS"""
        try:
            if not self.google_api_key:
                return {
                    'success': False,
                    'error': 'Google API key not configured',
                    'provider': 'google_tts'
                }
            
            url = "https://texttospeech.googleapis.com/v1/text:synthesize"
            
            payload = {
                "input": {"text": text},
                "voice": {
                    "languageCode": language,
                    "name": voice
                },
                "audioConfig": {
                    "audioEncoding": "MP3",
                    "pitch": 0.0,
                    "speakingRate": speed
                }
            }
            
            response = requests.post(
                f"{url}?key={self.google_api_key}",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                audio_content = data.get('audioContent', '')
                
                return {
                    'success': True,
                    'audio': audio_content,
                    'audio_format': 'mp3',
                    'provider': 'google_tts',
                    'voice': voice,
                    'timestamp': datetime.utcnow().isoformat()
                }
            else:
                error_msg = response.json().get('error', {}).get('message', 'Unknown error')
                return {
                    'success': False,
                    'error': f"Google TTS error: {error_msg}",
                    'provider': 'google_tts',
                    'status_code': response.status_code
                }
                
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Request timeout - Google TTS took too long',
                'provider': 'google_tts'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'provider': 'google_tts'
            }
    
    def _synthesize_elevenlabs(self, text: str, voice: str = 'Bella') -> Dict[str, Any]:
        """Synthesize using ElevenLabs"""
        try:
            if not self.elevenlabs_api_key:
                return {
                    'success': False,
                    'error': 'ElevenLabs API key not configured',
                    'provider': 'elevenlabs'
                }
            
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"
            headers = {
                "xi-api-key": self.elevenlabs_api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "text": text,
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                audio_base64 = base64.b64encode(response.content).decode('utf-8')
                
                return {
                    'success': True,
                    'audio': audio_base64,
                    'audio_format': 'mp3',
                    'provider': 'elevenlabs',
                    'voice': voice,
                    'timestamp': datetime.utcnow().isoformat()
                }
            else:
                return {
                    'success': False,
                    'error': f"ElevenLabs error: {response.text}",
                    'provider': 'elevenlabs',
                    'status_code': response.status_code
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'provider': 'elevenlabs'
            }
    
    def get_health_status(self) -> Dict[str, Any]:
        """Check TTS service health"""
        return {
            'status': 'healthy',
            'provider': self.provider,
            'coqui_available': bool(self.tts_model),
            'google_configured': bool(self.google_api_key),
            'elevenlabs_configured': bool(self.elevenlabs_api_key),
            'timestamp': datetime.utcnow().isoformat()
        }


# Singleton instance
tts_service = TTSService()


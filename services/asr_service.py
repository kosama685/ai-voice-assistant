"""
ASR Service - Speech-to-Text Integration
Supports Whisper (local/API) and Google Speech-to-Text
"""

import os
import io
import json
import base64
import requests
from typing import Dict, Any, Optional
from datetime import datetime

class ASRService:
    """Automatic Speech Recognition Service"""
    
    def __init__(self):
        self.provider = os.environ.get('ASR_PROVIDER', 'local_whisper')
        self.whisper_model = os.environ.get('WHISPER_MODEL', 'base')
        self.google_api_key = os.environ.get('GOOGLE_CLOUD_API_KEY', '')
        self.google_project = os.environ.get('GOOGLE_CLOUD_PROJECT', '')
        
        # Try to import whisper if using local
        self.whisper = None
        if self.provider == 'local_whisper':
            try:
                import whisper
                self.whisper = whisper
                self.model = whisper.load_model(self.whisper_model)
                print(f"✅ Whisper model '{self.whisper_model}' loaded successfully")
            except ImportError:
                print("⚠️ Whisper not installed. Install with: pip install openai-whisper")
            except Exception as e:
                print(f"⚠️ Failed to load Whisper model: {e}")
    
    def transcribe(
        self,
        audio_data: bytes,
        audio_format: str = 'wav',
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Transcribe audio to text
        
        Args:
            audio_data: Audio bytes
            audio_format: Audio format (wav, mp3, etc.)
            language: Language code (optional)
            
        Returns:
            Dict with transcribed text and metadata
        """
        if self.provider == 'local_whisper':
            return self._transcribe_local_whisper(audio_data, language)
        elif self.provider == 'google_asr':
            return self._transcribe_google_asr(audio_data, language)
        else:
            return {
                'success': False,
                'error': f'Unknown ASR provider: {self.provider}',
                'provider': self.provider
            }
    
    def _transcribe_local_whisper(
        self,
        audio_data: bytes,
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        """Transcribe using local Whisper"""
        try:
            if not self.whisper or not self.model:
                return {
                    'success': False,
                    'error': 'Whisper model not loaded',
                    'provider': 'local_whisper'
                }
            
            # Save audio to temporary file
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
                tmp.write(audio_data)
                tmp_path = tmp.name
            
            try:
                # Transcribe
                result = self.model.transcribe(
                    tmp_path,
                    language=language,
                    verbose=False
                )
                
                text = result.get('text', '').strip()
                
                return {
                    'success': True,
                    'text': text,
                    'language': result.get('language', 'unknown'),
                    'provider': 'local_whisper',
                    'model': self.whisper_model,
                    'confidence': 0.95,  # Whisper doesn't provide confidence
                    'timestamp': datetime.utcnow().isoformat()
                }
            finally:
                # Clean up temp file
                import os as os_module
                if os_module.path.exists(tmp_path):
                    os_module.remove(tmp_path)
                    
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'provider': 'local_whisper'
            }
    
    def _transcribe_google_asr(
        self,
        audio_data: bytes,
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        """Transcribe using Google Speech-to-Text API"""
        try:
            if not self.google_api_key:
                return {
                    'success': False,
                    'error': 'Google API key not configured',
                    'provider': 'google_asr'
                }
            
            # Encode audio to base64
            audio_content = base64.b64encode(audio_data).decode('utf-8')
            
            url = f"https://speech.googleapis.com/v1/speech:recognize?key={self.google_api_key}"
            
            payload = {
                "config": {
                    "encoding": "LINEAR16",
                    "sampleRateHertz": 16000,
                    "languageCode": language or "en-US",
                    "enableAutomaticPunctuation": True,
                },
                "audio": {
                    "content": audio_content
                }
            }
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                if results:
                    text = results[0]['alternatives'][0]['transcript']
                    confidence = results[0]['alternatives'][0].get('confidence', 0)
                    
                    return {
                        'success': True,
                        'text': text,
                        'language': language or 'en-US',
                        'provider': 'google_asr',
                        'confidence': confidence,
                        'timestamp': datetime.utcnow().isoformat()
                    }
                else:
                    return {
                        'success': False,
                        'error': 'No speech detected',
                        'provider': 'google_asr'
                    }
            else:
                error_msg = response.json().get('error', {}).get('message', 'Unknown error')
                return {
                    'success': False,
                    'error': f"Google ASR error: {error_msg}",
                    'provider': 'google_asr',
                    'status_code': response.status_code
                }
                
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Request timeout - Google ASR took too long',
                'provider': 'google_asr'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'provider': 'google_asr'
            }
    
    def get_health_status(self) -> Dict[str, Any]:
        """Check ASR service health"""
        if self.provider == 'local_whisper':
            return {
                'status': 'healthy' if self.model else 'unhealthy',
                'provider': 'local_whisper',
                'model': self.whisper_model,
                'timestamp': datetime.utcnow().isoformat()
            }
        else:
            return {
                'status': 'healthy' if self.google_api_key else 'unhealthy',
                'provider': 'google_asr',
                'api_key_configured': bool(self.google_api_key),
                'timestamp': datetime.utcnow().isoformat()
            }


# Singleton instance
asr_service = ASRService()


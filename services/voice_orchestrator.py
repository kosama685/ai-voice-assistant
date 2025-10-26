"""
Voice Orchestrator Service
Orchestrates ASR -> LLM -> TTS pipeline
"""

import os
from typing import Dict, Any, Optional
from datetime import datetime
from .llm_service import llm_service
from .asr_service import asr_service
from .tts_service import tts_service

class VoiceOrchestrator:
    """Orchestrates complete voice conversation pipeline"""
    
    def __init__(self):
        self.llm_service = llm_service
        self.asr_service = asr_service
        self.tts_service = tts_service
        self.conversation_stats = {}
    
    def process_voice_input(
        self,
        audio_data: bytes,
        session_id: str,
        audio_format: str = 'wav',
        language: Optional[str] = None,
        synthesize_response: bool = True,
        voice: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Complete voice processing pipeline:
        1. Transcribe audio (ASR)
        2. Generate response (LLM)
        3. Synthesize response (TTS)
        
        Args:
            audio_data: Audio bytes
            session_id: Conversation session ID
            audio_format: Audio format
            language: Language code
            synthesize_response: Whether to synthesize TTS
            voice: Voice for TTS
            
        Returns:
            Dict with transcribed text, response, and audio
        """
        try:
            # Step 1: Transcribe audio
            transcription = self.asr_service.transcribe(
                audio_data,
                audio_format=audio_format,
                language=language
            )
            
            if not transcription['success']:
                return {
                    'success': False,
                    'error': f"Transcription failed: {transcription['error']}",
                    'stage': 'asr'
                }
            
            user_text = transcription['text']
            
            # Step 2: Generate LLM response
            llm_response = self.llm_service.generate_response(
                user_text,
                session_id=session_id
            )
            
            if not llm_response['success']:
                return {
                    'success': False,
                    'error': f"LLM failed: {llm_response['error']}",
                    'stage': 'llm',
                    'transcribed_text': user_text
                }
            
            response_text = llm_response['response']
            
            # Step 3: Synthesize response (optional)
            audio_response = None
            if synthesize_response:
                tts_result = self.tts_service.synthesize(
                    response_text,
                    voice=voice
                )
                
                if tts_result['success']:
                    audio_response = tts_result['audio']
            
            # Update stats
            self._update_stats(session_id, user_text, response_text)
            
            return {
                'success': True,
                'transcribed_text': user_text,
                'response_text': response_text,
                'audio_response': audio_response,
                'asr_provider': transcription['provider'],
                'llm_provider': llm_response['provider'],
                'tts_provider': tts_result['provider'] if synthesize_response else None,
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'stage': 'orchestration'
            }
    
    def process_text_input(
        self,
        text: str,
        session_id: str,
        synthesize_response: bool = True,
        voice: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process text input (skip ASR):
        1. Generate response (LLM)
        2. Synthesize response (TTS)
        
        Args:
            text: User text
            session_id: Conversation session ID
            synthesize_response: Whether to synthesize TTS
            voice: Voice for TTS
            
        Returns:
            Dict with response and audio
        """
        try:
            # Step 1: Generate LLM response
            llm_response = self.llm_service.generate_response(
                text,
                session_id=session_id
            )
            
            if not llm_response['success']:
                return {
                    'success': False,
                    'error': f"LLM failed: {llm_response['error']}",
                    'stage': 'llm'
                }
            
            response_text = llm_response['response']
            
            # Step 2: Synthesize response (optional)
            audio_response = None
            tts_provider = None
            if synthesize_response:
                tts_result = self.tts_service.synthesize(
                    response_text,
                    voice=voice
                )
                
                if tts_result['success']:
                    audio_response = tts_result['audio']
                    tts_provider = tts_result['provider']
            
            # Update stats
            self._update_stats(session_id, text, response_text)
            
            return {
                'success': True,
                'user_text': text,
                'response_text': response_text,
                'audio_response': audio_response,
                'llm_provider': llm_response['provider'],
                'tts_provider': tts_provider,
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'stage': 'orchestration'
            }
    
    def _update_stats(self, session_id: str, user_text: str, response_text: str):
        """Update conversation statistics"""
        if session_id not in self.conversation_stats:
            self.conversation_stats[session_id] = {
                'created_at': datetime.utcnow().isoformat(),
                'turn_count': 0,
                'total_user_chars': 0,
                'total_response_chars': 0,
                'messages': []
            }
        
        stats = self.conversation_stats[session_id]
        stats['turn_count'] += 1
        stats['total_user_chars'] += len(user_text)
        stats['total_response_chars'] += len(response_text)
        stats['messages'].append({
            'user': user_text,
            'response': response_text,
            'timestamp': datetime.utcnow().isoformat()
        })
    
    def get_conversation_stats(self, session_id: str) -> Dict[str, Any]:
        """Get conversation statistics"""
        if session_id not in self.conversation_stats:
            return {'error': 'Session not found'}
        
        stats = self.conversation_stats[session_id]
        return {
            'session_id': session_id,
            'created_at': stats['created_at'],
            'turn_count': stats['turn_count'],
            'total_user_chars': stats['total_user_chars'],
            'total_response_chars': stats['total_response_chars'],
            'avg_response_length': stats['total_response_chars'] / stats['turn_count'] if stats['turn_count'] > 0 else 0,
            'messages': stats['messages'][-10:]  # Last 10 messages
        }
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health"""
        return {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'services': {
                'asr': self.asr_service.get_health_status(),
                'llm': self.llm_service.get_health_status(),
                'tts': self.tts_service.get_health_status()
            },
            'active_sessions': len(self.conversation_stats)
        }
    
    def clear_session(self, session_id: str):
        """Clear session data"""
        if session_id in self.conversation_stats:
            del self.conversation_stats[session_id]
        self.llm_service.clear_conversation(session_id)


# Singleton instance
voice_orchestrator = VoiceOrchestrator()


"""
Voice Chat Service - Handles voice conversation workflows
Combines ASR, LLM, and TTS
"""

import json
from datetime import datetime
from typing import Dict, Any, Optional
from services.ai_service import ai_service
from models import Conversation, Message
from extensions import db

class VoiceChatService:
    """Service for managing voice conversations"""
    
    def __init__(self):
        self.ai_service = ai_service
    
    def create_conversation(self, user_id: int, title: str = None) -> Dict[str, Any]:
        """Create a new conversation"""
        try:
            conversation = Conversation(
                user_id=user_id,
                title=title or f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                status='active'
            )
            db.session.add(conversation)
            db.session.commit()
            
            return {
                'success': True,
                'conversation_id': conversation.id,
                'title': conversation.title,
                'created_at': conversation.created_at.isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def process_voice_input(self, conversation_id: int, audio_file_path: str) -> Dict[str, Any]:
        """
        Process voice input: transcribe -> generate response -> synthesize
        
        Args:
            conversation_id: ID of conversation
            audio_file_path: Path to audio file
            
        Returns:
            Dict with transcription, response, and audio
        """
        try:
            # Step 1: Transcribe audio
            transcription_result = self.ai_service.transcribe_audio(audio_file_path)
            if not transcription_result['success']:
                return {
                    'success': False,
                    'error': f"Transcription failed: {transcription_result.get('error', 'Unknown error')}"
                }
            
            user_text = transcription_result['text']
            
            # Step 2: Get conversation context
            conversation = Conversation.query.get(conversation_id)
            if not conversation:
                return {'success': False, 'error': 'Conversation not found'}
            
            context = self._build_context(conversation)
            
            # Step 3: Generate AI response
            ai_response = self.ai_service.generate_response(user_text, context)
            if not ai_response['success']:
                return {
                    'success': False,
                    'error': f"AI response failed: {ai_response.get('error', 'Unknown error')}"
                }
            
            response_text = ai_response['response']
            
            # Step 4: Synthesize response to speech
            tts_result = self.ai_service.synthesize_speech(response_text)
            if not tts_result['success']:
                # TTS failed but we still have text response
                tts_result = {'audio': None, 'provider': 'none'}
            
            # Step 5: Save messages to database
            user_message = Message(
                conversation_id=conversation_id,
                sender='user',
                content=user_text,
                message_type='voice'
            )
            
            assistant_message = Message(
                conversation_id=conversation_id,
                sender='assistant',
                content=response_text,
                message_type='voice',
                metadata=json.dumps({
                    'tts_provider': tts_result.get('provider', 'none'),
                    'ai_model': ai_response.get('model', 'unknown')
                })
            )
            
            db.session.add(user_message)
            db.session.add(assistant_message)
            db.session.commit()
            
            return {
                'success': True,
                'user_text': user_text,
                'response_text': response_text,
                'audio': tts_result.get('audio'),
                'audio_format': tts_result.get('format', 'mp3'),
                'tts_provider': tts_result.get('provider', 'none'),
                'ai_model': ai_response.get('model', 'unknown'),
                'message_id': assistant_message.id,
                'conversation_id': conversation_id
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def process_text_input(self, conversation_id: int, text: str, synthesize: bool = True) -> Dict[str, Any]:
        """
        Process text input: generate response -> optionally synthesize
        
        Args:
            conversation_id: ID of conversation
            text: User text input
            synthesize: Whether to synthesize response to speech
            
        Returns:
            Dict with response and optional audio
        """
        try:
            # Get conversation context
            conversation = Conversation.query.get(conversation_id)
            if not conversation:
                return {'success': False, 'error': 'Conversation not found'}
            
            context = self._build_context(conversation)
            
            # Generate AI response
            ai_response = self.ai_service.generate_response(text, context)
            if not ai_response['success']:
                return {
                    'success': False,
                    'error': f"AI response failed: {ai_response.get('error', 'Unknown error')}"
                }
            
            response_text = ai_response['response']
            
            # Optionally synthesize to speech
            tts_result = {'audio': None, 'provider': 'none'}
            if synthesize:
                tts_result = self.ai_service.synthesize_speech(response_text)
            
            # Save messages
            user_message = Message(
                conversation_id=conversation_id,
                sender='user',
                content=text,
                message_type='text'
            )
            
            assistant_message = Message(
                conversation_id=conversation_id,
                sender='assistant',
                content=response_text,
                message_type='text' if not synthesize else 'voice',
                metadata=json.dumps({
                    'tts_provider': tts_result.get('provider', 'none'),
                    'ai_model': ai_response.get('model', 'unknown')
                })
            )
            
            db.session.add(user_message)
            db.session.add(assistant_message)
            db.session.commit()
            
            return {
                'success': True,
                'response_text': response_text,
                'audio': tts_result.get('audio') if synthesize else None,
                'audio_format': tts_result.get('format', 'mp3'),
                'tts_provider': tts_result.get('provider', 'none'),
                'ai_model': ai_response.get('model', 'unknown'),
                'message_id': assistant_message.id,
                'conversation_id': conversation_id
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_conversation_history(self, conversation_id: int, limit: int = 50) -> Dict[str, Any]:
        """Get conversation history"""
        try:
            conversation = Conversation.query.get(conversation_id)
            if not conversation:
                return {'success': False, 'error': 'Conversation not found'}
            
            messages = Message.query.filter_by(conversation_id=conversation_id)\
                .order_by(Message.created_at.desc())\
                .limit(limit)\
                .all()
            
            messages_data = [{
                'id': m.id,
                'sender': m.sender,
                'content': m.content,
                'type': m.message_type,
                'created_at': m.created_at.isoformat()
            } for m in reversed(messages)]
            
            return {
                'success': True,
                'conversation_id': conversation_id,
                'title': conversation.title,
                'messages': messages_data,
                'total_messages': len(messages_data)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _build_context(self, conversation: 'Conversation') -> str:
        """Build conversation context from recent messages"""
        recent_messages = Message.query.filter_by(conversation_id=conversation.id)\
            .order_by(Message.created_at.desc())\
            .limit(10)\
            .all()
        
        context_lines = []
        for msg in reversed(recent_messages):
            sender = "User" if msg.sender == 'user' else "Assistant"
            context_lines.append(f"{sender}: {msg.content}")
        
        return "\n".join(context_lines) if context_lines else ""
    
    def analyze_conversation(self, conversation_id: int) -> Dict[str, Any]:
        """Analyze conversation for insights"""
        try:
            messages = Message.query.filter_by(conversation_id=conversation_id).all()
            
            if not messages:
                return {'success': False, 'error': 'No messages in conversation'}
            
            # Combine all messages
            full_text = " ".join([m.content for m in messages])
            
            # Analyze sentiment
            sentiment = self.ai_service.analyze_sentiment(full_text)
            
            # Extract entities
            entities = self.ai_service.extract_entities(full_text)
            
            return {
                'success': True,
                'conversation_id': conversation_id,
                'message_count': len(messages),
                'sentiment': sentiment,
                'entities': entities
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


# Singleton instance
voice_chat_service = VoiceChatService()


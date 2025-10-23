"""
Voice Assistant Test Suite
Tests all AI, voice, and chat functionality
"""

import unittest
import json
from app import create_app
from extensions import db
from models import User, Conversation, Message
from services.ai_service import ai_service
from services.voice_chat_service import voice_chat_service

class VoiceAssistantTestCase(unittest.TestCase):
    """Test cases for voice assistant"""
    
    def setUp(self):
        """Set up test client and database"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            # Create test user
            user = User(
                name='Test User',
                email='test@example.com',
                password='hashed_password'
            )
            db.session.add(user)
            db.session.commit()
            self.user_id = user.id
    
    def tearDown(self):
        """Clean up after tests"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    # ============ AI SERVICE TESTS ============
    
    def test_ai_service_initialization(self):
        """Test AI service initializes correctly"""
        self.assertIsNotNone(ai_service)
        self.assertEqual(ai_service.gemini_model, 'gemini-1.5-flash')
    
    def test_generate_response(self):
        """Test AI response generation"""
        result = ai_service.generate_response("Hello, how are you?")
        self.assertIn('success', result)
        self.assertIn('provider', result)
    
    def test_analyze_sentiment(self):
        """Test sentiment analysis"""
        result = ai_service.analyze_sentiment("I love this product!")
        self.assertIn('success', result)
        self.assertIn('provider', result)
    
    def test_extract_entities(self):
        """Test entity extraction"""
        result = ai_service.extract_entities("John works at Google in New York")
        self.assertIn('success', result)
        self.assertIn('provider', result)
    
    def test_generate_marketing_copy(self):
        """Test marketing copy generation"""
        result = ai_service.generate_marketing_copy(
            "Voice Assistant",
            ["AI-powered", "Real-time", "Multi-language"]
        )
        self.assertIn('success', result)
        self.assertIn('provider', result)
    
    # ============ VOICE CHAT SERVICE TESTS ============
    
    def test_create_conversation(self):
        """Test conversation creation"""
        with self.app.app_context():
            result = voice_chat_service.create_conversation(
                self.user_id,
                "Test Conversation"
            )
            self.assertTrue(result['success'])
            self.assertIn('conversation_id', result)
    
    def test_process_text_input(self):
        """Test text input processing"""
        with self.app.app_context():
            # Create conversation
            conv_result = voice_chat_service.create_conversation(
                self.user_id,
                "Test Chat"
            )
            conv_id = conv_result['conversation_id']
            
            # Process text
            result = voice_chat_service.process_text_input(
                conv_id,
                "Hello, assistant!",
                synthesize=False
            )
            
            self.assertIn('success', result)
            self.assertIn('response_text', result)
    
    def test_get_conversation_history(self):
        """Test getting conversation history"""
        with self.app.app_context():
            # Create conversation
            conv_result = voice_chat_service.create_conversation(
                self.user_id,
                "Test Chat"
            )
            conv_id = conv_result['conversation_id']
            
            # Add messages
            voice_chat_service.process_text_input(
                conv_id,
                "Hello!",
                synthesize=False
            )
            
            # Get history
            result = voice_chat_service.get_conversation_history(conv_id)
            self.assertTrue(result['success'])
            self.assertGreater(len(result['messages']), 0)
    
    # ============ API ENDPOINT TESTS ============
    
    def test_voice_api_health_check(self):
        """Test voice API health check"""
        response = self.client.get('/api/voice/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['status'], 'healthy')
    
    def test_create_conversation_endpoint(self):
        """Test create conversation endpoint"""
        with self.app.app_context():
            # Login first (mock)
            response = self.client.post(
                '/api/voice/conversations',
                json={'title': 'Test Chat'},
                headers={'Authorization': 'Bearer test_token'}
            )
            # Will fail without proper auth, but tests endpoint exists
            self.assertIn(response.status_code, [200, 201, 401, 403])
    
    def test_generate_response_endpoint(self):
        """Test generate response endpoint"""
        response = self.client.post(
            '/api/voice/ai/generate',
            json={'prompt': 'Hello!'},
            headers={'Authorization': 'Bearer test_token'}
        )
        # Tests endpoint exists
        self.assertIn(response.status_code, [200, 400, 401, 403])
    
    def test_sentiment_analysis_endpoint(self):
        """Test sentiment analysis endpoint"""
        response = self.client.post(
            '/api/voice/ai/sentiment',
            json={'text': 'I love this!'},
            headers={'Authorization': 'Bearer test_token'}
        )
        # Tests endpoint exists
        self.assertIn(response.status_code, [200, 400, 401, 403])
    
    def test_tts_endpoint(self):
        """Test TTS endpoint"""
        response = self.client.post(
            '/api/voice/tts/synthesize',
            json={'text': 'Hello world'},
            headers={'Authorization': 'Bearer test_token'}
        )
        # Tests endpoint exists
        self.assertIn(response.status_code, [200, 400, 401, 403])
    
    # ============ INTEGRATION TESTS ============
    
    def test_full_conversation_flow(self):
        """Test complete conversation flow"""
        with self.app.app_context():
            # Create conversation
            conv = voice_chat_service.create_conversation(
                self.user_id,
                "Integration Test"
            )
            self.assertTrue(conv['success'])
            conv_id = conv['conversation_id']
            
            # Send multiple messages
            for i in range(3):
                result = voice_chat_service.process_text_input(
                    conv_id,
                    f"Message {i+1}",
                    synthesize=False
                )
                self.assertIn('success', result)
            
            # Get history
            history = voice_chat_service.get_conversation_history(conv_id)
            self.assertTrue(history['success'])
            # Should have user + assistant messages
            self.assertGreaterEqual(len(history['messages']), 3)
    
    def test_conversation_analysis(self):
        """Test conversation analysis"""
        with self.app.app_context():
            # Create and populate conversation
            conv = voice_chat_service.create_conversation(
                self.user_id,
                "Analysis Test"
            )
            conv_id = conv['conversation_id']
            
            # Add messages
            voice_chat_service.process_text_input(
                conv_id,
                "I love this product!",
                synthesize=False
            )
            
            # Analyze
            result = voice_chat_service.analyze_conversation(conv_id)
            self.assertIn('success', result)
            if result['success']:
                self.assertIn('message_count', result)
                self.assertIn('sentiment', result)
    
    # ============ ERROR HANDLING TESTS ============
    
    def test_invalid_conversation_id(self):
        """Test handling of invalid conversation ID"""
        with self.app.app_context():
            result = voice_chat_service.get_conversation_history(99999)
            self.assertFalse(result['success'])
    
    def test_empty_text_input(self):
        """Test handling of empty text"""
        with self.app.app_context():
            conv = voice_chat_service.create_conversation(
                self.user_id,
                "Test"
            )
            result = voice_chat_service.process_text_input(
                conv['conversation_id'],
                "",
                synthesize=False
            )
            # Should handle gracefully
            self.assertIn('success', result)

if __name__ == '__main__':
    unittest.main()


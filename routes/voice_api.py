"""
Voice API Routes - Handles voice chat and AI operations
"""

import os
import json
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from services.voice_chat_service import voice_chat_service
from services.ai_service import ai_service
from models import Conversation, Message
from extensions import db

voice_api_bp = Blueprint('voice_api', __name__, url_prefix='/api/voice')

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'm4a', 'flac'}
UPLOAD_FOLDER = '/tmp/voice_uploads'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ============ CONVERSATION MANAGEMENT ============

@voice_api_bp.route('/conversations', methods=['GET'])
@login_required
def get_conversations():
    """Get all conversations for current user"""
    try:
        conversations = Conversation.query.filter_by(user_id=current_user.id)\
            .order_by(Conversation.created_at.desc())\
            .all()
        
        data = [{
            'id': c.id,
            'title': c.title,
            'status': c.status,
            'created_at': c.created_at.isoformat(),
            'message_count': len(c.messages)
        } for c in conversations]
        
        return jsonify({
            'success': True,
            'conversations': data,
            'total': len(data)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@voice_api_bp.route('/conversations', methods=['POST'])
@login_required
def create_conversation():
    """Create a new conversation"""
    try:
        data = request.get_json()
        title = data.get('title', f'Conversation {len(current_user.conversations) + 1}')
        
        result = voice_chat_service.create_conversation(current_user.id, title)
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@voice_api_bp.route('/conversations/<int:conversation_id>', methods=['GET'])
@login_required
def get_conversation(conversation_id):
    """Get conversation details"""
    try:
        conversation = Conversation.query.get(conversation_id)
        
        if not conversation or conversation.user_id != current_user.id:
            return jsonify({'success': False, 'error': 'Conversation not found'}), 404
        
        result = voice_chat_service.get_conversation_history(conversation_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============ VOICE CHAT ============

@voice_api_bp.route('/chat/voice', methods=['POST'])
@login_required
def voice_chat():
    """Process voice input and return voice response"""
    try:
        if 'audio' not in request.files:
            return jsonify({'success': False, 'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        conversation_id = request.form.get('conversation_id', type=int)
        
        if not conversation_id:
            return jsonify({'success': False, 'error': 'Conversation ID required'}), 400
        
        # Verify conversation belongs to user
        conversation = Conversation.query.get(conversation_id)
        if not conversation or conversation.user_id != current_user.id:
            return jsonify({'success': False, 'error': 'Conversation not found'}), 404
        
        if not allowed_file(audio_file.filename):
            return jsonify({'success': False, 'error': 'Invalid audio format'}), 400
        
        # Save audio file
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filename = secure_filename(audio_file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        audio_file.save(filepath)
        
        # Process voice input
        result = voice_chat_service.process_voice_input(conversation_id, filepath)
        
        # Clean up
        try:
            os.remove(filepath)
        except:
            pass
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@voice_api_bp.route('/chat/text', methods=['POST'])
@login_required
def text_chat():
    """Process text input and optionally return voice response"""
    try:
        data = request.get_json()
        conversation_id = data.get('conversation_id')
        text = data.get('text', '').strip()
        synthesize = data.get('synthesize', True)
        
        if not conversation_id or not text:
            return jsonify({'success': False, 'error': 'Conversation ID and text required'}), 400
        
        # Verify conversation
        conversation = Conversation.query.get(conversation_id)
        if not conversation or conversation.user_id != current_user.id:
            return jsonify({'success': False, 'error': 'Conversation not found'}), 404
        
        result = voice_chat_service.process_text_input(conversation_id, text, synthesize)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============ AI OPERATIONS ============

@voice_api_bp.route('/ai/generate', methods=['POST'])
@login_required
def generate_response():
    """Generate AI response"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        context = data.get('context', '')
        temperature = data.get('temperature', 0.7)
        
        if not prompt:
            return jsonify({'success': False, 'error': 'Prompt required'}), 400
        
        result = ai_service.generate_response(prompt, context, temperature)
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@voice_api_bp.route('/ai/sentiment', methods=['POST'])
@login_required
def analyze_sentiment():
    """Analyze sentiment of text"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'success': False, 'error': 'Text required'}), 400
        
        result = ai_service.analyze_sentiment(text)
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@voice_api_bp.route('/ai/entities', methods=['POST'])
@login_required
def extract_entities():
    """Extract entities from text"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'success': False, 'error': 'Text required'}), 400
        
        result = ai_service.extract_entities(text)
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@voice_api_bp.route('/ai/marketing', methods=['POST'])
@login_required
def generate_marketing():
    """Generate marketing copy"""
    try:
        data = request.get_json()
        product_name = data.get('product_name', '').strip()
        features = data.get('features', [])
        
        if not product_name or not features:
            return jsonify({'success': False, 'error': 'Product name and features required'}), 400
        
        result = ai_service.generate_marketing_copy(product_name, features)
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============ SPEECH SYNTHESIS ============

@voice_api_bp.route('/tts/synthesize', methods=['POST'])
@login_required
def synthesize():
    """Synthesize text to speech"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        voice = data.get('voice', 'default')
        
        if not text:
            return jsonify({'success': False, 'error': 'Text required'}), 400
        
        result = ai_service.synthesize_speech(text, voice)
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============ CONVERSATION ANALYSIS ============

@voice_api_bp.route('/conversations/<int:conversation_id>/analyze', methods=['GET'])
@login_required
def analyze_conversation(conversation_id):
    """Analyze conversation"""
    try:
        conversation = Conversation.query.get(conversation_id)
        if not conversation or conversation.user_id != current_user.id:
            return jsonify({'success': False, 'error': 'Conversation not found'}), 404
        
        result = voice_chat_service.analyze_conversation(conversation_id)
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============ HEALTH CHECK ============

@voice_api_bp.route('/health', methods=['GET'])
def health_check():
    """Check API health and provider status"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'providers': {
            'llm': 'gemini',
            'asr': 'whisper',
            'tts': 'coqui/google/elevenlabs',
            'database': 'mysql'
        }
    }), 200


"""
Voice Assistant Widget Routes
Handles widget API endpoints and widget management
"""

from flask import Blueprint, request, jsonify, render_template, current_app
from flask_login import login_required, current_user
from datetime import datetime
import json
import uuid

widget_bp = Blueprint('widget', __name__, url_prefix='/widget')

# In-memory widget sessions (in production, use database)
widget_sessions = {}

class WidgetSession:
    """Manages widget session data"""
    def __init__(self, session_id):
        self.session_id = session_id
        self.created_at = datetime.utcnow()
        self.messages = []
        self.turn_count = 0
        self.analytics = {
            'voice_plays': 0,
            'clicks': 0,
            'turns': 0
        }

    def add_message(self, sender, text):
        """Add message to session"""
        self.messages.append({
            'sender': sender,
            'text': text,
            'timestamp': datetime.utcnow().isoformat()
        })
        self.turn_count += 1

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'session_id': self.session_id,
            'created_at': self.created_at.isoformat(),
            'messages': self.messages,
            'turn_count': self.turn_count,
            'analytics': self.analytics
        }


# ============================================================================
# WIDGET CHAT API
# ============================================================================

@widget_bp.route('/api/chat', methods=['POST'])
def widget_chat():
    """Handle widget chat messages"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        session_id = data.get('sessionId', str(uuid.uuid4()))
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400

        # Get or create session
        if session_id not in widget_sessions:
            widget_sessions[session_id] = WidgetSession(session_id)
        
        session = widget_sessions[session_id]
        session.add_message('user', message)

        # Generate response (simple echo for now, can integrate with AI)
        response_text = generate_widget_response(message)
        session.add_message('assistant', response_text)

        return jsonify({
            'success': True,
            'response': response_text,
            'sessionId': session_id,
            'turnCount': session.turn_count
        }), 200

    except Exception as e:
        print(f"❌ Widget Chat Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@widget_bp.route('/api/voice', methods=['POST'])
def widget_voice():
    """Handle widget voice input"""
    try:
        data = request.get_json()
        audio_data = data.get('audio')
        session_id = data.get('sessionId', str(uuid.uuid4()))

        if not audio_data:
            return jsonify({'error': 'Audio data is required'}), 400

        # Get or create session
        if session_id not in widget_sessions:
            widget_sessions[session_id] = WidgetSession(session_id)

        # Process audio (transcribe, generate response, synthesize)
        transcribed_text = "Voice input received"  # Placeholder
        response_text = generate_widget_response(transcribed_text)
        
        # Generate TTS audio
        audio_url = f"/static/audio/response_{session_id}.mp3"

        return jsonify({
            'success': True,
            'transcribed': transcribed_text,
            'response': response_text,
            'audioUrl': audio_url,
            'sessionId': session_id
        }), 200

    except Exception as e:
        print(f"❌ Widget Voice Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@widget_bp.route('/api/session/<session_id>', methods=['GET'])
def get_session(session_id):
    """Get widget session data"""
    try:
        if session_id not in widget_sessions:
            return jsonify({'error': 'Session not found'}), 404

        session = widget_sessions[session_id]
        return jsonify(session.to_dict()), 200

    except Exception as e:
        print(f"❌ Get Session Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@widget_bp.route('/api/session/<session_id>/clear', methods=['POST'])
def clear_session(session_id):
    """Clear widget session"""
    try:
        if session_id in widget_sessions:
            del widget_sessions[session_id]
            return jsonify({'success': True, 'message': 'Session cleared'}), 200
        return jsonify({'error': 'Session not found'}), 404

    except Exception as e:
        print(f"❌ Clear Session Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# WIDGET MANAGEMENT (Admin)
# ============================================================================

@widget_bp.route('/dashboard', methods=['GET'])
@login_required
def widget_dashboard():
    """Widget management dashboard"""
    try:
        if current_user.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403

        return render_template('widget_dashboard.html', 
                             sessions=widget_sessions,
                             session_count=len(widget_sessions))

    except Exception as e:
        print(f"❌ Widget Dashboard Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@widget_bp.route('/embed-code', methods=['GET'])
@login_required
def get_embed_code():
    """Generate embed code for widget"""
    try:
        config = {
            'apiUrl': request.args.get('apiUrl', 'http://127.0.0.1:5000'),
            'theme': request.args.get('theme', 'light'),
            'position': request.args.get('position', 'bottom-right'),
            'primaryColor': request.args.get('primaryColor', '#667eea'),
            'secondaryColor': request.args.get('secondaryColor', '#764ba2'),
            'companyName': request.args.get('companyName', 'Voice Assistant'),
            'cornerRadius': request.args.get('cornerRadius', '12px')
        }

        embed_code = f"""
<!-- Voice Assistant Widget -->
<script src="{config['apiUrl']}/static/widget.js"></script>
<script>
    const widget = new VoiceAssistantWidget({{
        apiUrl: '{config['apiUrl']}',
        theme: '{config['theme']}',
        position: '{config['position']}',
        primaryColor: '{config['primaryColor']}',
        secondaryColor: '{config['secondaryColor']}',
        companyName: '{config['companyName']}',
        cornerRadius: '{config['cornerRadius']}'
    }});
</script>
<!-- End Voice Assistant Widget -->
        """.strip()

        return jsonify({
            'success': True,
            'embedCode': embed_code,
            'config': config
        }), 200

    except Exception as e:
        print(f"❌ Embed Code Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@widget_bp.route('/stats', methods=['GET'])
@login_required
def get_widget_stats():
    """Get widget statistics"""
    try:
        if current_user.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403

        total_sessions = len(widget_sessions)
        total_messages = sum(len(s.messages) for s in widget_sessions.values())
        total_turns = sum(s.turn_count for s in widget_sessions.values())

        stats = {
            'totalSessions': total_sessions,
            'totalMessages': total_messages,
            'totalTurns': total_turns,
            'averageTurnsPerSession': total_turns / total_sessions if total_sessions > 0 else 0,
            'sessions': [s.to_dict() for s in list(widget_sessions.values())[-10:]]
        }

        return jsonify(stats), 200

    except Exception as e:
        print(f"❌ Widget Stats Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def generate_widget_response(user_message):
    """Generate response for widget (can be enhanced with AI)"""
    responses = {
        'hello': 'Hello! How can I help you today?',
        'hi': 'Hi there! What can I do for you?',
        'help': 'I can help you with various tasks. What do you need?',
        'pricing': 'We offer 4 plans: Free, Starter ($29), Professional ($99), and Enterprise (custom).',
        'features': 'Our widget includes chat, voice input, analytics, and more!',
        'support': 'Our support team is available 24/7. How can we assist?',
    }

    user_lower = user_message.lower()
    
    for key, response in responses.items():
        if key in user_lower:
            return response

    return f"Thank you for your message: '{user_message}'. Our team will respond shortly."


# ============================================================================
# HEALTH CHECK
# ============================================================================

@widget_bp.route('/health', methods=['GET'])
def widget_health():
    """Widget health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'activeSessions': len(widget_sessions)
    }), 200


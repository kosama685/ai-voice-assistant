"""
Admin Panel Routes
Comprehensive admin dashboard for managing voice assistant
"""

from flask import Blueprint, request, jsonify, render_template, current_app
from flask_login import login_required, current_user
from functools import wraps
from datetime import datetime, timedelta
from models import db, User, Prompt, Conversation, Message
import json

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

# ============================================================================
# ADMIN DASHBOARD
# ============================================================================

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard with overview"""
    return render_template('admin/dashboard.html')

@admin_bp.route('/api/dashboard/stats')
@login_required
@admin_required
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        # User stats
        total_users = User.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        
        # Conversation stats
        total_conversations = Conversation.query.count()
        today_conversations = Conversation.query.filter(
            Conversation.created_at >= datetime.utcnow().date()
        ).count()
        
        # Message stats
        total_messages = Message.query.count()
        avg_response_time = db.session.query(
            db.func.avg(Message.response_time)
        ).scalar() or 0
        
        # Success rate
        successful_messages = Message.query.filter_by(status='success').count()
        success_rate = (successful_messages / total_messages * 100) if total_messages > 0 else 0
        
        return jsonify({
            'success': True,
            'stats': {
                'total_users': total_users,
                'active_users': active_users,
                'total_conversations': total_conversations,
                'today_conversations': today_conversations,
                'total_messages': total_messages,
                'avg_response_time': round(avg_response_time, 2),
                'success_rate': round(success_rate, 2)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# USER MANAGEMENT
# ============================================================================

@admin_bp.route('/users')
@login_required
@admin_required
def users_page():
    """User management page"""
    return render_template('admin/users.html')

@admin_bp.route('/api/users', methods=['GET'])
@login_required
@admin_required
def get_users():
    """Get all users with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        role = request.args.get('role', None)
        
        query = User.query
        if role:
            query = query.filter_by(role=role)
        
        paginated = query.paginate(page=page, per_page=per_page)
        
        users_data = [{
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'role': u.role,
            'is_active': u.is_active,
            'created_at': u.created_at.isoformat(),
            'last_login': u.last_login.isoformat() if u.last_login else None
        } for u in paginated.items]
        
        return jsonify({
            'success': True,
            'users': users_data,
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@admin_bp.route('/api/users/<int:user_id>', methods=['PUT'])
@login_required
@admin_required
def update_user(user_id):
    """Update user details"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        if 'role' in data:
            user.role = data['role']
        if 'is_active' in data:
            user.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'User updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@admin_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_user(user_id):
    """Delete user"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'User deleted successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# PROMPT MANAGEMENT
# ============================================================================

@admin_bp.route('/prompts')
@login_required
@admin_required
def prompts_page():
    """Prompt management page"""
    return render_template('admin/prompts.html')

@admin_bp.route('/api/prompts', methods=['GET'])
@login_required
@admin_required
def get_prompts():
    """Get all system prompts"""
    try:
        prompts = Prompt.query.all()
        
        prompts_data = [{
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'content': p.content,
            'personality': p.personality,
            'tone': p.tone,
            'is_active': p.is_active,
            'created_at': p.created_at.isoformat()
        } for p in prompts]
        
        return jsonify({
            'success': True,
            'prompts': prompts_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@admin_bp.route('/api/prompts', methods=['POST'])
@login_required
@admin_required
def create_prompt():
    """Create new prompt"""
    try:
        data = request.get_json()
        
        prompt = Prompt(
            name=data.get('name'),
            description=data.get('description'),
            content=data.get('content'),
            personality=data.get('personality', 'friendly'),
            tone=data.get('tone', 'conversational')
        )
        
        db.session.add(prompt)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Prompt created successfully',
            'prompt_id': prompt.id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@admin_bp.route('/api/prompts/<int:prompt_id>', methods=['PUT'])
@login_required
@admin_required
def update_prompt(prompt_id):
    """Update prompt"""
    try:
        prompt = Prompt.query.get(prompt_id)
        if not prompt:
            return jsonify({'error': 'Prompt not found'}), 404
        
        data = request.get_json()
        
        if 'name' in data:
            prompt.name = data['name']
        if 'description' in data:
            prompt.description = data['description']
        if 'content' in data:
            prompt.content = data['content']
        if 'personality' in data:
            prompt.personality = data['personality']
        if 'tone' in data:
            prompt.tone = data['tone']
        if 'is_active' in data:
            prompt.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Prompt updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# MONITORING & ANALYTICS
# ============================================================================

@admin_bp.route('/monitoring')
@login_required
@admin_required
def monitoring_page():
    """Real-time monitoring page"""
    return render_template('admin/monitoring.html')

@admin_bp.route('/api/monitoring/realtime')
@login_required
@admin_required
def get_realtime_monitoring():
    """Get real-time system metrics"""
    try:
        # Active conversations in last 5 minutes
        five_min_ago = datetime.utcnow() - timedelta(minutes=5)
        active_conversations = Conversation.query.filter(
            Conversation.updated_at >= five_min_ago
        ).count()
        
        # Recent messages
        recent_messages = Message.query.order_by(
            Message.created_at.desc()
        ).limit(10).all()
        
        return jsonify({
            'success': True,
            'metrics': {
                'active_conversations': active_conversations,
                'timestamp': datetime.utcnow().isoformat(),
                'recent_messages': [{
                    'id': m.id,
                    'text': m.text[:100],
                    'status': m.status,
                    'created_at': m.created_at.isoformat()
                } for m in recent_messages]
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@admin_bp.route('/api/analytics/usage')
@login_required
@admin_required
def get_usage_analytics():
    """Get usage analytics"""
    try:
        # Daily usage for last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        daily_usage = db.session.query(
            db.func.date(Message.created_at).label('date'),
            db.func.count(Message.id).label('count')
        ).filter(
            Message.created_at >= thirty_days_ago
        ).group_by(
            db.func.date(Message.created_at)
        ).all()
        
        usage_data = [{
            'date': str(date),
            'count': count
        } for date, count in daily_usage]
        
        return jsonify({
            'success': True,
            'usage': usage_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


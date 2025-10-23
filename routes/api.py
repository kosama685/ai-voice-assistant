from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import (
    User, Prompt, Conversation, Message,
    Function, SystemConfig, AuditLog, Subscription
)
from extensions import db
from datetime import datetime, timedelta

api_bp = Blueprint('api', __name__)

# User routes
@api_bp.route('/users', methods=['GET'])
@login_required
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@api_bp.route('/users', methods=['POST'])
@login_required
def create_user():
    data = request.get_json()
    
    # Check if email already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(
        name=data['name'],
        email=data['email'],
        role=data.get('role', 'tester'),
        status=data.get('status', 'active'),
        usage_limit=data.get('usage_limit', 1000)
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    # Log the action
    log = AuditLog(
        user_id=current_user.id,
        action='create',
        resource='user',
        resource_id=user.id,
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify(user.to_dict()), 201

@api_bp.route('/users/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@api_bp.route('/users/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.role = data.get('role', user.role)
    user.status = data.get('status', user.status)
    user.usage_limit = data.get('usage_limit', user.usage_limit)
    
    if 'password' in data and data['password']:
        user.set_password(data['password'])
    
    db.session.commit()
    
    # Log the action
    log = AuditLog(
        user_id=current_user.id,
        action='update',
        resource='user',
        resource_id=user.id,
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify(user.to_dict())

@api_bp.route('/users/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # Log the action before deletion
    log = AuditLog(
        user_id=current_user.id,
        action='delete',
        resource='user',
        resource_id=user.id,
        ip_address=request.remote_addr
    )
    db.session.add(log)
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User deleted successfully'})

# Prompt routes
@api_bp.route('/prompts', methods=['GET'])
@login_required
def get_prompts():
    prompts = Prompt.query.all()
    return jsonify([prompt.to_dict() for prompt in prompts])

@api_bp.route('/prompts', methods=['POST'])
@login_required
def create_prompt():
    data = request.get_json()
    
    prompt = Prompt(
        name=data['name'],
        type=data.get('type', 'custom'),
        content=data['content'],
        status=data.get('status', 'active'),
        created_by=current_user.id
    )
    
    db.session.add(prompt)
    db.session.commit()
    
    # Log the action
    log = AuditLog(
        user_id=current_user.id,
        action='create',
        resource='prompt',
        resource_id=prompt.id,
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify(prompt.to_dict()), 201

@api_bp.route('/prompts/<int:prompt_id>', methods=['GET'])
@login_required
def get_prompt(prompt_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    return jsonify(prompt.to_dict())

@api_bp.route('/prompts/<int:prompt_id>', methods=['PUT'])
@login_required
def update_prompt(prompt_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    data = request.get_json()
    
    prompt.name = data.get('name', prompt.name)
    prompt.type = data.get('type', prompt.type)
    prompt.content = data.get('content', prompt.content)
    prompt.status = data.get('status', prompt.status)
    prompt.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    # Log the action
    log = AuditLog(
        user_id=current_user.id,
        action='update',
        resource='prompt',
        resource_id=prompt.id,
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify(prompt.to_dict())

@api_bp.route('/prompts/<int:prompt_id>', methods=['DELETE'])
@login_required
def delete_prompt(prompt_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    
    # Log the action before deletion
    log = AuditLog(
        user_id=current_user.id,
        action='delete',
        resource='prompt',
        resource_id=prompt.id,
        ip_address=request.remote_addr
    )
    db.session.add(log)
    
    db.session.delete(prompt)
    db.session.commit()
    
    return jsonify({'message': 'Prompt deleted successfully'})

# Conversation routes
@api_bp.route('/conversations', methods=['GET'])
@login_required
def get_conversations():
    conversations = Conversation.query.all()
    return jsonify([conv.to_dict() for conv in conversations])

@api_bp.route('/conversations', methods=['POST'])
@login_required
def create_conversation():
    data = request.get_json()
    
    conversation = Conversation(
        user_id=data.get('user_id'),
        status=data.get('status', 'active')
    )
    
    db.session.add(conversation)
    db.session.commit()
    
    return jsonify(conversation.to_dict()), 201

@api_bp.route('/conversations/<int:conv_id>', methods=['GET'])
@login_required
def get_conversation(conv_id):
    conversation = Conversation.query.get_or_404(conv_id)
    return jsonify(conversation.to_dict())

@api_bp.route('/conversations/<int:conv_id>/messages', methods=['GET'])
@login_required
def get_conversation_messages(conv_id):
    messages = Message.query.filter_by(conversation_id=conv_id).all()
    return jsonify([msg.to_dict() for msg in messages])

@api_bp.route('/conversations/<int:conv_id>/messages', methods=['POST'])
@login_required
def add_conversation_message(conv_id):
    data = request.get_json()
    
    message = Message(
        conversation_id=conv_id,
        sender=data.get('sender', 'user'),
        content=data['content']
    )
    
    db.session.add(message)
    
    # Update conversation message count
    conversation = Conversation.query.get(conv_id)
    if conversation:
        conversation.message_count += 1
    
    db.session.commit()
    
    return jsonify(message.to_dict()), 201

# Function routes
@api_bp.route('/functions', methods=['GET'])
@login_required
def get_functions():
    functions = Function.query.all()
    return jsonify([func.to_dict() for func in functions])

@api_bp.route('/functions', methods=['POST'])
@login_required
def create_function():
    data = request.get_json()
    
    function = Function(
        name=data['name'],
        description=data.get('description', ''),
        status=data.get('status', 'active')
    )
    
    db.session.add(function)
    db.session.commit()
    
    # Log the action
    log = AuditLog(
        user_id=current_user.id,
        action='create',
        resource='function',
        resource_id=function.id,
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify(function.to_dict()), 201

@api_bp.route('/functions/<int:func_id>', methods=['PUT'])
@login_required
def update_function(func_id):
    function = Function.query.get_or_404(func_id)
    data = request.get_json()
    
    function.name = data.get('name', function.name)
    function.description = data.get('description', function.description)
    function.status = data.get('status', function.status)
    
    db.session.commit()
    
    # Log the action
    log = AuditLog(
        user_id=current_user.id,
        action='update',
        resource='function',
        resource_id=function.id,
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify(function.to_dict())

@api_bp.route('/functions/<int:func_id>', methods=['DELETE'])
@login_required
def delete_function(func_id):
    function = Function.query.get_or_404(func_id)
    
    # Log the action before deletion
    log = AuditLog(
        user_id=current_user.id,
        action='delete',
        resource='function',
        resource_id=function.id,
        ip_address=request.remote_addr
    )
    db.session.add(log)
    
    db.session.delete(function)
    db.session.commit()
    
    return jsonify({'message': 'Function deleted successfully'})

# System Config routes
@api_bp.route('/config', methods=['GET'])
@login_required
def get_config():
    configs = SystemConfig.query.all()
    return jsonify([config.to_dict() for config in configs])

@api_bp.route('/config', methods=['POST'])
@login_required
def create_config():
    data = request.get_json()
    
    config = SystemConfig(
        key=data['key'],
        value=data.get('value', ''),
        description=data.get('description', ''),
        updated_by=current_user.id
    )
    
    db.session.add(config)
    db.session.commit()
    
    # Log the action
    log = AuditLog(
        user_id=current_user.id,
        action='create',
        resource='config',
        resource_id=config.id,
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify(config.to_dict()), 201

@api_bp.route('/config/<int:config_id>', methods=['PUT'])
@login_required
def update_config(config_id):
    config = SystemConfig.query.get_or_404(config_id)
    data = request.get_json()
    
    config.value = data.get('value', config.value)
    config.description = data.get('description', config.description)
    config.updated_at = datetime.utcnow()
    config.updated_by = current_user.id
    
    db.session.commit()
    
    # Log the action
    log = AuditLog(
        user_id=current_user.id,
        action='update',
        resource='config',
        resource_id=config.id,
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify(config.to_dict())

# Analytics routes
@api_bp.route('/audit-logs', methods=['GET'])
@login_required
def get_audit_logs():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(100).all()
    return jsonify([log.to_dict() for log in logs])

@api_bp.route('/dashboard/stats', methods=['GET'])
@login_required
def get_dashboard_stats():
    # Calculate stats
    total_users = User.query.count()
    active_users = User.query.filter_by(status='active').count()
    total_conversations = Conversation.query.count()
    today_conversations = Conversation.query.filter(
        Conversation.start_time >= datetime.utcnow().date()
    ).count()
    
    # Get function usage
    functions = Function.query.all()
    function_usage = {func.name: func.usage_count for func in functions}
    
    # Get recent activities
    recent_logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(5).all()
    recent_activities = [log.to_dict() for log in recent_logs]
    
    return jsonify({
        'total_users': total_users,
        'active_users': active_users,
        'total_conversations': total_conversations,
        'today_conversations': today_conversations,
        'function_usage': function_usage,
        'recent_activities': recent_activities
    })

@api_bp.route('/analytics/usage', methods=['GET'])
@login_required
def get_usage_analytics():
    # Get date range from query params
    days = request.args.get('days', 7, type=int)
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get daily conversation counts
    daily_counts = []
    for i in range(days):
        date = start_date + timedelta(days=i)
        count = Conversation.query.filter(
            Conversation.start_time >= date.date(),
            Conversation.start_time < (date + timedelta(days=1)).date()
        ).count()
        daily_counts.append({
            'date': date.strftime('%Y-%m-%d'),
            'count': count
        })
    
    # Get function usage
    functions = Function.query.all()
    function_usage = [func.to_dict() for func in functions]
    
    # Get success vs fallback rates
    total_conversations = Conversation.query.count()
    completed_conversations = Conversation.query.filter_by(status='completed').count()
    error_conversations = Conversation.query.filter_by(status='error').count()
    
    success_rate = (completed_conversations / total_conversations * 100) if total_conversations > 0 else 0
    error_rate = (error_conversations / total_conversations * 100) if total_conversations > 0 else 0
    
    return jsonify({
        'daily_counts': daily_counts,
        'function_usage': function_usage,
        'success_rate': success_rate,
        'error_rate': error_rate
    })

# Subscription routes
@api_bp.route('/subscriptions', methods=['GET'])
@login_required
def get_subscriptions():
    subscriptions = Subscription.query.all()
    return jsonify([sub.to_dict() for sub in subscriptions])

@api_bp.route('/subscriptions/user/<int:user_id>', methods=['GET'])
@login_required
def get_user_subscription(user_id):
    subscription = Subscription.query.filter_by(user_id=user_id).first()
    if subscription:
        return jsonify(subscription.to_dict())
    return jsonify({'error': 'No subscription found'}), 404

@api_bp.route('/subscriptions', methods=['POST'])
@login_required
def create_subscription():
    data = request.get_json()

    # Check if user already has a subscription
    existing = Subscription.query.filter_by(user_id=data['user_id']).first()
    if existing:
        return jsonify({'error': 'User already has a subscription'}), 400

    subscription = Subscription(
        user_id=data['user_id'],
        plan=data.get('plan', 'free'),
        status=data.get('status', 'active'),
        price=data.get('price', 0.0),
        billing_cycle=data.get('billing_cycle', 'monthly'),
        auto_renew=data.get('auto_renew', True)
    )

    # Set end date based on billing cycle
    if data.get('plan') == 'demo':
        subscription.end_date = datetime.utcnow() + timedelta(days=30)
    elif data.get('billing_cycle') == 'yearly':
        subscription.end_date = datetime.utcnow() + timedelta(days=365)
    else:
        subscription.end_date = datetime.utcnow() + timedelta(days=30)

    db.session.add(subscription)
    db.session.commit()

    # Log the action
    log = AuditLog(
        user_id=current_user.id,
        action='create',
        resource='subscription',
        resource_id=subscription.id,
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()

    return jsonify(subscription.to_dict()), 201

@api_bp.route('/subscriptions/<int:sub_id>', methods=['PUT'])
@login_required
def update_subscription(sub_id):
    subscription = Subscription.query.get_or_404(sub_id)
    data = request.get_json()

    subscription.plan = data.get('plan', subscription.plan)
    subscription.status = data.get('status', subscription.status)
    subscription.price = data.get('price', subscription.price)
    subscription.billing_cycle = data.get('billing_cycle', subscription.billing_cycle)
    subscription.auto_renew = data.get('auto_renew', subscription.auto_renew)
    subscription.updated_at = datetime.utcnow()

    db.session.commit()

    # Log the action
    log = AuditLog(
        user_id=current_user.id,
        action='update',
        resource='subscription',
        resource_id=subscription.id,
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()

    return jsonify(subscription.to_dict())

@api_bp.route('/subscriptions/<int:sub_id>', methods=['DELETE'])
@login_required
def delete_subscription(sub_id):
    subscription = Subscription.query.get_or_404(sub_id)

    # Log the action before deletion
    log = AuditLog(
        user_id=current_user.id,
        action='delete',
        resource='subscription',
        resource_id=subscription.id,
        ip_address=request.remote_addr
    )
    db.session.add(log)

    db.session.delete(subscription)
    db.session.commit()

    return jsonify({'message': 'Subscription deleted successfully'})

@api_bp.route('/subscriptions/demo/start', methods=['POST'])
@login_required
def start_demo_subscription():
    """Start a 30-day demo subscription for the current user"""
    data = request.get_json()
    user_id = data.get('user_id', current_user.id)

    # Check if user already has an active demo
    existing_demo = Subscription.query.filter_by(
        user_id=user_id,
        plan='demo',
        status='active'
    ).first()

    if existing_demo:
        return jsonify({'error': 'User already has an active demo subscription'}), 400

    # Create demo subscription
    demo_sub = Subscription(
        user_id=user_id,
        plan='demo',
        status='active',
        price=0.0,
        billing_cycle='monthly',
        auto_renew=False,
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=30)
    )

    db.session.add(demo_sub)
    db.session.commit()

    # Log the action
    log = AuditLog(
        user_id=current_user.id,
        action='create',
        resource='demo_subscription',
        resource_id=demo_sub.id,
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({
        'message': 'Demo subscription started successfully',
        'subscription': demo_sub.to_dict()
    }), 201
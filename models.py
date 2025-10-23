from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
import bcrypt

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='tester')  # admin, developer, tester
    status = db.Column(db.String(20), default='active')  # active, inactive
    usage_limit = db.Column(db.Integer, default=1000)
    usage_current = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        ph = self.password_hash
        # If the stored hash looks like bcrypt ($2y$, $2b$, $2a$), use bcrypt directly.
        if isinstance(ph, str) and ph.startswith('$2'):
            try:
                # normalize $2y$ -> $2b$ for bcrypt library compatibility
                ph_fixed = ph.replace('$2y$', '$2b$', 1) if ph.startswith('$2y$') else ph
                return bcrypt.checkpw(password.encode('utf-8'), ph_fixed.encode('utf-8'))
            except Exception:
                return False

        # Fallback to Werkzeug for other hash schemes
        try:
            return check_password_hash(ph, password)
        except Exception:
            return False
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'status': self.status,
            'usage_limit': self.usage_limit,
            'usage_current': self.usage_current,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

class Prompt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), default='custom')  # system, function, custom
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default='general')  # general, customer_service, technical, sales, other
    status = db.Column(db.String(20), default='active')  # active, inactive, draft
    usage_count = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)
    version = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'content': self.content,
            'category': self.category,
            'status': self.status,
            'usage_count': self.usage_count,
            'rating': self.rating,
            'version': self.version,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by
        }

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')  # active, completed, error
    message_count = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'status': self.status,
            'message_count': self.message_count
        }

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))
    sender = db.Column(db.String(20), default='user')  # user, assistant
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'sender': self.sender,
            'content': self.content,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

class Function(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')  # active, inactive
    usage_count = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'usage_count': self.usage_count
        }

class SystemConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    description = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'key': self.key,
            'value': self.value,
            'description': self.description,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'updated_by': self.updated_by
        }

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    action = db.Column(db.String(50), nullable=False)
    resource = db.Column(db.String(100))
    resource_id = db.Column(db.Integer)
    ip_address = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='success')  # success, failed

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'resource': self.resource,
            'resource_id': self.resource_id,
            'ip_address': self.ip_address,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'status': self.status
        }

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan = db.Column(db.String(50), default='free')  # free, starter, professional, enterprise, demo
    status = db.Column(db.String(20), default='active')  # active, inactive, expired, cancelled
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    price = db.Column(db.Float, default=0.0)
    billing_cycle = db.Column(db.String(20), default='monthly')  # monthly, yearly
    auto_renew = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plan': self.plan,
            'status': self.status,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'price': self.price,
            'billing_cycle': self.billing_cycle,
            'auto_renew': self.auto_renew,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

def initialize_database():
    try:
        # Create admin user if not exists
        if not User.query.filter_by(email='admin@example.com').first():
            admin = User(
                name='Admin User',
                email='admin@example.com',
                role='admin',
                status='active'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

        # Create default system prompts if not exists
        if not Prompt.query.filter_by(name='Default Assistant').first():
            default_prompt = Prompt(
                name='Default Assistant',
                type='system',
                content='You are a helpful assistant. Your role is to assist users with their questions and tasks. Please be polite, professional, and provide accurate information. If you don\'t know the answer, be honest and suggest alternative approaches.',
                status='active',
                created_by=1
            )
            db.session.add(default_prompt)
            db.session.commit()
    except Exception as e:
        # If database schema is not yet updated, skip initialization
        print(f"Database initialization skipped: {str(e)}")
        db.session.rollback()

    # Create default functions if not exists
    if not Function.query.filter_by(name='Weather Lookup').first():
        weather_func = Function(
            name='Weather Lookup',
            description='Get current weather information for a location',
            status='active'
        )
        db.session.add(weather_func)
        db.session.commit()

    # Create default system configs if not exists
    default_configs = [
        {
            'key': 'llm_provider',
            'value': 'openai',
            'description': 'LLM Provider (openai, claude, gemini)'
        },
        {
            'key': 'llm_model',
            'value': 'gpt-4',
            'description': 'LLM Model'
        },
        {
            'key': 'llm_temperature',
            'value': '0.7',
            'description': 'LLM Temperature (0-1)'
        },
        {
            'key': 'asr_provider',
            'value': 'whisper',
            'description': 'ASR Provider'
        },
        {
            'key': 'tts_provider',
            'value': 'elevenlabs',
            'description': 'TTS Provider'
        }
    ]

    for config_data in default_configs:
        if not SystemConfig.query.filter_by(key=config_data['key']).first():
            config = SystemConfig(
                key=config_data['key'],
                value=config_data['value'],
                description=config_data['description'],
                updated_by=1
            )
            db.session.add(config)

    db.session.commit()
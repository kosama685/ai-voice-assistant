from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models import User, Conversation, Message, Prompt, SystemConfig

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # If not authenticated, show landing page
    if not current_user.is_authenticated:
        return render_template('landing.html')
    # If authenticated, show dashboard
    return render_template('index.html')

@main_bp.route('/widget-demo')
def widget_demo():
    """Widget demo page"""
    return render_template('widget_demo.html')

@main_bp.route('/analytics')
@login_required
def analytics():
    return render_template('analytics.html')

@main_bp.route('/prompts')
@login_required
def prompts():
    prompts = Prompt.query.all()
    return render_template('prompts.html', prompts=prompts)

@main_bp.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@main_bp.route('/config')
@login_required
def config():
    configs = SystemConfig.query.all()
    return render_template('config.html', configs=configs)

@main_bp.route('/monitoring')
@login_required
def monitoring():
    return render_template('monitoring.html')

@main_bp.route('/security')
@login_required
def security():
    return render_template('security.html')

@main_bp.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@main_bp.route('/analytics-enhanced')
@login_required
def analytics_enhanced():
    return render_template('analytics_enhanced.html')

@main_bp.route('/prompts-enhanced')
@login_required
def prompts_enhanced():
    prompts = Prompt.query.all()
    return render_template('prompts_enhanced.html', prompts=prompts)

@main_bp.route('/pricing')
@login_required
def pricing():
    return render_template('pricing.html')
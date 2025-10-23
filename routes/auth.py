from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import User, AuditLog, Subscription
from extensions import db
from datetime import datetime, timedelta
import json

# Try to import requests, if not available, provide fallback
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    requests = None

auth_bp = Blueprint('auth', __name__)

# ClickPay Configuration
CLICKPAY_PROFILE_ID = "44272"
CLICKPAY_SERVER_KEY = "SHJNLTLLM2-JLNJLDLZLH-GBRHMTJ92M"
CLICKPAY_BASE_URL = "https://secure.clickpay.com.sa"

@auth_bp.route('/landing')
def landing():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template('landing.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()

            # Log the login
            log = AuditLog(
                user_id=user.id,
                action='login',
                ip_address=request.remote_addr
            )
            db.session.add(log)
            db.session.commit()

            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password')

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    # Get plan from URL parameter if provided
    plan_param = request.args.get('plan', 'free')

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        plan = request.form.get('plan', 'free')

        # Validation
        if not all([name, email, password, confirm_password]):
            flash('All fields are required')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match')
            return render_template('register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters')
            return render_template('register.html')

        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return render_template('register.html')

        # Create user
        user = User(
            name=name,
            email=email,
            role='user',
            status='active'
        )
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        # Create subscription
        if plan == 'free':
            subscription = Subscription(
                user_id=user.id,
                plan='free',
                status='active',
                price=0.0,
                billing_cycle='monthly'
            )
            db.session.add(subscription)
            db.session.commit()

            # Log registration
            log = AuditLog(
                user_id=user.id,
                action='user_registered',
                ip_address=request.remote_addr
            )
            db.session.add(log)
            db.session.commit()

            flash('Registration successful! Please login.')
            return redirect(url_for('auth.login'))
        else:
            # Redirect to payment for paid plans
            db.session.commit()
            return redirect(url_for('auth.checkout', user_id=user.id, plan=plan))

    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    # Log the logout
    log = AuditLog(
        user_id=current_user.id,
        action='logout',
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()

    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/checkout/<int:user_id>/<plan>', methods=['GET', 'POST'])
def checkout(user_id, plan):
    user = User.query.get(user_id)
    if not user:
        flash('User not found')
        return redirect(url_for('auth.register'))

    # Pricing
    pricing = {
        'starter': {'price': 29.00, 'currency': 'SAR', 'name': 'Starter Plan'},
        'professional': {'price': 99.00, 'currency': 'SAR', 'name': 'Professional Plan'},
        'enterprise': {'price': 299.00, 'currency': 'SAR', 'name': 'Enterprise Plan'}
    }

    if plan not in pricing:
        flash('Invalid plan selected')
        return redirect(url_for('auth.register'))

    plan_info = pricing[plan]

    if request.method == 'POST':
        # Create payment request with ClickPay
        payment_response = create_clickpay_payment(
            order_id=f"USER_{user_id}_{int(datetime.utcnow().timestamp())}",
            amount=plan_info['price'],
            currency=plan_info['currency'],
            user_id=user_id,
            plan=plan
        )

        if 'error' in payment_response:
            flash(f"Payment error: {payment_response['error']}")
            return redirect(url_for('auth.checkout', user_id=user_id, plan=plan))

        # Redirect to ClickPay payment page
        return redirect(payment_response['redirect_url'])

    return render_template('checkout.html', user=user, plan=plan, plan_info=plan_info)

def create_clickpay_payment(order_id, amount, currency, user_id, plan):
    """Create payment request with ClickPay"""
    endpoint = "payment/request"
    description = f"Voice Assistant {plan.title()} Plan"

    data = {
        "profile_id": CLICKPAY_PROFILE_ID,
        "tran_type": "sale",
        "tran_class": "ecom",
        "cart_id": str(order_id),
        "cart_currency": currency,
        "cart_amount": f"{amount:.2f}",
        "cart_description": description,
        "callback": request.url_root.rstrip('/') + url_for('auth.payment_callback'),
        "return": request.url_root.rstrip('/') + url_for('auth.payment_return'),
        "return_using_get": True,
        "user_defined": {
            "udf1": str(user_id),
            "udf2": plan
        }
    }

    try:
        response = requests.post(
            f"{CLICKPAY_BASE_URL}/{endpoint}",
            json=data,
            headers={
                "authorization": CLICKPAY_SERVER_KEY,
                "Content-Type": "application/json"
            },
            timeout=30,
            verify=True
        )

        if response.status_code != 200:
            return {'error': f"ClickPay API returned HTTP {response.status_code}"}

        decoded = response.json()

        if 'redirect_url' not in decoded:
            return {'error': "No redirect URL in response"}

        return decoded

    except requests.exceptions.RequestException as e:
        return {'error': f"Request error: {str(e)}"}
    except Exception as e:
        return {'error': f"Error: {str(e)}"}

@auth_bp.route('/payment/callback', methods=['POST'])
def payment_callback():
    """ClickPay payment callback"""
    try:
        data = request.get_json()

        # Verify payment
        if data.get('response_code') == '000':  # Success
            user_id = int(data.get('user_defined', {}).get('udf1', 0))
            plan = data.get('user_defined', {}).get('udf2', 'starter')

            user = User.query.get(user_id)
            if user:
                # Create or update subscription
                subscription = Subscription.query.filter_by(user_id=user_id).first()
                if not subscription:
                    subscription = Subscription(user_id=user_id)

                subscription.plan = plan
                subscription.status = 'active'
                subscription.start_date = datetime.utcnow()
                subscription.end_date = datetime.utcnow() + timedelta(days=30)
                subscription.billing_cycle = 'monthly'
                subscription.auto_renew = True

                # Set price based on plan
                pricing = {'starter': 29.00, 'professional': 99.00, 'enterprise': 299.00}
                subscription.price = pricing.get(plan, 0.0)

                db.session.add(subscription)

                # Log payment
                log = AuditLog(
                    user_id=user_id,
                    action='payment_successful',
                    details=f"Plan: {plan}, Amount: {subscription.price}",
                    ip_address=request.remote_addr
                )
                db.session.add(log)
                db.session.commit()

                return jsonify({'status': 'success', 'message': 'Payment processed'}), 200

        return jsonify({'status': 'failed', 'message': 'Payment failed'}), 400

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@auth_bp.route('/payment/return', methods=['GET'])
def payment_return():
    """ClickPay payment return page"""
    response_code = request.args.get('response_code')
    user_id = request.args.get('udf1')
    plan = request.args.get('udf2')

    if response_code == '000':  # Success
        flash('Payment successful! Your subscription is now active.')
        user = User.query.get(user_id)
        if user:
            login_user(user)
            return redirect(url_for('main.index'))
    else:
        flash('Payment failed. Please try again.')

    return redirect(url_for('auth.login'))
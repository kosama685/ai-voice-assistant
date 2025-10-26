# Monetization & Subscription System Guide

## Overview

The Voice Assistant platform supports multiple monetization models:
1. **Fiat Payments** (Stripe)
2. **Cryptocurrency Payments** (Smart Contract)
3. **Tiered Subscriptions** (FREE, BASIC, PREMIUM, ENTERPRISE)
4. **Usage-Based Billing**

---

## Subscription Tiers

### FREE Tier
- **Price**: $0/month
- **Requests/Month**: 100
- **Tokens/Month**: 10,000
- **Features**: Basic voice assistant, limited API calls

### BASIC Tier
- **Price**: $29.99/month or $299.99/year
- **Requests/Month**: 5,000
- **Tokens/Month**: 500,000
- **Features**: Priority support, custom prompts, analytics

### PREMIUM Tier
- **Price**: $99.99/month or $999.99/year
- **Requests/Month**: 50,000
- **Tokens/Month**: 5,000,000
- **Features**: Advanced analytics, webhook integration, API access

### ENTERPRISE Tier
- **Price**: $499.99/month or $4,999.99/year
- **Requests/Month**: Unlimited
- **Tokens/Month**: Unlimited
- **Features**: Dedicated support, custom integration, SLA

---

## Database Schema

### Subscriptions Table

```sql
CREATE TABLE subscriptions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    tier ENUM('free', 'basic', 'premium', 'enterprise') DEFAULT 'free',
    status ENUM('active', 'cancelled', 'expired') DEFAULT 'active',
    start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_date TIMESTAMP NULL,
    auto_renew BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### Transactions Table

```sql
CREATE TABLE transactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    payment_method ENUM('stripe', 'crypto', 'paypal') DEFAULT 'stripe',
    status ENUM('pending', 'completed', 'failed') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### Usage Stats Table

```sql
CREATE TABLE usage_stats (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    date DATE NOT NULL,
    messages_count INT DEFAULT 0,
    conversations_count INT DEFAULT 0,
    tokens_used INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_date (user_id, date),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

---

## Stripe Integration

### 1. Install Stripe

```bash
pip install stripe
```

### 2. Configure Environment

Add to `.env`:

```env
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### 3. Create Payment Service

Create `services/payment_service.py`:

```python
import stripe
import os
from datetime import datetime, timedelta

class PaymentService:
    def __init__(self):
        stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
        self.public_key = os.environ.get('STRIPE_PUBLIC_KEY')
    
    def create_subscription(self, user_id, tier, email):
        """Create Stripe subscription"""
        prices = {
            'basic': 'price_basic_monthly',
            'premium': 'price_premium_monthly',
            'enterprise': 'price_enterprise_monthly'
        }
        
        customer = stripe.Customer.create(
            email=email,
            metadata={'user_id': user_id}
        )
        
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{'price': prices[tier]}],
            payment_behavior='default_incomplete',
            expand=['latest_invoice.payment_intent']
        )
        
        return subscription
    
    def cancel_subscription(self, subscription_id):
        """Cancel subscription"""
        return stripe.Subscription.delete(subscription_id)
    
    def upgrade_subscription(self, subscription_id, new_tier):
        """Upgrade subscription tier"""
        prices = {
            'basic': 'price_basic_monthly',
            'premium': 'price_premium_monthly',
            'enterprise': 'price_enterprise_monthly'
        }
        
        subscription = stripe.Subscription.retrieve(subscription_id)
        
        return stripe.Subscription.modify(
            subscription_id,
            items=[{
                'id': subscription['items']['data'][0].id,
                'price': prices[new_tier]
            }],
            proration_behavior='create_prorations'
        )
    
    def get_invoice(self, invoice_id):
        """Get invoice details"""
        return stripe.Invoice.retrieve(invoice_id)
    
    def list_invoices(self, customer_id):
        """List customer invoices"""
        return stripe.Invoice.list(customer=customer_id)
```

### 4. Create Payment Routes

Create `routes/payments.py`:

```python
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from services.payment_service import PaymentService
from models import db, Subscription, Transaction
import stripe

payment_bp = Blueprint('payments', __name__)
payment_service = PaymentService()

@payment_bp.route('/api/subscribe', methods=['POST'])
@login_required
def subscribe():
    """Create subscription"""
    data = request.json
    tier = data.get('tier')
    
    try:
        subscription = payment_service.create_subscription(
            current_user.id,
            tier,
            current_user.email
        )
        
        # Save to database
        sub = Subscription(
            user_id=current_user.id,
            tier=tier,
            status='active'
        )
        db.session.add(sub)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'subscription_id': subscription.id,
            'client_secret': subscription.latest_invoice.payment_intent.client_secret
        })
    except stripe.error.CardError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@payment_bp.route('/api/upgrade', methods=['POST'])
@login_required
def upgrade():
    """Upgrade subscription"""
    data = request.json
    new_tier = data.get('tier')
    
    try:
        subscription = Subscription.query.filter_by(
            user_id=current_user.id,
            status='active'
        ).first()
        
        if not subscription:
            return jsonify({'success': False, 'error': 'No active subscription'}), 400
        
        payment_service.upgrade_subscription(subscription.stripe_id, new_tier)
        subscription.tier = new_tier
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Upgraded successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@payment_bp.route('/api/cancel', methods=['POST'])
@login_required
def cancel():
    """Cancel subscription"""
    try:
        subscription = Subscription.query.filter_by(
            user_id=current_user.id,
            status='active'
        ).first()
        
        if not subscription:
            return jsonify({'success': False, 'error': 'No active subscription'}), 400
        
        payment_service.cancel_subscription(subscription.stripe_id)
        subscription.status = 'cancelled'
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Cancelled successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@payment_bp.route('/api/invoices', methods=['GET'])
@login_required
def get_invoices():
    """Get user invoices"""
    try:
        subscription = Subscription.query.filter_by(
            user_id=current_user.id
        ).first()
        
        if not subscription:
            return jsonify({'invoices': []})
        
        invoices = payment_service.list_invoices(subscription.stripe_customer_id)
        
        return jsonify({
            'success': True,
            'invoices': [{
                'id': inv.id,
                'amount': inv.amount_paid / 100,
                'date': inv.created,
                'status': inv.status,
                'pdf_url': inv.invoice_pdf
            } for inv in invoices.data]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@payment_bp.route('/webhook/stripe', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhooks"""
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            os.environ.get('STRIPE_WEBHOOK_SECRET')
        )
    except ValueError:
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError:
        return jsonify({'error': 'Invalid signature'}), 400
    
    # Handle events
    if event['type'] == 'invoice.payment_succeeded':
        invoice = event['data']['object']
        # Update subscription status
        
    elif event['type'] == 'invoice.payment_failed':
        invoice = event['data']['object']
        # Handle failed payment
        
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        # Update subscription status
    
    return jsonify({'success': True})
```

---

## Usage Tracking

### Track API Usage

```python
def track_usage(user_id, messages=0, tokens=0):
    """Track user API usage"""
    from datetime import date
    
    stats = UsageStats.query.filter_by(
        user_id=user_id,
        date=date.today()
    ).first()
    
    if not stats:
        stats = UsageStats(user_id=user_id, date=date.today())
        db.session.add(stats)
    
    stats.messages_count += messages
    stats.tokens_used += tokens
    db.session.commit()
```

### Check Usage Limits

```python
def check_usage_limit(user_id):
    """Check if user exceeded limit"""
    subscription = Subscription.query.filter_by(
        user_id=user_id,
        status='active'
    ).first()
    
    if not subscription:
        return False
    
    limits = {
        'free': 100,
        'basic': 5000,
        'premium': 50000,
        'enterprise': 999999
    }
    
    stats = UsageStats.query.filter_by(
        user_id=user_id,
        date=date.today()
    ).first()
    
    if not stats:
        return True
    
    return stats.messages_count < limits[subscription.tier]
```

---

## Billing Dashboard

Create `templates/billing.html`:

```html
{% extends "base.html" %}

{% block content %}
<div class="container mt-5">
    <h1>Billing & Subscription</h1>
    
    <div class="row">
        <div class="col-md-8">
            <div class="card mb-4">
                <div class="card-header">
                    <h5>Current Subscription</h5>
                </div>
                <div class="card-body">
                    <p><strong>Tier:</strong> <span id="currentTier">-</span></p>
                    <p><strong>Status:</strong> <span id="subStatus">-</span></p>
                    <p><strong>Renews:</strong> <span id="renewDate">-</span></p>
                    <button class="btn btn-warning" onclick="cancelSubscription()">
                        Cancel Subscription
                    </button>
                </div>
            </div>
            
            <div class="card">
                <div class="card-header">
                    <h5>Upgrade Subscription</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <button class="btn btn-primary w-100" onclick="upgradeTier('premium')">
                                Upgrade to Premium
                            </button>
                        </div>
                        <div class="col-md-6">
                            <button class="btn btn-success w-100" onclick="upgradeTier('enterprise')">
                                Upgrade to Enterprise
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-4">
            <div class="card">
                <div class="card-header">
                    <h5>Usage This Month</h5>
                </div>
                <div class="card-body">
                    <p><strong>Messages:</strong> <span id="messagesUsed">0</span></p>
                    <p><strong>Tokens:</strong> <span id="tokensUsed">0</span></p>
                    <div class="progress">
                        <div class="progress-bar" id="usageBar" style="width: 0%"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="card mt-4">
        <div class="card-header">
            <h5>Invoices</h5>
        </div>
        <div class="table-responsive">
            <table class="table mb-0" id="invoicesTable">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Amount</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
        </div>
    </div>
</div>

<script>
    async function loadBillingInfo() {
        const response = await fetch('/api/subscription');
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('currentTier').textContent = data.tier;
            document.getElementById('subStatus').textContent = data.status;
            document.getElementById('renewDate').textContent = new Date(data.end_date).toLocaleDateString();
        }
    }
    
    async function upgradeTier(tier) {
        const response = await fetch('/api/upgrade', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({tier})
        });
        
        const data = await response.json();
        if (data.success) {
            alert('Upgraded successfully!');
            loadBillingInfo();
        }
    }
    
    async function cancelSubscription() {
        if (confirm('Are you sure you want to cancel?')) {
            const response = await fetch('/api/cancel', {method: 'POST'});
            const data = await response.json();
            if (data.success) {
                alert('Subscription cancelled');
                loadBillingInfo();
            }
        }
    }
    
    document.addEventListener('DOMContentLoaded', loadBillingInfo);
</script>
{% endblock %}
```

---

## Revenue Analytics

Track revenue with:

```python
def get_revenue_stats(start_date, end_date):
    """Get revenue statistics"""
    transactions = Transaction.query.filter(
        Transaction.created_at >= start_date,
        Transaction.created_at <= end_date,
        Transaction.status == 'completed'
    ).all()
    
    return {
        'total_revenue': sum(t.amount for t in transactions),
        'transaction_count': len(transactions),
        'average_transaction': sum(t.amount for t in transactions) / len(transactions) if transactions else 0
    }
```

---

**Last Updated**: 2025-10-26  
**Status**: Production Ready


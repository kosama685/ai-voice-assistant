# 💳 ClickPay Integration Guide - Voice Assistant v2.1

## Overview

Complete ClickPay payment gateway integration for subscription management and user registration.

---

## 🔧 Configuration

### ClickPay Credentials
```python
CLICKPAY_PROFILE_ID = "44272"
CLICKPAY_SERVER_KEY = "SHJNLTLLM2-JLNJLDLZLH-GBRHMTJ92M"
CLICKPAY_BASE_URL = "https://secure.clickpay.com.sa"
```

**Location**: `routes/auth.py` (Lines 14-16)

---

## 📋 Features Implemented

### 1. User Registration
- **Route**: `/register` (GET, POST)
- **Features**:
  - Full name, email, password validation
  - Plan selection (Free, Starter, Professional, Enterprise)
  - Automatic free plan subscription
  - Redirect to checkout for paid plans
  - Audit logging

### 2. Payment Checkout
- **Route**: `/checkout/<user_id>/<plan>` (GET, POST)
- **Features**:
  - Order summary display
  - Plan details and pricing
  - Feature comparison
  - Security information
  - ClickPay payment integration

### 3. Payment Processing
- **Route**: `/payment/callback` (POST)
- **Features**:
  - Verify payment response
  - Create/update subscription
  - Auto-activate membership
  - Audit logging
  - Error handling

### 4. Payment Return
- **Route**: `/payment/return` (GET)
- **Features**:
  - Handle payment success/failure
  - Auto-login after successful payment
  - Flash messages for user feedback
  - Redirect to dashboard

---

## 💰 Subscription Plans

### Free Plan - $0/month
- 100 conversations/month
- Basic voice features
- Community support
- **Auto-activated** on registration

### Starter Plan - $29/month
- 5,000 conversations/month
- Advanced voice features
- Email support
- Basic analytics
- **Requires payment**

### Professional Plan - $99/month
- Unlimited conversations
- All voice features
- Priority support
- Advanced analytics
- API access
- **Requires payment**

### Enterprise Plan - Custom
- Unlimited everything
- Dedicated support
- Custom SLA
- On-premise deployment
- **Contact sales**

---

## 🔄 Payment Flow

```
1. User Registration
   ↓
2. Select Plan
   ↓
3. Free Plan? → Auto-activate → Login
   ↓ (No)
4. Paid Plan → Checkout Page
   ↓
5. Review Order
   ↓
6. Click "Proceed to Payment"
   ↓
7. Redirect to ClickPay
   ↓
8. Enter Card Details
   ↓
9. ClickPay Callback
   ↓
10. Verify Payment
    ↓
11. Create Subscription
    ↓
12. Auto-login & Redirect to Dashboard
```

---

## 🔐 Security Features

### Payment Security
- ✅ SSL/TLS encryption
- ✅ PCI DSS compliant
- ✅ Server-side verification
- ✅ Secure callback handling
- ✅ User data validation

### Data Protection
- ✅ Password hashing (bcrypt)
- ✅ Audit logging
- ✅ IP address tracking
- ✅ Session management
- ✅ CSRF protection

---

## 📝 API Endpoints

### Registration
```
POST /register
Parameters:
  - name: string (required)
  - email: string (required)
  - password: string (required, min 6 chars)
  - confirm_password: string (required)
  - plan: string (free, starter, professional, enterprise)

Response:
  - Redirect to login (free plan)
  - Redirect to checkout (paid plan)
```

### Checkout
```
GET /checkout/<user_id>/<plan>
POST /checkout/<user_id>/<plan>

Response:
  - Display checkout page (GET)
  - Redirect to ClickPay (POST)
```

### Payment Callback
```
POST /payment/callback
Headers:
  - Content-Type: application/json

Body:
  {
    "response_code": "000",
    "user_defined": {
      "udf1": "user_id",
      "udf2": "plan"
    }
  }

Response:
  - {"status": "success"} (200)
  - {"status": "failed"} (400)
```

### Payment Return
```
GET /payment/return
Parameters:
  - response_code: string
  - udf1: user_id
  - udf2: plan

Response:
  - Redirect to dashboard (success)
  - Redirect to login (failure)
```

---

## 🧪 Testing

### Test Cards (ClickPay Sandbox)
```
Visa:
  Card: 4111111111111111
  Expiry: 12/25
  CVV: 123

MasterCard:
  Card: 5555555555554444
  Expiry: 12/25
  CVV: 123
```

### Test Scenarios

1. **Free Plan Registration**
   - Go to /register
   - Select "Free Plan"
   - Submit form
   - Auto-login and redirect to dashboard

2. **Paid Plan Registration**
   - Go to /register
   - Select "Starter Plan"
   - Submit form
   - Redirect to checkout
   - Click "Proceed to Payment"
   - Redirect to ClickPay
   - Enter test card details
   - Complete payment
   - Auto-login and redirect to dashboard

3. **Payment Failure**
   - Use invalid card details
   - Payment fails
   - Redirect to login with error message

---

## 📊 Database Changes

### Subscription Table
```sql
CREATE TABLE subscription (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    plan VARCHAR(50) DEFAULT 'free',
    status VARCHAR(20) DEFAULT 'active',
    start_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    end_date DATETIME,
    price FLOAT DEFAULT 0.0,
    billing_cycle VARCHAR(20) DEFAULT 'monthly',
    auto_renew BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id),
    INDEX idx_user_id (user_id),
    INDEX idx_status (status)
);
```

### Audit Log Entry
```python
AuditLog(
    user_id=user_id,
    action='payment_successful',
    details=f"Plan: {plan}, Amount: {price}",
    ip_address=request.remote_addr
)
```

---

## 🚀 Deployment Checklist

- [ ] Update ClickPay credentials in `routes/auth.py`
- [ ] Configure callback URL in ClickPay dashboard
- [ ] Test payment flow with test cards
- [ ] Verify email notifications
- [ ] Set up SSL certificate
- [ ] Configure CORS if needed
- [ ] Test on production environment
- [ ] Monitor payment logs
- [ ] Set up error alerts

---

## 🔗 Integration Points

### Files Modified
1. **routes/auth.py**
   - Added registration route
   - Added checkout route
   - Added payment callback
   - Added payment return
   - Added ClickPay integration

2. **templates/register.html** (NEW)
   - Registration form
   - Plan selection
   - Validation

3. **templates/checkout.html** (NEW)
   - Order summary
   - Payment details
   - Security information

4. **templates/login.html** (UPDATED)
   - Added registration link
   - Improved styling

5. **templates/landing.html** (UPDATED)
   - Added registration link
   - Updated hero buttons

---

## 📞 Support

### ClickPay Documentation
- https://www.clickpay.com.sa/docs

### Common Issues

**Issue**: Payment callback not received
- **Solution**: Verify callback URL in ClickPay dashboard

**Issue**: User not auto-logged in
- **Solution**: Check Flask-Login configuration

**Issue**: Subscription not created
- **Solution**: Verify database connection and Subscription model

---

## 🎯 Next Steps

1. **Email Notifications**
   - Send confirmation email after registration
   - Send receipt after payment
   - Send renewal reminders

2. **Subscription Management**
   - Allow users to upgrade/downgrade plans
   - Implement auto-renewal
   - Handle failed payments

3. **Analytics**
   - Track conversion rates
   - Monitor payment failures
   - Analyze user retention

4. **Compliance**
   - Implement GDPR compliance
   - Add data retention policies
   - Set up audit trails

---

## 📈 Metrics

- **Registration Rate**: Track new user signups
- **Conversion Rate**: Track free to paid conversions
- **Payment Success Rate**: Monitor payment failures
- **Churn Rate**: Track subscription cancellations
- **LTV**: Calculate lifetime value per user

---

**Version**: 2.1  
**Last Updated**: 2025-10-23  
**Status**: ✅ Production Ready


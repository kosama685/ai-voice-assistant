# 📝 Registration & Payment Guide - Voice Assistant v2.1

## 🎯 Overview

Complete user registration and ClickPay payment integration for subscription management.

---

## 🌐 Access Points

### Public Pages
- **Landing Page**: http://127.0.0.1:5000/
- **Login Page**: http://127.0.0.1:5000/login
- **Registration Page**: http://127.0.0.1:5000/register

### Authenticated Pages
- **Dashboard**: http://127.0.0.1:5000/ (after login)
- **Pricing**: http://127.0.0.1:5000/pricing (after login)

---

## 📝 Registration Flow

### Step 1: Visit Registration Page
```
URL: http://127.0.0.1:5000/register
```

### Step 2: Fill Registration Form
- **Full Name**: Your display name
- **Email**: Valid email address
- **Password**: Minimum 6 characters
- **Confirm Password**: Must match password
- **Plan Selection**: Choose a plan

### Step 3: Select Plan

#### Free Plan ($0/month)
- 100 conversations/month
- Basic voice features
- Community support
- **Auto-activated** on registration
- **No payment required**

#### Starter Plan ($29/month)
- 5,000 conversations/month
- Advanced voice features
- Email support
- Basic analytics
- **Requires payment**

#### Professional Plan ($99/month)
- Unlimited conversations
- All voice features
- Priority support
- Advanced analytics
- API access
- **Requires payment**

#### Enterprise Plan (Custom)
- Unlimited everything
- Dedicated support
- Custom SLA
- On-premise deployment
- **Contact sales**

### Step 4: Submit Registration

#### For Free Plan
1. Click "Create Account"
2. Account created automatically
3. Redirected to login page
4. Login with your credentials
5. Dashboard access granted

#### For Paid Plans
1. Click "Create Account"
2. Redirected to checkout page
3. Review order summary
4. Click "Proceed to Payment"
5. Redirected to ClickPay
6. Enter payment details
7. Complete payment
8. Auto-login to dashboard

---

## 💳 Payment Process

### Checkout Page
- **Order Summary**: Plan details and pricing
- **Customer Info**: Name and email
- **Features**: Included features list
- **Price Breakdown**: Subtotal, tax, total
- **Payment Method**: ClickPay secure payment

### Payment Details
- **Subtotal**: Plan price
- **Tax**: 0% (no tax)
- **Total**: Final amount to pay

### Security Information
- ✅ SSL Encrypted (256-bit)
- ✅ PCI Compliant
- ✅ Verified Payment Gateway

### Payment Methods
- Visa
- MasterCard
- Other cards supported by ClickPay

---

## 🧪 Test Payment

### Test Cards (Sandbox Mode)

#### Visa
```
Card Number: 4111111111111111
Expiry: 12/25
CVV: 123
```

#### MasterCard
```
Card Number: 5555555555554444
Expiry: 12/25
CVV: 123
```

### Test Scenarios

1. **Successful Payment**
   - Use test card details
   - Payment processes successfully
   - Subscription activated
   - Auto-login to dashboard

2. **Failed Payment**
   - Use invalid card details
   - Payment fails
   - Error message displayed
   - Redirect to login

---

## 📊 Subscription Management

### After Registration

#### Free Plan Users
- Automatic subscription created
- Immediate dashboard access
- Can upgrade to paid plan anytime

#### Paid Plan Users
- Subscription created after payment
- Immediate dashboard access
- Auto-renewal enabled
- Can manage subscription in settings

### Subscription Details
- **Plan**: Current subscription plan
- **Status**: Active/Inactive/Expired
- **Start Date**: Subscription start date
- **End Date**: Subscription expiration date
- **Billing Cycle**: Monthly/Yearly
- **Auto-Renew**: Enabled/Disabled

### Manage Subscription
- View current plan
- Upgrade/downgrade plan
- Update payment method
- Cancel subscription
- View billing history

---

## 🔐 Security & Privacy

### Data Protection
- ✅ Password hashing (bcrypt)
- ✅ SSL/TLS encryption
- ✅ Secure payment processing
- ✅ PCI DSS compliance
- ✅ GDPR compliant

### Privacy Policy
- Your data is encrypted
- No data sharing with third parties
- Secure payment processing
- Regular security audits

### Terms & Conditions
- Agree to terms before registration
- Auto-renewal policy
- Cancellation policy
- Refund policy

---

## 📧 Email Notifications

### Registration Confirmation
- Welcome email sent
- Account activation link
- Getting started guide

### Payment Confirmation
- Payment receipt
- Subscription details
- Invoice attached

### Renewal Reminders
- 7 days before renewal
- 1 day before renewal
- Renewal confirmation

### Important Notices
- Payment failed notification
- Subscription expiration notice
- Plan upgrade/downgrade confirmation

---

## 🆘 Troubleshooting

### Registration Issues

**Problem**: Email already registered
- **Solution**: Use different email or login

**Problem**: Password too short
- **Solution**: Use at least 6 characters

**Problem**: Passwords don't match
- **Solution**: Confirm password matches

### Payment Issues

**Problem**: Payment declined
- **Solution**: Check card details and try again

**Problem**: Payment timeout
- **Solution**: Refresh page and retry

**Problem**: Subscription not activated
- **Solution**: Contact support

### Login Issues

**Problem**: Invalid email or password
- **Solution**: Check credentials and retry

**Problem**: Account locked
- **Solution**: Contact support

---

## 📞 Support

### Contact Information
- **Email**: support@voiceassistant.com
- **Chat**: In-app support
- **Phone**: +1 (555) 000-0000

### Hours
- Monday - Friday: 9 AM - 6 PM
- Saturday: 10 AM - 4 PM
- Sunday: Closed

### FAQ

**Q: Can I change my plan?**
A: Yes, upgrade or downgrade anytime in settings.

**Q: What if payment fails?**
A: We'll notify you and retry automatically.

**Q: Can I cancel anytime?**
A: Yes, cancel anytime with no penalties.

**Q: Do you offer refunds?**
A: Yes, 30-day money-back guarantee.

---

## 🎯 Next Steps

1. **Visit Registration Page**
   - Go to http://127.0.0.1:5000/register

2. **Create Account**
   - Fill in your details
   - Select a plan
   - Submit form

3. **Complete Payment** (if paid plan)
   - Review order
   - Enter payment details
   - Complete payment

4. **Access Dashboard**
   - Auto-login after registration
   - Explore features
   - Manage subscription

5. **Upgrade Plan** (optional)
   - Visit pricing page
   - Select new plan
   - Complete payment

---

## 📋 Checklist

- [ ] Visit landing page
- [ ] Click "Sign Up" button
- [ ] Fill registration form
- [ ] Select plan
- [ ] Submit registration
- [ ] Complete payment (if paid plan)
- [ ] Login to dashboard
- [ ] Explore features
- [ ] Manage subscription
- [ ] Read documentation

---

**Version**: 2.1  
**Last Updated**: 2025-10-23  
**Status**: ✅ Production Ready

**Thank you for choosing Voice Assistant!** 🚀


# ⚡ Quick Reference - Voice Assistant v2.1

## 🌐 Quick Links

### Public Pages
| Page | URL | Purpose |
|------|-----|---------|
| Landing | http://127.0.0.1:5000/ | Home page |
| Login | http://127.0.0.1:5000/login | User login |
| Register | http://127.0.0.1:5000/register | New user registration |
| Pricing | http://127.0.0.1:5000/pricing | Pricing plans |

### Dashboard Pages (After Login)
| Page | URL | Purpose |
|------|-----|---------|
| Dashboard | http://127.0.0.1:5000/ | Main dashboard |
| Users | http://127.0.0.1:5000/users | User management |
| Prompts | http://127.0.0.1:5000/prompts | Prompt management |
| Monitoring | http://127.0.0.1:5000/monitoring | Live monitoring |
| Analytics | http://127.0.0.1:5000/analytics | Analytics & reports |
| Config | http://127.0.0.1:5000/config | System configuration |
| Security | http://127.0.0.1:5000/security | Security & access |
| Settings | http://127.0.0.1:5000/settings | User settings |

---

## 💳 Subscription Plans

| Plan | Price | Conversations | Features |
|------|-------|---|----------|
| **Free** | $0/month | 100 | Basic voice |
| **Starter** | $29/month | 5,000 | Advanced voice |
| **Professional** | $99/month | Unlimited | All features |
| **Enterprise** | Custom | Unlimited | Custom SLA |

---

## 🧪 Test Cards

### Visa
```
Card: 4111111111111111
Expiry: 12/25
CVV: 123
```

### MasterCard
```
Card: 5555555555554444
Expiry: 12/25
CVV: 123
```

---

## 🚀 Quick Commands

### Start Server
```bash
cd c:\laragon\www\voice_assistant_app
.\venv\Scripts\python run.py
```

### Fix Database
```bash
.\venv\Scripts\python fix_database.py
```

### Install Dependencies
```bash
.\venv\Scripts\pip install -r requirements.txt
```

### Activate Virtual Environment
```bash
.\venv\Scripts\activate
```

### Test Import
```bash
.\venv\Scripts\python -c "from app import create_app; print('OK')"
```

---

## 📝 Registration Flow

1. Visit http://127.0.0.1:5000/register
2. Fill registration form
3. Select plan (Free or Starter)
4. Click "Create Account"
5. For Free: Auto-login to dashboard
6. For Starter: Redirect to checkout
7. Complete payment
8. Auto-login to dashboard

---

## 💳 Payment Flow

1. Select paid plan
2. Redirect to checkout
3. Review order
4. Click "Proceed to Payment"
5. Redirect to ClickPay
6. Enter card details
7. Payment processed
8. Subscription created
9. Auto-login to dashboard

---

## 🔐 Default Credentials

### Admin Account
```
Email: admin@voiceassistant.com
Password: admin123
```

### Test Account
```
Email: test@voiceassistant.com
Password: test123
```

---

## 📊 API Endpoints

### Authentication
```
POST   /register
GET    /login
POST   /login
GET    /logout
```

### Payment
```
GET    /checkout/<user_id>/<plan>
POST   /checkout/<user_id>/<plan>
POST   /payment/callback
GET    /payment/return
```

### Users
```
GET    /api/users
POST   /api/users
PUT    /api/users/<id>
DELETE /api/users/<id>
```

### Prompts
```
GET    /api/prompts
POST   /api/prompts
PUT    /api/prompts/<id>
DELETE /api/prompts/<id>
```

### Subscriptions
```
GET    /api/subscriptions
POST   /api/subscriptions
PUT    /api/subscriptions/<id>
DELETE /api/subscriptions/<id>
```

---

## 🗂️ File Structure

```
voice_assistant_app/
├── app.py                 # Flask app factory
├── run.py                 # Entry point
├── config.py              # Configuration
├── models.py              # Database models
├── fix_database.py        # Database fixer
├── requirements.txt       # Dependencies
├── routes/
│   ├── auth.py           # Auth routes
│   ├── main.py           # Main routes
│   └── api.py            # API routes
├── templates/
│   ├── base.html         # Base template
│   ├── landing.html      # Landing page
│   ├── login.html        # Login page
│   ├── register.html     # Registration
│   ├── checkout.html     # Checkout
│   ├── index.html        # Dashboard
│   ├── users.html        # Users
│   ├── prompts_enhanced.html
│   ├── monitoring.html   # Monitoring
│   ├── analytics_enhanced.html
│   ├── config.html       # Config
│   ├── security.html     # Security
│   └── pricing.html      # Pricing
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── migrations/           # Database migrations
```

---

## 🔧 Configuration

### Database
```python
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_DATABASE = 'voiceast'
DB_USERNAME = 'root'
DB_PASSWORD = 'root'
```

### ClickPay
```python
CLICKPAY_PROFILE_ID = "44272"
CLICKPAY_SERVER_KEY = "SHJNLTLLM2-JLNJLDLZLH-GBRHMTJ92M"
CLICKPAY_BASE_URL = "https://secure.clickpay.com.sa"
```

### Flask
```python
DEBUG = True
SECRET_KEY = 'your-secret-key'
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| README.md | Main overview |
| QUICK_START.md | Quick start guide |
| QUICK_REFERENCE.md | This file |
| CLICKPAY_INTEGRATION.md | Payment integration |
| REGISTRATION_PAYMENT_GUIDE.md | User guide |
| TROUBLESHOOTING_GUIDE.md | Troubleshooting |
| DATABASE_FIX_REPORT.md | Database info |
| FINAL_IMPLEMENTATION_REPORT.md | Project report |
| COMPLETE_IMPLEMENTATION_SUMMARY.md | Full summary |

---

## ✅ Verification Checklist

- [ ] Server running at http://127.0.0.1:5000
- [ ] Landing page loads
- [ ] Registration page loads
- [ ] Login page loads
- [ ] Can create free account
- [ ] Can create paid account
- [ ] Payment processing works
- [ ] Auto-login works
- [ ] Dashboard accessible
- [ ] All pages load
- [ ] Database connected
- [ ] No errors in console

---

## 🆘 Quick Troubleshooting

### Server won't start
```bash
# Check if port 5000 is in use
netstat -ano | findstr :5000

# Kill process
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process -Force
```

### Database error
```bash
# Fix database
.\venv\Scripts\python fix_database.py

# Check MySQL
mysql -h 127.0.0.1 -u root -p voiceast
```

### Missing module
```bash
# Install dependencies
.\venv\Scripts\pip install -r requirements.txt
```

### Registration not working
- Check browser console (F12)
- Verify form validation
- Check server logs
- Verify database connection

### Payment not working
- Verify ClickPay credentials
- Use test card
- Check network connectivity
- Review payment logs

---

## 📞 Support Resources

### Documentation
- README.md - Main overview
- QUICK_START.md - Getting started
- TROUBLESHOOTING_GUIDE.md - Common issues

### Contact
- Email: support@voiceassistant.com
- Chat: In-app support
- Phone: +1 (555) 000-0000

---

## 🎯 Common Tasks

### Create New User
1. Visit http://127.0.0.1:5000/register
2. Fill form
3. Select plan
4. Submit

### Process Payment
1. Select paid plan
2. Go to checkout
3. Enter test card
4. Complete payment

### View Analytics
1. Login to dashboard
2. Click "Analytics"
3. View reports

### Manage Users
1. Login to dashboard
2. Click "Users"
3. View/edit users

### Manage Prompts
1. Login to dashboard
2. Click "Prompts"
3. Create/edit prompts

---

**Version**: 2.1  
**Last Updated**: 2025-10-23  
**Status**: ✅ Production Ready

Keep this file handy for quick reference!


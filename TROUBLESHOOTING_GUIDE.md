# 🔧 Troubleshooting Guide - Voice Assistant v2.1

## Common Issues & Solutions

---

## 🚨 Issue 1: ModuleNotFoundError: No module named 'requests'

### Error Message
```
ModuleNotFoundError: No module named 'requests'
```

### Cause
The `requests` module is not installed in the virtual environment.

### Solution

**Option 1: Install via pip**
```bash
cd c:\laragon\www\voice_assistant_app
.\venv\Scripts\pip install requests
```

**Option 2: Install from requirements.txt**
```bash
cd c:\laragon\www\voice_assistant_app
.\venv\Scripts\pip install -r requirements.txt
```

**Option 3: Verify installation**
```bash
.\venv\Scripts\python -c "import requests; print(requests.__version__)"
```

### Prevention
- Always run `pip install -r requirements.txt` after cloning
- Keep requirements.txt updated with all dependencies
- Use virtual environment consistently

---

## 🚨 Issue 2: Unknown column 'prompt.category' in 'field list'

### Error Message
```
MySQLdb.OperationalError: (1054, "Unknown column 'prompt.category' in 'field list'")
```

### Cause
Database schema is out of sync with model definitions.

### Solution

**Option 1: Run database fix script**
```bash
cd c:\laragon\www\voice_assistant_app
.\venv\Scripts\python fix_database.py
```

**Option 2: Manual migration**
```bash
.\venv\Scripts\python -m flask db upgrade
```

**Option 3: Verify columns exist**
```sql
DESCRIBE prompt;
```

### Prevention
- Always run migrations after model changes
- Keep database synchronized with models
- Test database changes before deployment

---

## 🚨 Issue 3: Flask app not starting

### Error Message
```
Error: Could not locate a Flask application
```

### Cause
Flask cannot find the application factory.

### Solution

**Option 1: Check run.py**
```bash
cd c:\laragon\www\voice_assistant_app
.\venv\Scripts\python run.py
```

**Option 2: Check app.py**
```bash
.\venv\Scripts\python -c "from app import create_app; app = create_app(); print('App created successfully')"
```

**Option 3: Check imports**
- Verify all imports in app.py are correct
- Check for circular imports
- Verify all blueprints are registered

### Prevention
- Keep app.py simple and clean
- Use proper blueprint registration
- Test imports before deployment

---

## 🚨 Issue 4: Database connection failed

### Error Message
```
MySQLdb.OperationalError: (2003, "Can't connect to MySQL server")
```

### Cause
MySQL server is not running or credentials are incorrect.

### Solution

**Option 1: Start MySQL**
```bash
# Windows
net start MySQL80

# Or use Laragon
# Click "Start All" in Laragon
```

**Option 2: Verify credentials**
```python
# Check config.py
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_DATABASE = 'voiceast'
DB_USERNAME = 'root'
DB_PASSWORD = 'root'
```

**Option 3: Test connection**
```bash
mysql -h 127.0.0.1 -u root -p voiceast
```

### Prevention
- Ensure MySQL is running before starting app
- Use correct credentials
- Test database connection regularly

---

## 🚨 Issue 5: Port 5000 already in use

### Error Message
```
OSError: [Errno 48] Address already in use
```

### Cause
Another application is using port 5000.

### Solution

**Option 1: Kill process on port 5000**
```bash
# Windows PowerShell
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process -Force
```

**Option 2: Use different port**
```bash
.\venv\Scripts\python run.py --port 5001
```

**Option 3: Check what's using the port**
```bash
netstat -ano | findstr :5000
```

### Prevention
- Close previous Flask instances
- Use process manager for production
- Configure port in environment variables

---

## 🚨 Issue 6: Registration form not submitting

### Error Message
```
Form submission fails silently
```

### Cause
Validation errors or missing form fields.

### Solution

**Option 1: Check browser console**
- Open Developer Tools (F12)
- Check Console tab for JavaScript errors
- Check Network tab for failed requests

**Option 2: Verify form fields**
- Ensure all required fields are filled
- Check password length (minimum 6 characters)
- Verify passwords match

**Option 3: Check server logs**
- Look at Flask console output
- Check for validation errors
- Verify database connection

### Prevention
- Add client-side validation
- Provide clear error messages
- Test form submission thoroughly

---

## 🚨 Issue 7: Payment not processing

### Error Message
```
ClickPay API error or payment declined
```

### Cause
Invalid credentials, test card, or network issue.

### Solution

**Option 1: Verify ClickPay credentials**
```python
# Check routes/auth.py
CLICKPAY_PROFILE_ID = "44272"
CLICKPAY_SERVER_KEY = "SHJNLTLLM2-JLNJLDLZLH-GBRHMTJ92M"
CLICKPAY_BASE_URL = "https://secure.clickpay.com.sa"
```

**Option 2: Use test card**
```
Card: 4111111111111111
Expiry: 12/25
CVV: 123
```

**Option 3: Check network connectivity**
- Verify internet connection
- Check firewall settings
- Test ClickPay API directly

### Prevention
- Use correct credentials
- Test with test cards first
- Monitor payment logs
- Set up error alerts

---

## 🚨 Issue 8: Auto-login not working

### Error Message
```
User not logged in after payment
```

### Cause
Flask-Login not configured properly or session issue.

### Solution

**Option 1: Check Flask-Login setup**
```python
# Verify in app.py
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
```

**Option 2: Verify user loader**
```python
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

**Option 3: Check session configuration**
```python
# Verify in config.py
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
```

### Prevention
- Test login functionality separately
- Verify user loader is registered
- Check session configuration
- Monitor authentication logs

---

## 🆘 General Troubleshooting Steps

### 1. Check Logs
```bash
# Flask console output
# Check for error messages
# Look for stack traces
```

### 2. Verify Configuration
```bash
# Check config.py
# Verify database credentials
# Check API keys
```

### 3. Test Components
```bash
# Test database connection
# Test API endpoints
# Test form submission
```

### 4. Clear Cache
```bash
# Clear browser cache
# Clear Flask cache
# Restart server
```

### 5. Check Dependencies
```bash
.\venv\Scripts\pip list
# Verify all required packages are installed
```

---

## 📞 Getting Help

### Check Documentation
- README.md
- QUICK_START.md
- CLICKPAY_INTEGRATION.md
- REGISTRATION_PAYMENT_GUIDE.md

### Check Logs
- Flask console output
- Database error logs
- Browser developer console

### Contact Support
- Email: support@voiceassistant.com
- Chat: In-app support
- Phone: +1 (555) 000-0000

---

## 🔍 Debugging Tips

### Enable Debug Mode
```python
# In run.py
app.run(debug=True)
```

### Add Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Use Flask Shell
```bash
.\venv\Scripts\python -m flask shell
```

### Test Database
```bash
mysql -h 127.0.0.1 -u root -p voiceast
```

---

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment activated
- [ ] All dependencies installed
- [ ] MySQL running
- [ ] Database created
- [ ] Migrations applied
- [ ] Flask app starts
- [ ] Registration page loads
- [ ] Login works
- [ ] Payment processing works
- [ ] Auto-login works
- [ ] Dashboard accessible

---

## 🚀 Quick Fix Commands

```bash
# Install dependencies
.\venv\Scripts\pip install -r requirements.txt

# Fix database
.\venv\Scripts\python fix_database.py

# Start server
.\venv\Scripts\python run.py

# Test import
.\venv\Scripts\python -c "from app import create_app; print('OK')"

# Check requests module
.\venv\Scripts\python -c "import requests; print(requests.__version__)"
```

---

**Version**: 2.1  
**Last Updated**: 2025-10-23  
**Status**: ✅ Complete

For more help, refer to the comprehensive documentation files in the project folder.


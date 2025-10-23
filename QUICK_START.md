# Quick Start Guide - Voice Assistant Management System

## Starting the Application

### Option 1: Using Virtual Environment (Recommended)
```bash
cd c:\laragon\www\voice_assistant_app
.\venv\Scripts\activate
python run.py
```

### Option 2: Direct Python
```bash
cd c:\laragon\www\voice_assistant_app
python run.py
```

The application will start at: **http://127.0.0.1:5000**

## Default Login Credentials

**Email**: admin@example.com  
**Password**: admin123

## Navigation Menu

### 1. **Dashboard** 📊
- View system statistics
- See usage trends over 7 days
- Check recent activities
- Monitor system status

### 2. **User Management** 👥
- View all users
- Add new users
- Edit user details
- Delete users
- Track user usage

### 3. **Prompt & Logic** 💬
- Manage system prompts
- Create custom prompts
- Edit prompt content
- Enable/disable prompts
- View function calls

### 4. **Live Monitoring** 📈
- Real-time statistics
- Active users count
- Ongoing conversations
- Response time metrics
- Error rate tracking
- Recent conversations list

### 5. **Analytics & Reports** 📉
- Usage analytics
- Conversation trends
- Function usage statistics
- Success/error rates

### 6. **System Configuration** ⚙️
- LLM Provider settings
- ASR (Speech Recognition) settings
- TTS (Text-to-Speech) settings
- Custom configurations
- Search and filter configs

### 7. **Security & Access** 🔒
- View user roles and permissions
- Audit log tracking
- Security statistics
- Failed login attempts
- Recent logins

## Key Features

### CRUD Operations
All pages support full CRUD (Create, Read, Update, Delete):
- **Create**: Use "Add" buttons in each section
- **Read**: View data in tables
- **Update**: Click edit buttons or inline editing
- **Delete**: Click delete buttons with confirmation

### Search & Filter
- Config page has search functionality
- Filter by configuration type
- Real-time search results

### Real-time Updates
- Monitoring page auto-refreshes every 30 seconds
- Manual refresh available
- Live statistics

### Audit Logging
- All actions are logged
- Track who did what and when
- IP address recording
- Success/failure status

## User Roles

### Admin
- Full access to all features
- Manage users, prompts, config
- View security logs
- System administration

### Developer
- Manage prompts and functions
- Monitor system
- View analytics
- Limited user management

### Tester
- View monitoring and analytics
- Limited system access
- Cannot modify configurations

## Common Tasks

### Add a New User
1. Go to **User Management**
2. Click **Add New User**
3. Fill in name, email, password, role
4. Click **Add User**

### Create a System Configuration
1. Go to **System Configuration**
2. Click **Add Configuration**
3. Enter key, value, and description
4. Click **Add Configuration**

### Edit a Configuration
1. Go to **System Configuration**
2. Click the **Edit** button on the configuration
3. Update the value
4. Click **Update**

### Delete a Configuration
1. Go to **System Configuration**
2. Click the **Delete** button
3. Confirm deletion

### View Audit Logs
1. Go to **Security & Access**
2. Scroll to **Audit Logs** section
3. View all system activities with timestamps

### Monitor System
1. Go to **Live Monitoring**
2. View real-time statistics
3. Check recent conversations
4. Click **Refresh** for manual update

## Troubleshooting

### Application Won't Start
- Check if port 5000 is available
- Ensure virtual environment is activated
- Check Python version (3.8+)

### Database Errors
- Run migrations: `flask db upgrade`
- Check database connection in config.py
- Ensure MySQL is running

### Missing Dependencies
- Run: `pip install -r requirements.txt`
- Or: `.\venv\Scripts\pip install -r requirements.txt`

### Login Issues
- Use default credentials: admin@example.com / admin123
- Check if database is initialized
- Clear browser cache and cookies

## API Endpoints

All endpoints require authentication (login).

### Users
- `GET /api/users` - List all users
- `POST /api/users` - Create user
- `PUT /api/users/<id>` - Update user
- `DELETE /api/users/<id>` - Delete user

### Prompts
- `GET /api/prompts` - List prompts
- `POST /api/prompts` - Create prompt
- `PUT /api/prompts/<id>` - Update prompt
- `DELETE /api/prompts/<id>` - Delete prompt

### Configuration
- `GET /api/config` - List configs
- `POST /api/config` - Create config
- `PUT /api/config/<id>` - Update config
- `DELETE /api/config/<id>` - Delete config

### Analytics
- `GET /api/dashboard/stats` - Dashboard statistics
- `GET /api/analytics/usage` - Usage analytics
- `GET /api/audit-logs` - Audit logs

## Support

For issues or questions:
1. Check the IMPLEMENTATION_SUMMARY.md
2. Review the code comments
3. Check browser console for errors
4. Check Flask debug output

---

**Version**: 1.0  
**Last Updated**: 2025-10-22


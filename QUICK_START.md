# Quick Start Guide - Voice Assistant Management System v2.3

## Installation & Setup (5 minutes)

### 1. Clone Repository
```bash
git clone https://github.com/kosama685/ai-voice-assistant.git
cd ai-voice-assistant
```

### 2. Create Virtual Environment
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 5. Initialize Database
```bash
flask db upgrade
python -c "from models import initialize_database; initialize_database()"
```

### 6. Run Application
```bash
python run.py
```

The application will start at: **http://127.0.0.1:5000**

## Default Login Credentials

**Email**: admin@example.com
**Password**: admin123

## Admin Panel Features

### 1. **Dashboard** 📊 (`/admin/dashboard`)
- Real-time statistics (total users, active users, conversations)
- 30-day usage trends with Chart.js visualization
- System health indicators
- Recent activity feed
- Auto-refresh every 30 seconds

### 2. **User Management** 👥 (`/admin/users`)
- View all users with pagination
- Filter by role (admin, developer, tester, user)
- Filter by status (active, inactive)
- Edit user role and status
- Delete users with confirmation
- Track per-user usage statistics

### 3. **Prompt Management** 💬 (`/admin/prompts`)
- Create new system prompts
- Edit existing prompts
- Set personality (Friendly, Professional, Casual, Formal)
- Set tone (Conversational, Informative, Supportive, Neutral)
- Enable/disable prompts
- View prompt preview

### 4. **Real-time Monitoring** 📈 (`/admin/monitoring`)
- Active conversations counter
- Messages per minute tracking
- Average response time
- Error rate monitoring
- Real-time activity chart
- Recent messages log
- Configurable refresh rate (5s, 10s, 30s)
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


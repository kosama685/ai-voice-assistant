# Admin Panel Documentation

## Overview

The Voice Assistant Admin Panel provides comprehensive management tools for administrators to control users, prompts, monitor system performance, and manage subscriptions.

---

## Features

### 1. Dashboard
- **Real-time Statistics**: Total users, active users, conversations, success rate
- **Usage Trends**: 30-day usage analytics with Chart.js visualization
- **System Health**: Performance indicators and alerts
- **Recent Activity**: Latest user interactions and system events

**Access**: `/admin/dashboard`

### 2. User Management
- **User List**: View all users with pagination
- **Role Assignment**: Assign roles (admin, developer, tester, user)
- **Status Control**: Activate/deactivate users
- **User Actions**: Edit, delete, block users
- **Usage Statistics**: Per-user API usage and conversation count

**Access**: `/admin/users`

**API Endpoints**:
- `GET /admin/api/users?page=1&per_page=20` - List users
- `PUT /admin/api/users/<id>` - Update user
- `DELETE /admin/api/users/<id>` - Delete user

### 3. Prompt Management
- **Create Prompts**: Define system prompts with personality and tone
- **Edit Prompts**: Modify existing prompts
- **Version Control**: Track prompt changes
- **A/B Testing**: Compare prompt performance
- **Personality Settings**: Friendly, Professional, Casual, Formal
- **Tone Settings**: Conversational, Informative, Supportive, Neutral

**Access**: `/admin/prompts`

**API Endpoints**:
- `GET /admin/api/prompts` - List all prompts
- `POST /admin/api/prompts` - Create prompt
- `PUT /admin/api/prompts/<id>` - Update prompt
- `DELETE /admin/api/prompts/<id>` - Delete prompt

### 4. Real-time Monitoring
- **Active Conversations**: Live count of ongoing conversations
- **Messages Per Minute**: Real-time message throughput
- **Response Time**: Average API response time
- **Error Rate**: System error percentage
- **Activity Chart**: Real-time activity visualization
- **Recent Messages**: Latest messages with status

**Access**: `/admin/monitoring`

**Features**:
- Auto-refresh every 5/10/30 seconds (configurable)
- Real-time metrics updates
- Error log display
- System alerts

### 5. Analytics & Reports
- **Usage Trends**: Daily/weekly/monthly usage patterns
- **Most Used Functions**: Popular features and tools
- **Success vs Fallback Rates**: System reliability metrics
- **Session Duration**: Average conversation length
- **Export Options**: CSV, JSON, PDF formats

**Access**: `/admin/analytics`

### 6. System Configuration
- **API Keys**: Manage LLM, ASR, TTS provider keys
- **Webhooks**: Configure webhook endpoints
- **Feature Flags**: Enable/disable features
- **Rate Limiting**: Set API rate limits
- **Backup Settings**: Configure backup schedules

**Access**: `/admin/config`

---

## Access Control

### Role-Based Access

| Feature | Admin | Developer | Tester | User |
|---------|-------|-----------|--------|------|
| Dashboard | ✅ | ✅ | ✅ | ❌ |
| User Management | ✅ | ❌ | ❌ | ❌ |
| Prompt Management | ✅ | ✅ | ❌ | ❌ |
| Monitoring | ✅ | ✅ | ✅ | ❌ |
| Analytics | ✅ | ✅ | ✅ | ❌ |
| System Config | ✅ | ❌ | ❌ | ❌ |

### Authentication

All admin endpoints require:
1. User to be logged in (`@login_required`)
2. User to have admin role (`@admin_required`)

```python
@admin_bp.route('/api/users')
@login_required
@admin_required
def get_users():
    # Admin-only endpoint
    pass
```

---

## API Reference

### Dashboard Stats

```bash
GET /admin/api/dashboard/stats
```

**Response**:
```json
{
  "success": true,
  "stats": {
    "total_users": 150,
    "active_users": 45,
    "total_conversations": 1200,
    "today_conversations": 85,
    "success_rate": 98.5
  }
}
```

### User Management

**List Users**:
```bash
GET /admin/api/users?page=1&per_page=20&role=admin
```

**Update User**:
```bash
PUT /admin/api/users/123
Content-Type: application/json

{
  "role": "developer",
  "is_active": true
}
```

**Delete User**:
```bash
DELETE /admin/api/users/123
```

### Prompt Management

**Create Prompt**:
```bash
POST /admin/api/prompts
Content-Type: application/json

{
  "name": "Customer Support",
  "description": "Support agent prompt",
  "content": "You are a helpful customer support agent...",
  "personality": "friendly",
  "tone": "supportive"
}
```

**Update Prompt**:
```bash
PUT /admin/api/prompts/1
Content-Type: application/json

{
  "name": "Updated Name",
  "content": "Updated content...",
  "is_active": true
}
```

### Real-time Monitoring

```bash
GET /admin/api/monitoring/realtime
```

**Response**:
```json
{
  "success": true,
  "metrics": {
    "active_conversations": 12,
    "messages_per_minute": 45,
    "avg_response_time": 1.2,
    "error_rate": 0.5,
    "recent_messages": [
      {
        "id": 1,
        "text": "Hello",
        "status": "success",
        "created_at": "2025-10-26T10:30:00"
      }
    ]
  }
}
```

### Analytics

```bash
GET /admin/api/analytics/usage?days=30
```

**Response**:
```json
{
  "success": true,
  "analytics": {
    "daily_usage": [
      {"date": "2025-10-26", "count": 150},
      {"date": "2025-10-25", "count": 145}
    ],
    "total_messages": 4500,
    "total_tokens": 450000
  }
}
```

---

## Database Models

### User Model
```python
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
```

### Prompt Model
```python
class Prompt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False)
    personality = db.Column(db.String(50))
    tone = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

---

## Configuration

### Environment Variables

```env
# Admin Panel
ADMIN_PANEL_ENABLED=true
ADMIN_REFRESH_RATE=30  # seconds

# Database
DATABASE_URL=mysql://user:password@localhost/voiceast

# API Keys
GEMINI_API_KEY=your_key_here
```

---

## Security Best Practices

1. **Authentication**: All admin endpoints require login
2. **Authorization**: Role-based access control
3. **Audit Logging**: Track all admin actions
4. **Rate Limiting**: Prevent brute force attacks
5. **HTTPS**: Use SSL/TLS in production
6. **CSRF Protection**: Enable CSRF tokens
7. **Input Validation**: Validate all inputs
8. **SQL Injection**: Use parameterized queries

---

## Troubleshooting

### Admin Panel Not Loading
- Check user has admin role
- Verify authentication is working
- Check browser console for errors

### API Endpoints Returning 403
- Verify user is logged in
- Check user role is 'admin'
- Verify `@admin_required` decorator is applied

### Charts Not Displaying
- Check Chart.js is loaded
- Verify data is being returned from API
- Check browser console for JavaScript errors

### Database Connection Issues
- Verify DATABASE_URL is correct
- Check MySQL server is running
- Verify database credentials

---

## Performance Optimization

### Pagination
All list endpoints support pagination:
```bash
GET /admin/api/users?page=1&per_page=50
```

### Caching
Implement caching for frequently accessed data:
```python
@cache.cached(timeout=300)
def get_dashboard_stats():
    # Cached for 5 minutes
    pass
```

### Indexing
Database indexes for common queries:
- `users.email`
- `users.role`
- `conversations.user_id`
- `messages.created_at`

---

## Future Enhancements

- [ ] Advanced filtering and search
- [ ] Bulk user operations
- [ ] Custom report builder
- [ ] Email notifications
- [ ] Webhook integrations
- [ ] API rate limiting dashboard
- [ ] System health alerts
- [ ] Data export scheduling

---

**Last Updated**: 2025-10-26  
**Version**: 1.0  
**Status**: Production Ready


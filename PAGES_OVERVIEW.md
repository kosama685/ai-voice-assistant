# Voice Assistant Management System - Pages Overview

## 🗺️ Complete Site Map

```
Voice Assistant Management System
│
├── 🔐 Login Page
│   └── Email & Password Authentication
│
└── 📊 Main Application (After Login)
    │
    ├── 📈 Dashboard (/)
    │   ├── Statistics Cards (4)
    │   ├── Usage Trends Chart
    │   ├── Recent Activities Timeline
    │   ├── System Status
    │   ├── Top Functions Widget
    │   ├── Performance Metrics
    │   ├── Conversation Distribution Chart
    │   └── Quick Actions Panel
    │
    ├── 👥 User Management (/users)
    │   ├── User Statistics (4 cards)
    │   ├── Search Bar
    │   ├── User Directory Table
    │   ├── Role Distribution Chart
    │   ├── Status Distribution Chart
    │   ├── Add User Modal
    │   └── Export Button
    │
    ├── 💬 Prompt Management (/prompts-enhanced)
    │   ├── Prompt Statistics (4 cards)
    │   ├── Search & Filter
    │   ├── Prompt Library Table
    │   ├── Top Prompts Widget
    │   ├── Performance Chart
    │   ├── Create Prompt Modal
    │   └── Export Button
    │
    ├── 📈 Live Monitoring (/monitoring)
    │   ├── Live Statistics (4 cards)
    │   ├── Real-time Activity Chart
    │   ├── System Alerts
    │   ├── Recent Conversations Table
    │   └── Auto-refresh (30s)
    │
    ├── 📊 Analytics & Reports (/analytics-enhanced)
    │   ├── Date Range Selector
    │   ├── Key Metrics (4 cards)
    │   ├── Conversation Trends Chart
    │   ├── Response Time Distribution
    │   ├── Error Analysis Chart
    │   ├── Top Functions Report
    │   └── Export Options (CSV, JSON, PDF)
    │
    ├── ⚙️ System Configuration (/config)
    │   ├── Category Filters
    │   ├── Search Bar
    │   ├── Configuration Table
    │   ├── Add Configuration Modal
    │   └── Edit/Delete Operations
    │
    ├── 🔒 Security & Access (/security)
    │   ├── Role Permissions
    │   ├── Security Statistics
    │   ├── Audit Logs Table
    │   └── Status Indicators
    │
    ├── ⚙️ Settings & Profile (/settings)
    │   ├── User Profile Section
    │   ├── Account Security
    │   ├── Preferences
    │   ├── Notifications
    │   ├── API Keys
    │   └── System Settings
    │
    └── 🚪 Logout
        └── Session Termination
```

---

## 📄 Page Details

### 1. Dashboard (/)
**Purpose**: System overview and quick access

**Key Metrics**:
- Total Users: 42
- Conversations Today: 150
- Avg Response Time: 245ms
- Success Rate: 98.5%

**Visualizations**:
- Line Chart: 7-day trends
- Doughnut Chart: Conversation status
- Bar Chart: Performance metrics
- Timeline: Recent activities

**Quick Actions**:
- Add New User
- Create Prompt
- Configure System
- View Monitoring

---

### 2. User Management (/users)
**Purpose**: Manage system users

**Statistics**:
- Total Users: 42
- Active Users: 38
- Admins: 3
- Developers: 8

**Features**:
- Search by name/email
- View user details
- Add new users
- Edit user info
- Delete users
- Export as CSV

**Charts**:
- Pie: Role distribution
- Doughnut: Status distribution

**Table Columns**:
- User (with avatar)
- Email
- Role (badge)
- Status (badge)
- Usage (progress bar)
- Last Login
- Created Date
- Actions

---

### 3. Prompt Management (/prompts-enhanced)
**Purpose**: Manage system prompts

**Statistics**:
- Total Prompts: 15
- Active Prompts: 12
- Total Uses: 1,245
- Avg Rating: 4.5 ⭐

**Features**:
- Search prompts
- Filter by category
- View prompt library
- Create new prompts
- Edit prompts
- Delete prompts
- Export as CSV

**Categories**:
- General
- Customer Service
- Technical Support
- Sales
- Other

**Table Columns**:
- Name
- Category (badge)
- Status (badge)
- Uses (count)
- Rating (stars)
- Version
- Created Date
- Actions

---

### 4. Live Monitoring (/monitoring)
**Purpose**: Real-time system monitoring

**Live Metrics**:
- Active Users: 12
- Ongoing Conversations: 8
- Avg Response Time: 245ms
- Error Rate: 1.5%

**Features**:
- Real-time chart updates
- System alerts
- Recent conversations
- Auto-refresh (30s)
- Manual refresh button

**Alerts**:
- High CPU usage
- Database backup status
- System operational status

---

### 5. Analytics & Reports (/analytics-enhanced)
**Purpose**: Detailed analytics and reporting

**Filters**:
- Start Date selector
- End Date selector
- Metric type dropdown
- Update button

**Key Metrics**:
- Total Conversations: 1,245 (↑ +12%)
- Avg Response Time: 245ms (↓ -5%)
- Success Rate: 98.5% (↑ +2%)
- Total Users: 42 (↑ +8)

**Charts**:
- Line: Conversation trends
- Bar: Response time distribution
- Doughnut: Error analysis

**Reports**:
- Top functions
- Error breakdown
- Performance metrics

**Export Options**:
- CSV format
- JSON format
- PDF format (placeholder)

---

### 6. System Configuration (/config)
**Purpose**: Manage system settings

**Categories**:
- All
- LLM (Language Model)
- ASR (Speech Recognition)
- TTS (Text-to-Speech)
- Custom

**Features**:
- Search configurations
- Filter by category
- Add new config
- Edit config value
- Delete config
- Real-time updates

**Table Columns**:
- Key
- Value
- Category
- Description
- Actions (Edit/Delete)

---

### 7. Security & Access (/security)
**Purpose**: Security management

**Role Permissions**:
- Admin: Full access
- Developer: Create, Read, Update, Delete
- Tester: Read only

**Statistics**:
- Active Sessions: 12
- Recent Logins: 45
- Failed Attempts: 3

**Audit Logs**:
- Timestamp
- User ID
- Action (Create/Update/Delete)
- Resource Type
- Resource ID
- IP Address
- Status (Success/Failed)

---

### 8. Settings & Profile (/settings)
**Purpose**: User preferences and system settings

**Sections**:

**Profile**:
- Avatar upload
- Full name
- Email
- Phone
- Department
- Bio

**Account Security**:
- Change password
- Two-Factor Authentication
- Active sessions
- Device management

**Preferences**:
- Theme (Light/Dark/Auto)
- Language
- Timezone
- Date format

**Notifications**:
- Email notifications
- Push notifications
- SMS notifications
- Weekly reports

**API Keys**:
- View existing keys
- Generate new keys
- Revoke keys
- Track usage

**System Settings**:
- System version
- Database info
- Cache management
- Danger zone options

---

## 🎨 Visual Elements

### Statistics Cards
- Color-coded by metric type
- Large number display
- Subtitle description
- Trend indicator (if applicable)

### Charts
- **Line Charts**: Trends over time
- **Bar Charts**: Comparisons
- **Pie Charts**: Distribution
- **Doughnut Charts**: Status breakdown
- **Progress Bars**: Usage/capacity

### Tables
- Sortable columns
- Responsive design
- Action buttons
- Status badges
- Color-coded rows

### Modals
- Form inputs
- Validation
- Submit/Cancel buttons
- Close button

### Notifications
- Toast style
- Auto-dismiss (3s)
- Color-coded (success/error/info)
- Dismissible

---

## 🔄 Navigation Flow

### Sidebar Menu
1. Dashboard
2. User Management
3. Prompt & Logic
4. Live Monitoring
5. Analytics & Reports
6. System Configuration
7. Security & Access
8. Settings & Profile
9. Logout

### Top Header
- Page title
- User name
- User avatar
- Logout option

---

## 📱 Responsive Breakpoints

### Desktop (1200px+)
- Full sidebar
- Multi-column layouts
- All charts visible
- Full tables

### Tablet (768px-1199px)
- Sidebar visible
- 2-column layouts
- Stacked charts
- Responsive tables

### Mobile (<768px)
- Collapsible sidebar
- Single column
- Stacked components
- Touch-friendly buttons

---

## 🎯 User Workflows

### Adding a User
1. Click "Add New User" button
2. Fill in user details
3. Select role and status
4. Click "Add User"
5. See success notification

### Creating a Prompt
1. Click "Create Prompt" button
2. Enter prompt name
3. Select category
4. Write prompt content
5. Set status
6. Click "Create Prompt"

### Viewing Analytics
1. Select date range
2. Choose metric type
3. Click "Update"
4. View charts and reports
5. Export if needed

### Managing Configuration
1. Search or filter configs
2. Click "Edit" to modify
3. Enter new value
4. Click "Update"
5. Or click "Delete" to remove

---

## 📊 Data Display Standards

### Status Indicators
- 🟢 Green: Active, Success, Online
- 🔴 Red: Inactive, Error, Offline
- 🟡 Yellow: Warning, Pending
- 🔵 Blue: Info, Primary
- ⚫ Gray: Secondary, Disabled

### Badge Colors
- Primary (Blue): Default
- Success (Green): Active
- Danger (Red): Error/Delete
- Warning (Yellow): Caution
- Info (Cyan): Information
- Secondary (Gray): Inactive

---

**Last Updated**: 2025-10-22  
**Version**: 2.0


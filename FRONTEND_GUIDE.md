# Frontend Pages Guide - Voice Assistant Management System

## 🎨 Visual Layout & Components

### Page Structure
All pages follow a consistent layout:
```
┌─────────────────────────────────────────────────────────┐
│                    TOP HEADER                           │
│  Page Title                    User Info & Avatar       │
├──────────────┬──────────────────────────────────────────┤
│              │                                          │
│   SIDEBAR    │         MAIN CONTENT AREA               │
│   MENU       │                                          │
│              │  - Statistics Cards                      │
│  - Dashboard │  - Search/Filter Options                │
│  - Users     │  - Data Tables                          │
│  - Prompts   │  - Charts & Visualizations              │
│  - Monitoring│  - Action Buttons                       │
│  - Analytics │  - Modals & Forms                       │
│  - Config    │                                          │
│  - Security  │                                          │
│  - Settings  │                                          │
│  - Logout    │                                          │
└──────────────┴──────────────────────────────────────────┘
```

---

## 📄 Page Descriptions

### 1. **Dashboard** (/)
**Purpose**: System overview and quick access to key metrics

**Components:**
```
┌─ Statistics Cards (4 columns) ─────────────────────┐
│ Total Users │ Conversations │ Avg Response │ Success │
│     42      │      150      │    245ms     │  98.5%  │
└────────────────────────────────────────────────────┘

┌─ Usage Trends Chart ──────────────────────────────┐
│  Line Chart: 7-day conversation trends            │
│  X-axis: Dates | Y-axis: Conversation Count      │
└────────────────────────────────────────────────────┘

┌─ Recent Activities Timeline ──────────────────────┐
│  • User login - 2 minutes ago                     │
│  • Config updated - 15 minutes ago                │
│  • Prompt created - 1 hour ago                    │
└────────────────────────────────────────────────────┘

┌─ System Status ───────────────────────────────────┐
│ ● API Server (Online)  ● Database (Online)       │
│ ⚠ ASR Service (Warning) ● TTS Service (Online)   │
└────────────────────────────────────────────────────┘

┌─ Top Functions ───────────────────────────────────┐
│ Function Name          Uses                       │
│ • Get User Info        245 uses                   │
│ • Process Audio        189 uses                   │
│ • Generate Response    156 uses                   │
└────────────────────────────────────────────────────┘

┌─ Performance Metrics ──────────────────────────────┐
│ CPU Usage: ████░░░░░░ 45%                        │
│ Memory: ██████░░░░░░ 62%                         │
│ Disk: ████████░░░░░░ 78%                         │
│ Network: ███░░░░░░░░ 35%                         │
└────────────────────────────────────────────────────┘

┌─ Conversation Distribution ───────────────────────┐
│  Doughnut Chart:                                  │
│  • Active (45%) - Green                          │
│  • Completed (35%) - Blue                        │
│  • Error (20%) - Red                             │
└────────────────────────────────────────────────────┘

┌─ Quick Actions ───────────────────────────────────┐
│ [+ Add New User]  [+ Create Prompt]              │
│ [⚙ Configure System]  [📊 View Monitoring]       │
└────────────────────────────────────────────────────┘
```

---

### 2. **User Management** (/users)
**Purpose**: Manage system users and view user statistics

**Components:**
```
┌─ User Statistics (4 cards) ───────────────────────┐
│ Total Users │ Active Users │ Admins │ Developers  │
│     42      │      38      │   3    │     8       │
└────────────────────────────────────────────────────┘

┌─ Search & Actions ────────────────────────────────┐
│ [Search users...] [+ Add New User] [📥 Export]   │
└────────────────────────────────────────────────────┘

┌─ User Directory Table ────────────────────────────┐
│ User │ Email │ Role │ Status │ Usage │ Last Login │
├──────┼───────┼──────┼────────┼───────┼────────────┤
│ [👤] │ email │ Role │ Active │ 45/50 │ 2 min ago  │
│ John │ john@ │ Dev  │ Active │ ████░ │ 2 min ago  │
│ Jane │ jane@ │ Admin│ Active │ ██░░░ │ 1 hour ago │
│ Bob  │ bob@  │ Test │ Inactive│ ░░░░░ │ Never      │
└──────┴───────┴──────┴────────┴───────┴────────────┘

┌─ Role Distribution Chart ─────────────────────────┐
│  Pie Chart:                                       │
│  • Admin (3) - Red                               │
│  • Developer (8) - Blue                          │
│  • Tester (31) - Gray                            │
└────────────────────────────────────────────────────┘

┌─ Status Distribution Chart ───────────────────────┐
│  Doughnut Chart:                                  │
│  • Active (38) - Green                           │
│  • Inactive (4) - Red                            │
└────────────────────────────────────────────────────┘
```

---

### 3. **Prompt & Logic** (/prompts-enhanced)
**Purpose**: Manage system prompts and templates

**Components:**
```
┌─ Prompt Statistics (4 cards) ─────────────────────┐
│ Total Prompts │ Active │ Total Uses │ Avg Rating  │
│      15       │   12   │    1,245   │    4.5 ⭐   │
└────────────────────────────────────────────────────┘

┌─ Search & Actions ────────────────────────────────┐
│ [Search prompts...] [+ Create Prompt] [📥 Export]│
└────────────────────────────────────────────────────┘

┌─ Prompt Library Table ────────────────────────────┐
│ Name │ Category │ Status │ Uses │ Rating │ Version │
├──────┼──────────┼────────┼──────┼────────┼─────────┤
│ Greet│ General  │ Active │ 245  │ 4.8 ⭐ │ v1.2    │
│ Help │ Support  │ Active │ 189  │ 4.5 ⭐ │ v1.0    │
│ FAQ  │ General  │ Draft  │  45  │ 4.2 ⭐ │ v0.9    │
└──────┴──────────┴────────┴──────┴────────┴─────────┘

┌─ Top Prompts by Usage ────────────────────────────┐
│ Prompt Name          Uses                         │
│ • Greeting Prompt    245 uses                     │
│ • Help Prompt        189 uses                     │
│ • FAQ Prompt         156 uses                     │
└────────────────────────────────────────────────────┘

┌─ Prompt Performance Chart ────────────────────────┐
│  Bar Chart: Top 5 Prompts by Usage               │
│  Y-axis: Usage Count | X-axis: Prompt Names      │
└────────────────────────────────────────────────────┘
```

---

### 4. **Live Monitoring** (/monitoring)
**Purpose**: Real-time system monitoring and statistics

**Components:**
```
┌─ Live Statistics (4 cards) ───────────────────────┐
│ Active Users │ Conversations │ Avg Response │ Error │
│      12      │       8       │    245ms     │ 1.5%  │
└────────────────────────────────────────────────────┘

┌─ Real-time Activity Chart ────────────────────────┐
│  Line Chart: Live activity over last hour        │
│  Updates every 30 seconds                        │
└────────────────────────────────────────────────────┘

┌─ System Alerts ───────────────────────────────────┐
│ ⚠ High CPU usage detected (85%)                  │
│ ℹ Database backup completed successfully         │
│ ✓ All systems operational                        │
└────────────────────────────────────────────────────┘

┌─ Recent Conversations ────────────────────────────┐
│ User │ Duration │ Status │ Messages │ Timestamp   │
├──────┼──────────┼────────┼──────────┼─────────────┤
│ John │ 2m 30s   │ Active │    12    │ Just now    │
│ Jane │ 5m 15s   │ Active │    18    │ 1 min ago   │
│ Bob  │ 1m 45s   │ Ended  │     8    │ 3 min ago   │
└──────┴──────────┴────────┴──────────┴─────────────┘
```

---

### 5. **Analytics & Reports** (/analytics-enhanced)
**Purpose**: Detailed analytics and reporting

**Components:**
```
┌─ Date Range & Filters ────────────────────────────┐
│ [Start Date] [End Date] [Metric ▼] [Update]      │
└────────────────────────────────────────────────────┘

┌─ Key Metrics (4 cards) ───────────────────────────┐
│ Total Conv. │ Avg Response │ Success Rate │ Users  │
│    1,245    │    245ms     │    98.5%     │  42    │
│ ↑ +12%      │ ↓ -5%        │ ↑ +2%        │ ↑ +8   │
└────────────────────────────────────────────────────┘

┌─ Conversation Trends Chart ───────────────────────┐
│  Line Chart: Conversations over selected period  │
└────────────────────────────────────────────────────┘

┌─ Response Time Distribution ──────────────────────┐
│  Bar Chart: Response time buckets                │
│  0-100ms | 100-200ms | 200-300ms | 300-500ms    │
└────────────────────────────────────────────────────┘

┌─ Top Functions Report ────────────────────────────┐
│ Function Name          Uses                       │
│ • Get User Info        245 uses                   │
│ • Process Audio        189 uses                   │
│ • Generate Response    156 uses                   │
└────────────────────────────────────────────────────┘

┌─ Error Analysis ──────────────────────────────────┐
│  Doughnut Chart: Error Types                     │
│  • Timeout (35%)                                 │
│  • Invalid Input (25%)                           │
│  • Server Error (20%)                            │
│  • Auth Error (20%)                              │
└────────────────────────────────────────────────────┘

┌─ Export Options ──────────────────────────────────┐
│ [📄 Export PDF] [📊 Export CSV] [📋 Export JSON] │
└────────────────────────────────────────────────────┘
```

---

### 6. **System Configuration** (/config)
**Purpose**: Manage system settings and configurations

**Components:**
```
┌─ Configuration Categories ────────────────────────┐
│ [All] [LLM] [ASR] [TTS] [Custom]                 │
└────────────────────────────────────────────────────┘

┌─ Search & Actions ────────────────────────────────┐
│ [Search configs...] [+ Add Configuration]        │
└────────────────────────────────────────────────────┘

┌─ Configuration Table ─────────────────────────────┐
│ Key │ Value │ Category │ Description │ Actions    │
├─────┼───────┼──────────┼─────────────┼────────────┤
│ LLM │ GPT-4 │ LLM      │ Main LLM    │ ✏️ 🗑️     │
│ ASR │ Google│ ASR      │ Speech Rec. │ ✏️ 🗑️     │
│ TTS │ Azure │ TTS      │ Text-to-Sp. │ ✏️ 🗑️     │
└─────┴───────┴──────────┴─────────────┴────────────┘
```

---

### 7. **Security & Access** (/security)
**Purpose**: Security management and audit logs

**Components:**
```
┌─ Role Permissions ────────────────────────────────┐
│ Admin: [Create] [Read] [Update] [Delete] [Admin] │
│ Dev:   [Create] [Read] [Update] [Delete]         │
│ Test:  [Read]                                    │
└────────────────────────────────────────────────────┘

┌─ Security Statistics (3 cards) ───────────────────┐
│ Active Sessions │ Recent Logins │ Failed Attempts │
│       12        │      45       │        3        │
└────────────────────────────────────────────────────┘

┌─ Audit Logs Table ────────────────────────────────┐
│ Time │ User │ Action │ Resource │ IP │ Status     │
├──────┼──────┼────────┼──────────┼────┼────────────┤
│ 2:30 │ John │ Create │ User     │ IP │ ✓ Success  │
│ 2:15 │ Jane │ Update │ Config   │ IP │ ✓ Success  │
│ 2:00 │ Bob  │ Delete │ Prompt   │ IP │ ✗ Failed   │
└──────┴──────┴────────┴──────────┴────┴────────────┘
```

---

### 8. **Settings & Profile** (/settings)
**Purpose**: User profile and system preferences

**Components:**
```
┌─ Settings Navigation ─────────────────────────────┐
│ • Profile                                         │
│ • Account Security                                │
│ • Preferences                                     │
│ • Notifications                                   │
│ • API Keys                                        │
│ • System Settings                                 │
└────────────────────────────────────────────────────┘

┌─ Profile Section ─────────────────────────────────┐
│ [👤 Avatar]  Full Name: [________]               │
│              Email: [________]                    │
│              Phone: [________]                    │
│              Department: [________]               │
│              Bio: [________________]              │
│              [Save Changes]                       │
└────────────────────────────────────────────────────┘

┌─ Account Security ────────────────────────────────┐
│ Change Password:                                  │
│ Current: [________]                              │
│ New: [________]                                  │
│ Confirm: [________]                              │
│ [Update Password]                                │
│                                                  │
│ Two-Factor Auth: [Enable 2FA]                    │
│                                                  │
│ Active Sessions:                                 │
│ • Chrome on Windows - Just now [Logout]          │
│ • Safari on iPhone - 2 hours ago [Logout]        │
└────────────────────────────────────────────────────┘

┌─ API Keys ────────────────────────────────────────┐
│ Key Name │ Key │ Created │ Last Used │ Action     │
├──────────┼─────┼─────────┼───────────┼────────────┤
│ Prod Key │ sk_ │ Jan 15  │ Just now  │ [Revoke]   │
│ Dev Key  │ sk_ │ Jan 10  │ 2 days ago│ [Revoke]   │
└──────────┴─────┴─────────┴───────────┴────────────┘
```

---

## 🎯 Color Coding

### Status Badges:
- 🟢 **Green**: Active, Success, Online
- 🔴 **Red**: Inactive, Error, Offline, Danger
- 🟡 **Yellow**: Warning, Pending
- 🔵 **Blue**: Info, Primary
- ⚫ **Gray**: Secondary, Disabled

### Progress Bars:
- 🟢 Green: 0-50% (Good)
- 🟡 Yellow: 50-75% (Caution)
- 🔴 Red: 75-100% (Critical)

---

## 📱 Responsive Behavior

### Desktop (1200px+):
- Full sidebar visible
- Multi-column layouts
- All charts visible

### Tablet (768px-1199px):
- Sidebar visible but narrower
- 2-column layouts
- Stacked charts

### Mobile (<768px):
- Collapsible sidebar
- Single column layout
- Stacked components
- Touch-friendly buttons

---

**Last Updated**: 2025-10-22


# Voice Assistant Database - Entity Relationship Diagram (ERD)

## Database Schema Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         VOICE ASSISTANT DATABASE                            │
│                              (voiceast)                                      │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────┐         ┌──────────────────────┐
│      USERS           │         │    SUBSCRIPTIONS     │
├──────────────────────┤         ├──────────────────────┤
│ id (PK)              │◄────────│ id (PK)              │
│ username             │         │ user_id (FK)         │
│ email                │         │ tier                 │
│ password_hash        │         │ status               │
│ role                 │         │ start_date           │
│ is_active            │         │ end_date             │
│ created_at           │         │ auto_renew           │
│ last_login           │         │ created_at           │
└──────────────────────┘         └──────────────────────┘
         │                                │
         │                                │
         ├────────────────┬───────────────┤
         │                │               │
         ▼                ▼               ▼
┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
│   CONVERSATIONS      │  │    TRANSACTIONS      │  │   USAGE_STATS        │
├──────────────────────┤  ├──────────────────────┤  ├──────────────────────┤
│ id (PK)              │  │ id (PK)              │  │ id (PK)              │
│ user_id (FK)         │  │ user_id (FK)         │  │ user_id (FK)         │
│ title                │  │ amount               │  │ date                 │
│ status               │  │ currency             │  │ messages_count       │
│ created_at           │  │ payment_method       │  │ conversations_count  │
│ updated_at           │  │ status               │  │ tokens_used          │
└──────────────────────┘  │ created_at           │  │ created_at           │
         │                └──────────────────────┘  └──────────────────────┘
         │
         ▼
┌──────────────────────┐
│     MESSAGES         │
├──────────────────────┤
│ id (PK)              │
│ conversation_id (FK) │
│ user_id (FK)         │
│ text                 │
│ response_text        │
│ status               │
│ response_time        │
│ created_at           │
└──────────────────────┘


┌──────────────────────┐         ┌──────────────────────┐
│     PROMPTS          │         │   FUNCTIONS          │
├──────────────────────┤         ├──────────────────────┤
│ id (PK)              │         │ id (PK)              │
│ name                 │         │ name                 │
│ description          │         │ description          │
│ content              │         │ schema               │
│ personality          │         │ is_active            │
│ tone                 │         │ created_at           │
│ is_active            │         └──────────────────────┘
│ created_at           │
│ updated_at           │
└──────────────────────┘


┌──────────────────────┐         ┌──────────────────────┐
│   AUDIT_LOGS         │         │   SYSTEM_CONFIG      │
├──────────────────────┤         ├──────────────────────┤
│ id (PK)              │         │ id (PK)              │
│ user_id (FK)         │         │ key                  │
│ action               │         │ value                │
│ resource_type        │         │ description          │
│ resource_id          │         │ updated_at           │
│ changes              │         └──────────────────────┘
│ ip_address           │
│ created_at           │
└──────────────────────┘
```

---

## Table Definitions

### 1. USERS
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'developer', 'tester', 'user') DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    INDEX idx_email (email),
    INDEX idx_role (role)
);
```

### 2. SUBSCRIPTIONS
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
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status)
);
```

### 3. CONVERSATIONS
```sql
CREATE TABLE conversations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(255),
    status ENUM('active', 'archived', 'deleted') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
);
```

### 4. MESSAGES
```sql
CREATE TABLE messages (
    id INT PRIMARY KEY AUTO_INCREMENT,
    conversation_id INT NOT NULL,
    user_id INT NOT NULL,
    text TEXT NOT NULL,
    response_text TEXT,
    status ENUM('success', 'failed', 'pending') DEFAULT 'pending',
    response_time INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_conversation_id (conversation_id),
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
);
```

### 5. PROMPTS
```sql
CREATE TABLE prompts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    content TEXT NOT NULL,
    personality VARCHAR(50),
    tone VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_is_active (is_active)
);
```

### 6. FUNCTIONS
```sql
CREATE TABLE functions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    schema JSON,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_is_active (is_active)
);
```

### 7. TRANSACTIONS
```sql
CREATE TABLE transactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    payment_method ENUM('stripe', 'crypto', 'paypal') DEFAULT 'stripe',
    status ENUM('pending', 'completed', 'failed') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status)
);
```

### 8. USAGE_STATS
```sql
CREATE TABLE usage_stats (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    date DATE NOT NULL,
    messages_count INT DEFAULT 0,
    conversations_count INT DEFAULT 0,
    tokens_used INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_date (user_id, date),
    INDEX idx_date (date)
);
```

### 9. AUDIT_LOGS
```sql
CREATE TABLE audit_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    action VARCHAR(50) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id INT,
    changes JSON,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
);
```

### 10. SYSTEM_CONFIG
```sql
CREATE TABLE system_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    key VARCHAR(255) NOT NULL UNIQUE,
    value TEXT,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_key (key)
);
```

---

## Relationships

| From | To | Type | Cardinality |
|------|----|----|-------------|
| users | subscriptions | 1:N | One user has many subscriptions |
| users | conversations | 1:N | One user has many conversations |
| users | messages | 1:N | One user sends many messages |
| users | transactions | 1:N | One user has many transactions |
| users | usage_stats | 1:N | One user has many usage records |
| users | audit_logs | 1:N | One user performs many actions |
| conversations | messages | 1:N | One conversation has many messages |

---

## Indexes for Performance

- `users.email` - Fast user lookup by email
- `users.role` - Filter users by role
- `subscriptions.user_id` - Get user subscriptions
- `subscriptions.status` - Find active subscriptions
- `conversations.user_id` - Get user conversations
- `conversations.created_at` - Sort by date
- `messages.conversation_id` - Get conversation messages
- `messages.created_at` - Recent messages
- `transactions.user_id` - User transaction history
- `transactions.status` - Find pending transactions
- `usage_stats.date` - Daily analytics
- `audit_logs.created_at` - Recent audit logs

---

## Data Types & Constraints

- **Timestamps**: All tables have `created_at` and most have `updated_at`
- **Enums**: Used for status fields (role, tier, status)
- **Foreign Keys**: Cascade delete for data integrity
- **Unique Constraints**: Email, username, function names
- **JSON Fields**: For flexible schema (changes, schema)

---

## Backup & Recovery

```bash
# Backup database
mysqldump -u root -p voiceast > backup.sql

# Restore database
mysql -u root -p voiceast < backup.sql
```

---

**Database Version**: 1.0  
**Last Updated**: 2025-10-23  
**Status**: Production Ready


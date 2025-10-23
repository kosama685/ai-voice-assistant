#!/usr/bin/env python
"""
Script to manually add missing columns to the prompt table
"""
import MySQLdb
from config import Config

def fix_database():
    try:
        # Connect to MySQL
        conn = MySQLdb.connect(
            host=Config.DB_HOST,
            user=Config.DB_USERNAME,
            passwd=Config.DB_PASSWORD,
            db=Config.DB_DATABASE
        )
        cursor = conn.cursor()
        
        print("Connected to database successfully!")
        
        # Check if columns exist and add them if they don't
        columns_to_add = [
            ('category', "VARCHAR(50) DEFAULT 'general'"),
            ('usage_count', "INT DEFAULT 0"),
            ('rating', "FLOAT DEFAULT 0.0"),
            ('version', "INT DEFAULT 1")
        ]
        
        for col_name, col_type in columns_to_add:
            try:
                # Try to add the column
                query = f"ALTER TABLE prompt ADD COLUMN {col_name} {col_type}"
                cursor.execute(query)
                print(f"✓ Added column: {col_name}")
            except MySQLdb.OperationalError as e:
                if "Duplicate column name" in str(e):
                    print(f"✓ Column {col_name} already exists")
                else:
                    print(f"✗ Error adding {col_name}: {e}")
        
        # Create subscription table if it doesn't exist
        create_subscription_table = """
        CREATE TABLE IF NOT EXISTS subscription (
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
        )
        """
        
        try:
            cursor.execute(create_subscription_table)
            print("✓ Subscription table created or already exists")
        except MySQLdb.OperationalError as e:
            print(f"✗ Error creating subscription table: {e}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n✓ Database fix completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == '__main__':
    fix_database()


#!/usr/bin/env python
"""
Create default admin user for Voice Assistant
"""
import sys
from app import create_app, db
from models import User, Subscription
from datetime import datetime, timedelta

def create_admin_user():
    """Create default admin user"""
    app = create_app()
    
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(email='admin@voiceassistant.com').first()
        
        if admin:
            print("✓ Admin user already exists!")
            print(f"  Email: {admin.email}")
            print(f"  Name: {admin.name}")
            return True
        
        try:
            # Create admin user
            admin = User(
                name='Administrator',
                email='admin@voiceassistant.com',
                role='admin',
                status='active'
            )
            admin.set_password('Admin@123456')
            
            db.session.add(admin)
            db.session.commit()
            
            print("✓ Admin user created successfully!")
            print(f"  Email: admin@voiceassistant.com")
            print(f"  Password: Admin@123456")
            print(f"  Name: Administrator")
            
            # Create enterprise subscription for admin
            subscription = Subscription(
                user_id=admin.id,
                plan='enterprise',
                status='active',
                start_date=datetime.utcnow(),
                end_date=datetime.utcnow() + timedelta(days=365),
                price=0,
                billing_cycle='yearly',
                auto_renew=True
            )
            
            db.session.add(subscription)
            db.session.commit()
            
            print("\n✓ Enterprise subscription created for admin!")
            print(f"  Plan: Enterprise")
            print(f"  Status: Active")
            print(f"  Duration: 1 year")
            
            return True
            
        except Exception as e:
            print(f"✗ Error creating admin user: {e}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    print("=" * 60)
    print("CREATING DEFAULT ADMIN USER")
    print("=" * 60)
    print()
    
    success = create_admin_user()
    
    print()
    print("=" * 60)
    if success:
        print("✓ ADMIN USER SETUP COMPLETE")
        print("=" * 60)
        print("\nYou can now login with:")
        print("  Email: admin@voiceassistant.com")
        print("  Password: Admin@123456")
        sys.exit(0)
    else:
        print("✗ ADMIN USER SETUP FAILED")
        print("=" * 60)
        sys.exit(1)


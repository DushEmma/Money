#!/usr/bin/env python3
"""
Script to check admin accounts in the database
"""

import os
import sys
from flask import Flask
from models import db, User, Employer, Worker

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_admin_accounts():
    """Check admin accounts in the database"""
    app = Flask(__name__)
    
    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///umukozi.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    with app.app_context():
        try:
            # Check all admin users
            admin_users = User.query.filter_by(user_type='admin').all()
            
            print(f'🔍 Found {len(admin_users)} admin account(s) in database:')
            print('=' * 60)
            
            if admin_users:
                for i, admin in enumerate(admin_users, 1):
                    print(f'{i}. Admin User:')
                    print(f'   ID: {admin.id}')
                    print(f'   Name: {admin.full_name}')
                    print(f'   Email: {admin.email}')
                    print(f'   Phone: {admin.phone}')
                    print(f'   Is Active: {admin.is_active}')
                    print(f'   Is Approved: {admin.is_approved}')
                    print(f'   Is Blocked: {admin.is_blocked}')
                    print(f'   Created At: {admin.created_at}')
                    if admin.approved_at:
                        print(f'   Approved At: {admin.approved_at}')
                    if admin.blocked_at:
                        print(f'   Blocked At: {admin.blocked_at}')
                    print('-' * 40)
            else:
                print('❌ No admin accounts found in database')
                print('\n💡 To create an admin account, you can run:')
                print('   python create_admin.py')
                
            # Check all users by type for overview
            print('\n📊 User Overview:')
            print('=' * 60)
            total_users = User.query.count()
            admin_count = User.query.filter_by(user_type='admin').count()
            employer_count = User.query.filter_by(user_type='employer').count()
            worker_count = User.query.filter_by(user_type='worker').count()
            
            print(f'Total Users: {total_users}')
            print(f'Admin Users: {admin_count}')
            print(f'Employer Users: {employer_count}')
            print(f'Worker Users: {worker_count}')
            
            return len(admin_users) > 0
                
        except Exception as e:
            print(f'❌ Error checking admin accounts: {e}')
            return False

if __name__ == '__main__':
    print('🔍 Checking admin accounts in database...')
    success = check_admin_accounts()
    if success:
        print('\n🎉 Admin account check completed!')
    else:
        print('\n💥 No admin accounts found.')

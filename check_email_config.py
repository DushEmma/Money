#!/usr/bin/env python3
"""
Script to check email configuration in the database
"""

import os
import sys
from flask import Flask
from models import db, EmailConfig

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_email_config():
    """Check email configuration in the database"""
    app = Flask(__name__)
    
    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///umukozi.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    with app.app_context():
        try:
            email_config = EmailConfig.query.filter_by(is_active=True).first()
            if email_config:
                print('✅ Email configuration found in database:')
                print(f'   ID: {email_config.id}')
                print(f'   SMTP Server: {email_config.smtp_server}')
                print(f'   SMTP Port: {email_config.smtp_port}')
                print(f'   SMTP Encryption: {email_config.smtp_encryption}')
                print(f'   SMTP Username: {email_config.smtp_username}')
                print(f'   From Name: {email_config.from_name}')
                print(f'   Reply To: {email_config.reply_to}')
                print(f'   Notifications Enabled: {email_config.enable_notifications}')
                print(f'   Welcome Emails Enabled: {email_config.enable_welcome_emails}')
                print(f'   Job Alerts Enabled: {email_config.enable_job_alerts}')
                print(f'   Verification Emails Enabled: {email_config.enable_verification_emails}')
                print(f'   Is Active: {email_config.is_active}')
                print(f'   Created At: {email_config.created_at}')
                print(f'   Updated At: {email_config.updated_at}')
                return True
            else:
                print('❌ No email configuration found in database')
                return False
                
        except Exception as e:
            print(f'❌ Error checking email configuration: {e}')
            return False

if __name__ == '__main__':
    print('🔍 Checking email configuration in database...')
    success = check_email_config()
    if success:
        print('🎉 Email configuration is properly saved in database!')
    else:
        print('💥 No email configuration found in database.')

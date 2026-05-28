#!/usr/bin/env python3
"""
Script to create the EmailConfig table in the database
"""

import os
import sys
from flask import Flask
from models import db, EmailConfig

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_email_config_table():
    """Create the EmailConfig table if it doesn't exist"""
    app = Flask(__name__)
    
    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///umukozi.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    with app.app_context():
        try:
            # Create the EmailConfig table
            EmailConfig.__table__.create(db.engine, checkfirst=True)
            print("✅ EmailConfig table created successfully!")
            
            # Check if there's already an email config
            existing_config = EmailConfig.query.filter_by(is_active=True).first()
            if not existing_config:
                # Create default email config from environment variables
                default_config = EmailConfig(
                    smtp_server=os.getenv('SMTP_SERVER', ''),
                    smtp_port=int(os.getenv('SMTP_PORT', '587')),
                    smtp_encryption=os.getenv('SMTP_ENCRYPTION', 'tls'),
                    smtp_username=os.getenv('SMTP_USERNAME', ''),
                    smtp_password=os.getenv('SMTP_PASSWORD', ''),
                    from_name=os.getenv('EMAIL_FROM_NAME', 'Umukozi'),
                    reply_to=os.getenv('EMAIL_REPLY_TO', ''),
                    enable_notifications=os.getenv('ENABLE_EMAIL_NOTIFICATIONS', 'true').lower() == 'true',
                    enable_welcome_emails=os.getenv('ENABLE_WELCOME_EMAILS', 'true').lower() == 'true',
                    enable_job_alerts=os.getenv('ENABLE_JOB_ALERTS', 'true').lower() == 'true',
                    enable_verification_emails=os.getenv('ENABLE_VERIFICATION_EMAILS', 'true').lower() == 'true'
                )
                db.session.add(default_config)
                db.session.commit()
                print("✅ Default email configuration created!")
            else:
                print("ℹ️  Email configuration already exists in database.")
                
        except Exception as e:
            print(f"❌ Error creating EmailConfig table: {e}")
            return False
    
    return True

if __name__ == '__main__':
    print("🔧 Creating EmailConfig table...")
    success = create_email_config_table()
    if success:
        print("🎉 EmailConfig table setup completed!")
    else:
        print("💥 Failed to create EmailConfig table.")
        sys.exit(1)

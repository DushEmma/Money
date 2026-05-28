#!/usr/bin/env python3
"""
Database initialization script for Umukozi deployment
This script creates all database tables and sets up initial data
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User, Worker, Employer, Job, Application, Review, Message, Notification, Payment, WorkerContactAccess, AdminMessage, AdminNotification, MessageTemplate, NotificationPreference

def run_migrations():
    """Run schema migrations to add missing columns"""
    print("🔄 Running schema migrations...")
    from sqlalchemy import text
    
    try:
        inspector = db.inspect(db.engine)
        
        # 0. Update User table first
        user_columns = [col['name'] for col in inspector.get_columns('user')]
        missing_user_cols = [
            ('is_active', 'BOOLEAN'),
            ('is_approved', 'BOOLEAN'),
            ('is_blocked', 'BOOLEAN'),
            ('approved_at', 'TIMESTAMP'),
            ('approved_by', 'INTEGER'),
            ('blocked_at', 'TIMESTAMP'),
            ('blocked_by', 'INTEGER'),
            ('rejection_reason', 'TEXT')
        ]
        
        for col_name, col_type in missing_user_cols:
            if col_name not in user_columns:
                print(f"   Adding column user.{col_name}...")
                with db.engine.connect() as conn:
                    if col_name.endswith('_by'):
                        conn.execute(text(f"ALTER TABLE \"user\" ADD COLUMN {col_name} {col_type} REFERENCES \"user\"(id)"))
                    else:
                        conn.execute(text(f"ALTER TABLE \"user\" ADD COLUMN {col_name} {col_type}"))
                    conn.commit()
                print(f"   ✅ Added user.{col_name}")
        
        # 1. Update Worker table
        worker_columns = [col['name'] for col in inspector.get_columns('worker')]
        missing_worker_cols = [
            ('age', 'INTEGER'),
            ('date_of_birth', 'DATE'),
            ('id_photo', 'VARCHAR(200)'),
            ('experience_details', 'TEXT'),
            ('reference_name', 'VARCHAR(100)'),
            ('reference_phone', 'VARCHAR(20)'),
            ('reference_relationship', 'VARCHAR(50)'),
            ('national_id_number', 'VARCHAR(30)')
        ]
        
        for col_name, col_type in missing_worker_cols:
            if col_name not in worker_columns:
                print(f"   Adding column worker.{col_name}...")
                with db.engine.connect() as conn:
                    conn.execute(text(f"ALTER TABLE worker ADD COLUMN {col_name} {col_type}"))
                    conn.commit()
                print(f"   ✅ Added worker.{col_name}")
        
        # 2. Update Notification table
        notification_columns = [col['name'] for col in inspector.get_columns('notification')]
        missing_notif_cols = [
            ('title', 'VARCHAR(255)'),
            ('notification_type', 'VARCHAR(50)'),
            ('action_url', 'VARCHAR(500)'),
            ('action_text', 'VARCHAR(100)'),
            ('related_user_id', 'INTEGER'),
            ('related_job_id', 'INTEGER')
        ]
        
        for col_name, col_type in missing_notif_cols:
            if col_name not in notification_columns:
                print(f"   Adding column notification.{col_name}...")
                with db.engine.connect() as conn:
                    if col_name.endswith('_id'):
                        ref_table = col_name.split('_')[1] # user or job
                        conn.execute(text(f"ALTER TABLE notification ADD COLUMN {col_name} {col_type} REFERENCES \"{ref_table}\"(id)"))
                    else:
                        conn.execute(text(f"ALTER TABLE notification ADD COLUMN {col_name} {col_type}"))
                    conn.commit()
                print(f"   ✅ Added notification.{col_name}")

        # 3. Update WorkerContactAccess table
        wca_columns = [col['name'] for col in inspector.get_columns('worker_contact_access')]
        missing_wca_cols = [
            ('created_at', 'TIMESTAMP'),
            ('granted_at', 'TIMESTAMP'),
            ('expires_at', 'TIMESTAMP'),
            ('access_granted', 'BOOLEAN'),
            ('phone_visible', 'BOOLEAN'),
            ('email_visible', 'BOOLEAN'),
            ('whatsapp_accessible', 'BOOLEAN')
        ]
        
        for col_name, col_type in missing_wca_cols:
            if col_name not in wca_columns:
                print(f"   Adding column worker_contact_access.{col_name}...")
                with db.engine.connect() as conn:
                    conn.execute(text(f"ALTER TABLE worker_contact_access ADD COLUMN {col_name} {col_type}"))
                    conn.commit()
                print(f"   ✅ Added worker_contact_access.{col_name}")

        # 4. Update Job table
        job_columns = [col['name'] for col in inspector.get_columns('job')]
        if 'deadline' not in job_columns:
            print("   Adding column job.deadline...")
            with db.engine.connect() as conn:
                conn.execute(text("ALTER TABLE job ADD COLUMN deadline DATE"))
                conn.commit()
            print("   ✅ Added job.deadline")

        # 5. Update Payment table
        payment_columns = [col['name'] for col in inspector.get_columns('payment')]
        if 'verified_by' not in payment_columns:
            print("   Adding column payment.verified_by...")
            with db.engine.connect() as conn:
                conn.execute(text("ALTER TABLE payment ADD COLUMN verified_by INTEGER REFERENCES \"user\"(id)"))
                conn.commit()
            print("   ✅ Added payment.verified_by")

        # 3. Update EmailConfig table (if exists)
        try:
            email_config_columns = [col['name'] for col in inspector.get_columns('email_config')]
            if email_config_columns and 'created_by' not in email_config_columns:
                print("   Adding column email_config.created_by...")
                with db.engine.connect() as conn:
                    conn.execute(text("ALTER TABLE email_config ADD COLUMN created_by INTEGER REFERENCES \"user\"(id)"))
                    conn.commit()
                print("   ✅ Added email_config.created_by")
        except:
            pass # Table might not exist yet
            
        print("✅ Schema migrations completed!")
        return True
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        return True

def init_database():
    """Initialize database with all tables"""
    print("🔧 Initializing database...")
    
    with app.app_context():
        try:
            # Create all tables
            print("📊 Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Run migrations to add missing columns
            run_migrations()
            
            # Check if admin user exists
            admin_user = User.query.filter_by(user_type='admin').first()
            if not admin_user:
                print("👤 Creating default admin user...")
                from werkzeug.security import generate_password_hash
                
                admin = User(
                    email='admin@umukozi.rw',
                    password=generate_password_hash('admin123', method='pbkdf2:sha256'),
                    full_name='System Administrator',
                    phone='+250000000000',
                    user_type='admin',
                    is_approved=True,
                    is_active=True
                )
                db.session.add(admin)
                db.session.commit()
                print("✅ Default admin user created!")
                print("   Email: admin@umukozi.rw")
                print("   Password: admin123")
                print("   ⚠️  Please change this password after first login!")
            else:
                print("✅ Admin user already exists")
            
            print("🎉 Database initialization completed successfully!")
            
        except Exception as e:
            print(f"❌ Database initialization failed: {str(e)}")
            return False
    
    return True

def check_database_connection():
    """Test database connection"""
    print("🔍 Testing database connection...")
    
    with app.app_context():
        try:
            # Test connection by executing a simple query
            from sqlalchemy import text
            result = db.session.execute(text('SELECT 1'))
            print("✅ Database connection successful!")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {str(e)}")
            return False

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Umukozi Database Initialization")
    print("=" * 50)
    
    # Check environment
    database_url = os.getenv('DATABASE_URL', 'sqlite:///umukozi.db')
    print(f"📡 Database URL: {database_url}")
    
    # Test connection first
    if check_database_connection():
        # Initialize database
        if init_database():
            print("\n✨ Ready to start the application!")
        else:
            print("\n❌ Database initialization failed!")
            sys.exit(1)
    else:
        print("\n❌ Cannot connect to database!")
        sys.exit(1)

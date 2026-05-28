#!/usr/bin/env python3
"""
Migration script to create the SystemSettings table and insert default settings.
Run this script to add the SystemSettings table to your existing database.
"""

import sys
import os

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import SystemSettings

def create_system_settings_table():
    """Create SystemSettings table and insert default settings"""
    
    with app.app_context():
        try:
            # Create the table
            db.create_all()
            
            # Check if settings already exist
            existing_settings = SystemSettings.query.first()
            if existing_settings:
                print("✅ SystemSettings table already exists with data.")
                print(f"Current settings: reg={existing_settings.allow_registration}, jobs={existing_settings.allow_job_posting}, apps={existing_settings.allow_job_applications}")
                return
            
            # Create default settings
            default_settings = SystemSettings(
                allow_registration=True,
                allow_job_posting=True,
                allow_job_applications=True,
                is_active=True
            )
            
            db.session.add(default_settings)
            db.session.commit()
            
            print("✅ SystemSettings table created successfully!")
            print("📋 Default settings inserted:")
            print(f"   - User Registration: {'Enabled' if default_settings.allow_registration else 'Disabled'}")
            print(f"   - Job Posting: {'Enabled' if default_settings.allow_job_posting else 'Disabled'}")
            print(f"   - Job Applications: {'Enabled' if default_settings.allow_job_applications else 'Disabled'}")
            
        except Exception as e:
            print(f"❌ Error creating SystemSettings table: {e}")
            db.session.rollback()
            sys.exit(1)

if __name__ == "__main__":
    print("🔧 Creating SystemSettings table...")
    create_system_settings_table()
    print("✨ Migration completed successfully!")

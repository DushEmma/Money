#!/usr/bin/env python3
"""
Migration script to add the missing 'title' column to the notifications table.
This fixes the 500 error during registration.
"""

import os
import sys
from sqlalchemy import text

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db

def add_notification_title_column():
    """Add the title column to the notifications table"""
    with app.app_context():
        try:
            # Check if the column already exists
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('notification')]
            
            if 'title' not in columns:
                print("Adding 'title' column to notifications table...")
                
                # Add the column
                db.session.execute(text("""
                    ALTER TABLE notification 
                    ADD COLUMN title VARCHAR(255) NOT NULL DEFAULT 'Notification'
                """))
                
                db.session.commit()
                print("✅ Successfully added 'title' column to notifications table")
                
                # Update existing notifications with appropriate titles
                db.session.execute(text("""
                    UPDATE notification 
                    SET title = CASE 
                        WHEN message LIKE '%Welcome%' THEN 'Welcome to Umukozi!'
                        WHEN message LIKE '%application%' THEN 'Job Application Update'
                        WHEN message LIKE '%payment%' THEN 'Payment Update'
                        ELSE 'Notification'
                    END
                    WHERE title = 'Notification'
                """))
                
                db.session.commit()
                print("✅ Updated existing notifications with appropriate titles")
                
            else:
                print("✅ 'title' column already exists in notifications table")
                
        except Exception as e:
            print(f"❌ Error adding title column: {e}")
            db.session.rollback()
            return False
            
        return True

if __name__ == "__main__":
    print("🔄 Running notification title column migration...")
    success = add_notification_title_column()
    
    if success:
        print("✅ Migration completed successfully!")
        print("🎉 Registration should now work without 500 errors.")
    else:
        print("❌ Migration failed. Please check the error above.")
        sys.exit(1)

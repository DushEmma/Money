#!/usr/bin/env python3
"""
Migration script to add the deadline column to the jobs table.
This adds the application deadline feature for job postings.
"""

import os
import sys
from sqlalchemy import text

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db

def add_job_deadline_column():
    """Add the deadline column to the jobs table"""
    with app.app_context():
        try:
            # Check if the column already exists
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('job')]
            
            if 'deadline' not in columns:
                print("Adding 'deadline' column to jobs table...")
                
                # Add the column
                db.session.execute(text("""
                    ALTER TABLE job 
                    ADD COLUMN deadline DATE
                """))
                
                db.session.commit()
                print("✅ Successfully added 'deadline' column to jobs table")
                
                # Set default deadline for existing jobs (30 days from creation)
                db.session.execute(text("""
                    UPDATE job 
                    SET deadline = DATE(created_at, '+30 days')
                    WHERE deadline IS NULL AND created_at IS NOT NULL
                """))
                
                db.session.commit()
                print("✅ Set default deadlines for existing jobs")
                
            else:
                print("✅ 'deadline' column already exists in jobs table")
                
        except Exception as e:
            print(f"❌ Error adding deadline column: {e}")
            db.session.rollback()
            return False
            
        return True

if __name__ == "__main__":
    print("🔄 Running job deadline column migration...")
    success = add_job_deadline_column()
    
    if success:
        print("✅ Migration completed successfully!")
        print("🎉 Job postings can now have application deadlines.")
    else:
        print("❌ Migration failed. Please check the error above.")
        sys.exit(1)

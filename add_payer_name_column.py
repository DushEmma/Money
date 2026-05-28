#!/usr/bin/env python3
"""
Database migration script to add payer_name column to Payment table
"""

import sqlite3
import os
from datetime import datetime

def add_payer_name_column():
    """Add payer_name column to Payment table"""
    
    # Database path
    db_path = 'umukozi.db'
    
    if not os.path.exists(db_path):
        print(f"Database file {db_path} not found!")
        return False
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(payment)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'payer_name' in columns:
            print("payer_name column already exists in Payment table")
            return True
        
        # Add the column
        print("Adding payer_name column to Payment table...")
        cursor.execute("""
            ALTER TABLE payment 
            ADD COLUMN payer_name VARCHAR(100)
        """)
        
        # Commit changes
        conn.commit()
        print("✅ payer_name column added successfully!")
        
        # Verify the column was added
        cursor.execute("PRAGMA table_info(payment)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'payer_name' in columns:
            print("✅ Column verification successful!")
            return True
        else:
            print("❌ Column verification failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error adding column: {str(e)}")
        return False
        
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("=" * 50)
    print("Database Migration: Add payer_name Column")
    print("=" * 50)
    
    success = add_payer_name_column()
    
    if success:
        print("\n✅ Migration completed successfully!")
    else:
        print("\n❌ Migration failed!")
    
    print("=" * 50)

#!/usr/bin/env python3
"""
Create payment table and fix null worker_id issue
"""

import os
import sqlite3
from datetime import datetime

def create_payment_table():
    """Create payment table with proper structure"""
    
    # Database path
    db_path = 'umukozi.db'
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create payment table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employer_id INTEGER NOT NULL,
                worker_id INTEGER NOT NULL,
                amount REAL NOT NULL DEFAULT 10000.00,
                payment_method VARCHAR(50) DEFAULT 'momo',
                transaction_id VARCHAR(100),
                phone_number VARCHAR(20),
                status VARCHAR(20) DEFAULT 'pending',
                verification_code VARCHAR(10),
                screenshot_path VARCHAR(200),
                verified_by INTEGER,
                paid_at DATETIME,
                verified_at DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employer_id) REFERENCES user(id),
                FOREIGN KEY (worker_id) REFERENCES worker(id)
            )
        ''')
        
        conn.commit()
        print("✅ Payment table created successfully!")
        
        # Check for null worker_id records
        cursor.execute("SELECT id, employer_id, worker_id, amount FROM payment WHERE worker_id IS NULL")
        null_payments = cursor.fetchall()
        
        if null_payments:
            print(f"\n⚠️  Found {len(null_payments)} payment(s) with null worker_id:")
            for payment in null_payments:
                print(f"  ID: {payment[0]}, Employer: {payment[1]}, Amount: {payment[2]}, Worker: NULL")
            
            # Fix null worker_id by setting to a default value
            cursor.execute("UPDATE payment SET worker_id = 0 WHERE worker_id IS NULL")
            conn.commit()
            print(f"✅ Fixed {len(null_payments)} payment records by setting worker_id = 0")
        
        return True
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("Create payment table and fix null worker_id")
    print("=" * 50)
    
    success = create_payment_table()
    
    if success:
        print("\nOperation completed successfully!")
    else:
        print("\nOperation completed with errors.")

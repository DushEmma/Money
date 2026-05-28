#!/usr/bin/env python3
"""
Fix specific payment record with null worker_id
This script targets the specific payment record mentioned in the error.
"""

import os
import sqlite3
from datetime import datetime

def fix_specific_payment():
    """Fix the specific payment record with null worker_id"""
    
    # Database path
    db_path = 'umukozi.db'
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if the specific payment record exists
        cursor.execute("""
            SELECT id, employer_id, worker_id, amount, payment_method, transaction_id, phone_number, status, created_at
            FROM payment 
            WHERE id = 1 AND worker_id IS NULL
        """)
        
        payment = cursor.fetchone()
        
        if payment:
            print(f"Found payment record with null worker_id:")
            print(f"  ID: {payment[0]}")
            print(f"  Employer ID: {payment[1]}")
            print(f"  Worker ID: {payment[2]} (NULL)")
            print(f"  Amount: {payment[3]}")
            print(f"  Payment Method: {payment[4]}")
            print(f"  Transaction ID: {payment[5]}")
            print(f"  Phone: {payment[6]}")
            print(f"  Status: {payment[7]}")
            print(f"  Created: {payment[8]}")
            
            # Ask for confirmation
            response = input(f"\nDelete this payment record? (y/N): ")
            if response.lower() == 'y':
                # Delete the problematic record
                cursor.execute("DELETE FROM payment WHERE id = 1")
                conn.commit()
                print("Successfully deleted payment record with null worker_id.")
                return True
            else:
                print("Operation cancelled.")
                return False
        else:
            print("No payment record with ID=1 and null worker_id found.")
            return False
            
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
    print("Fix specific payment record with null worker_id")
    print("=" * 50)
    
    success = fix_specific_payment()
    
    if success:
        print("\nOperation completed successfully!")
    else:
        print("\nOperation completed (no changes needed).")

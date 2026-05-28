#!/usr/bin/env python3
"""
Fix payment record with null worker_id violating not-null constraint
This script finds and fixes payment records with null worker_id values.
"""

import os
import sqlite3

def fix_payment_null_constraint():
    """Fix payment records with null worker_id"""
    
    # Database path
    db_path = 'umukozi.db'
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Find all payment records with null worker_id
        cursor.execute("""
            SELECT id, employer_id, worker_id, amount, payment_method, transaction_id, phone_number, status, created_at
            FROM payment 
            WHERE worker_id IS NULL
        """)
        
        null_payments = cursor.fetchall()
        
        if null_payments:
            print(f"Found {len(null_payments)} payment(s) with null worker_id:")
            for payment in null_payments:
                print(f"  ID: {payment[0]}, Employer: {payment[1]}, Amount: {payment[2]}, Method: {payment[3]}")
                
            # Option 1: Update with a valid worker_id (if we know it)
            # Option 2: Delete the problematic records
            print("\nOptions:")
            print("1. Update with valid worker_id (if known)")
            print("2. Delete problematic records")
            
            choice = input("Choose option (1/2): ")
            
            if choice == "1":
                worker_id = input("Enter valid worker_id: ")
                if worker_id.isdigit():
                    cursor.execute("UPDATE payment SET worker_id = ? WHERE id = ?", (int(worker_id),))
                    conn.commit()
                    print(f"Updated payment record {payment[0]} with worker_id {worker_id}")
                else:
                    print("Invalid worker_id format.")
                    return False
                    
            elif choice == "2":
                # Delete the problematic records
                cursor.execute("DELETE FROM payment WHERE worker_id IS NULL")
                conn.commit()
                print(f"Successfully deleted {len(null_payments)} payment records.")
                
            else:
                print("Invalid choice.")
                return False
                
        else:
            print("No payment records with null worker_id found.")
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
    print("Fix payment null constraint violation")
    print("=" * 50)
    
    success = fix_payment_null_constraint()
    
    if success:
        print("\nOperation completed successfully!")
    else:
        print("\nOperation completed with issues.")

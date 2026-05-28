#!/usr/bin/env python3
"""
Fix null worker_id in payment table
This script fixes the database error where a payment record has null worker_id
violating the not-null constraint.
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def fix_null_worker_id():
    """Fix payment record with null worker_id"""
    
    # Database URL from environment or default
    database_url = os.getenv('DATABASE_URL', 'sqlite:///umukozi.db')
    
    try:
        # Create database engine
        engine = create_engine(database_url)
        
        with engine.connect() as connection:
            # First, check the problematic payment record
            result = connection.execute(text("""
                SELECT id, employer_id, worker_id, amount, payment_method, transaction_id, phone_number, status, created_at
                FROM payment 
                WHERE worker_id IS NULL
            """))
            
            null_payments = result.fetchall()
            
            if null_payments:
                print(f"Found {len(null_payments)} payment(s) with null worker_id:")
                for payment in null_payments:
                    print(f"  Payment ID: {payment[0]}, Employer ID: {payment[1]}, Amount: {payment[2]}")
                
                # Ask user for confirmation before proceeding
                response = input(f"\nDo you want to DELETE these {len(null_payments)} payment record(s) with null worker_id? (y/N): ")
                if response.lower() != 'y':
                    print("Operation cancelled.")
                    return False
                
                # Delete the problematic payment records
                print("\nDeleting payment records with null worker_id...")
                connection.execute(text("DELETE FROM payment WHERE worker_id IS NULL"))
                connection.commit()
                print(f"Successfully deleted {len(null_payments)} payment records.")
                
                return True
            else:
                print("No payment records with null worker_id found.")
                return False
                
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("Fix null worker_id in payment table")
    print("=" * 50)
    
    success = fix_null_worker_id()
    
    if success:
        print("\nOperation completed successfully!")
    else:
        print("\nOperation completed (no changes needed).")

#!/usr/bin/env python3
"""
Database migration script to ensure all Worker table columns exist.
Adds missing columns that are needed for the profile completion feature.
Handles both SQLite (development) and PostgreSQL (production).
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, Column, String, Integer, Date, Text, Float, Boolean
from sqlalchemy.orm import sessionmaker
import logging

load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# Database connection
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///umukozi.db')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def check_and_add_worker_columns():
    """Check if Worker table has all required columns, add missing ones"""
    
    inspector = inspect(engine)
    
    # Check if Worker table exists
    if 'worker' not in inspector.get_table_names():
        logger.error("Worker table does not exist!")
        return False
    
    # Get existing columns
    existing_columns = {col['name'].lower() for col in inspector.get_columns('worker')}
    
    # Required columns for profile completion
    required_columns = {
        'id_photo',
        'experience_details',
        'reference_name',
        'reference_phone',
        'reference_relationship',
        'national_id_number'
    }
    
    # Check which columns are missing
    missing_columns = required_columns - existing_columns
    
    if not missing_columns:
        logger.info("✅ All required Worker columns already exist!")
        return True
    
    logger.info(f"Found missing columns: {missing_columns}")
    
    # Add missing columns
    try:
        session = Session()
        connection = engine.raw_connection()
        cursor = connection.cursor()
        
        # Column definitions for different database types
        column_definitions = {
            'id_photo': 'VARCHAR(200)',
            'experience_details': 'TEXT',
            'reference_name': 'VARCHAR(100)',
            'reference_phone': 'VARCHAR(20)',
            'reference_relationship': 'VARCHAR(50)',
            'national_id_number': 'VARCHAR(30)'
        }
        
        # Check database type
        is_postgres = 'postgresql' in DATABASE_URL.lower()
        
        for column_name in missing_columns:
            try:
                if is_postgres:
                    # PostgreSQL syntax
                    sql = f'ALTER TABLE "worker" ADD COLUMN "{column_name}" {column_definitions[column_name]};'
                else:
                    # SQLite syntax
                    sql = f'ALTER TABLE worker ADD COLUMN {column_name} {column_definitions[column_name]};'
                
                cursor.execute(sql)
                connection.commit()
                logger.info(f"✅ Added column: {column_name}")
            except Exception as col_err:
                # Column might already exist, continue
                logger.warning(f"⚠️ Could not add {column_name}: {str(col_err)}")
                connection.rollback()
        
        connection.close()
        session.close()
        
        logger.info("✅ Worker table columns check completed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error adding columns: {str(e)}")
        return False

def verify_columns():
    """Verify that all required columns now exist"""
    
    inspector = inspect(engine)
    existing_columns = {col['name'].lower() for col in inspector.get_columns('worker')}
    
    required_columns = {
        'id_photo',
        'experience_details',
        'reference_name',
        'reference_phone',
        'reference_relationship',
        'national_id_number'
    }
    
    missing = required_columns - existing_columns
    
    if not missing:
        logger.info("✅ All required columns verified to exist!")
        return True
    else:
        logger.error(f"❌ Still missing columns: {missing}")
        return False

if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("🔄 Worker Table Column Migration")
    logger.info("=" * 60)
    
    try:
        success = check_and_add_worker_columns()
        if success:
            verify_columns()
            logger.info("\n✅ Migration completed successfully!")
        else:
            logger.info("\n❌ Migration encountered issues. See above for details.")
    except Exception as e:
        logger.error(f"\n❌ Migration failed: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

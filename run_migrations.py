#!/usr/bin/env python3
"""
Production migration runner script.
This script runs all database migrations needed for deployment.
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_migration(script_name, description):
    """Run a migration script and return success status"""
    print(f"\n🔄 Running {description}...")
    try:
        if os.path.exists(script_name):
            # Import and run the migration
            import importlib.util
            spec = importlib.util.spec_from_file_location(script_name[:-3], script_name)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Check if the main function exists and run it
            if hasattr(module, 'main') or hasattr(module, '__main__'):
                if hasattr(module, 'main'):
                    success = module.main()
                else:
                    # Run the script directly
                    success = True
                    print(f"✅ {description} completed")
            else:
                success = True
                print(f"✅ {description} completed")
                
            return success
        else:
            print(f"❌ Migration script {script_name} not found")
            return False
            
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False

def main():
    """Run all required migrations"""
    print("🚀 Starting production database migrations...")
    
    migrations = [
        ("add_job_deadline_column.py", "Job deadline column migration"),
        ("add_notification_title_column.py", "Notification title column migration"),
    ]
    
    success_count = 0
    total_count = len(migrations)
    
    for script_name, description in migrations:
        if run_migration(script_name, description):
            success_count += 1
        else:
            print(f"❌ Failed to run {description}")
            return False
    
    print(f"\n✅ Successfully ran {success_count}/{total_count} migrations")
    print("🎉 Production database is now up to date!")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("❌ Migration process failed. Please check the errors above.")
        sys.exit(1)
    else:
        print("✅ All migrations completed successfully!")

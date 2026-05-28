#!/usr/bin/env python3
"""
Deployment setup script for Umukozi
This script helps set up the environment and database for deployment
"""

import os
import sys
import subprocess

def check_requirements():
    """Check if required packages are installed"""
    print("🔍 Checking requirements...")
    
    required_packages = [
        'flask',
        'flask_sqlalchemy', 
        'flask_login',
        'werkzeug',
        'python-dotenv',
        'psycopg2-binary'  # For PostgreSQL
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
        print("✅ All packages installed!")
    else:
        print("✅ All required packages are installed!")

def setup_environment():
    """Set up environment variables"""
    print("\n🌍 Setting up environment...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("📝 Creating .env file from template...")
        
        # Read template
        if os.path.exists('.env.docker'):
            with open('.env.docker', 'r') as f:
                content = f.read()
            
            # Create .env with production settings
            with open('.env', 'w') as f:
                f.write(content.replace('your-very-secure-secret-key-change-in-production', 
                                      os.urandom(24).hex()))
            
            print("✅ .env file created!")
            print("⚠️  Please review and update the .env file with your actual settings!")
        else:
            print("❌ .env.docker template not found!")
            return False
    else:
        print("✅ .env file already exists!")
    
    return True

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        'instance',
        'static/uploads',
        'logs'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created {directory}/")
        else:
            print(f"✅ {directory}/ already exists!")

def main():
    """Main setup function"""
    print("=" * 60)
    print("🚀 Umukozi Deployment Setup")
    print("=" * 60)
    
    # Check requirements
    check_requirements()
    
    # Setup environment
    if not setup_environment():
        print("❌ Environment setup failed!")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Review and update .env file with your actual settings")
    print("2. Run 'python init_database.py' to initialize the database")
    print("3. Start the application with 'python app.py' or using Docker")
    print("4. Access the application and login with admin credentials")

if __name__ == '__main__':
    main()

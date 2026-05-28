#!/usr/bin/env python3
"""
Render startup script - initializes database and starts application
"""

import os
import sys
import logging
from datetime import datetime

def main():
    """Main startup function for Render deployment"""
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    logger.info("🚀 Starting Umukozi on Render...")
    
    try:
        # Add current directory to Python path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Test and initialize database
        logger.info("🔧 Initializing database...")
        from init_database import check_database_connection, init_database
        
        if check_database_connection():
            init_database()
            logger.info("✅ Database initialized successfully")
        else:
            logger.error("❌ Database connection failed")
            sys.exit(1)
        
        # Start the application
        logger.info("🌐 Starting Flask application...")
        from app import app
        
        # Use Render's port
        port = int(os.environ.get('PORT', 5000))
        
        logger.info(f"🎉 Application starting on port {port}")
        app.run(host='0.0.0.0', port=port, debug=False)
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == '__main__':
    main()

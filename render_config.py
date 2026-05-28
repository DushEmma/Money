import os
import logging

logger = logging.getLogger(__name__)

def setup_render_environment():
    """
    Setup environment for Render or Heroku deployment.
    Parses connection strings properly for SQLAlchemy.
    """
    database_url = os.environ.get('DATABASE_URL')
    
    # SQLAlchemy 1.4+ requires `postgresql://` but some PaaS (like Heroku/Render) 
    # historically provide `postgres://`
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
        logger.info("Converted postgres:// to postgresql:// in database URL")
        
    return database_url

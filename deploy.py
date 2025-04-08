"""
A simple script to prepare the application for deployment.
This script ensures the database is set up correctly without requiring Flask-Migrate.
"""
import os
import logging
from app import app, db
from models import Application

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_database():
    """Set up the database for deployment"""
    logger.info("Setting up database for deployment...")
    
    with app.app_context():
        # Create all tables
        db.create_all()
        logger.info("Database tables created")
        
        # Check if there are any applications in the database
        app_count = Application.query.count()
        logger.info(f"Found {app_count} existing applications in the database")

if __name__ == "__main__":
    setup_database()
    logger.info("Deployment preparation complete. The application is ready to be deployed.")
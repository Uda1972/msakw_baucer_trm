"""
A simple script to keep the application alive by pinging it regularly.
Run this script separately from your main application.
"""
import time
import urllib.request
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def ping_app():
    """Send a ping to the application to keep it alive"""
    try:
        # Update the URL to match your application's URL
        response = urllib.request.urlopen("http://localhost:5000/")
        status_code = response.getcode()
        logger.info(f"Ping successful, status code: {status_code}")
        return True
    except Exception as e:
        logger.error(f"Ping failed: {str(e)}")
        return False

def main():
    """Main function to keep the application alive"""
    logger.info("Starting keep-alive service...")
    
    # Ping interval in seconds (5 minutes)
    interval = 300
    
    while True:
        success = ping_app()
        if not success:
            logger.warning("Application may be down. Waiting before next attempt...")
        
        # Sleep for the specified interval
        logger.info(f"Sleeping for {interval} seconds...")
        time.sleep(interval)

if __name__ == "__main__":
    main()
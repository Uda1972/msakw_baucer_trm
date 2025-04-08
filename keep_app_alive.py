"""
A simple script to keep your deployed application alive by sending regular pings.
This is useful for free tier services that go to sleep after inactivity.

Usage:
1. Update the APP_URL with your deployed application URL
2. Run this script on a server or computer that's always on
3. It will send a request to your application every 10 minutes to keep it active

You can also use free services like UptimeRobot.com to ping your application regularly.
"""
import time
import logging
import requests
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("keep_alive.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
APP_URL = "https://your-app-url.onrender.com"  # Replace with your actual URL
PING_INTERVAL = 10 * 60  # 10 minutes in seconds

def ping_app():
    """Send a ping to keep the application alive"""
    try:
        start_time = time.time()
        response = requests.get(APP_URL, timeout=30)
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            logger.info(f"Application pinged successfully in {elapsed_time:.2f} seconds")
        else:
            logger.warning(f"Ping received non-200 status code: {response.status_code}")
            
    except Exception as e:
        logger.error(f"Failed to ping application: {e}")

def main():
    """Main function to keep the application alive"""
    logger.info(f"Starting keep-alive service for {APP_URL}")
    logger.info(f"Pinging every {PING_INTERVAL} seconds")
    
    while True:
        ping_app()
        time.sleep(PING_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Keep-alive service stopped by user")
    except Exception as e:
        logger.error(f"Keep-alive service crashed: {e}")
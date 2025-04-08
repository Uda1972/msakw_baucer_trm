"""
A monitoring script that checks if the application is running and restarts it if needed.
Run this script in a separate terminal.
"""
import time
import urllib.request
import logging
import subprocess
import signal
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def check_app_running():
    """Check if the application is running by sending a request to it"""
    try:
        response = urllib.request.urlopen("http://localhost:5000/")
        status_code = response.getcode()
        logger.info(f"Application is running. Status code: {status_code}")
        return True
    except Exception as e:
        logger.error(f"Application check failed: {str(e)}")
        return False

def restart_application():
    """Restart the application by running the gunicorn command"""
    logger.info("Attempting to restart the application...")
    
    try:
        # Kill any existing gunicorn processes
        os.system("pkill -f gunicorn || true")
        time.sleep(2)  # Wait for processes to terminate
        
        # Start gunicorn in a new process
        cmd = "gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app"
        process = subprocess.Popen(cmd, shell=True)
        
        logger.info(f"Started application with PID: {process.pid}")
        
        # Wait for the application to start
        for _ in range(5):  # Try 5 times
            time.sleep(5)  # Wait 5 seconds
            if check_app_running():
                logger.info("Application successfully restarted!")
                return True
        
        logger.error("Failed to restart the application after multiple attempts")
        return False
    except Exception as e:
        logger.error(f"Error restarting application: {str(e)}")
        return False

def main():
    """Main function to monitor and restart the application if needed"""
    logger.info("Starting application monitor...")
    
    # Check interval in seconds (1 minute)
    interval = 60
    
    # Setup signal handlers for graceful shutdown
    def signal_handler(sig, frame):
        logger.info("Monitor shutting down...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    while True:
        if not check_app_running():
            logger.warning("Application is not running. Attempting to restart...")
            restart_application()
        
        logger.info(f"Sleeping for {interval} seconds before next check...")
        time.sleep(interval)

if __name__ == "__main__":
    main()
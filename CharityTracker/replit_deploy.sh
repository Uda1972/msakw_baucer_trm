#!/bin/bash

# This script is used for Replit deployment

# Initialize environment variables if not set
export PORT=${PORT:-5000}

# Make sure the database directory exists
mkdir -p instance

# Run the deployment preparation script
echo "Running deployment preparation..."
python deploy.py

# Initialize the database with sample data (if needed)
echo "Initializing database with sample data..."
python init_db_data.py

# Start the application with gunicorn
echo "Starting application with gunicorn..."
exec gunicorn --bind 0.0.0.0:$PORT --workers=4 main:app
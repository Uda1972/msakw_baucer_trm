#!/bin/bash

# This script is used for deployment on free hosting platforms

# Initialize environment variables if not set
PORT=${PORT:-10000}

# Make sure the database directory exists
mkdir -p instance

# Run the deployment preparation script
echo "Running deployment preparation..."
python deploy.py

# Initialize the database with sample data (if needed)
echo "Initializing database with sample data..."
python init_db_data.py

# Start the application with gunicorn
# Using minimal resources for free tier hosting
echo "Starting application with gunicorn..."
gunicorn --bind 0.0.0.0:$PORT --workers=1 --threads=2 --timeout=120 main:app
#!/bin/bash

# This script is used for deployment on free hosting platforms

# Initialize environment variables if not set
PORT=${PORT:-10000}

# Ensure the database directory exists and is writable
# The DATABASE_PATH is set in render.yaml
mkdir -p $(dirname "$DATABASE_PATH") || true
touch "$DATABASE_PATH" || true
chmod 666 "$DATABASE_PATH" || true
echo "Database will be stored at: $DATABASE_PATH"

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
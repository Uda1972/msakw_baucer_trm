#!/bin/bash

# Start the main application
echo "Starting the main application..."
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app &
APP_PID=$!

# Wait for the application to start
echo "Waiting for the application to start..."
sleep 5

# Start the monitor in the background
echo "Starting the application monitor..."
python monitor_app.py &
MONITOR_PID=$!

# Function to clean up on exit
cleanup() {
    echo "Shutting down..."
    kill $APP_PID $MONITOR_PID 2>/dev/null
    exit
}

# Set up trap to catch signals
trap cleanup SIGINT SIGTERM

# Wait for signals
echo "Application and monitor are running. Press Ctrl+C to stop."
wait

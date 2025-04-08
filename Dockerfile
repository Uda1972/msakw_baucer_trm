FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY pyproject.toml .

# Install dependencies
RUN pip install --no-cache-dir -e .

# Copy the rest of the application code
COPY . .

# Make scripts executable
RUN chmod +x replit_deploy.sh deployment_start.sh

# Make sure the database directory exists
RUN mkdir -p instance

# Expose the port the app runs on
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["./replit_deploy.sh"]
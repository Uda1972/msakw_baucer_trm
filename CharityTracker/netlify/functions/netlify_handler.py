"""
Netlify function handler for the Flask application.
This script acts as a bridge between the Netlify Functions JavaScript handler and the Flask application.
"""
import os
import sys
import io
from contextlib import redirect_stdout, redirect_stderr

# Add the parent directory to the path so we can import the Flask app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    # Set environment variables for SQLite
    os.environ['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.environ.get('SQLITE_DB_PATH', '/tmp/instance/assistance.db')}"
    
    # Import the Flask app
    from main import app
    
    # Create a WSGI environment from the Netlify Function event
    environ = {
        'wsgi.input': io.BytesIO(sys.stdin.buffer.read()),
        'wsgi.errors': sys.stderr,
        'wsgi.version': (1, 0),
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
        'wsgi.url_scheme': 'https',
        'REQUEST_METHOD': os.environ.get('REQUEST_METHOD', 'GET'),
        'PATH_INFO': os.environ.get('REQUEST_PATH', '/'),
        'QUERY_STRING': os.environ.get('QUERY_STRING', ''),
        'CONTENT_TYPE': os.environ.get('CONTENT_TYPE', ''),
        'CONTENT_LENGTH': os.environ.get('CONTENT_LENGTH', ''),
        'SERVER_NAME': 'netlify',
        'SERVER_PORT': '443',
    }
    
    # Add headers
    for key, value in os.environ.items():
        if key.startswith('HTTP_'):
            environ[key] = value
    
    # Capture the response
    response_body = io.BytesIO()
    response_headers = []
    response_status = ['200 OK']  # Default status
    
    def start_response(status, headers):
        response_status[0] = status
        response_headers.extend(headers)
        return response_body.write
    
    # Run the Flask app
    output = app(environ, start_response)
    
    # Write output to buffer
    for data in output:
        if data:
            response_body.write(data)
    
    # Print the response in a format that the JS handler can parse
    print(response_status[0].split(' ')[0])  # Status code
    for key, value in response_headers:
        print(f"{key}: {value}")
    print("")  # Empty line to separate headers from body
    print(response_body.getvalue().decode('utf-8'), end='')
    
except Exception as e:
    # In case of errors, print an error status and log the exception
    print("500")
    print("Content-Type: application/json")
    print("")
    print(f'{{"error": "{str(e)}"}}')
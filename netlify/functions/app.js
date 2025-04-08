// Netlify Function for serving the Flask application
const { spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');

// Prepare SQLite database directory
const dbDir = path.join('/tmp', 'instance');
if (!fs.existsSync(dbDir)) {
  fs.mkdirSync(dbDir, { recursive: true });
}

exports.handler = async (event, context) => {
  try {
    // Prepare environment
    const env = {
      ...process.env,
      SQLITE_DB_PATH: path.join('/tmp', 'instance', 'assistance.db'),
      REQUEST_METHOD: event.httpMethod,
      REQUEST_PATH: event.path,
      QUERY_STRING: new URLSearchParams(event.queryStringParameters || {}).toString(),
      CONTENT_LENGTH: event.body ? Buffer.byteLength(event.body).toString() : '0',
      CONTENT_TYPE: event.headers['content-type'] || '',
    };

    // Add headers
    Object.keys(event.headers).forEach(key => {
      env[`HTTP_${key.toUpperCase().replace(/-/g, '_')}`] = event.headers[key];
    });

    // Run Python script that handles the Flask app
    const result = spawnSync('python', [path.join(__dirname, 'netlify_handler.py')], {
      input: event.body,
      env,
      encoding: 'utf8',
      maxBuffer: 10 * 1024 * 1024, // 10MB buffer
    });

    if (result.error) {
      console.error('Error executing Python script:', result.error);
      return {
        statusCode: 500,
        body: JSON.stringify({ error: 'Internal Server Error' }),
      };
    }

    if (result.status !== 0) {
      console.error('Python script exited with non-zero status:', result.status);
      console.error('STDERR:', result.stderr);
      return {
        statusCode: 500,
        body: JSON.stringify({ error: 'Internal Server Error' }),
      };
    }

    // Parse response from Python script
    const lines = result.stdout.split('\n');
    const statusLine = lines[0];
    const headerLines = [];
    let i = 1;
    while (i < lines.length && lines[i].trim() !== '') {
      headerLines.push(lines[i]);
      i++;
    }
    
    const body = lines.slice(i + 1).join('\n');
    const statusCode = parseInt(statusLine.split(' ')[0], 10);
    
    // Parse headers
    const headers = {};
    headerLines.forEach(line => {
      const [key, ...values] = line.split(':');
      headers[key.trim()] = values.join(':').trim();
    });

    return {
      statusCode,
      headers,
      body,
    };
  } catch (error) {
    console.error('Error in Netlify function:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Internal Server Error' }),
    };
  }
};
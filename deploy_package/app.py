from flask import Flask, jsonify
import os
import sys

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Deployed Python App</title>
        <style>
            body { font-family: Arial; padding: 20px; text-align: center; }
            .success { color: #28a745; font-size: 24px; margin: 20px 0; }
            .btn { background: #0078d4; color: white; padding: 15px; border: none; border-radius: 8px; margin: 10px; }
            .info { background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <h1 class="success">âœ… Successfully Deployed!</h1>
        <p>Python Flask + Azure SQL Application</p>
        
        <div class="info">
            <p><strong>Status:</strong> <span id="status">Loading...</span></p>
            <p><strong>Python Version:</strong> <span id="python">Loading...</span></p>
        </div>
        
        <button class="btn" onclick="testAPI()">Test API</button>
        <div id="result"></div>
        
        <script>
            async function testAPI() {
                const response = await fetch('/api/health');
                const data = await response.json();
                document.getElementById('result').innerHTML = 
                    '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                document.getElementById('status').innerHTML = data.status;
                document.getElementById('python').innerHTML = data.python;
            }
            
            // Test on load
            window.onload = testAPI;
        </script>
    </body>
    </html>
    '''

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'deployed': True,
        'python': sys.version.split()[0],
        'timestamp': os.environ.get('DEPLOY_TIME', 'Not set')
    })

if __name__ == '__main__':
    print(f"Starting app on port 5000...")
    app.run(host='0.0.0.0', port=5000)

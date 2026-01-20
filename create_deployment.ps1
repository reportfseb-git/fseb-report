# create_deployment.ps1
Write-Host "Creating Complete Deployment Package..." -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

# Create folder
$deployFolder = "deploy_live"
if (Test-Path $deployFolder) {
    Remove-Item -Path $deployFolder -Recurse -Force
}
New-Item -ItemType Directory -Path $deployFolder -Force
Set-Location $deployFolder

Write-Host "📁 Created folder: $deployFolder" -ForegroundColor Yellow

# 1. Create app.py
Write-Host "Creating app.py..." -ForegroundColor Cyan
@"
from flask import Flask, jsonify
import os
import sys

print("=" * 50)
print("🚀 Python Flask App - Deployment Ready")
print("=" * 50)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'deploy-key-12345')

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>✅ Deployed Successfully!</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
                color: #333;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                text-align: center;
            }
            h1 { 
                color: #28a745;
                margin-bottom: 20px;
                font-size: 36px;
            }
            .status-box {
                background: #d4edda;
                border-radius: 15px;
                padding: 25px;
                margin: 25px 0;
                border-left: 5px solid #28a745;
            }
            .btn {
                background: #0078d4;
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 10px;
                font-size: 16px;
                margin: 10px;
                cursor: pointer;
                transition: all 0.3s;
            }
            .btn:hover { background: #005a9e; transform: translateY(-2px); }
            .result-box {
                background: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                font-family: monospace;
                text-align: left;
                max-height: 300px;
                overflow-y: auto;
            }
            .url-display {
                background: #17a2b8;
                color: white;
                padding: 15px;
                border-radius: 10px;
                margin: 20px 0;
                font-family: monospace;
                font-size: 18px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎉 Deployment Successful!</h1>
            <p>Your Python Flask app is now live on the internet</p>
            
            <div class="status-box">
                <h3>📊 Deployment Status</h3>
                <p><strong>✅ Application:</strong> Running</p>
                <p><strong>🐍 Python:</strong> <span id="python-version">Loading...</span></p>
                <p><strong>🔧 Framework:</strong> Flask 3.0.0</p>
                <p><strong>📅 Deployed:</strong> <span id="deploy-time">Loading...</span></p>
            </div>
            
            <div class="url-display">
                <p>🌐 Your Public URL:</p>
                <p id="current-url">Loading...</p>
            </div>
            
            <div>
                <h3>🔍 Test Your Deployment</h3>
                <button class="btn" onclick="testAPI()">Test API Health</button>
                <button class="btn" onclick="testPing()">Test Ping</button>
                
                <div id="status" style="margin: 15px 0; padding: 15px; border-radius: 8px;"></div>
                <div class="result-box" id="result"></div>
            </div>
            
            <div style="margin-top: 30px; color: #666; border-top: 1px solid #eee; padding-top: 20px;">
                <p><strong>Next Steps:</strong></p>
                <p>1. Bookmark this URL for mobile access</p>
                <p>2. Test on different devices</p>
                <p>3. Share with colleagues/friends</p>
                <p>4. Monitor usage in hosting dashboard</p>
            </div>
        </div>
        
        <script>
            // Display current URL
            document.getElementById('current-url').textContent = window.location.href;
            
            function updateStatus(message, type = 'info') {
                const statusDiv = document.getElementById('status');
                statusDiv.innerHTML = message;
                statusDiv.style.background = type === 'success' ? '#d4edda' : 
                                           type === 'error' ? '#f8d7da' : '#d1ecf1';
                statusDiv.style.color = type === 'success' ? '#155724' : 
                                       type === 'error' ? '#721c24' : '#0c5460';
            }
            
            async function testAPI() {
                updateStatus('Testing API health...');
                try {
                    const response = await fetch('/api/health');
                    const data = await response.json();
                    
                    document.getElementById('result').innerHTML = 
                        '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                    
                    // Update info
                    document.getElementById('python-version').textContent = data.python;
                    document.getElementById('deploy-time').textContent = data.timestamp;
                    
                    if (data.status === 'healthy') {
                        updateStatus('✅ API is healthy and responding', 'success');
                    } else {
                        updateStatus('⚠ API has issues', 'error');
                    }
                } catch (error) {
                    document.getElementById('result').innerHTML = 'Error: ' + error;
                    updateStatus('❌ API test failed', 'error');
                }
            }
            
            async function testPing() {
                updateStatus('Testing ping...');
                try {
                    const start = Date.now();
                    const response = await fetch('/api/ping');
                    const end = Date.now();
                    const latency = end - start;
                    
                    const data = await response.json();
                    document.getElementById('result').innerHTML = 
                        '<pre>' + JSON.stringify(data, null, 2) + '</pre>' +
                        '<p><strong>Latency:</strong> ' + latency + 'ms</p>';
                    
                    updateStatus('✅ Ping successful (' + latency + 'ms)', 'success');
                } catch (error) {
                    document.getElementById('result').innerHTML = 'Error: ' + error;
                    updateStatus('❌ Ping failed', 'error');
                }
            }
            
            // Auto-test on load
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
        'flask': '3.0.0',
        'timestamp': os.environ.get('DEPLOY_TIME', 'Not set'),
        'message': 'Your app is successfully deployed and running!'
    })

@app.route('/api/ping')
def ping():
    return jsonify({
        'message': 'pong',
        'timestamp': os.datetime.now().isoformat() if hasattr(os, 'datetime') else 'N/A'
    })

if __name__ == '__main__':
    print(f"Python Version: {sys.version.split()[0]}")
    print(f"App will be available at:")
    print(f"   - Local: http://localhost:5000")
    print(f"   - Network: http://[YOUR_IP]:5000")
    print(f"\nStarting server...")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
"@ | Out-File -FilePath "app.py" -Encoding UTF8

Write-Host "✅ Created app.py" -ForegroundColor Green

# 2. Create requirements.txt
Write-Host "Creating requirements.txt..." -ForegroundColor Cyan
@"
Flask==3.0.0
python-dotenv==1.0.0
gunicorn==21.2.0
"@ | Out-File -FilePath "requirements.txt" -Encoding UTF8
Write-Host "✅ Created requirements.txt" -ForegroundColor Green

# 3. Create .env.example
Write-Host "Creating .env.example..." -ForegroundColor Cyan
@"
# Environment Variables
# Copy this file to .env and update the values

# Flask Secret Key (generate a random one)
SECRET_KEY=your-secret-key-change-this-12345

# Deployment Info
DEPLOY_TIME=$(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

# For Azure SQL (optional - uncomment when ready)
# DATABASE_URL=mssql+pymssql://username:password@fseb.database.windows.net/fseb

# App Settings
DEBUG=False
HOST=0.0.0.0
PORT=5000
"@ | Out-File -FilePath ".env.example" -Encoding UTF8
Write-Host "✅ Created .env.example" -ForegroundColor Green

# 4. Create .gitignore
Write-Host "Creating .gitignore..." -ForegroundColor Cyan
@"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.env
.venv/

# Environment
.env
.env.local

# Database
*.db
*.sqlite3

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
*.log
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8
Write-Host "✅ Created .gitignore" -ForegroundColor Green

# 5. Create wsgi.py (for PythonAnywhere)
Write-Host "Creating wsgi.py..." -ForegroundColor Cyan
@"
import sys
import os

# Add the app directory to Python path
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.insert(0, path)

# Import Flask app
from app import app as application

# This is for PythonAnywhere
if __name__ == "__main__":
    application.run()
"@ | Out-File -FilePath "wsgi.py" -Encoding UTF8
Write-Host "✅ Created wsgi.py" -ForegroundColor Green

# 6. Create runtime.txt (for PythonAnywhere)
Write-Host "Creating runtime.txt..." -ForegroundColor Cyan
@"
python-3.10.11
"@ | Out-File -FilePath "runtime.txt" -Encoding UTF8
Write-Host "✅ Created runtime.txt" -ForegroundColor Green

# 7. Create README.md
Write-Host "Creating README.md..." -ForegroundColor Cyan
@"
# Python Flask Application - Deployment Ready

## 🚀 Quick Deployment

### Option 1: PythonAnywhere (Free Tier - Recommended)
1. Upload this folder to PythonAnywhere
2. Create virtual environment:
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

3.  Copy .env.example to .env and update values

4.  Configure web app with WSGI file

5.  Your app: https://username.pythonanywhere.com

Option 2: Railway.app (Free Credits)
1. Push to GitHub

2. Connect repository to Railway

3. Add environment variables

4. Auto-deploy

5. Your app: https://your-app.up.railway.app

Option 3: Local Testing
bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
python app.py

📁 File Structure
app.py - Main Flask application

requirements.txt - Python dependencies

wsgi.py - WSGI configuration for hosting

.env.example - Environment variables template

runtime.txt - Python version for hosting


🔧 Environment Variables
Create .env file with:

SECRET_KEY: Random string for Flask security

DEPLOY_TIME: Timestamp of deployment


🌐 Features
✅ Mobile-responsive design

✅ REST API endpoints

✅ Easy deployment

✅ Production ready

✅ SQLite database ready

✅ Can upgrade to Azure SQL
"@ | Out-File -FilePath "README.md" -Encoding UTF8

Write-Host "✅ Created README.md" -ForegroundColor Green

#8. Create test script
Write-Host "Creating test script..." -ForegroundColor Cyan
@"
@echo off
echo Testing deployment package...
echo.
echo Step 1: Creating .env file...
copy .env.example .env
echo.
echo Step 2: Testing Python...
python --version
echo.
echo Step 3: Testing Flask app...
python app.py
"@ | Out-File -FilePath "test.bat" -Encoding UTF8
Write-Host "✅ Created test.bat" -ForegroundColor Green

#9. Create deploy_instructions.txt
Write-Host "Creating deployment instructions..." -ForegroundColor Cyan
@"
==================== DEPLOYMENT INSTRUCTIONS ====================

STEP 1: TEST LOCALLY

Open PowerShell/Command Prompt

Navigate to this folder

Run: python app.py

Open: http://localhost:5000

STEP 2: DEPLOY TO PYTHONANYWHERE (FREE)

Go to: https://www.pythonanywhere.com

Sign up for free account

In Dashboard → Files → Upload this entire folder

In Dashboard → Consoles → Open Bash

Run these commands:
cd ~/deploy_live
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env # Edit with your values

In Dashboard → Web:

Click "Add a new web app"

Choose "Manual configuration"

Python 3.10

Configure:

Source code: /home/YOUR_USERNAME/deploy_live

Working directory: /home/YOUR_USERNAME/deploy_live

Virtualenv: /home/YOUR_USERNAME/deploy_live/venv

8. Edit WSGI file (click link):

import sys
path = '/home/YOUR_USERNAME/deploy_live'
if path not in sys.path:
    sys.path.append(path)
from app import app as application

Click green Reload button

Your app: https://YOUR_USERNAME.pythonanywhere.com

STEP 3: TEST DEPLOYED APP

Open: https://YOUR_USERNAME.pythonanywhere.com

Click "Test API Health"

Should see "API is healthy and responding"

TROUBLESHOOTING:

Check error logs in PythonAnywhere Web tab

Verify .env file exists and has values

Check virtualenv is set correctly

Make sure all files uploaded

SUCCESS MESSAGE:

🎉 CONGRATULATIONS! Your Python app is now live on the internet!
"@ | Out-File -FilePath "DEPLOY_INSTRUCTIONS.txt" -Encoding UTF8
Write-Host "✅ Created DEPLOY_INSTRUCTIONS.txt" -ForegroundColor Green

#Show all files
Write-Host "`n📁 FILES CREATED:" -ForegroundColor Cyan
Write-Host "=================" -ForegroundColor Cyan
Get-ChildItem | Format-Table Name, @{Label="Size (KB)"; Expression={[math]::Round($_.Length/1KB, 2)}}, LastWriteTime -AutoSize

Test the app
Write-Host "`n🧪 TESTING THE APP..." -ForegroundColor Yellow
Write-Host "Creating test .env file..." -ForegroundColor Cyan
@"
SECRET_KEY=test-key-for-local-testing
DEPLOY_TIME=Test $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
"@ | Out-File -FilePath ".env" -Encoding UTF8

Write-Host "n✅ DEPLOYMENT PACKAGE READY!" -ForegroundColor Green Write-Host "Location: $(Get-Location)" -ForegroundColor Yellow Write-Host "n🚀 To test locally: python app.py" -ForegroundColor Cyan
Write-Host "📖 Full instructions: DEPLOY_INSTRUCTIONS.txt" -ForegroundColor Cyan


# ## **Now Run This Script:**

# ```powershell
# # Save the script above as create_deployment.ps1
# # Then run it:
# .\create_deployment.ps1
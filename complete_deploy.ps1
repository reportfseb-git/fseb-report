# complete_deploy.ps1
Write-Host "🚀 Creating Complete Deployment Package" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

# Create deploy folder
$deployPath = "deploy_package"
if (Test-Path $deployPath) {
    Remove-Item -Path $deployPath -Recurse -Force
}
New-Item -ItemType Directory -Path $deployPath -Force
Set-Location $deployPath

Write-Host "Created folder: $deployPath" -ForegroundColor Yellow

# 1. Create app.py
@"
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
        <h1 class="success">✅ Successfully Deployed!</h1>
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
"@ | Out-File -FilePath "app.py" -Encoding UTF8
Write-Host "1. Created app.py" -ForegroundColor Green

# 2. Create requirements.txt
@"
Flask==3.0.0
python-dotenv==1.0.0
gunicorn==21.2.0
"@ | Out-File -FilePath "requirements.txt" -Encoding UTF8
Write-Host "2. Created requirements.txt" -ForegroundColor Green

# 3. Create wsgi.py
@"
import sys
import os

path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.insert(0, path)

from app import app as application
"@ | Out-File -FilePath "wsgi.py" -Encoding UTF8
Write-Host "3. Created wsgi.py" -ForegroundColor Green

# 4. Create .env.example
@"
# Copy this to .env and fill in your values
DATABASE_URL=mssql+pymssql://username:password@fseb.database.windows.net/fseb
SECRET_KEY=your-secret-key-here-change-in-production
FLASK_APP=app.py
DEPLOY_TIME=$(Get-Date -Format yyyy-MM-dd)
"@ | Out-File -FilePath ".env.example" -Encoding UTF8
Write-Host "4. Created .env.example" -ForegroundColor Green

# 5. Create .gitignore
@"
.env
*.pyc
__pycache__/
*.db
*.log
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8
Write-Host "5. Created .gitignore" -ForegroundColor Green

# 6. Create deploy_instructions.txt
@"
========== DEPLOYMENT INSTRUCTIONS ==========

OPTION 1: PYTHONANYWHERE (Free Tier)
====================================
1. Go to pythonanywhere.com and create free account
2. In Dashboard → Files → Upload files:
   - Upload this entire folder
3. In Dashboard → Consoles → Bash:
   - cd ~/deploy_package
   - python3.10 -m venv venv
   - source venv/bin/activate
   - pip install -r requirements.txt
4. Copy .env.example to .env and edit with your values
5. In Dashboard → Web:
   - Click "Add a new web app"
   - Choose "Manual configuration"
   - Python 3.10
6. Configure Web App:
   - Source code: /home/YOUR_USERNAME/deploy_package
   - Working directory: /home/YOUR_USERNAME/deploy_package
   - Virtualenv: /home/YOUR_USERNAME/deploy_package/venv
7. Edit WSGI file (click the link):
   - DELETE ALL CONTENT
   - Add: 
        import sys
        path = '/home/YOUR_USERNAME/deploy_package'
        if path not in sys.path:
            sys.path.append(path)
        from app import app as application
8. Click Reload (green button)
9. Your app: https://YOUR_USERNAME.pythonanywhere.com

OPTION 2: RAILWAY.APP (Free Credits)
=====================================
1. Push this folder to GitHub
2. Go to railway.app and sign up with GitHub
3. Create New Project → Deploy from GitHub repo
4. Select your repository
5. Add environment variables:
   - DATABASE_URL: your Azure SQL connection string
   - SECRET_KEY: a random secret key
6. Railway will auto-deploy
7. Your app: https://your-project.up.railway.app

OPTION 3: RENDER.COM (Free Tier)
=================================
1. Push to GitHub
2. Go to render.com and sign up
3. New Web Service → Connect GitHub repo
4. Settings:
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn app:app
   - Add environment variables
5. Deploy
6. Your app: https://your-app.onrender.com
"@ | Out-File -FilePath "DEPLOY_INSTRUCTIONS.txt" -Encoding UTF8
Write-Host "6. Created DEPLOY_INSTRUCTIONS.txt" -ForegroundColor Green

# 7. Test locally first
Write-Host "`nTesting locally..." -ForegroundColor Yellow
@"
# Create test .env for local testing
DATABASE_URL=sqlite:///test.db
SECRET_KEY=local-test-key
DEPLOY_TIME=Local Test
"@ | Out-File -FilePath ".env" -Encoding UTF8

Write-Host "Created test .env file" -ForegroundColor Cyan

# Show folder contents
Write-Host "`n📁 Deployment Package Contents:" -ForegroundColor Cyan
Get-ChildItem | Format-Table Name, Length, LastWriteTime -AutoSize

Write-Host "`n✅ DEPLOYMENT PACKAGE READY!" -ForegroundColor Green
Write-Host "Location: $(Get-Location)" -ForegroundColor Yellow
Write-Host "`n📋 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Review DEPLOY_INSTRUCTIONS.txt" -ForegroundColor White
Write-Host "2. Choose a hosting platform (PythonAnywhere recommended)" -ForegroundColor White
Write-Host "3. Follow the step-by-step instructions" -ForegroundColor White
Write-Host "`n🚀 To test locally: python app.py" -ForegroundColor Green
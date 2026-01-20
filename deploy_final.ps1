
# Create a fresh deployment package
$deployFolder = "deploy_final"
if (Test-Path $deployFolder) {
    Remove-Item -Path $deployFolder -Recurse -Force
}
New-Item -ItemType Directory -Path $deployFolder -Force
Set-Location $deployFolder

Write-Host "Creating final deployment package..." -ForegroundColor Green

# 1. Create app.py (the simple version above)
# Copy the Python code above and save as app.py

# 2. Create requirements.txt
@"
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
python-dotenv==1.0.0
gunicorn==21.2.0
"@ | Out-File -FilePath "requirements.txt" -Encoding UTF8

# 3. Create runtime.txt (for PythonAnywhere)
@"
python-3.10.11
"@ | Out-File -FilePath "runtime.txt" -Encoding UTF8

# 4. Create .env.example
@"
# Copy to .env and update values
SECRET_KEY=change-this-to-a-random-secret-key
DEPLOY_TIME=2025-01-19
# For Azure SQL later:
# DATABASE_URL=mssql+pymssql://username:password@server/database
"@ | Out-File -FilePath ".env.example" -Encoding UTF8

# 5. Create .gitignore
@"
.env
*.pyc
__pycache__/
*.db
*.log
instance/
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8

# 6. Create Procfile (for Railway/Render)
@"
web: gunicorn app:app
"@ | Out-File -FilePath "Procfile" -Encoding UTF8

# 7. Create railway.json (for Railway)
@"
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn app:app --bind 0.0.0.0:$PORT",
    "healthcheckPath": "/api/health"
  }
}
"@ | Out-File -FilePath "railway.json" -Encoding UTF8

# 8. Create README.md
@"
# Python Flask Deployment

## Quick Start

1. **Local Development:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   python app.py
Deployment Options:

PythonAnywhere (Free Tier)
Upload this folder

Create virtual environment

Configure WSGI file

Set environment variables

Railway.app (Free Credits)
Push to GitHub

Connect to Railway

Add environment variables

Auto-deploy

Render.com (Free Tier)
Push to GitHub

Create Web Service

Set start command: gunicorn app:app

Environment Variables
Create .env file with:

SECRET_KEY: Random secret for Flask sessions

DEPLOY_TIME: Deployment timestamp

Features
✅ Flask REST API

✅ SQLite database

✅ Mobile responsive

✅ Ready for production

✅ Easy to switch to Azure SQL

"@ | Out-File -FilePath "README.md" -Encoding UTF8

#9. Create test locally script
@"
@echo off
echo Testing deployment package locally...
python -m venv venv_test
call venv_test\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python app.py
"@ | Out-File -FilePath "test_local.bat" -Encoding UTF8

Write-Host "✅ Created deployment package with all files" -ForegroundColor Green
Get-ChildItem | Format-Table Name




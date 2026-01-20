# deploy_pa.ps1 - PythonAnywhere Deployment Helper
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   PYTHONANYWHERE DEPLOYMENT PREP       " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Create deployment package
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$deployFolder = "deploy_pythonanywhere_$timestamp"

New-Item -ItemType Directory -Path $deployFolder -Force | Out-Null

Write-Host "`n📁 Creating deployment package: $deployFolder" -ForegroundColor Yellow

# List files to copy
$filesToCopy = @(
    "app_azure_fixed.py",
    "requirements.txt",
    ".env"
)

# Copy files
foreach ($file in $filesToCopy) {
    if (Test-Path $file) {
        Copy-Item $file -Destination $deployFolder -Force
        Write-Host "  ✅ Copied: $file" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ Missing: $file" -ForegroundColor Yellow
    }
}

# Create PythonAnywhere specific files
Write-Host "`n📝 Creating PythonAnywhere specific files..." -ForegroundColor Yellow

# 1. WSGI configuration file
$wsgiContent = @'
# /var/www/{username}_pythonanywhere_com_wsgi.py
# This file should be placed in your PythonAnywhere WSGI configuration

import sys
import os

# Add your app directory to path
path = '/home/{username}/fseb_report'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
# IMPORTANT: Set these in PythonAnywhere Web app config instead of here for security
# os.environ['AZURE_PASSWORD'] = 'Welcome1'
# os.environ['SECRET_KEY'] = 'your-secret-key'

# Import Flask app
from app_azure_fixed import app as application

print("Azure SQL Flask App loaded successfully!")
'@

$wsgiContent | Out-File -FilePath "$deployFolder/wsgi_configuration.py" -Encoding UTF8
Write-Host "  ✅ Created: wsgi_configuration.py" -ForegroundColor Green

# 2. PythonAnywhere setup instructions
$instructions = @'
# PYTHONANYWHERE DEPLOYMENT INSTRUCTIONS
# ======================================

## 1. UPLOAD FILES
1. Log in to PythonAnywhere
2. Go to Files tab
3. Upload all files from this folder to: /home/{username}/fseb_report/

## 2. SET UP VIRTUAL ENVIRONMENT (Optional)
```bash
cd ~/fseb_report
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. CONFIGURE WEB APP
Go to Web tab

Click "Add a new web app"

Choose "Manual configuration" (Python 3.10 recommended)

Click on the WSGI configuration file link

Replace content with wsgi_configuration.py content

4. SET ENVIRONMENT VARIABLES
In Web app configuration page, add:

AZURE_SERVER = fseb.database.windows.net

AZURE_DATABASE = fseb

AZURE_USERNAME = fseb_admin

AZURE_PASSWORD = Welcome1

SECRET_KEY = pythonanywhere-secret-key-123

5. CONFIGURE AZURE FIREWALL
Go to Azure Portal

Find your SQL Server

Go to Firewall settings

Add PythonAnywhere server IP:

Run on PythonAnywhere bash: curl ifconfig.me

Add that IP to Azure firewall

6. TEST CONNECTION
On PythonAnywhere bash console:

bash
cd ~/fseb_report
python3 -c "
import pymssql
try:
    conn = pymssql.connect(
        server='fseb.database.windows.net',
        database='fseb',
        user='fseb_admin',
        password='Welcome1'
    )
    print('✅ Azure connection successful!')
    conn.close()
except Exception as e:
    print(f'❌ Error: {e}')
"
7. RELOAD WEB APP
Go to Web tab

Click the green Reload button

Visit: https://{username}.pythonanywhere.com

TROUBLESHOOTING
Check error logs: /var/log/{username}.pythonanywhere.com.error.log

Test connection from bash console

Verify Azure firewall rules

Check environment variables are set
'@

$instructions | Out-File -FilePath "$deployFolder/DEPLOYMENT_INSTRUCTIONS.md" -Encoding UTF8
Write-Host " ✅ Created: DEPLOYMENT_INSTRUCTIONS.md" -ForegroundColor Green

#3. Test script for PythonAnywhere
$testScript = @'
#!/usr/bin/env python3

test_pythonanywhere.py - Run this on PythonAnywhere
import os
import sys

print("PythonAnywhere Connection Test")
print("=" * 50)

Check environment variables
required_vars = ['AZURE_PASSWORD']
missing_vars = []

for var in required_vars:
if var not in os.environ:
missing_vars.append(var)

if missing_vars:
print("❌ Missing environment variables:")
for var in missing_vars:
print(f" - {var}")
print("\n💡 Set them with:")
print(" export AZURE_PASSWORD='Welcome1'")
print(" Or set in Web app configuration")
sys.exit(1)

Test pymssql
try:
import pymssql
print("✅ pymssql imported")
except ImportError:
print("❌ pymssql not installed")
print(" Install with: pip install pymssql")
sys.exit(1)

Test connection
try:
conn = pymssql.connect(
server=os.environ.get('AZURE_SERVER', 'fseb.database.windows.net'),
database=os.environ.get('AZURE_DATABASE', 'fseb'),
user=os.environ.get('AZURE_USERNAME', 'fseb_admin'),
password=os.environ.get('AZURE_PASSWORD', '')
)

text
cursor = conn.cursor()
cursor.execute('SELECT @@VERSION')
version = cursor.fetchone()[0]

print("✅ Azure SQL Connection Successful!")
print(f"   Server: fseb.database.windows.net")
print(f"   Version: {version[:60]}...")

# List tables
cursor.execute("""
    SELECT TABLE_NAME 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_TYPE = 'BASE TABLE'
""")
tables = cursor.fetchall()

print(f"   Tables found: {len(tables)}")
for table in tables[:5]:  # Show first 5
    print(f"     - {table[0]}")
if len(tables) > 5:
    print(f"     ... and {len(tables) - 5} more")

conn.close()
except Exception as e:
print(f"❌ Connection failed: {e}")
print("\n💡 Check:")
print("1. Azure firewall allows PythonAnywhere IP")
print("2. Password is correct")
print("3. Server name is correct")

print("\n" + "=" * 50)
print("Test complete!")
'@

$testScript | Out-File -FilePath "$deployFolder/test_pythonanywhere.py" -Encoding UTF8
Write-Host " ✅ Created: test_pythonanywhere.py" -ForegroundColor Green

Write-Host "n📦 Deployment package created in: $deployFolder" -ForegroundColor Cyan Write-Host "n📋 NEXT STEPS:" -ForegroundColor Yellow
Write-Host "1. Zip the folder: Compress-Archive $deployFolder $deployFolder.zip" -ForegroundColor Gray
Write-Host "2. Upload zip to PythonAnywhere" -ForegroundColor Gray
Write-Host "3. Follow instructions in DEPLOYMENT_INSTRUCTIONS.md" -ForegroundColor Gray

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host " READY FOR PYTHONANYWHERE! " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan


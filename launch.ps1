# launch.ps1
function Show-Menu {
    Clear-Host
    Write-Host "==================== AZURE SQL DEPLOYMENT ====================" -ForegroundColor Cyan
    Write-Host "1. Test Azure Connection" -ForegroundColor Yellow
    Write-Host "2. Run Flask App Locally" -ForegroundColor Yellow
    Write-Host "3. Prepare for PythonAnywhere" -ForegroundColor Yellow
    Write-Host "4. Exit" -ForegroundColor Red
    Write-Host "==============================================================" -ForegroundColor Cyan
}

function Test-AzureConnection {
    Write-Host "`n🔌 Testing Azure SQL Connection..." -ForegroundColor Green
    
    # Set environment variables
    $env:AZURE_PASSWORD = "Welcome1"
    $env:AZURE_USERNAME = "fseb_admin"
    $env:AZURE_SERVER = "fseb.database.windows.net"
    $env:AZURE_DATABASE = "fseb"
    
    # Create test script
    $testScript = @'
import pymssql
import os

try:
    conn = pymssql.connect(
        server=os.environ.get("AZURE_SERVER"),
        database=os.environ.get("AZURE_DATABASE"),
        user=os.environ.get("AZURE_USERNAME"),
        password=os.environ.get("AZURE_PASSWORD")
    )
    cursor = conn.cursor()
    cursor.execute('SELECT @@VERSION')
    version = cursor.fetchone()[0]
    print("✅ CONNECTION SUCCESSFUL!")
    print(f"SQL Server: {version[:50]}...")
    conn.close()
except Exception as e:
    print(f"❌ CONNECTION FAILED: {e}")
'@
    
    $testScript | Out-File -FilePath "temp_test.py" -Encoding UTF8
    python temp_test.py
    Remove-Item "temp_test.py" -ErrorAction SilentlyContinue
}

function Run-FlaskApp {
    Write-Host "`n🚀 Starting Flask App..." -ForegroundColor Green
    Write-Host "Local:  http://localhost:5000" -ForegroundColor Yellow
    Write-Host "Mobile: http://192.168.40.7:5000" -ForegroundColor Yellow
    Write-Host "`nPress Ctrl+C to stop" -ForegroundColor Gray
    
    $env:AZURE_PASSWORD = "Welcome1"
    $env:AZURE_USERNAME = "fseb_admin"
    $env:AZURE_SERVER = "fseb.database.windows.net"
    $env:AZURE_DATABASE = "fseb"
    $env:SECRET_KEY = "win-secret-" + (-join ((65..90) + (97..122) | Get-Random -Count 16 | % {[char]$_}))
    
    python app_azure_fixed.py
}

function Prepare-PythonAnywhere {
    Write-Host "`n🌐 Preparing for PythonAnywhere..." -ForegroundColor Green
    
    # Create requirements.txt
    $requirements = @'
Flask==2.3.3
pymssql==2.3.11
Flask-SQLAlchemy==3.0.5
Flask-CORS==4.0.0
python-dotenv==1.0.0
SQLAlchemy==2.0.19
'@
    
    $requirements | Out-File -FilePath "requirements.txt" -Encoding UTF8
    Write-Host "✅ Created requirements.txt"
    
    # Show next steps
    Write-Host "`n📝 NEXT STEPS:" -ForegroundColor Cyan
    Write-Host "1. Upload to PythonAnywhere:" -ForegroundColor Yellow
    Write-Host "   - app_azure_fixed.py" -ForegroundColor Gray
    Write-Host "   - requirements.txt" -ForegroundColor Gray
    Write-Host "   - templates/ and static/ folders" -ForegroundColor Gray
    Write-Host "`n2. On PythonAnywhere bash console:" -ForegroundColor Yellow
    Write-Host "   pip install --user -r requirements.txt" -ForegroundColor Gray
    Write-Host "   export AZURE_PASSWORD='Welcome1'" -ForegroundColor Gray
    Write-Host "`n3. Configure web app with WSGI" -ForegroundColor Yellow
}

do {
    Show-Menu
    $choice = Read-Host "`nSelect option (1-4)"
    
    switch ($choice) {
        '1' { Test-AzureConnection; pause }
        '2' { Run-FlaskApp }
        '3' { Prepare-PythonAnywhere; pause }
        '4' { Write-Host "Goodbye!" -ForegroundColor Green; exit }
    }
} while ($choice -ne '4')

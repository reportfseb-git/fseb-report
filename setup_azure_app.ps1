# fixed_setup.ps1
Write-Host "Fixing Azure SQL Setup..." -ForegroundColor Green
Write-Host "==========================" -ForegroundColor Green

# Stop any running app first (Ctrl+C if needed)

# Create a clean .env with proper format
Write-Host "`nCreating proper .env file..." -ForegroundColor Yellow

# URL encode the password (in case it has special characters)
$password = Read-Host "Enter Azure SQL password again" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password)
$plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

# URL encode special characters
$encodedPassword = [System.Web.HttpUtility]::UrlEncode($plainPassword)

@"
# Flask Application
FLASK_APP=app_azure.py
FLASK_DEBUG=True
SECRET_KEY=azure-app-$(Get-Date -Format yyyyMMddHHmmss)

# Azure SQL - Simple connection string
DATABASE_URL=mssql+pymssql://fseb_admin:$encodedPassword@fseb.database.windows.net/fseb

# Alternative: Use separate variables
AZURE_SQL_SERVER=fseb.database.windows.net
AZURE_SQL_DATABASE=fseb
AZURE_SQL_USERNAME=fseb_admin
AZURE_SQL_PASSWORD=$plainPassword
"@ | Out-File -FilePath ".env" -Encoding UTF8 -Force

Write-Host "✅ Updated .env file" -ForegroundColor Green

# Test connection with a simple script
Write-Host "`nTesting connection..." -ForegroundColor Yellow
@"
import pymssql
import os

print("Testing Azure SQL connection...")

# Try direct connection
try:
    # Connect directly (bypass SQLAlchemy for testing)
    conn = pymssql.connect(
        server='fseb.database.windows.net',
        database='fseb',
        user='fseb_admin',
        password='$plainPassword'
    )
    print("✅ Direct pymssql connection SUCCESSFUL!")
    
    # Test a query
    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION")
    version = cursor.fetchone()
    print(f"SQL Server: {version[0][:50]}...")
    
    # Check existing tables
    cursor.execute("""
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE'
    """)
    tables = cursor.fetchall()
    print(f"Existing tables: {[t[0] for t in tables] if tables else 'None'}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Connection failed: {str(e)[:200]}")
    print("\nCommon solutions:")
    print("1. Check if server exists: fseb.database.windows.net")
    print("2. Check firewall settings in Azure Portal")
    print("3. Enable 'Allow Azure services' in firewall")
    print("4. Verify database name is correct")
"@ | Out-File -FilePath "test_conn.py" -Encoding UTF8

python test_conn.py
Remove-Item -Path "test_conn.py" -ErrorAction SilentlyContinue

# Start the app
Write-Host "`nStarting application..." -ForegroundColor Cyan
python app_azure.py
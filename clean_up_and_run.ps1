# clean_up_and_run.ps1
Write-Host "Cleaning up and starting fresh..." -ForegroundColor Yellow

# Remove problematic files
Remove-Item -Path ".env" -ErrorAction SilentlyContinue
Remove-Item -Path "app.db" -ErrorAction SilentlyContinue
Remove-Item -Path "*.pyc" -ErrorAction SilentlyContinue
Remove-Item -Path "__pycache__" -Recurse -ErrorAction SilentlyContinue

# Create clean .env
@"
FLASK_APP=app.py
FLASK_DEBUG=True
SECRET_KEY=my-secret-key-12345-change-this
DATABASE_URL=mssql+pymssql://fseb_admin:seb202@2@fseb.database.windows.net/fseb
HOST=0.0.0.0
PORT=5000
"@ | Out-File -FilePath ".env" -Encoding UTF8

Write-Host "✅ Created clean .env file" -ForegroundColor Green
Write-Host "Starting app..." -ForegroundColor Cyan
Write-Host ""

# Run the app
python app.py
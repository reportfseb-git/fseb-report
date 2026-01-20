# run_app.ps1 - Windows PowerShell script
$env:AZURE_PASSWORD = "Welcome1"
$env:AZURE_USERNAME = "fseb_admin"
$env:AZURE_SERVER = "fseb.database.windows.net"
$env:AZURE_DATABASE = "fseb"
$env:SECRET_KEY = "azure-app-secret-" + (-join ((65..90) + (97..122) | Get-Random -Count 16 | % {[char]$_}))

Write-Host "🚀 Starting Azure SQL Flask App..." -ForegroundColor Green
Write-Host "Azure Password: *******" -ForegroundColor Yellow
Write-Host "Server: $env:AZURE_SERVER" -ForegroundColor Cyan

python app_azure_fixed.py
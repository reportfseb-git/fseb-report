@echo off
echo ========================================
echo  AZURE SQL FLASK APP - WINDOWS LAUNCHER
echo ========================================
echo.

set AZURE_PASSWORD=Welcome1
set AZURE_USERNAME=fseb_admin
set AZURE_SERVER=fseb.database.windows.net
set AZURE_DATABASE=fseb

echo Starting Flask app with Azure SQL...
echo Server: %AZURE_SERVER%
echo.

python app_azure_fixed.py

pause
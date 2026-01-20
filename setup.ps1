# setup.ps1 - Complete setup script
Write-Host "Setting up Python 3.14 Azure SQL App..." -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green

# Check Python version
Write-Host "`nChecking Python version..." -ForegroundColor Yellow
python --version

# Install required packages
Write-Host "`nInstalling packages..." -ForegroundColor Yellow
pip install Flask==3.0.0 Flask-CORS==4.0.0 Flask-Migrate==4.0.5
pip install Flask-SQLAlchemy==3.1.1 Flask-Login==0.6.3
pip install sqlalchemy==2.0.45 pymssql==2.3.11
pip install python-dotenv==1.0.0 openpyxl==3.1.2
pip install python-dateutil==2.8.2 pytest==7.4.3 gunicorn==21.2.0

# Create .env if it doesn't exist
if (!(Test-Path ".env")) {
    Write-Host "`nCreating .env file..." -ForegroundColor Yellow
    @"
# Flask
FLASK_APP=app.py
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production

# Azure SQL with pymssql (Python 3.14 compatible)
DB_SERVER=your-server.database.windows.net
DB_NAME=your-database-name
DB_USERNAME=your-username
DB_PASSWORD=your-password

# SQLAlchemy connection string for pymssql
DATABASE_URL=mssql+pymssql://`${DB_USERNAME}:`${DB_PASSWORD}@`${DB_SERVER}/`${DB_NAME}

# Application
HOST=0.0.0.0
PORT=5000
"@ | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "Created .env file. Please update with your Azure SQL credentials." -ForegroundColor Cyan
} else {
    Write-Host ".env file already exists." -ForegroundColor Cyan
}

# Create database initialization script
Write-Host "`nCreating database setup script..." -ForegroundColor Yellow
$initScript = @"
from app import app, db

with app.app_context():
    print('Creating database tables...')
    try:
        db.create_all()
        print('✓ Database tables created successfully')
        
        # Test connection
        try:
            db.session.execute('SELECT 1')
            print('✓ Database connection successful')
        except Exception as e:
            print(f'⚠ Database connection issue: {e}')
            print('Make sure to update .env with correct Azure SQL credentials')
            print('Or use SQLite by changing DATABASE_URL to: sqlite:///app.db')
    except Exception as e:
        print(f'✗ Error creating tables: {e}')
"@

$initScript | Out-File -FilePath "init_db.py" -Encoding UTF8

# Initialize database
Write-Host "`nInitializing database..." -ForegroundColor Yellow
python init_db.py

# Clean up
Remove-Item -Path "init_db.py" -ErrorAction SilentlyContinue

Write-Host "`n✅ Setup complete!" -ForegroundColor Green
Write-Host "`n📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Update .env file with your Azure SQL credentials" -ForegroundColor White
Write-Host "2. Or use SQLite by changing DATABASE_URL to: sqlite:///app.db" -ForegroundColor White
Write-Host "3. Run the app: python app.py" -ForegroundColor White
Write-Host "4. Open browser to: http://localhost:5000" -ForegroundColor White
Write-Host "`n📱 Mobile access:" -ForegroundColor Cyan
Write-Host "- On same WiFi: http://[YOUR-COMPUTER-IP]:5000" -ForegroundColor White
Write-Host "- Find your IP: ipconfig | findstr IPv4" -ForegroundColor White
Write-Host "`n🚀 Quick commands:" -ForegroundColor Cyan
Write-Host "  python app.py                    # Run development server" -ForegroundColor White
Write-Host "  pytest                           # Run tests" -ForegroundColor White
Write-Host "  flask db init                   # Initialize migrations (first time)" -ForegroundColor White
Write-Host "  flask db migrate -m 'message'   # Create migration" -ForegroundColor White
Write-Host "  flask db upgrade                # Apply migrations" -ForegroundColor White
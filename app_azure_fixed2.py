# app_azure_fixed.py - WINDOWS COMPATIBLE VERSION
from flask import Flask, jsonify, render_template
import pymssql
import os
import sys
import platform
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import text

print("=" * 70)
print("🚀 AZURE SQL FLASK APP - WINDOWS VERSION")
print("=" * 70)
print(f"Platform: {platform.system()} {platform.release()}")
print(f"Python: {sys.version.split()[0]}")

# Detect if we're on Windows
IS_WINDOWS = platform.system() == 'Windows'

# Load environment
if os.path.exists('.env'):
    load_dotenv()
    print("✅ Loaded .env file")
else:
    print("⚠ No .env file - using environment variables")

app = Flask(__name__)
CORS(app)

# ========== AZURE SQL CONFIGURATION ==========
# On Windows, we need to handle environment variables differently

if IS_WINDOWS:
    # Windows environment variables
    AZURE_PASSWORD = os.environ.get('AZURE_PASSWORD') or 'Welcome1'  # Your password
    print("🌍 Running on WINDOWS - using Windows env vars")
else:
    # Unix/Linux/PythonAnywhere
    AZURE_PASSWORD = os.environ.get('AZURE_PASSWORD', '')
    print("🐧 Running on UNIX/LINUX")

# Set Azure credentials
AZURE_SERVER = 'fseb.database.windows.net'
AZURE_DATABASE = 'fseb'
AZURE_USERNAME = 'fseb_admin'

print(f"\n📊 Azure Configuration:")
print(f"   Server: {AZURE_SERVER}")
print(f"   Database: {AZURE_DATABASE}")
print(f"   Username: {AZURE_USERNAME}")
print(f"   Password: {'*' * 8 if AZURE_PASSWORD else 'NOT SET'}")

# Connection configuration
PYMSSQL_CONFIG = {
    'server': AZURE_SERVER,
    'database': AZURE_DATABASE,
    'user': AZURE_USERNAME,
    'password': AZURE_PASSWORD
}

SQLALCHEMY_URI = f"mssql+pymssql://{AZURE_USERNAME}:{AZURE_PASSWORD}@{AZURE_SERVER}:1433/{AZURE_DATABASE}"

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_URI
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'win-azure-' + os.urandom(8).hex())
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ========== MODELS ==========
class TestUser(db.Model):
    __tablename__ = 'test_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))

# ========== CONNECTION FUNCTIONS ==========
def test_direct_connection():
    """Test direct connection to Azure SQL"""
    try:
        print(f"\n🔌 Testing connection to {AZURE_SERVER}...")
        
        conn = pymssql.connect(**PYMSSQL_CONFIG)
        cursor = conn.cursor()
        
        # Get version
        cursor.execute('SELECT @@VERSION')
        version = cursor.fetchone()[0]
        
        # Get tables
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        return {
            'success': True,
            'version': version[:100] + '...' if len(version) > 100 else version,
            'tables': tables,
            'table_count': len(tables),
            'platform': 'Windows' if IS_WINDOWS else 'Unix',
            'server': AZURE_SERVER
        }
        
    except Exception as e:
        error_msg = str(e)
        return {
            'success': False,
            'error': error_msg,
            'platform': 'Windows' if IS_WINDOWS else 'Unix',
            'server': AZURE_SERVER
        }

# ========== ROUTES (keep your existing routes) ==========
@app.route('/')
def home():
    return render_template('index.html')  # Or your existing HTML

@app.route('/api/test')
def test_api():
    result = test_direct_connection()
    return jsonify(result)

@app.route('/api/info')
def info():
    return jsonify({
        'platform': platform.platform(),
        'python': sys.version,
        'windows': IS_WINDOWS,
        'server': AZURE_SERVER,
        'connected': test_direct_connection()['success']
    })

# ========== MAIN ==========
if __name__ == '__main__':
    # Test connection
    print("\n" + "=" * 70)
    print("🔧 Testing Azure SQL Connection...")
    
    result = test_direct_connection()
    
    if result['success']:
        print(f"✅ CONNECTION SUCCESSFUL!")
        print(f"   Server: {result['server']}")
        print(f"   Tables found: {result['table_count']}")
        if result['tables']:
            print(f"   Table list: {', '.join(result['tables'])}")
    else:
        print(f"❌ CONNECTION FAILED: {result['error']}")
        print("\n💡 Troubleshooting tips:")
        print("   1. Check if password is correct")
        print("   2. Make sure Azure firewall allows your IP")
        print("   3. Verify server name: fseb.database.windows.net")
    
    print("\n" + "=" * 70)
    print("🌐 Starting Flask Server...")
    print("=" * 70)
    
    if IS_WINDOWS:
        print("📱 Local URL: http://localhost:5000")
        print("🌐 Network URL: http://192.168.40.7:5000")
    else:
        print("🌐 Server will be available at configured host")
    
    print("\nPress Ctrl+C to stop the server")
    print("=" * 70)
    
    # Start server
    app.run(
        debug=True,
        host='0.0.0.0' if not IS_WINDOWS else 'localhost',
        port=5000,
        use_reloader=False
    )
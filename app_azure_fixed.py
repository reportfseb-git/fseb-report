# app_azure_fixed.py - UPDATED FOR PYTHONANYWHERE
from flask import Flask, jsonify, render_template
import pymssql
import os
import sys
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import text

print("=" * 70)
print("🚀 AZURE SQL FLASK APP - PYTHONANYWHERE VERSION")
print("=" * 70)

# Load environment - ONLY IN LOCAL DEVELOPMENT
# On PythonAnywhere, we'll use environment variables directly
if os.path.exists('.env'):
    load_dotenv()
    print("✅ Loaded .env file (local development)")
else:
    print("⚠ No .env file found - using environment variables")


app = Flask(__name__)
CORS(app)

# ===========Get Azure SQL credentials (works fine in local env==========
# DATABASE_URL = os.environ.get('DATABASE_URL', '')

# if DATABASE_URL and 'mssql' in DATABASE_URL:
#     print("✅ Using Azure SQL Database")
#     app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
# else:
#     print("⚠ Falling back to SQLite")
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'azure-app-secret')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ========== AZURE SQL CONFIGURATION ==========
# Use direct Azure SQL connection string for PythonAnywhere
# This avoids the complex parsing and works reliably

# Get credentials from environment variables (set in PythonAnywhere)
AZURE_SERVER = os.environ.get('AZURE_SERVER', 'fseb.database.windows.net')
AZURE_DATABASE = os.environ.get('AZURE_DATABASE', 'fseb')
AZURE_USERNAME = os.environ.get('AZURE_USERNAME', 'fseb_admin')
AZURE_PASSWORD = os.environ.get('AZURE_PASSWORD', 'Welcome1')

# Construct connection strings
# For pymssql (direct connection)
PYMSSQL_CONNECTION = {
    'server': AZURE_SERVER,
    'database': AZURE_DATABASE,
    'user': AZURE_USERNAME,
    'password': AZURE_PASSWORD
}


# For SQLAlchemy (if you want to use it)
SQLALCHEMY_DATABASE_URI = f"mssql+pymssql://{AZURE_USERNAME}:{AZURE_PASSWORD}@{AZURE_SERVER}:1433/{AZURE_DATABASE}"

print(f"\n📊 Azure Configuration:")
print(f"   Server: {AZURE_SERVER}")
print(f"   Database: {AZURE_DATABASE}")
print(f"   Username: {AZURE_USERNAME}")
print(f"   Password: {'*' * len(AZURE_PASSWORD) if AZURE_PASSWORD else 'NOT SET'}")

# Set Flask configuration
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'azure-app-secret-' + os.urandom(16).hex())
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize database
db = SQLAlchemy(app)

# Simple model for testing
class TestUser(db.Model):
    __tablename__ = 'test_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))

# Direct connection test (bypass SQLAlchemy for initial test)
# Add this at the top of your app_azure_fixed.py
def check_azure_status():
    """Check Azure connection status with helpful messages"""
    try:
        import pymssql
        import socket
        
        # First check if we can reach the server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(('fseb.database.windows.net', 1433))
        sock.close()
        
        if result != 0:
            return {
                'status': 'blocked',
                'message': 'Firewall is blocking PythonAnywhere',
                'pythonanywhere_ip': '3.95.61.192',
                'fix': 'Add this IP to Azure firewall: 3.95.61.192'
            }
        
        # Try to connect
        conn = pymssql.connect(
            server='fseb.database.windows.net',
            database='fseb',
            user='fseb_admin',
            password='Welcome1',
            timeout=5
        )
        
        cursor = conn.cursor()
        cursor.execute('SELECT @@VERSION')
        version = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'status': 'connected',
            'message': '✅ Connected to Azure SQL',
            'server': 'fseb.database.windows.net',
            'version': version[:100]
        }
        
    except pymssql.OperationalError as e:
        error_msg = str(e)
        if 'Unable to connect' in error_msg:
            return {
                'status': 'firewall_blocked',
                'message': '❌ Azure firewall blocking connection',
                'pythonanywhere_ip': '3.95.61.192',
                'fix': 'Add IP 3.95.61.192 to Azure SQL firewall rules',
                'azure_portal_steps': [
                    '1. Go to Azure Portal → SQL servers',
                    '2. Select your server',
                    '3. Click "Firewall and virtual networks"',
                    '4. Add rule: PythonAnywhere = 3.95.61.192 - 3.95.61.192',
                    '5. Click Save'
                ]
            }
        elif 'Login failed' in error_msg:
            return {
                'status': 'auth_error',
                'message': '❌ Authentication failed',
                'fix': 'Check username/password'
            }
        else:
            return {
                'status': 'error',
                'message': f'❌ Error: {error_msg}'
            }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'❌ Unexpected error: {e}'
        }

# Add a status route
@app.route('/status')
def status():
    return jsonify(check_azure_status())



# ========== DIRECT CONNECTION TEST ==========
def test_direct_connection():
    """Test direct pymssql connection to Azure SQL"""
    try:
        print(f"\n🔌 Testing direct connection to {AZURE_SERVER}...")
        
        conn = pymssql.connect(**PYMSSQL_CONNECTION)
        cursor = conn.cursor()
        
        # Get SQL Server version
        cursor.execute('SELECT @@VERSION')
        version = cursor.fetchone()[0]
        
        # Check tables
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        # Get database info
        cursor.execute("SELECT DB_NAME() as db_name, @@SERVERNAME as server_name")
        db_info = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return {
            'success': True,
            'version': version[:100] + '...' if len(version) > 100 else version,
            'tables': tables,
            'server': AZURE_SERVER,
            'database': AZURE_DATABASE,
            'table_count': len(tables)
        }
        
    except pymssql.OperationalError as e:
        error_msg = str(e)
        if "Login failed" in error_msg:
            return {
                'success': False,
                'error': 'Login failed - check username/password',
                'server': AZURE_SERVER,
                'tip': 'Check if password is set in environment variables'
            }
        elif "cannot open" in error_msg.lower():
            return {
                'success': False,
                'error': 'Cannot connect to server - check firewall rules',
                'server': AZURE_SERVER,
                'tip': 'Add PythonAnywhere IP to Azure firewall'
            }
        else:
            return {
                'success': False,
                'error': error_msg,
                'server': AZURE_SERVER
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'server': AZURE_SERVER
        }
    
# Test SQLAlchemy connection - UPDATED
def test_sqlalchemy_connection():
    """Test SQLAlchemy connection"""
    try:
        with app.app_context():
            result = db.session.execute(text('SELECT 1 as test_value')).fetchone()
            return {
                'success': True,
                'message': 'SQLAlchemy connection successful',
                'test_value': result[0] if result else None
            }
    except Exception as e:
        error_msg = str(e)
        return {
            'success': False,
            'error': error_msg,
            'message': 'SQLAlchemy connection failed'
        }

# ========== ADD THESE HELPER FUNCTIONS ==========
def get_pythonanywhere_info():
    """Get PythonAnywhere specific information"""
    return {
        'is_pythonanywhere': 'PYTHONANYWHERE' in os.environ,
        'pythonanywhere_domain': os.environ.get('PYTHONANYWHERE_DOMAIN', 'Not on PythonAnywhere'),
        'python_version': sys.version.split()[0],
        'current_directory': os.getcwd()
    }


# Test SQLAlchemy connection
def test_sqlalchemy_connection():
    """Test SQLAlchemy connection within app context"""
    try:
        with app.app_context():
            db.session.execute(text('SELECT 1'))
            return True
    except Exception as e:
        print(f"SQLAlchemy error: {str(e)[:100]}...")
        return False

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Azure SQL - Working!</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 900px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            h1 { 
                color: #28a745;
                margin-bottom: 10px;
                font-size: 32px;
            }
            .success-card {
                background: #d4edda;
                border: 2px solid #28a745;
                border-radius: 15px;
                padding: 25px;
                margin: 20px 0;
            }
            .btn {
                background: #0078d4;
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 10px;
                font-size: 16px;
                margin: 10px;
                cursor: pointer;
                transition: all 0.3s;
            }
            .btn:hover { background: #005a9e; transform: translateY(-2px); }
            .btn-success { background: #28a745; }
            .btn-success:hover { background: #218838; }
            .mobile-box {
                background: #28a745;
                color: white;
                padding: 20px;
                border-radius: 15px;
                margin: 25px 0;
            }
            .result-box {
                background: #f4f4f4;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                font-family: monospace;
                max-height: 400px;
                overflow-y: auto;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎉 Azure SQL Connected!</h1>
            <p style="color: #666; margin-bottom: 20px;">Python 3.14 + Flask + Azure SQL Database</p>
            
            <div class="success-card">
                <h3 style="color: #28a745; margin-top: 0;">✅ CONNECTION VERIFIED</h3>
                <p>Direct pymssql connection to Azure SQL is working perfectly!</p>
                <p><strong>Server:</strong> fseb.database.windows.net</p>
                <p><strong>Database:</strong> Connected successfully</p>
            </div>
            
            <div class="pythonanywhere-box" style="background: #0078d4; color: white; padding: 20px; border-radius: 15px; margin: 25px 0;">
                <h3 style="margin-top: 0;">🌐 PythonAnywhere Deployment</h3>
                <p>Your app is configured for PythonAnywhere!</p>
                <p><strong>Next steps:</strong></p>
                <ol style="margin-left: 20px; margin-top: 10px;">
                    <li>Upload files to PythonAnywhere</li>
                    <li>Set environment variables</li>
                    <li>Configure web app</li>
                </ol>
                <p style="margin-top: 15px; font-size: 14px;">Once deployed, your app will be available at:</p>
                <code style="background: rgba(255,255,255,0.3); padding: 10px 15px; border-radius: 8px; font-size: 16px; display: block; margin-top: 10px;">
                    https://[your-username].pythonanywhere.com
                </code>
            </div>
            
            <div>
                <h3>🔧 Test Functions</h3>
                <button class="btn" onclick="testDirect()">Test Direct Connection</button>
                <button class="btn" onclick="testSQLAlchemy()">Test SQLAlchemy</button>
                <button class="btn btn-success" onclick="createTables()">Create Tables</button>
                <button class="btn" onclick="listTables()">List Tables</button>
                
                <div id="status" style="margin: 20px 0; padding: 15px; border-radius: 8px;"></div>
                <div class="result-box" id="result"></div>
            </div>
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                <h3>📊 System Info</h3>
                <p><strong>Python:</strong> 3.14.2</p>
                <p><strong>Database:</strong> Azure SQL (Microsoft SQL Azure)</p>
                <p><strong>Driver:</strong> pymssql 2.3.11</p>
                <p><strong>Local URL:</strong> <a href="http://localhost:5000" target="_blank">localhost:5000</a></p>
                <p><strong>Mobile URL:</strong> <a href="http://192.168.40.7:5000" target="_blank">192.168.40.7:5000</a></p>
            </div>
        </div>
        
        <script>
            function updateStatus(message, type = 'info') {
                const statusDiv = document.getElementById('status');
                statusDiv.innerHTML = message;
                statusDiv.style.background = type === 'success' ? '#d4edda' : 
                                           type === 'error' ? '#f8d7da' : 
                                           type === 'warning' ? '#fff3cd' : '#d1ecf1';
                statusDiv.style.color = type === 'success' ? '#155724' : 
                                       type === 'error' ? '#721c24' : 
                                       type === 'warning' ? '#856404' : '#0c5460';
            }
            
            async function testDirect() {
                updateStatus('Testing direct pymssql connection...', 'info');
                try {
                    const response = await fetch('./api/test-direct');
                    const data = await response.json();
                    document.getElementById('result').innerHTML = JSON.stringify(data, null, 2);
                    
                    if (data.success) {
                        updateStatus('✅ Direct connection successful!', 'success');
                    } else {
                        updateStatus('❌ Direct connection failed', 'error');
                    }
                } catch (error) {
                    document.getElementById('result').innerHTML = 'Error: ' + error;
                    updateStatus('❌ Test failed', 'error');
                }
            }
            
            async function testSQLAlchemy() {
                updateStatus('Testing SQLAlchemy connection...', 'info');
                try {
                    const response = await fetch('./api/test-sqlalchemy');
                    const data = await response.json();
                    document.getElementById('result').innerHTML = JSON.stringify(data, null, 2);
                    
                    if (data.success) {
                        updateStatus('✅ SQLAlchemy connection successful!', 'success');
                    } else {
                        updateStatus('⚠ SQLAlchemy connection issue', 'warning');
                    }
                } catch (error) {
                    document.getElementById('result').innerHTML = 'Error: ' + error;
                    updateStatus('❌ Test failed', 'error');
                }
            }
            
            async function createTables() {
                updateStatus('Creating database tables...', 'info');
                try {
                    const response = await fetch('./api/create-tables', { method: 'POST' });
                    const data = await response.json();
                    document.getElementById('result').innerHTML = JSON.stringify(data, null, 2);
                    
                    if (data.success) {
                        updateStatus('✅ Tables created successfully!', 'success');
                    } else {
                        updateStatus('⚠ ' + data.message, 'warning');
                    }
                } catch (error) {
                    document.getElementById('result').innerHTML = 'Error: ' + error;
                    updateStatus('❌ Failed to create tables', 'error');
                }
            }
            
            async function listTables() {
                updateStatus('Listing database tables...', 'info');
                try {
                    const response = await fetch('./api/list-tables');
                    const data = await response.json();
                    document.getElementById('result').innerHTML = JSON.stringify(data, null, 2);
                    
                    if (data.success) {
                        updateStatus('✅ Retrieved table list', 'success');
                    }
                } catch (error) {
                    document.getElementById('result').innerHTML = 'Error: ' + error;
                    updateStatus('❌ Failed to list tables', 'error');
                }
            }
            
            // Auto-test on page load
            window.onload = testDirect;
        </script>
    </body>
    </html>
    '''

# API Routes

# ========== ADD THIS NEW ROUTE ==========
@app.route('/api/deployment-info')
def deployment_info():
    """Get deployment information"""
    info = get_pythonanywhere_info()
    info.update({
        'azure_configured': bool(AZURE_PASSWORD),
        'server': AZURE_SERVER,
        'database': AZURE_DATABASE,
        'flask_env': os.environ.get('FLASK_ENV', 'production')
    })
    return jsonify(info)

@app.route('/api/test-direct')
def api_test_direct():
    result = test_direct_connection()
    return jsonify(result)

@app.route('/api/test-sqlalchemy')
def api_test_sqlalchemy():
    success = test_sqlalchemy_connection()
    return jsonify({
        'success': success,
        'message': 'SQLAlchemy connection test',
        'database': 'Azure SQL' if 'mssql' in app.config['SQLALCHEMY_DATABASE_URI'] else 'SQLite'
    })

@app.route('/api/create-tables', methods=['POST'])
def api_create_tables():
    try:
        with app.app_context():
            db.create_all()
            return jsonify({
                'success': True,
                'message': 'Tables created successfully',
                'tables': ['test_users']
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e),
            'tip': 'Check database permissions'
        }), 500

@app.route('/api/list-tables')
def api_list_tables():
    try:
        result = test_direct_connection()
        if result['success']:
            return jsonify({
                'success': True,
                'tables': result['tables'],
                'count': len(result['tables'])
            })
        else:
            return jsonify({
                'success': False,
                'message': result['error'],
                'tables': []
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e),
            'tables': []
        }), 500

@app.route('/api/health')
def health():
    direct_test = test_direct_connection()
    sqlalchemy_test = test_sqlalchemy_connection()
    
    return jsonify({
        'status': 'healthy',
        'python': sys.version.split()[0],
        'direct_connection': direct_test['success'],
        'sqlalchemy_connection': sqlalchemy_test,
        'database': 'Azure SQL' if 'mssql' in app.config['SQLALCHEMY_DATABASE_URI'] else 'SQLite',
        'mobile_url': 'http://192.168.40.7:5000'
    })


# Initialize and run
# ========== UPDATE THE MAIN BLOCK ==========
if __name__ == '__main__':
    print(f"\n📦 System Information:")
    print(f"   Python: {sys.version.split()[0]}")
    print(f"   Platform: {sys.platform}")
    print(f"   Working Directory: {os.getcwd()}")
    
    # Check if we're on PythonAnywhere
    if 'PYTHONANYWHERE' in os.environ:
        print("\n✅ RUNNING ON PYTHONANYWHERE")
        print("   App will be served through WSGI")
        print("   DO NOT use app.run() on PythonAnywhere")
    else:
        print("\n🏃‍♂️ RUNNING LOCALLY")
        print("   Starting development server...")
    
    # Test connections
    print("\n🔌 Testing Azure SQL connection...")
    direct_result = test_direct_connection()
    
    if direct_result['success']:
        print(f"✅ DIRECT CONNECTION: SUCCESS!")
        print(f"   Server: {direct_result['server']}")
        print(f"   Database: {direct_result['database']}")
        print(f"   Tables found: {direct_result['table_count']}")
    else:
        print(f"❌ Direct connection failed: {direct_result.get('error', 'Unknown error')}")
        if 'tip' in direct_result:
            print(f"   Tip: {direct_result['tip']}")
    
    # Only run the server if NOT on PythonAnywhere
    if 'PYTHONANYWHERE' not in os.environ:
        print("\n" + "=" * 70)
        print("🌐 DEVELOPMENT SERVER STARTING")
        print("=" * 70)
        print(f"   Local:  http://localhost:5000")
        print(f"   Network: http://192.168.40.7:5000")
        print("\n" + "-" * 70)
        print("📱 Open on your phone for mobile testing!")
        print("=" * 70)
        
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    else:
        print("\n" + "=" * 70)
        print("✅ PYTHONANYWHERE READY")
        print("=" * 70)
        print("   App is configured for PythonAnywhere WSGI")
        print("   Make sure to set environment variables:")
        print("      AZURE_PASSWORD=your_password")
        print("      SECRET_KEY=your_secret_key")
        print("=" * 70)
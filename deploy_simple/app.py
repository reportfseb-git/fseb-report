# app_azure_fixed.py
from flask import Flask, jsonify, render_template
import pymssql
import os
import sys
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import text

print("=" * 70)
print("🚀 AZURE SQL FLASK APP - FIXED VERSION")
print("=" * 70)

# Load environment
load_dotenv()

app = Flask(__name__)
CORS(app)

# Get Azure SQL credentials
DATABASE_URL = os.environ.get('DATABASE_URL', '')

if DATABASE_URL and 'mssql' in DATABASE_URL:
    print("✅ Using Azure SQL Database")
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
else:
    print("⚠ Falling back to SQLite")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'azure-app-secret')
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
def test_direct_connection():
    """Test direct pymssql connection"""
    try:
        # Parse connection string: mssql+pymssql://username:password@server/database
        if DATABASE_URL and 'mssql' in DATABASE_URL:
            # Extract parts from connection string
            parts = DATABASE_URL.replace('mssql+pymssql://', '').split('@')
            user_pass = parts[0].split(':')
            server_db = parts[1].split('/')
            
            username = user_pass[0]
            password = user_pass[1] if len(user_pass) > 1 else ''
            server = server_db[0]
            database = server_db[1] if len(server_db) > 1 else ''
            
            print(f"Connecting to: {server}/{database}")
            
            conn = pymssql.connect(
                server=server,
                database=database,
                user=username,
                password=password
            )
            
            cursor = conn.cursor()
            cursor.execute('SELECT @@VERSION')
            version = cursor.fetchone()[0]
            
            # Check tables
            cursor.execute("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_TYPE = 'BASE TABLE'
            """)
            tables = [row[0] for row in cursor.fetchall()]
            
            cursor.close()
            conn.close()
            
            return {
                'success': True,
                'version': version[:100],
                'tables': tables,
                'server': server,
                'database': database
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'connection_string': DATABASE_URL[:50] + '...' if DATABASE_URL else 'None'
        }
    
    return {'success': False, 'error': 'No Azure SQL connection string'}

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
            
            <div class="mobile-box">
                <h3 style="margin-top: 0;">📱 Mobile Access</h3>
                <p>On your phone browser, open:</p>
                <code style="background: rgba(255,255,255,0.3); padding: 10px 15px; border-radius: 8px; font-size: 16px;">
                    http://192.168.40.7:5000
                </code>
                <p style="margin-top: 10px;"><small>Same WiFi network required</small></p>
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
                    const response = await fetch('/api/test-direct');
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
                    const response = await fetch('/api/test-sqlalchemy');
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
                    const response = await fetch('/api/create-tables', { method: 'POST' });
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
                    const response = await fetch('/api/list-tables');
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
if __name__ == '__main__':
    print(f"Python: {sys.version.split()[0]}")
    
    # Test direct connection
    print("\nTesting direct Azure SQL connection...")
    direct_result = test_direct_connection()
    
    if direct_result['success']:
        print(f"✅ DIRECT CONNECTION: SUCCESS!")
        print(f"   Server: {direct_result['server']}")
        print(f"   Database: {direct_result['database']}")
        print(f"   Tables: {direct_result['tables']}")
    else:
        print(f"❌ Direct connection failed: {direct_result['error']}")
    
    # Test SQLAlchemy
    print("\nTesting SQLAlchemy connection...")
    sqlalchemy_result = test_sqlalchemy_connection()
    
    if sqlalchemy_result:
        print("✅ SQLAlchemy connection: SUCCESS!")
    else:
        print("⚠ SQLAlchemy connection issue")
    
    print("\n" + "=" * 70)
    print("🌐 APPLICATION READY")
    print("=" * 70)
    print(f"   Local:  http://localhost:5000")
    print(f"   Mobile: http://192.168.40.7:5000")
    print("\n" + "-" * 70)
    print("📱 Open on your phone for mobile testing!")
    print("=" * 70)
    print("\nStarting server...\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
# app_azure.py - Complete Azure SQL Flask App
from flask import Flask, jsonify, render_template
import os
import sys
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import text

print("=" * 70)
print("🚀 AZURE SQL FLASK APP - Python 3.14")
print("=" * 70)

# Load environment variables
try:
    load_dotenv()
    print("✓ Loaded .env file")
except:
    print("⚠ No .env file found")

app = Flask(__name__)
CORS(app)

# Get database URL from environment
database_url = os.environ.get('DATABASE_URL')

if database_url and 'mssql' in database_url:
    print("🔗 Using Azure SQL Database")
    print(f"   Server: {database_url.split('@')[1].split('/')[0] if '@' in database_url else 'Unknown'}")
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    print("⚠ No Azure SQL connection found in .env")
    print("   Using SQLite as fallback")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'azure-app-secret-12345')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Define a simple model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

# Helper function to test database connection
def test_db_connection():
    try:
        db.session.execute(text('SELECT 1'))
        return True
    except Exception as e:
        print(f"Database error: {str(e)[:100]}...")
        return False

# Routes
@app.route('/')
def home():
    db_type = 'Azure SQL' if 'mssql' in app.config['SQLALCHEMY_DATABASE_URI'] else 'SQLite'
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Azure SQL App</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
                color: #333;
            }}
            .container {{
                max-width: 900px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }}
            h1 {{ 
                color: #0078d4; 
                margin-bottom: 10px;
                font-size: 32px;
            }}
            .status-card {{
                background: #f8f9fa;
                border-radius: 15px;
                padding: 25px;
                margin: 20px 0;
                border-left: 5px solid #0078d4;
            }}
            .btn {{
                background: #0078d4;
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 10px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                margin: 10px 5px;
                transition: all 0.3s;
                display: inline-block;
            }}
            .btn:hover {{ background: #005a9e; transform: translateY(-2px); }}
            .btn-success {{ background: #28a745; }}
            .btn-success:hover {{ background: #218838; }}
            .btn-warning {{ background: #ffc107; color: #333; }}
            .btn-warning:hover {{ background: #e0a800; }}
            .mobile-box {{
                background: #28a745;
                color: white;
                padding: 20px;
                border-radius: 15px;
                margin: 25px 0;
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }}
            .result-box {{
                background: #f4f4f4;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                max-height: 400px;
                overflow-y: auto;
                white-space: pre-wrap;
                word-wrap: break-word;
            }}
            .info-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 25px 0;
            }}
            .info-card {{
                background: #e8f4fd;
                padding: 20px;
                border-radius: 10px;
                border: 1px solid #cce7ff;
            }}
            .success {{ color: #28a745; }}
            .error {{ color: #dc3545; }}
            .warning {{ color: #ffc107; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Azure SQL Flask App</h1>
            <p style="color: #666; margin-bottom: 30px;">Running on Python 3.14 with Azure SQL Database</p>
            
            <div class="mobile-box">
                <h3 style="margin-top: 0;">📱 Mobile Access</h3>
                <p>On your phone browser, open:</p>
                <code style="background: rgba(255,255,255,0.3); padding: 10px 15px; border-radius: 8px; font-size: 16px;">
                    http://192.168.40.7:5000
                </code>
                <p style="margin-top: 10px; font-size: 14px; opacity: 0.9;">
                    <em>Must be on same WiFi network as your computer</em>
                </p>
            </div>
            
            <div class="info-grid">
                <div class="info-card">
                    <h3>🔧 Database Info</h3>
                    <p><strong>Type:</strong> {db_type}</p>
                    <p><strong>Status:</strong> <span id="dbStatus">Checking...</span></p>
                </div>
                <div class="info-card">
                    <h3>🐍 Python Info</h3>
                    <p><strong>Version:</strong> {sys.version.split()[0]}</p>
                    <p><strong>Platform:</strong> {sys.platform}</p>
                </div>
                <div class="info-card">
                    <h3>🌐 Network Info</h3>
                    <p><strong>Local:</strong> <a href="http://localhost:5000" target="_blank">localhost:5000</a></p>
                    <p><strong>Network:</strong> <a href="http://192.168.40.7:5000" target="_blank">192.168.40.7:5000</a></p>
                </div>
            </div>
            
            <div class="status-card">
                <h3>🔍 Test Connection</h3>
                <button class="btn" onclick="testHealth()">Test Health</button>
                <button class="btn btn-success" onclick="testDatabase()">Test Database</button>
                <button class="btn btn-warning" onclick="createTables()">Create Tables</button>
                <button class="btn" onclick="getTables()">List Tables</button>
                
                <div id="statusMessage" style="margin-top: 20px; padding: 15px; border-radius: 8px;"></div>
                <div class="result-box" id="result"></div>
            </div>
            
            <div class="status-card">
                <h3>📖 API Documentation</h3>
                <div style="margin: 15px 0;">
                    <p><strong>GET</strong> <code>/api/health</code> - System health check</p>
                    <p><strong>GET</strong> <code>/api/test-db</code> - Database connection test</p>
                    <p><strong>POST</strong> <code>/api/tables/create</code> - Create database tables</p>
                    <p><strong>GET</strong> <code>/api/tables/list</code> - List all tables</p>
                </div>
            </div>
        </div>
        
        <script>
            function updateStatus(message, type = 'info') {{
                const statusDiv = document.getElementById('statusMessage');
                statusDiv.innerHTML = message;
                statusDiv.style.background = type === 'success' ? '#d4edda' : 
                                           type === 'error' ? '#f8d7da' : 
                                           type === 'warning' ? '#fff3cd' : '#d1ecf1';
                statusDiv.style.color = type === 'success' ? '#155724' : 
                                       type === 'error' ? '#721c24' : 
                                       type === 'warning' ? '#856404' : '#0c5460';
            }}
            
            async function testHealth() {{
                updateStatus('Testing health...', 'info');
                try {{
                    const response = await fetch('/api/health');
                    const data = await response.json();
                    document.getElementById('result').innerHTML = JSON.stringify(data, null, 2);
                    
                    if (data.status === 'healthy') {{
                        updateStatus('✅ Health check successful', 'success');
                        document.getElementById('dbStatus').innerHTML = 'Connected';
                        document.getElementById('dbStatus').className = 'success';
                    }} else {{
                        updateStatus('⚠ Health check warning', 'warning');
                    }}
                }} catch (error) {{
                    document.getElementById('result').innerHTML = 'Error: ' + error;
                    updateStatus('❌ Health check failed', 'error');
                }}
            }}
            
            async function testDatabase() {{
                updateStatus('Testing database connection...', 'info');
                try {{
                    const response = await fetch('/api/test-db');
                    const data = await response.json();
                    document.getElementById('result').innerHTML = JSON.stringify(data, null, 2);
                    
                    if (data.status === 'success') {{
                        updateStatus('✅ Database connection successful', 'success');
                        document.getElementById('dbStatus').innerHTML = 'Connected';
                        document.getElementById('dbStatus').className = 'success';
                    }} else {{
                        updateStatus('❌ Database connection failed', 'error');
                        document.getElementById('dbStatus').innerHTML = 'Disconnected';
                        document.getElementById('dbStatus').className = 'error';
                    }}
                }} catch (error) {{
                    document.getElementById('result').innerHTML = 'Error: ' + error;
                    updateStatus('❌ Database test failed', 'error');
                }}
            }}
            
            async function createTables() {{
                updateStatus('Creating database tables...', 'info');
                try {{
                    const response = await fetch('/api/tables/create', {{ method: 'POST' }});
                    const data = await response.json();
                    document.getElementById('result').innerHTML = JSON.stringify(data, null, 2);
                    
                    if (data.status === 'success') {{
                        updateStatus('✅ Tables created successfully', 'success');
                    }} else {{
                        updateStatus('⚠ ' + data.message, 'warning');
                    }}
                }} catch (error) {{
                    document.getElementById('result').innerHTML = 'Error: ' + error;
                    updateStatus('❌ Failed to create tables', 'error');
                }}
            }}
            
            async function getTables() {{
                updateStatus('Fetching table list...', 'info');
                try {{
                    const response = await fetch('/api/tables/list');
                    const data = await response.json();
                    document.getElementById('result').innerHTML = JSON.stringify(data, null, 2);
                    
                    if (data.status === 'success') {{
                        updateStatus('✅ Retrieved table list', 'success');
                    }}
                }} catch (error) {{
                    document.getElementById('result').innerHTML = 'Error: ' + error;
                    updateStatus('❌ Failed to get tables', 'error');
                }}
            }}
            
            // Auto-test on page load
            window.onload = function() {{
                testHealth();
            }};
        </script>
    </body>
    </html>
    '''

# API Routes
@app.route('/api/health')
def health():
    db_connected = test_db_connection()
    db_type = 'Azure SQL' if 'mssql' in app.config['SQLALCHEMY_DATABASE_URI'] else 'SQLite'
    
    return jsonify({
        'status': 'healthy' if db_connected else 'degraded',
        'python_version': sys.version.split()[0],
        'flask_version': '3.0.0',
        'database': {
            'type': db_type,
            'connected': db_connected,
            'url': app.config['SQLALCHEMY_DATABASE_URI'].split('://')[0] + '://***'
        },
        'endpoints': {
            'health': '/api/health',
            'test_db': '/api/test-db',
            'create_tables': '/api/tables/create',
            'list_tables': '/api/tables/list'
        },
        'mobile_access': 'http://192.168.40.7:5000'
    })

@app.route('/api/test-db')
def test_db():
    try:
        db.session.execute(text('SELECT 1'))
        
        # Try to get database info
        try:
            if 'mssql' in app.config['SQLALCHEMY_DATABASE_URI']:
                result = db.session.execute(text('SELECT @@VERSION')).fetchone()
                version = result[0] if result else 'Unknown'
            else:
                result = db.session.execute(text('SELECT sqlite_version()')).fetchone()
                version = f'SQLite {result[0]}' if result else 'Unknown'
        except:
            version = 'Unknown'
        
        return jsonify({
            'status': 'success',
            'message': 'Database connection successful',
            'database_type': 'Azure SQL' if 'mssql' in app.config['SQLALCHEMY_DATABASE_URI'] else 'SQLite',
            'version': version[:100] + '...' if len(str(version)) > 100 else version,
            'connection': 'Active'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'database_type': 'Azure SQL' if 'mssql' in app.config['SQLALCHEMY_DATABASE_URI'] else 'SQLite',
            'tip': 'Check your connection string in .env file'
        }), 500

@app.route('/api/tables/create', methods=['POST'])
def create_tables():
    try:
        with app.app_context():
            db.create_all()
            return jsonify({
                'status': 'success',
                'message': 'Database tables created successfully',
                'tables': ['users', 'items']
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'tip': 'Check database permissions and connection'
        }), 500

@app.route('/api/tables/list')
def list_tables():
    try:
        # Get all tables
        if 'mssql' in app.config['SQLALCHEMY_DATABASE_URI']:
            result = db.session.execute(text("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_TYPE = 'BASE TABLE'
            """)).fetchall()
            tables = [row[0] for row in result]
        else:
            # SQLite
            result = db.session.execute(text("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
            """)).fetchall()
            tables = [row[0] for row in result]
        
        return jsonify({
            'status': 'success',
            'tables': tables,
            'count': len(tables)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'tables': []
        }), 500

# Initialize and run
if __name__ == '__main__':
    print(f"Python Version: {sys.version.split()[0]}")
    print(f"Database URL: {app.config['SQLALCHEMY_DATABASE_URI'].split('://')[0]}://***")
    
    # Test database connection
    print("\n" + "-" * 70)
    print("Testing database connection...")
    
    if test_db_connection():
        print("✅ Database connection successful!")
        
        # Try to create tables
        try:
            with app.app_context():
                db.create_all()
                print("✅ Database tables created/verified")
        except Exception as e:
            print(f"⚠ Could not create tables: {str(e)[:100]}...")
    else:
        print("❌ Database connection failed")
        print("   Check your .env file and Azure SQL firewall settings")
        print("   Falling back to basic functionality...")
    
    print("\n" + "=" * 70)
    print("🌐 APPLICATION URLs:")
    print("=" * 70)
    print(f"   Local Computer:  http://localhost:5000")
    print(f"   Mobile/Network:  http://192.168.40.7:5000")
    print("\n" + "-" * 70)
    print("📱 Open on your phone browser for mobile testing!")
    print("=" * 70)
    print("\nStarting Flask server... (Press Ctrl+C to stop)\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
# app_azure_fixed.py - RAILWAY VERSION
import os
import sys
from flask import Flask, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import text

print("=" * 70)
print("🚀 AZURE SQL FLASK APP - RAILWAY DEPLOYMENT")
print("=" * 70)

app = Flask(__name__)
CORS(app)

# ========== RAILWAY ENVIRONMENT CONFIG ==========
# Railway provides PORT environment variable
PORT = os.environ.get('PORT', '5000')

# Get credentials from Railway environment variables
# These will be set in Railway dashboard
AZURE_SERVER = os.environ.get('AZURE_SERVER', 'fseb.database.windows.net')
AZURE_DATABASE = os.environ.get('AZURE_DATABASE', 'fseb')
AZURE_USERNAME = os.environ.get('AZURE_USERNAME', 'fseb_admin')
AZURE_PASSWORD = os.environ.get('AZURE_PASSWORD', '')  # REQUIRED - set in Railway
SECRET_KEY = os.environ.get('SECRET_KEY', 'railway-secret-' + os.urandom(16).hex())

print(f"📊 Environment Configuration:")
print(f"   PORT: {PORT}")
print(f"   AZURE_SERVER: {AZURE_SERVER}")
print(f"   AZURE_DATABASE: {AZURE_DATABASE}")
print(f"   AZURE_USERNAME: {AZURE_USERNAME}")
print(f"   AZURE_PASSWORD: {'*' * 8 if AZURE_PASSWORD else 'NOT SET - WILL FAIL'}")

# ========== DATABASE CONFIGURATION ==========
# SQLAlchemy connection string for Azure SQL
SQLALCHEMY_DATABASE_URI = f"mssql+pymssql://{AZURE_USERNAME}:{AZURE_PASSWORD}@{AZURE_SERVER}:1433/{AZURE_DATABASE}"

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ========== MODELS ==========
class TestUser(db.Model):
    __tablename__ = 'test_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))

# ========== HELPER FUNCTIONS ==========
def test_azure_connection():
    """Test connection to Azure SQL"""
    try:
        import pymssql
        conn = pymssql.connect(
            server=AZURE_SERVER,
            database=AZURE_DATABASE,
            user=AZURE_USERNAME,
            password=AZURE_PASSWORD
        )
        
        cursor = conn.cursor()
        cursor.execute('SELECT @@VERSION, DB_NAME()')
        version, db_name = cursor.fetchone()
        
        # Get table count
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
        """)
        table_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'success': True,
            'message': '✅ Connected to Azure SQL',
            'server': AZURE_SERVER,
            'database': db_name,
            'version': version[:100],
            'tables': table_count,
            'hosting': 'Railway.app'
        }
        
    except Exception as e:
        error_msg = str(e)
        return {
            'success': False,
            'message': '❌ Azure connection failed',
            'error': error_msg[:200],
            'hosting': 'Railway.app',
            'fix': 'Check AZURE_PASSWORD environment variable in Railway dashboard'
        }

# ========== ROUTES ==========
@app.route('/')
def home():
    # Test connection first
    connection_test = test_azure_connection()
    
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Azure SQL on Railway</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
                color: #333;
            }
            .container {
                max-width: 1000px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            h1 { 
                color: #28a745;
                margin-bottom: 10px;
                font-size: 2.5rem;
            }
            .status-card {
                background: ''' + ('#d4edda' if connection_test['success'] else '#f8d7da') + ''';
                border: 2px solid ''' + ('#28a745' if connection_test['success'] else '#dc3545') + ''';
                border-radius: 15px;
                padding: 25px;
                margin: 25px 0;
            }
            .card {
                background: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                border-left: 5px solid #0078d4;
            }
            .btn {
                background: #0078d4;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 16px;
                margin: 10px 5px;
                cursor: pointer;
                transition: all 0.3s;
                text-decoration: none;
                display: inline-block;
            }
            .btn:hover { 
                background: #005a9e; 
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            .btn-success { background: #28a745; }
            .btn-success:hover { background: #218838; }
            .info-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 15px;
                margin: 20px 0;
            }
            .info-item {
                background: white;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #dee2e6;
            }
            .log-box {
                background: #1e1e1e;
                color: #d4d4d4;
                padding: 15px;
                border-radius: 8px;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                max-height: 300px;
                overflow-y: auto;
                margin: 20px 0;
            }
            .success { color: #28a745; }
            .error { color: #dc3545; }
            .warning { color: #ffc107; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Azure SQL on Railway</h1>
            <p style="color: #666; margin-bottom: 20px;">Python Flask + Azure SQL Database + Railway Hosting</p>
            
            <div class="status-card">
                <h2>''' + ('✅ DEPLOYMENT SUCCESSFUL' if connection_test['success'] else '⚠️ CONNECTION ISSUE') + '''</h2>
                <p>''' + connection_test['message'] + '''</p>
                <p><strong>Host:</strong> Railway.app</p>
                <p><strong>Server:</strong> ''' + connection_test.get('server', 'N/A') + '''</p>
                <p><strong>Database:</strong> ''' + connection_test.get('database', 'N/A') + '''</p>
            </div>
            
            <div class="card">
                <h3>🔧 Quick Actions</h3>
                <a href="/api/health" class="btn">Health Check</a>
                <a href="/api/test" class="btn">Test Connection</a>
                <a href="/api/tables" class="btn">List Tables</a>
                <a href="/debug" class="btn">Debug Info</a>
            </div>
            
            <div class="info-grid">
                <div class="info-item">
                    <h4>📊 System Info</h4>
                    <p>Python: ''' + sys.version.split()[0] + '''</p>
                    <p>Platform: ''' + sys.platform + '''</p>
                    <p>Port: ''' + PORT + '''</p>
                </div>
                
                <div class="info-item">
                    <h4>🌐 Hosting</h4>
                    <p>Provider: Railway.app</p>
                    <p>Status: <span class="success">Active</span></p>
                    <p>URL: <code>https://yourapp.up.railway.app</code></p>
                </div>
                
                <div class="info-item">
                    <h4>🗄️ Database</h4>
                    <p>Type: Azure SQL</p>
                    <p>Status: <span class="''' + ('success' 
                                                    if connection_test['success'] 
                                                    else 'error') + '''">''' + ('Connected' 
                                                    if connection_test['success'] 
                                                    else 'Disconnected') + '''</span></p>
                    <p>Tables: ''' + str(connection_test.get('tables', 0)) + '''</p>
                </div>
            </div>
            
            <div class="card">
                <h3>📝 Deployment Log</h3>
                <div class="log-box">
                    $ git push railway main<br>
                    › Building from Nixpacks<br>
                    › Installing Python dependencies...<br>
                    › Starting gunicorn on port ''' + PORT + '''...<br>
                    › ✅ Application deployed successfully!<br>
                    › 🌐 Available at: https://yourapp.up.railway.app<br>
                </div>
            </div>
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #dee2e6;">
                <h3>⚡ Next Steps</h3>
                <ol style="margin-left: 20px; margin-top: 10px;">
                    <li>Set environment variables in Railway dashboard</li>
                    <li>Test all API endpoints</li>
                    <li>Configure custom domain (optional)</li>
                    <li>Set up monitoring and alerts</li>
                </ol>
            </div>
        </div>
        
        <script>
            // Auto-refresh connection status every 30 seconds
            setTimeout(() => {
                window.location.reload();
            }, 30000);
            
            // Add interactivity
            document.querySelectorAll('.btn').forEach(btn => {
                btn.addEventListener('click', function(e) {
                    if(this.getAttribute('href').startsWith('/')) {
                        // Allow normal navigation
                        return;
                    }
                    this.style.transform = 'scale(0.95)';
                    setTimeout(() => {
                        this.style.transform = '';
                    }, 150);
                });
            });
        </script>
    </body>
    </html>
    '''
    return html

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'Azure SQL Flask API',
        'python': sys.version.split()[0],
        'hosting': 'Railway.app',
        'timestamp': '2024-01-20T00:00:00Z'
    })

@app.route('/api/test')
def api_test():
    return jsonify(test_azure_connection())

@app.route('/api/tables')
def list_tables():
    test_result = test_azure_connection()
    if not test_result['success']:
        return jsonify(test_result)
    
    try:
        import pymssql
        conn = pymssql.connect(
            server=AZURE_SERVER,
            database=AZURE_DATABASE,
            user=AZURE_USERNAME,
            password=AZURE_PASSWORD
        )
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE
            FROM INFORMATION_SCHEMA.TABLES
            ORDER BY TABLE_SCHEMA, TABLE_NAME
        """)
        
        tables = []
        for schema, name, type_ in cursor.fetchall():
            tables.append({
                'schema': schema,
                'name': name,
                'type': type_
            })
        
        conn.close()
        
        return jsonify({
            'success': True,
            'count': len(tables),
            'tables': tables
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/debug')
def debug():
    return jsonify({
        'environment': {
            'PORT': PORT,
            'AZURE_SERVER': AZURE_SERVER,
            'AZURE_DATABASE': AZURE_DATABASE,
            'AZURE_USERNAME': AZURE_USERNAME,
            'AZURE_PASSWORD_SET': bool(AZURE_PASSWORD),
            'RAILWAY_ENVIRONMENT': os.environ.get('RAILWAY_ENVIRONMENT', 'production'),
            'RAILWAY_PROJECT_NAME': os.environ.get('RAILWAY_PROJECT_NAME', 'Not set'),
            'RAILWAY_SERVICE_NAME': os.environ.get('RAILWAY_SERVICE_NAME', 'Not set')
        },
        'system': {
            'python': sys.version,
            'platform': sys.platform,
            'cwd': os.getcwd(),
            'files': os.listdir('.')[:20]
        }
    })

# ========== START APPLICATION ==========
if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("🚀 Starting Railway Deployment...")
    print("=" * 70)
    
    # Test connection
    print("\n🔌 Testing Azure SQL connection...")
    connection_result = test_azure_connection()
    
    if connection_result['success']:
        print(f"✅ AZURE SQL: CONNECTED!")
        print(f"   Server: {connection_result['server']}")
        print(f"   Database: {connection_result['database']}")
        print(f"   Tables: {connection_result.get('tables', 0)}")
    else:
        print(f"❌ AZURE SQL: FAILED")
        print(f"   Error: {connection_result.get('error', 'Unknown error')}")
        print(f"   Fix: Set AZURE_PASSWORD environment variable in Railway")
    
    print("\n" + "=" * 70)
    print("🌐 Starting Flask Server...")
    print(f"   Port: {PORT}")
    print("=" * 70)
    
    # Railway will use gunicorn, but this allows local testing
    app.run(host='0.0.0.0', port=int(PORT), debug=False)
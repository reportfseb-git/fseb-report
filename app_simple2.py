# app_simple.py - Minimal working Flask app with Azure SQL
from flask import Flask, jsonify, render_template_string
import pymssql
import os

app = Flask(__name__)

# Azure SQL configuration
AZURE_CONFIG = {
    'server': 'fseb.database.windows.net',
    'database': 'fseb',
    'user': 'fseb_admin',
    'password': 'Welcome1'  # Your password
}

def test_connection():
    """Test connection to Azure SQL"""
    try:
        conn = pymssql.connect(**AZURE_CONFIG)
        cursor = conn.cursor()
        cursor.execute('SELECT @@VERSION')
        version = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return {
            'success': True,
            'version': version[:100],
            'tables': tables,
            'table_count': len(tables)
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Azure SQL - Simple Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .success { color: green; }
            .error { color: red; }
            .card { 
                background: #f5f5f5; 
                padding: 20px; 
                border-radius: 10px;
                margin: 20px 0;
            }
            button { 
                background: #0078d4; 
                color: white; 
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                margin: 5px;
            }
            button:hover { background: #005a9e; }
        </style>
    </head>
    <body>
        <h1>Azure SQL Flask App</h1>
        <div class="card">
            <h3>Connection Status: <span id="status">Testing...</span></h3>
            <div id="result"></div>
        </div>
        
        <div>
            <button onclick="testConnection()">Test Connection</button>
            <button onclick="listTables()">List Tables</button>
        </div>
        
        <script>
            async function testConnection() {
                const response = await fetch('/api/test');
                const data = await response.json();
                document.getElementById('result').innerHTML = 
                    `<pre>${JSON.stringify(data, null, 2)}</pre>`;
                
                if(data.success) {
                    document.getElementById('status').innerHTML = '✅ Connected';
                    document.getElementById('status').className = 'success';
                } else {
                    document.getElementById('status').innerHTML = '❌ Failed';
                    document.getElementById('status').className = 'error';
                }
            }
            
            async function listTables() {
                const response = await fetch('/api/tables');
                const data = await response.json();
                document.getElementById('result').innerHTML = 
                    `<pre>${JSON.stringify(data, null, 2)}</pre>`;
            }
            
            // Auto-test on page load
            window.onload = testConnection;
        </script>
    </body>
    </html>
    '''

@app.route('/api/test')
def api_test():
    return jsonify(test_connection())

@app.route('/api/tables')
def api_tables():
    result = test_connection()
    if result['success']:
        return jsonify({
            'success': True,
            'tables': result['tables'],
            'count': result['table_count']
        })
    return jsonify(result)

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Starting Simple Azure SQL Flask App")
    print("=" * 60)
    
    # Test connection first
    print("Testing Azure SQL connection...")
    test_result = test_connection()
    
    if test_result['success']:
        print(f"✅ Connection successful!")
        print(f"   Server: fseb.database.windows.net")
        print(f"   Database: fseb")
        print(f"   Tables found: {test_result['table_count']}")
    else:
        print(f"❌ Connection failed: {test_result['error']}")
    
    print("\n🌐 Starting Flask server...")
    print("   Local:  http://localhost:5000")
    print("   Mobile: http://192.168.40.7:5000")
    print("\nPress Ctrl+C to stop")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
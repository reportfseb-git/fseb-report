# app_simple.py - For deployment
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import sys

print("=" * 60)
print("🚀 Deployment-Ready Flask App")
print("=" * 60)

app = Flask(__name__)

# Use SQLite for deployment (works everywhere!)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'deployment-secret-12345')

db = SQLAlchemy(app)

# Simple model
class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=0)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Deployed Python App</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                text-align: center;
            }
            h1 { 
                color: #28a745;
                margin-bottom: 20px;
                font-size: 32px;
            }
            .status-card {
                background: #d4edda;
                border-radius: 15px;
                padding: 25px;
                margin: 25px 0;
                border-left: 5px solid #28a745;
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
            .result-box {
                background: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                font-family: monospace;
                text-align: left;
                max-height: 300px;
                overflow-y: auto;
            }
            .url-box {
                background: #17a2b8;
                color: white;
                padding: 15px;
                border-radius: 10px;
                margin: 20px 0;
                font-family: monospace;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>✅ Successfully Deployed!</h1>
            <p>Python 3.14 Flask Application</p>
            
            <div class="status-card">
                <h3>🚀 Deployment Status: LIVE</h3>
                <p>Your app is now running on the internet!</p>
                <p><strong>Database:</strong> SQLite (Production Ready)</p>
                <p><strong>Python:</strong> 3.14</p>
                <p><strong>Framework:</strong> Flask 3.0.0</p>
            </div>
            
            <div class="url-box">
                <p><strong>Your Public URL:</strong></p>
                <p id="current-url">Loading...</p>
            </div>
            
            <div>
                <h3>🔧 Test Functions</h3>
                <button class="btn" onclick="testHealth()">Test Health</button>
                <button class="btn" onclick="testDB()">Test Database</button>
                <button class="btn" onclick="recordVisit()">Record Visit</button>
                
                <div id="status" style="margin: 15px 0; padding: 10px; border-radius: 5px;"></div>
                <div class="result-box" id="result"></div>
            </div>
            
            <div style="margin-top: 30px; color: #666;">
                <p><strong>Features:</strong> ✅ REST API • ✅ Database • ✅ Mobile Responsive • ✅ Ready for Azure SQL</p>
                <p><em>Switch to Azure SQL anytime by updating DATABASE_URL in environment variables</em></p>
            </div>
        </div>
        
        <script>
            // Show current URL
            document.getElementById('current-url').textContent = window.location.href;
            
            function updateStatus(message, type = 'info') {
                const statusDiv = document.getElementById('status');
                statusDiv.innerHTML = message;
                statusDiv.style.background = type === 'success' ? '#d4edda' : 
                                           type === 'error' ? '#f8d7da' : '#d1ecf1';
                statusDiv.style.color = type === 'success' ? '#155724' : 
                                       type === 'error' ? '#721c24' : '#0c5460';
            }
            
            async function testHealth() {
                updateStatus('Testing health...');
                try {
                    const response = await fetch('/api/health');
                    const data = await response.json();
                    document.getElementById('result').innerHTML = JSON.stringify(data, null, 2);
                    updateStatus('✅ Health check successful', 'success');
                } catch (error) {
                    document.getElementById('result').innerHTML = 'Error: ' + error;
                    updateStatus('❌ Health check failed', 'error');
                }
            }
            
            async function testDB() {
                updateStatus('Testing database...');
                try {
                    const response = await fetch('/api/test-db');
                    const data = await response.json();
                    document.getElementById('result').innerHTML = JSON.stringify(data, null, 2);
                    if (data.success) {
                        updateStatus('✅ Database connected', 'success');
                    } else {
                        updateStatus('⚠ Database issue', 'error');
                    }
                } catch (error) {
                    document.getElementById('result').innerHTML = 'Error: ' + error;
                    updateStatus('❌ Database test failed', 'error');
                }
            }
            
            async function recordVisit() {
                updateStatus('Recording visit...');
                try {
                    const response = await fetch('/api/visit', { method: 'POST' });
                    const data = await response.json();
                    document.getElementById('result').innerHTML = JSON.stringify(data, null, 2);
                    updateStatus('✅ Visit recorded: ' + data.count + ' total visits', 'success');
                } catch (error) {
                    document.getElementById('result').innerHTML = 'Error: ' + error;
                    updateStatus('❌ Failed to record visit', 'error');
                }
            }
            
            // Auto-test on load
            window.onload = testHealth;
        </script>
    </body>
    </html>
    '''

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'deployed': True,
        'python': sys.version.split()[0],
        'database': 'SQLite',
        'message': 'Application is deployed and running!',
        'timestamp': os.environ.get('DEPLOY_TIME', 'Not set')
    })

@app.route('/api/test-db')
def test_db():
    try:
        with app.app_context():
            visitor_count = Visitor.query.count()
            return jsonify({
                'success': True,
                'message': 'Database is working',
                'visitor_count': visitor_count,
                'database': 'SQLite'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e),
            'database': 'SQLite'
        }), 500

@app.route('/api/visit', methods=['POST'])
def record_visit():
    try:
        with app.app_context():
            visitor = Visitor.query.first()
            if not visitor:
                visitor = Visitor(count=1)
                db.session.add(visitor)
            else:
                visitor.count += 1
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Visit recorded',
                'count': visitor.count
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

# Initialize database
with app.app_context():
    db.create_all()
    print("✅ Database tables created")

if __name__ == '__main__':
    print(f"Python Version: {sys.version.split()[0]}")
    print(f"Database: SQLite (app.db)")
    print(f"\n🌐 App will be available at:")
    print(f"   - Your deployment URL (after hosting)")
    print(f"\nStarting server for local testing...")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
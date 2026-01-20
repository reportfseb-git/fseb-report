# app.py - Clean working version
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
import os
import sys
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text

print("=" * 60)
print("🚀 Starting Python 3.14 Flask App")
print("=" * 60)
print(f"Python: {sys.version.split()[0]}")
print(f"Working directory: {os.getcwd()}")

# Try to load .env
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✓ Loaded .env file")
except:
    print("⚠ No .env file found, using defaults")

# App configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-12345-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

print(f"Database: {app.config['SQLALCHEMY_DATABASE_URI'].split('://')[0]}")

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)

# Models
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('Item', backref='owner', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Helper functions
def test_db_connection():
    try:
        db.session.execute(text('SELECT 1'))
        return True
    except:
        return False

def create_sample_data():
    if User.query.count() == 0:
        print("Creating sample data...")
        
        # Create admin user
        admin = User(username='admin', email='admin@example.com')
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create test user
        test_user = User(username='test', email='test@example.com')
        test_user.set_password('test123')
        db.session.add(test_user)
        
        db.session.commit()
        
        # Create sample items
        items = [
            Item(title='Welcome to the app', description='Explore the features', user_id=admin.id),
            Item(title='Test mobile access', description='Open on your phone', user_id=test_user.id),
            Item(title='Learn Flask', description='Study Flask documentation', user_id=admin.id),
        ]
        
        for item in items:
            db.session.add(item)
        
        db.session.commit()
        print(f"✓ Created {User.query.count()} users and {Item.query.count()} items")

# Routes
@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Python 3.14 Mobile App</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container { 
            max-width: 800px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 15px; 
            padding: 30px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        h1 { 
            color: #333; 
            margin-bottom: 20px; 
            text-align: center;
        }
        .card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
        }
        .btn {
            background: #0078d4;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            margin: 5px;
            transition: background 0.3s;
        }
        .btn:hover { background: #005a9e; }
        .status { 
            padding: 15px; 
            background: #e8f4fd; 
            border-radius: 8px;
            margin: 15px 0;
            border-left: 4px solid #0078d4;
        }
        .mobile-box {
            background: #28a745;
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
        }
        pre {
            background: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-family: monospace;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📱 Python 3.14 Mobile App</h1>
        <p style="text-align: center; color: #666;">Fully functional web app accessible from your phone!</p>
        
        <div class="mobile-box">
            <h3 style="margin-top: 0;">📲 Mobile Access:</h3>
            <p>On your phone browser, open:</p>
            <code style="background: rgba(255,255,255,0.2); padding: 5px 10px; border-radius: 5px;">http://192.168.40.7:5000</code>
            <p><small>(Must be on same WiFi network)</small></p>
        </div>
        
        <div class="card">
            <h3>Test API Endpoints</h3>
            <button class="btn" onclick="testHealth()">Test Health</button>
            <button class="btn" onclick="testDB()">Test Database</button>
            <div class="status" id="status">Ready to test...</div>
            <pre id="result"></pre>
        </div>
        
        <div class="card">
            <h3>Quick Links</h3>
            <p><a href="/api/health" target="_blank">/api/health - Health Check</a></p>
            <p><a href="/api/test-db" target="_blank">/api/test-db - Database Test</a></p>
            <p><a href="/api/auth/me" target="_blank">/api/auth/me - Current User</a></p>
        </div>
        
        <div class="card">
            <h3>Test Users</h3>
            <p><strong>Username:</strong> admin | <strong>Password:</strong> admin123</p>
            <p><strong>Username:</strong> test | <strong>Password:</strong> test123</p>
            <p><em>Use these to test login functionality</em></p>
        </div>
        
        <div class="card">
            <h3>API Documentation</h3>
            <p><strong>GET /api/health</strong> - Check system health</p>
            <p><strong>GET /api/test-db</strong> - Test database connection</p>
            <p><strong>POST /api/auth/login</strong> - User login</p>
            <p><strong>POST /api/auth/register</strong> - User registration</p>
            <p><strong>GET /api/items</strong> - Get user items</p>
        </div>
    </div>
    
    <script>
        async function testHealth() {
            document.getElementById('status').innerHTML = 'Testing health...';
            try {
                const response = await fetch('/api/health');
                const data = await response.json();
                document.getElementById('result').innerHTML = JSON.stringify(data, null, 2);
                document.getElementById('status').innerHTML = '✓ Health check successful';
            } catch (error) {
                document.getElementById('result').innerHTML = 'Error: ' + error;
                document.getElementById('status').innerHTML = '✗ Health check failed';
            }
        }
        
        async function testDB() {
            document.getElementById('status').innerHTML = 'Testing database...';
            try {
                const response = await fetch('/api/test-db');
                const data = await response.json();
                document.getElementById('result').innerHTML = JSON.stringify(data, null, 2);
                if (data.status === 'success') {
                    document.getElementById('status').innerHTML = '✓ Database connected';
                } else {
                    document.getElementById('status').innerHTML = '✗ Database error';
                }
            } catch (error) {
                document.getElementById('result').innerHTML = 'Error: ' + error;
                document.getElementById('status').innerHTML = '✗ Database test failed';
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
        'python': sys.version.split()[0],
        'database': 'connected' if test_db_connection() else 'disconnected',
        'app': 'Flask Mobile App',
        'mobile_url': 'http://192.168.40.7:5000',
        'message': 'App is running successfully!'
    })

@app.route('/api/test-db')
def test_db():
    try:
        db.session.execute(text('SELECT 1'))
        tables = [table.name for table in db.metadata.tables.values()]
        return jsonify({
            'status': 'success',
            'message': 'Database connection successful',
            'database': app.config['SQLALCHEMY_DATABASE_URI'].split('://')[0],
            'tables': tables,
            'record_counts': {
                'users': User.query.count(),
                'items': Item.query.count()
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'tip': 'Check your .env file or use DATABASE_URL=sqlite:///app.db'
        }), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(username=data.get('username')).first()
        
        if user and user.check_password(data.get('password', '')):
            login_user(user)
            return jsonify({
                'message': 'Login successful',
                'user': user.to_dict()
            })
        return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if User.query.filter_by(username=data.get('username')).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        user = User(username=data.get('username'), email=data.get('email', ''))
        user.set_password(data.get('password', ''))
        
        db.session.add(user)
        db.session.commit()
        login_user(user)
        
        return jsonify({
            'message': 'Registration successful',
            'user': user.to_dict()
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out'})

@app.route('/api/auth/me')
@login_required
def get_current_user():
    return jsonify(current_user.to_dict())

@app.route('/api/items')
@login_required
def get_items():
    items = Item.query.filter_by(user_id=current_user.id).all()
    return jsonify([item.to_dict() for item in items])

@app.route('/api/items', methods=['POST'])
@login_required
def create_item():
    data = request.get_json()
    item = Item(
        title=data.get('title', ''),
        description=data.get('description', ''),
        user_id=current_user.id
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

# Initialize app
if __name__ == '__main__':
    with app.app_context():
        print("\n" + "="*60)
        print("Initializing database...")
        
        try:
            db.create_all()
            print("✓ Database tables created")
            
            create_sample_data()
            
            if test_db_connection():
                print("✓ Database connection successful")
            else:
                print("⚠ Database connection failed")
                
        except Exception as e:
            print(f"✗ Error: {e}")
            print("Trying with SQLite...")
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
            db.init_app(app)
            with app.app_context():
                db.create_all()
                print("✓ Created SQLite database")
    
    print("\n" + "="*60)
    print("🚀 APPLICATION READY")
    print("="*60)
    print("Local Access:  http://localhost:5000")
    print("Mobile Access: http://192.168.40.7:5000")
    print("\nTest Users:")
    print("  • admin / admin123")
    print("  • test  / test123")
    print("\nAPI Endpoints:")
    print("  • /api/health    - System health")
    print("  • /api/test-db   - Database test")
    print("  • /api/auth/login - User login")
    print("="*60)
    print("\nStarting server... (Press Ctrl+C to stop)\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
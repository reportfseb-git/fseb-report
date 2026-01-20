#!/usr/bin/env python3
"""
PythonAnywhere Setup Helper
Run this on PythonAnywhere bash console
"""
import os
import subprocess
import sys

def check_pythonanywhere():
    """Check if we're on PythonAnywhere"""
    return 'PYTHONANYWHERE' in os.environ

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False
    return True

def test_azure_connection():
    """Test Azure SQL connection"""
    print("\n🔌 Testing Azure SQL connection...")
    try:
        # Create a simple test script
        test_script = """
import pymssql
import os

server = os.environ.get('AZURE_SERVER', 'fseb.database.windows.net')
database = os.environ.get('AZURE_DATABASE', 'fseb')
username = os.environ.get('AZURE_USERNAME', 'fseb_admin')
password = os.environ.get('AZURE_PASSWORD', '')

print(f"Testing connection to: {server}")
print(f"Database: {database}")
print(f"Username: {username}")

if not password:
    print("❌ ERROR: AZURE_PASSWORD environment variable not set!")
    print("   Set it with: export AZURE_PASSWORD='your_password'")
    exit(1)

try:
    conn = pymssql.connect(server=server, database=database, user=username, password=password)
    cursor = conn.cursor()
    cursor.execute('SELECT @@VERSION')
    version = cursor.fetchone()[0]
    print(f"✅ Connection successful!")
    print(f"   SQL Server: {version[:50]}...")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("   Check:")
    print("   1. Is AZURE_PASSWORD set correctly?")
    print("   2. Is PythonAnywhere IP allowed in Azure firewall?")
    print("   3. Is the server name correct?")
"""
        
        with open('test_pa_connection.py', 'w') as f:
            f.write(test_script)
        
        subprocess.check_call([sys.executable, "test_pa_connection.py"])
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def create_wsgi_file(username):
    """Create WSGI configuration file content"""
    wsgi_content = f'''import sys
import os

# Add your app's directory to path
path = '/home/{username}/fseb_report'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables for Azure SQL
os.environ['AZURE_SERVER'] = 'fseb.database.windows.net'
os.environ['AZURE_DATABASE'] = 'fseb'
os.environ['AZURE_USERNAME'] = 'fseb_admin'
# IMPORTANT: Set your actual password here or in Web app config
os.environ['AZURE_PASSWORD'] = 'YOUR_ACTUAL_PASSWORD_HERE'
os.environ['SECRET_KEY'] = 'your-secret-key-here'

# Import Flask app
from app_azure_fixed import app as application
'''
    
    print("\n📝 WSGI file content (copy this to your WSGI file on PythonAnywhere):")
    print("=" * 60)
    print(wsgi_content)
    print("=" * 60)
    
    # Save to file
    with open('wsgi_config.py', 'w') as f:
        f.write(wsgi_content)
    
    print("\n✅ WSGI config saved to 'wsgi_config.py'")
    print("   Copy this content to your PythonAnywhere WSGI file")

def main():
    print("=" * 60)
    print("🐍 PythonAnywhere Deployment Setup")
    print("=" * 60)
    
    if not check_pythonanywhere():
        print("⚠ This script is designed for PythonAnywhere")
        print("   Running in simulation mode...")
    
    # Get PythonAnywhere username
    pa_username = os.environ.get('USER', 'your_username')
    print(f"\n👤 Detected username: {pa_username}")
    
    # Step 1: Install requirements
    print("\n1️⃣ Installing requirements...")
    if install_requirements():
        print("   ✅ Done")
    else:
        print("   ❌ Failed - check above errors")
    
    # Step 2: Test connection
    print("\n2️⃣ Testing Azure SQL connection...")
    print("   Make sure to set AZURE_PASSWORD first:")
    print("   export AZURE_PASSWORD='your_actual_password'")
    input("\n   Press Enter to test connection...")
    
    test_azure_connection()
    
    # Step 3: Show WSGI config
    print("\n3️⃣ WSGI Configuration")
    create_wsgi_file(pa_username)
    
    print("\n" + "=" * 60)
    print("🎉 Setup Complete!")
    print("=" * 60)
    print("\nNext steps on PythonAnywhere:")
    print("1. Go to Web tab → Add a new web app")
    print("2. Choose 'Manual configuration' → Python 3.10")
    print("3. Go to 'WSGI configuration file'")
    print("4. Replace content with the WSGI config above")
    print("5. Set environment variables in Web app config:")
    print("   - AZURE_PASSWORD=your_actual_password")
    print("   - SECRET_KEY=your_secret_key")
    print("6. Reload the web app")
    print("\nYour app will be at: https://{pa_username}.pythonanywhere.com")

if __name__ == '__main__':
    main()
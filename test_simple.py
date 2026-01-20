# test_simple.py
import sys
import pymssql
from flask import Flask

print("✅ All imports successful!")
print(f"Python: {sys.version.split()[0]}")
print(f"Flask imported: {Flask.__version__ if hasattr(Flask, '__version__') else 'Yes'}")

# Test Azure connection
print("\n🔌 Testing Azure SQL connection...")
try:
    conn = pymssql.connect(
        server='fseb.database.windows.net',
        database='fseb',
        user='fseb_admin',
        password='Welcome1'
    )
    print("✅ Azure connection successful!")
    
    cursor = conn.cursor()
    cursor.execute('SELECT @@VERSION')
    version = cursor.fetchone()[0]
    print(f"SQL Version: {version[:50]}...")
    
    # List tables
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"Tables found: {len(tables)}")
    for table in tables:
        print(f"  - {table}")
    
    conn.close()
    print("\n🎉 All tests passed! Ready to run Flask app.")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\n💡 Make sure:")
    print("1. Password is correct: Welcome1")
    print("2. Azure firewall allows your IP")
    print("3. Server name is correct: fseb.database.windows.net")
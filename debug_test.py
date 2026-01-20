# debug_test.py
import sys
import os
import platform

print("=" * 60)
print("DEBUG TEST - AZURE SQL CONNECTION")
print("=" * 60)

print(f"Python: {sys.version}")
print(f"Platform: {platform.system()}")
print(f"Current dir: {os.getcwd()}")
print(f"Files in dir: {os.listdir('.')[:10]}")

# Try to import pymssql
try:
    import pymssql
    print(f"✅ pymssql imported (version might not have __version__)")
except ImportError as e:
    print(f"❌ pymssql import failed: {e}")

# Try to import Flask
try:
    from flask import Flask
    print("✅ Flask imported")
except ImportError as e:
    print(f"❌ Flask import failed: {e}")

# Test Azure connection directly
print("\n" + "=" * 60)
print("TESTING AZURE CONNECTION...")
print("=" * 60)

# Set password directly
AZURE_PASSWORD = "Welcome1"  # Your password

try:
    import pymssql
    conn = pymssql.connect(
        server='fseb.database.windows.net',
        database='fseb',
        user='fseb_admin',
        password=AZURE_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute('SELECT @@VERSION')
    version = cursor.fetchone()[0]
    print(f"✅ AZURE CONNECTION SUCCESSFUL!")
    print(f"   SQL Server: {version[:80]}")
    conn.close()
    
    # Also test listing tables
    conn = pymssql.connect(
        server='fseb.database.windows.net',
        database='fseb',
        user='fseb_admin',
        password=AZURE_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute("""
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE'
    """)
    tables = cursor.fetchall()
    print(f"   Tables found: {len(tables)}")
    for table in tables:
        print(f"     - {table[0]}")
    conn.close()
    
except Exception as e:
    print(f"❌ AZURE CONNECTION FAILED: {e}")
    print("\nTroubleshooting:")
    print("1. Check password: Welcome1")
    print("2. Check server: fseb.database.windows.net")
    print("3. Check firewall rules in Azure Portal")

print("\n" + "=" * 60)
print("DEBUG COMPLETE")
print("=" * 60)
input("Press Enter to exit...")
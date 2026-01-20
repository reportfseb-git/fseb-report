#!/usr/bin/env python3

#test_pythonanywhere.py - Run this on PythonAnywhere
import os
import sys

print("PythonAnywhere Connection Test")
print("=" * 50)

#Check environment variables
required_vars = ['AZURE_PASSWORD']
missing_vars = []

for var in required_vars:
    if var not in os.environ:
        missing_vars.append(var)

if missing_vars:
    print("âŒ Missing environment variables:")
for var in missing_vars:
    print(f" - {var}")
print("\nðŸ’¡ Set them with:")
print(" export AZURE_PASSWORD='Welcome1'")
print(" Or set in Web app configuration")
sys.exit(1)

#Test pymssql
try:
    import pymssql
    print("âœ… pymssql imported")
except ImportError:
    print("âŒ pymssql not installed")
    print(" Install with: pip install pymssql")
    sys.exit(1)

#Test connection
try:
    conn = pymssql.connect(
    server=os.environ.get('AZURE_SERVER', 'fseb.database.windows.net'),
    database=os.environ.get('AZURE_DATABASE', 'fseb'),
    user=os.environ.get('AZURE_USERNAME', 'fseb_admin'),
    password=os.environ.get('AZURE_PASSWORD', '')
    )

#text
    cursor = conn.cursor()
    cursor.execute('SELECT @@VERSION')
    version = cursor.fetchone()[0]

    print("âœ… Azure SQL Connection Successful!")
    print(f"   Server: fseb.database.windows.net")
    print(f"   Version: {version[:60]}...")

# List tables
    cursor.execute("""
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE'
    """)
    tables = cursor.fetchall()

    print(f"   Tables found: {len(tables)}")
    for table in tables[:5]:  # Show first 5
        print(f"     - {table[0]}")
    if len(tables) > 5:
        print(f"     ... and {len(tables) - 5} more")

    conn.close()
except Exception as e:
    print(f"âŒ Connection failed: {e}")
    print("\nðŸ’¡ Check:")
    print("1. Azure firewall allows PythonAnywhere IP")
    print("2. Password is correct")
    print("3. Server name is correct")

    print("\n" + "=" * 50)
    print("Test complete!")

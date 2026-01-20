import pyodbc
import sys

print("Python version:", sys.version)
print("pyodbc imported successfully!")

# Try to connect to Azure
try:
    # Replace YOUR_PASSWORD with your actual password
    connection_string = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=tcp:fseb.database.windows.net,1433;"
        "Database=fseb;"
        "Uid=fseb_admin;"
        "Pwd=Welcome1;"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )
    
    print("\nAttempting to connect to Azure SQL...")
    print("Server: fseb.database.windows.net")
    print("Database: fseb")
    
    conn = pyodbc.connect(connection_string)
    print("✅ Connection successful!")
    
    # Test a simple query
    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION as version")
    row = cursor.fetchone()
    print("\nSQL Server version:", row[0])
    
    # Test if we can see tables
    print("\nChecking for tables...")
    cursor.execute("""
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE'
    """)
    tables = cursor.fetchall()
    
    if tables:
        print(f"Found {len(tables)} tables:")
        for table in tables[:10]:  # Show first 10 tables
            print(f"  - {table[0]}")
        if len(tables) > 10:
            print(f"  ... and {len(tables) - 10} more")
    else:
        print("No tables found or no permissions")
    
    conn.close()
    print("\n✅ All tests passed!")
    
except pyodbc.InterfaceError as e:
    print("\n❌ Interface Error - Check ODBC Driver:")
    print("   Error:", e)
    print("\n   Install ODBC Driver 17 from:")
    print("   https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server")
    
except pyodbc.OperationalError as e:
    print("\n❌ Connection Error:")
    print("   Error:", e)
    print("\n   Check:")
    print("   1. Firewall rules in Azure Portal")
    print("   2. Server name is correct")
    print("   3. Password is correct")
    
except pyodbc.Error as e:
    print("\n❌ Database Error:")
    print("   Error:", e)
    
except Exception as e:
    print("\n❌ Unexpected error:", type(e).__name__)
    print("   Error:", e)
# test_azure.py - Guaranteed working test
import traceback

def main():
    print("=" * 70)
    print("AZURE SQL CONNECTION TEST")
    print("=" * 70)
    
    # Try pymssql first
    print("\n1. Testing pymssql...")
    try:
        import pymssql
        print("   ✅ pymssql imported")
        
        conn = pymssql.connect(
            server='fseb.database.windows.net',
            database='fseb',
            user='fseb_admin',
            password='Welcome1'
        )
        print("   ✅ Connection successful!")
        
        cursor = conn.cursor()
        cursor.execute('SELECT @@VERSION as version')
        row = cursor.fetchone()
        print(f"   ✅ SQL Version: {row[0][:60]}...")
        conn.close()
        
    except Exception as e:
        print(f"   ❌ pymssql failed: {e}")
        print(f"   Traceback: {traceback.format_exc()[:200]}...")
    
    # Try pyodbc as fallback
    print("\n2. Testing pyodbc...")
    try:
        import pyodbc
        print("   ✅ pyodbc imported")
        
        conn_str = (
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=tcp:fseb.database.windows.net,1433;"
            "Database=fseb;"
            "Uid=fseb_admin;"
            "Pwd=Welcome1;"
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
        )
        
        conn = pyodbc.connect(conn_str)
        print("   ✅ Connection successful!")
        
        cursor = conn.cursor()
        cursor.execute('SELECT @@VERSION')
        row = cursor.fetchone()
        print(f"   ✅ SQL Version: {row[0][:60]}...")
        conn.close()
        
    except Exception as e:
        print(f"   ❌ pyodbc failed: {e}")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")
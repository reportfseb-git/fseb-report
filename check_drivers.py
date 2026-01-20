import pyodbc

print("Available ODBC Drivers:")
print("-" * 40)

try:
    drivers = pyodbc.drivers()
    if drivers:
        for driver in drivers:
            print(f"• {driver}")
    else:
        print("No ODBC drivers found!")
except Exception as e:
    print(f"Error checking drivers: {e}")
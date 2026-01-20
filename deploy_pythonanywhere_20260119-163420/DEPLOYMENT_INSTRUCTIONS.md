# PYTHONANYWHERE DEPLOYMENT INSTRUCTIONS
# ======================================

## 1. UPLOAD FILES
1. Log in to PythonAnywhere
2. Go to Files tab
3. Upload all files from this folder to: /home/{username}/fseb_report/

## 2. SET UP VIRTUAL ENVIRONMENT (Optional)
```bash
cd ~/fseb_report
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. CONFIGURE WEB APP
Go to Web tab

Click "Add a new web app"

Choose "Manual configuration" (Python 3.10 recommended)

Click on the WSGI configuration file link

Replace content with wsgi_configuration.py content

4. SET ENVIRONMENT VARIABLES
In Web app configuration page, add:

AZURE_SERVER = fseb.database.windows.net

AZURE_DATABASE = fseb

AZURE_USERNAME = fseb_admin

AZURE_PASSWORD = Welcome1

SECRET_KEY = pythonanywhere-secret-key-123

5. CONFIGURE AZURE FIREWALL
Go to Azure Portal

Find your SQL Server

Go to Firewall settings

Add PythonAnywhere server IP:

Run on PythonAnywhere bash: curl ifconfig.me

Add that IP to Azure firewall

6. TEST CONNECTION
On PythonAnywhere bash console:

bash
cd ~/fseb_report
python3 -c "
import pymssql
try:
    conn = pymssql.connect(
        server='fseb.database.windows.net',
        database='fseb',
        user='fseb_admin',
        password='Welcome1'
    )
    print('âœ… Azure connection successful!')
    conn.close()
except Exception as e:
    print(f'âŒ Error: {e}')
"
7. RELOAD WEB APP
Go to Web tab

Click the green Reload button

Visit: https://{username}.pythonanywhere.com

TROUBLESHOOTING
Check error logs: /var/log/{username}.pythonanywhere.com.error.log

Test connection from bash console

Verify Azure firewall rules

Check environment variables are set

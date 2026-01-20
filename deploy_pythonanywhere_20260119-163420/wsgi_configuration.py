# /var/www/{username}_pythonanywhere_com_wsgi.py
# This file should be placed in your PythonAnywhere WSGI configuration

import sys
import os

# Add your app directory to path
path = '/home/{username}/fseb_report'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
# IMPORTANT: Set these in PythonAnywhere Web app config instead of here for security
# os.environ['AZURE_PASSWORD'] = 'Welcome1'
# os.environ['SECRET_KEY'] = 'your-secret-key'

# Import Flask app
from app_azure_fixed import app as application

print("Azure SQL Flask App loaded successfully!")

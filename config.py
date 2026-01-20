# config.py
import os

class Config:
    AZURE_SERVER = os.environ.get('AZURE_SERVER', 'fseb.database.windows.net')
    AZURE_DATABASE = os.environ.get('AZURE_DATABASE', 'fseb')
    AZURE_USERNAME = os.environ.get('AZURE_USERNAME', 'fseb_admin')
    AZURE_PASSWORD = os.environ.get('AZURE_PASSWORD', 'Welcome1')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'pythonanywhere-secret-key-123')
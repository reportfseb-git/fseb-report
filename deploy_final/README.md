# Python Flask Deployment

## Quick Start

1. **Local Development:**
   `ash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   python app.py
Deployment Options:

PythonAnywhere (Free Tier)
Upload this folder

Create virtual environment

Configure WSGI file

Set environment variables

Railway.app (Free Credits)
Push to GitHub

Connect to Railway

Add environment variables

Auto-deploy

Render.com (Free Tier)
Push to GitHub

Create Web Service

Set start command: gunicorn app:app

Environment Variables
Create .env file with:

SECRET_KEY: Random secret for Flask sessions

DEPLOY_TIME: Deployment timestamp

Features
 Flask REST API

 SQLite database

 Mobile responsive

 Ready for production

 Easy to switch to Azure SQL


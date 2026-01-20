# PythonAnywhere Deployment Guide

## Prerequisites
1. Working Azure SQL Database: fseb.database.windows.net
2. PythonAnywhere free account
3. Your app files ready

## Step 1: Prepare Azure Firewall
1. Go to Azure Portal → SQL Server → Firewall settings
2. Add PythonAnywhere IP (run `curl ifconfig.me` on PythonAnywhere)
3. OR temporarily allow all IPs: 0.0.0.0 to 255.255.255.255

## Step 2: Upload Files to PythonAnywhere
1. Log in to PythonAnywhere
2. Go to Files tab
3. Upload:
   - app_azure_fixed.py
   - requirements.txt
   - Any templates/static folders

## Step 3: Install Dependencies
Open Bash console and run:
```bash
cd ~/fseb_report
pip install --user -r requirements.txt
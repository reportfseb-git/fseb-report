# Python Azure SQL App - Deployment

## Quick Deploy

### PythonAnywhere:
1. Upload this folder
2. Create virtual environment
3. Install requirements: pip install -r requirements.txt
4. Configure WSGI file
5. Set environment variables in .env

### Railway.app:
1. Push to GitHub
2. Connect to Railway
3. Add DATABASE_URL environment variable
4. Auto-deploy

## Environment Variables:
- DATABASE_URL=mssql+pymssql://username:password@server/database
- SECRET_KEY=your-secret-key

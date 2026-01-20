from app import app, db
from sqlalchemy import text

print('Initializing database...')
with app.app_context():
    try:
        db.create_all()
        print(' Database tables created')
        
        # Test connection (SQLAlchemy 2.0 compatible)
        try:
            db.session.execute(text('SELECT 1'))
            print(' Database connection successful')
            print(f'Database URL: {app.config["SQLALCHEMY_DATABASE_URI"]}')
        except Exception as e:
            print(f' Database connection issue: {e}')
            print('Tip: Use SQLite by changing DATABASE_URL in .env to: sqlite:///app.db')
    except Exception as e:
        print(f' Error: {e}')

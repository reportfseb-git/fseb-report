import sys
import os

# Add the app directory to the Python path
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.insert(0, path)

from app import app as application

# Optional: Import for initialization
if __name__ == "__main__":
    application.run()

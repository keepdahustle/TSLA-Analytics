"""WSGI entry point untuk Vercel deployment"""
import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import the Dash app from app.py
from app import app

# The WSGI app that Vercel expects
application = app.server

# For debugging
if __name__ == "__main__":
    application.run(debug=False)

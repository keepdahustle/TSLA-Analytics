"""WSGI entry point untuk Vercel deployment"""
import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import the Dash app from app.py
from app import app as dash_app

# Export the WSGI application
# Vercel expects: api.wsgi:app (module.variable_name:app)
app = dash_app.server

if __name__ == "__main__":
    app.run(debug=False)


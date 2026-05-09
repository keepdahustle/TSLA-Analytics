"""Entry point untuk Vercel Serverless Function"""
from api.handler import app

# Vercel expects the app to be exported as 'app'
# For local development: python -m flask --app api.handler run
# For Vercel deployment: handler is automatically called

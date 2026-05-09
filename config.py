"""Configuration untuk deployment Vercel dengan PostgreSQL"""
import os
from urllib.parse import urlparse

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/tesla_stock")

# Parse database URL
if DATABASE_URL:
    db_config = urlparse(DATABASE_URL)
    DB_CONFIG = {
        "host": db_config.hostname or "localhost",
        "port": db_config.port or 5432,
        "database": db_config.path.lstrip("/") or "tesla_stock",
        "user": db_config.username or "postgres",
        "password": db_config.password or "password"
    }
else:
    DB_CONFIG = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", 5432)),
        "database": os.getenv("DB_NAME", "tesla_stock"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "password")
    }

# Flask Configuration
FLASK_ENV = os.getenv("FLASK_ENV", "production")
DEBUG = FLASK_ENV == "development"

# Connection Pool Settings
POOL_SIZE = 5
MAX_OVERFLOW = 10
POOL_TIMEOUT = 30
POOL_RECYCLE = 3600
